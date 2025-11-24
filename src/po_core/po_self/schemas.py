"""Schemas used by the Po_self package."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PhilosopherContribution:
    """Normalized contribution emitted by a philosopher adapter."""

    name: str
    summary: str
    freedom_scalar: float
    semantic_vector: List[float]
    blocked_scalar: float
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass
class AggregationTensors:
    """Aggregated tensor-like signals derived from philosopher contributions."""

    freedom_pressure: float
    semantic_profile: List[float]
    blocked_tensor: float


@dataclass
class AggregationResult:
    """Bundle holding philosopher contributions alongside aggregated tensors."""

    contributions: List[PhilosopherContribution]
    tensors: AggregationTensors
    prompt: str
    seed: Optional[int] = None
