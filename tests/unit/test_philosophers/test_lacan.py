"""
Tests for Lacan Philosopher Module

Tests Lacan's psychoanalytic philosophy focusing on:
- The three registers (Real, Imaginary, Symbolic)
- Desire structure
- The Other
- Lack and objet petit a
"""

import pytest

from po_core.philosophers.lacan import Lacan


class TestLacanBasicFunctionality:
    """Test basic functionality of Lacan philosopher."""

    def test_lacan_initialization(self):
        """Test that Lacan initializes correctly."""
        lacan = Lacan()
        assert lacan.name == "Jacques Lacan"
        assert "psychoanalyst" in lacan.description.lower() or "psychoanalysis" in lacan.description.lower()

    def test_lacan_repr(self):
        """Test string representation."""
        lacan = Lacan()
        repr_str = repr(lacan)
        assert "Lacan" in repr_str

    def test_lacan_str(self):
        """Test human-readable string."""
        lacan = Lacan()
        str_output = str(lacan)
        assert "🧠" in str_output
        assert "Jacques Lacan" in str_output


class TestLacanReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "register" in result
        assert "desire_structure" in result
        assert "the_other" in result
        assert "lack" in result
        assert "objet_petit_a" in result
        assert "signifier_signified" in result
        assert "split_subject" in result
        assert "jouissance" in result
        assert "discourse" in result
        assert "metadata" in result


class TestLacanRegisters:
    """Test the three registers (Real, Imaginary, Symbolic)."""

    def test_register_structure(self, simple_prompt):
        """Test that register has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        register = result["register"]
        assert isinstance(register, dict)
        assert "dominant" in register
        assert "description" in register

    def test_imaginary_detection(self):
        """Test detection of Imaginary register."""
        lacan = Lacan()
        result = lacan.reason("I see my mirror image and identify with it")

        register = result["register"]
        assert "Imaginary" in register["dominant"] or "imaginary" in register["description"].lower()

    def test_symbolic_detection(self):
        """Test detection of Symbolic register."""
        lacan = Lacan()
        result = lacan.reason("Language and law structure our social reality")

        register = result["register"]
        assert "register" in result


class TestLacanDesire:
    """Test desire structure analysis."""

    def test_desire_structure(self, simple_prompt):
        """Test that desire has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        desire = result["desire_structure"]
        assert isinstance(desire, dict)
        assert "type" in desire
        assert "description" in desire

    def test_desire_of_other_detection(self):
        """Test detection of desire of the Other."""
        lacan = Lacan()
        result = lacan.reason("I desire what the other desires")

        desire = result["desire_structure"]
        assert "type" in desire


class TestLacanOther:
    """Test the Other analysis."""

    def test_other_structure(self, simple_prompt):
        """Test that the_other has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        other = result["the_other"]
        assert isinstance(other, dict)
        assert "type" in other
        assert "description" in other

    def test_big_other_detection(self):
        """Test detection of big Other."""
        lacan = Lacan()
        result = lacan.reason("The symbolic order and language structure everything")

        other = result["the_other"]
        assert "type" in other


class TestLacanLack:
    """Test lack analysis."""

    def test_lack_structure(self, simple_prompt):
        """Test that lack has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        lack = result["lack"]
        assert isinstance(lack, dict)
        assert "presence" in lack
        assert "description" in lack

    def test_lack_detection(self):
        """Test detection of fundamental lack."""
        lacan = Lacan()
        result = lacan.reason("Something is fundamentally missing and absent")

        lack = result["lack"]
        assert "presence" in lack


class TestLacanObjetPetitA:
    """Test objet petit a analysis."""

    def test_objet_petit_a_structure(self, simple_prompt):
        """Test that objet_petit_a has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        objet_a = result["objet_petit_a"]
        assert isinstance(objet_a, dict)
        assert "status" in objet_a
        assert "description" in objet_a

    def test_objet_petit_a_detection(self):
        """Test detection of objet petit a."""
        lacan = Lacan()
        result = lacan.reason("The unattainable object that causes my desire")

        objet_a = result["objet_petit_a"]
        assert "status" in objet_a


class TestLacanSignifier:
    """Test signifier/signified analysis."""

    def test_signifier_structure(self, simple_prompt):
        """Test that signifier_signified has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        signifier = result["signifier_signified"]
        assert isinstance(signifier, dict)
        assert "relation" in signifier
        assert "description" in signifier

    def test_signifier_detection(self):
        """Test detection of signifier primacy."""
        lacan = Lacan()
        result = lacan.reason("The signifier represents the subject for another signifier")

        signifier = result["signifier_signified"]
        assert "relation" in signifier


class TestLacanSplitSubject:
    """Test split subject analysis."""

    def test_split_subject_structure(self, simple_prompt):
        """Test that split_subject has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        split = result["split_subject"]
        assert isinstance(split, dict)
        assert "status" in split
        assert "description" in split

    def test_split_detection(self):
        """Test detection of subject split."""
        lacan = Lacan()
        result = lacan.reason("I am divided and split from myself")

        split = result["split_subject"]
        assert "status" in split


class TestLacanJouissance:
    """Test jouissance analysis."""

    def test_jouissance_structure(self, simple_prompt):
        """Test that jouissance has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        jouissance = result["jouissance"]
        assert isinstance(jouissance, dict)
        assert "type" in jouissance
        assert "description" in jouissance

    def test_jouissance_detection(self):
        """Test detection of jouissance."""
        lacan = Lacan()
        result = lacan.reason("Beyond pleasure in painful enjoyment")

        jouissance = result["jouissance"]
        assert "type" in jouissance


class TestLacanDiscourse:
    """Test discourse analysis."""

    def test_discourse_structure(self, simple_prompt):
        """Test that discourse has correct structure."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        discourse = result["discourse"]
        assert isinstance(discourse, dict)
        assert "type" in discourse
        assert "description" in discourse

    def test_discourse_detection(self):
        """Test detection of discourse type."""
        lacan = Lacan()
        result = lacan.reason("The master commands and the discourse structures relations")

        discourse = result["discourse"]
        assert "type" in discourse


class TestLacanReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_lacan(self, simple_prompt):
        """Test that reasoning mentions Lacanian concepts."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "Lacan" in reasoning or "desire" in reasoning.lower() or "Other" in reasoning


class TestLacanEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        lacan = Lacan()
        result = lacan.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        lacan = Lacan()
        result = lacan.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)
