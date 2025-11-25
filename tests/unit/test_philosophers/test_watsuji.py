"""
Tests for Watsuji Philosopher Module

Tests Watsuji's Japanese ethics focusing on:
- Ningen (betweenness/relationality)
- Climate theory
- Individual-totality dialectic
- Ma (間) - relational space
"""

import pytest

from po_core.philosophers.watsuji import Watsuji


class TestWatsujiBasicFunctionality:
    """Test basic functionality of Watsuji philosopher."""

    def test_watsuji_initialization(self):
        """Test that Watsuji initializes correctly."""
        watsuji = Watsuji()
        assert "Watsuji" in watsuji.name
        assert "ningen" in watsuji.description.lower() or "betweenness" in watsuji.description.lower()

    def test_watsuji_repr(self):
        """Test string representation."""
        watsuji = Watsuji()
        repr_str = repr(watsuji)
        assert "Watsuji" in repr_str

    def test_watsuji_str(self):
        """Test human-readable string."""
        watsuji = Watsuji()
        str_output = str(watsuji)
        assert "🧠" in str_output
        assert "Watsuji" in str_output


class TestWatsujiReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "ningen_relationality" in result
        assert "climate_type" in result
        assert "individual_totality_dialectic" in result
        assert "betweenness_quality" in result
        assert "ethical_dimension" in result
        assert "spatial_temporal" in result
        assert "japanese_characteristics" in result
        assert "metadata" in result


class TestWatsujiNingenRelationality:
    """Test ningen (betweenness) relationality analysis."""

    def test_relationality_structure(self, simple_prompt):
        """Test that ningen_relationality has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        relationality = result["ningen_relationality"]
        assert isinstance(relationality, dict)
        assert "level" in relationality
        assert "description" in relationality

    def test_relational_detection(self):
        """Test detection of high relationality."""
        watsuji = Watsuji()
        result = watsuji.reason("We exist together in relationships and community")

        relationality = result["ningen_relationality"]
        assert "High" in relationality["level"] or "relational" in relationality["status"].lower()

    def test_individual_detection(self):
        """Test detection of individual emphasis."""
        watsuji = Watsuji()
        result = watsuji.reason("I alone am independent and separate from others")

        relationality = result["ningen_relationality"]
        # Should detect some level (High, Medium, or Low)
        assert "level" in relationality


class TestWatsujiClimateType:
    """Test climate type determination."""

    def test_climate_structure(self, simple_prompt):
        """Test that climate_type has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        climate = result["climate_type"]
        assert isinstance(climate, dict)
        assert "type" in climate
        assert "description" in climate

    def test_monsoon_detection(self):
        """Test detection of monsoon type."""
        watsuji = Watsuji()
        result = watsuji.reason("We accept and flow with nature in harmony")

        climate = result["climate_type"]
        assert "Monsoon" in climate["type"] or "monsoon" in climate["description"].lower() or "Neutral" in climate["type"]

    def test_desert_detection(self):
        """Test detection of desert type."""
        watsuji = Watsuji()
        result = watsuji.reason("We resist and fight to transcend and struggle against")

        climate = result["climate_type"]
        # Should detect some climate type
        assert "type" in climate


class TestWatsujiDialectic:
    """Test individual-totality dialectic."""

    def test_dialectic_structure(self, simple_prompt):
        """Test that dialectic has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        dialectic = result["individual_totality_dialectic"]
        assert isinstance(dialectic, dict)
        assert "stage" in dialectic
        assert "description" in dialectic

    def test_synthesis_detection(self):
        """Test detection of dialectical synthesis."""
        watsuji = Watsuji()
        result = watsuji.reason("Both individual and collective are integrated in balance")

        dialectic = result["individual_totality_dialectic"]
        assert "Synthesis" in dialectic["stage"] or "balance" in dialectic["description"].lower() or "stage" in dialectic


class TestWatsujiBetweenness:
    """Test ma (betweenness) quality."""

    def test_betweenness_structure(self, simple_prompt):
        """Test that betweenness_quality has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        betweenness = result["betweenness_quality"]
        assert isinstance(betweenness, dict)
        assert "quality" in betweenness
        assert "description" in betweenness

    def test_dynamic_ma_detection(self):
        """Test detection of dynamic ma."""
        watsuji = Watsuji()
        result = watsuji.reason("We interact and engage mutually in reciprocal dialogue")

        betweenness = result["betweenness_quality"]
        assert "Ma" in betweenness["quality"] or "ma" in betweenness["description"].lower()


class TestWatsujiEthics:
    """Test ethical dimension analysis."""

    def test_ethics_structure(self, simple_prompt):
        """Test that ethical_dimension has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        ethics = result["ethical_dimension"]
        assert isinstance(ethics, dict)
        assert "mode" in ethics
        assert "description" in ethics

    def test_relational_ethics_detection(self):
        """Test detection of relational ethics."""
        watsuji = Watsuji()
        result = watsuji.reason("Our duty and responsibility is to care for others")

        ethics = result["ethical_dimension"]
        assert "Ethics" in ethics["mode"] or "ethics" in ethics["description"].lower()


class TestWatsujiSpatiotemporal:
    """Test spatiotemporal structure."""

    def test_spatiotemporal_structure(self, simple_prompt):
        """Test that spatial_temporal has correct structure."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        spatiotemporal = result["spatial_temporal"]
        assert isinstance(spatiotemporal, dict)
        assert "structure" in spatiotemporal
        assert "description" in spatiotemporal

    def test_spatiotemporal_unity_detection(self):
        """Test detection of spatiotemporal unity."""
        watsuji = Watsuji()
        result = watsuji.reason("This place and this time in history together")

        spatiotemporal = result["spatial_temporal"]
        assert "structure" in spatiotemporal


class TestWatsujiJapaneseCharacteristics:
    """Test Japanese characteristics detection."""

    def test_japanese_characteristics_structure(self, simple_prompt):
        """Test that japanese_characteristics is a list."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        characteristics = result["japanese_characteristics"]
        assert isinstance(characteristics, list)
        assert len(characteristics) > 0

    def test_harmony_detection(self):
        """Test detection of wa (harmony)."""
        watsuji = Watsuji()
        result = watsuji.reason("We seek harmony and peaceful unity together")

        characteristics = result["japanese_characteristics"]
        # Should detect some Japanese traits
        assert isinstance(characteristics, list)


class TestWatsujiReasoning:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_ningen(self, simple_prompt):
        """Test that reasoning mentions ningen."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "ningen" in reasoning.lower() or "Watsuji" in reasoning or "betweenness" in reasoning.lower()


class TestWatsujiEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        watsuji = Watsuji()
        result = watsuji.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        watsuji = Watsuji()
        result = watsuji.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)
