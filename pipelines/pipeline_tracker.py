"""Pipeline & Activity Tracker.

Logs active initiatives and operational tasks to Airtable. The Chief of
Staff calls `add_initiative()` / `update_status()` whenever a Director's
output represents a trackable piece of work, and `snapshot()` when the user
asks "what's the status of everything" (which feeds status_report.py).
"""
from __future__ import annotations

import datetime as dt

from agents.config_loader import load_config
from database_sync import airtable_sync


class PipelineTracker:
    def add_initiative(
        self,
        initiative: str,
        director: str,
        owner: str = "Kaitlyn Hedderman",
        status: str = "In Progress",
        due_date: str | None = None,
        notes: str = "",
    ) -> dict:
        fields = {
            "Initiative": initiative,
            "Director": director,
            "Owner": owner,
            "Status": status,
            "Notes": notes,
            "Logged At": dt.datetime.utcnow().isoformat() + "Z",
        }
        if due_date:
            fields["Due Date"] = due_date
        return airtable_sync.upsert_pipeline_item(fields)

    def update_status(self, record_id: str, status: str, notes: str = "") -> dict:
        fields = {"Status": status}
        if notes:
            fields["Notes"] = notes
        return airtable_sync.upsert_pipeline_item(fields, record_id=record_id)

    def snapshot(self) -> list[dict]:
        result = airtable_sync.list_active_items()
        return result.get("records", [])

    def queue_unattended_request(self, request: str, director: str = "project_management") -> dict:
        """Logs a request for future unattended execution WITHOUT executing
        anything. This never runs code on its own — it only writes a row so
        the request isn't lost, and reflects config.yaml's operating_mode
        so the status honestly says whether unattended mode is even on.

        Turning unattended mode on is a deliberate, separate act (editing
        config.yaml's operating_mode.unattended.enabled) — this method
        never does that itself.
        """
        cfg = load_config()
        unattended_enabled = cfg.get("operating_mode", {}).get("unattended", {}).get("enabled", False)
        status = (
            "Queued — awaiting unattended mode enablement"
            if not unattended_enabled
            else "Queued — unattended mode enabled, awaiting scheduler"
        )
        return self.add_initiative(
            initiative=request,
            director=director,
            status=status,
            notes="Logged via queue_unattended_request(); no code has executed.",
        )
