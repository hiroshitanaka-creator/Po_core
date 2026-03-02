"""Deterministic axis scoring based on keyword-hit ratio.

This module projects free-form proposal text into axis scores by counting
whether dimension-specific keywords appear in normalized text.
The resulting score expresses a *relative emphasis* among dimensions
(keyword-hit ratio), not a semantic truth estimate.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Optional

from po_core.axis.spec import AxisSpec, load_axis_spec
from po_core.tensors.axis_calibration import (
    AxisCalibrationModel,
    load_calibration_model_from_env,
)
from po_core.text.normalize import normalize_text

_SCORING_CALIBRATION_ENV_VAR = "PO_AXIS_SCORING_CALIBRATION_PARAMS"

_KEYWORDS_BY_DIMENSION: dict[str, tuple[str, ...]] = {
    "safety": (
        "risk",
        "harm",
        "danger",
        "safety",
        "危険",
        "リスク",
        "安全",
        "炎上",
        "損害",
        "法的",
    ),
    "benefit": (
        "benefit",
        "value",
        "utility",
        "profit",
        "メリット",
        "価値",
        "利益",
        "効果",
        "便益",
        "成長",
    ),
    "feasibility": (
        "feasible",
        "practical",
        "plan",
        "steps",
        "implement",
        "現実的",
        "実現",
        "可能",
        "手順",
        "実装",
        "工数",
        "予算",
    ),
}


def score_text_with_debug(
    text: str, spec: AxisSpec
) -> tuple[dict[str, float], dict[str, object]]:
    """Score text and return deterministic scoring diagnostics.

    Debug payload intentionally contains only aggregate counters to avoid
    leaking raw content.
    """

    normalized = normalize_text(text)
    dimension_ids = [d.dimension_id for d in spec.dimensions]
    if not dimension_ids:
        return {}, {
            "total_hits": 0,
            "hits_by_dimension": {},
            "calibrated": False,
        }

    hits_by_dimension: dict[str, int] = {}
    for dimension_id in dimension_ids:
        keywords = _KEYWORDS_BY_DIMENSION.get(dimension_id, ())
        hits = sum(1 for kw in keywords if kw in normalized)
        hits_by_dimension[dimension_id] = hits

    total_hits = sum(hits_by_dimension.values())
    if total_hits <= 0:
        uniform = 1.0 / float(len(dimension_ids))
        raw_scores = {dimension_id: uniform for dimension_id in dimension_ids}
    else:
        raw_scores = {
            dimension_id: (hits_by_dimension[dimension_id] / float(total_hits))
            for dimension_id in dimension_ids
        }

    debug: dict[str, object] = {
        "total_hits": int(total_hits),
        "hits_by_dimension": hits_by_dimension,
        "calibrated": False,
    }

    model = _load_scoring_calibration_model()
    if model is None:
        return raw_scores, debug

    try:
        features = [float(raw_scores.get(dim, 0.0)) for dim in model.feature_order]
        calibrated = model.apply(features, dims=model.feature_order)
        calibrated_by_dimension = {
            dimension_id: float(calibrated[idx])
            for idx, dimension_id in enumerate(model.feature_order)
        }
        projected_scores = {
            dimension_id: float(calibrated_by_dimension.get(dimension_id, 0.0))
            for dimension_id in dimension_ids
        }
    except Exception:
        return raw_scores, debug

    calibrated_total = sum(projected_scores.values())
    if calibrated_total <= 0:
        uniform = 1.0 / float(len(dimension_ids))
        debug["calibrated"] = True
        return {dimension_id: uniform for dimension_id in dimension_ids}, debug

    debug["calibrated"] = True
    return (
        {
            dimension_id: (projected_scores[dimension_id] / float(calibrated_total))
            for dimension_id in dimension_ids
        },
        debug,
    )


def score_text(text: str, spec: AxisSpec) -> Dict[str, float]:
    """Score text across axis dimensions by normalized keyword-hit ratios.

    The score means "how strongly each dimension is emphasized *relative to the
    other dimensions* by keyword presence". It is intentionally lightweight and
    deterministic, and should be interpreted as a heuristic projection.
    """

    scores, _ = score_text_with_debug(text, spec)
    return scores


@lru_cache(maxsize=1)
def _load_scoring_calibration_model() -> Optional[AxisCalibrationModel]:
    return load_calibration_model_from_env(env_var=_SCORING_CALIBRATION_ENV_VAR)


def _clear_scoring_calibration_model_cache() -> None:
    _load_scoring_calibration_model.cache_clear()


__all__ = [
    "score_text",
    "score_text_with_debug",
    "load_axis_spec",
    "AxisSpec",
    "_clear_scoring_calibration_model_cache",
]
