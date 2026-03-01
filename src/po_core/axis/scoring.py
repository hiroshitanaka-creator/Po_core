"""Deterministic axis scoring based on keyword-hit ratio.

This module projects free-form proposal text into axis scores by counting
whether dimension-specific keywords appear in normalized text.
The resulting score expresses a *relative emphasis* among dimensions
(keyword-hit ratio), not a semantic truth estimate.
"""

from __future__ import annotations

from typing import Dict

from po_core.axis.spec import AxisSpec, load_axis_spec
from po_core.text.normalize import normalize_text

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


def score_text(text: str, spec: AxisSpec) -> Dict[str, float]:
    """Score text across axis dimensions by normalized keyword-hit ratios.

    The score means "how strongly each dimension is emphasized *relative to the
    other dimensions* by keyword presence". It is intentionally lightweight and
    deterministic, and should be interpreted as a heuristic projection.
    """

    normalized = normalize_text(text)
    dimension_ids = [d.dimension_id for d in spec.dimensions]
    if not dimension_ids:
        return {}

    hits_by_dimension: dict[str, int] = {}
    for dimension_id in dimension_ids:
        keywords = _KEYWORDS_BY_DIMENSION.get(dimension_id, ())
        hits = sum(1 for kw in keywords if kw in normalized)
        hits_by_dimension[dimension_id] = hits

    total_hits = sum(hits_by_dimension.values())
    if total_hits <= 0:
        uniform = 1.0 / float(len(dimension_ids))
        return {dimension_id: uniform for dimension_id in dimension_ids}

    return {
        dimension_id: (hits_by_dimension[dimension_id] / float(total_hits))
        for dimension_id in dimension_ids
    }


__all__ = ["score_text", "load_axis_spec", "AxisSpec"]
