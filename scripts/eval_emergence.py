#!/usr/bin/env python3
"""Evaluate emergence with/without deliberation rounds.

This script runs the same inputs in two configurations (baseline vs with-deliberation)
and compares emergence metrics from ``DeliberationCompleted`` trace summaries.

Definition note:
- ``avg_novelty`` is a **signals-weighted mean** over all emergence signals in the
  evaluated set of cases.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from po_core.app.api import run
from po_core.runtime.settings import Settings
from po_core.trace.in_memory import InMemoryTracer


@dataclass(frozen=True)
class CaseMetrics:
    case_id: str
    n_signals: int
    peak_novelty: float
    avg_novelty: float


@dataclass(frozen=True)
class AggregateMetrics:
    total_cases: int
    total_signals: int
    peak_novelty: float
    avg_novelty: float
    avg_signals_per_case: float


def _parse_input_item(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for key in ("user_input", "input", "prompt", "text"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value
    raise ValueError(f"Unsupported input item format: {item!r}")


def _load_inputs(paths: list[str]) -> list[str]:
    """Load input prompts from txt/json/yaml files."""

    if not paths:
        return [
            "転職と家族ケアの優先順位をどう決めるべきか",
            "短期利益と長期信頼のトレードオフをどう扱うか",
        ]

    loaded: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        suffix = path.suffix.lower()

        if suffix == ".txt":
            lines = [
                line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            ]
            loaded.extend(line for line in lines if line)
            continue

        if suffix in {".json", ".yaml", ".yml"}:
            if suffix == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
            else:
                try:
                    import yaml
                except ImportError as exc:  # pragma: no cover
                    raise RuntimeError(
                        "PyYAML is required to load .yaml/.yml inputs"
                    ) from exc
                data = yaml.safe_load(path.read_text(encoding="utf-8"))

            if isinstance(data, list):
                loaded.extend(_parse_input_item(item) for item in data)
            elif isinstance(data, dict):
                if "inputs" in data and isinstance(data["inputs"], list):
                    loaded.extend(_parse_input_item(item) for item in data["inputs"])
                else:
                    loaded.append(_parse_input_item(data))
            else:
                raise ValueError(
                    f"Unsupported input document type in {path}: {type(data)}"
                )
            continue

        raise ValueError(f"Unsupported input file extension: {path}")

    if not loaded:
        raise ValueError("No inputs were loaded.")
    return loaded


def _find_deliberation_summary(tracer: InMemoryTracer) -> dict[str, Any] | None:
    """Find DeliberationCompleted payload from in-memory tracer events."""

    for event in tracer.events:
        if event.event_type == "DeliberationCompleted":
            payload = event.payload
            if isinstance(payload, dict):
                return payload
    return None


def _run_case(case_id: str, user_input: str, rounds: int) -> CaseMetrics:
    tracer = InMemoryTracer()
    settings = Settings(deliberation_max_rounds=rounds)
    run(user_input=user_input, settings=settings, tracer=tracer)

    summary = _find_deliberation_summary(tracer) or {}
    emergence = summary.get("emergence") if isinstance(summary, dict) else {}
    if not isinstance(emergence, dict):
        emergence = {}

    n_signals = int(emergence.get("n_signals", 0) or 0)
    peak_novelty = float(emergence.get("peak_novelty", 0.0) or 0.0)
    avg_novelty = float(emergence.get("avg_novelty", 0.0) or 0.0)

    return CaseMetrics(
        case_id=case_id,
        n_signals=n_signals,
        peak_novelty=peak_novelty,
        avg_novelty=avg_novelty,
    )


def _aggregate(rows: list[CaseMetrics]) -> AggregateMetrics:
    total_cases = len(rows)
    total_signals = sum(r.n_signals for r in rows)
    peak = max((r.peak_novelty for r in rows), default=0.0)
    if total_signals == 0:
        avg_novelty = 0.0
    else:
        avg_novelty = sum(r.avg_novelty * r.n_signals for r in rows) / total_signals
    avg_signals = (total_signals / total_cases) if total_cases else 0.0
    return AggregateMetrics(
        total_cases=total_cases,
        total_signals=total_signals,
        peak_novelty=peak,
        avg_novelty=avg_novelty,
        avg_signals_per_case=avg_signals,
    )


def _format_aggregate(metrics: AggregateMetrics) -> str:
    return (
        "[Aggregate] "
        f"cases={metrics.total_cases} "
        f"signals={metrics.total_signals} "
        f"peak_novelty={metrics.peak_novelty:.4f} "
        f"avg_novelty(signals-weighted)={metrics.avg_novelty:.4f} "
        f"avg_signals_per_case={metrics.avg_signals_per_case:.2f}"
    )


def _print_human_readable(
    baseline_rows: list[CaseMetrics],
    with_rows: list[CaseMetrics],
    baseline_agg: AggregateMetrics,
    with_agg: AggregateMetrics,
) -> None:
    print("=== Emergence Compare (baseline vs with-deliberation) ===")
    for base, var in zip(baseline_rows, with_rows):
        print(
            f"[Case] {base.case_id} "
            f"signals {base.n_signals} -> {var.n_signals} | "
            f"peak {base.peak_novelty:.4f} -> {var.peak_novelty:.4f} | "
            f"avg {base.avg_novelty:.4f} -> {var.avg_novelty:.4f}"
        )

    print("\n-- Baseline --")
    print(_format_aggregate(baseline_agg))
    print("\n-- With Deliberation --")
    print(_format_aggregate(with_agg))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate emergence with/without deliberation"
    )
    parser.add_argument(
        "--inputs", nargs="*", default=[], help="Input files (.txt/.json/.yaml/.yml)"
    )
    parser.add_argument(
        "--baseline-rounds",
        type=int,
        default=1,
        help="Deliberation rounds for baseline",
    )
    parser.add_argument(
        "--with-rounds", type=int, default=3, help="Deliberation rounds for variant"
    )
    parser.add_argument(
        "--output-json", default="", help="Optional path to save JSON report"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    inputs = _load_inputs(args.inputs)

    baseline_rows: list[CaseMetrics] = []
    with_rows: list[CaseMetrics] = []

    for idx, user_input in enumerate(inputs, start=1):
        case_id = f"case_{idx:03d}"
        baseline_rows.append(
            _run_case(case_id, user_input, rounds=args.baseline_rounds)
        )
        with_rows.append(_run_case(case_id, user_input, rounds=args.with_rounds))

    baseline_agg = _aggregate(baseline_rows)
    with_agg = _aggregate(with_rows)
    _print_human_readable(baseline_rows, with_rows, baseline_agg, with_agg)

    if args.output_json:
        report = {
            "definition": {
                "avg_novelty": "signals-weighted mean over all emergence signals",
            },
            "config": {
                "baseline_rounds": args.baseline_rounds,
                "with_rounds": args.with_rounds,
                "inputs_count": len(inputs),
            },
            "baseline": {
                "cases": [asdict(row) for row in baseline_rows],
                "aggregate": asdict(baseline_agg),
            },
            "with_deliberation": {
                "cases": [asdict(row) for row in with_rows],
                "aggregate": asdict(with_agg),
            },
        }
        Path(args.output_json).write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        print(f"\nSaved JSON report: {args.output_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
