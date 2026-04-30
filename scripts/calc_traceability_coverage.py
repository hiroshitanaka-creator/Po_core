#!/usr/bin/env python3
"""Calculate acceptance golden coverage from traceability matrix.

Usage:
  python scripts/calc_traceability_coverage.py
  python scripts/calc_traceability_coverage.py --min-at 8 --format json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRACEABILITY_PATH = ROOT / "docs" / "traceability" / "traceability_v1.yaml"
ACCEPTANCE_GOLDEN_DIR = ROOT / "tests" / "acceptance" / "scenarios"
AT_PATTERN = re.compile(r"AT-\d{3}")


def _collect_traceability_at_ids(traceability: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for requirement in traceability.get("requirements", []):
        for test_ref in requirement.get("tests", []):
            found.update(AT_PATTERN.findall(str(test_ref)))
    return found


def _collect_golden_at_ids(golden_dir: Path) -> set[str]:
    at_ids: set[str] = set()
    for path in sorted(golden_dir.glob("at_*_expected.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        at_id = payload.get("at_id")
        if isinstance(at_id, str) and AT_PATTERN.fullmatch(at_id):
            at_ids.add(at_id)
    return at_ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-at", type=int, default=8)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    traceability = yaml.safe_load(TRACEABILITY_PATH.read_text(encoding="utf-8"))
    traceability_at_ids = _collect_traceability_at_ids(traceability)
    golden_at_ids = _collect_golden_at_ids(ACCEPTANCE_GOLDEN_DIR)

    covered = sorted(traceability_at_ids & golden_at_ids)
    uncovered = sorted(traceability_at_ids - golden_at_ids)

    report = {
        "traceability_path": str(TRACEABILITY_PATH.relative_to(ROOT)),
        "golden_dir": str(ACCEPTANCE_GOLDEN_DIR.relative_to(ROOT)),
        "traceability_at_ids": sorted(traceability_at_ids),
        "golden_at_ids": sorted(golden_at_ids),
        "covered_at_ids": covered,
        "uncovered_at_ids": uncovered,
        "covered_count": len(covered),
        "required_min_at": args.min_at,
        "threshold_passed": len(covered) >= args.min_at,
    }

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Traceability Matrix: {report['traceability_path']}")
        print(f"Acceptance golden dir: {report['golden_dir']}")
        print(f"Covered AT IDs ({len(covered)}): {', '.join(covered) or '(none)'}")
        print(
            f"Uncovered AT IDs ({len(uncovered)}): {', '.join(uncovered) or '(none)'}"
        )
        print(
            f"Threshold: covered_count >= {args.min_at} -> {'PASS' if report['threshold_passed'] else 'FAIL'}"
        )

    return 0 if report["threshold_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
