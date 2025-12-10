"""
Tests for Derrida Philosopher Module

Tests Derrida's deconstructionist analysis focusing on:
- Binary oppositions
- Traces (absent presences)
- Différance
- Contradictions
"""

import pytest

from po_core.philosophers.derrida import Derrida


class TestDerridaBasicFunctionality:
    """Test basic functionality of Derrida philosopher."""

    def test_derrida_initialization(self):
        """Test that Derrida initializes correctly."""
        derrida = Derrida()
        assert derrida.name == "Jacques Derrida"
        assert "Deconstructionist" in derrida.description
        assert "différance" in derrida.description

    def test_derrida_repr(self):
        """Test string representation."""
        derrida = Derrida()
        repr_str = repr(derrida)
        assert "Derrida" in repr_str
        assert "Jacques Derrida" in repr_str

    def test_derrida_str(self):
        """Test human-readable string."""
        derrida = Derrida()
        str_output = str(derrida)
        assert "🧠" in str_output
        assert "Jacques Derrida" in str_output


class TestDerridaReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "binary_oppositions" in result
        assert "traces" in result
        assert "differance" in result
        assert "contradictions" in result
        assert "what_is_excluded" in result
        assert "metadata" in result


class TestDerridaBinaryOppositions:
    """Test detection of binary oppositions."""

    def test_binary_oppositions_detected(self):
        """Test detection of binary oppositions."""
        derrida = Derrida()
        result = derrida.reason("What is true and what is false?")

        binaries = result["binary_oppositions"]
        assert isinstance(binaries, list)
        assert len(binaries) > 0
        assert any("true" in b["opposition"].lower() for b in binaries)

    def test_implicit_oppositions(self, simple_prompt):
        """Test detection of implicit oppositions."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        binaries = result["binary_oppositions"]
        assert len(binaries) > 0

    def test_multiple_oppositions(self):
        """Test detection of multiple oppositions."""
        derrida = Derrida()
        result = derrida.reason("The real authentic self versus the false appearance")

        binaries = result["binary_oppositions"]
        assert len(binaries) >= 2


class TestDerridaTraces:
    """Test detection of traces (absent presences)."""

    def test_traces_detected(self, simple_prompt):
        """Test that traces are detected."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        traces = result["traces"]
        assert isinstance(traces, list)
        assert len(traces) > 0

    def test_negation_creates_trace(self):
        """Test that negation creates a trace."""
        derrida = Derrida()
        result = derrida.reason("This is not what I meant")

        traces = result["traces"]
        assert any("negation" in t.lower() for t in traces)

    def test_absence_as_trace(self):
        """Test that absence is recognized as trace."""
        derrida = Derrida()
        result = derrida.reason("What is missing shapes what is present")

        traces = result["traces"]
        assert any("absence" in t.lower() or "missing" in t.lower() for t in traces)


class TestDerridaDifferance:
    """Test différance analysis."""

    def test_differance_structure(self, simple_prompt):
        """Test that différance has correct structure."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        differance = result["differance"]
        assert isinstance(differance, dict)
        assert "temporal_deferral" in differance
        assert "spatial_difference" in differance
        assert "status" in differance

    def test_temporal_deferral_detection(self):
        """Test detection of temporal deferral."""
        derrida = Derrida()
        result = derrida.reason("I will become who I am meant to be")

        differance = result["differance"]
        assert differance["temporal_deferral"] is True

    def test_spatial_difference_detection(self):
        """Test detection of spatial difference."""
        derrida = Derrida()
        result = derrida.reason("This is different from that")

        differance = result["differance"]
        assert differance["spatial_difference"] is True


class TestDerridaContradictions:
    """Test detection of contradictions."""

    def test_contradictions_detected(self, simple_prompt):
        """Test that contradictions are detected."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        contradictions = result["contradictions"]
        assert isinstance(contradictions, list)
        assert len(contradictions) > 0

    def test_explicit_contradiction(self):
        """Test detection of explicit contradiction."""
        derrida = Derrida()
        result = derrida.reason("I am authentic but also inauthentic")

        contradictions = result["contradictions"]
        assert len(contradictions) > 0


class TestDerridaExclusion:
    """Test detection of what is excluded."""

    def test_excluded_detected(self, simple_prompt):
        """Test that excluded elements are detected."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        excluded = result["what_is_excluded"]
        assert isinstance(excluded, list)
        assert len(excluded) > 0

    def test_meaning_excludes_nonsense(self):
        """Test that meaning excludes nonsense."""
        derrida = Derrida()
        result = derrida.reason("What is the meaning of life?")

        excluded = result["what_is_excluded"]
        assert any("nonsense" in e.lower() or "ambiguity" in e.lower() for e in excluded)


class TestDerridaReasoning:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_deconstruction(self, simple_prompt):
        """Test that reasoning mentions deconstruction."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "deconstruction" in reasoning.lower() or "différance" in reasoning.lower()


class TestDerridaEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        derrida = Derrida()
        result = derrida.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result
        assert "binary_oppositions" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        derrida = Derrida()
        result = derrida.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)
