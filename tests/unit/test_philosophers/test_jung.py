"""
Tests for Jung Philosopher Module

Tests Jung's analytical psychology focusing on:
- Archetypes
- Collective unconscious
- Individuation
- Shadow integration
"""

import pytest

from po_core.philosophers.jung import Jung


class TestJungBasicFunctionality:
    """Test basic functionality of Jung philosopher."""

    def test_jung_initialization(self):
        """Test that Jung initializes correctly."""
        jung = Jung()
        assert jung.name == "Carl Gustav Jung"
        assert "Analytical" in jung.description
        assert "archetypes" in jung.description

    def test_jung_repr(self):
        """Test string representation."""
        jung = Jung()
        repr_str = repr(jung)
        assert "Jung" in repr_str
        assert "Carl Gustav Jung" in repr_str

    def test_jung_str(self):
        """Test human-readable string."""
        jung = Jung()
        str_output = str(jung)
        assert "🧠" in str_output
        assert "Carl Gustav Jung" in str_output


class TestJungReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        jung = Jung()
        result = jung.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "archetypes_detected" in result
        assert "collective_unconscious_themes" in result
        assert "individuation_stage" in result
        assert "psychological_type" in result
        assert "shadow_integration" in result
        assert "synchronicity_indicators" in result
        assert "self_realization" in result
        assert "metadata" in result


class TestJungArchetypes:
    """Test archetype detection."""

    def test_archetypes_detected(self, simple_prompt):
        """Test that archetypes are detected."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        archetypes = result["archetypes_detected"]
        assert isinstance(archetypes, list)
        assert len(archetypes) > 0
        assert "archetype" in archetypes[0]
        assert "description" in archetypes[0]

    def test_shadow_archetype_detection(self):
        """Test detection of Shadow archetype."""
        jung = Jung()
        result = jung.reason("I hide my dark secrets from everyone")

        archetypes = result["archetypes_detected"]
        assert any(a["archetype"] == "Shadow" for a in archetypes)

    def test_hero_archetype_detection(self):
        """Test detection of Hero archetype."""
        jung = Jung()
        result = jung.reason("I must overcome this challenge on my journey")

        archetypes = result["archetypes_detected"]
        assert any(a["archetype"] == "Hero" for a in archetypes)

    def test_mother_archetype_detection(self):
        """Test detection of Mother archetype."""
        jung = Jung()
        result = jung.reason("The nurturing mother gives birth to new life")

        archetypes = result["archetypes_detected"]
        assert any(a["archetype"] == "Mother" for a in archetypes)


class TestJungCollectiveUnconscious:
    """Test collective unconscious theme identification."""

    def test_collective_themes_detected(self, simple_prompt):
        """Test that collective themes are detected."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        themes = result["collective_unconscious_themes"]
        assert isinstance(themes, list)
        assert len(themes) > 0

    def test_death_rebirth_theme(self):
        """Test detection of death and rebirth theme."""
        jung = Jung()
        result = jung.reason("Through death comes rebirth and transformation")

        themes = result["collective_unconscious_themes"]
        assert any("death and rebirth" in t.lower() for t in themes)

    def test_journey_theme(self):
        """Test detection of journey theme."""
        jung = Jung()
        result = jung.reason("I seek the path to discover my true self")

        themes = result["collective_unconscious_themes"]
        assert any("journey" in t.lower() for t in themes)


class TestJungIndividuation:
    """Test individuation stage assessment."""

    def test_individuation_structure(self, simple_prompt):
        """Test that individuation has correct structure."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        individuation = result["individuation_stage"]
        assert isinstance(individuation, dict)
        assert "stage" in individuation
        assert "description" in individuation
        assert "level" in individuation

    def test_persona_stage_detection(self):
        """Test detection of persona identification stage."""
        jung = Jung()
        result = jung.reason("I should do what is expected of me in my role")

        individuation = result["individuation_stage"]
        assert "Persona" in individuation["stage"]

    def test_shadow_stage_detection(self):
        """Test detection of shadow integration stage."""
        jung = Jung()
        result = jung.reason("I must confront and acknowledge my hidden darkness")

        individuation = result["individuation_stage"]
        assert "Shadow" in individuation["stage"]


class TestJungPsychologicalType:
    """Test psychological type determination."""

    def test_psychological_type_structure(self, simple_prompt):
        """Test that psychological type has correct structure."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        psych_type = result["psychological_type"]
        assert isinstance(psych_type, dict)
        assert "attitude" in psych_type
        assert "dominant_function" in psych_type

    def test_introversion_detection(self):
        """Test detection of introverted attitude."""
        jung = Jung()
        result = jung.reason("I prefer to reflect alone in my inner world")

        psych_type = result["psychological_type"]
        assert "Introverted" in psych_type["attitude"]

    def test_thinking_function_detection(self):
        """Test detection of thinking function."""
        jung = Jung()
        result = jung.reason("I analyze this logically with reason")

        psych_type = result["psychological_type"]
        assert psych_type["dominant_function"] in ["Thinking", "Sensation", "Feeling", "Intuition"]


class TestJungShadowIntegration:
    """Test shadow integration assessment."""

    def test_shadow_integration_structure(self, simple_prompt):
        """Test that shadow integration has correct structure."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        shadow = result["shadow_integration"]
        assert isinstance(shadow, dict)
        assert "status" in shadow
        assert "level" in shadow

    def test_shadow_denial_detection(self):
        """Test detection of shadow denial."""
        jung = Jung()
        result = jung.reason("That is not me, I would never do that")

        shadow = result["shadow_integration"]
        assert "Denying" in shadow["status"] or "Unconscious" in shadow["status"]

    def test_shadow_integration_detection(self):
        """Test detection of shadow integration."""
        jung = Jung()
        result = jung.reason("I acknowledge and accept my dark flaws")

        shadow = result["shadow_integration"]
        assert "Integrating" in shadow["status"]


class TestJungSynchronicity:
    """Test synchronicity detection."""

    def test_synchronicity_structure(self, simple_prompt):
        """Test that synchronicity has correct structure."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        synchronicity = result["synchronicity_indicators"]
        assert isinstance(synchronicity, dict)
        assert "present" in synchronicity
        assert "description" in synchronicity

    def test_synchronicity_detection(self):
        """Test detection of synchronicity."""
        jung = Jung()
        result = jung.reason("A meaningful coincidence connected these events")

        synchronicity = result["synchronicity_indicators"]
        assert synchronicity["present"] is True


class TestJungReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_archetypes(self, simple_prompt):
        """Test that reasoning mentions archetypes."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "archetype" in reasoning.lower()


class TestJungEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        jung = Jung()
        result = jung.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result
        assert "archetypes_detected" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        jung = Jung()
        result = jung.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestJungTensionField:
    """Test Jung's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        jung = Jung()
        result = jung.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
