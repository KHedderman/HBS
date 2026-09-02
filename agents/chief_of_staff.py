"""Eliot — the Chief of Staff & Intelligent Router (Hub).

Namesake: Charles William Eliot, Harvard's longest-serving president
(1869-1909), who built the coordinating structure that let Harvard's
separate schools function as one university. Same job here: one executive
view across every Director underneath it. See config.yaml's
`naming_convention` for the full scheme (hub roles get University-wide
namesakes; Directors get HBS-specific ones).

Flow for every request:
    1. Query the Memory Curator for relevant prior context.
    2. Classify the request against each Director's declared domain
       keywords (a lightweight, dependency-free router; swap `_route()`
       for an LLM-based classifier once you want nuance beyond keywords —
       nothing else changes).
    3. Dispatch to the matched Directors IN PARALLEL. Directors never see
       each other's output at this stage.
    4. Collect outputs; any output flagged `requires_hitl` is gated before
       it's allowed into the final synthesis.
    5. Synthesize all approved Director outputs into one unified response.
    6. Hand the exchange back to the Memory Curator to curate + sync.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from agents.base_director import DirectorOutput
from agents.directors import REGISTRY
from agents.hitl import HITLGate
from agents.llm_provider import ModelRouter
from agents.memory_curator import MemoryCurator


class ChiefOfStaff:
    namesake = "Eliot"

    def __init__(self, non_interactive: bool = False):
        self.router = ModelRouter()
        self.memory = MemoryCurator()
        self.hitl = HITLGate(non_interactive=non_interactive)
        self.directors = {director_id: cls(self.router) for director_id, cls in REGISTRY.items()}

    # -- Intelligent Router --------------------------------------------------
    def _route(self, request: str) -> list[str]:
        """Keyword-overlap classifier: scores every Director by how many of
        its declared keywords appear in the request, returns every Director
        scoring > 0. Falls back to `project_management` (general operations
        triage) when nothing matches, so no request is silently dropped.
        """
        text = request.lower()
        scored = []
        for director_id, director in self.directors.items():
            score = sum(1 for kw in getattr(director, "keywords", []) if kw in text)
            if score > 0:
                scored.append((score, director_id))

        if not scored:
            return ["project_management"]

        scored.sort(reverse=True)
        return [director_id for _, director_id in scored]

    # -- Parallel dispatch ----------------------------------------------------
    def _dispatch(self, request: str, director_ids: list[str], context: str) -> list[DirectorOutput]:
        outputs: list[DirectorOutput] = []
        with ThreadPoolExecutor(max_workers=max(1, len(director_ids))) as pool:
            futures = {
                pool.submit(self.directors[d].handle, request, context): d for d in director_ids
            }
            for future in as_completed(futures):
                outputs.append(future.result())
        return outputs

    # -- HITL gating ----------------------------------------------------------
    def _gate(self, outputs: list[DirectorOutput]) -> list[DirectorOutput]:
        approved = []
        for output in outputs:
            if output.requires_hitl is None:
                approved.append(output)
                continue

            if output.requires_hitl == "cost_bearing_action":
                choice = self.hitl.present_cost_choice(
                    requested_model=output.metadata.get("model", "unknown"),
                    reason=output.body,
                )
                if choice == "keep_free_path":
                    approved.append(output)
                else:
                    output.body += "\n\n[Flagged for manual upgrade — not executed.]"
                    approved.append(output)
                continue

            description = f"{output.title}: {output.summary}"
            if self.hitl.require_approval(output.requires_hitl, description):
                approved.append(output)
            else:
                output.body = "[Held pending human approval — not included in final synthesis.]"
                approved.append(output)
        return approved

    # -- Synthesis --------------------------------------------------------------
    def _synthesize(self, request: str, outputs: list[DirectorOutput]) -> str:
        sections = [f"# Eliot — Chief of Staff Synthesis\n\n**Request:** {request}\n"]
        for output in outputs:
            flag = " ⚠️ _(stubbed — no API key configured)_" if output.stubbed else ""
            sections.append(f"## {output.title}{flag}\n{output.body}\n")
        return "\n".join(sections)

    # -- Public entrypoint --------------------------------------------------------
    def handle_request(self, request: str) -> str:
        context = self.memory.recall(request)
        director_ids = self._route(request)
        raw_outputs = self._dispatch(request, director_ids, context)
        approved_outputs = self._gate(raw_outputs)
        synthesized = self._synthesize(request, approved_outputs)

        self.memory.remember(
            request=request,
            synthesized_response=synthesized,
            directors_invoked=director_ids,
        )
        return synthesized
