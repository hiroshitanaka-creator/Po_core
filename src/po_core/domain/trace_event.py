"""
TraceEvent - Trace events for audit trail.

This is what the trace/ module records.
All significant events in the system are captured as TraceEvents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class TraceEventType(str, Enum):
    """Types of trace events.

    These represent the key events in the reasoning pipeline.
    Used for observability and debugging.
    """

    # Context events
    CONTEXT_CREATED = "context_created"
    CONTEXT_ENRICHED = "context_enriched"

    # Tensor events
    TENSOR_COMPUTED = "tensor_computed"
    TENSOR_SNAPSHOT_CREATED = "tensor_snapshot_created"

    # Autonomy/Will events (for Solar Will integration)
    WILL_UPDATED = "will_updated"
    INTENT_GENERATED = "intent_generated"
    GOAL_CANDIDATES_GENERATED = "goal_candidates_generated"

    # Philosopher events
    PHILOSOPHER_STARTED = "philosopher_started"
    PHILOSOPHER_COMPLETED = "philosopher_completed"
    PHILOSOPHER_REASONING = "philosopher_reasoning"

    # Proposal events
    PROPOSAL_CREATED = "proposal_created"
    PROPOSAL_AGGREGATED = "proposal_aggregated"

    # Safety events
    SAFETY_CHECK_STARTED = "safety_check_started"
    VIOLATION_DETECTED = "violation_detected"
    REPAIR_ATTEMPTED = "repair_attempted"
    REPAIR_SUCCEEDED = "repair_succeeded"
    REPAIR_FAILED = "repair_failed"
    SAFETY_VERDICT_ISSUED = "safety_verdict_issued"

    # Ensemble events
    ENSEMBLE_STARTED = "ensemble_started"
    ENSEMBLE_COMPLETED = "ensemble_completed"
    CONSENSUS_REACHED = "consensus_reached"

    # Decision events
    DECISION_MADE = "decision_made"
    DECISION_BLOCKED = "decision_blocked"
    DECISION_ESCALATED = "decision_escalated"

    # System events
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


@dataclass
class TraceEvent:
    """
    A single trace event.

    Trace events are the atomic units of the audit trail.
    They should be:
    - Immutable (don't modify after creation)
    - Self-contained (include all context needed)
    - Structured (use the data dict for typed content)

    Attributes:
        event_type: Type of event
        source: Source component (e.g., 'ensemble', 'wethics_gate', 'aristotle')
        message: Human-readable description
        event_id: Unique event identifier
        timestamp: When the event occurred
        session_id: Session this event belongs to
        context_id: Context this event relates to
        proposal_id: Proposal this event relates to (if applicable)
        data: Structured event data
        metadata: Additional metadata
    """

    event_type: TraceEventType
    """Type of event."""

    source: str
    """Source component."""

    message: str
    """Human-readable description."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique event identifier."""

    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    """Event timestamp."""

    session_id: Optional[str] = None
    """Session this event belongs to."""

    context_id: Optional[str] = None
    """Context this event relates to."""

    proposal_id: Optional[str] = None
    """Proposal this event relates to."""

    data: Dict[str, Any] = field(default_factory=dict)
    """Structured event data."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""

    @property
    def level(self) -> str:
        """Get the log level for this event type."""
        if self.event_type == TraceEventType.ERROR:
            return "ERROR"
        elif self.event_type == TraceEventType.WARNING:
            return "WARNING"
        elif self.event_type == TraceEventType.DEBUG:
            return "DEBUG"
        elif self.event_type in (
            TraceEventType.VIOLATION_DETECTED,
            TraceEventType.DECISION_BLOCKED,
        ):
            return "WARNING"
        else:
            return "INFO"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source": self.source,
            "message": self.message,
            "timestamp": self.timestamp,
            "level": self.level,
        }
        if self.session_id:
            result["session_id"] = self.session_id
        if self.context_id:
            result["context_id"] = self.context_id
        if self.proposal_id:
            result["proposal_id"] = self.proposal_id
        if self.data:
            result["data"] = self.data
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def tensor_computed(
        cls,
        tensor_name: str,
        value: float,
        session_id: Optional[str] = None,
        context_id: Optional[str] = None,
        dimensions: Optional[Dict[str, float]] = None,
    ) -> "TraceEvent":
        """Create a TENSOR_COMPUTED event."""
        data: Dict[str, Any] = {"tensor_name": tensor_name, "value": value}
        if dimensions:
            data["dimensions"] = dimensions
        return cls(
            event_type=TraceEventType.TENSOR_COMPUTED,
            source="tensors",
            message=f"Computed {tensor_name}: {value:.3f}",
            session_id=session_id,
            context_id=context_id,
            data=data,
        )

    @classmethod
    def philosopher_reasoning(
        cls,
        philosopher_name: str,
        perspective: str,
        session_id: Optional[str] = None,
        context_id: Optional[str] = None,
        metrics: Optional[Dict[str, float]] = None,
    ) -> "TraceEvent":
        """Create a PHILOSOPHER_REASONING event."""
        data: Dict[str, Any] = {
            "philosopher": philosopher_name,
            "perspective": perspective,
        }
        if metrics:
            data["metrics"] = metrics
        return cls(
            event_type=TraceEventType.PHILOSOPHER_REASONING,
            source=f"philosopher.{philosopher_name.lower().replace(' ', '_')}",
            message=f"{philosopher_name} reasoned from {perspective}",
            session_id=session_id,
            context_id=context_id,
            data=data,
        )

    @classmethod
    def safety_verdict(
        cls,
        verdict_type: str,
        proposal_id: str,
        session_id: Optional[str] = None,
        violations_count: int = 0,
        was_repaired: bool = False,
        explanation: str = "",
    ) -> "TraceEvent":
        """Create a SAFETY_VERDICT_ISSUED event."""
        return cls(
            event_type=TraceEventType.SAFETY_VERDICT_ISSUED,
            source="wethics_gate",
            message=f"Safety verdict: {verdict_type}",
            session_id=session_id,
            proposal_id=proposal_id,
            data={
                "verdict_type": verdict_type,
                "violations_count": violations_count,
                "was_repaired": was_repaired,
                "explanation": explanation,
            },
        )

    @classmethod
    def ensemble_completed(
        cls,
        philosophers_count: int,
        consensus_leader: Optional[str],
        session_id: Optional[str] = None,
        context_id: Optional[str] = None,
        metrics: Optional[Dict[str, float]] = None,
    ) -> "TraceEvent":
        """Create an ENSEMBLE_COMPLETED event."""
        data: Dict[str, Any] = {
            "philosophers_count": philosophers_count,
            "consensus_leader": consensus_leader,
        }
        if metrics:
            data["metrics"] = metrics
        return cls(
            event_type=TraceEventType.ENSEMBLE_COMPLETED,
            source="ensemble",
            message=f"Ensemble completed with {philosophers_count} philosophers, leader: {consensus_leader}",
            session_id=session_id,
            context_id=context_id,
            data=data,
        )


__all__ = ["TraceEvent", "TraceEventType"]
