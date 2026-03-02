from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_eval_module():
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "eval_axis_scoring_calibration.py"
    spec = importlib.util.spec_from_file_location("eval_axis_scoring_calibration", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluate_axis_scoring_calibration_smoke(tmp_path) -> None:
    eval_module = _load_eval_module()

    dataset_path = tmp_path / "tiny.jsonl"
    rows = [
        {
            "text": "risk harm",
            "labels": {"safety": 0.8, "benefit": 0.1, "feasibility": 0.1},
        },
        {
            "text": "benefit value feasible",
            "labels": {"safety": 0.1, "benefit": 0.6, "feasibility": 0.3},
        },
    ]
    dataset_path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

    result = eval_module.evaluate_axis_scoring_calibration(
        dataset_path=dataset_path,
        split=0.5,
        seed=0,
    )

    assert "raw" in result
    assert "overall_mae" in result["raw"]
    assert "per_dimension_mae" in result["raw"]
    assert {"safety", "benefit", "feasibility"} == set(result["raw"]["per_dimension_mae"].keys())
