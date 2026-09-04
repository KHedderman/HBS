"""Every JSONL log's documented schema, actually enforced. Each test pairs
a valid record (the exact shape that file's README/docstring documents)
with an invalid one, so a schema that silently accepts garbage fails here
first."""
import pytest
from pydantic import ValidationError

from agents.schemas import (
    AppConfig,
    CostChoiceRecord,
    DirectorConfig,
    HITLCheckpointRecord,
    MemoryEntry,
    MetricEntry,
    RoutingLogEntry,
)


def test_memory_entry_accepts_documented_shape():
    entry = MemoryEntry(
        timestamp="2026-09-04T12:00:00Z",
        request="Draft an executive briefing",
        response="Full synthesized response",
        directors_invoked=["market_intelligence"],
        tags=["briefing"],
    )
    assert entry.directors_invoked == ["market_intelligence"]


def test_memory_entry_rejects_empty_request():
    with pytest.raises(ValidationError):
        MemoryEntry(timestamp="2026-09-04T12:00:00Z", request="", response="something")


def test_hitl_checkpoint_record_valid():
    rec = HITLCheckpointRecord(
        checkpoint="pedagogical_review",
        description="Facilitation deck for Module 3",
        approved=True,
        mode="interactive_chat",
        timestamp="2026-09-04T12:00:00Z",
    )
    assert rec.approved is True


def test_hitl_checkpoint_record_rejects_missing_description():
    with pytest.raises(ValidationError):
        HITLCheckpointRecord(
            checkpoint="pedagogical_review",
            approved=True,
            mode="interactive_chat",
            timestamp="2026-09-04T12:00:00Z",
        )


def test_cost_choice_record_valid():
    rec = CostChoiceRecord(
        requested_model="elevenlabs paid tier",
        reason="Free quota would be exceeded",
        choice="flag_for_manual_upgrade",
        timestamp="2026-09-04T12:00:00Z",
    )
    assert rec.checkpoint == "cost_bearing_action"


def test_cost_choice_record_rejects_invalid_choice():
    with pytest.raises(ValidationError):
        CostChoiceRecord(
            requested_model="elevenlabs paid tier",
            reason="Free quota would be exceeded",
            choice="just spend the money",
            timestamp="2026-09-04T12:00:00Z",
        )


def test_routing_log_entry_valid():
    entry = RoutingLogEntry(
        timestamp="2026-09-04T12:00:00Z",
        request="Draft a facilitation deck for Module 3",
        directors_invoked=["donham", "copeland"],
    )
    assert len(entry.directors_invoked) == 2


def test_metric_entry_accepts_numeric_and_string_value():
    numeric = MetricEntry(
        timestamp="2026-09-04T12:00:00Z",
        program="Deciding Where to Deploy AI",
        metric="session_satisfaction",
        value=4.6,
        source="Post-session survey",
    )
    assert numeric.value == 4.6

    stringy = MetricEntry(
        timestamp="2026-09-04T12:00:00Z",
        program="Deciding Where to Deploy AI",
        metric="completion_rate",
        value="18/20",
        source="Program roster",
    )
    assert stringy.value == "18/20"


def test_metric_entry_rejects_empty_program():
    with pytest.raises(ValidationError):
        MetricEntry(
            timestamp="2026-09-04T12:00:00Z",
            program="",
            metric="session_satisfaction",
            value=4.6,
            source="Post-session survey",
        )


def test_director_config_rejects_malformed_model_ref():
    with pytest.raises(ValidationError):
        DirectorConfig(id="doriot", title="Director of Market Intelligence", model="not-a-valid-ref")


def test_director_config_allows_undeclared_extra_fields():
    # config.yaml's real directors carry lots of extra prose fields
    # (namesake_note, expansion_note, tools, ...) — the schema must not
    # reject a real record just because it isn't exhaustively modeled.
    d = DirectorConfig(
        id="donham",
        title="Director of Pedagogical Synthesis",
        model="anthropic_pro.chat",
        namesake="Wallace Donham",
        domains=["curriculum design"],
        frameworks=["ADDIE", "SAM"],
        expansion_note="Expanded 2026-09-03...",
    )
    assert d.id == "donham"


def test_app_config_validates_real_config_yaml():
    import yaml
    from agents.config_loader import CONFIG_PATH

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    # Should not raise — this is the actual, current config.yaml.
    AppConfig.model_validate(raw)


def test_app_config_rejects_duplicate_director_ids():
    with pytest.raises(ValidationError):
        AppConfig.model_validate(
            {
                "agents": {
                    "chief_of_staff": {"namesake": "Eliot", "role": "Chief of Staff", "model": "anthropic_pro.reasoning"},
                    "memory_curator": {"namesake": "Winsor", "role": "Memory Curator", "model": "anthropic_pro.fast"},
                    "directors": [
                        {"id": "doriot", "title": "A", "model": "anthropic_pro.chat", "domains": []},
                        {"id": "doriot", "title": "B", "model": "anthropic_pro.chat", "domains": []},
                    ],
                },
                "logging": {
                    "qa_logs_dir": "qa_logs",
                    "routing_log": "qa_logs/routing_log.jsonl",
                    "hitl_decision_log": "qa_logs/hitl_decision_log.jsonl",
                    "outputs_dir": "outputs",
                },
            }
        )
