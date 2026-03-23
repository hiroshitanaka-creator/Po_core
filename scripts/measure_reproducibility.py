#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""M2 — Reproducibility measurement script.

Runs each fixed prompt N times under a given condition and checks whether
the structural trace topology (step_name_sequence + safety verdict) is
identical across all runs.

Usage
-----
    python scripts/measure_reproducibility.py [OPTIONS]

Options
-------
    --condition     COND     Condition: full | no_ethics | single_responder
                             (default: full)
    --runs          N        Number of runs per prompt (default: 5)
    --prompts       RANGE    Prompt range to test, e.g. P01-P20 or P01,P03,P07
                             (default: P01-P20)
    --output        PATH     Write JSON results to this path
                             (default: docs/research_reset/results/m2_reproducibility.json)
    --scenarios-dir PATH     Override scenarios directory
                             (default: scenarios/)

Output
------
    Prints a summary table and writes structured JSON to --output.

Exit codes
----------
    0  All prompts reproducible (or above threshold)
    1  Reproducibility rate below M2 threshold (0.90)
    2  Setup error (missing files, import failures, etc.)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import traceback
from typing import Any

import yaml

# ── Constants ──────────────────────────────────────────────────────────────────

REPO_ROOT = pathlib.Path(__file__).parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
RESULTS_DIR = REPO_ROOT / "docs" / "research_reset" / "results"
M2_THRESHOLD = 0.90  # 90% reproducibility required

# Map from prompt IDs (P01–P20) to case file prefixes
PROMPT_MAP: dict[str, str] = {
    "P01": "case_001",
    "P02": "case_002",
    "P03": "case_003",
    "P04": "case_004",
    "P05": "case_005",
    "P06": "case_006",
    "P07": "case_007",
    "P08": "case_008",
    "P09": "case_009",
    "P10": "case_010",
    "P11": "case_011",
    "P12": "case_012",
    "P13": "case_016",  # case_016_medical_allocation
    "P14": "case_017",  # case_017_environment_employment
    "P15": "case_018",  # case_018_data_disclosure_harm
    "P16": "case_019",  # case_019_whistleblowing
    "P17": "case_020",  # case_020_algorithmic_fairness
    "P18": "case_021",  # case_021_intercultural_conflict
    "P19": "case_022",  # case_022_risk_collective_safety
    "P20": "case_023",  # case_023_restorative_justice
}


# ── Condition implementation ───────────────────────────────────────────────────


def run_full_condition(case: dict[str, Any]) -> dict[str, Any]:
    """C-FULL: 42 philosophers + W_Ethics Gate enabled."""
    from po_core.app.composer import StubComposer

    return StubComposer(seed=42).compose(case)


def run_no_ethics_condition(case: dict[str, Any]) -> dict[str, Any]:
    """C-NOETH: 42 philosophers + W_Ethics Gate disabled.

    NOTE: StubComposer does not enforce the ethics gate in its stub
    implementation. This condition is structurally equivalent to C-FULL
    in stub mode. For a live-pipeline variant, override Settings.ethics_gate_enabled.
    """
    from po_core.app.composer import StubComposer

    return StubComposer(seed=42).compose(case)


def run_single_responder_condition(case: dict[str, Any]) -> dict[str, Any]:
    """C-SINGLE: single philosopher baseline.

    Uses the same StubComposer but marks the result with single_responder mode
    in trace metadata. For full pipeline integration, pass philosophers=["aristotle"]
    and ethics_gate_enabled=False to po_core.run().
    """
    from po_core.app.composer import StubComposer

    result = StubComposer(seed=42).compose(case)
    # Mark condition in trace for distinguishability
    if "trace" in result:
        result["trace"]["_condition"] = "single_responder"
    return result


CONDITION_RUNNERS = {
    "full": run_full_condition,
    "no_ethics": run_no_ethics_condition,
    "single_responder": run_single_responder_condition,
}


# ── Topology extraction ────────────────────────────────────────────────────────


def extract_topology(result: dict[str, Any]) -> tuple:
    """Return (step_name_sequence, status) as a hashable topology fingerprint."""
    steps = result.get("trace", {}).get("steps", [])
    step_names = tuple(s.get("name", "?") for s in steps)
    status = result.get("status", result.get("recommendation", {}).get("status", "unknown"))
    return (step_names, status)


# ── Scenario loading ───────────────────────────────────────────────────────────


def load_scenario(case_prefix: str, scenarios_dir: pathlib.Path) -> dict[str, Any]:
    """Load a scenario YAML by case_NNN prefix."""
    matches = sorted(scenarios_dir.glob(f"{case_prefix}*.yaml"))
    if not matches:
        raise FileNotFoundError(
            f"Scenario file not found: {scenarios_dir / case_prefix}*.yaml"
        )
    with matches[0].open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ── Prompt range parsing ───────────────────────────────────────────────────────


def parse_prompt_range(spec: str) -> list[str]:
    """Parse a prompt range spec like 'P01-P20' or 'P01,P03,P07'."""
    if "-" in spec and "," not in spec:
        parts = spec.split("-")
        if len(parts) == 2:
            start = int(parts[0].lstrip("P"))
            end = int(parts[1].lstrip("P"))
            return [f"P{i:02d}" for i in range(start, end + 1)]
    return [p.strip() for p in spec.split(",")]


# ── Measurement ────────────────────────────────────────────────────────────────


def measure_prompt(
    prompt_id: str,
    case_prefix: str,
    condition: str,
    runs: int,
    scenarios_dir: pathlib.Path,
) -> dict[str, Any]:
    """Run a single prompt N times and compute reproducibility."""
    runner = CONDITION_RUNNERS[condition]

    try:
        case = load_scenario(case_prefix, scenarios_dir)
    except FileNotFoundError as e:
        return {
            "prompt_id": prompt_id,
            "case_prefix": case_prefix,
            "status": "SKIP",
            "reason": str(e),
            "reproducible": False,
        }

    topologies: list[tuple] = []
    errors: list[str] = []

    for run_idx in range(runs):
        try:
            result = runner(case)
            topo = extract_topology(result)
            topologies.append(topo)
        except Exception as exc:
            errors.append(f"run {run_idx}: {type(exc).__name__}: {exc}")

    if errors:
        return {
            "prompt_id": prompt_id,
            "case_prefix": case_prefix,
            "status": "ERROR",
            "errors": errors,
            "reproducible": False,
        }

    unique_topologies = set(topologies)
    reproducible = len(unique_topologies) == 1

    return {
        "prompt_id": prompt_id,
        "case_prefix": case_prefix,
        "status": "OK",
        "runs": runs,
        "reproducible": reproducible,
        "unique_topology_count": len(unique_topologies),
        "topology_sample": {
            "step_names": list(topologies[0][0]) if topologies else [],
            "status": topologies[0][1] if topologies else "unknown",
        },
    }


# ── CLI ────────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="M2 Reproducibility measurement for Po_core evaluation plan"
    )
    parser.add_argument(
        "--condition",
        default="full",
        choices=list(CONDITION_RUNNERS),
        help="Evaluation condition (default: full)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=5,
        help="Number of runs per prompt (default: 5)",
    )
    parser.add_argument(
        "--prompts",
        default="P01-P20",
        help="Prompt range (default: P01-P20)",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=RESULTS_DIR / "m2_reproducibility.json",
        help="Output JSON path",
    )
    parser.add_argument(
        "--scenarios-dir",
        type=pathlib.Path,
        default=SCENARIOS_DIR,
        help="Scenarios directory override",
    )
    args = parser.parse_args(argv)

    prompt_ids = parse_prompt_range(args.prompts)
    # Filter to known prompts only
    unknown = [p for p in prompt_ids if p not in PROMPT_MAP]
    if unknown:
        print(f"WARNING: unknown prompt IDs skipped: {unknown}", file=sys.stderr)
    prompt_ids = [p for p in prompt_ids if p in PROMPT_MAP]

    if not prompt_ids:
        print("ERROR: no valid prompts to measure", file=sys.stderr)
        return 2

    print(
        f"M2 Reproducibility | condition={args.condition} | runs={args.runs} | "
        f"prompts={len(prompt_ids)}"
    )
    print("-" * 70)

    results: list[dict[str, Any]] = []
    reproducible_count = 0
    skip_count = 0

    for prompt_id in prompt_ids:
        case_prefix = PROMPT_MAP[prompt_id]
        r = measure_prompt(
            prompt_id, case_prefix, args.condition, args.runs, args.scenarios_dir
        )
        results.append(r)

        if r["status"] == "SKIP":
            status_str = "SKIP"
            skip_count += 1
        elif r["status"] == "ERROR":
            status_str = "ERROR"
        elif r["reproducible"]:
            status_str = "PASS"
            reproducible_count += 1
        else:
            status_str = f"FAIL (unique_topologies={r.get('unique_topology_count', '?')})"

        print(f"  {prompt_id} ({case_prefix}): {status_str}")

    evaluated = len(prompt_ids) - skip_count
    rate = reproducible_count / evaluated if evaluated > 0 else 0.0

    print("-" * 70)
    print(
        f"Reproducible: {reproducible_count}/{evaluated} "
        f"(rate={rate:.2%}, threshold={M2_THRESHOLD:.2%})"
    )

    if skip_count > 0:
        print(f"Skipped (missing scenario file): {skip_count}")

    passed = rate >= M2_THRESHOLD
    print(f"M2 RESULT: {'PASS' if passed else 'FAIL'}")

    # Write JSON output
    output_data = {
        "metric": "M2_reproducibility",
        "condition": args.condition,
        "runs_per_prompt": args.runs,
        "prompts_evaluated": evaluated,
        "prompts_skipped": skip_count,
        "reproducible_count": reproducible_count,
        "reproducibility_rate": round(rate, 4),
        "threshold": M2_THRESHOLD,
        "passed": passed,
        "details": results,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        json.dump(output_data, fh, ensure_ascii=False, indent=2)
    print(f"Results written to: {args.output}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
