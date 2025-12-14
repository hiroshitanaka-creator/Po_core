"""
Philosophical Annotator

Automatically adds philosophical annotations to reasoning traces.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PhilosophicalAnnotation:
    """
    Philosophical annotation for a reasoning step.

    Attributes:
        philosopher: Source philosopher
        concept: Philosophical concept applied
        explanation: Explanation of the concept
        relevance: Why this concept is relevant
        references: Related philosophical references
    """

    philosopher: str
    concept: str
    explanation: str
    relevance: str
    references: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "philosopher": self.philosopher,
            "concept": self.concept,
            "explanation": self.explanation,
            "relevance": self.relevance,
            "references": self.references,
        }


class PhilosophicalAnnotator:
    """
    Annotates reasoning with philosophical concepts.

    Maps reasoning steps to philosophical frameworks and adds
    explanatory annotations.
    """

    def __init__(self) -> None:
        """Initialize annotator with philosophical knowledge base."""
        self.concept_library = self._initialize_concept_library()

    def _initialize_concept_library(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize library of philosophical concepts.

        Returns:
            Dictionary mapping concept keywords to details
        """
        return {
            # Existentialism
            "freedom": {
                "philosopher": "Jean-Paul Sartre",
                "concept": "Radical Freedom",
                "explanation": "Humans are condemned to be free and must take full responsibility for their choices.",
                "references": ["Being and Nothingness", "Existentialism is a Humanism"],
            },
            "authenticity": {
                "philosopher": "Martin Heidegger",
                "concept": "Authentic Existence (Eigentlichkeit)",
                "explanation": "Living in accordance with one's own possibilities rather than social expectations.",
                "references": ["Being and Time"],
            },
            "dasein": {
                "philosopher": "Martin Heidegger",
                "concept": "Dasein (Being-there)",
                "explanation": "Human existence characterized by being-in-the-world and temporal awareness.",
                "references": ["Being and Time"],
            },
            # Phenomenology
            "consciousness": {
                "philosopher": "Edmund Husserl",
                "concept": "Intentionality of Consciousness",
                "explanation": "Consciousness is always consciousness of something; it is directed toward objects.",
                "references": ["Ideas", "Cartesian Meditations"],
            },
            # Ethics
            "responsibility": {
                "philosopher": "Emmanuel Levinas",
                "concept": "Ethical Responsibility",
                "explanation": "Ethics as first philosophy; infinite responsibility to the Other.",
                "references": ["Totality and Infinity", "Otherwise than Being"],
            },
            # Deconstruction
            "trace": {
                "philosopher": "Jacques Derrida",
                "concept": "Trace (La Trace)",
                "explanation": "The mark of absence that shapes presence; meaning is differential and deferred.",
                "references": ["Of Grammatology", "Writing and Difference"],
            },
            "difference": {
                "philosopher": "Jacques Derrida",
                "concept": "Différance",
                "explanation": "Meaning is both different and deferred; no pure presence exists.",
                "references": ["Margins of Philosophy"],
            },
            # Will to Power
            "power": {
                "philosopher": "Friedrich Nietzsche",
                "concept": "Will to Power",
                "explanation": "Fundamental drive of all living things to assert and enhance their power.",
                "references": ["Thus Spoke Zarathustra", "Beyond Good and Evil"],
            },
            "ubermensch": {
                "philosopher": "Friedrich Nietzsche",
                "concept": "Übermensch (Overman)",
                "explanation": "One who creates their own values and overcomes nihilism.",
                "references": ["Thus Spoke Zarathustra"],
            },
            # Language
            "language_game": {
                "philosopher": "Ludwig Wittgenstein",
                "concept": "Language Game",
                "explanation": "Meaning emerges from use within specific forms of life and practices.",
                "references": ["Philosophical Investigations"],
            },
            # Phenomenology of Perception
            "embodiment": {
                "philosopher": "Maurice Merleau-Ponty",
                "concept": "Embodied Consciousness",
                "explanation": "Consciousness is fundamentally embodied and situated in the world.",
                "references": ["Phenomenology of Perception"],
            },
            # Eastern Philosophy
            "wu_wei": {
                "philosopher": "Zhuangzi",
                "concept": "Wu Wei (Non-action)",
                "explanation": "Effortless action in harmony with the natural flow of things.",
                "references": ["Zhuangzi"],
            },
            "ren": {
                "philosopher": "Confucius",
                "concept": "Ren (Humaneness)",
                "explanation": "Fundamental virtue of benevolence and humaneness toward others.",
                "references": ["Analects"],
            },
        }

    def annotate_reasoning(
        self,
        reasoning: Dict[str, Any],
        philosopher: Optional[str] = None,
    ) -> List[PhilosophicalAnnotation]:
        """
        Generate philosophical annotations for reasoning.

        Args:
            reasoning: Reasoning dictionary to annotate
            philosopher: Source philosopher (optional)

        Returns:
            List of philosophical annotations
        """
        annotations = []

        # Extract text content from reasoning
        text_content = self._extract_text(reasoning)

        # Find relevant concepts
        for keyword, concept_info in self.concept_library.items():
            if keyword in text_content.lower():
                # Create annotation
                annotation = PhilosophicalAnnotation(
                    philosopher=concept_info["philosopher"],
                    concept=concept_info["concept"],
                    explanation=concept_info["explanation"],
                    relevance=f"This concept appears relevant to the reasoning about: {keyword}",
                    references=concept_info["references"],
                )
                annotations.append(annotation)

        # Add philosopher-specific annotations if specified
        if philosopher:
            phil_annotations = self._get_philosopher_annotations(
                philosopher, text_content
            )
            annotations.extend(phil_annotations)

        return annotations

    def _extract_text(self, data: Any) -> str:
        """
        Extract text content from various data structures.

        Args:
            data: Data to extract text from

        Returns:
            Combined text content
        """
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            texts = []
            for value in data.values():
                texts.append(self._extract_text(value))
            return " ".join(texts)
        elif isinstance(data, list):
            return " ".join(self._extract_text(item) for item in data)
        else:
            return str(data)

    def _get_philosopher_annotations(
        self, philosopher: str, text: str
    ) -> List[PhilosophicalAnnotation]:
        """
        Get philosopher-specific annotations.

        Args:
            philosopher: Philosopher name
            text: Text content

        Returns:
            List of annotations
        """
        annotations = []

        # Philosopher-specific concept mapping
        philosopher_concepts = {
            "Martin Heidegger": ["dasein", "authenticity"],
            "Jean-Paul Sartre": ["freedom", "responsibility"],
            "Jacques Derrida": ["trace", "difference"],
            "Friedrich Nietzsche": ["power", "ubermensch"],
            "Ludwig Wittgenstein": ["language_game"],
            "Maurice Merleau-Ponty": ["embodiment"],
            "Zhuangzi": ["wu_wei"],
            "Confucius": ["ren"],
        }

        # Find concepts for this philosopher
        concepts = philosopher_concepts.get(philosopher, [])

        for concept_key in concepts:
            if concept_key in self.concept_library:
                concept_info = self.concept_library[concept_key]
                annotation = PhilosophicalAnnotation(
                    philosopher=philosopher,
                    concept=concept_info["concept"],
                    explanation=concept_info["explanation"],
                    relevance=f"{philosopher}'s perspective applies this concept to the reasoning",
                    references=concept_info["references"],
                )
                annotations.append(annotation)

        return annotations

    def annotate_trace_entry(
        self, trace_entry: Dict[str, Any]
    ) -> List[PhilosophicalAnnotation]:
        """
        Annotate a trace entry.

        Args:
            trace_entry: Trace entry dictionary

        Returns:
            List of annotations
        """
        philosopher = trace_entry.get("philosopher")
        data = trace_entry.get("data", {})

        return self.annotate_reasoning(data, philosopher)

    def get_concept_explanation(self, concept_keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get explanation for a philosophical concept.

        Args:
            concept_keyword: Keyword for the concept

        Returns:
            Concept information dictionary, or None if not found
        """
        return self.concept_library.get(concept_keyword.lower())

    def add_concept(
        self,
        keyword: str,
        philosopher: str,
        concept: str,
        explanation: str,
        references: List[str],
    ) -> None:
        """
        Add a new concept to the library.

        Args:
            keyword: Keyword identifier
            philosopher: Source philosopher
            concept: Concept name
            explanation: Explanation of the concept
            references: List of reference works
        """
        self.concept_library[keyword.lower()] = {
            "philosopher": philosopher,
            "concept": concept,
            "explanation": explanation,
            "references": references,
        }
