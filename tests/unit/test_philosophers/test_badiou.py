"""
Tests for Badiou Philosopher Module

Tests Badiou's philosophy focusing on:
- Event
- Truth procedures
- Fidelity to the event
- Subject formation
"""

import pytest

from po_core.philosophers.badiou import Badiou


class TestBadiouBasicFunctionality:
    """Test basic functionality of Badiou philosopher."""

    def test_badiou_initialization(self):
        """Test that Badiou initializes correctly."""
        badiou = Badiou()
        assert badiou.name == "Alain Badiou"
        assert "event" in badiou.description.lower() or "truth" in badiou.description.lower()

    def test_badiou_repr(self):
        """Test string representation."""
        badiou = Badiou()
        repr_str = repr(badiou)
        assert "Badiou" in repr_str

    def test_badiou_str(self):
        """Test human-readable string."""
        badiou = Badiou()
        str_output = str(badiou)
        assert "🧠" in str_output
        assert "Alain Badiou" in str_output


class TestBadiouReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "event" in result
        assert "truth_procedure" in result
        assert "fidelity" in result
        assert "subject" in result
        assert "void" in result
        assert "situation" in result
        assert "generic" in result
        assert "forcing" in result
        assert "subtraction" in result
        assert "metadata" in result


class TestBadiouEvent:
    """Test event analysis."""

    def test_event_structure(self, simple_prompt):
        """Test that event has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        event = result["event"]
        assert isinstance(event, dict)
        assert "presence" in event
        assert "description" in event

    def test_event_detection(self):
        """Test detection of event."""
        badiou = Badiou()
        result = badiou.reason("Something radically new and unprecedented happens that ruptures the situation")

        event = result["event"]
        assert "Event" in event["presence"] or "event" in event["description"].lower()


class TestBadiouTruthProcedure:
    """Test truth procedure analysis."""

    def test_truth_procedure_structure(self, simple_prompt):
        """Test that truth_procedure has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        truth = result["truth_procedure"]
        assert isinstance(truth, dict)
        assert "type" in truth
        assert "description" in truth

    def test_truth_procedure_detection(self):
        """Test detection of truth procedures."""
        badiou = Badiou()
        result = badiou.reason("Through science, art, politics, and love we create truths")

        truth = result["truth_procedure"]
        assert "type" in truth


class TestBadiouFidelity:
    """Test fidelity analysis."""

    def test_fidelity_structure(self, simple_prompt):
        """Test that fidelity has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        fidelity = result["fidelity"]
        assert isinstance(fidelity, dict)
        assert "level" in fidelity
        assert "description" in fidelity

    def test_fidelity_detection(self):
        """Test detection of fidelity to event."""
        badiou = Badiou()
        result = badiou.reason("I remain faithful and committed to what happened")

        fidelity = result["fidelity"]
        assert "Fidelity" in fidelity["level"] or "faithful" in fidelity["description"].lower()


class TestBadiouSubject:
    """Test subject formation analysis."""

    def test_subject_structure(self, simple_prompt):
        """Test that subject has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        subject = result["subject"]
        assert isinstance(subject, dict)
        assert "formation" in subject
        assert "description" in subject

    def test_subject_detection(self):
        """Test detection of subject formation."""
        badiou = Badiou()
        result = badiou.reason("I become a subject through fidelity to truth")

        subject = result["subject"]
        assert "formation" in subject


class TestBadiouVoid:
    """Test void analysis."""

    def test_void_structure(self, simple_prompt):
        """Test that void has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        void = result["void"]
        assert isinstance(void, dict)
        assert "presence" in void
        assert "description" in void

    def test_void_detection(self):
        """Test detection of the void."""
        badiou = Badiou()
        result = badiou.reason("The empty set, what is excluded and uncounted")

        void = result["void"]
        assert "presence" in void


class TestBadiouSituation:
    """Test situation analysis."""

    def test_situation_structure(self, simple_prompt):
        """Test that situation has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        situation = result["situation"]
        assert isinstance(situation, dict)
        assert "state" in situation
        assert "description" in situation

    def test_situation_detection(self):
        """Test detection of situation state."""
        badiou = Badiou()
        result = badiou.reason("The structured state of things as they are")

        situation = result["situation"]
        assert "state" in situation


class TestBadiouGeneric:
    """Test generic analysis."""

    def test_generic_structure(self, simple_prompt):
        """Test that generic has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        generic = result["generic"]
        assert isinstance(generic, dict)
        assert "presence" in generic
        assert "description" in generic

    def test_generic_detection(self):
        """Test detection of generic set."""
        badiou = Badiou()
        result = badiou.reason("The indiscernible and unnameable subset")

        generic = result["generic"]
        assert "presence" in generic


class TestBadiouForcing:
    """Test forcing analysis."""

    def test_forcing_structure(self, simple_prompt):
        """Test that forcing has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        forcing = result["forcing"]
        assert isinstance(forcing, dict)
        assert "presence" in forcing
        assert "description" in forcing

    def test_forcing_detection(self):
        """Test detection of forcing."""
        badiou = Badiou()
        result = badiou.reason("Forcing new truths into being from the future")

        forcing = result["forcing"]
        assert "presence" in forcing


class TestBadiouSubtraction:
    """Test subtraction analysis."""

    def test_subtraction_structure(self, simple_prompt):
        """Test that subtraction has correct structure."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        subtraction = result["subtraction"]
        assert isinstance(subtraction, dict)
        assert "presence" in subtraction
        assert "description" in subtraction

    def test_subtraction_detection(self):
        """Test detection of subtraction."""
        badiou = Badiou()
        result = badiou.reason("Subtracting from identities and representations")

        subtraction = result["subtraction"]
        assert "presence" in subtraction


class TestBadiouReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_badiou(self, simple_prompt):
        """Test that reasoning mentions Badiouian concepts."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "Badiou" in reasoning or "event" in reasoning.lower() or "truth" in reasoning.lower()


class TestBadiouEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        badiou = Badiou()
        result = badiou.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        badiou = Badiou()
        result = badiou.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)
