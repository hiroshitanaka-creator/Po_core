"""Evaluate emergence metrics across cases.

This utility aggregates per-case emergence observations and reports dataset-level
statistics.

`avg_novelty` is defined as a **signals-weighted mean** across all emergence
signals (not a case-level mean and not a mean of `peak_novelty`).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaseMetrics:
    """Per-case emergence metrics."""

    case_id: str
    n_signals: int
    peak_novelty: float
    avg_novelty: float


@dataclass(frozen=True)
class AggregateMetrics:
    """Aggregated emergence metrics across evaluated cases."""

    total_cases: int
    total_signals: int
    peak_novelty: float
    avg_novelty: float
    avg_signals_per_case: float


def _aggregate(rows: list[CaseMetrics]) -> AggregateMetrics:
    """Aggregate case metrics into dataset-level metrics.

    `avg_novelty` is computed as a signals-weighted mean:
    sum(case_avg_novelty * n_signals) / sum(n_signals).
    """

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
    """Render human-readable aggregate output."""

    return (
        "[Aggregate] "
        f"cases={metrics.total_cases} "
        f"signals={metrics.total_signals} "
        f"peak_novelty={metrics.peak_novelty:.4f} "
        f"avg_novelty(signals-weighted)={metrics.avg_novelty:.4f} "
        f"avg_signals_per_case={metrics.avg_signals_per_case:.2f}"
    )
