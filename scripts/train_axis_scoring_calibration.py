#!/usr/bin/env python3
"""Train linear calibration parameters for axis scoring from JSONL labels."""

from __future__ import annotations

import argparse
import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

from po_core.axis.scoring import score_text
from po_core.axis.spec import load_axis_spec

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

_ENV_CALIB_PATH = "PO_AXIS_SCORING_CALIBRATION_PARAMS"


@contextmanager
def _temporarily_disable_axis_scoring_calibration() -> Iterator[None]:
    original = os.environ.pop(_ENV_CALIB_PATH, None)
    try:
        yield
    finally:
        if original is not None:
            os.environ[_ENV_CALIB_PATH] = original


def _iter_jsonl(path: Path) -> Iterable[Mapping[str, object]]:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        yield json.loads(line)


def _coerce_label(value: object) -> float:
    if isinstance(value, bool):
        raise ValueError("bool is not a valid label value")
    as_float = float(value)
    return min(max(as_float, 0.0), 1.0)


def _load_dataset(
    dataset_path: Path,
    dimension_ids: Sequence[str],
    spec: object,
) -> Tuple[List[List[float]], Dict[str, List[float]]]:
    x_rows: List[List[float]] = []
    y_rows: Dict[str, List[float]] = {dim: [] for dim in dimension_ids}

    for idx, rec in enumerate(_iter_jsonl(dataset_path), start=1):
        text = rec.get("text")
        labels = rec.get("labels")

        if not isinstance(text, str):
            raise ValueError(f"line {idx}: 'text' must be a string")
        if not isinstance(labels, dict):
            raise ValueError(f"line {idx}: 'labels' must be an object")

        missing = [dim for dim in dimension_ids if dim not in labels]
        if missing:
            raise ValueError(f"line {idx}: missing labels for dimensions: {missing}")

        try:
            y_vals = {dim: _coerce_label(labels[dim]) for dim in dimension_ids}
        except (TypeError, ValueError) as exc:
            raise ValueError(f"line {idx}: invalid label value ({exc})") from exc

        with _temporarily_disable_axis_scoring_calibration():
            raw_scores = score_text(text, spec=spec)

        x_rows.append([float(raw_scores[dim]) for dim in dimension_ids])
        for dim in dimension_ids:
            y_rows[dim].append(y_vals[dim])

    if not x_rows:
        raise ValueError("No valid training samples found in dataset.")

    return x_rows, y_rows


def _fit_ridge_numpy(
    x_rows: List[List[float]],
    y: List[float],
    alpha: float,
) -> Tuple[float, List[float]]:
    assert np is not None
    x = np.array(x_rows, dtype=np.float64)
    y_vec = np.array(y, dtype=np.float64)

    ones = np.ones((x.shape[0], 1), dtype=np.float64)
    x_aug = np.hstack([ones, x])

    reg = np.eye(x_aug.shape[1], dtype=np.float64)
    reg[0, 0] = 0.0

    lhs = x_aug.T @ x_aug + alpha * reg
    rhs = x_aug.T @ y_vec

    coeff = np.linalg.solve(lhs, rhs)
    return float(coeff[0]), [float(v) for v in coeff[1:]]


def _fit_ridge_fallback(
    x_rows: List[List[float]],
    y: List[float],
    alpha: float,
) -> Tuple[float, List[float]]:
    _ = alpha
    mean = sum(y) / max(len(y), 1)
    return float(mean), [0.0 for _ in x_rows[0]]


def _fit_ridge(
    x_rows: List[List[float]],
    y: List[float],
    alpha: float,
) -> Tuple[float, List[float]]:
    if np is None:
        return _fit_ridge_fallback(x_rows, y, alpha)
    return _fit_ridge_numpy(x_rows, y, alpha)


def train(
    dataset_path: Path,
    output_path: Path,
    alpha: float,
    spec_path: str | None = None,
) -> Dict[str, object]:
    spec = load_axis_spec(spec_path)
    dimension_ids = [d.dimension_id for d in spec.dimensions]
    x_rows, y_rows = _load_dataset(dataset_path, dimension_ids, spec)

    labels: Dict[str, Dict[str, object]] = {}
    for dim in dimension_ids:
        bias, weights = _fit_ridge(x_rows, y_rows[dim], alpha)
        labels[dim] = {"bias": bias, "weights": weights}

    params = {
        "version": "axis_scoring_calibration_v1",
        "feature_order": dimension_ids,
        "ridge_alpha": float(alpha),
        "labels": labels,
        "backend": "numpy" if np is not None else "fallback",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return params


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, help="Path to JSONL training dataset")
    parser.add_argument(
        "--output",
        default="calibration/axis_scoring_params_v1.json",
        help="Output params file path (default: calibration/axis_scoring_params_v1.json)",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="Ridge regularization alpha (default: 0.1)",
    )
    parser.add_argument(
        "--spec",
        default=None,
        help="Optional axis spec path (default: po_core.axis.spec.load_axis_spec())",
    )
    args = parser.parse_args()

    params = train(
        dataset_path=Path(args.dataset),
        output_path=Path(args.output),
        alpha=args.alpha,
        spec_path=args.spec,
    )
    print(f"trained dims={len(params['labels'])} output={args.output}")


if __name__ == "__main__":
    main()
