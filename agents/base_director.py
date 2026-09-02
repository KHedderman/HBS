"""Shared base class for every specialized Director (spoke).

Strict communication rule: a Director's `handle()` method receives only
(task, context) from the Chief of Staff and returns a DirectorOutput back to
the Chief of Staff. Directors must never import or call one another —
that boundary is enforced by convention here and by code review, since
Python can't easily forbid cross-imports at runtime without heavy tooling.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from agents.llm_provider import ModelRouter, PaidTierRequiredError


@dataclass
class DirectorOutput:
    director_id: str
    title: str
    summary: str
    body: str
    requires_hitl: Optional[str] = None  # checkpoint id, if this output must be gated
    metadata: dict[str, Any] = field(default_factory=dict)
    stubbed: bool = False
    namesake: Optional[str] = None  # e.g. "Doriot" — see config.yaml's naming_convention


class BaseDirector:
    director_id: str = "base"
    title: str = "Base Director"
    namesake: Optional[str] = None  # real Harvard/HBS namesake, or None (see config.yaml)
    model_ref: str = "anthropic_pro.chat"
    system_prompt: str = "You are a specialized director. Be concise and actionable."

    def __init__(self, router: Optional[ModelRouter] = None):
        self.router = router or ModelRouter()

    def handle(self, task: str, context: str = "") -> DirectorOutput:
        """Default synchronous handler: builds a domain system prompt, calls
        the governed model router, and returns polished output. Subclasses
        override `handle()` when they need multi-step logic (e.g. PRD
        generation, accessibility audits) but should still route every
        model call through `self._complete()`.
        """
        try:
            result = self._complete(task, context)
        except PaidTierRequiredError as exc:
            return DirectorOutput(
                director_id=self.director_id,
                title=self.title,
                summary="Paused — requires cost governance decision.",
                body=str(exc),
                requires_hitl="cost_bearing_action",
                namesake=self.namesake,
            )

        return DirectorOutput(
            director_id=self.director_id,
            title=self.title,
            summary=self._summarize(result.text),
            body=result.text,
            stubbed=result.stubbed,
            metadata={"provider": result.provider, "model": result.model},
            namesake=self.namesake,
        )

    def _complete(self, task: str, context: str):
        prompt = f"CONTEXT FROM MEMORY CURATOR:\n{context}\n\nTASK:\n{task}"
        return self.router.complete(self.model_ref, self.system_prompt, prompt)

    @staticmethod
    def _summarize(text: str, limit: int = 160) -> str:
        one_line = " ".join(text.strip().split())
        return one_line[:limit] + ("…" if len(one_line) > limit else "")
