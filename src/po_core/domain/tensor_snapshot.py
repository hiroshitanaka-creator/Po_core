"""
TensorSnapshot - tensors層の出力はこれ"だけ"。計測のスナップショット。

This is the OUTPUT contract from the tensor layer.
It's immutable to ensure tensor values cannot be modified after computation.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional


# Backward compatibility: TensorValue for existing code
@dataclass(frozen=True)
class TensorValue:
    """
    A single tensor value with metadata (backward compat).
    """

    name: str
    value: float
    dimensions: Optional[Dict[str, float]] = None
    confidence: float = 1.0
    source: str = "computed"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result: Dict[str, Any] = {
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
    tensors層の出力はこれ"だけ"。計測のスナップショット。

    Attributes:
        computed_at: When the tensors were computed (UTC)
        metrics: Mapping of metric name to value
        version: Schema version for forward compatibility
        values: Dict of TensorValue objects (backward compat)
    """

    computed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metrics: Mapping[str, float] = field(default_factory=dict)
    version: str = "v1"

    # Backward compatibility fields
    values: Dict[str, TensorValue] = field(default_factory=dict)
    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    context_id: Optional[str] = None
    aggregate_metrics: Optional[Dict[str, float]] = None

    @staticmethod
    def empty() -> "TensorSnapshot":
        """Create an empty snapshot."""
        return TensorSnapshot(
            computed_at=datetime.now(timezone.utc),
            metrics={},
        )

    @staticmethod
    def now(metrics: Mapping[str, float]) -> "TensorSnapshot":
        """Create a snapshot with current timestamp."""
        return TensorSnapshot(
            computed_at=datetime.now(timezone.utc),
            metrics=dict(metrics),
        )

    def as_dict(self) -> Dict[str, float]:
        """Return metrics as a mutable dict."""
        if self.metrics:
            return dict(self.metrics)
        # Backward compat: extract from values
        return {name: tv.value for name, tv in self.values.items()}

    def get(self, key: str, default: float = 0.0) -> float:
        """Get a metric value with default."""
        if key in self.metrics:
            return self.metrics.get(key, default)
        # Backward compat: look in values
        if key in self.values:
            return self.values[key].value
        return default

    # Backward compat properties
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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result: Dict[str, Any] = {
            "computed_at": self.computed_at.isoformat(),
            "metrics": dict(self.metrics) if self.metrics else self.as_dict(),
            "version": self.version,
        }
        if self.values:
            result["values"] = {name: tv.to_dict() for name, tv in self.values.items()}
        if self.snapshot_id:
            result["snapshot_id"] = self.snapshot_id
        if self.context_id:
            result["context_id"] = self.context_id
        if self.aggregate_metrics:
            result["aggregate_metrics"] = dict(self.aggregate_metrics)
        return result


__all__ = ["TensorSnapshot", "TensorValue"]
