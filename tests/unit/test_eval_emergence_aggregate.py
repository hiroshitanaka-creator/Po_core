from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "eval_emergence.py"
SPEC = importlib.util.spec_from_file_location("eval_emergence", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

CaseMetrics = MODULE.CaseMetrics
_aggregate = MODULE._aggregate


def test_aggregate_avg_novelty_weighted_by_signal_count() -> None:
    rows = [
        CaseMetrics(prompt="p1", n_signals=1, peak_novelty=0.95, avg_novelty=0.10),
        CaseMetrics(prompt="p2", n_signals=3, peak_novelty=0.20, avg_novelty=0.50),
        CaseMetrics(prompt="p3", n_signals=2, peak_novelty=0.10, avg_novelty=0.90),
    ]

    aggregated = _aggregate(rows)

    expected_weighted_avg = ((0.10 * 1) + (0.50 * 3) + (0.90 * 2)) / 6
    assert aggregated.total_signals == 6
    assert aggregated.avg_novelty == expected_weighted_avg

    # Guard against regression: this must NOT be average of peak_novelty.
    peak_mean = (0.95 + 0.20 + 0.10) / 3
    assert aggregated.avg_novelty != peak_mean


def test_aggregate_avg_novelty_zero_when_no_signals() -> None:
    rows = [
        CaseMetrics(prompt="p1", n_signals=0, peak_novelty=0.90, avg_novelty=0.80),
        CaseMetrics(prompt="p2", n_signals=0, peak_novelty=0.30, avg_novelty=0.20),
    ]

    aggregated = _aggregate(rows)

    assert aggregated.total_signals == 0
    assert aggregated.avg_novelty == 0.0
