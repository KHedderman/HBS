"""Winsor — the Memory Curator, persistent context engine (Core Pillar).

Namesake: Justin Winsor, Harvard's University Librarian (1877-1897) and a
founding figure of American librarianship, who built the systems for
organizing and preserving the university's collective knowledge. Same job
here, and — like the Chief of Staff's Eliot — a University-wide namesake
rather than an HBS-specific one, since this role serves every Director.

Runs alongside the Chief of Staff, not underneath it: every routing
decision consults `recall()` first, and every completed exchange is handed
to `remember()`, which curates it into structured long-term storage and
syncs it out to GitHub and Notion.

Storage layout:
    memory/session_logs/<date>.jsonl   — raw, timestamped turn-by-turn log
    memory/long_term/knowledge_base.jsonl — curated, deduplicated entries
                                             (what recall() searches)
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

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
        record = {
            "timestamp": timestamp,
            "request": request,
            "response": synthesized_response,
            "directors_invoked": directors_invoked,
            "tags": tags or [],
        }

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
