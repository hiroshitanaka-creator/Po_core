"""
Tests for Wittgenstein Philosopher Module

Tests Wittgenstein's language philosophy focusing on:
- Language Games
- Forms of Life
- Meaning as Use
- Family Resemblance
- Private Language
- Philosophical Confusion
- Limits of Language
"""

import pytest

from po_core.philosophers.wittgenstein import Wittgenstein


class TestWittgensteinBasicFunctionality:
    """Test basic functionality of Wittgenstein philosopher."""

    def test_wittgenstein_initialization(self):
        """Test that Wittgenstein initializes correctly."""
        wittgenstein = Wittgenstein()
        assert wittgenstein.name == "Ludwig Wittgenstein"
        assert "language" in wittgenstein.description.lower()

    def test_wittgenstein_repr(self):
        """Test string representation."""
        wittgenstein = Wittgenstein()
        assert "Wittgenstein" in repr(wittgenstein)

    def test_wittgenstein_str(self):
        """Test human-readable string."""
        wittgenstein = Wittgenstein()
        assert "🧠" in str(wittgenstein)


class TestWittgensteinReasonMethod:
    """Test the reason() method."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test required fields in result."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        assert "reasoning" in result
        assert "perspective" in result
        assert "language_games" in result
        assert "forms_of_life" in result
        assert "meaning_use" in result
        assert "metadata" in result


class TestWittgensteinLanguageGames:
    """Test language games identification."""

    def test_interrogative_game_detection(self):
        """Test detection of interrogative language game."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("What is the meaning of this? How does it work?")
        games = result["language_games"]
        assert any("Interrogative" in game for game in games["games"])

    def test_descriptive_game_detection(self):
        """Test detection of descriptive language game."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("This is a table. The sky is blue.")
        games = result["language_games"]
        assert any("Descriptive" in game for game in games["games"])

    def test_language_games_has_note(self, simple_prompt):
        """Test that language games includes note."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        games = result["language_games"]
        assert "note" in games


class TestWittgensteinFormsOfLife:
    """Test forms of life assessment."""

    def test_communal_form_detection(self):
        """Test detection of communal form of life."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("We all share this community together.")
        forms = result["forms_of_life"]
        assert any("Communal" in form for form in forms["forms"])

    def test_scientific_form_detection(self):
        """Test detection of scientific form of life."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("We test our hypothesis with evidence and theory.")
        forms = result["forms_of_life"]
        assert any("Scientific" in form for form in forms["forms"])


class TestWittgensteinMeaningUse:
    """Test meaning as use evaluation."""

    def test_use_theory_detection(self):
        """Test detection of use-theory of meaning."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("The meaning depends on how we use it in practice.")
        meaning_use = result["meaning_use"]
        assert "Use-Theory" in meaning_use["adherence"]

    def test_meaning_use_has_principle(self, simple_prompt):
        """Test that meaning_use includes principle."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        meaning_use = result["meaning_use"]
        assert "principle" in meaning_use
        assert "use" in meaning_use["principle"].lower()


class TestWittgensteinPhilosophicalConfusion:
    """Test philosophical confusion detection."""

    def test_confusion_detection(self):
        """Test detection of philosophical confusion."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason("What is the essence of reality? What is the ultimate meaning?")
        confusion = result["philosophical_confusion"]
        assert "Confusion" in confusion["detection"]

    def test_confusion_has_principle(self, simple_prompt):
        """Test that confusion includes therapeutic principle."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        confusion = result["philosophical_confusion"]
        assert "principle" in confusion


class TestWittgensteinReasoningText:
    """Test reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        assert isinstance(result["reasoning"], str)
        assert len(result["reasoning"]) > 0

    def test_reasoning_mentions_wittgenstein(self, simple_prompt):
        """Test that reasoning mentions Wittgensteinian concepts."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt)
        reasoning = result["reasoning"]
        assert "Wittgenstein" in reasoning or "language game" in reasoning.lower()


class TestWittgensteinEdgeCases:
    """Test edge cases."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(empty_prompt)
        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        wittgenstein = Wittgenstein()
        result = wittgenstein.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)
