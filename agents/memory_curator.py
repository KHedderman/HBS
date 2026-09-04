"""Winsor — the Memory Curator, persistent context AND governance/reporting
engine (Core Pillar).

Namesake: Justin Winsor, Harvard's University Librarian (1877-1897) and a
founding figure of American librarianship, who built the systems for
organizing and preserving the university's collective knowledge. Same job
here, and — like the Chief of Staff's Eliot — a University-wide namesake
rather than an HBS-specific one, since this role serves every Director.

Runs alongside the Chief of Staff, not underneath it: every routing
decision consults `recall()` first, and every completed exchange is handed
to `remember()`, which curates it into structured long-term storage and
syncs it out to GitHub and Notion.

Winsor's charter is deliberately broader than passive logging — paperwork,
notes, governance, AND reporting, not just storage. (This mirrors a pattern
AI advisor Allie K. Miller describes in her own hub-and-spoke agent system:
a Chief of Staff paired with an assistant who owns governance and reporting,
since orchestration plus documentation — not agent count — is what actually
makes a multi-agent system work.) Concretely, that means Winsor also reads
back across the HITL decision log and produces a standing `governance_digest()`
— what's pending, what's been approved or denied, and what needs follow-up —
rather than leaving that record purely as an unread audit trail.

Storage layout:
    memory/session_logs/<date>.jsonl   — raw, timestamped turn-by-turn log
    memory/long_term/knowledge_base.jsonl — curated, deduplicated entries
                                             (what recall() searches)
    qa_logs/hitl_decision_log.jsonl    — HITLGate's raw approval/denial log
                                          (what governance_digest() reads)
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from agents.config_loader import load_config
from agents.schemas import MemoryEntry
from database_sync import github_sync, notion_sync

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_LOG_DIR = REPO_ROOT / "memory" / "session_logs"
LONG_TERM_PATH = REPO_ROOT / "memory" / "long_term" / "knowledge_base.jsonl"


class MemoryCurator:
    namesake = "Winsor"

    def __init__(self):
        SESSION_LOG_DIR.mkdir(parents=True, exist_ok=True)
        LONG_TERM_PATH.parent.mkdir(parents=True, exist_ok=True)
        LONG_TERM_PATH.touch(exist_ok=True)
        cfg = load_config()
        self.hitl_log_path = REPO_ROOT / cfg["logging"]["hitl_decision_log"]

    # -- write path -----------------------------------------------------
    def remember(
        self,
        request: str,
        synthesized_response: str,
        directors_invoked: list[str],
        tags: list[str] | None = None,
    ) -> dict:
        """Curates one Chief-of-Staff exchange into long-term memory and
        syncs it to GitHub + Notion. Always writes the raw session log
        locally regardless of sync outcomes.
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"
        # Validated, not just constructed: a malformed entry (empty request,
        # wrong type for directors_invoked, ...) fails here, loudly, before
        # it ever reaches disk — not silently inside recall() weeks later.
        entry = MemoryEntry(
            timestamp=timestamp,
            request=request,
            response=synthesized_response,
            directors_invoked=directors_invoked,
            tags=tags or [],
        )
        record = entry.model_dump()

        self._append_session_log(record)
        self._append_long_term(record)

        github_status = github_sync.push_memory_file(
            "memory/long_term/knowledge_base.jsonl",
            LONG_TERM_PATH.read_text(encoding="utf-8"),
            commit_message=f"memory: curate entry {timestamp}",
        )
        notion_status = notion_sync.log_memory_entry(
            title=self._title_for(request),
            summary=synthesized_response,
            tags=tags,
        )

        return {"github": github_status, "notion": notion_status}

    def ingest_external_transcript(self, record: dict) -> dict:
        """Curates a transcript from an external source (currently: Granola
        meeting notes, via database_sync.granola_sync.normalize_transcript)
        into the same long-term store as a normal exchange, and syncs it out.

        `record` is expected to carry: source, title, date, transcript —
        see granola_sync.normalize_transcript() for the exact shape.
        """
        return self.remember(
            request=f"[{record['source']} meeting: {record['title']} ({record['date']})]",
            synthesized_response=record["transcript"],
            directors_invoked=["pedagogical_synthesis"],
            tags=[record["source"], "meeting_transcript"],
        )

    def _append_session_log(self, record: dict) -> None:
        today = dt.date.today().isoformat()
        path = SESSION_LOG_DIR / f"{today}.jsonl"
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def _append_long_term(self, record: dict) -> None:
        with open(LONG_TERM_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    @staticmethod
    def _title_for(request: str) -> str:
        one_line = " ".join(request.strip().split())
        return one_line[:80] + ("…" if len(one_line) > 80 else "")

    # -- governance & reporting --------------------------------------------
    def governance_digest(self, recent_limit: int = 5) -> str:
        """Winsor's standing report: reads HITLGate's raw decision log and
        the curated memory store, and turns them into one readable digest —
        pending/approved/denied checkpoint counts, the most recent decisions,
        and the most recent activity. This is the "documentation is the
        actual unlock" piece: a synthesized report, not just an audit trail
        nobody re-reads.
        """
        decisions: list[dict[str, Any]] = []
        if self.hitl_log_path.exists():
            with open(self.hitl_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        decisions.append(json.loads(line))

        approved = [d for d in decisions if d.get("approved") is True]
        denied = [d for d in decisions if d.get("approved") is False]
        cost_flags = [d for d in decisions if d.get("checkpoint") == "cost_bearing_action"]

        recent_activity: list[dict[str, Any]] = []
        if LONG_TERM_PATH.exists():
            with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
                recent_activity = [json.loads(line) for line in f if line.strip()]
        recent_activity = recent_activity[-recent_limit:]

        lines = [
            f"# Governance Digest — {dt.date.today().isoformat()}",
            "",
            "## HITL checkpoints",
            f"- Approved: {len(approved)}",
            f"- Denied (fail-safe or explicit): {len(denied)}",
            f"- Cost-bearing flags raised: {len(cost_flags)}",
        ]
        if decisions:
            lines.append("")
            lines.append("### Most recent decisions")
            for d in decisions[-recent_limit:][::-1]:
                if d.get("checkpoint") == "cost_bearing_action":
                    status = f"💸 {d.get('choice', '?')}"
                else:
                    status = "✅ approved" if d.get("approved") else "⛔ denied"
                lines.append(f"- [{d.get('timestamp', '?')}] {d.get('checkpoint', '?')} — {status}")
        else:
            lines.append("- No HITL checkpoints logged yet.")

        lines.append("")
        lines.append("## Recent activity")
        if recent_activity:
            for r in reversed(recent_activity):
                lines.append(
                    f"- [{r['timestamp']}] {r['request'][:100]} "
                    f"(directors: {', '.join(r.get('directors_invoked', [])) or 'none'})"
                )
        else:
            lines.append("- No activity recorded yet.")

        return "\n".join(lines)

    def publish_governance_digest(self) -> dict:
        """Winsor's reporting duty made concrete: pushes the current digest
        out to Notion as a real page, the same free-tier sync path
        `remember()` already uses — so governance reporting is an actual
        artifact stakeholders can read, not just something the workforce
        could theoretically generate.
        """
        digest = self.governance_digest()
        return notion_sync.log_memory_entry(
            title=f"Governance Digest — {dt.date.today().isoformat()}",
            summary=digest,
            tags=["governance_digest"],
        )

    # -- read path --------------------------------------------------------
    def recall(self, query: str, limit: int = 5) -> str:
        """Naive keyword-overlap retrieval over the curated long-term store.
        This is intentionally simple and dependency-free; swap in an
        embeddings-backed retriever here once you've decided on a vector
        store, without touching any caller.
        """
        if not LONG_TERM_PATH.exists():
            return "(no memory yet)"

        query_terms = set(query.lower().split())
        scored: list[tuple[int, dict[str, Any]]] = []

        with open(LONG_TERM_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                haystack = (record.get("request", "") + " " + record.get("response", "")).lower()
                score = sum(1 for term in query_terms if term in haystack)
                if score > 0:
                    scored.append((score, record))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        top = scored[:limit]
        if not top:
            return "(no relevant memory found)"

        lines = []
        for score, record in top:
            lines.append(f"- [{record['timestamp']}] {record['request']} -> {record['response'][:200]}")
        return "\n".join(lines)
