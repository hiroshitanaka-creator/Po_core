"""
Heidegger - Phenomenological Philosopher

Martin Heidegger (1889-1976)
Focus: Being and Time, Dasein (Being-there), Existential Analysis

Key Concepts:
- Dasein: Human existence as "being-in-the-world"
- Being vs. Beings: The ontological difference
- Temporality: Past, present, and future as constitutive of being
- Authenticity vs. Inauthenticity
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Heidegger(Philosopher):
    """
    Heidegger's phenomenological perspective.

    Analyzes prompts through the lens of Being and Time,
    focusing on existence, temporality, and authenticity.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Martin Heidegger",
            description="Phenomenologist focused on Being, Time, and Dasein (being-in-the-world)"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Heidegger's phenomenological perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Heidegger's philosophical analysis
        """
        # Basic existential analysis
        analysis = self._analyze_being(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Phenomenological / Existential",
            "key_concepts": analysis["concepts"],
            "questions": analysis["questions"],
            "temporal_dimension": analysis["temporality"],
            "authenticity_check": analysis["authenticity"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Being and Time analysis",
                "focus": "Dasein, temporality, and meaning"
            }
        }

    def _analyze_being(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Heideggerian existential analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Identify key existential themes
        concepts = []
        questions = []

        # Check for temporal dimensions
        has_past = any(word in prompt.lower() for word in ["was", "were", "had", "before", "past"])
        has_future = any(word in prompt.lower() for word in ["will", "shall", "future", "tomorrow"])
        has_present = any(word in prompt.lower() for word in ["is", "are", "now", "today", "currently"])

        temporality = {
            "past_present": has_past,
            "future_oriented": has_future,
            "present_focused": has_present,
            "temporal_awareness": "Multi-temporal" if (has_past and has_future) else "Single-temporal"
        }

        # Check for existential themes
        if any(word in prompt.lower() for word in ["being", "exist", "meaning", "purpose"]):
            concepts.append("Dasein (Being-in-the-world)")
            questions.append("What does it mean to be?")

        if any(word in prompt.lower() for word in ["authentic", "genuine", "true", "real"]):
            concepts.append("Authenticity")
            questions.append("Is this an authentic mode of being?")

        if any(word in prompt.lower() for word in ["time", "moment", "duration", "when"]):
            concepts.append("Temporality")
            questions.append("How does time constitute this being?")

        # Default concepts if none found
        if not concepts:
            concepts.append("Being-in-the-world")
            questions.append("What is the mode of being here?")

        # Assess authenticity
        authenticity_indicators = ["choice", "responsibility", "freedom", "own"]
        inauthenticity_indicators = ["they", "everyone", "always", "supposed to"]

        auth_score = sum(1 for word in authenticity_indicators if word in prompt.lower())
        inauth_score = sum(1 for word in inauthenticity_indicators if word in prompt.lower())

        if auth_score > inauth_score:
            authenticity = "Tends toward authentic being"
        elif inauth_score > auth_score:
            authenticity = "Shows signs of 'Das Man' (they-self)"
        else:
            authenticity = "Neutral - requires deeper analysis"

        reasoning = (
            f"From a Heideggerian perspective, this prompt invites us to question "
            f"the nature of being itself. {concepts[0]} emerges as a central theme. "
            f"The temporal structure reveals a {temporality['temporal_awareness'].lower()} orientation. "
            f"Authenticity assessment: {authenticity}."
        )

        return {
            "reasoning": reasoning,
            "concepts": concepts,
            "questions": questions,
            "temporality": temporality,
            "authenticity": authenticity
        }
