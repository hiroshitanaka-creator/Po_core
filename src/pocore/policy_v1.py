"""src/pocore/policy_v1.py — Recommendation arbitration policy constants (v1)."""

from __future__ import annotations

from typing import Any, Dict

UNKNOWN_BLOCK = 4
UNKNOWN_SOFT = 1
TIME_PRESSURE_DAYS = 7



def should_block_recommendation(features: Dict[str, Any]) -> bool:
    """Return True when missing critical information should block recommendation."""
    unknowns_count = int(features.get("unknowns_count", 0) or 0)
    return unknowns_count >= UNKNOWN_BLOCK



def has_time_pressure_with_unknowns(features: Dict[str, Any]) -> bool:
    """Return True when deadline is near and unknowns remain."""
    days_to_deadline = features.get("days_to_deadline")
    unknowns_count = int(features.get("unknowns_count", 0) or 0)
    return (
        isinstance(days_to_deadline, int)
        and days_to_deadline <= TIME_PRESSURE_DAYS
        and unknowns_count > 0
    )
