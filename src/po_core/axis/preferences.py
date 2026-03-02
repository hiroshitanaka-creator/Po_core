"""Preference weight parsing and alignment utilities for axis vectors."""

from __future__ import annotations

import math
from typing import Dict, List


def parse_weights_str(s: str) -> Dict[str, float]:
    """Parse comma-separated ``name:value`` weights into a dictionary."""
    weights: Dict[str, float] = {}
    if not isinstance(s, str):
        return weights

    for raw_part in s.split(","):
        part = raw_part.strip()
        if not part or ":" not in part:
            continue
        dim, raw_value = part.split(":", 1)
        key = dim.strip()
        value_text = raw_value.strip()
        if not key:
            continue
        try:
            weights[key] = float(value_text)
        except (TypeError, ValueError):
            continue

    return weights


def normalize_weights(weights: Dict[str, float], dims: List[str]) -> Dict[str, float]:
    """Normalize weights over ``dims`` with deterministic fallback behavior."""
    ordered_dims = [str(dim) for dim in dims]
    if not ordered_dims:
        return {}

    invalid = False
    normalized: Dict[str, float] = {}
    for dim in ordered_dims:
        value = weights.get(dim, 0.0)
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            invalid = True
            break
        value_f = float(value)
        if value_f < 0:
            invalid = True
            break
        normalized[dim] = value_f

    if invalid:
        uniform = 1.0 / float(len(ordered_dims))
        return {dim: uniform for dim in ordered_dims}

    total = sum(normalized.values())
    if total <= 0:
        uniform = 1.0 / float(len(ordered_dims))
        return {dim: uniform for dim in ordered_dims}

    return {dim: normalized[dim] / total for dim in ordered_dims}


def alignment(axis_scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """Compute weighted alignment as a dot product."""
    score = 0.0
    for dim, weight in weights.items():
        value = axis_scores.get(dim, 0.0)
        if isinstance(value, (int, float)):
            score += float(value) * float(weight)
    return score
