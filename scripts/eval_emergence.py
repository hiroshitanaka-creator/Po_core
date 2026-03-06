#!/usr/bin/env python3
"""Evaluate emergence metrics with and without deliberation rounds.

Runs the same input set with two settings:
- baseline: deliberation_max_rounds=1
- variant:  deliberation_max_rounds=N (2 or 3)

Metric definitions (strict):
- n_signals: count of detected emergence signals.
- peak_novelty: maximum novelty score among all signals.
- avg_novelty: signal-weighted mean novelty across all emergence signals.
  (i.e., global mean over all signals, not mean of per-case peaks)
- avg_peak_novelty: arithmetic mean of per-case peak_novelty (reported separately).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from po_core.app.api import run
from po_core.runtime.settings import Settings
from po_core.trace.in_memory import InMemoryTracer

DEFAULT_INPUTS = [
    "What is justice in an unequal world?",
    "Should we prioritize economic growth over ecological stability?",
    "Is individual freedom more important than social solidarity?",
    "How should AI be governed when values conflict across cultures?",
]


@dataclass(frozen=True)
class CaseMetrics:
    prompt: str
    n_signals: int
    peak_novelty: float
    avg_novelty: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "n_signals": self.n_signals,
            "peak_novelty": round(self.peak_novelty, 4),
            "avg_novelty": round(self.avg_novelty, 4),
        }


@dataclass(frozen=True)
class AggregateMetrics:
    total_cases: int
    total_signals: int
    peak_novelty: float
    avg_peak_novelty: float
    avg_novelty: float
    avg_signals_per_case: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_cases": self.total_cases,
            "total_signals": self.total_signals,
            "peak_novelty": round(self.peak_novelty, 4),
            "avg_peak_novelty": round(self.avg_peak_novelty, 4),
            "avg_novelty": round(self.avg_novelty, 4),
            "avg_signals_per_case": round(self.avg_signals_per_case, 4),
        }


def _load_inputs(path: Path | None) -> list[str]:
    if path is None:
        return list(DEFAULT_INPUTS)

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yml", ".yaml"}:
        data = yaml.safe_load(text)
    elif path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        return [line.strip() for line in text.splitlines() if line.strip()]

    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError("inputs file must be a list of prompt strings")
    return [x.strip() for x in data if x.strip()]


def _find_deliberation_summary(events: list[Any]) -> dict[str, Any]:
    for event in events:
        if getattr(event, "event_type", "") == "DeliberationCompleted":
            payload = getattr(event, "payload", {})
            if isinstance(payload, dict):
                return payload
    return {}


def _run_case(prompt: str, rounds: int) -> CaseMetrics:
    tracer = InMemoryTracer()
    run(prompt, settings=Settings(deliberation_max_rounds=rounds), tracer=tracer)
    summary = _find_deliberation_summary(tracer.events)
    emergence = summary.get("emergence", {}) if isinstance(summary, dict) else {}

    n_signals = int(emergence.get("n_signals", 0) or 0)
    peak = float(emergence.get("peak_novelty", 0.0) or 0.0)
    avg = float(emergence.get("avg_novelty", 0.0) or 0.0)

    return CaseMetrics(
        prompt=prompt,
        n_signals=n_signals,
        peak_novelty=peak,
        avg_novelty=avg,
    )


def _aggregate(rows: list[CaseMetrics]) -> AggregateMetrics:
    total_cases = len(rows)
    total_signals = sum(r.n_signals for r in rows)
    peak = max((r.peak_novelty for r in rows), default=0.0)
    avg_peak_novelty = statistics.fmean([r.peak_novelty for r in rows]) if rows else 0.0
    avg_novelty = (
        sum(r.avg_novelty * r.n_signals for r in rows) / total_signals
        if total_signals > 0
        else 0.0
    )
    avg_signals = (total_signals / total_cases) if total_cases else 0.0
    return AggregateMetrics(
        total_cases=total_cases,
        total_signals=total_signals,
        peak_novelty=peak,
        avg_peak_novelty=avg_peak_novelty,
        avg_novelty=avg_novelty,
        avg_signals_per_case=avg_signals,
    )


def _print_human_readable(
    baseline_rounds: int,
    variant_rounds: int,
    baseline_rows: list[CaseMetrics],
    variant_rows: list[CaseMetrics],
) -> None:
    print("=== Emergence Evaluation (deliberation on/off) ===")
    print(f"baseline deliberation_max_rounds={baseline_rounds}")
    print(f"variant  deliberation_max_rounds={variant_rounds}")
    print("metric defs: avg_novelty=signal-weighted mean, avg_peak_novelty=mean(per-case peak)")
    print()

    print("[Per-case]")
    for idx, (base, var) in enumerate(zip(baseline_rows, variant_rows), start=1):
        print(f"{idx:02d}. {base.prompt}")
        print(
            "    baseline: "
            f"signals={base.n_signals}, peak_novelty={base.peak_novelty:.4f}, "
            f"avg_novelty={base.avg_novelty:.4f}"
        )
        print(
            "    variant : "
            f"signals={var.n_signals}, peak_novelty={var.peak_novelty:.4f}, "
            f"avg_novelty={var.avg_novelty:.4f}"
        )

    base_aggr = _aggregate(baseline_rows)
    var_aggr = _aggregate(variant_rows)

    print()
    print("[Aggregate]")
    print(
        "baseline: "
        f"total_signals={base_aggr.total_signals}, "
        f"peak_novelty={base_aggr.peak_novelty:.4f}, "
        f"avg_peak_novelty={base_aggr.avg_peak_novelty:.4f}, "
        f"avg_novelty={base_aggr.avg_novelty:.4f}"
    )
    print(
        "variant : "
        f"total_signals={var_aggr.total_signals}, "
        f"peak_novelty={var_aggr.peak_novelty:.4f}, "
        f"avg_peak_novelty={var_aggr.avg_peak_novelty:.4f}, "
        f"avg_novelty={var_aggr.avg_novelty:.4f}"
    )
    print(
        "delta   : "
        f"signals={var_aggr.total_signals - base_aggr.total_signals:+d}, "
        f"peak_novelty={var_aggr.peak_novelty - base_aggr.peak_novelty:+.4f}, "
        f"avg_peak_novelty={var_aggr.avg_peak_novelty - base_aggr.avg_peak_novelty:+.4f}, "
        f"avg_novelty={var_aggr.avg_novelty - base_aggr.avg_novelty:+.4f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare emergence metrics with deliberation_max_rounds=1 vs N"
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=None,
        help="Path to prompts file (txt/json/yaml). Defaults to built-in prompt set.",
    )
    parser.add_argument(
        "--baseline-rounds",
        type=int,
        default=1,
        help="Baseline deliberation rounds (default: 1)",
    )
    parser.add_argument(
        "--with-rounds",
        type=int,
        default=3,
        help="Variant deliberation rounds (default: 3)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to save machine-readable results JSON",
    )
    args = parser.parse_args()

    if args.baseline_rounds < 1 or args.with_rounds < 1:
        raise ValueError("rounds must be >= 1")

    prompts = _load_inputs(args.inputs)
    if not prompts:
        raise ValueError("input set is empty")

    baseline_rows = [_run_case(prompt, args.baseline_rounds) for prompt in prompts]
    variant_rows = [_run_case(prompt, args.with_rounds) for prompt in prompts]

    _print_human_readable(
        args.baseline_rounds,
        args.with_rounds,
        baseline_rows,
        variant_rows,
    )

    if args.output_json is not None:
        payload = {
            "config": {
                "baseline_rounds": args.baseline_rounds,
                "with_rounds": args.with_rounds,
                "n_inputs": len(prompts),
            },
            "baseline": {
                "aggregate": _aggregate(baseline_rows).to_dict(),
                "cases": [row.to_dict() for row in baseline_rows],
            },
            "variant": {
                "aggregate": _aggregate(variant_rows).to_dict(),
                "cases": [row.to_dict() for row in variant_rows],
            },
        }
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\nSaved JSON report: {args.output_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
