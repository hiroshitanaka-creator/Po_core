"""Preference-weight overlay for trade-off map views."""

from __future__ import annotations

import copy
from typing import Any, Dict, List

from po_core.axis.preferences import alignment, normalize_weights


def _infer_dims(axis: Dict[str, Any]) -> List[str]:
    scoreboard = axis.get("scoreboard")
    if isinstance(scoreboard, dict) and scoreboard:
        return sorted(str(key) for key in scoreboard.keys())

    axis_vectors = axis.get("axis_vectors")
    dims: set[str] = set()
    if isinstance(axis_vectors, list):
        for item in axis_vectors:
            if not isinstance(item, dict):
                continue
            axis_scores = item.get("axis_scores")
            if not isinstance(axis_scores, dict):
                continue
            for key in axis_scores.keys():
                dims.add(str(key))
    return sorted(dims)


def apply_preference_view(
    tradeoff_map: dict, weights: Dict[str, float] | None = None
) -> dict:
    """Return a deep-copied tradeoff map with ``axis.preference_view`` injected."""
    result = copy.deepcopy(tradeoff_map)
    axis = result.get("axis")
    if not isinstance(axis, dict):
        return result

    dims = _infer_dims(axis)
    normalized_weights = normalize_weights(weights or {}, dims)

    alignment_by_author: Dict[str, float] = {}
    axis_vectors = axis.get("axis_vectors")
    if isinstance(axis_vectors, list):
        for item in axis_vectors:
            if not isinstance(item, dict):
                continue
            author = item.get("author")
            axis_scores = item.get("axis_scores")
            if not author or not isinstance(axis_scores, dict):
                continue
            alignment_by_author[str(author)] = alignment(
                axis_scores, normalized_weights
            )

    ranked_authors = [
        author
        for author, _ in sorted(
            alignment_by_author.items(),
            key=lambda pair: (-pair[1], pair[0]),
        )
    ]

    axis["preference_view"] = {
        "weights_used": normalized_weights,
        "ranked_authors": ranked_authors,
        "alignment_by_author": alignment_by_author,
    }
    return result
