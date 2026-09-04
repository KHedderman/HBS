import pytest

from agents.llm_provider import ModelRouter, PaidTierRequiredError


def test_resolve_known_ref_returns_provider_and_model():
    router = ModelRouter()
    provider, model = router.resolve("anthropic_pro.chat")
    assert provider == "anthropic_pro"
    assert model  # real model id from config.yaml's approved_free_tier_models


def test_resolve_unapproved_ref_raises_paid_tier_required():
    router = ModelRouter()
    with pytest.raises(PaidTierRequiredError):
        router.resolve("openai.gpt4")


def test_resolve_malformed_ref_raises_paid_tier_required():
    router = ModelRouter()
    with pytest.raises(PaidTierRequiredError):
        router.resolve("not-a-ref-at-all")


def test_complete_without_api_key_returns_labeled_stub(monkeypatch):
    # The whole "runs end-to-end before you've wired a single integration"
    # promise in llm_provider.py's docstring lives or dies on this path.
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    router = ModelRouter()
    result = router.complete("anthropic_pro.chat", "You are a test.", "Say hi.")
    assert result.stubbed is True
    assert "STUBBED RESPONSE" in result.text
    assert result.provider == "anthropic_pro"
