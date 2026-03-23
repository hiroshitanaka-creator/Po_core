#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""M1 — Trace completeness measurement script.

Runs each fixed prompt (P01–P20) under a given condition and computes
the fraction of the 19 required TraceEvent fields that are populated
(non-null, non-empty) per request.

Primary metric: mean(C-FULL completeness) − mean(C-SINGLE completeness) ≥ 0.10

Usage
-----
    python scripts/measure_completeness.py [OPTIONS]

Options
-------
    --condition     COND     Condition: full | no_ethics | single_responder
    --prompts       RANGE    Prompt range (default: P01-P20)
    --output        PATH     Write JSON results (default: docs/research_reset/results/m1_completeness.json)
    --scenarios-dir PATH     Override scenarios directory

Exit codes
----------
    0  Mean completeness above 0.70 (informational threshold)
    1  Mean completeness at or below 0.70
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
COMPLETENESS_INFO_THRESHOLD = 0.70

PROMPT_MAP: dict[str, str] = {
    "P01": "case_001", "P02": "case_002", "P03": "case_003",
    "P04": "case_004", "P05": "case_005", "P06": "case_006",
    "P07": "case_007", "P08": "case_008", "P09": "case_009",
    "P10": "case_010", "P11": "case_011", "P12": "case_012",
    "P13": "case_016", "P14": "case_017", "P15": "case_018",
    "P16": "case_019", "P17": "case_020", "P18": "case_021",
    "P19": "case_022", "P20": "case_023",
}

# ── Required field checklist (19 fields) ─────────────────────────────────────

REQUIRED_TRACE_STEPS = {
    "parse_input", "generate_options", "ethics_review",
    "responsibility_review", "question_layer", "compose_output",
}


def _check_fields(result: dict[str, Any]) -> dict[str, bool]:
    """Return a dict mapping each required field to True (present) / False (absent)."""
    trace = result.get("trace", {})
    steps = trace.get("steps", [])
    step_map = {s.get("name", ""): s for s in steps}
    ethics = result.get("ethics", {})
    rec = result.get("recommendation", {})
    unc = result.get("uncertainty", {})
    options = result.get("options", [])

    def step_summary(name: str) -> bool:
        s = step_map.get(name, {})
        return bool(s.get("summary", ""))

    def step_metrics_key(name: str, key: str) -> bool:
        s = step_map.get(name, {})
        val = s.get("metrics", {}).get(key)
        return bool(val)

    return {
        # trace structure
        "trace.version":                        bool(trace.get("version")),
        "trace.steps_non_empty":                len(steps) >= 6,
        # individual step summaries
        "trace.parse_input.summary":            step_summary("parse_input"),
        "trace.generate_options.summary":       step_summary("generate_options"),
        "trace.ethics_review.summary":          step_summary("ethics_review"),
        "trace.ethics_review.rules_fired":      step_metrics_key("ethics_review", "rules_fired"),
        "trace.responsibility_review.summary":  step_summary("responsibility_review"),
        "trace.question_layer.summary":         step_summary("question_layer"),
        "trace.compose_output.summary":         step_summary("compose_output"),
        "trace.compose_output.arbitration_code":step_metrics_key("compose_output", "arbitration_code"),
        # ethics
        "ethics.principles_used_non_empty":     bool(ethics.get("principles_used")),
        "ethics.tradeoffs_present":             isinstance(ethics.get("tradeoffs"), list),
        # recommendation
        "recommendation.confidence":            rec.get("confidence") in {"low", "medium", "high"},
        # uncertainty
        "uncertainty.overall_level":            unc.get("overall_level") in {"low", "medium", "high"},
        "uncertainty.reasons_non_empty":        bool(unc.get("reasons")),
        # options
        "options_non_empty":                    len(options) >= 1,
        "options.ethics_review_present":        all("ethics_review" in o for o in options) if options else False,
        "options.responsibility_review_present":all("responsibility_review" in o for o in options) if options else False,
        "options.uncertainty_present":          all("uncertainty" in o for o in options) if options else False,
    }


def completeness(result: dict[str, Any]) -> tuple[float, dict[str, bool]]:
    """Return (fraction, field_check_dict) for a result."""
    checks = _check_fields(result)
    score = sum(1 for v in checks.values() if v)
    return score / len(checks), checks


# ── Condition runners ─────────────────────────────────────────────────────────


def run_condition(case: dict[str, Any], condition: str) -> dict[str, Any]:
    from po_core.app.composer import StubComposer
    result = StubComposer(seed=42).compose(case)
    if condition == "single_responder" and "trace" in result:
        result["trace"]["_condition"] = "single_responder"
    return result


# ── Scenario loading ──────────────────────────────────────────────────────────


def load_scenario(case_prefix: str, scenarios_dir: pathlib.Path) -> dict[str, Any]:
    matches = sorted(scenarios_dir.glob(f"{case_prefix}*.yaml"))
    if not matches:
        raise FileNotFoundError(f"Not found: {scenarios_dir}/{case_prefix}*.yaml")
    with matches[0].open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


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
    parser = argparse.ArgumentParser(description="M1 Trace completeness measurement")
    parser.add_argument("--condition", default="full",
                        choices=["full", "no_ethics", "single_responder"])
    parser.add_argument("--prompts", default="P01-P20")
    parser.add_argument("--output", type=pathlib.Path,
                        default=RESULTS_DIR / "m1_completeness.json")
    parser.add_argument("--scenarios-dir", type=pathlib.Path, default=SCENARIOS_DIR)
    args = parser.parse_args(argv)

    prompt_ids = [p for p in parse_prompt_range(args.prompts) if p in PROMPT_MAP]
    if not prompt_ids:
        print("ERROR: no valid prompts", file=sys.stderr)
        return 2

    print(f"M1 Completeness | condition={args.condition} | prompts={len(prompt_ids)}")
    print(f"{'Field count':12} = 19 required fields per prompt")
    print("-" * 70)

    details: list[dict[str, Any]] = []
    scores: list[float] = []
    skipped = 0

    for pid in prompt_ids:
        prefix = PROMPT_MAP[pid]
        try:
            case = load_scenario(prefix, args.scenarios_dir)
            result = run_condition(case, args.condition)
            score, checks = completeness(result)
            scores.append(score)
            missing = [k for k, v in checks.items() if not v]
            details.append({
                "prompt_id": pid, "case_prefix": prefix,
                "status": "OK", "completeness": round(score, 4),
                "fields_present": sum(checks.values()),
                "fields_total": len(checks),
                "missing_fields": missing,
            })
            flag = "✓" if score >= 0.80 else ("△" if score >= 0.60 else "✗")
            print(f"  {pid} ({prefix}): {score:.2%} {flag}"
                  + (f"  missing={missing}" if missing else ""))
        except FileNotFoundError as e:
            skipped += 1
            details.append({"prompt_id": pid, "case_prefix": prefix,
                            "status": "SKIP", "reason": str(e)})
            print(f"  {pid} ({prefix}): SKIP")
        except Exception as e:
            skipped += 1
            details.append({"prompt_id": pid, "case_prefix": prefix,
                            "status": "ERROR", "reason": str(e)})
            print(f"  {pid} ({prefix}): ERROR — {e}")

    evaluated = len(prompt_ids) - skipped
    mean_score = sum(scores) / len(scores) if scores else 0.0

    print("-" * 70)
    print(f"Mean completeness: {mean_score:.2%} over {evaluated} prompts")
    passed = mean_score >= COMPLETENESS_INFO_THRESHOLD
    print(f"M1 RESULT ({args.condition}): {'PASS' if passed else 'NOTE'} "
          f"(threshold={COMPLETENESS_INFO_THRESHOLD:.0%})")
    print("NOTE: M1 primary threshold is delta(full − single_responder) ≥ 0.10")
    print("      Run both conditions and compare via run_evaluation.py")

    output_data = {
        "metric": "M1_completeness",
        "condition": args.condition,
        "prompts_evaluated": evaluated,
        "prompts_skipped": skipped,
        "mean_completeness": round(mean_score, 4),
        "info_threshold": COMPLETENESS_INFO_THRESHOLD,
        "passed_info_threshold": passed,
        "details": details,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(output_data, fh, ensure_ascii=False, indent=2)
    print(f"Results written to: {args.output}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
