"""Utilities for optional axis calibration parameter loading and inference."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence

import numpy as np

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AxisCalibrationModel:
    """Linear calibration model for 6D freedom-pressure raw scores."""

    feature_order: Sequence[str]
    weights: Dict[str, np.ndarray]
    bias: Dict[str, float]

    def apply(self, features: np.ndarray, dims: Sequence[str]) -> np.ndarray:
        """Apply per-dimension linear transform and clamp to [0, 1]."""
        calibrated = np.array(features, dtype=np.float64)
        for idx, dim in enumerate(dims):
            if dim not in self.weights:
                continue
            row = self.weights[dim]
            calibrated[idx] = float(np.dot(row, features) + self.bias[dim])
        return np.clip(calibrated, 0.0, 1.0)


def load_calibration_model_from_path(path: Optional[str]) -> Optional[AxisCalibrationModel]:
    """Load axis calibration model from json file path."""
    if not path:
        return None
    file_path = Path(path)
    if not file_path.exists():
        logger.warning("Calibration params file not found: %s", file_path)
        return None

    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Failed to read calibration params: %s", exc)
        return None

    if not isinstance(payload, Mapping):
        logger.warning("Calibration params is not a JSON object: %s", file_path)
        return None

    labels = payload.get("labels")
    if not isinstance(labels, Mapping):
        logger.warning("Calibration params missing `labels`: %s", file_path)
        return None

    feature_order = payload.get("feature_order")
    if not isinstance(feature_order, list) or not all(
        isinstance(item, str) for item in feature_order
    ):
        logger.warning("Calibration params missing valid `feature_order`: %s", file_path)
        return None

    weights: Dict[str, np.ndarray] = {}
    bias: Dict[str, float] = {}
    for dim, spec in labels.items():
        if not isinstance(dim, str) or not isinstance(spec, Mapping):
            continue
        raw_weights = spec.get("weights")
        raw_bias = spec.get("bias")
        if not isinstance(raw_weights, list) or not isinstance(raw_bias, (int, float)):
            continue
        if len(raw_weights) != len(feature_order):
            continue
        weights[dim] = np.array([float(v) for v in raw_weights], dtype=np.float64)
        bias[dim] = float(raw_bias)

    if not weights:
        logger.warning("Calibration params contains no usable labels: %s", file_path)
        return None

    return AxisCalibrationModel(feature_order=feature_order, weights=weights, bias=bias)


def load_calibration_model_from_env(
    env_var: str = "PO_CALIBRATION_PARAMS",
) -> Optional[AxisCalibrationModel]:
    """Load calibration model if env var points to a valid params file."""
    path = os.getenv(env_var)
    return load_calibration_model_from_path(path)


__all__ = [
    "AxisCalibrationModel",
    "load_calibration_model_from_env",
    "load_calibration_model_from_path",
]
