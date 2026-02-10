"""
Semantic Profile

Tracks the evolution of meaning across conversation and reasoning steps.

The Semantic Profile maintains a dynamic representation of how meaning
shifts and develops through philosophical analysis.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np

from po_core.tensors.base import Tensor


class SemanticProfile(Tensor):
    """
    Semantic Profile Tensor.

    Tracks meaning evolution across the reasoning process.
    Records semantic shifts, conceptual development, and meaning density.

    Dimensions:
        - Abstract_level: Degree of abstraction
        - Concrete_level: Degree of concreteness
        - Emotional_valence: Emotional tone
        - Logical_coherence: Logical consistency
        - Novelty: Newness of concepts
        - Depth: Depth of analysis

    The profile maintains a history of semantic states for tracking evolution.
    """

    DEFAULT_DIMENSIONS = 6

    def __init__(
        self,
        name: str = "Semantic_Profile",
        dimensions: int = DEFAULT_DIMENSIONS,
        initial_value: Optional[np.ndarray] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize Semantic Profile.

        Args:
            name: Name of the tensor
            dimensions: Number of dimensions (default: 6)
            initial_value: Initial tensor values
            metadata: Additional metadata
        """
        super().__init__(name, dimensions, initial_value, metadata)

        # Initialize dimension names
        self.dimension_names = [
            "abstract_level",
            "concrete_level",
            "emotional_valence",
            "logical_coherence",
            "novelty",
            "depth",
        ]

        # History tracking
        self.history: List[Dict[str, Any]] = []
        self.evolution_delta: List[np.ndarray] = []

    def compute(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
        previous_state: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Compute semantic profile from text.

        Args:
            text: Text to analyze
            context: Optional context information
            previous_state: Previous semantic state for delta calculation

        Returns:
            Computed semantic profile
        """
        context = context or {}

        # Analyze text semantics
        profile = self._analyze_text_semantics(text)

        # Calculate delta if previous state exists
        if previous_state is not None:
            delta = profile - previous_state
            self.evolution_delta.append(delta)
        else:
            delta = np.zeros_like(profile)

        # Record in history
        self._record_state(text, profile, delta)

        self.data = profile
        return self.data

    def _analyze_text_semantics(self, text: str) -> np.ndarray:
        """
        Analyze text to extract semantic features.

        Args:
            text: Text to analyze

        Returns:
            Semantic feature array
        """
        text_lower = text.lower()

        # Abstract level: Presence of abstract terms
        abstract_terms = [
            "concept",
            "theory",
            "abstract",
            "principle",
            "essence",
            "universal",
        ]
        abstract = sum(1 for term in abstract_terms if term in text_lower)
        abstract = min(abstract / len(abstract_terms), 1.0)

        # Concrete level: Presence of concrete terms
        concrete_terms = [
            "example",
            "specific",
            "particular",
            "instance",
            "case",
            "concrete",
        ]
        concrete = sum(1 for term in concrete_terms if term in text_lower)
        concrete = min(concrete / len(concrete_terms), 1.0)

        # Emotional valence: Emotional words
        positive_terms = ["good", "joy", "happy", "love", "hope", "beautiful"]
        negative_terms = ["bad", "sad", "fear", "hate", "despair", "ugly"]
        positive = sum(1 for term in positive_terms if term in text_lower)
        negative = sum(1 for term in negative_terms if term in text_lower)
        # Scale from -1 to 1
        valence = (positive - negative) / max(positive + negative, 1)
        valence = (valence + 1) / 2  # Normalize to [0, 1]

        # Logical coherence: Logical connectors
        logical_terms = [
            "therefore",
            "thus",
            "because",
            "however",
            "although",
            "consequently",
        ]
        coherence = sum(1 for term in logical_terms if term in text_lower)
        coherence = min(coherence / len(logical_terms), 1.0)

        # Novelty: Question marks and exploration terms
        novelty_indicators = ["?", "new", "novel", "innovative", "original", "unique"]
        novelty = sum(1 for indicator in novelty_indicators if indicator in text_lower)
        novelty = min(novelty / len(novelty_indicators), 1.0)

        # Depth: Length and complexity indicators
        depth_indicators = ["because", "why", "how", "explain", "understand", "reason"]
        depth = sum(1 for indicator in depth_indicators if indicator in text_lower)
        depth = min(depth / len(depth_indicators), 1.0)

        return np.array(
            [abstract, concrete, valence, coherence, novelty, depth], dtype=np.float64
        )

    def _record_state(self, text: str, profile: np.ndarray, delta: np.ndarray) -> None:
        """
        Record current state in history.

        Args:
            text: Input text
            profile: Computed profile
            delta: Change from previous state
        """
        state = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "text_length": len(text),
            "profile": profile.tolist(),
            "delta": delta.tolist(),
            "norm": float(np.linalg.norm(profile)),
        }
        self.history.append(state)

    def get_evolution_trajectory(self) -> np.ndarray:
        """
        Get trajectory of semantic evolution.

        Returns:
            Array of historical states (T x D) where T is timesteps
        """
        if not self.history:
            return np.array([])

        profiles = [np.array(state["profile"]) for state in self.history]
        return np.array(profiles)

    def get_semantic_delta(self) -> Optional[np.ndarray]:
        """
        Get most recent semantic delta.

        Returns:
            Latest delta, or None if no history
        """
        if not self.evolution_delta:
            return None
        return self.evolution_delta[-1]

    def get_total_evolution(self) -> float:
        """
        Calculate total semantic evolution magnitude.

        Returns:
            Sum of all delta norms
        """
        if not self.evolution_delta:
            return 0.0

        return float(sum(np.linalg.norm(delta) for delta in self.evolution_delta))

    def get_dimension_evolution(self, dimension_name: str) -> List[float]:
        """
        Get evolution of a specific dimension over time.

        Args:
            dimension_name: Name of the dimension

        Returns:
            List of values over time

        Raises:
            ValueError: If dimension name is invalid
        """
        try:
            idx = self.dimension_names.index(dimension_name)
        except ValueError:
            raise ValueError(
                f"Invalid dimension name: {dimension_name}. "
                f"Valid names: {self.dimension_names}"
            )

        return [float(state["profile"][idx]) for state in self.history]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with evolution details.

        Returns:
            Enhanced dictionary representation
        """
        base_dict = super().to_dict()
        base_dict["dimension_names"] = self.dimension_names
        base_dict["history_length"] = len(self.history)
        base_dict["total_evolution"] = self.get_total_evolution()

        if self.get_semantic_delta() is not None:
            base_dict["latest_delta"] = self.get_semantic_delta().tolist()  # type: ignore

        # Include recent history (last 5 states)
        base_dict["recent_history"] = self.history[-5:] if self.history else []

        return base_dict
