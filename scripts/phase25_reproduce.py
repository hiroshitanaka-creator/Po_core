#!/usr/bin/env python3
"""Phase 25 reproducibility runner.

One-command entry point for external verification / full validation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import List

EXTERNAL_COMMANDS: List[List[str]] = [
    ["pytest", "-q", "tests/test_input_schema.py"],
    ["pytest", "-q", "tests/test_output_schema.py"],
    ["pytest", "-q", "tests/test_golden_e2e.py"],
    ["pytest", "-q", "tests/test_traceability.py"],
]


def build_commands(profile: str) -> List[List[str]]:
    if profile == "external":
        return EXTERNAL_COMMANDS
    if profile == "full":
        return EXTERNAL_COMMANDS + [["pytest", "-q"]]
    raise ValueError(f"unsupported profile: {profile}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run reproducibility checks for Phase 25"
    )
    parser.add_argument(
        "--profile",
        choices=["external", "full"],
        default="external",
        help="Command set to run (default: external)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them",
    )
    args = parser.parse_args()

    commands = build_commands(args.profile)
    for command in commands:
        printable = " ".join(command)
        print(f"[phase25] {printable}")
        if args.dry_run:
            continue
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            print(
                f"[phase25] failed: {printable} (exit={completed.returncode})",
                file=sys.stderr,
            )
            return completed.returncode

    print(f"[phase25] profile={args.profile} completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
