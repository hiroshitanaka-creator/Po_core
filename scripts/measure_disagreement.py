#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""M4 — Disagreement visibility measurement script (supporting metric).

Checks whether each C-FULL trace shows evidence of multi-perspective
divergence, using the proxy defined in evaluation_plan.md:

    has_visible_disagreement(result) = True
        if len(options) >= 2
        AND (len(ethics.tradeoffs) > 0 OR recommendation.counter != "")

Primary question: what % of full-mode traces show visible disagreement?
Pass threshold: ≥ 70% of non-trivial prompts (M4).

Usage
-----
    python scripts/measure_disagreement.py [OPTIONS]

Options
-------
    --condition     COND     Condition: full | no_ethics | single_responder
    --prompts       RANGE    Prompt range (default: P01-P20)
    --output        PATH     Write JSON results
    --scenarios-dir PATH     Override scenarios directory

Exit codes
----------
    0  Disagreement visibility rate ≥ 70%
    1  Rate below threshold
    2  Setup error
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
RESULTS_DIR = REPO_ROOT / "docs" / "research_reset" / "results"
M4_THRESHOLD = 0.70

PROMPT_MAP: dict[str, str] = {
    "P01": "case_001", "P02": "case_002", "P03": "case_003",
    "P04": "case_004", "P05": "case_005", "P06": "case_006",
    "P07": "case_007", "P08": "case_008", "P09": "case_009",
    "P10": "case_010", "P11": "case_011", "P12": "case_012",
    "P13": "case_016", "P14": "case_017", "P15": "case_018",
    "P16": "case_019", "P17": "case_020", "P18": "case_021",
    "P19": "case_022", "P20": "case_023",
}


# ── Proxy function (from evaluation_plan.md §4 M4) ───────────────────────────

def has_visible_disagreement(result: dict[str, Any]) -> bool:
    """Return True if trace shows evidence of multi-perspective divergence."""
    options = result.get("options", [])
    tradeoffs = result.get("ethics", {}).get("tradeoffs", [])
    counter = result.get("recommendation", {}).get("counter", "")
    return len(options) >= 2 and (len(tradeoffs) > 0 or bool(counter))


def disagreement_details(result: dict[str, Any]) -> dict[str, Any]:
    """Return structured detail for disagreement analysis."""
    options = result.get("options", [])
    tradeoffs = result.get("ethics", {}).get("tradeoffs", [])
    counter = result.get("recommendation", {}).get("counter", "")
    return {
        "option_count": len(options),
        "tradeoff_count": len(tradeoffs),
        "has_counter": bool(counter),
        "visible": has_visible_disagreement(result),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_scenario(case_prefix: str, scenarios_dir: pathlib.Path) -> dict[str, Any]:
    matches = sorted(scenarios_dir.glob(f"{case_prefix}*.yaml"))
    if not matches:
        raise FileNotFoundError(f"Not found: {scenarios_dir}/{case_prefix}*.yaml")
    with matches[0].open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run_condition(case: dict[str, Any], condition: str) -> dict[str, Any]:
    from po_core.app.composer import StubComposer
    result = StubComposer(seed=42).compose(case)
    if condition == "single_responder" and "trace" in result:
        result["trace"]["_condition"] = "single_responder"
    return result


def parse_prompt_range(spec: str) -> list[str]:
    if "-" in spec and "," not in spec:
        parts = spec.split("-")
        if len(parts) == 2:
            start = int(parts[0].lstrip("P"))
            end = int(parts[1].lstrip("P"))
            return [f"P{i:02d}" for i in range(start, end + 1)]
    return [p.strip() for p in spec.split(",")]


# ── Main ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="M4 Disagreement visibility measurement")
    parser.add_argument("--condition", default="full",
                        choices=["full", "no_ethics", "single_responder"])
    parser.add_argument("--prompts", default="P01-P20")
    parser.add_argument("--output", type=pathlib.Path,
                        default=RESULTS_DIR / "m4_disagreement.json")
    parser.add_argument("--scenarios-dir", type=pathlib.Path, default=SCENARIOS_DIR)
    args = parser.parse_args(argv)

    prompt_ids = [p for p in parse_prompt_range(args.prompts) if p in PROMPT_MAP]
    if not prompt_ids:
        print("ERROR: no valid prompts", file=sys.stderr)
        return 2

    print(f"M4 Disagreement | condition={args.condition} | prompts={len(prompt_ids)}")
    print("-" * 70)

    details: list[dict[str, Any]] = []
    visible_count = 0
    skipped = 0

    for pid in prompt_ids:
        prefix = PROMPT_MAP[pid]
        try:
            case = load_scenario(prefix, args.scenarios_dir)
            result = run_condition(case, args.condition)
            d = disagreement_details(result)
            if d["visible"]:
                visible_count += 1
            details.append({"prompt_id": pid, "case_prefix": prefix,
                            "status": "OK", **d})
            flag = "✓" if d["visible"] else "✗"
            print(f"  {pid} ({prefix}): {flag}  "
                  f"opts={d['option_count']} "
                  f"tradeoffs={d['tradeoff_count']} "
                  f"counter={d['has_counter']}")
        except FileNotFoundError as e:
            skipped += 1
            details.append({"prompt_id": pid, "case_prefix": prefix,
                            "status": "SKIP", "reason": str(e), "visible": False})
            print(f"  {pid} ({prefix}): SKIP")
        except Exception as e:
            skipped += 1
            details.append({"prompt_id": pid, "case_prefix": prefix,
                            "status": "ERROR", "reason": str(e), "visible": False})
            print(f"  {pid} ({prefix}): ERROR — {e}")

    evaluated = len(prompt_ids) - skipped
    rate = visible_count / evaluated if evaluated > 0 else 0.0

    print("-" * 70)
    print(f"Disagreement visible: {visible_count}/{evaluated} (rate={rate:.2%}, threshold={M4_THRESHOLD:.0%})")
    passed = rate >= M4_THRESHOLD
    print(f"M4 RESULT ({args.condition}): {'PASS' if passed else 'FAIL'}")

    output_data = {
        "metric": "M4_disagreement",
        "condition": args.condition,
        "prompts_evaluated": evaluated,
        "prompts_skipped": skipped,
        "visible_count": visible_count,
        "visibility_rate": round(rate, 4),
        "threshold": M4_THRESHOLD,
        "passed": passed,
        "details": details,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(output_data, fh, ensure_ascii=False, indent=2)
    print(f"Results written to: {args.output}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
