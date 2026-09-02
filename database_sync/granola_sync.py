"""Granola sync adapter — connector-only, no unattended path.

Granola (the AI meeting notepad) has no public REST API for personal
accounts, so unlike github_sync/notion_sync/airtable_sync this module does
NOT make outbound HTTP calls itself. There is nothing here for main.py's
standalone/unattended mode to call.

The real flow only exists in interactive mode:
    1. In a live Claude Code chat with the Granola connector connected,
       Claude calls the Granola MCP tools directly (e.g. list_meetings /
       get_meeting_transcript) to fetch a transcript.
    2. Claude hands that transcript text to `normalize_transcript()` below
       to shape it into the record MemoryCurator expects.
    3. Claude calls `MemoryCurator.ingest_external_transcript(...)` with
       that record so it's curated and synced like any other memory entry.

This module exists so that shaping step has one canonical, testable place
instead of being ad-hoc per conversation.
"""
from __future__ import annotations

import datetime as dt


def normalize_transcript(meeting_title: str, transcript_text: str, meeting_date: str | None = None) -> dict:
    """Shapes a raw Granola transcript into the dict MemoryCurator's
    ingest_external_transcript() expects. Pure function — no network calls,
    no connector dependency — so it's usable/testable without Granola
    connected.
    """
    return {
        "source": "granola",
        "title": meeting_title,
        "date": meeting_date or dt.date.today().isoformat(),
        "transcript": transcript_text,
    }
