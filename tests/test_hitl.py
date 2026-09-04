import json

from agents.hitl import HITLGate


def _gate_writing_to(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: (_ for _ in ()).throw(AssertionError("must not prompt")))
    gate = HITLGate(non_interactive=True)
    # Redirect off the real, tracked qa_logs/hitl_decision_log.jsonl so
    # tests never write into the actual repo log.
    gate.log_path = tmp_path / "hitl_decision_log.jsonl"
    return gate


def test_require_approval_fail_safe_denies_and_logs(tmp_path, monkeypatch):
    gate = _gate_writing_to(tmp_path, monkeypatch)

    approved = gate.require_approval("pedagogical_review", "Facilitation deck for Module 3")

    assert approved is False
    lines = gate.log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["checkpoint"] == "pedagogical_review"
    assert record["approved"] is False
    assert record["mode"] == "non_interactive"
    assert "timestamp" in record


def test_present_cost_choice_fail_safe_flags_and_logs(tmp_path, monkeypatch):
    gate = _gate_writing_to(tmp_path, monkeypatch)

    choice = gate.present_cost_choice("elevenlabs paid tier", "Free quota exceeded")

    assert choice == "flag_for_manual_upgrade"
    record = json.loads(gate.log_path.read_text(encoding="utf-8").strip())
    assert record["checkpoint"] == "cost_bearing_action"
    assert record["choice"] == "flag_for_manual_upgrade"
