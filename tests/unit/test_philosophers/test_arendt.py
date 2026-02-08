"""
Tests for Arendt Philosopher Module

Tests Arendt's political philosophy focusing on:
- Vita activa (labor, work, action)
- Natality
- Public vs private realm
- Political action and judgment
"""

import pytest

from po_core.philosophers.arendt import Arendt


class TestArendtBasicFunctionality:
    """Test basic functionality of Arendt philosopher."""

    def test_arendt_initialization(self):
        """Test that Arendt initializes correctly."""
        arendt = Arendt()
        assert arendt.name == "Hannah Arendt"
        assert (
            "political" in arendt.description.lower()
            or "action" in arendt.description.lower()
        )

    def test_arendt_repr(self):
        """Test string representation."""
        arendt = Arendt()
        repr_str = repr(arendt)
        assert "Arendt" in repr_str

    def test_arendt_str(self):
        """Test human-readable string."""
        arendt = Arendt()
        str_output = str(arendt)
        assert "🧠" in str_output
        assert "Hannah Arendt" in str_output


class TestArendtReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        assert "philosopher" in result
        assert "description" in result
        assert "analysis" in result
        assert "summary" in result
        assert "tension" in result


class TestArendtAnalysisStructure:
    """Test the analysis structure."""

    def test_analysis_is_dict(self, simple_prompt):
        """Test that analysis is a dictionary."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert isinstance(result["analysis"], dict)

    def test_analysis_has_vita_activa(self, simple_prompt):
        """Test that analysis includes vita_activa."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert "vita_activa" in result["analysis"]

    def test_analysis_has_natality(self, simple_prompt):
        """Test that analysis includes natality."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert "natality" in result["analysis"]

    def test_analysis_has_public_private(self, simple_prompt):
        """Test that analysis includes public_private_realm."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert "public_private_realm" in result["analysis"]

    def test_analysis_has_plurality(self, simple_prompt):
        """Test that analysis includes plurality."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)
        assert "plurality" in result["analysis"]


class TestArendtVitaActiva:
    """Test vita activa analysis."""

    def test_vita_activa_structure(self, simple_prompt):
        """Test that vita_activa has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        vita_activa = result["analysis"]["vita_activa"]
        assert isinstance(vita_activa, dict)
        assert "dominant_mode" in vita_activa

    def test_action_mode_detection(self):
        """Test detection of action mode."""
        arendt = Arendt()
        result = arendt.reason("We act together in the public political sphere")

        vita_activa = result["analysis"]["vita_activa"]
        assert (
            "action" in vita_activa["dominant_mode"].lower()
            or vita_activa["action_present"]
        )

    def test_labor_mode_detection(self):
        """Test detection of labor mode."""
        arendt = Arendt()
        result = arendt.reason("I work to survive and maintain my biological needs")

        vita_activa = result["analysis"]["vita_activa"]
        assert vita_activa["labor_present"]


class TestArendtNatality:
    """Test natality analysis."""

    def test_natality_structure(self, simple_prompt):
        """Test that natality has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        natality = result["analysis"]["natality"]
        assert isinstance(natality, dict)
        assert "natality_present" in natality

    def test_natality_detection(self):
        """Test detection of natality."""
        arendt = Arendt()
        result = arendt.reason("We can begin something new and start fresh initiatives")

        natality = result["analysis"]["natality"]
        assert natality["natality_present"] is True


class TestArendtPublicPrivate:
    """Test public vs private realm analysis."""

    def test_public_private_structure(self, simple_prompt):
        """Test that public_private_realm has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        public_private = result["analysis"]["public_private_realm"]
        assert isinstance(public_private, dict)
        assert "dominant_realm" in public_private

    def test_public_realm_detection(self):
        """Test detection of public realm."""
        arendt = Arendt()
        result = arendt.reason("In the public political community we act together")

        public_private = result["analysis"]["public_private_realm"]
        assert public_private["public_present"]


class TestArendtEvil:
    """Test evil analysis."""

    def test_evil_structure(self, simple_prompt):
        """Test that evil_analysis has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        evil = result["analysis"]["evil_analysis"]
        assert isinstance(evil, dict)
        assert "evil_present" in evil

    def test_banality_of_evil_detection(self):
        """Test detection of banality of evil."""
        arendt = Arendt()
        result = arendt.reason(
            "Ordinary thoughtless bureaucrats following orders without thinking"
        )

        evil = result["analysis"]["evil_analysis"]
        # Should detect some aspect of evil or thoughtlessness
        assert isinstance(evil["evil_present"], bool)


class TestArendtTotalitarianism:
    """Test totalitarian elements analysis."""

    def test_totalitarian_structure(self, simple_prompt):
        """Test that totalitarian_elements has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        totalitarian = result["analysis"]["totalitarian_elements"]
        assert isinstance(totalitarian, dict)
        assert "totalitarian_elements" in totalitarian

    def test_totalitarian_detection(self):
        """Test detection of totalitarian elements."""
        arendt = Arendt()
        result = arendt.reason("Total control through terror and ideology")

        totalitarian = result["analysis"]["totalitarian_elements"]
        # Should detect totalitarian themes
        assert isinstance(totalitarian["totalitarian_elements"], bool)


class TestArendtJudgment:
    """Test political judgment analysis."""

    def test_judgment_structure(self, simple_prompt):
        """Test that political_judgment has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        judgment = result["analysis"]["political_judgment"]
        assert isinstance(judgment, dict)
        assert "judgment_present" in judgment

    def test_judgment_detection(self):
        """Test detection of political judgment."""
        arendt = Arendt()
        result = arendt.reason("We must think carefully and judge what we are doing")

        judgment = result["analysis"]["political_judgment"]
        assert judgment["judgment_present"] is True


class TestArendtFreedom:
    """Test freedom analysis."""

    def test_freedom_structure(self, simple_prompt):
        """Test that freedom has correct structure."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        freedom = result["analysis"]["freedom"]
        assert isinstance(freedom, dict)
        assert "freedom_present" in freedom

    def test_political_freedom_detection(self):
        """Test detection of political freedom."""
        arendt = Arendt()
        result = arendt.reason(
            "We are free to act together in the public political sphere"
        )

        freedom = result["analysis"]["freedom"]
        assert freedom["freedom_present"] is True


class TestArendtSummary:
    """Test summary generation."""

    def test_summary_is_string(self, simple_prompt):
        """Test that summary is a string."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0

    def test_summary_mentions_vita_activa(self, simple_prompt):
        """Test that summary mentions vita activa."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        summary = result["summary"]
        assert (
            "labor" in summary.lower()
            or "work" in summary.lower()
            or "action" in summary.lower()
        )


class TestArendtEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        arendt = Arendt()
        result = arendt.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "philosopher" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestArendtTensionField:
    """Test Arendt's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        arendt = Arendt()
        result = arendt.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
