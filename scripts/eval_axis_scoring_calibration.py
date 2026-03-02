#!/usr/bin/env python3
"""Evaluate raw vs calibrated axis scoring against labeled JSONL data."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterable, Iterator, Mapping, Sequence

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC_PATH = _REPO_ROOT / "src"
if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))

from po_core.axis.scoring import _clear_scoring_calibration_model_cache, score_text
from po_core.axis.spec import load_axis_spec

_ENV_CALIB_PATH = "PO_AXIS_SCORING_CALIBRATION_PARAMS"


@contextmanager
def _temporary_calibration_env(path: str | None) -> Iterator[None]:
    original = os.environ.get(_ENV_CALIB_PATH)
    if path:
        os.environ[_ENV_CALIB_PATH] = path
    else:
        os.environ.pop(_ENV_CALIB_PATH, None)
    _clear_scoring_calibration_model_cache()
    try:
        yield
    finally:
        if original is None:
            os.environ.pop(_ENV_CALIB_PATH, None)
        else:
            os.environ[_ENV_CALIB_PATH] = original
        _clear_scoring_calibration_model_cache()


def _iter_jsonl(path: Path) -> Iterable[Mapping[str, object]]:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        yield json.loads(line)


def _coerce_label(value: object) -> float:
    if isinstance(value, bool):
        raise ValueError("bool is not a valid label value")
    return min(max(float(value), 0.0), 1.0)


def _load_records(dataset_path: Path, dimension_ids: Sequence[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
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
            coerced_labels = {dim: _coerce_label(labels[dim]) for dim in dimension_ids}
        except (TypeError, ValueError) as exc:
            raise ValueError(f"line {idx}: invalid label value ({exc})") from exc

        records.append({"text": text, "labels": coerced_labels})

    if not records:
        raise ValueError("No valid samples found in dataset.")
    return records


def _select_holdout(records: list[dict[str, object]], split: float, seed: int) -> list[dict[str, object]]:
    if not (0.0 < split <= 1.0):
        raise ValueError("split must be within (0, 1].")

    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    holdout_size = max(1, int(round(len(shuffled) * split)))
    holdout_size = min(len(shuffled), holdout_size)
    return shuffled[:holdout_size]


def _compute_mae(records: list[dict[str, object]], dimension_ids: Sequence[str], spec: object) -> dict[str, object]:
    abs_error_sum = {dim: 0.0 for dim in dimension_ids}
    sample_count = len(records)

    for rec in records:
        labels: Mapping[str, float] = rec["labels"]  # type: ignore[assignment]
        scores = score_text(rec["text"], spec=spec)  # type: ignore[arg-type]
        for dim in dimension_ids:
            abs_error_sum[dim] += abs(float(scores.get(dim, 0.0)) - float(labels[dim]))

    per_dimension_mae = {dim: abs_error_sum[dim] / float(sample_count) for dim in dimension_ids}
    overall_mae = sum(per_dimension_mae.values()) / float(len(dimension_ids))
    return {
        "per_dimension_mae": per_dimension_mae,
        "overall_mae": overall_mae,
        "samples": sample_count,
    }


def evaluate_axis_scoring_calibration(
    dataset_path: Path,
    params_path: Path | None = None,
    seed: int = 0,
    split: float = 0.2,
    spec_path: str | None = None,
) -> dict[str, object]:
    spec = load_axis_spec(spec_path)
    dimension_ids = [d.dimension_id for d in spec.dimensions]
    records = _load_records(dataset_path, dimension_ids)
    holdout_records = _select_holdout(records, split=split, seed=seed)

    with _temporary_calibration_env(None):
        raw_metrics = _compute_mae(holdout_records, dimension_ids, spec)

    result: dict[str, object] = {
        "raw": raw_metrics,
        "split": split,
        "seed": seed,
        "holdout_samples": len(holdout_records),
    }

    if params_path is not None:
        with _temporary_calibration_env(str(params_path)):
            calibrated_metrics = _compute_mae(holdout_records, dimension_ids, spec)

        delta_per_dim = {
            dim: calibrated_metrics["per_dimension_mae"][dim] - raw_metrics["per_dimension_mae"][dim]  # type: ignore[index]
            for dim in dimension_ids
        }
        delta_overall = float(calibrated_metrics["overall_mae"]) - float(raw_metrics["overall_mae"])
        result["calibrated"] = calibrated_metrics
        result["delta"] = {
            "per_dimension_mae": delta_per_dim,
            "overall_mae": delta_overall,
        }

    return result


def _print_metrics(metrics: Mapping[str, object], prefix: str) -> None:
    print(f"[{prefix}] overall_mae={float(metrics['overall_mae']):.6f} samples={int(metrics['samples'])}")
    per_dim = metrics["per_dimension_mae"]
    for dim, value in per_dim.items():
        print(f"[{prefix}] {dim}_mae={float(value):.6f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, help="Path to labeled JSONL dataset")
    parser.add_argument(
        "--params",
        default=None,
        help="Optional calibration params JSON path; if omitted evaluates raw only",
    )
    parser.add_argument("--seed", type=int, default=0, help="Random seed for holdout split")
    parser.add_argument(
        "--split",
        type=float,
        default=0.2,
        help="Holdout fraction in (0, 1] (default: 0.2)",
    )
    parser.add_argument(
        "--spec",
        default=None,
        help="Optional axis spec path (default: po_core.axis.spec.load_axis_spec())",
    )
    args = parser.parse_args()

    result = evaluate_axis_scoring_calibration(
        dataset_path=Path(args.dataset),
        params_path=Path(args.params) if args.params else None,
        seed=args.seed,
        split=args.split,
        spec_path=args.spec,
    )

    _print_metrics(result["raw"], "raw")
    if "calibrated" in result:
        _print_metrics(result["calibrated"], "calibrated")
        delta = result["delta"]
        print(f"[delta] overall_mae={float(delta['overall_mae']):+.6f}")
        for dim, value in delta["per_dimension_mae"].items():
            print(f"[delta] {dim}_mae={float(value):+.6f}")


if __name__ == "__main__":
    main()
