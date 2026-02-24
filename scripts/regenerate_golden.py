#!/usr/bin/env python3
"""Regenerate scenario golden JSON files deterministically and safely."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pocore.runner import run_case_file

SCENARIOS_DIR = ROOT / "scenarios"
FROZEN_CASES = {"case_001", "case_009"}


def _expected_path(case_name: str) -> Path:
    return SCENARIOS_DIR / f"{case_name}_expected.json"


def _yaml_path(case_name: str) -> Path:
    return SCENARIOS_DIR / f"{case_name}.yaml"


def _discover_cases() -> list[str]:
    return sorted(p.stem for p in SCENARIOS_DIR.glob("case_*.yaml"))


def _normalize_case_name(raw: str) -> str:
    case = raw.strip()
    if case.endswith(".yaml"):
        case = case[:-5]
    if case.endswith("_expected.json"):
        case = case[: -len("_expected.json")]
    return case


def _load_expected(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _json_dump(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _diff_lines(old: str, new: str, *, name: str) -> list[str]:
    return list(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"expected/{name}",
            tofile=f"actual/{name}",
            n=3,
        )
    )


def _iter_target_cases(cases: Iterable[str] | None, use_all: bool) -> list[str]:
    if use_all:
        return _discover_cases()
    requested = [_normalize_case_name(c) for c in (cases or [])]
    if not requested:
        raise SystemExit("No cases provided. Use --case CASE or --all.")
    return sorted(dict.fromkeys(requested))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate *_expected.json files using run_case_file with fixed deterministic parameters."
        )
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        help="Target case name (e.g. case_001, case_001.yaml, case_001_expected.json). Repeatable.",
    )
    parser.add_argument("--all", action="store_true", help="Target all scenarios/case_*.yaml.")
    parser.add_argument("--seed", type=int, default=0, help="Deterministic seed (default: 0).")
    parser.add_argument(
        "--now",
        default="2026-02-22T00:00:00Z",
        help="Injected timestamp used by deterministic pipeline.",
    )
    parser.add_argument(
        "--deterministic",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Deterministic mode for run_case_file (default: true).",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually overwrite *_expected.json when diffs are detected.",
    )
    parser.add_argument(
        "--allow-frozen",
        action="store_true",
        help="Allow writing frozen cases (case_001/case_009).",
    )
    args = parser.parse_args()

    cases = _iter_target_cases(args.cases, args.all)
    changed_cases: list[str] = []

    for case_name in cases:
        yaml_path = _yaml_path(case_name)
        expected_path = _expected_path(case_name)

        if not yaml_path.exists():
            print(f"[ERROR] Missing scenario YAML: {yaml_path.relative_to(ROOT)}", file=sys.stderr)
            return 2

        actual = run_case_file(
            yaml_path,
            seed=args.seed,
            now=args.now,
            deterministic=args.deterministic,
        )
        actual_text = _json_dump(actual)

        prev = _load_expected(expected_path)
        prev_text = "" if prev is None else _json_dump(prev)
        diffs = _diff_lines(prev_text, actual_text, name=expected_path.name)

        if not diffs:
            print(f"[OK] {case_name}: no changes")
            continue

        changed_cases.append(case_name)
        print(f"[DIFF] {case_name}: {len(diffs)} diff lines")
        for line in diffs[:120]:
            print(line, end="")
        if len(diffs) > 120:
            print("... (diff truncated)")

        if not args.write:
            print(f"[SKIP] {case_name}: not written (use --write)")
            continue

        if case_name in FROZEN_CASES and not args.allow_frozen:
            print(
                f"[SKIP] {case_name}: frozen guard active (use --allow-frozen with --write)",
                file=sys.stderr,
            )
            continue

        expected_path.write_text(actual_text, encoding="utf-8")
        print(f"[WRITE] {expected_path.relative_to(ROOT)}")

    if changed_cases and not args.write:
        print(
            "\nDetected differences but did not write files. Re-run with --write to apply.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
