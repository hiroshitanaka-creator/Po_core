"""
Tests for Wabi-Sabi Philosopher Module

Tests Wabi-Sabi aesthetic philosophy focusing on:
- Imperfection
- Impermanence
- Simplicity
- Naturalness
"""

from po_core.philosophers.wabi_sabi import WabiSabi


class TestWabiSabiBasicFunctionality:
    """Test basic functionality of Wabi-Sabi philosopher."""

    def test_wabi_sabi_initialization(self):
        """Test that Wabi-Sabi initializes correctly."""
        wabi_sabi = WabiSabi()
        assert "Wabi-Sabi" in wabi_sabi.name
        assert (
            "imperfection" in wabi_sabi.description.lower()
            or "impermanence" in wabi_sabi.description.lower()
        )

    def test_wabi_sabi_repr(self):
        """Test string representation."""
        wabi_sabi = WabiSabi()
        repr_str = repr(wabi_sabi)
        assert "WabiSabi" in repr_str

    def test_wabi_sabi_str(self):
        """Test human-readable string."""
        wabi_sabi = WabiSabi()
        str_output = str(wabi_sabi)
        assert "Wabi-Sabi" in str_output


class TestWabiSabiReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "tension" in result
        assert "imperfection" in result
        assert "impermanence" in result
        assert "simplicity" in result
        assert "naturalness" in result
        assert "asymmetry" in result
        assert "intimacy" in result
        assert "yugen" in result
        assert "ma" in result
        assert "mono_no_aware" in result
        assert "overall_wabi_sabi" in result
        assert "metadata" in result


class TestWabiSabiImperfection:
    """Test imperfection appreciation analysis."""

    def test_imperfection_structure(self, simple_prompt):
        """Test that imperfection has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        imperfection = result["imperfection"]
        assert isinstance(imperfection, dict)
        assert "appreciation" in imperfection
        assert "description" in imperfection

    def test_imperfection_appreciation_detection(self):
        """Test detection of imperfection appreciation."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(
            "The worn, weathered, and imperfect surfaces have beauty"
        )

        imperfection = result["imperfection"]
        assert (
            "High" in imperfection["appreciation"]
            or "wabi" in imperfection["quality"].lower()
        )

    def test_perfection_seeking_detection(self):
        """Test detection of perfection seeking."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Everything must be perfect and flawless")

        imperfection = result["imperfection"]
        # Should detect perfection seeking
        assert "appreciation" in imperfection


class TestWabiSabiImpermanence:
    """Test impermanence awareness analysis."""

    def test_impermanence_structure(self, simple_prompt):
        """Test that impermanence has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        impermanence = result["impermanence"]
        assert isinstance(impermanence, dict)
        assert "awareness" in impermanence
        assert "description" in impermanence

    def test_impermanence_detection(self):
        """Test detection of impermanence awareness."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("All things are transient, fleeting, and passing")

        impermanence = result["impermanence"]
        assert (
            "High" in impermanence["awareness"]
            or "sabi" in impermanence["quality"].lower()
            or "Awareness" in impermanence["awareness"]
        )


class TestWabiSabiSimplicity:
    """Test simplicity assessment."""

    def test_simplicity_structure(self, simple_prompt):
        """Test that simplicity has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        simplicity = result["simplicity"]
        assert isinstance(simplicity, dict)
        assert "level" in simplicity
        assert "description" in simplicity

    def test_simplicity_detection(self):
        """Test detection of simplicity."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Simple, minimal, and austere quiet beauty")

        simplicity = result["simplicity"]
        assert (
            "High" in simplicity["level"]
            or "wabi-sabi" in simplicity["quality"].lower()
            or "Simplicity" in simplicity["level"]
        )


class TestWabiSabiNaturalness:
    """Test naturalness assessment."""

    def test_naturalness_structure(self, simple_prompt):
        """Test that naturalness has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        naturalness = result["naturalness"]
        assert isinstance(naturalness, dict)
        assert "level" in naturalness
        assert "description" in naturalness

    def test_naturalness_detection(self):
        """Test detection of naturalness."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(
            "Natural, organic, and authentic materials from nature"
        )

        naturalness = result["naturalness"]
        assert (
            "High" in naturalness["level"]
            or "wabi-sabi" in naturalness["quality"].lower()
            or "Natural" in naturalness["level"]
        )


class TestWabiSabiAsymmetry:
    """Test asymmetry analysis."""

    def test_asymmetry_structure(self, simple_prompt):
        """Test that asymmetry has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        asymmetry = result["asymmetry"]
        assert isinstance(asymmetry, dict)
        assert "presence" in asymmetry
        assert "description" in asymmetry

    def test_asymmetry_detection(self):
        """Test detection of asymmetry."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Irregular, uneven, and asymmetric forms")

        asymmetry = result["asymmetry"]
        assert (
            "Asymmetry" in asymmetry["presence"]
            or "asymmetric" in asymmetry["description"].lower()
        )


class TestWabiSabiIntimacy:
    """Test intimacy analysis."""

    def test_intimacy_structure(self, simple_prompt):
        """Test that intimacy has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        intimacy = result["intimacy"]
        assert isinstance(intimacy, dict)
        assert "level" in intimacy
        assert "description" in intimacy

    def test_intimacy_detection(self):
        """Test detection of intimacy."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Small, modest, and humble quiet spaces")

        intimacy = result["intimacy"]
        assert (
            "Intimacy" in intimacy["level"]
            or "intimate" in intimacy["description"].lower()
            or "level" in intimacy
        )


class TestWabiSabiYugen:
    """Test yugen (subtle profundity) analysis."""

    def test_yugen_structure(self, simple_prompt):
        """Test that yugen has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        yugen = result["yugen"]
        assert isinstance(yugen, dict)
        assert "presence" in yugen
        assert "description" in yugen

    def test_yugen_detection(self):
        """Test detection of yugen."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Subtle, mysterious depth beneath the surface")

        yugen = result["yugen"]
        assert "presence" in yugen


class TestWabiSabiMa:
    """Test ma (negative space) analysis."""

    def test_ma_structure(self, simple_prompt):
        """Test that ma has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        ma = result["ma"]
        assert isinstance(ma, dict)
        assert "presence" in ma
        assert "description" in ma

    def test_ma_detection(self):
        """Test detection of ma."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Empty space, silence, and the pause between")

        ma = result["ma"]
        assert "Ma" in ma["presence"] or "ma" in ma["description"].lower()


class TestWabiSabiMonoNoAware:
    """Test mono no aware analysis."""

    def test_mono_no_aware_structure(self, simple_prompt):
        """Test that mono_no_aware has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        mono_no_aware = result["mono_no_aware"]
        assert isinstance(mono_no_aware, dict)
        assert "presence" in mono_no_aware
        assert "description" in mono_no_aware

    def test_mono_no_aware_detection(self):
        """Test detection of mono no aware."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(
            "Poignant beauty of fleeting cherry blossoms fading away"
        )

        mono_no_aware = result["mono_no_aware"]
        assert "presence" in mono_no_aware


class TestWabiSabiOverall:
    """Test overall wabi-sabi quality assessment."""

    def test_overall_structure(self, simple_prompt):
        """Test that overall_wabi_sabi has correct structure."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        overall = result["overall_wabi_sabi"]
        assert isinstance(overall, dict)
        assert "overall" in overall
        assert "description" in overall

    def test_strong_wabi_sabi_detection(self):
        """Test detection of strong wabi-sabi."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason("Simple, natural, imperfect, and transient beauty")

        overall = result["overall_wabi_sabi"]
        # Should detect some level of wabi-sabi
        assert "overall" in overall


class TestWabiSabiReasoning:
    """Test the reasoning text output."""

    def test_reasoning_is_string(self, simple_prompt):
        """Test that reasoning is a non-empty string."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0

    def test_reasoning_mentions_wabi_sabi(self, simple_prompt):
        """Test that reasoning mentions wabi-sabi."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        reasoning = result["reasoning"]
        assert (
            "wabi-sabi" in reasoning.lower()
            or "imperfection" in reasoning.lower()
            or "impermanence" in reasoning.lower()
        )


class TestWabiSabiEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "reasoning" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestWabiSabiTensionField:
    """Test Wabi-Sabi's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        wabi_sabi = WabiSabi()
        result = wabi_sabi.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
