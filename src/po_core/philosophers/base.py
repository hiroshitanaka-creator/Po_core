"""
Base Philosopher Class

Abstract base class for all philosophical reasoning modules.
Each philosopher provides a unique perspective for analyzing and generating meaning.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


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

    def __repr__(self) -> str:
        """String representation of the philosopher."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"🧠 {self.name}: {self.description}"
