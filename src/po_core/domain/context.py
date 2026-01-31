"""
Context - Input context for philosophical reasoning.

This is what philosophers receive as input.
It's immutable once created to ensure consistent reasoning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, FrozenSet, Optional
import uuid


@dataclass(frozen=True)
class Context:
    """
    Immutable context for philosophical reasoning.

    This is the INPUT contract - what philosophers receive.
    Using frozen=True ensures the context cannot be modified
    during reasoning, preventing side effects.

    Attributes:
        prompt: The user's input prompt (required)
        session_id: Unique session identifier
        created_at: When this context was created
        tensor_values: Snapshot of tensor values at context creation
        intent: Optional high-level intent from Solar Will
        goals: Optional goal candidates
        previous_proposals: Previous proposals for reference
        metadata: Additional unstructured metadata
    """

    prompt: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    tensor_values: Optional[Dict[str, float]] = None
    intent: Optional[str] = None
    goals: Optional[FrozenSet[str]] = None
    previous_proposals: Optional[tuple] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def minimal(cls, prompt: str) -> "Context":
        """Create a minimal context with just a prompt."""
        return cls(prompt=prompt)

    def with_tensors(self, tensor_values: Dict[str, float]) -> "Context":
        """Create a new context with tensor values added."""
        return Context(
            prompt=self.prompt,
            session_id=self.session_id,
            created_at=self.created_at,
            tensor_values=tensor_values,
            intent=self.intent,
            goals=self.goals,
            previous_proposals=self.previous_proposals,
            metadata=self.metadata,
        )

    def with_intent(self, intent: str) -> "Context":
        """Create a new context with intent added."""
        return Context(
            prompt=self.prompt,
            session_id=self.session_id,
            created_at=self.created_at,
            tensor_values=self.tensor_values,
            intent=intent,
            goals=self.goals,
            previous_proposals=self.previous_proposals,
            metadata=self.metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result: Dict[str, Any] = {
            "prompt": self.prompt,
            "session_id": self.session_id,
            "created_at": self.created_at,
        }
        if self.tensor_values:
            result["tensor_values"] = dict(self.tensor_values)
        if self.intent:
            result["intent"] = self.intent
        if self.goals:
            result["goals"] = list(self.goals)
        if self.previous_proposals:
            result["previous_proposals"] = list(self.previous_proposals)
        if self.metadata:
            result["metadata"] = dict(self.metadata)
        return result


class ContextBuilder:
    """
    Fluent builder for Context objects.

    Use this when building a context incrementally:

        ctx = (ContextBuilder(prompt="...")
               .with_session_id("abc123")
               .with_tensor("freedom_pressure", 0.7)
               .with_intent("explore alternatives")
               .build())
    """

    def __init__(self, prompt: str) -> None:
        self._prompt = prompt
        self._session_id: Optional[str] = None
        self._tensor_values: Dict[str, float] = {}
        self._intent: Optional[str] = None
        self._goals: set = set()
        self._metadata: Dict[str, Any] = {}

    def with_session_id(self, session_id: str) -> "ContextBuilder":
        """Set the session ID."""
        self._session_id = session_id
        return self

    def with_tensor(self, name: str, value: float) -> "ContextBuilder":
        """Add a tensor value."""
        self._tensor_values[name] = value
        return self

    def with_tensors(self, tensor_values: Dict[str, float]) -> "ContextBuilder":
        """Add multiple tensor values."""
        self._tensor_values.update(tensor_values)
        return self

    def with_intent(self, intent: str) -> "ContextBuilder":
        """Set the intent."""
        self._intent = intent
        return self

    def with_goal(self, goal: str) -> "ContextBuilder":
        """Add a goal."""
        self._goals.add(goal)
        return self

    def with_metadata(self, key: str, value: Any) -> "ContextBuilder":
        """Add metadata."""
        self._metadata[key] = value
        return self

    def build(self) -> Context:
        """Build the immutable Context."""
        return Context(
            prompt=self._prompt,
            session_id=self._session_id or str(uuid.uuid4()),
            tensor_values=dict(self._tensor_values) if self._tensor_values else None,
            intent=self._intent,
            goals=frozenset(self._goals) if self._goals else None,
            metadata=dict(self._metadata) if self._metadata else None,
        )


__all__ = ["Context", "ContextBuilder"]
