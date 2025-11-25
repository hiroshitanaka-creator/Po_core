"""Minimal deterministic tensor representations for Po_self."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class TensorState:
    """Represents a single tensor output from a philosopher or ensemble."""

    name: str
    value: Any
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable view of the tensor."""

        return {
            "name": self.name,
            "value": self.value,
            "description": self.description,
            "metadata": self.metadata,
        }
