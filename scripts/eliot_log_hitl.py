#!/usr/bin/env python3
"""Lets Eliot write a real entry into the HITL decision log from inside an
actual Claude Code session — the same gap `scripts/eliot_remember.py`
closes for memory.

`agents/hitl.py`'s `HITLGate` is built for a CLI with a human at a stdin
prompt (`input("Approve? [y/N]: ")`) — nothing like that runs when Kaitlyn
approves or denies a checkpoint directly in a Claude Code chat message.
Without this script, `qa_logs/hitl_decision_log.jsonl` (declared in
config.yaml's `logging` block) never gets written, so Winsor's
`governance_digest()` always reads an empty log even after real HITL
checkpoints were actually enforced in conversation.

This script reuses `HITLGate`'s own `_log()` — same schema, same file path
read from config.yaml — just called directly with the real decision
already made in chat, instead of re-prompting on stdin.

Usage — a standing checkpoint (strategic_approval, pedagogical_review,
external_publish, or a routine check):
    python scripts/eliot_log_hitl.py checkpoint \
        --checkpoint pedagogical_review \
        --description "Facilitation deck for Module 3, approved by Kaitlyn in chat" \
        --approved yes

Usage — the cost-governance choice:
    python scripts/eliot_log_hitl.py cost_choice \
        --requested-model "elevenlabs paid tier" \
        --reason "Free character quota would be exceeded for this voiceover" \
        --choice keep_free_path
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.hitl import HITLGate  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="kind", required=True)

    checkpoint_parser = sub.add_parser("checkpoint", help="Log a standing HITL checkpoint decision")
    checkpoint_parser.add_argument("--checkpoint", required=True, help="e.g. strategic_approval, pedagogical_review, external_publish")
    checkpoint_parser.add_argument("--description", required=True)
    checkpoint_parser.add_argument("--approved", required=True, choices=["yes", "no"])

    cost_parser = sub.add_parser("cost_choice", help="Log a cost-governance checkpoint decision")
    cost_parser.add_argument("--requested-model", required=True, dest="requested_model")
    cost_parser.add_argument("--reason", required=True)
    cost_parser.add_argument("--choice", required=True, choices=["keep_free_path", "flag_for_manual_upgrade"])

    args = parser.parse_args()
    gate = HITLGate()

    if args.kind == "checkpoint":
        gate._log(
            {
                "checkpoint": args.checkpoint,
                "description": args.description,
                "approved": args.approved == "yes",
                "mode": "interactive_chat",
            }
        )
        print(f"Logged {args.checkpoint} -> approved={args.approved == 'yes'} in {gate.log_path}")
    else:
        gate._log(
            {
                "checkpoint": "cost_bearing_action",
                "requested_model": args.requested_model,
                "reason": args.reason,
                "choice": args.choice,
            }
        )
        print(f"Logged cost_bearing_action -> {args.choice} in {gate.log_path}")


if __name__ == "__main__":
    main()
