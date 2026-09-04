#!/usr/bin/env python3
"""Lets Eliot (via Henderson) write a real, schema-validated entry into
`metrics/learning_metrics.jsonl` from inside an actual Claude Code session.

`metrics/README.md` documents this file's schema but, until now, its only
write path was "hand Henderson the raw number and ask it to append a
properly-formed line, or edit this file directly" — no actual writer
existed, so nothing enforced the documented shape. This script is that
writer: same schema (`agents.schemas.MetricEntry`), validated before every
append, so a malformed entry fails loudly instead of silently corrupting
the one instrument Henderson actually reads from.

Usage:
    python scripts/eliot_log_metric.py \
        --program "Deciding Where to Deploy AI in Your Function" \
        --metric session_satisfaction \
        --value 4.6 \
        --source "Post-session survey" \
        --notes "n=18 VPs, first live run"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.schemas import MetricEntry  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
METRICS_PATH = REPO_ROOT / "metrics" / "learning_metrics.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--program", required=True, help="Program or session name this data point belongs to")
    parser.add_argument("--metric", required=True, help="e.g. session_satisfaction, completion_rate — see metrics/README.md")
    parser.add_argument("--value", required=True, help="The measured value — a number or a short string")
    parser.add_argument("--source", required=True, help="Where this number came from, e.g. 'Post-session survey'")
    parser.add_argument("--notes", default=None, help="Optional context (sample size, caveats)")
    args = parser.parse_args()

    value: float | str
    try:
        value = float(args.value)
    except ValueError:
        value = args.value

    entry = MetricEntry(
        timestamp=dt.datetime.utcnow().isoformat() + "Z",
        program=args.program,
        metric=args.metric,
        value=value,
        source=args.source,
        notes=args.notes,
    )

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump()) + "\n")

    print(f"Logged {args.metric}={value!r} for {args.program!r} in {METRICS_PATH}")


if __name__ == "__main__":
    main()
