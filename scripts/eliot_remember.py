#!/usr/bin/env python3
"""Lets Eliot write a real entry into Winsor's memory store from inside an
actual Claude Code session.

Why this exists: `agents/chief_of_staff.py`'s `ChiefOfStaff.handle_request()`
already calls `MemoryCurator.remember()` after every exchange — but that
orchestrator is a standalone Python entry point, and it is not what runs
when Kaitlyn talks to the "eliot" subagent inside Claude Code (see
`.claude/agents/eliot.md`). Without this script, that real memory/governance
system sits unused and every exchange's context dies at the session
boundary. This script is the bridge: the same `MemoryCurator.remember()`
call, invoked directly, so real Claude Code sessions actually populate
`memory/session_logs/`, `memory/long_term/knowledge_base.jsonl` (which
Winsor's `recall()` and `governance_digest()` read), and Notion, if
configured.

Usage:
    python scripts/eliot_remember.py \
        --request "What Kaitlyn asked, or a short label for the decision" \
        --response "What Eliot synthesized, or the rule/decision being kept" \
        --directors doriot,donham \
        --tags rule_change,interview_prep

`--directors` and `--tags` are optional, comma-separated. After this
script runs, Winsor's `_commit_local` fallback (see
`database_sync/github_sync.py`) stages and commits
`memory/long_term/knowledge_base.jsonl` locally when no `GITHUB_TOKEN` /
`GITHUB_REPO` are configured — Eliot still needs to `git push` for that
commit to actually reach GitHub and survive a session boundary.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.memory_curator import MemoryCurator  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, help="Kaitlyn's request, or a short label for the decision being persisted")
    parser.add_argument("--response", required=True, help="Eliot's synthesized response, or the rule/decision text being kept")
    parser.add_argument("--directors", default="", help="Comma-separated Director IDs actually engaged, e.g. doriot,donham")
    parser.add_argument("--tags", default="", help="Comma-separated tags, e.g. rule_change,interview_prep")
    args = parser.parse_args()

    directors = [d.strip() for d in args.directors.split(",") if d.strip()]
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    curator = MemoryCurator()
    result = curator.remember(
        request=args.request,
        synthesized_response=args.response,
        directors_invoked=directors,
        tags=tags,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
