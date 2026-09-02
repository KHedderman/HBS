"""Notion sync adapter — long-term organizational memory, transcripts, and
context logs. Free-tier compatible: Notion's personal integration API has
no metered billing.
"""
from __future__ import annotations

import requests

from agents.config_loader import env

NOTION_VERSION = "2022-06-28"
API_ROOT = "https://api.notion.com/v1"


def _available() -> bool:
    return bool(env("NOTION_API_KEY") and env("NOTION_MEMORY_DATABASE_ID"))


def log_memory_entry(title: str, summary: str, tags: list[str] | None = None) -> dict:
    """Creates a page in the configured Notion database representing one
    curated memory entry (a session summary, a decision, a piece of
    long-term context). No-ops with a clear status when unconfigured.
    """
    if not _available():
        return {"status": "skipped", "reason": "NOTION_API_KEY / NOTION_MEMORY_DATABASE_ID not set"}

    headers = {
        "Authorization": f"Bearer {env('NOTION_API_KEY')}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    payload = {
        "parent": {"database_id": env("NOTION_MEMORY_DATABASE_ID")},
        "properties": {
            "Name": {"title": [{"text": {"content": title[:200]}}]},
            "Tags": {"multi_select": [{"name": t} for t in (tags or [])]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": summary[:2000]}}]},
            }
        ],
    }
    try:
        resp = requests.post(f"{API_ROOT}/pages", headers=headers, json=payload, timeout=15)
        if resp.status_code in (200, 201):
            return {"status": "synced", "page_id": resp.json().get("id")}
        return {"status": "error", "detail": resp.text[:300]}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "detail": str(exc)}
