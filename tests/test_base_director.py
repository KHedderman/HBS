from dataclasses import dataclass

from agents.base_director import BaseDirector, DirectorOutput
from agents.llm_provider import CompletionResult, PaidTierRequiredError


class _FakeRouter:
    """Stands in for ModelRouter so this test exercises BaseDirector's own
    logic (summarizing, HITL gating) without a real model call."""

    def __init__(self, result=None, raises=None):
        self._result = result
        self._raises = raises
        self.calls = []

    def complete(self, model_ref, system_prompt, user_prompt, max_tokens=1024):
        self.calls.append((model_ref, system_prompt, user_prompt))
        if self._raises:
            raise self._raises
        return self._result


def test_handle_happy_path_returns_populated_director_output():
    fake = _FakeRouter(result=CompletionResult(provider="anthropic_pro", model="claude-sonnet-5", text="  Hello   world.  "))
    director = BaseDirector(router=fake)
    director.director_id = "test_director"
    director.title = "Test Director"

    output = director.handle("Do the thing", context="prior context")

    assert isinstance(output, DirectorOutput)
    assert output.director_id == "test_director"
    assert output.body.strip() == "Hello   world."
    assert output.summary == "Hello world."
    assert output.requires_hitl is None
    assert output.stubbed is False
    assert output.metadata == {"provider": "anthropic_pro", "model": "claude-sonnet-5"}
    # BaseDirector must pass context through, not drop it.
    assert "prior context" in fake.calls[0][2]


def test_handle_routes_paid_tier_required_to_hitl_checkpoint():
    fake = _FakeRouter(raises=PaidTierRequiredError("openai.gpt4", "not on the approved list"))
    director = BaseDirector(router=fake)

    output = director.handle("Do an expensive thing")

    assert output.requires_hitl == "cost_bearing_action"
    assert "not on the approved list" in output.body


def test_summarize_truncates_long_text_with_ellipsis():
    long_text = "word " * 100
    summary = BaseDirector._summarize(long_text, limit=20)
    assert len(summary) == 21  # 20 chars + the ellipsis character
    assert summary.endswith("…")


def test_summarize_leaves_short_text_untouched():
    assert BaseDirector._summarize("short answer") == "short answer"
