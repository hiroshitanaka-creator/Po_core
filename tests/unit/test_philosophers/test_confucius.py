"""
Tests for Confucius Philosopher Module

Tests Confucian philosophy focusing on:
- Ren (Benevolence)
- Li (Ritual Propriety)
- Yi (Righteousness)
- Xiao (Filial Piety)
- Junzi (Exemplary Person)
- Zhong and Shu (Loyalty and Reciprocity)
- De (Virtue)
- Tianming (Mandate of Heaven)
- Learning and Self-Cultivation
"""

from po_core.philosophers.confucius import Confucius


class TestConfuciusBasicFunctionality:
    """Test basic functionality of Confucius philosopher."""

    def test_confucius_initialization(self):
        """Test that Confucius initializes correctly."""
        confucius = Confucius()
        assert "Confucius" in confucius.name or "孔子" in confucius.name
        assert (
            "ren" in confucius.description.lower()
            or "benevolence" in confucius.description.lower()
        )

    def test_confucius_repr(self):
        """Test string representation."""
        confucius = Confucius()
        assert "Confucius" in repr(confucius)

    def test_confucius_str(self):
        """Test human-readable string."""
        Confucius()


class TestConfuciusReasonMethod:
    """Test the reason() method."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test required fields in result."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)
        assert "philosopher" in result
        assert "analysis" in result
        assert "summary" in result
        assert "tension" in result

        analysis = result["analysis"]
        assert "ren_benevolence" in analysis
        assert "li_ritual_propriety" in analysis
        assert "yi_righteousness" in analysis
        assert "xiao_filial_piety" in analysis
        assert "junzi_exemplary_person" in analysis


class TestConfuciusRen:
    """Test Confucius's ren (benevolence) assessment."""

    def test_ren_detection(self):
        """Test detection of ren (benevolence)."""
        confucius = Confucius()
        result = confucius.reason(
            "I show compassion and kindness to all, caring for others with love and benevolence."
        )
        ren = result["analysis"]["ren_benevolence"]
        assert ren["ren_present"] is True

    def test_ren_has_interpretation(self, simple_prompt):
        """Test that ren includes interpretation."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)
        ren = result["analysis"]["ren_benevolence"]
        assert "interpretation" in ren


class TestConfuciusLi:
    """Test Confucius's li (ritual propriety) assessment."""

    def test_li_detection(self):
        """Test detection of li (ritual propriety)."""
        confucius = Confucius()
        result = confucius.reason(
            "I follow proper ritual and etiquette, showing respect and courtesy with decorum."
        )
        li = result["analysis"]["li_ritual_propriety"]
        assert li["li_present"] is True

    def test_li_has_interpretation(self, simple_prompt):
        """Test that li includes interpretation."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)
        li = result["analysis"]["li_ritual_propriety"]
        assert "interpretation" in li


class TestConfuciusYi:
    """Test Confucius's yi (righteousness) assessment."""

    def test_yi_detection(self):
        """Test detection of yi (righteousness)."""
        confucius = Confucius()
        result = confucius.reason(
            "I uphold justice and moral principles with righteous integrity."
        )
        yi = result["analysis"]["yi_righteousness"]
        assert yi["yi_present"] is True


class TestConfuciusXiao:
    """Test Confucius's xiao (filial piety) assessment."""

    def test_xiao_detection(self):
        """Test detection of xiao (filial piety)."""
        confucius = Confucius()
        result = confucius.reason(
            "I honor my parents and ancestors, showing filial respect to my family elders."
        )
        xiao = result["analysis"]["xiao_filial_piety"]
        assert xiao["xiao_present"] is True


class TestConfuciusJunzi:
    """Test Confucius's junzi (exemplary person) assessment."""

    def test_junzi_detection(self):
        """Test detection of junzi ideal."""
        confucius = Confucius()
        result = confucius.reason(
            "I cultivate my character with virtue and moral excellence, becoming an exemplary gentleman."
        )
        junzi = result["analysis"]["junzi_exemplary_person"]
        assert junzi["junzi_present"] is True


class TestConfuciusZhongShu:
    """Test Confucius's zhong and shu assessment."""

    def test_zhong_loyalty_detection(self):
        """Test detection of zhong (loyalty)."""
        confucius = Confucius()
        result = confucius.reason("I am loyal and faithful, dedicated with commitment.")
        zhong_shu = result["analysis"]["zhong_shu_loyalty_reciprocity"]
        assert zhong_shu["zhong_loyalty_present"] is True

    def test_shu_reciprocity_detection(self):
        """Test detection of shu (reciprocity)."""
        confucius = Confucius()
        result = confucius.reason(
            "I treat others with empathy and reciprocity, showing mutual respect and consideration."
        )
        zhong_shu = result["analysis"]["zhong_shu_loyalty_reciprocity"]
        assert zhong_shu["shu_reciprocity_present"] is True


class TestConfuciusReasoningText:
    """Test reasoning text output."""

    def test_summary_is_string(self, simple_prompt):
        """Test that summary is a non-empty string."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0


class TestConfuciusEdgeCases:
    """Test edge cases."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        confucius = Confucius()
        result = confucius.reason(empty_prompt)
        assert isinstance(result, dict)
        assert "analysis" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestConfuciusTensionField:
    """Test Confucius's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        confucius = Confucius()
        result = confucius.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
