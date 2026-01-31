"""
Memory Port
===========

Abstract interface for memory/self systems.

This port defines how the core system interacts with memory,
WITHOUT knowing the concrete implementation (Po_self, etc.).

Key principle: Core modules (philosophers, tensors, autonomy)
can read MemorySnapshot but cannot modify memory directly.
Only the runtime/wiring layer connects to concrete memory.

DEPENDENCY RULES:
- This file depends ONLY on: stdlib, typing
- This file MUST NOT import from any po_core modules
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid


@dataclass(frozen=True)
class MemorySnapshot:
    """
    Read-only snapshot of memory state.

    This is what philosophers/tensors/autonomy can see.
    They cannot modify the original memory, only observe this snapshot.

    Attributes:
        snapshot_id: Unique identifier
        session_id: Current session ID
        created_at: When this snapshot was taken
        conversation_history: Recent conversation turns
        philosopher_states: State info per philosopher (read-only)
        metrics_history: Historical metrics
        metadata: Additional context
    """

    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    conversation_history: tuple = ()  # Immutable tuple of (role, content) pairs
    philosopher_states: Optional[Dict[str, Dict[str, Any]]] = None
    metrics_history: Optional[Dict[str, List[float]]] = None
    metadata: Optional[Dict[str, Any]] = None

    def get_recent_turns(self, n: int = 5) -> List[Dict[str, str]]:
        """Get the n most recent conversation turns."""
        return [
            {"role": role, "content": content}
            for role, content in self.conversation_history[-n:]
        ]

    def get_philosopher_state(self, name: str) -> Optional[Dict[str, Any]]:
        """Get state for a specific philosopher."""
        if self.philosopher_states:
            return self.philosopher_states.get(name.lower())
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result: Dict[str, Any] = {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
        }
        if self.session_id:
            result["session_id"] = self.session_id
        if self.conversation_history:
            result["conversation_history"] = [
                {"role": r, "content": c} for r, c in self.conversation_history
            ]
        if self.philosopher_states:
            result["philosopher_states"] = self.philosopher_states
        if self.metrics_history:
            result["metrics_history"] = self.metrics_history
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class MemoryQuery:
    """
    Query for memory retrieval.

    Used to request specific information from memory
    without accessing it directly.
    """

    query_type: str  # "recent_history", "philosopher_state", "metrics"
    parameters: Dict[str, Any] = field(default_factory=dict)


class MemoryPort(ABC):
    """
    Abstract port for memory operations.

    Implementations:
    - adapters/memory_poself.py: Wraps Po_self
    - adapters/memory_inmemory.py: In-memory for testing

    Usage in core:
        # In runtime/wiring.py
        memory: MemoryPort = PoSelfMemoryAdapter()

        # In ensemble.py (receives via DI)
        snapshot = memory.get_snapshot()
        # Philosophers can only read the snapshot

    NEVER import concrete implementations in core modules.
    """

    @abstractmethod
    def get_snapshot(self, session_id: Optional[str] = None) -> MemorySnapshot:
        """
        Get a read-only snapshot of current memory state.

        Args:
            session_id: Optional session to snapshot

        Returns:
            Immutable MemorySnapshot
        """
        pass

    @abstractmethod
    def record_turn(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a conversation turn.

        Args:
            role: "user" or "assistant" or "system"
            content: The message content
            session_id: Optional session ID
            metadata: Additional metadata
        """
        pass

    @abstractmethod
    def record_philosopher_output(
        self,
        philosopher_name: str,
        output: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> None:
        """
        Record a philosopher's output for history.

        Args:
            philosopher_name: Name of the philosopher
            output: The philosopher's reasoning output
            session_id: Optional session ID
        """
        pass

    @abstractmethod
    def record_metrics(
        self,
        metrics: Dict[str, float],
        session_id: Optional[str] = None,
    ) -> None:
        """
        Record metrics for history tracking.

        Args:
            metrics: Dictionary of metric name -> value
            session_id: Optional session ID
        """
        pass

    @abstractmethod
    def start_session(self, session_id: Optional[str] = None) -> str:
        """
        Start a new session.

        Args:
            session_id: Optional explicit session ID

        Returns:
            The session ID (generated if not provided)
        """
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> None:
        """
        End a session.

        Args:
            session_id: The session to end
        """
        pass


class InMemoryMemory(MemoryPort):
    """
    Simple in-memory implementation for testing.

    Not for production use - just for unit tests.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._current_session: Optional[str] = None

    def get_snapshot(self, session_id: Optional[str] = None) -> MemorySnapshot:
        sid = session_id or self._current_session
        if not sid or sid not in self._sessions:
            return MemorySnapshot()

        session = self._sessions[sid]
        return MemorySnapshot(
            session_id=sid,
            conversation_history=tuple(session.get("history", [])),
            philosopher_states=session.get("philosophers"),
            metrics_history=session.get("metrics"),
        )

    def record_turn(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        sid = session_id or self._current_session
        if not sid:
            sid = self.start_session()

        if sid not in self._sessions:
            self._sessions[sid] = {"history": [], "philosophers": {}, "metrics": {}}

        self._sessions[sid]["history"].append((role, content))

    def record_philosopher_output(
        self,
        philosopher_name: str,
        output: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> None:
        sid = session_id or self._current_session
        if not sid or sid not in self._sessions:
            return

        if "philosophers" not in self._sessions[sid]:
            self._sessions[sid]["philosophers"] = {}

        self._sessions[sid]["philosophers"][philosopher_name.lower()] = output

    def record_metrics(
        self,
        metrics: Dict[str, float],
        session_id: Optional[str] = None,
    ) -> None:
        sid = session_id or self._current_session
        if not sid or sid not in self._sessions:
            return

        if "metrics" not in self._sessions[sid]:
            self._sessions[sid]["metrics"] = {}

        for key, value in metrics.items():
            if key not in self._sessions[sid]["metrics"]:
                self._sessions[sid]["metrics"][key] = []
            self._sessions[sid]["metrics"][key].append(value)

    def start_session(self, session_id: Optional[str] = None) -> str:
        sid = session_id or str(uuid.uuid4())
        self._sessions[sid] = {"history": [], "philosophers": {}, "metrics": {}}
        self._current_session = sid
        return sid

    def end_session(self, session_id: str) -> None:
        if session_id == self._current_session:
            self._current_session = None


__all__ = [
    "MemoryPort",
    "MemorySnapshot",
    "MemoryQuery",
    "InMemoryMemory",
]
