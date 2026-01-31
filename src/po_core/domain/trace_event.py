"""
TraceEvent - 観測可能性の単位。viewerはこれだけ見ればよい。

Trace events are the atomic units of the audit trail.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class TraceEvent:
    """
    観測可能性の単位。viewerはこれだけ見ればよい。

    Attributes:
        event_type: Type of event (e.g., "TensorComputed", "WillUpdated")
        occurred_at: When the event occurred (UTC)
        correlation_id: Usually Context.request_id for tracing
        payload: Event-specific structured data
    """

    event_type: str  # 例: "TensorComputed", "WillUpdated", ...
    occurred_at: datetime
    correlation_id: str  # 通常は Context.request_id を入れる
    payload: Mapping[str, Any] = field(default_factory=dict)

    @staticmethod
    def now(
        event_type: str,
        correlation_id: str,
        payload: Optional[Mapping[str, Any]] = None,
    ) -> "TraceEvent":
        """Create a trace event with current timestamp."""
        return TraceEvent(
            event_type=event_type,
            occurred_at=datetime.now(timezone.utc),
            correlation_id=correlation_id,
            payload=dict(payload or {}),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": self.correlation_id,
            "payload": dict(self.payload),
        }


__all__ = ["TraceEvent"]
