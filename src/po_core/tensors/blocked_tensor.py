"""
Blocked Tensor (Rejection Log)

Based on Derrida's theory of trace and Heidegger's concept of absence.

The Blocked Tensor records what was NOT said - the rejected, filtered,
or suppressed meanings. This captures the "trace" of absent possibilities.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import numpy as np

from po_core.tensors.base import Tensor


class BlockedEntry:
    """
    Represents a single blocked/rejected meaning.

    Attributes:
        content: What was blocked
        reason: Why it was blocked
        timestamp: When it was blocked
        philosopher: Which philosopher blocked it
        alternative: What was chosen instead
        intensity: Strength of the blocking
    """

    def __init__(
        self,
        content: str,
        reason: str,
        philosopher: Optional[str] = None,
        alternative: Optional[str] = None,
        intensity: float = 1.0,
    ) -> None:
        """
        Initialize a blocked entry.

        Args:
            content: The blocked content
            reason: Reason for blocking
            philosopher: Philosopher who blocked it
            alternative: What was chosen instead
            intensity: Blocking intensity (0-1)
        """
        self.content = content
        self.reason = reason
        self.philosopher = philosopher
        self.alternative = alternative
        self.intensity = max(0.0, min(1.0, intensity))
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "reason": self.reason,
            "philosopher": self.philosopher,
            "alternative": self.alternative,
            "intensity": self.intensity,
            "timestamp": self.timestamp,
        }


class BlockedTensor(Tensor):
    """
    Blocked Tensor - Records rejected meanings.

    Maintains a log of what was filtered, suppressed, or rejected
    during the reasoning process. This tensor represents the "absence"
    that shapes the "presence" of the final output.

    Dimensions (aggregation vectors):
        - Ethical filtering: Blocked for ethical reasons
        - Logical filtering: Blocked for logical inconsistency
        - Relevance filtering: Blocked as irrelevant
        - Bias filtering: Blocked as biased
        - Harmful filtering: Blocked as potentially harmful
        - Redundancy filtering: Blocked as redundant

    The tensor data represents the aggregate intensity of blocking
    in each category.
    """

    DEFAULT_DIMENSIONS = 6

    def __init__(
        self,
        name: str = "Blocked_Tensor",
        dimensions: int = DEFAULT_DIMENSIONS,
        initial_value: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize Blocked Tensor.

        Args:
            name: Name of the tensor
            dimensions: Number of dimensions (default: 6)
            initial_value: Initial tensor values
            metadata: Additional metadata
        """
        super().__init__(name, dimensions, initial_value, metadata)

        # Initialize dimension names
        self.dimension_names = [
            "ethical_filtering",
            "logical_filtering",
            "relevance_filtering",
            "bias_filtering",
            "harmful_filtering",
            "redundancy_filtering",
        ]

        # Blocked entries log
        self.blocked_entries: List[BlockedEntry] = []

        # Category mapping for classification
        self.category_keywords = {
            "ethical_filtering": [
                "unethical",
                "immoral",
                "wrong",
                "harmful values",
            ],
            "logical_filtering": [
                "inconsistent",
                "contradictory",
                "illogical",
                "fallacy",
            ],
            "relevance_filtering": [
                "irrelevant",
                "off-topic",
                "unrelated",
                "tangential",
            ],
            "bias_filtering": ["biased", "prejudiced", "stereotypical", "unfair"],
            "harmful_filtering": [
                "harmful",
                "dangerous",
                "toxic",
                "offensive",
            ],
            "redundancy_filtering": [
                "redundant",
                "repetitive",
                "duplicate",
                "already said",
            ],
        }

    def compute(
        self, blocked_entries: Optional[List[BlockedEntry]] = None
    ) -> np.ndarray:
        """
        Compute blocked tensor from entries.

        Args:
            blocked_entries: List of blocked entries to process

        Returns:
            Computed blocked tensor
        """
        if blocked_entries:
            for entry in blocked_entries:
                self.add_blocked_entry(entry)

        # Aggregate intensities by category
        category_intensities = np.zeros(self.dimensions, dtype=np.float64)

        for entry in self.blocked_entries:
            category_idx = self._classify_blocking_reason(entry.reason)
            category_intensities[category_idx] += entry.intensity

        # Normalize by number of entries (if any)
        if self.blocked_entries:
            category_intensities /= len(self.blocked_entries)

        self.data = category_intensities
        return self.data

    def add_blocked_entry(
        self,
        content: str = None,
        reason: str = None,
        philosopher: Optional[str] = None,
        alternative: Optional[str] = None,
        intensity: float = 1.0,
        entry: Optional[BlockedEntry] = None,
    ) -> None:
        """
        Add a blocked entry.

        Args:
            content: What was blocked
            reason: Why it was blocked
            philosopher: Who blocked it
            alternative: What was chosen instead
            intensity: Blocking intensity
            entry: Pre-constructed BlockedEntry (overrides other args)
        """
        if entry is not None:
            self.blocked_entries.append(entry)
        elif content is not None and reason is not None:
            entry = BlockedEntry(content, reason, philosopher, alternative, intensity)
            self.blocked_entries.append(entry)
        else:
            raise ValueError("Must provide either entry or (content and reason)")

        # Recompute tensor
        self.compute()

    def _classify_blocking_reason(self, reason: str) -> int:
        """
        Classify blocking reason into a category.

        Args:
            reason: Blocking reason text

        Returns:
            Category index
        """
        reason_lower = reason.lower()

        # Check each category's keywords
        for i, (category, keywords) in enumerate(self.category_keywords.items()):
            if any(keyword in reason_lower for keyword in keywords):
                return i

        # Default to relevance filtering if no match
        return 2

    def get_blocked_count(self) -> int:
        """
        Get total number of blocked entries.

        Returns:
            Count of blocked entries
        """
        return len(self.blocked_entries)

    def get_blocked_by_philosopher(self, philosopher: str) -> List[BlockedEntry]:
        """
        Get entries blocked by a specific philosopher.

        Args:
            philosopher: Philosopher name

        Returns:
            List of blocked entries
        """
        return [
            entry
            for entry in self.blocked_entries
            if entry.philosopher == philosopher
        ]

    def get_blocked_by_category(self, category: str) -> List[BlockedEntry]:
        """
        Get entries blocked in a specific category.

        Args:
            category: Category name

        Returns:
            List of blocked entries

        Raises:
            ValueError: If category is invalid
        """
        if category not in self.dimension_names:
            raise ValueError(
                f"Invalid category: {category}. Valid categories: {self.dimension_names}"
            )

        category_idx = self.dimension_names.index(category)

        result = []
        for entry in self.blocked_entries:
            if self._classify_blocking_reason(entry.reason) == category_idx:
                result.append(entry)

        return result

    def get_blocking_summary(self) -> Dict[str, Any]:
        """
        Get summary of blocking activity.

        Returns:
            Dictionary with blocking statistics
        """
        summary = {
            "total_blocked": self.get_blocked_count(),
            "by_category": {},
            "by_philosopher": {},
            "average_intensity": 0.0,
        }

        # Category breakdown
        for category in self.dimension_names:
            entries = self.get_blocked_by_category(category)
            summary["by_category"][category] = len(entries)

        # Philosopher breakdown
        philosophers = set(
            entry.philosopher
            for entry in self.blocked_entries
            if entry.philosopher
        )
        for phil in philosophers:
            entries = self.get_blocked_by_philosopher(phil)
            summary["by_philosopher"][phil] = len(entries)

        # Average intensity
        if self.blocked_entries:
            total_intensity = sum(entry.intensity for entry in self.blocked_entries)
            summary["average_intensity"] = total_intensity / len(self.blocked_entries)

        return summary

    def get_trace_of_absence(self) -> List[Dict[str, Any]]:
        """
        Get the "trace" of absent meanings (Derridean trace).

        Returns what was rejected, revealing the structure of absence
        that shapes the present discourse.

        Returns:
            List of blocked entry dictionaries
        """
        return [entry.to_dict() for entry in self.blocked_entries]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with blocking details.

        Returns:
            Enhanced dictionary representation
        """
        base_dict = super().to_dict()
        base_dict["dimension_names"] = self.dimension_names
        base_dict["blocked_count"] = self.get_blocked_count()
        base_dict["blocking_summary"] = self.get_blocking_summary()
        base_dict["trace_of_absence"] = self.get_trace_of_absence()

        return base_dict
