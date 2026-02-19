"""
Tensor Engine
=============

The unified entry point for tensor computation.

This module provides a clean API for computing tensors.
All tensor computation should go through this module.

DEPENDENCY RULES:
- This module can import from: tensors/* (siblings), domain/*
- This module MUST NOT import from: philosophers/*, safety/*, ensemble.py

OUTPUT:
- Returns TensorSnapshot from domain/tensor_snapshot.py
- Never returns raw numpy arrays or internal objects

USAGE:
    from po_core.tensors.engine import compute_tensors

    snapshot = compute_tensors(prompt, context_id="abc123")
    print(snapshot.freedom_pressure)  # 0.7
"""

import os
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from po_core.domain.context import Context
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.tensor_snapshot import TensorSnapshot, TensorValue
from po_core.tensors.freedom_pressure import FreedomPressureTensor
from po_core.tensors.freedom_pressure_v2 import FreedomPressureV2, create_freedom_pressure_v2

# Type alias for metric functions
MetricFn = Callable[[Context, MemorySnapshot], Tuple[str, float]]


class TensorEngine:
    """
    TensorEngine implements TensorEnginePort.

    Computes tensor metrics from context and memory.
    """

    def __init__(self, metrics: Iterable[MetricFn] = ()):
        self._metrics = list(metrics)

    def compute(self, ctx: Context, memory: MemorySnapshot) -> TensorSnapshot:
        """Compute tensors from context and memory."""
        values: Dict[str, float] = {}
        for fn in self._metrics:
            k, v = fn(ctx, memory)
            values[k] = float(v)

        return TensorSnapshot(
            computed_at=datetime.now(timezone.utc),
            metrics=values,
            version="v1",
        )


def compute_tensors(
    prompt: str,
    *,
    context_id: Optional[str] = None,
    reasoning_text: Optional[str] = None,
    philosopher_perspectives: Optional[List[Dict[str, Any]]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> TensorSnapshot:
    """
    Compute all tensors for a given prompt.

    This is the main entry point for tensor computation.
    Returns an immutable TensorSnapshot.

    Args:
        prompt: The input prompt
        context_id: Optional context ID for correlation
        reasoning_text: Optional reasoning text for semantic analysis
        philosopher_perspectives: Optional list of philosopher analyses
        context: Optional context dictionary with modifiers

    Returns:
        TensorSnapshot with all computed tensor values
    """
    values: Dict[str, TensorValue] = {}

    # Compute Freedom Pressure
    # Feature flag: PO_FREEDOM_PRESSURE_V2=true → ML-native FreedomPressureV2
    _use_v2 = os.getenv("PO_FREEDOM_PRESSURE_V2", "").lower() in ("1", "true", "yes")
    if _use_v2:
        _fp_v2 = create_freedom_pressure_v2()
        memory_depth = len(context.get("memory_items", [])) if context else 0
        _fp_snapshot = _fp_v2.compute_v2(prompt, memory_depth=memory_depth)
        fp_value = _fp_snapshot.overall
        fp_dimensions: Dict[str, float] = dict(_fp_snapshot.values)
        fp_dimensions["coherence_score"] = _fp_snapshot.coherence_score
        fp_source = f"FreedomPressureV2/{_fp_snapshot.backend}"
    else:
        fp_tensor = FreedomPressureTensor()
        fp_tensor.compute(
            prompt,
            context=context,
            philosopher_perspectives=philosopher_perspectives,
        )
        fp_value = float(fp_tensor.norm())  # Overall pressure is the norm
        fp_dimensions = fp_tensor.get_pressure_summary()
        fp_source = "FreedomPressureTensor"

    values["freedom_pressure"] = TensorValue(
        name="freedom_pressure",
        value=fp_value,
        dimensions=fp_dimensions,
        source=fp_source,
    )

    # Compute Semantic Delta (simple token-based)
    semantic_delta = compute_semantic_delta(prompt, reasoning_text)
    values["semantic_delta"] = TensorValue(
        name="semantic_delta",
        value=semantic_delta,
        source="token_overlap",
    )

    # Compute Blocked Tensor (derived)
    blocked_tensor = compute_blocked_tensor(fp_value, semantic_delta)
    values["blocked_tensor"] = TensorValue(
        name="blocked_tensor",
        value=blocked_tensor,
        source="derived",
    )

    # Aggregate metrics
    aggregate_metrics = {
        "freedom_pressure": fp_value,
        "semantic_delta": semantic_delta,
        "blocked_tensor": blocked_tensor,
    }

    return TensorSnapshot(
        values=values,
        context_id=context_id,
        aggregate_metrics=aggregate_metrics,
    )


def compute_freedom_pressure(
    prompt: str,
    *,
    context: Optional[Dict[str, Any]] = None,
    philosopher_perspectives: Optional[List[Dict[str, Any]]] = None,
) -> TensorValue:
    """
    Compute Freedom Pressure tensor.

    Args:
        prompt: The input prompt
        context: Optional context dictionary
        philosopher_perspectives: Optional philosopher analyses

    Returns:
        TensorValue with freedom pressure
    """
    fp_tensor = FreedomPressureTensor()
    fp_tensor.compute(
        prompt,
        context=context,
        philosopher_perspectives=philosopher_perspectives,
    )

    return TensorValue(
        name="freedom_pressure",
        value=float(fp_tensor.norm()),
        dimensions=fp_tensor.get_pressure_summary(),
        source="FreedomPressureTensor",
    )


def compute_semantic_delta(
    prompt: str,
    reasoning_text: Optional[str] = None,
) -> float:
    """
    Compute semantic delta between prompt and reasoning.

    Measures how much the reasoning diverges from the prompt.
    A higher value means more divergence.

    Args:
        prompt: The input prompt
        reasoning_text: The reasoning text (if None, returns 1.0)

    Returns:
        Semantic delta in [0, 1]
    """
    if not reasoning_text:
        return 1.0

    prompt_tokens = set(_tokenize(prompt))
    reasoning_tokens = set(_tokenize(reasoning_text))

    if not prompt_tokens or not reasoning_tokens:
        return 1.0

    overlap = len(prompt_tokens & reasoning_tokens)
    coverage = overlap / len(prompt_tokens)
    return round(1 - coverage, 2)


def compute_blocked_tensor(
    freedom_pressure: float,
    semantic_delta: float,
) -> float:
    """
    Compute blocked tensor from freedom pressure and semantic delta.

    The blocked tensor represents the degree to which reasoning
    is blocked or constrained.

    Args:
        freedom_pressure: Freedom pressure value
        semantic_delta: Semantic delta value

    Returns:
        Blocked tensor in [0, 1]
    """
    return round(max(0.0, (1 - freedom_pressure) * 0.5 + semantic_delta * 0.5), 2)


def _tokenize(text: str) -> List[str]:
    """
    Simple tokenizer for text analysis.

    Args:
        text: Text to tokenize

    Returns:
        List of lowercase tokens
    """
    tokens: List[str] = []
    for raw in text.split():
        cleaned = raw.strip(".,!?\"'()[]{}:;`").lower()
        if cleaned:
            tokens.append(cleaned)
    return tokens


# Simple functions for backward compatibility with ensemble.py
def compute_freedom_pressure_simple(reasoning: str) -> float:
    """
    Simple freedom pressure computation (backward compat).

    Used by ensemble.py. Returns the unique token ratio.
    """
    tokens = _tokenize(reasoning)
    if not tokens:
        return 0.35
    unique_ratio = len(set(tokens)) / len(tokens)
    return round(0.35 + 0.65 * unique_ratio, 2)


def compute_semantic_delta_simple(prompt: str, reasoning: str) -> float:
    """
    Simple semantic delta computation (backward compat).

    Used by ensemble.py.
    """
    return compute_semantic_delta(prompt, reasoning)


def compute_blocked_tensor_simple(
    freedom_pressure: float, semantic_delta: float
) -> float:
    """
    Simple blocked tensor computation (backward compat).

    Used by ensemble.py.
    """
    return compute_blocked_tensor(freedom_pressure, semantic_delta)


__all__ = [
    # Port implementation
    "TensorEngine",
    "MetricFn",
    # Main API
    "compute_tensors",
    # Individual tensor computations
    "compute_freedom_pressure",
    "compute_semantic_delta",
    "compute_blocked_tensor",
    # Phase 6-A: ML-native Freedom Pressure
    "FreedomPressureV2",
    "create_freedom_pressure_v2",
    # Backward compat (will be deprecated)
    "compute_freedom_pressure_simple",
    "compute_semantic_delta_simple",
    "compute_blocked_tensor_simple",
]
