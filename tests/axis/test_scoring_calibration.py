from __future__ import annotations

import json

import pytest

from po_core.axis.scoring import _clear_scoring_calibration_model_cache, score_text
from po_core.axis.spec import load_axis_spec


def test_score_text_without_calibration_env_returns_keyword_ratios(monkeypatch) -> None:
    monkeypatch.delenv("PO_AXIS_SCORING_CALIBRATION_PARAMS", raising=False)
    _clear_scoring_calibration_model_cache()

    spec = load_axis_spec()
    text = "risk harm value feasible"

    scores = score_text(text, spec)

    assert scores == {
        "safety": 0.5,
        "benefit": 0.25,
        "feasibility": 0.25,
    }


def test_score_text_with_calibration_env_changes_distribution(
    tmp_path, monkeypatch
) -> None:
    params_path = tmp_path / "axis_scoring_params.json"
    params_path.write_text(
        json.dumps(
            {
                "version": "axis_scoring_calibration_v1",
                "feature_order": ["safety", "benefit", "feasibility"],
                "labels": {
                    "safety": {"weights": [1.5, 0.0, 0.0], "bias": 0.0},
                    "benefit": {"weights": [0.0, 1.0, 0.0], "bias": 0.0},
                    "feasibility": {"weights": [0.0, 0.0, 1.0], "bias": 0.0},
                },
            }
        ),
        encoding="utf-8",
    )

    spec = load_axis_spec()
    text = "risk harm value feasible"

    monkeypatch.delenv("PO_AXIS_SCORING_CALIBRATION_PARAMS", raising=False)
    _clear_scoring_calibration_model_cache()
    raw_scores = score_text(text, spec)

    monkeypatch.setenv("PO_AXIS_SCORING_CALIBRATION_PARAMS", str(params_path))
    _clear_scoring_calibration_model_cache()
    calibrated_scores = score_text(text, spec)

    assert set(calibrated_scores.keys()) == set(raw_scores.keys())
    assert calibrated_scores["safety"] > raw_scores["safety"]
    assert calibrated_scores != raw_scores
    assert sum(calibrated_scores.values()) == pytest.approx(1.0)
