"""Generates a downloadable status file mapping current progress across all
active initiatives. The Chief of Staff calls `generate()` on request and
returns the resulting path to the user.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

from pipelines.pipeline_tracker import PipelineTracker

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"


def generate(tracker: PipelineTracker | None = None) -> Path:
    tracker = tracker or PipelineTracker()
    records = tracker.snapshot()

    timestamp = dt.datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUTS_DIR / f"status_report_{timestamp}.md"

    lines = [
        "# HBS AI Institute — Pipeline Status Report",
        f"_Generated {dt.datetime.utcnow().isoformat()}Z_",
        "",
    ]

    if not records:
        lines.append(
            "_No Airtable records available (either the pipeline is empty, "
            "or AIRTABLE_API_KEY / AIRTABLE_BASE_ID are not configured yet)._"
        )
    else:
        lines.append("| Initiative | Director | Owner | Status | Due Date | Notes |")
        lines.append("|---|---|---|---|---|---|")
        for rec in records:
            f = rec.get("fields", {})
            lines.append(
                f"| {f.get('Initiative','')} | {f.get('Director','')} | "
                f"{f.get('Owner','')} | {f.get('Status','')} | "
                f"{f.get('Due Date','')} | {f.get('Notes','')} |"
            )

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
