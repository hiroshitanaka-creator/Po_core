#!/usr/bin/env python3
"""Regenerate golden expected JSON files from scenario YAML deterministically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pocore.runner import run_case_file


def regenerate(yaml_path: Path, *, seed: int, now: str, deterministic: bool) -> Path:
    output = run_case_file(yaml_path, seed=seed, now=now, deterministic=deterministic)
    expected_path = yaml_path.with_name(f"{yaml_path.stem}_expected.json")
    expected_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return expected_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", nargs="+", type=Path, help="Path(s) to scenario yaml files")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--now", default="2026-02-22T00:00:00Z")
    parser.add_argument("--deterministic", action="store_true", default=True)
    args = parser.parse_args()

    for case_path in args.cases:
        regenerated = regenerate(
            case_path,
            seed=args.seed,
            now=args.now,
            deterministic=args.deterministic,
        )
        print(f"regenerated: {regenerated}")


if __name__ == "__main__":
    main()
