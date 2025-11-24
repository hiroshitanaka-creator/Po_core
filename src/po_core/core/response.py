"""Shared response schema for Po_core outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from po_core.po_self.schemas import AggregationTensors, PhilosopherContribution


@dataclass
class PoCoreResponse:
    """Container holding generated content and trace metadata."""

    text: str
    tensors: AggregationTensors
    contributions: List[PhilosopherContribution]
    trace_meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def freedom_pressure(self) -> float:
        return self.tensors.freedom_pressure

    @property
    def semantic_profile(self) -> List[float]:
        return self.tensors.semantic_profile

    @property
    def blocked_tensor(self) -> float:
        return self.tensors.blocked_tensor

    @property
    def philosophers_involved(self) -> List[str]:
        return [contribution.name for contribution in self.contributions]

    def trace_payload(self) -> Dict[str, Any]:
        """Return a lightweight payload suitable for Po_trace integration."""

        return {
            "text": self.text,
            "freedom_pressure": self.tensors.freedom_pressure,
            "semantic_profile": self.tensors.semantic_profile,
            "blocked_tensor": self.tensors.blocked_tensor,
            "contributions": [contribution.metadata for contribution in self.contributions],
            "trace_meta": self.trace_meta,
        }

    @classmethod
    def placeholder(
        cls,
        *,
        text: str = "",
        tensors: Optional[AggregationTensors] = None,
        contributions: Optional[List[PhilosopherContribution]] = None,
        trace_meta: Optional[Dict[str, Any]] = None,
    ) -> "PoCoreResponse":
        return cls(
            text=text,
            tensors=tensors or AggregationTensors(0.0, [], 0.0),
            contributions=contributions or [],
            trace_meta=trace_meta or {},
        )
