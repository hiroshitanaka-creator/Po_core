"""
Po_self Memory Adapter
======================

Wraps Po_self as a MemoryPort implementation.

This adapter allows the core system to interact with Po_self
through the abstract MemoryPort interface, breaking the
direct dependency cycle.

IMPORTANT: This is the ONLY file that should import from po_self directly.
All other modules should use the MemoryPort interface.
"""

from typing import Any, Dict, List, Optional
import uuid

from po_core.ports.memory import (
    MemoryPort,
    MemorySnapshot,
)


class PoSelfMemoryAdapter(MemoryPort):
    """
    Adapter that wraps Po_self as a MemoryPort.

    This provides a clean interface to Po_self's memory capabilities
    without creating circular dependencies.

    Note: Lazy imports Po_self to avoid import-time cycles.
    """

    def __init__(self) -> None:
        self._po_self = None
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._current_session: Optional[str] = None

    def _get_po_self(self):
        """Lazy load Po_self to avoid import-time cycles."""
        if self._po_self is None:
            # Import at runtime to break cycle
            from po_core.po_self import PoSelf
            self._po_self = PoSelf()
        return self._po_self

    def get_snapshot(self, session_id: Optional[str] = None) -> MemorySnapshot:
        """Get a read-only snapshot of current memory state."""
        sid = session_id or self._current_session

        # Build snapshot from session data
        session_data = self._sessions.get(sid, {}) if sid else {}

        return MemorySnapshot(
            session_id=sid,
            conversation_history=tuple(session_data.get("history", [])),
            philosopher_states=session_data.get("philosophers"),
            metrics_history=session_data.get("metrics"),
            metadata=session_data.get("metadata"),
        )

    def record_turn(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a conversation turn."""
        sid = session_id or self._current_session
        if not sid:
            sid = self.start_session()

        if sid not in self._sessions:
            self._sessions[sid] = {"history": [], "philosophers": {}, "metrics": {}}

        self._sessions[sid]["history"].append((role, content))
        if metadata:
            if "turn_metadata" not in self._sessions[sid]:
                self._sessions[sid]["turn_metadata"] = []
            self._sessions[sid]["turn_metadata"].append(metadata)

    def record_philosopher_output(
        self,
        philosopher_name: str,
        output: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> None:
        """Record a philosopher's output for history."""
        sid = session_id or self._current_session
        if not sid:
            return

        if sid not in self._sessions:
            self._sessions[sid] = {"history": [], "philosophers": {}, "metrics": {}}

        if "philosophers" not in self._sessions[sid]:
            self._sessions[sid]["philosophers"] = {}

        self._sessions[sid]["philosophers"][philosopher_name.lower()] = output

    def record_metrics(
        self,
        metrics: Dict[str, float],
        session_id: Optional[str] = None,
    ) -> None:
        """Record metrics for history tracking."""
        sid = session_id or self._current_session
        if not sid:
            return

        if sid not in self._sessions:
            return

        if "metrics" not in self._sessions[sid]:
            self._sessions[sid]["metrics"] = {}

        for key, value in metrics.items():
            if key not in self._sessions[sid]["metrics"]:
                self._sessions[sid]["metrics"][key] = []
            self._sessions[sid]["metrics"][key].append(value)

    def start_session(self, session_id: Optional[str] = None) -> str:
        """Start a new session."""
        sid = session_id or str(uuid.uuid4())
        self._sessions[sid] = {
            "history": [],
            "philosophers": {},
            "metrics": {},
            "metadata": {},
        }
        self._current_session = sid
        return sid

    def end_session(self, session_id: str) -> None:
        """End a session."""
        if session_id == self._current_session:
            self._current_session = None

    # Additional methods specific to Po_self integration

    def generate(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using Po_self.

        This is a pass-through to Po_self.generate() for backward compatibility.
        New code should use the ensemble directly via app/api.py.

        Args:
            prompt: The input prompt

        Returns:
            PoSelfResponse as a dictionary
        """
        po_self = self._get_po_self()
        response = po_self.generate(prompt)

        # Record the interaction
        if self._current_session:
            self.record_turn("user", prompt)
            self.record_turn("assistant", response.text)
            self.record_metrics({
                "freedom_pressure": response.metrics.freedom_pressure,
                "semantic_delta": response.metrics.semantic_delta,
                "blocked_tensor": response.metrics.blocked_tensor,
            })

        # Convert to dict for clean interface
        return {
            "text": response.text,
            "philosophers": response.philosophers,
            "metrics": {
                "freedom_pressure": response.metrics.freedom_pressure,
                "semantic_delta": response.metrics.semantic_delta,
                "blocked_tensor": response.metrics.blocked_tensor,
            },
            "responses": response.responses,
            "log": response.log,
            "consensus_leader": response.consensus_leader,
        }


__all__ = ["PoSelfMemoryAdapter"]
