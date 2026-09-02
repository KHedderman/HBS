"""Model router + cost/model governance guardrail.

Every Director asks THIS module for a completion instead of calling a
provider SDK directly. That's what makes the "free tier only" rule
enforceable in one place: if a requested model/provider isn't on the
approved list in config.yaml, we raise PaidTierRequiredError instead of
silently spending money, and the Chief of Staff turns that into a HITL
checkpoint.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from agents.config_loader import load_config, env


class PaidTierRequiredError(Exception):
    """Raised when a task would require a model/tool outside the approved
    free-tier / subscription-included roster. Callers MUST route this to a
    HITL checkpoint (see agents.hitl) rather than catching-and-continuing.
    """

    def __init__(self, requested: str, reason: str):
        self.requested = requested
        self.reason = reason
        super().__init__(f"Paid tier required for '{requested}': {reason}")


@dataclass
class CompletionResult:
    provider: str
    model: str
    text: str
    grounded: bool = False
    stubbed: bool = False


class ModelRouter:
    """Resolves a logical model reference like 'anthropic_pro.chat' against
    config.yaml, verifies it's on the approved free-tier list, and (when a
    key is present) calls the real provider. Without a key, it returns a
    clearly-labeled stub so the rest of the pipeline (routing, synthesis,
    memory, HITL) is fully exercisable offline.
    """

    def __init__(self):
        self.cfg = load_config()
        self.approved = self.cfg["model_governance"]["approved_free_tier_models"]

    def resolve(self, logical_ref: str) -> tuple[str, str]:
        """'anthropic_pro.chat' -> ('anthropic_pro', 'claude-sonnet-5')"""
        provider, _, key = logical_ref.partition(".")
        if not key or provider not in self.approved or key not in self.approved[provider]:
            raise PaidTierRequiredError(
                logical_ref,
                "Model reference is not present in config.yaml's "
                "approved_free_tier_models. Refusing to guess a paid substitute.",
            )
        return provider, self.approved[provider][key]

    def complete(
        self,
        logical_ref: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1024,
    ) -> CompletionResult:
        provider, model = self.resolve(logical_ref)

        if provider == "anthropic_pro":
            return self._call_anthropic(model, system_prompt, user_prompt, max_tokens)
        if provider == "google_ai_studio":
            return self._call_google_ai_studio(model, system_prompt, user_prompt, max_tokens)
        if provider == "perplexity":
            return self._call_perplexity(model, system_prompt, user_prompt, max_tokens)

        raise PaidTierRequiredError(logical_ref, f"No handler wired for provider '{provider}'.")

    # -- provider handlers ---------------------------------------------------
    # Each handler degrades to a stub when its API key isn't configured, so
    # the whole hub-and-spoke pipeline runs end-to-end before you've wired
    # a single integration.

    def _call_anthropic(self, model, system_prompt, user_prompt, max_tokens) -> CompletionResult:
        # NOTE: this is Anthropic's metered, pay-per-token Developer API
        # (console.anthropic.com), a separate paid product from a claude.ai
        # Pro/Max seat — there is no portable API key tied to that
        # subscription. Only set ANTHROPIC_API_KEY if you deliberately want
        # this standalone script to make real, billed calls; leaving it
        # unset returns a clearly-labeled stub and costs nothing.
        api_key = env("ANTHROPIC_API_KEY")
        if not api_key:
            return self._stub("anthropic_pro", model, user_prompt)
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            text = "".join(block.text for block in resp.content if hasattr(block, "text"))
            return CompletionResult("anthropic_pro", model, text)
        except Exception as exc:  # pragma: no cover - network/SDK failures
            return self._stub("anthropic_pro", model, user_prompt, error=str(exc))

    def _call_google_ai_studio(self, model, system_prompt, user_prompt, max_tokens) -> CompletionResult:
        api_key = env("GOOGLE_AI_STUDIO_API_KEY")
        if not api_key:
            return self._stub("google_ai_studio", model, user_prompt)
        try:
            import requests

            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent?key={api_key}"
            )
            payload = {
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
                "generationConfig": {"maxOutputTokens": max_tokens},
            }
            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return CompletionResult("google_ai_studio", model, text)
        except Exception as exc:  # pragma: no cover
            return self._stub("google_ai_studio", model, user_prompt, error=str(exc))

    def _call_perplexity(self, model, system_prompt, user_prompt, max_tokens) -> CompletionResult:
        api_key = env("PERPLEXITY_API_KEY")
        if not api_key:
            return self._stub("perplexity", model, user_prompt)
        try:
            import requests

            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": max_tokens,
                },
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            return CompletionResult("perplexity", model, text, grounded=True)
        except Exception as exc:  # pragma: no cover
            return self._stub("perplexity", model, user_prompt, error=str(exc))

    @staticmethod
    def _stub(provider: str, model: str, user_prompt: str, error: Optional[str] = None) -> CompletionResult:
        note = f" (call failed: {error})" if error else " (no API key configured)"
        text = (
            f"[STUBBED RESPONSE from {provider}/{model}{note}]\n"
            f"This Director would have processed:\n{user_prompt}\n\n"
            f"Add the relevant key to your .env file to get a live response."
        )
        return CompletionResult(provider, model, text, stubbed=True)
