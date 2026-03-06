from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_eval_emergence_module():
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "scripts" / "eval_emergence.py"
    spec = importlib.util.spec_from_file_location(
        "eval_emergence_for_tests", module_path
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_aggregate_avg_novelty_is_signals_weighted_not_peak_average():
    module = _load_eval_emergence_module()
    CaseMetrics = module.CaseMetrics
    aggregate = module._aggregate

    rows = [
        CaseMetrics("a", n_signals=2, peak_novelty=0.9, avg_novelty=0.3),
        CaseMetrics("b", n_signals=1, peak_novelty=0.1, avg_novelty=0.1),
    ]

    metrics = aggregate(rows)

    expected_weighted = (0.3 * 2 + 0.1 * 1) / 3
    peak_average = (0.9 + 0.1) / 2

    assert metrics.avg_novelty == pytest.approx(expected_weighted)
    assert metrics.avg_novelty != pytest.approx(peak_average)


def test_aggregate_avg_novelty_is_zero_when_total_signals_is_zero():
    module = _load_eval_emergence_module()
    CaseMetrics = module.CaseMetrics
    aggregate = module._aggregate

    rows = [
        CaseMetrics("a", n_signals=0, peak_novelty=0.7, avg_novelty=0.4),
        CaseMetrics("b", n_signals=0, peak_novelty=0.9, avg_novelty=0.8),
    ]

    metrics = aggregate(rows)

    assert metrics.total_signals == 0
    assert metrics.avg_novelty == 0.0
