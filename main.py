#!/usr/bin/env python3
"""HBS AI Institute — Multi-Agent Content Command Center
CLI entrypoint. This is the only interface you talk to directly — everything
downstream (routing, Directors, memory, HITL, sync) is orchestrated for you.

Usage:
    python main.py "Draft a LinkedIn post about our new AI course launch"
    python main.py --status                 # generate a downloadable status file
    python main.py                          # interactive REPL
    python main.py --unattended "..."       # blocked unless config.yaml explicitly enables it

Operating mode: config.yaml's operating_mode.default is "interactive" — this
CLI still requires a human at the keyboard to answer every HITL prompt on
stdin. True unattended (headless, cron/CI, no human) is a separate, currently
disabled mode. See config.yaml's `operating_mode.unattended` for how to turn
it on when you actually want that.
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

from agents.chief_of_staff import ChiefOfStaff
from agents.config_loader import load_config
from pipelines.status_report import generate as generate_status_report


def main() -> None:
    load_dotenv()

    args = sys.argv[1:]

    if args and args[0] == "--unattended":
        cfg = load_config()
        if not cfg.get("operating_mode", {}).get("unattended", {}).get("enabled", False):
            print(
                "🛑 Unattended mode is disabled in config.yaml "
                "(operating_mode.unattended.enabled: false).\n"
                "This is deliberate — nothing runs headless until you "
                "explicitly flip that flag yourself. Run without --unattended "
                "for the normal, HITL-gated interactive CLI, or edit "
                "config.yaml if you really want this enabled."
            )
            sys.exit(1)
        # Falls through only once a human has deliberately enabled it.
        chief_of_staff = ChiefOfStaff(non_interactive=True)
        request = " ".join(args[1:])
        print(chief_of_staff.handle_request(request))
        return

    chief_of_staff = ChiefOfStaff()

    if args and args[0] == "--status":
        path = generate_status_report()
        print(f"✅ Status report generated: {path}")
        return

    if args:
        request = " ".join(args)
        print(chief_of_staff.handle_request(request))
        return

    print("HBS AI Institute Command Center — talk to your Chief of Staff.")
    print("(type 'exit' to quit, '--status' for a pipeline status report)\n")
    while True:
        try:
            request = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not request:
            continue
        if request.lower() in ("exit", "quit"):
            break
        if request == "--status":
            path = generate_status_report()
            print(f"✅ Status report generated: {path}\n")
            continue
        print()
        print(chief_of_staff.handle_request(request))
        print()


if __name__ == "__main__":
    main()
