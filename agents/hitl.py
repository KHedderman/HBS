"""Human-in-the-Loop checkpoint enforcement.

Every checkpoint defined in config.yaml's `hitl_checkpoints` funnels through
`require_approval()`. In this CLI bootstrap, "blocking" means prompting on
stdin; when the Command Center is wired into a chat surface (Slack, a web
app, etc.) swap `_prompt()` for that surface's approval mechanism — nothing
else in the system needs to change, since Directors and the Chief of Staff
only ever call `require_approval()` / `present_cost_choice()`.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Literal

from agents.config_loader import load_config

REPO_ROOT = Path(__file__).resolve().parent.parent


class HITLGate:
    def __init__(self, non_interactive: bool = False):
        self.cfg = load_config()
        self.log_path = REPO_ROOT / self.cfg["logging"]["hitl_decision_log"]
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        # non_interactive=True is used by automated/CI contexts: checkpoints
        # auto-deny (fail safe) instead of hanging on input().
        self.non_interactive = non_interactive

    def _log(self, record: dict) -> None:
        record["timestamp"] = dt.datetime.utcnow().isoformat() + "Z"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def require_approval(self, checkpoint_id: str, description: str) -> bool:
        """Blocks (interactively or via fail-safe deny) until the human
        approves or rejects. Returns True only on explicit approval.
        """
        print(f"\n🛑 HITL CHECKPOINT [{checkpoint_id}]")
        print(f"   {description}")

        if self.non_interactive:
            approved = False
            print("   (non-interactive mode: auto-denied, fail-safe)")
        else:
            answer = input("   Approve? [y/N]: ").strip().lower()
            approved = answer in ("y", "yes")

        self._log(
            {
                "checkpoint": checkpoint_id,
                "description": description,
                "approved": approved,
                "mode": "non_interactive" if self.non_interactive else "interactive",
            }
        )
        return approved

    def present_cost_choice(self, requested_model: str, reason: str) -> Literal["keep_free_path", "flag_for_manual_upgrade"]:
        """Implements the mandatory guardrail: when a Director's task would
        exceed the free tier, the human chooses between degrading gracefully
        or flagging the request for a manual, deliberate upgrade. There is
        no silent third option that spends money.
        """
        print(f"\n💸 COST GOVERNANCE CHECKPOINT")
        print(f"   Requested: {requested_model}")
        print(f"   Reason: {reason}")
        print("   1) Keep free/included path (degrade gracefully)")
        print("   2) Flag for manual user upgrade (no spend, logged for follow-up)")

        if self.non_interactive:
            choice = "flag_for_manual_upgrade"
            print("   (non-interactive mode: auto-flagged, no spend)")
        else:
            answer = input("   Choose [1/2]: ").strip()
            choice = "keep_free_path" if answer == "1" else "flag_for_manual_upgrade"

        self._log(
            {
                "checkpoint": "cost_bearing_action",
                "requested_model": requested_model,
                "reason": reason,
                "choice": choice,
            }
        )
        return choice
