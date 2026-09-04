import json

import agents.memory_curator as memory_curator_module
from agents.memory_curator import MemoryCurator


def _isolated_curator(tmp_path, monkeypatch):
    """Points every path MemoryCurator touches at tmp_path, and stubs out
    both external syncs, so this test never writes into the real repo's
    memory/ files and never makes a real GitHub/Notion call."""
    session_dir = tmp_path / "session_logs"
    long_term_path = tmp_path / "long_term" / "knowledge_base.jsonl"
    monkeypatch.setattr(memory_curator_module, "SESSION_LOG_DIR", session_dir)
    monkeypatch.setattr(memory_curator_module, "LONG_TERM_PATH", long_term_path)
    monkeypatch.setattr(
        memory_curator_module.github_sync, "push_memory_file",
        lambda *a, **kw: {"status": "stubbed_for_test"},
    )
    monkeypatch.setattr(
        memory_curator_module.notion_sync, "log_memory_entry",
        lambda *a, **kw: {"status": "stubbed_for_test"},
    )
    curator = MemoryCurator()
    return curator, session_dir, long_term_path


def test_remember_writes_one_schema_valid_line_to_both_logs(tmp_path, monkeypatch):
    curator, session_dir, long_term_path = _isolated_curator(tmp_path, monkeypatch)

    curator.remember(
        request="Draft an executive briefing",
        synthesized_response="Full synthesized response text",
        directors_invoked=["market_intelligence"],
        tags=["briefing"],
    )

    long_term_lines = long_term_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(long_term_lines) == 1
    record = json.loads(long_term_lines[0])
    assert record["request"] == "Draft an executive briefing"
    assert record["directors_invoked"] == ["market_intelligence"]

    session_files = list(session_dir.glob("*.jsonl"))
    assert len(session_files) == 1
    assert json.loads(session_files[0].read_text(encoding="utf-8").strip())["tags"] == ["briefing"]


def test_remember_rejects_empty_request(tmp_path, monkeypatch):
    import pytest
    from pydantic import ValidationError

    curator, _, _ = _isolated_curator(tmp_path, monkeypatch)
    with pytest.raises(ValidationError):
        curator.remember(request="", synthesized_response="something", directors_invoked=[])


def test_recall_finds_entry_by_keyword_after_remember(tmp_path, monkeypatch):
    curator, _, _ = _isolated_curator(tmp_path, monkeypatch)
    curator.remember(
        request="Track new agentic AI product launches",
        synthesized_response="Three launches this week worth executive attention.",
        directors_invoked=["market_intelligence"],
    )

    result = curator.recall("agentic launches")
    assert "Track new agentic AI product launches" in result


def test_recall_with_no_memory_yet_says_so(tmp_path, monkeypatch):
    curator, _, long_term_path = _isolated_curator(tmp_path, monkeypatch)
    assert long_term_path.exists()  # __init__ touches it
    assert curator.recall("anything") == "(no relevant memory found)"
