"""
Base Philosopher Class

Abstract base class for all philosophical reasoning modules.
Each philosopher provides a unique perspective for analyzing and generating meaning.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PhilosopherSignal:
    """Normalized signal returned by a philosopher module."""

    name: str
    reasoning: str
    perspective: str
    tensions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


class Philosopher(ABC):
    """
    Abstract base class for all philosophers.

    Each philosopher must implement their own reasoning method that reflects
    their unique philosophical perspective.
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize a philosopher.

        Args:
            name: The philosopher's name
            description: A brief description of their philosophical approach
        """
        self.name = name
        self.description = description
        self._context: Dict[str, Any] = {}

    @abstractmethod
    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate philosophical reasoning for the given prompt.

        Args:
            prompt: The input text to reason about
            context: Optional context information

        Returns:
            A dictionary containing:
                - reasoning: The philosophical analysis
                - perspective: The philosopher's unique viewpoint
                - tension: Identified tensions or contradictions
                - metadata: Additional reasoning metadata
        """
        pass

    def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> PhilosopherSignal:
        """Normalize the philosopher output into a common schema."""

        raw = self.reason(prompt, context=context)
        reasoning = str(raw.get("reasoning", "")).strip()
        perspective = str(raw.get("perspective", self.description))

        tensions: List[str] = []
        raw_tension = raw.get("tension")
        if isinstance(raw_tension, list):
            tensions = [str(item) for item in raw_tension if item]
        elif raw_tension:
            tensions = [str(raw_tension)]

        metadata = {"philosopher": self.name}
        metadata.update(raw.get("metadata", {}))

        return PhilosopherSignal(
            name=self.name,
            reasoning=reasoning,
            perspective=perspective,
            tensions=tensions,
            metadata=metadata,
            raw=raw,
        )

    def __repr__(self) -> str:
        """String representation of the philosopher."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"🧠 {self.name}: {self.description}"
