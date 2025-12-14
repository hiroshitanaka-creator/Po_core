"""
Philosophical Concept Quantification System

This module provides numerical quantification of philosophical concepts,
allowing for mathematical operations on philosophical ideas.

Concepts are represented as multi-dimensional vectors, enabling:
- Concept similarity measurement
- Concept evolution tracking
- Cross-philosopher concept comparison
- Tension and harmony calculation between concepts
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from po_core.tensors.base import Tensor


@dataclass
class PhilosophicalConcept:
    """
    Represents a quantified philosophical concept.

    Attributes:
        name: Name of the concept (e.g., "freedom", "being")
        philosopher: Associated philosopher
        vector: Numerical representation as numpy array
        confidence: Confidence in this quantification (0-1)
        metadata: Additional concept information
    """
    name: str
    philosopher: str
    vector: np.ndarray
    confidence: float = 1.0
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate and normalize."""
        if self.confidence < 0.0 or self.confidence > 1.0:
            self.confidence = np.clip(self.confidence, 0.0, 1.0)
        if self.metadata is None:
            self.metadata = {}

    def similarity(self, other: 'PhilosophicalConcept') -> float:
        """
        Calculate similarity with another concept.

        Uses cosine similarity between concept vectors.

        Args:
            other: Another philosophical concept

        Returns:
            Similarity score (0-1, where 1 is identical)
        """
        if self.vector.shape != other.vector.shape:
            raise ValueError("Concept vectors must have same dimensions")

        # Cosine similarity
        norm_self = np.linalg.norm(self.vector)
        norm_other = np.linalg.norm(other.vector)

        if norm_self == 0 or norm_other == 0:
            return 0.0

        similarity = np.dot(self.vector, other.vector) / (norm_self * norm_other)
        # Normalize to [0, 1]
        return (similarity + 1) / 2

    def tension(self, other: 'PhilosophicalConcept') -> float:
        """
        Calculate tension with another concept.

        Tension is inverse of similarity.

        Args:
            other: Another philosophical concept

        Returns:
            Tension score (0-1, where 1 is maximum tension)
        """
        return 1.0 - self.similarity(other)

    def distance(self, other: 'PhilosophicalConcept') -> float:
        """
        Calculate Euclidean distance to another concept.

        Args:
            other: Another philosophical concept

        Returns:
            Distance in concept space
        """
        if self.vector.shape != other.vector.shape:
            raise ValueError("Concept vectors must have same dimensions")

        return float(np.linalg.norm(self.vector - other.vector))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "philosopher": self.philosopher,
            "vector": self.vector.tolist(),
            "confidence": self.confidence,
            "metadata": self.metadata
        }


class ConceptQuantifier(Tensor):
    """
    Tensor for quantifying philosophical concepts.

    This tensor provides numerical representations of philosophical
    concepts, enabling mathematical operations on ideas.

    Dimensions represent conceptual axes:
    0: Abstract ←→ Concrete
    1: Subjective ←→ Objective
    2: Individual ←→ Universal
    3: Static ←→ Dynamic
    4: Positive ←→ Negative (valence)
    5: Rational ←→ Intuitive
    6: Ethical ←→ Aesthetic
    7: Freedom ←→ Determinism
    """

    DEFAULT_DIMENSIONS = 8

    def __init__(self, dimensions: int = DEFAULT_DIMENSIONS):
        super().__init__(
            name="Concept_Quantifier",
            dimensions=dimensions,
            metadata={"type": "philosophical_concept"}
        )

        self.dimension_names = [
            "abstract_concrete",
            "subjective_objective",
            "individual_universal",
            "static_dynamic",
            "positive_negative",
            "rational_intuitive",
            "ethical_aesthetic",
            "freedom_determinism"
        ]

        # Library of quantified concepts
        self.concept_library: Dict[str, Dict[str, PhilosophicalConcept]] = {}
        self._initialize_concept_library()

    def compute(self, concept_name: str, philosopher: str,
                text: Optional[str] = None,
                context: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Compute quantification for a philosophical concept.

        Args:
            concept_name: Name of the concept (e.g., "freedom", "being")
            philosopher: Name of the philosopher
            text: Optional text context for concept extraction
            context: Optional additional context

        Returns:
            Quantified concept vector
        """
        # Check if we have this concept in library
        if concept_name in self.concept_library:
            if philosopher in self.concept_library[concept_name]:
                cached = self.concept_library[concept_name][philosopher]
                self.data = cached.vector.copy()
                return self.data

        # Otherwise, quantify from text or use defaults
        if text:
            self.data = self._quantify_from_text(concept_name, text, philosopher)
        else:
            self.data = self._get_default_quantification(concept_name, philosopher)

        return self.data

    def _initialize_concept_library(self) -> None:
        """Initialize library with key philosophical concepts."""
        # Sartre: Freedom
        self.add_concept(PhilosophicalConcept(
            name="freedom",
            philosopher="sartre",
            vector=np.array([0.3, 0.6, 0.4, 0.8, 0.5, 0.6, 0.9, 0.95]),
            # abstract, subjective, individual, dynamic, positive, balance, ethical, freedom
            confidence=0.95,
            metadata={"description": "Radical freedom and responsibility"}
        ))

        # Heidegger: Being (Sein)
        self.add_concept(PhilosophicalConcept(
            name="being",
            philosopher="heidegger",
            vector=np.array([0.9, 0.5, 0.8, 0.7, 0.5, 0.3, 0.4, 0.4]),
            # highly abstract, balance subj/obj, universal, dynamic, neutral, intuitive
            confidence=0.9,
            metadata={"description": "Being as fundamental question"}
        ))

        # Nietzsche: Will to Power
        self.add_concept(PhilosophicalConcept(
            name="will_to_power",
            philosopher="nietzsche",
            vector=np.array([0.4, 0.5, 0.6, 0.9, 0.7, 0.6, 0.5, 0.8]),
            # somewhat abstract, subjective, individual/universal, highly dynamic, positive, balance
            confidence=0.92,
            metadata={"description": "Fundamental life force and drive"}
        ))

        # Derrida: Différance
        self.add_concept(PhilosophicalConcept(
            name="differance",
            philosopher="derrida",
            vector=np.array([0.95, 0.6, 0.9, 0.95, 0.5, 0.7, 0.3, 0.5]),
            # highly abstract, subjective, universal, dynamic, neutral, rational/intuitive
            confidence=0.85,
            metadata={"description": "Difference and deferral in language"}
        ))

        # Wittgenstein: Language Games
        self.add_concept(PhilosophicalConcept(
            name="language_games",
            philosopher="wittgenstein",
            vector=np.array([0.5, 0.4, 0.7, 0.7, 0.5, 0.8, 0.2, 0.4]),
            # balance abstract/concrete, objective, universal, dynamic, neutral, rational
            confidence=0.88,
            metadata={"description": "Forms of life and rule-following"}
        ))

        # Confucius: Ren (仁 - Benevolence)
        self.add_concept(PhilosophicalConcept(
            name="ren",
            philosopher="confucius",
            vector=np.array([0.4, 0.5, 0.3, 0.4, 0.9, 0.6, 0.9, 0.3]),
            # somewhat abstract, balance, individual, somewhat static, positive, balance, ethical
            confidence=0.9,
            metadata={"description": "Benevolence and humaneness"}
        ))

        # Zhuangzi: Wu Wei (無為 - Non-action)
        self.add_concept(PhilosophicalConcept(
            name="wu_wei",
            philosopher="zhuangzi",
            vector=np.array([0.6, 0.6, 0.5, 0.6, 0.6, 0.2, 0.6, 0.6]),
            # abstract, subjective, balance, somewhat dynamic, positive, intuitive, balance
            confidence=0.87,
            metadata={"description": "Effortless action in harmony with Dao"}
        ))

    def add_concept(self, concept: PhilosophicalConcept) -> None:
        """
        Add a concept to the library.

        Args:
            concept: Philosophical concept to add
        """
        if concept.name not in self.concept_library:
            self.concept_library[concept.name] = {}

        self.concept_library[concept.name][concept.philosopher] = concept

    def get_concept(self, concept_name: str, philosopher: str) -> Optional[PhilosophicalConcept]:
        """
        Retrieve a concept from the library.

        Args:
            concept_name: Name of the concept
            philosopher: Name of the philosopher

        Returns:
            Philosophical concept or None if not found
        """
        if concept_name in self.concept_library:
            return self.concept_library[concept_name].get(philosopher)
        return None

    def find_similar_concepts(self, concept: PhilosophicalConcept,
                            threshold: float = 0.7) -> List[Tuple[PhilosophicalConcept, float]]:
        """
        Find concepts similar to the given concept.

        Args:
            concept: Reference concept
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of (concept, similarity_score) tuples
        """
        similar = []

        for concept_name, philosophers in self.concept_library.items():
            for phil_name, other_concept in philosophers.items():
                # Skip self
                if (other_concept.name == concept.name and
                    other_concept.philosopher == concept.philosopher):
                    continue

                similarity = concept.similarity(other_concept)
                if similarity >= threshold:
                    similar.append((other_concept, similarity))

        # Sort by similarity (descending)
        similar.sort(key=lambda x: x[1], reverse=True)
        return similar

    def find_tensions(self, concept: PhilosophicalConcept,
                     threshold: float = 0.7) -> List[Tuple[PhilosophicalConcept, float]]:
        """
        Find concepts in tension with the given concept.

        Args:
            concept: Reference concept
            threshold: Minimum tension threshold (0-1)

        Returns:
            List of (concept, tension_score) tuples
        """
        tensions = []

        for concept_name, philosophers in self.concept_library.items():
            for phil_name, other_concept in philosophers.items():
                # Skip self
                if (other_concept.name == concept.name and
                    other_concept.philosopher == concept.philosopher):
                    continue

                tension = concept.tension(other_concept)
                if tension >= threshold:
                    tensions.append((other_concept, tension))

        # Sort by tension (descending)
        tensions.sort(key=lambda x: x[1], reverse=True)
        return tensions

    def calculate_concept_space_position(self, concepts: List[PhilosophicalConcept]) -> np.ndarray:
        """
        Calculate the centroid position in concept space for multiple concepts.

        Args:
            concepts: List of philosophical concepts

        Returns:
            Centroid vector in concept space
        """
        if not concepts:
            return np.zeros(self.dimensions)

        # Weight by confidence
        vectors = np.array([c.vector for c in concepts])
        confidences = np.array([c.confidence for c in concepts])

        # Weighted average
        weighted_vectors = vectors * confidences[:, np.newaxis]
        centroid = np.sum(weighted_vectors, axis=0) / np.sum(confidences)

        return centroid

    def _quantify_from_text(self, concept_name: str, text: str, philosopher: str) -> np.ndarray:
        """
        Quantify a concept from text analysis.

        Args:
            concept_name: Name of the concept
            text: Text to analyze
            philosopher: Name of the philosopher

        Returns:
            Quantified concept vector
        """
        text_lower = text.lower()
        vector = np.zeros(self.dimensions)

        # Abstract ←→ Concrete
        abstract_words = ["abstract", "theoretical", "concept", "idea", "essence"]
        concrete_words = ["concrete", "practical", "specific", "particular", "example"]
        abstract_score = sum(1 for w in abstract_words if w in text_lower)
        concrete_score = sum(1 for w in concrete_words if w in text_lower)
        vector[0] = 0.5 + 0.4 * (abstract_score - concrete_score) / max(abstract_score + concrete_score, 1)

        # Subjective ←→ Objective
        subjective_words = ["feel", "believe", "think", "personal", "subjective"]
        objective_words = ["fact", "objective", "evidence", "proven", "reality"]
        subj_score = sum(1 for w in subjective_words if w in text_lower)
        obj_score = sum(1 for w in objective_words if w in text_lower)
        vector[1] = 0.5 + 0.4 * (subj_score - obj_score) / max(subj_score + obj_score, 1)

        # Individual ←→ Universal
        indiv_words = ["individual", "personal", "unique", "particular", "self"]
        univ_words = ["universal", "general", "common", "collective", "all"]
        indiv_score = sum(1 for w in indiv_words if w in text_lower)
        univ_score = sum(1 for w in univ_words if w in text_lower)
        vector[2] = 0.5 + 0.4 * (indiv_score - univ_score) / max(indiv_score + univ_score, 1)

        # Static ←→ Dynamic
        static_words = ["static", "fixed", "unchanging", "permanent", "eternal"]
        dynamic_words = ["dynamic", "changing", "evolving", "fluid", "becoming"]
        static_score = sum(1 for w in static_words if w in text_lower)
        dynamic_score = sum(1 for w in dynamic_words if w in text_lower)
        vector[3] = 0.5 + 0.4 * (dynamic_score - static_score) / max(static_score + dynamic_score, 1)

        # Positive ←→ Negative (valence)
        positive_words = ["good", "positive", "beneficial", "affirming", "joy"]
        negative_words = ["bad", "negative", "harmful", "denying", "suffering"]
        pos_score = sum(1 for w in positive_words if w in text_lower)
        neg_score = sum(1 for w in negative_words if w in text_lower)
        vector[4] = 0.5 + 0.4 * (pos_score - neg_score) / max(pos_score + neg_score, 1)

        # Rational ←→ Intuitive
        rational_words = ["rational", "logical", "reason", "analysis", "calculate"]
        intuitive_words = ["intuitive", "feeling", "sense", "instinct", "immediate"]
        rat_score = sum(1 for w in rational_words if w in text_lower)
        int_score = sum(1 for w in intuitive_words if w in text_lower)
        vector[5] = 0.5 + 0.4 * (rat_score - int_score) / max(rat_score + int_score, 1)

        # Ethical ←→ Aesthetic
        ethical_words = ["ethical", "moral", "right", "ought", "duty"]
        aesthetic_words = ["aesthetic", "beautiful", "art", "form", "style"]
        eth_score = sum(1 for w in ethical_words if w in text_lower)
        aes_score = sum(1 for w in aesthetic_words if w in text_lower)
        vector[6] = 0.5 + 0.4 * (eth_score - aes_score) / max(eth_score + aes_score, 1)

        # Freedom ←→ Determinism
        freedom_words = ["freedom", "choice", "will", "agency", "autonomy"]
        determ_words = ["determinism", "necessity", "determined", "caused", "fated"]
        free_score = sum(1 for w in freedom_words if w in text_lower)
        det_score = sum(1 for w in determ_words if w in text_lower)
        vector[7] = 0.5 + 0.4 * (free_score - det_score) / max(free_score + det_score, 1)

        # Clip to [0, 1]
        vector = np.clip(vector, 0.0, 1.0)

        return vector

    def _get_default_quantification(self, concept_name: str, philosopher: str) -> np.ndarray:
        """
        Get default quantification for unknown concepts.

        Args:
            concept_name: Name of the concept
            philosopher: Name of the philosopher

        Returns:
            Default concept vector
        """
        # Return neutral/balanced vector
        return np.full(self.dimensions, 0.5, dtype=np.float64)

    def export_concept_map(self) -> Dict[str, Any]:
        """
        Export the complete concept map for visualization.

        Returns:
            Dictionary with all concepts and their relationships
        """
        concepts_export = {}

        for concept_name, philosophers in self.concept_library.items():
            concepts_export[concept_name] = {}
            for phil_name, concept in philosophers.items():
                concepts_export[concept_name][phil_name] = concept.to_dict()

        return {
            "dimension_names": self.dimension_names,
            "concepts": concepts_export,
            "total_concepts": sum(len(p) for p in self.concept_library.values())
        }
