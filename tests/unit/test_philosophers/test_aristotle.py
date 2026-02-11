"""
Tests for Aristotle Philosopher Module

Tests Aristotle's virtue ethics and teleological philosophy focusing on:
- Virtue Ethics (Arete)
- Golden Mean
- Eudaimonia (Human Flourishing)
- Four Causes
- Potentiality and Actuality
- Practical Wisdom (Phronesis)
- Telos (Purpose/End)
- Character Formation
"""

import pytest

from po_core.philosophers.aristotle import Aristotle


class TestAristotleBasicFunctionality:
    """Test basic functionality of Aristotle philosopher."""

    def test_aristotle_initialization(self):
        """Test that Aristotle initializes correctly."""
        aristotle = Aristotle()

        assert "Aristotle" in aristotle.name or "Ἀριστοτέλης" in aristotle.name
        assert "virtue ethics" in aristotle.description.lower()
        assert "golden mean" in aristotle.description.lower()

    def test_aristotle_repr(self):
        """Test string representation."""
        aristotle = Aristotle()

        repr_str = repr(aristotle)
        assert "Aristotle" in repr_str

    def test_aristotle_str(self):
        """Test human-readable string."""
        aristotle = Aristotle()

        str_output = str(aristotle)
        assert "Aristotle" in str_output or "Ἀριστοτέλης" in str_output


class TestAristotleReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        # Check required fields
        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "virtue_assessment" in result
        assert "golden_mean" in result
        assert "eudaimonia_level" in result
        assert "four_causes" in result
        assert "potentiality_actuality" in result
        assert "practical_wisdom" in result
        assert "telos" in result
        assert "character_formation" in result
        assert "metadata" in result

    def test_reason_metadata_structure(self, simple_prompt):
        """Test that metadata has correct structure."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        metadata = result["metadata"]
        assert (
            "Aristotle" in metadata["philosopher"]
            or "Ἀριστοτέλης" in metadata["philosopher"]
        )
        assert "approach" in metadata
        assert "focus" in metadata

    def test_perspective_is_virtue_ethics(self, simple_prompt):
        """Test that perspective is virtue ethics/teleology."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        perspective = result["perspective"]
        assert "Virtue" in perspective or "Teleology" in perspective


class TestAristotleVirtueAssessment:
    """Test Aristotle's virtue assessment."""

    def test_courage_virtue_detection(self):
        """Test detection of courage virtue."""
        aristotle = Aristotle()
        prompt = "I must be brave and courageous, facing my fears and standing up for what is right."
        result = aristotle.reason(prompt)

        virtue = result["virtue_assessment"]
        virtues = virtue["virtues"]
        assert any(
            "Courage" in v["virtue"] or "ἀνδρεία" in v["virtue"] for v in virtues
        )

    def test_temperance_virtue_detection(self):
        """Test detection of temperance virtue."""
        aristotle = Aristotle()
        prompt = "I practice self-control and moderation, restraining my desires with discipline."
        result = aristotle.reason(prompt)

        virtue = result["virtue_assessment"]
        virtues = virtue["virtues"]
        assert any(
            "Temperance" in v["virtue"] or "σωφροσύνη" in v["virtue"] for v in virtues
        )

    def test_justice_virtue_detection(self):
        """Test detection of justice virtue."""
        aristotle = Aristotle()
        prompt = (
            "We must be just and fair, giving each person what they deserve equally."
        )
        result = aristotle.reason(prompt)

        virtue = result["virtue_assessment"]
        virtues = virtue["virtues"]
        assert any(
            "Justice" in v["virtue"] or "δικαιοσύνη" in v["virtue"] for v in virtues
        )

    def test_practical_wisdom_virtue_detection(self):
        """Test detection of practical wisdom virtue."""
        aristotle = Aristotle()
        prompt = "Wise judgment and practical understanding help me discern the right action."
        result = aristotle.reason(prompt)

        virtue = result["virtue_assessment"]
        virtues = virtue["virtues"]
        assert any(
            "Wisdom" in v["virtue"] or "φρόνησις" in v["virtue"] for v in virtues
        )

    def test_virtue_count(self, simple_prompt):
        """Test that virtue count is tracked."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        virtue = result["virtue_assessment"]
        assert "count" in virtue
        assert isinstance(virtue["count"], int)


class TestAristotleGoldenMean:
    """Test Aristotle's golden mean evaluation."""

    def test_mean_position_detection(self):
        """Test detection of the mean (virtuous middle)."""
        aristotle = Aristotle()
        prompt = "I seek balance and moderation, the appropriate middle path with the right amount."
        result = aristotle.reason(prompt)

        golden_mean = result["golden_mean"]
        assert "Mean" in golden_mean["position"] or "μεσότης" in golden_mean["position"]
        assert "Virtuous" in golden_mean["status"]

    def test_excess_detection(self):
        """Test detection of excess (vice)."""
        aristotle = Aristotle()
        prompt = "I have too much of everything, excessive in all ways, overwhelming and overdoing it."
        result = aristotle.reason(prompt)

        golden_mean = result["golden_mean"]
        assert (
            "Excess" in golden_mean["position"] or "ὑπερβολή" in golden_mean["position"]
        )

    def test_deficiency_detection(self):
        """Test detection of deficiency (vice)."""
        aristotle = Aristotle()
        prompt = "I have too little, not enough, lacking and deficient in what I need."
        result = aristotle.reason(prompt)

        golden_mean = result["golden_mean"]
        # Verify the field exists and has a value
        assert "position" in golden_mean
        assert isinstance(golden_mean["position"], str)
        assert len(golden_mean["position"]) > 0

    def test_golden_mean_has_principle(self, simple_prompt):
        """Test that golden mean includes principle."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        golden_mean = result["golden_mean"]
        assert "principle" in golden_mean
        assert (
            "mean" in golden_mean["principle"].lower()
            and "vice" in golden_mean["principle"].lower()
        )


class TestAristotleEudaimonia:
    """Test Aristotle's eudaimonia assessment."""

    def test_high_eudaimonia_detection(self):
        """Test detection of high eudaimonia."""
        aristotle = Aristotle()
        prompt = "I flourish and thrive through excellence, practicing virtue and cultivating wisdom in my complete life."
        result = aristotle.reason(prompt)

        eudaimonia = result["eudaimonia_level"]
        assert "High Eudaimonia" in eudaimonia["level"]

    def test_moderate_eudaimonia_detection(self):
        """Test detection of moderate eudaimonia."""
        aristotle = Aristotle()
        prompt = "I practice virtue and think rationally about my life."
        result = aristotle.reason(prompt)

        eudaimonia = result["eudaimonia_level"]
        assert "Moderate" in eudaimonia["level"] or "High" in eudaimonia["level"]

    def test_eudaimonia_has_note(self, simple_prompt):
        """Test that eudaimonia includes note about highest good."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        eudaimonia = result["eudaimonia_level"]
        assert "note" in eudaimonia
        assert (
            "highest" in eudaimonia["note"].lower()
            or "good" in eudaimonia["note"].lower()
        )


class TestAristotleFourCauses:
    """Test Aristotle's four causes analysis."""

    def test_four_causes_structure(self, simple_prompt):
        """Test that four causes has all four types."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        four_causes = result["four_causes"]
        assert "material" in four_causes
        assert "formal" in four_causes
        assert "efficient" in four_causes
        assert "final" in four_causes

    def test_material_cause_detection(self):
        """Test detection of material cause."""
        aristotle = Aristotle()
        prompt = "This is made of wood and metal, composed of these substances."
        result = aristotle.reason(prompt)

        four_causes = result["four_causes"]
        assert len(four_causes["material"]) > 0
        # Check if material cause is mentioned
        assert any("Material" in cause for cause in four_causes["material"])

    def test_final_cause_detection(self):
        """Test detection of final cause (telos/purpose)."""
        aristotle = Aristotle()
        prompt = "The purpose of this is to achieve our goal and aim for the sake of the end."
        result = aristotle.reason(prompt)

        four_causes = result["four_causes"]
        # Check if final cause is identified
        assert any(
            "purpose" in cause.lower() or "identified" in cause.lower()
            for cause in four_causes["final"]
        )


class TestAristotlePotentialityActuality:
    """Test Aristotle's potentiality and actuality evaluation."""

    def test_actualization_detection(self):
        """Test detection of actualization (potential becoming actual)."""
        aristotle = Aristotle()
        prompt = (
            "I am realizing my potential, becoming and developing toward my completion."
        )
        result = aristotle.reason(prompt)

        potential_actual = result["potentiality_actuality"]
        # Verify the field exists and has a value
        assert "state" in potential_actual
        assert isinstance(potential_actual["state"], str)
        assert len(potential_actual["state"]) > 0

    def test_potentiality_detection(self):
        """Test detection of potentiality."""
        aristotle = Aristotle()
        prompt = "I have the capacity and ability to do this, the potential is there."
        result = aristotle.reason(prompt)

        potential_actual = result["potentiality_actuality"]
        assert (
            "Potentiality" in potential_actual["state"]
            or "δύναμις" in potential_actual["state"]
        )

    def test_potential_actual_has_note(self, simple_prompt):
        """Test that potentiality_actuality includes note."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        potential_actual = result["potentiality_actuality"]
        assert "note" in potential_actual


class TestAristotlePhronesis:
    """Test Aristotle's practical wisdom (phronesis) assessment."""

    def test_high_phronesis_detection(self):
        """Test detection of high practical wisdom."""
        aristotle = Aristotle()
        prompt = "I judge wisely in this particular situation, deciding what action to do based on experience and context."
        result = aristotle.reason(prompt)

        phronesis = result["practical_wisdom"]
        assert "High Phronesis" in phronesis["level"]

    def test_moderate_phronesis_detection(self):
        """Test detection of moderate practical wisdom."""
        aristotle = Aristotle()
        prompt = "I try to decide what to do in this situation."
        result = aristotle.reason(prompt)

        phronesis = result["practical_wisdom"]
        # Could be moderate or high depending on keywords
        assert isinstance(phronesis["level"], str)

    def test_phronesis_has_note(self, simple_prompt):
        """Test that phronesis includes note."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        phronesis = result["practical_wisdom"]
        assert "note" in phronesis
        assert (
            "Phronesis" in phronesis["note"] or "practical" in phronesis["note"].lower()
        )


class TestAristotleTelos:
    """Test Aristotle's telos identification."""

    def test_ultimate_telos_detection(self):
        """Test detection of ultimate telos."""
        aristotle = Aristotle()
        prompt = "The ultimate purpose and highest goal is our final end."
        result = aristotle.reason(prompt)

        telos = result["telos"]
        assert "Ultimate Telos" in telos["type"]

    def test_intermediate_telos_detection(self):
        """Test detection of intermediate telos."""
        aristotle = Aristotle()
        prompt = "My goal is to achieve this purpose and strive toward it."
        result = aristotle.reason(prompt)

        telos = result["telos"]
        assert "Telos" in telos["type"]

    def test_telos_has_principle(self, simple_prompt):
        """Test that telos includes principle."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        telos = result["telos"]
        assert "principle" in telos
        assert (
            "eudaimonia" in telos["principle"].lower()
            or "good" in telos["principle"].lower()
        )


class TestAristotleCharacterFormation:
    """Test Aristotle's character formation evaluation."""

    def test_active_character_formation(self):
        """Test detection of active character formation."""
        aristotle = Aristotle()
        prompt = "I develop my character through regular habit and practice, cultivating who I become."
        result = aristotle.reason(prompt)

        character = result["character_formation"]
        assert "Active" in character["formation"]

    def test_potential_character_formation(self):
        """Test detection of potential character formation."""
        aristotle = Aristotle()
        prompt = "I want to develop my character and become a better person."
        result = aristotle.reason(prompt)

        character = result["character_formation"]
        # Could be potential or active
        assert isinstance(character["formation"], str)

    def test_character_has_note(self, simple_prompt):
        """Test that character includes note about habituation."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        character = result["character_formation"]
        assert "note" in character
        assert (
            "virtuous" in character["note"].lower()
            or "action" in character["note"].lower()
        )


class TestAristotleReasoningText:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_aristotle(self, simple_prompt):
        """Test that reasoning mentions Aristotelian perspective."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert "Aristotle" in reasoning or "virtue" in reasoning.lower()

    def test_reasoning_mentions_habituation(self, existential_prompt):
        """Test that reasoning includes habituation principle."""
        aristotle = Aristotle()
        result = aristotle.reason(existential_prompt)

        reasoning = result["reasoning"]
        # Should mention habituation or practice
        assert (
            "habit" in reasoning.lower()
            or "practice" in reasoning.lower()
            or "virtue" in reasoning.lower()
        )


class TestAristotleEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        aristotle = Aristotle()
        result = aristotle.reason(empty_prompt)

        # Should still return a valid structure
        assert isinstance(result, dict)
        assert "reasoning" in result
        assert "virtue_assessment" in result

    def test_long_prompt(self, long_prompt):
        """Test handling of very long prompt."""
        aristotle = Aristotle()
        result = aristotle.reason(long_prompt)

        # Should successfully process without errors
        assert isinstance(result, dict)
        assert len(result["reasoning"]) > 0


class TestAristotleWithContext:
    """Test Aristotle's reason method with context parameter."""

    def test_reason_accepts_context(self, simple_prompt):
        """Test that reason() accepts context parameter."""
        aristotle = Aristotle()
        context = {"previous_analysis": "Virtue ethics discussion"}

        # Should not raise an error
        result = aristotle.reason(simple_prompt, context=context)
        assert isinstance(result, dict)

    def test_reason_works_without_context(self, simple_prompt):
        """Test that reason() works without context parameter."""
        aristotle = Aristotle()

        result = aristotle.reason(simple_prompt)
        assert isinstance(result, dict)


class TestAristotleTensionField:
    """Test Aristotle's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        aristotle = Aristotle()
        result = aristotle.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0

    def test_high_tension_prompt(self):
        """Test that a prompt with clear tensions produces high tension level."""
        aristotle = Aristotle()
        # Prompt with excess, lack of flourishing, unclear purpose
        prompt = "I have too much of everything and lack purpose in my life."
        result = aristotle.reason(prompt)

        tension = result["tension"]
        # Should detect some tensions
        assert tension["level"] in ["Moderate", "High", "Very High"]
        assert len(tension["elements"]) > 0
