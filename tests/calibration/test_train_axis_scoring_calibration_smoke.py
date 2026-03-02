from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_train_function():
    script_path = Path("scripts/train_axis_scoring_calibration.py")
    spec = importlib.util.spec_from_file_location(
        "train_axis_scoring_calibration", script_path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.train


def test_train_axis_scoring_calibration_smoke(tmp_path: Path) -> None:
    train = _load_train_function()

    dataset_path = Path("calibration/axis_scoring_labels_sample.jsonl")
    output_path = tmp_path / "axis_scoring_params_v1.json"

    params = train(dataset_path=dataset_path, output_path=output_path, alpha=0.1)
    written = json.loads(output_path.read_text(encoding="utf-8"))

    assert params["version"] == "axis_scoring_calibration_v1"
    assert written["version"] == "axis_scoring_calibration_v1"

    feature_order = written["feature_order"]
    assert all(dim in feature_order for dim in ["safety", "benefit", "feasibility"])
    assert set(written["labels"].keys()) == set(feature_order)
