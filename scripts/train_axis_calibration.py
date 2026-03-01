#!/usr/bin/env python3
"""Train linear axis-calibration parameters from JSONL labels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

DIMS: Sequence[str] = (
    "choice",
    "responsibility",
    "urgency",
    "ethics",
    "social",
    "authenticity",
)

_KEYWORD_ANCHORS: List[List[str]] = [
    ["should", "must", "decide", "choose", "option", "alternative", "what"],
    ["responsible", "duty", "obligation", "accountable", "answer"],
    ["now", "urgent", "immediate", "quickly", "soon", "deadline"],
    ["right", "wrong", "good", "bad", "moral", "ethical", "virtue"],
    ["we", "us", "society", "people", "community", "others", "everyone"],
    ["authentic", "genuine", "true", "self", "real", "sincere"],
]


def _extract_keyword_features(text: str) -> List[float]:
    text_lower = text.lower()
    features: List[float] = []
    for keywords in _KEYWORD_ANCHORS:
        hits = sum(1 for kw in keywords if kw in text_lower)
        features.append(min(hits / max(len(keywords), 1), 1.0))
    return features


def _iter_jsonl(path: Path) -> Iterable[Dict[str, object]]:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        yield json.loads(line)


def _load_dataset(dataset_path: Path) -> Tuple[List[List[float]], Dict[str, List[float]]]:
    x_rows: List[List[float]] = []
    y_rows: Dict[str, List[float]] = {dim: [] for dim in DIMS}

    for rec in _iter_jsonl(dataset_path):
        text = rec.get("text")
        labels = rec.get("labels")
        if not isinstance(text, str) or not isinstance(labels, dict):
            continue
        if any(dim not in labels for dim in DIMS):
            continue

        try:
            y_vals = {dim: float(labels[dim]) for dim in DIMS}
        except (TypeError, ValueError):
            continue

        features = _extract_keyword_features(text)
        x_rows.append(features)
        for dim in DIMS:
            y_rows[dim].append(min(max(y_vals[dim], 0.0), 1.0))

    if not x_rows:
        raise ValueError("No valid training samples found in dataset.")

    return x_rows, y_rows


def _fit_ridge_numpy(x_rows: List[List[float]], y: List[float], alpha: float) -> Tuple[float, List[float]]:
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


def _fit_ridge_fallback(x_rows: List[List[float]], y: List[float], alpha: float) -> Tuple[float, List[float]]:
    # 最小依存 fallback: バイアスのみを推定（安全側）
    mean = sum(y) / max(len(y), 1)
    return float(mean), [0.0 for _ in x_rows[0]]


def _fit_ridge(x_rows: List[List[float]], y: List[float], alpha: float) -> Tuple[float, List[float]]:
    if np is None:
        return _fit_ridge_fallback(x_rows, y, alpha)
    return _fit_ridge_numpy(x_rows, y, alpha)


def train(dataset_path: Path, output_path: Path, alpha: float) -> Dict[str, object]:
    x_rows, y_rows = _load_dataset(dataset_path)
    labels: Dict[str, Dict[str, object]] = {}

    for dim in DIMS:
        bias, weights = _fit_ridge(x_rows, y_rows[dim], alpha)
        labels[dim] = {"bias": bias, "weights": weights}

    params = {
        "version": "axis_calibration_v1",
        "feature_order": list(DIMS),
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
        default="calibration/params_v1.json",
        help="Output params file path (default: calibration/params_v1.json)",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="Ridge regularization alpha (default: 0.1)",
    )
    args = parser.parse_args()

    params = train(Path(args.dataset), Path(args.output), alpha=args.alpha)
    print(f"trained dims={len(params['labels'])} output={args.output}")


if __name__ == "__main__":
    main()
