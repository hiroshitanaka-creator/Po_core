"""
Reasoning Tracer

Comprehensive logging system for tracking philosophical reasoning processes.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json


class TraceLevel(Enum):
    """Trace logging levels."""

    DEBUG = "debug"
    INFO = "info"
    REASONING = "reasoning"
    DECISION = "decision"
    BLOCKED = "blocked"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class TraceEntry:
    """
    Single entry in the reasoning trace.

    Attributes:
        timestamp: When the entry was created
        level: Logging level
        philosopher: Philosopher involved (if applicable)
        event: Event type/name
        message: Descriptive message
        data: Additional structured data
        metadata: Extra metadata
    """

    timestamp: str
    level: TraceLevel
    event: str
    message: str
    philosopher: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "event": self.event,
            "philosopher": self.philosopher,
            "message": self.message,
            "data": self.data,
            "metadata": self.metadata,
        }


class ReasoningTracer:
    """
    Comprehensive reasoning trace logger.

    Tracks the complete philosophical reasoning process including:
    - Philosopher activations and reasoning
    - Tensor computations
    - Blocked/rejected content
    - Decision points
    - Semantic evolution
    """

    def __init__(
        self,
        trace_id: Optional[str] = None,
        prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize reasoning tracer.

        Args:
            trace_id: Unique identifier for this trace
            prompt: Input prompt being processed
            metadata: Additional metadata
        """
        self.trace_id = trace_id or self._generate_trace_id()
        self.prompt = prompt
        self.metadata = metadata or {}

        # Trace entries
        self.entries: List[TraceEntry] = []

        # Start time
        self.started_at = datetime.utcnow().isoformat() + "Z"
        self.completed_at: Optional[str] = None

        # Statistics
        self.stats = {
            "total_entries": 0,
            "by_level": {level.value: 0 for level in TraceLevel},
            "by_philosopher": {},
            "blocked_count": 0,
        }

        # Log start
        self.log_event(
            level=TraceLevel.INFO,
            event="trace_started",
            message=f"Reasoning trace started: {self.trace_id}",
            data={"prompt": prompt, "metadata": metadata},
        )

    def _generate_trace_id(self) -> str:
        """Generate unique trace ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        return f"trace_{timestamp}"

    def log_event(
        self,
        level: TraceLevel,
        event: str,
        message: str,
        philosopher: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceEntry:
        """
        Log a reasoning event.

        Args:
            level: Trace level
            event: Event type/name
            message: Descriptive message
            philosopher: Philosopher involved
            data: Additional data
            metadata: Extra metadata

        Returns:
            Created trace entry
        """
        entry = TraceEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            level=level,
            event=event,
            message=message,
            philosopher=philosopher,
            data=data or {},
            metadata=metadata or {},
        )

        self.entries.append(entry)

        # Update statistics
        self.stats["total_entries"] += 1
        self.stats["by_level"][level.value] += 1

        if philosopher:
            if philosopher not in self.stats["by_philosopher"]:
                self.stats["by_philosopher"][philosopher] = 0
            self.stats["by_philosopher"][philosopher] += 1

        if level == TraceLevel.BLOCKED:
            self.stats["blocked_count"] += 1

        return entry

    def log_philosopher_reasoning(
        self,
        philosopher: str,
        reasoning: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceEntry:
        """
        Log philosopher reasoning.

        Args:
            philosopher: Philosopher name
            reasoning: Reasoning result dictionary
            metadata: Additional metadata

        Returns:
            Created trace entry
        """
        return self.log_event(
            level=TraceLevel.REASONING,
            event="philosopher_reasoning",
            message=f"{philosopher} completed reasoning",
            philosopher=philosopher,
            data={"reasoning": reasoning},
            metadata=metadata,
        )

    def log_blocked_content(
        self,
        content: str,
        reason: str,
        philosopher: Optional[str] = None,
        alternative: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceEntry:
        """
        Log blocked/rejected content.

        Args:
            content: What was blocked
            reason: Why it was blocked
            philosopher: Who blocked it
            alternative: What was chosen instead
            metadata: Additional metadata

        Returns:
            Created trace entry
        """
        return self.log_event(
            level=TraceLevel.BLOCKED,
            event="content_blocked",
            message=f"Content blocked: {reason}",
            philosopher=philosopher,
            data={
                "blocked_content": content,
                "reason": reason,
                "alternative": alternative,
            },
            metadata=metadata,
        )

    def log_tensor_computation(
        self,
        tensor_name: str,
        tensor_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceEntry:
        """
        Log tensor computation.

        Args:
            tensor_name: Name of the tensor
            tensor_data: Tensor data/result
            metadata: Additional metadata

        Returns:
            Created trace entry
        """
        return self.log_event(
            level=TraceLevel.INFO,
            event="tensor_computed",
            message=f"Computed {tensor_name}",
            data={"tensor_name": tensor_name, "tensor_data": tensor_data},
            metadata=metadata,
        )

    def log_decision(
        self,
        decision: str,
        reasoning: str,
        alternatives: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceEntry:
        """
        Log a decision point.

        Args:
            decision: Decision made
            reasoning: Reasoning behind decision
            alternatives: Alternative options considered
            metadata: Additional metadata

        Returns:
            Created trace entry
        """
        return self.log_event(
            level=TraceLevel.DECISION,
            event="decision_made",
            message=f"Decision: {decision}",
            data={
                "decision": decision,
                "reasoning": reasoning,
                "alternatives": alternatives or [],
            },
            metadata=metadata,
        )

    def complete(self, result: Optional[Dict[str, Any]] = None) -> None:
        """
        Mark trace as completed.

        Args:
            result: Final result (optional)
        """
        self.completed_at = datetime.utcnow().isoformat() + "Z"

        self.log_event(
            level=TraceLevel.INFO,
            event="trace_completed",
            message="Reasoning trace completed",
            data={"result": result, "statistics": self.stats},
        )

    def get_entries_by_level(self, level: TraceLevel) -> List[TraceEntry]:
        """
        Get entries by trace level.

        Args:
            level: Trace level to filter by

        Returns:
            Filtered list of entries
        """
        return [entry for entry in self.entries if entry.level == level]

    def get_entries_by_philosopher(self, philosopher: str) -> List[TraceEntry]:
        """
        Get entries by philosopher.

        Args:
            philosopher: Philosopher name

        Returns:
            Filtered list of entries
        """
        return [entry for entry in self.entries if entry.philosopher == philosopher]

    def get_blocked_content(self) -> List[TraceEntry]:
        """
        Get all blocked content entries.

        Returns:
            List of blocked content entries
        """
        return self.get_entries_by_level(TraceLevel.BLOCKED)

    def get_timeline(self) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of reasoning.

        Returns:
            List of entry dictionaries in chronological order
        """
        return [entry.to_dict() for entry in self.entries]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert trace to dictionary.

        Returns:
            Complete trace as dictionary
        """
        return {
            "trace_id": self.trace_id,
            "prompt": self.prompt,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self._calculate_duration(),
            "metadata": self.metadata,
            "statistics": self.stats,
            "entries": self.get_timeline(),
        }

    def _calculate_duration(self) -> Optional[float]:
        """Calculate trace duration in seconds."""
        if not self.completed_at:
            return None

        start = datetime.fromisoformat(self.started_at.replace("Z", "+00:00"))
        end = datetime.fromisoformat(self.completed_at.replace("Z", "+00:00"))
        return (end - start).total_seconds()

    def export_json(self, filepath: Optional[str] = None) -> str:
        """
        Export trace to JSON.

        Args:
            filepath: Optional file path to save to

        Returns:
            JSON string
        """
        json_str = json.dumps(self.to_dict(), indent=2)

        if filepath:
            with open(filepath, "w") as f:
                f.write(json_str)

        return json_str

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ReasoningTracer(trace_id='{self.trace_id}', "
            f"entries={len(self.entries)}, "
            f"completed={self.completed_at is not None})"
        )
