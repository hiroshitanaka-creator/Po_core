import json
import subprocess
import sys
from pathlib import Path

import pytest

from po_core.tensors.freedom_pressure_v2 import FreedomPressureV2


@pytest.mark.unit
def test_train_and_load_calibration_params_changes_estimation(tmp_path, monkeypatch):
    dataset = tmp_path / "train.jsonl"
    dataset.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "text": "choose choose choose option",
                        "labels": {
                            "choice": 0.95,
                            "responsibility": 0.05,
                            "urgency": 0.1,
                            "ethics": 0.1,
                            "social": 0.1,
                            "authenticity": 0.1,
                        },
                        "meta": {"lang": "ja", "domain": "career"},
                    },
                    ensure_ascii=False,
                ),
                json.dumps(
                    {
                        "text": "society community others people",
                        "labels": {
                            "choice": 0.05,
                            "responsibility": 0.1,
                            "urgency": 0.1,
                            "ethics": 0.1,
                            "social": 0.95,
                            "authenticity": 0.1,
                        },
                        "meta": {"lang": "ja", "domain": "career"},
                    },
                    ensure_ascii=False,
                ),
                json.dumps(
                    {
                        "text": "urgent now immediate deadline",
                        "labels": {
                            "choice": 0.05,
                            "responsibility": 0.1,
                            "urgency": 0.95,
                            "ethics": 0.05,
                            "social": 0.05,
                            "authenticity": 0.05,
                        },
                        "meta": {"lang": "ja", "domain": "career"},
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    params_path = tmp_path / "params_v1.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/train_axis_calibration.py",
            "--dataset",
            str(dataset),
            "--output",
            str(params_path),
            "--alpha",
            "0.05",
        ],
        check=True,
    )
    saved = json.loads(params_path.read_text(encoding="utf-8"))
    assert "labels" in saved and "choice" in saved["labels"]

    monkeypatch.delenv("PO_CALIBRATION_PARAMS", raising=False)
    baseline = FreedomPressureV2(
        model_name="__nonexistent_model_to_force_keyword_fallback__",
        ema_alpha=1.0,
        correlation_blend=0.0,
    ).compute_v2("choose choose choose option").values

    monkeypatch.setenv("PO_CALIBRATION_PARAMS", str(params_path))
    calibrated_engine_1 = FreedomPressureV2(
        model_name="__nonexistent_model_to_force_keyword_fallback__",
        ema_alpha=1.0,
        correlation_blend=0.0,
    )
    calibrated_engine_2 = FreedomPressureV2(
        model_name="__nonexistent_model_to_force_keyword_fallback__",
        ema_alpha=1.0,
        correlation_blend=0.0,
    )
    calibrated_1 = calibrated_engine_1.compute_v2("choose choose choose option").values
    calibrated_2 = calibrated_engine_2.compute_v2("choose choose choose option").values

    assert calibrated_1 == calibrated_2
    assert calibrated_1 != baseline


@pytest.mark.unit
def test_invalid_calibration_path_falls_back_to_heuristic(monkeypatch):
    monkeypatch.delenv("PO_CALIBRATION_PARAMS", raising=False)
    baseline = FreedomPressureV2(
        model_name="__nonexistent_model_to_force_keyword_fallback__",
        ema_alpha=1.0,
        correlation_blend=0.0,
    ).compute_v2("urgent now immediate deadline").values

    monkeypatch.setenv("PO_CALIBRATION_PARAMS", "/tmp/not_found_params_v1.json")
    fallback = FreedomPressureV2(
        model_name="__nonexistent_model_to_force_keyword_fallback__",
        ema_alpha=1.0,
        correlation_blend=0.0,
    ).compute_v2("urgent now immediate deadline").values

    assert fallback == baseline
