"""
Freedom Pressure Metric
=======================

A metric function for TensorEngine that computes freedom_pressure.
The key is that this metric ALWAYS returns a value (0.0 as stub).
This ensures SafetyMode never falls back to "missing" unnecessarily.

Future: Replace the stub with real computation based on
context complexity, user history, topic sensitivity, etc.
"""
from __future__ import annotations

from typing import Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot


def metric_freedom_pressure(ctx: Context, memory: MemorySnapshot) -> Tuple[str, float]:
    """
    Compute freedom_pressure metric.

    Args:
        ctx: Request context
        memory: Memory snapshot

    Returns:
        Tuple of ("freedom_pressure", value)

    Note:
        0.0〜1.0（高いほど縮退）
        まずはキーが常に出ることが重要。式は後で差し替える。
    """
    # TODO: Replace with real computation
    # For now, return 0.0 (NORMAL mode, no degradation)
    # This is intentionally permissive - real computation will be added later
    return "freedom_pressure", 0.0


__all__ = ["metric_freedom_pressure"]
