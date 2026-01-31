"""
TensorSnapshot - Immutable snapshot of tensor values.

This is what the tensors/ module OUTPUTS.
It's a pure data transfer object with no computation logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid


@dataclass(frozen=True)
class TensorValue:
    """
    A single tensor value with metadata.

    This represents one measured quantity (e.g., Freedom Pressure).
    """

    name: str
    """Name of the tensor (e.g., 'freedom_pressure')."""

    value: float
    """The computed value, typically in [0, 1]."""

    dimensions: Optional[Dict[str, float]] = None
    """Optional breakdown by dimension."""

    confidence: float = 1.0
    """Confidence in this measurement."""

    source: str = "computed"
    """How this value was obtained."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
        }
        if self.dimensions:
            result["dimensions"] = dict(self.dimensions)
        return result


@dataclass(frozen=True)
class TensorSnapshot:
    """
    Immutable snapshot of all tensor values at a point in time.

    This is the OUTPUT contract from the tensors/ module.
    It's frozen to ensure tensor values cannot be modified after computation.

    The ensemble system uses this to:
    1. Pass tensor values to philosophers as context
    2. Include tensor values in proposals for safety evaluation
    3. Log tensor values in trace events

    Attributes:
        snapshot_id: Unique identifier for this snapshot
        created_at: When this snapshot was taken
        context_id: ID of the context this was computed for
        values: Dictionary of tensor name -> TensorValue
        aggregate_metrics: Computed aggregate metrics
        metadata: Additional metadata
    """

    values: Dict[str, TensorValue]
    """All tensor values in this snapshot."""

    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique snapshot identifier."""

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    """Creation timestamp."""

    context_id: Optional[str] = None
    """ID of the context this was computed for."""

    aggregate_metrics: Optional[Dict[str, float]] = None
    """Computed aggregate metrics across all tensors."""

    metadata: Optional[Dict[str, Any]] = None
    """Additional metadata."""

    def get(self, name: str, default: float = 0.0) -> float:
        """Get a tensor value by name."""
        if name in self.values:
            return self.values[name].value
        return default

    def get_tensor(self, name: str) -> Optional[TensorValue]:
        """Get the full TensorValue object."""
        return self.values.get(name)

    @property
    def freedom_pressure(self) -> float:
        """Shortcut for freedom_pressure value."""
        return self.get("freedom_pressure", 0.5)

    @property
    def semantic_delta(self) -> float:
        """Shortcut for semantic_delta value."""
        return self.get("semantic_delta", 0.5)

    @property
    def blocked_tensor(self) -> float:
        """Shortcut for blocked_tensor value."""
        return self.get("blocked_tensor", 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "values": {name: tv.to_dict() for name, tv in self.values.items()},
        }
        if self.context_id:
            result["context_id"] = self.context_id
        if self.aggregate_metrics:
            result["aggregate_metrics"] = dict(self.aggregate_metrics)
        if self.metadata:
            result["metadata"] = dict(self.metadata)
        return result

    def to_flat_dict(self) -> Dict[str, float]:
        """Convert to a flat dictionary of name -> value."""
        return {name: tv.value for name, tv in self.values.items()}

    @classmethod
    def from_flat_dict(
        cls,
        values: Dict[str, float],
        context_id: Optional[str] = None,
    ) -> "TensorSnapshot":
        """Create a snapshot from a flat dictionary of values."""
        tensor_values = {
            name: TensorValue(name=name, value=value)
            for name, value in values.items()
        }
        return cls(values=tensor_values, context_id=context_id)

    @classmethod
    def empty(cls, context_id: Optional[str] = None) -> "TensorSnapshot":
        """Create an empty snapshot."""
        return cls(values={}, context_id=context_id)


__all__ = ["TensorSnapshot", "TensorValue"]
