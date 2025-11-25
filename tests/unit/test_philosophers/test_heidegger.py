"""
Tests for Heidegger Philosopher Module

Tests Heidegger's phenomenological analysis focusing on:
- Being (Dasein)
- Temporality (past, present, future)
- Authenticity vs Inauthenticity
"""

import pytest

from po_core.philosophers.heidegger import Heidegger


class TestHeideggerBasicFunctionality:
    """Test basic functionality of Heidegger philosopher."""

    def test_heidegger_initialization(self):
        """Test that Heidegger initializes correctly."""
        heidegger = Heidegger()

        assert heidegger.name == "Martin Heidegger"
        assert "Phenomenologist" in heidegger.description
        assert "Dasein" in heidegger.description

    def test_heidegger_repr(self):
        """Test string representation."""
        heidegger = Heidegger()

        repr_str = repr(heidegger)
        assert "Heidegger" in repr_str
        assert "Martin Heidegger" in repr_str

    def test_heidegger_str(self):
        """Test human-readable string."""
        heidegger = Heidegger()

        str_output = str(heidegger)
        assert "🧠" in str_output
        assert "Martin Heidegger" in str_output


class TestHeideggerReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        # Check required fields
        assert "reasoning" in result
        assert "perspective" in result
        assert "key_concepts" in result
        assert "questions" in result
        assert "temporal_dimension" in result
        assert "authenticity_check" in result
        assert "metadata" in result

    def test_reason_metadata_structure(self, simple_prompt):
        """Test that metadata has correct structure."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        metadata = result["metadata"]
        assert metadata["philosopher"] == "Martin Heidegger"
        assert "approach" in metadata
        assert "focus" in metadata

    def test_perspective_is_phenomenological(self, simple_prompt):
        """Test that perspective is phenomenological/existential."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        perspective = result["perspective"]
        assert "Phenomenological" in perspective or "Existential" in perspective


class TestHeideggerTemporalAnalysis:
    """Test Heidegger's temporal analysis capabilities."""

    def test_temporal_analysis_with_past(self):
        """Test detection of past temporal dimension."""
        heidegger = Heidegger()
        prompt = "I was happy before this happened."
        result = heidegger.reason(prompt)

        temporal = result["temporal_dimension"]
        assert temporal["past_present"] is True

    def test_temporal_analysis_with_future(self):
        """Test detection of future temporal dimension."""
        heidegger = Heidegger()
        prompt = "I will become who I am meant to be."
        result = heidegger.reason(prompt)

        temporal = result["temporal_dimension"]
        assert temporal["future_oriented"] is True

    def test_temporal_analysis_with_present(self):
        """Test detection of present temporal dimension."""
        heidegger = Heidegger()
        prompt = "I am here now, existing in this moment."
        result = heidegger.reason(prompt)

        temporal = result["temporal_dimension"]
        assert temporal["present_focused"] is True

    def test_multi_temporal_awareness(self, temporal_prompt):
        """Test detection of multi-temporal awareness."""
        heidegger = Heidegger()
        result = heidegger.reason(temporal_prompt)

        temporal = result["temporal_dimension"]
        assert temporal["temporal_awareness"] == "Multi-temporal"
        assert temporal["past_present"] is True
        assert temporal["future_oriented"] is True

    def test_single_temporal_awareness(self):
        """Test detection of single-temporal awareness."""
        heidegger = Heidegger()
        prompt = "I am present here and now."
        result = heidegger.reason(prompt)

        temporal = result["temporal_dimension"]
        assert temporal["temporal_awareness"] == "Single-temporal"


class TestHeideggerAuthenticityAnalysis:
    """Test Heidegger's authenticity vs inauthenticity analysis."""

    def test_authenticity_detection(self, authentic_prompt):
        """Test detection of authentic being."""
        heidegger = Heidegger()
        result = heidegger.reason(authentic_prompt)

        authenticity = result["authenticity_check"]
        assert "authentic" in authenticity.lower()

    def test_inauthenticity_detection(self, bad_faith_prompt):
        """Test detection of inauthentic being (Das Man)."""
        heidegger = Heidegger()
        result = heidegger.reason(bad_faith_prompt)

        authenticity = result["authenticity_check"]
        assert "Das Man" in authenticity or "they-self" in authenticity

    def test_neutral_authenticity(self):
        """Test neutral authenticity assessment."""
        heidegger = Heidegger()
        prompt = "The sky is blue."
        result = heidegger.reason(prompt)

        authenticity = result["authenticity_check"]
        assert "Neutral" in authenticity or "deeper analysis" in authenticity


class TestHeideggerKeyConceptsDetection:
    """Test detection of key Heideggerian concepts."""

    def test_dasein_concept_detection(self):
        """Test detection of Dasein (being-in-the-world)."""
        heidegger = Heidegger()
        prompt = "What does it mean to exist in the world?"
        result = heidegger.reason(prompt)

        concepts = result["key_concepts"]
        assert any("Dasein" in concept for concept in concepts)

    def test_authenticity_concept_detection(self):
        """Test detection of authenticity concept."""
        heidegger = Heidegger()
        prompt = "How can I live an authentic life?"
        result = heidegger.reason(prompt)

        concepts = result["key_concepts"]
        assert any("Authenticity" in concept for concept in concepts)

    def test_temporality_concept_detection(self):
        """Test detection of temporality concept."""
        heidegger = Heidegger()
        prompt = "Time shapes who we are."
        result = heidegger.reason(prompt)

        concepts = result["key_concepts"]
        assert any("Temporality" in concept for concept in concepts)

    def test_default_concept_when_no_match(self):
        """Test that a default concept is provided when no specific concept is detected."""
        heidegger = Heidegger()
        prompt = "The weather is nice today."
        result = heidegger.reason(prompt)

        concepts = result["key_concepts"]
        assert len(concepts) > 0
        assert any("Being" in concept for concept in concepts)


class TestHeideggerQuestions:
    """Test that Heidegger generates appropriate philosophical questions."""

    def test_questions_are_generated(self, simple_prompt):
        """Test that questions are generated."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        questions = result["questions"]
        assert len(questions) > 0
        assert all(isinstance(q, str) for q in questions)

    def test_questions_are_philosophical(self, existential_prompt):
        """Test that generated questions are philosophical."""
        heidegger = Heidegger()
        result = heidegger.reason(existential_prompt)

        questions = result["questions"]
        # Questions should end with '?'
        assert all(q.endswith("?") for q in questions)
        # Questions should be about being/existence
        assert any("be" in q.lower() or "being" in q.lower() for q in questions)


class TestHeideggerReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_heidegger(self, simple_prompt):
        """Test that reasoning mentions Heideggerian perspective."""
        heidegger = Heidegger()
        result = heidegger.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "Heidegger" in reasoning or "phenomenological" in reasoning.lower()

    def test_reasoning_coherence(self, existential_prompt):
        """Test that reasoning is coherent and mentions key concepts."""
        heidegger = Heidegger()
        result = heidegger.reason(existential_prompt)

        reasoning = result["reasoning"]
        # Should mention at least one key concept from the result
        concepts = result["key_concepts"]
        assert any(concept.split()[0].lower() in reasoning.lower() for concept in concepts)


class TestHeideggerEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        heidegger = Heidegger()
        result = heidegger.reason(empty_prompt)

        # Should still return a valid structure
        assert isinstance(result, dict)
        assert "reasoning" in result
        assert "key_concepts" in result

    def test_long_prompt(self, long_prompt):
        """Test handling of very long prompt."""
        heidegger = Heidegger()
        result = heidegger.reason(long_prompt)

        # Should successfully process without errors
        assert isinstance(result, dict)
        assert len(result["reasoning"]) > 0

    def test_special_characters_prompt(self):
        """Test handling of prompts with special characters."""
        heidegger = Heidegger()
        prompt = "What is @#$%^& being? !!! ???"
        result = heidegger.reason(prompt)

        # Should handle gracefully
        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_non_english_prompt(self):
        """Test handling of non-English prompt."""
        heidegger = Heidegger()
        prompt = "存在とは何か？"  # "What is being?" in Japanese
        result = heidegger.reason(prompt)

        # Should still return valid structure
        assert isinstance(result, dict)
        assert "reasoning" in result


class TestHeideggerWithContext:
    """Test Heidegger's reason method with context parameter."""

    def test_reason_accepts_context(self, simple_prompt):
        """Test that reason() accepts context parameter."""
        heidegger = Heidegger()
        context = {"previous_analysis": "Existential crisis"}

        # Should not raise an error
        result = heidegger.reason(simple_prompt, context=context)
        assert isinstance(result, dict)

    def test_reason_works_without_context(self, simple_prompt):
        """Test that reason() works without context parameter."""
        heidegger = Heidegger()

        result = heidegger.reason(simple_prompt)
        assert isinstance(result, dict)
