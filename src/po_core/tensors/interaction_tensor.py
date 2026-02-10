"""
Philosopher Interaction Tensor

This module calculates and represents interactions between philosophers,
measuring harmony, tension, and influence dynamics.

Enables analysis of:
- Conceptual harmony between philosophers
- Philosophical tensions and disagreements
- Influence patterns and resonance
- Synthesis potential
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from po_core.tensors.base import Tensor


@dataclass
class PhilosopherInteraction:
    """
    Represents an interaction between two philosophers.

    Attributes:
        philosopher_a: Name of first philosopher
        philosopher_b: Name of second philosopher
        harmony: Degree of conceptual harmony (0-1)
        tension: Degree of philosophical tension (0-1)
        influence_a_to_b: Influence from A to B (0-1)
        influence_b_to_a: Influence from B to A (0-1)
        synthesis_potential: Potential for synthesis (0-1)
        metadata: Additional interaction information
    """

    philosopher_a: str
    philosopher_b: str
    harmony: float
    tension: float
    influence_a_to_b: float
    influence_b_to_a: float
    synthesis_potential: float
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate values."""
        self.harmony = np.clip(self.harmony, 0.0, 1.0)
        self.tension = np.clip(self.tension, 0.0, 1.0)
        self.influence_a_to_b = np.clip(self.influence_a_to_b, 0.0, 1.0)
        self.influence_b_to_a = np.clip(self.influence_b_to_a, 0.0, 1.0)
        self.synthesis_potential = np.clip(self.synthesis_potential, 0.0, 1.0)
        if self.metadata is None:
            self.metadata = {}

    def reciprocal_influence(self) -> float:
        """Calculate reciprocal influence (bidirectional)."""
        return (self.influence_a_to_b + self.influence_b_to_a) / 2

    def asymmetry(self) -> float:
        """Calculate influence asymmetry."""
        return abs(self.influence_a_to_b - self.influence_b_to_a)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "philosopher_a": self.philosopher_a,
            "philosopher_b": self.philosopher_b,
            "harmony": self.harmony,
            "tension": self.tension,
            "influence_a_to_b": self.influence_a_to_b,
            "influence_b_to_a": self.influence_b_to_a,
            "synthesis_potential": self.synthesis_potential,
            "reciprocal_influence": self.reciprocal_influence(),
            "asymmetry": self.asymmetry(),
            "metadata": self.metadata,
        }


class InteractionTensor(Tensor):
    """
    Tensor for calculating philosopher interactions.

    Represents an N×N×D tensor where:
    - N: Number of philosophers
    - D: Interaction dimensions

    Dimensions:
    0: Conceptual harmony
    1: Philosophical tension
    2: Epistemological compatibility
    3: Ethical alignment
    4: Ontological resonance
    5: Methodological affinity
    """

    DEFAULT_DIMENSIONS = 6

    def __init__(self, num_philosophers: int, dimensions: int = DEFAULT_DIMENSIONS):
        """
        Initialize interaction tensor.

        Args:
            num_philosophers: Number of philosophers in the ensemble
            dimensions: Number of interaction dimensions
        """
        # Tensor is N×N×D (philosopher × philosopher × dimensions)
        super().__init__(
            name="Interaction_Tensor",
            dimensions=num_philosophers * num_philosophers * dimensions,
            metadata={
                "num_philosophers": num_philosophers,
                "interaction_dims": dimensions,
            },
        )

        self.num_philosophers = num_philosophers
        self.interaction_dims = dimensions

        # Reshape data to 3D tensor
        self.tensor_shape = (num_philosophers, num_philosophers, dimensions)
        self.interaction_data = np.zeros(self.tensor_shape, dtype=np.float64)

        self.dimension_names = [
            "conceptual_harmony",
            "philosophical_tension",
            "epistemological_compatibility",
            "ethical_alignment",
            "ontological_resonance",
            "methodological_affinity",
        ]

        # Store philosopher names
        self.philosopher_names: List[str] = []

        # Cache interactions
        self.interactions: Dict[Tuple[str, str], PhilosopherInteraction] = {}

    def compute(self, perspectives: List[Dict[str, Any]]) -> np.ndarray:
        """
        Compute interaction tensor from philosopher perspectives.

        Args:
            perspectives: List of philosopher perspective dictionaries

        Returns:
            Flattened interaction tensor
        """
        # Extract philosopher names
        self.philosopher_names = [
            p.get("philosopher", f"phil_{i}") for i, p in enumerate(perspectives)
        ]

        # Calculate pairwise interactions
        for i, persp_a in enumerate(perspectives):
            for j, persp_b in enumerate(perspectives):
                if i == j:
                    # Self-interaction (identity)
                    self.interaction_data[i, j, :] = self._compute_self_interaction()
                else:
                    # Calculate interaction between different philosophers
                    interaction_vector = self._compute_pairwise_interaction(
                        persp_a, persp_b
                    )
                    self.interaction_data[i, j, :] = interaction_vector

                    # Cache interaction object
                    phil_a = persp_a.get("philosopher", f"phil_{i}")
                    phil_b = persp_b.get("philosopher", f"phil_{j}")
                    self.interactions[(phil_a, phil_b)] = (
                        self._create_interaction_object(
                            phil_a, phil_b, interaction_vector
                        )
                    )

        # Flatten for return
        self.data = self.interaction_data.flatten()
        return self.data

    def _compute_self_interaction(self) -> np.ndarray:
        """
        Compute self-interaction (philosopher with themselves).

        Returns identity-like interaction.
        """
        return np.array([1.0, 0.0, 1.0, 1.0, 1.0, 1.0])  # Perfect harmony, no tension

    def _compute_pairwise_interaction(
        self, persp_a: Dict[str, Any], persp_b: Dict[str, Any]
    ) -> np.ndarray:
        """
        Compute interaction between two philosophers.

        Args:
            persp_a: First philosopher's perspective
            persp_b: Second philosopher's perspective

        Returns:
            Interaction vector
        """
        interaction = np.zeros(self.interaction_dims)

        # Extract responses and metadata
        response_a = persp_a.get("response", "")
        response_b = persp_b.get("response", "")
        confidence_a = persp_a.get("confidence", 0.5)
        confidence_b = persp_b.get("confidence", 0.5)

        # 0: Conceptual harmony
        interaction[0] = self._calculate_conceptual_harmony(response_a, response_b)

        # 1: Philosophical tension
        interaction[1] = self._calculate_philosophical_tension(response_a, response_b)

        # 2: Epistemological compatibility
        interaction[2] = self._calculate_epistemological_compatibility(persp_a, persp_b)

        # 3: Ethical alignment
        interaction[3] = self._calculate_ethical_alignment(response_a, response_b)

        # 4: Ontological resonance
        interaction[4] = self._calculate_ontological_resonance(response_a, response_b)

        # 5: Methodological affinity
        interaction[5] = self._calculate_methodological_affinity(persp_a, persp_b)

        # Weight by confidence
        confidence_factor = (confidence_a + confidence_b) / 2
        interaction *= confidence_factor

        return interaction

    def _calculate_conceptual_harmony(self, text_a: str, text_b: str) -> float:
        """
        Calculate conceptual harmony between two texts.

        Measures shared vocabulary and thematic overlap.
        """
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())

        if not words_a or not words_b:
            return 0.0

        # Jaccard similarity
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)

        if union == 0:
            return 0.0

        return intersection / union

    def _calculate_philosophical_tension(self, text_a: str, text_b: str) -> float:
        """
        Calculate philosophical tension.

        Detects contradictory or opposing concepts.
        """
        text_a_lower = text_a.lower()
        text_b_lower = text_b.lower()

        # Opposing word pairs
        oppositions = [
            ("freedom", "determinism"),
            ("individual", "collective"),
            ("subjective", "objective"),
            ("rational", "intuitive"),
            ("being", "becoming"),
            ("essence", "existence"),
            ("absolute", "relative"),
            ("certain", "uncertain"),
            ("order", "chaos"),
            ("unity", "plurality"),
        ]

        tension_count = 0
        for word_a, word_b in oppositions:
            if (word_a in text_a_lower and word_b in text_b_lower) or (
                word_b in text_a_lower and word_a in text_b_lower
            ):
                tension_count += 1

        # Normalize by number of oppositions
        return min(tension_count / len(oppositions), 1.0)

    def _calculate_epistemological_compatibility(
        self, persp_a: Dict[str, Any], persp_b: Dict[str, Any]
    ) -> float:
        """
        Calculate epistemological compatibility.

        How similar are their ways of knowing?
        """
        # Check for epistemic keywords
        epistemic_keywords_empirical = [
            "evidence",
            "observation",
            "experience",
            "sense",
        ]
        epistemic_keywords_rational = ["logic", "reason", "deduction", "proof"]
        epistemic_keywords_intuitive = ["intuition", "insight", "feeling", "immediate"]

        response_a = persp_a.get("response", "").lower()
        response_b = persp_b.get("response", "").lower()

        # Count epistemic approaches in each
        empirical_a = sum(1 for k in epistemic_keywords_empirical if k in response_a)
        rational_a = sum(1 for k in epistemic_keywords_rational if k in response_a)
        intuitive_a = sum(1 for k in epistemic_keywords_intuitive if k in response_a)

        empirical_b = sum(1 for k in epistemic_keywords_empirical if k in response_b)
        rational_b = sum(1 for k in epistemic_keywords_rational if k in response_b)
        intuitive_b = sum(1 for k in epistemic_keywords_intuitive if k in response_b)

        # Create epistemic vectors
        vec_a = np.array([empirical_a, rational_a, intuitive_a], dtype=float)
        vec_b = np.array([empirical_b, rational_b, intuitive_b], dtype=float)

        # Normalize
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.5  # Neutral if unknown

        # Cosine similarity
        similarity = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        return (similarity + 1) / 2  # Normalize to [0, 1]

    def _calculate_ethical_alignment(self, text_a: str, text_b: str) -> float:
        """
        Calculate ethical alignment.

        Do they share similar ethical orientations?
        """
        ethical_keywords_deontological = [
            "duty",
            "obligation",
            "rule",
            "principle",
            "ought",
        ]
        ethical_keywords_consequentialist = [
            "consequence",
            "result",
            "outcome",
            "utility",
            "benefit",
        ]
        ethical_keywords_virtue = [
            "virtue",
            "character",
            "excellence",
            "flourishing",
            "good",
        ]

        text_a_lower = text_a.lower()
        text_b_lower = text_b.lower()

        # Count ethical approaches
        deont_a = sum(1 for k in ethical_keywords_deontological if k in text_a_lower)
        conseq_a = sum(
            1 for k in ethical_keywords_consequentialist if k in text_a_lower
        )
        virtue_a = sum(1 for k in ethical_keywords_virtue if k in text_a_lower)

        deont_b = sum(1 for k in ethical_keywords_deontological if k in text_b_lower)
        conseq_b = sum(
            1 for k in ethical_keywords_consequentialist if k in text_b_lower
        )
        virtue_b = sum(1 for k in ethical_keywords_virtue if k in text_b_lower)

        # Create ethical vectors
        vec_a = np.array([deont_a, conseq_a, virtue_a], dtype=float)
        vec_b = np.array([deont_b, conseq_b, virtue_b], dtype=float)

        # Normalize
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.5  # Neutral

        # Cosine similarity
        similarity = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        return (similarity + 1) / 2

    def _calculate_ontological_resonance(self, text_a: str, text_b: str) -> float:
        """
        Calculate ontological resonance.

        Do they share similar views on being and existence?
        """
        ontological_keywords_being = ["being", "existence", "ontology", "reality", "is"]
        ontological_keywords_becoming = [
            "becoming",
            "change",
            "process",
            "flux",
            "transformation",
        ]
        ontological_keywords_substance = [
            "substance",
            "essence",
            "nature",
            "identity",
            "self",
        ]

        text_a_lower = text_a.lower()
        text_b_lower = text_b.lower()

        # Count ontological themes
        being_a = sum(1 for k in ontological_keywords_being if k in text_a_lower)
        becoming_a = sum(1 for k in ontological_keywords_becoming if k in text_a_lower)
        substance_a = sum(
            1 for k in ontological_keywords_substance if k in text_a_lower
        )

        being_b = sum(1 for k in ontological_keywords_being if k in text_b_lower)
        becoming_b = sum(1 for k in ontological_keywords_becoming if k in text_b_lower)
        substance_b = sum(
            1 for k in ontological_keywords_substance if k in text_b_lower
        )

        # Create ontological vectors
        vec_a = np.array([being_a, becoming_a, substance_a], dtype=float)
        vec_b = np.array([being_b, becoming_b, substance_b], dtype=float)

        # Normalize
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.5

        # Cosine similarity
        similarity = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        return (similarity + 1) / 2

    def _calculate_methodological_affinity(
        self, persp_a: Dict[str, Any], persp_b: Dict[str, Any]
    ) -> float:
        """
        Calculate methodological affinity.

        Do they use similar philosophical methods?
        """
        # Extract reasoning metadata
        reasoning_a = persp_a.get("reasoning", "").lower()
        reasoning_b = persp_b.get("reasoning", "").lower()

        methods_phenomenological = [
            "phenomenology",
            "experience",
            "consciousness",
            "lived",
        ]
        methods_analytical = ["analysis", "logic", "argument", "definition"]
        methods_dialectical = ["dialectic", "synthesis", "contradiction", "negation"]
        methods_hermeneutic = ["interpretation", "understanding", "meaning", "text"]

        # Count methods
        phenom_a = sum(1 for m in methods_phenomenological if m in reasoning_a)
        analyt_a = sum(1 for m in methods_analytical if m in reasoning_a)
        dialec_a = sum(1 for m in methods_dialectical if m in reasoning_a)
        hermen_a = sum(1 for m in methods_hermeneutic if m in reasoning_a)

        phenom_b = sum(1 for m in methods_phenomenological if m in reasoning_b)
        analyt_b = sum(1 for m in methods_analytical if m in reasoning_b)
        dialec_b = sum(1 for m in methods_dialectical if m in reasoning_b)
        hermen_b = sum(1 for m in methods_hermeneutic if m in reasoning_b)

        vec_a = np.array([phenom_a, analyt_a, dialec_a, hermen_a], dtype=float)
        vec_b = np.array([phenom_b, analyt_b, dialec_b, hermen_b], dtype=float)

        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.5

        similarity = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        return (similarity + 1) / 2

    def _create_interaction_object(
        self, phil_a: str, phil_b: str, interaction_vector: np.ndarray
    ) -> PhilosopherInteraction:
        """
        Create PhilosopherInteraction object from vector.

        Args:
            phil_a: Name of first philosopher
            phil_b: Name of second philosopher
            interaction_vector: Interaction values

        Returns:
            PhilosopherInteraction object
        """
        harmony = interaction_vector[0]
        tension = interaction_vector[1]

        # Calculate influence (asymmetric)
        # Influence is based on harmony and method compatibility
        epistem_compat = interaction_vector[2]
        method_affin = interaction_vector[5]

        influence_a_to_b = (harmony + method_affin) / 2
        influence_b_to_a = (harmony + epistem_compat) / 2

        # Synthesis potential (inverse of tension, boosted by harmony)
        synthesis_potential = harmony * (1 - tension)

        return PhilosopherInteraction(
            philosopher_a=phil_a,
            philosopher_b=phil_b,
            harmony=harmony,
            tension=tension,
            influence_a_to_b=influence_a_to_b,
            influence_b_to_a=influence_b_to_a,
            synthesis_potential=synthesis_potential,
            metadata={
                "epistemological_compatibility": epistem_compat,
                "ethical_alignment": interaction_vector[3],
                "ontological_resonance": interaction_vector[4],
                "methodological_affinity": method_affin,
            },
        )

    def get_interaction(
        self, phil_a: str, phil_b: str
    ) -> Optional[PhilosopherInteraction]:
        """
        Get interaction between two philosophers.

        Args:
            phil_a: Name of first philosopher
            phil_b: Name of second philosopher

        Returns:
            PhilosopherInteraction or None
        """
        return self.interactions.get((phil_a, phil_b))

    def get_harmony_matrix(self) -> np.ndarray:
        """
        Get N×N harmony matrix.

        Returns:
            Matrix of harmony scores between all philosophers
        """
        return self.interaction_data[:, :, 0]

    def get_tension_matrix(self) -> np.ndarray:
        """
        Get N×N tension matrix.

        Returns:
            Matrix of tension scores between all philosophers
        """
        return self.interaction_data[:, :, 1]

    def get_synthesis_potential_matrix(self) -> np.ndarray:
        """
        Get N×N synthesis potential matrix.

        Returns:
            Matrix of synthesis potential between all philosophers
        """
        harmony = self.interaction_data[:, :, 0]
        tension = self.interaction_data[:, :, 1]
        return harmony * (1 - tension)

    def export_interaction_map(self) -> Dict[str, Any]:
        """
        Export complete interaction map for visualization.

        Returns:
            Dictionary with all interactions and matrices
        """
        interactions_export = {}
        for (phil_a, phil_b), interaction in self.interactions.items():
            key = f"{phil_a}_{phil_b}"
            interactions_export[key] = interaction.to_dict()

        return {
            "philosophers": self.philosopher_names,
            "dimension_names": self.dimension_names,
            "interactions": interactions_export,
            "harmony_matrix": self.get_harmony_matrix().tolist(),
            "tension_matrix": self.get_tension_matrix().tolist(),
            "synthesis_potential_matrix": self.get_synthesis_potential_matrix().tolist(),
        }
