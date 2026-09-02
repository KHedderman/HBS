"""Airtable sync adapter for the Pipeline & Activity Tracker."""
from __future__ import annotations

import requests

from agents.config_loader import env

API_ROOT = "https://api.airtable.com/v0"


def _available() -> bool:
    return bool(env("AIRTABLE_API_KEY") and env("AIRTABLE_BASE_ID"))


def upsert_pipeline_item(fields: dict, record_id: str | None = None) -> dict:
    """Creates (or updates, if `record_id` is given) a row in the pipeline
    table. Fields typically include: Initiative, Owner, Status, Director,
    Due Date, Notes.
    """
    if not _available():
        return {"status": "skipped", "reason": "AIRTABLE_API_KEY / AIRTABLE_BASE_ID not set"}

    base_id = env("AIRTABLE_BASE_ID")
    table = env("AIRTABLE_PIPELINE_TABLE", "Pipeline")
    headers = {
        "Authorization": f"Bearer {env('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json",
    }
    url = f"{API_ROOT}/{base_id}/{table}"

    try:
        if record_id:
            resp = requests.patch(f"{url}/{record_id}", headers=headers, json={"fields": fields}, timeout=15)
        else:
            resp = requests.post(url, headers=headers, json={"fields": fields}, timeout=15)
        if resp.status_code in (200, 201):
            return {"status": "synced", "record": resp.json()}
        return {"status": "error", "detail": resp.text[:300]}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "detail": str(exc)}


def list_active_items() -> dict:
    if not _available():
        return {"status": "skipped", "reason": "AIRTABLE_API_KEY / AIRTABLE_BASE_ID not set", "records": []}

    base_id = env("AIRTABLE_BASE_ID")
    table = env("AIRTABLE_PIPELINE_TABLE", "Pipeline")
    headers = {"Authorization": f"Bearer {env('AIRTABLE_API_KEY')}"}
    try:
        resp = requests.get(f"{API_ROOT}/{base_id}/{table}", headers=headers, timeout=15)
        if resp.status_code == 200:
            return {"status": "ok", "records": resp.json().get("records", [])}
        return {"status": "error", "detail": resp.text[:300], "records": []}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "detail": str(exc), "records": []}
