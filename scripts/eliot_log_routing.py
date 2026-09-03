#!/usr/bin/env python3
"""Lets Eliot write a real entry into the routing log from inside an actual
Claude Code session.

`config.yaml`'s `logging.routing_log` declares `qa_logs/routing_log.jsonl`,
but nothing in this repo — not `agents/chief_of_staff.py`, not any
Director — ever actually wrote to it. It was a declared path with no
writer. This script is the writer: run it once per real routing decision
(which Director(s) Eliot dispatched a request to) so the log is a genuine
record, not an aspirational one.

Usage:
    python scripts/eliot_log_routing.py \
        --request "Draft a facilitation deck for Module 3" \
        --directors donham,copeland
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.config_loader import load_config  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, help="Kaitlyn's request, verbatim or summarized")
    parser.add_argument("--directors", required=True, help="Comma-separated Director IDs actually dispatched to")
    args = parser.parse_args()

    cfg = load_config()
    log_path = REPO_ROOT / cfg["logging"]["routing_log"]
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": dt.datetime.utcnow().isoformat() + "Z",
        "request": args.request,
        "directors_invoked": [d.strip() for d in args.directors.split(",") if d.strip()],
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f"Logged routing decision -> {record['directors_invoked']} in {log_path}")


if __name__ == "__main__":
    main()
