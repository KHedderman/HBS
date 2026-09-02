#!/usr/bin/env python3
"""HBS AI Institute — Multi-Agent Content Command Center
CLI entrypoint. This is the only interface you talk to directly — everything
downstream (routing, Directors, memory, HITL, sync) is orchestrated for you.

Usage:
    python main.py "Draft a LinkedIn post about our new AI course launch"
    python main.py --status                 # generate a downloadable status file
    python main.py                          # interactive REPL
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

from agents.chief_of_staff import ChiefOfStaff
from pipelines.status_report import generate as generate_status_report


def main() -> None:
    load_dotenv()
    chief_of_staff = ChiefOfStaff()

    args = sys.argv[1:]

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
