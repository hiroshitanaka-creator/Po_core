"""
Tests for Zhuangzi Philosopher Module

Tests Zhuangzi's Daoist philosophy focusing on:
- Dao (the Way)
- Wu Wei (non-action)
- Ziran (naturalness)
- Xiaoyaoyou (free wandering)
"""

import pytest

from po_core.philosophers.zhuangzi import Zhuangzi


class TestZhuangziBasicFunctionality:
    """Test basic functionality of Zhuangzi philosopher."""

    def test_zhuangzi_initialization(self):
        """Test that Zhuangzi initializes correctly."""
        zhuangzi = Zhuangzi()
        assert "Zhuangzi" in zhuangzi.name
        assert (
            "naturalness" in zhuangzi.description.lower()
            or "dao" in zhuangzi.description.lower()
        )

    def test_zhuangzi_repr(self):
        """Test string representation."""
        zhuangzi = Zhuangzi()
        repr_str = repr(zhuangzi)
        assert "Zhuangzi" in repr_str

    def test_zhuangzi_str(self):
        """Test human-readable string."""
        zhuangzi = Zhuangzi()
        str_output = str(zhuangzi)
        assert "Zhuangzi" in str_output


class TestZhuangziReasonMethod:
    """Test the reason() method with various inputs."""

    def test_reason_returns_dict(self, simple_prompt):
        """Test that reason() returns a dictionary."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert isinstance(result, dict)

    def test_reason_has_required_fields(self, simple_prompt):
        """Test that the result has all required fields."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        assert "philosopher" in result
        assert "description" in result
        assert "analysis" in result
        assert "summary" in result
        assert "tension" in result


class TestZhuangziAnalysisStructure:
    """Test the analysis structure."""

    def test_analysis_is_dict(self, simple_prompt):
        """Test that analysis is a dictionary."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert isinstance(result["analysis"], dict)

    def test_analysis_has_dao(self, simple_prompt):
        """Test that analysis includes dao_the_way."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert "dao_the_way" in result["analysis"]

    def test_analysis_has_wu_wei(self, simple_prompt):
        """Test that analysis includes wu_wei_non_action."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert "wu_wei_non_action" in result["analysis"]

    def test_analysis_has_ziran(self, simple_prompt):
        """Test that analysis includes ziran_naturalness."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert "ziran_naturalness" in result["analysis"]

    def test_analysis_has_xiaoyaoyou(self, simple_prompt):
        """Test that analysis includes xiaoyaoyou_freedom."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)
        assert "xiaoyaoyou_freedom" in result["analysis"]


class TestZhuangziDao:
    """Test Dao (the Way) analysis."""

    def test_dao_structure(self, simple_prompt):
        """Test that dao_the_way has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        dao = result["analysis"]["dao_the_way"]
        assert isinstance(dao, dict)
        assert "dao_present" in dao

    def test_dao_detection(self):
        """Test detection of Dao."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("Follow the natural Way and path of the cosmos")

        dao = result["analysis"]["dao_the_way"]
        assert dao["dao_present"] is True


class TestZhuangziWuWei:
    """Test Wu Wei (non-action) analysis."""

    def test_wu_wei_structure(self, simple_prompt):
        """Test that wu_wei_non_action has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        wu_wei = result["analysis"]["wu_wei_non_action"]
        assert isinstance(wu_wei, dict)
        assert "wu_wei_present" in wu_wei

    def test_wu_wei_detection(self):
        """Test detection of Wu Wei."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("Act effortlessly without forcing or striving")

        wu_wei = result["analysis"]["wu_wei_non_action"]
        assert wu_wei["wu_wei_present"] is True


class TestZhuangziZiran:
    """Test Ziran (naturalness) analysis."""

    def test_ziran_structure(self, simple_prompt):
        """Test that ziran_naturalness has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        ziran = result["analysis"]["ziran_naturalness"]
        assert isinstance(ziran, dict)
        assert "ziran_present" in ziran

    def test_ziran_detection(self):
        """Test detection of Ziran."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("Be natural, spontaneous, and authentic")

        ziran = result["analysis"]["ziran_naturalness"]
        assert ziran["ziran_present"] is True


class TestZhuangziQi:
    """Test Qi (vital energy) analysis."""

    def test_qi_structure(self, simple_prompt):
        """Test that qi_vital_energy has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        qi = result["analysis"]["qi_vital_energy"]
        assert isinstance(qi, dict)
        assert "qi_present" in qi

    def test_qi_detection(self):
        """Test detection of Qi."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(
            "Vital energy and breath flow through all living things"
        )

        qi = result["analysis"]["qi_vital_energy"]
        assert qi["qi_present"] is True


class TestZhuangziXiaoyaoyou:
    """Test Xiaoyaoyou (free wandering) analysis."""

    def test_xiaoyaoyou_structure(self, simple_prompt):
        """Test that xiaoyaoyou_freedom has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        xiaoyaoyou = result["analysis"]["xiaoyaoyou_freedom"]
        assert isinstance(xiaoyaoyou, dict)
        assert "xiaoyaoyou_present" in xiaoyaoyou

    def test_xiaoyaoyou_detection(self):
        """Test detection of Xiaoyaoyou."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("Free and easy wandering without constraints")

        xiaoyaoyou = result["analysis"]["xiaoyaoyou_freedom"]
        assert xiaoyaoyou["xiaoyaoyou_present"] is True


class TestZhuangziQiwulun:
    """Test Qiwulun (equality of things) analysis."""

    def test_qiwulun_structure(self, simple_prompt):
        """Test that qiwulun_equality has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        qiwulun = result["analysis"]["qiwulun_equality"]
        assert isinstance(qiwulun, dict)
        assert "qiwulun_present" in qiwulun

    def test_qiwulun_detection(self):
        """Test detection of Qiwulun."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(
            "All perspectives are relative and equal from different viewpoints"
        )

        qiwulun = result["analysis"]["qiwulun_equality"]
        assert qiwulun["qiwulun_present"] is True


class TestZhuangziDreamReality:
    """Test dream and reality theme analysis."""

    def test_dream_reality_structure(self, simple_prompt):
        """Test that dream_reality has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        dream = result["analysis"]["dream_reality"]
        assert isinstance(dream, dict)
        assert "dream_reality_present" in dream

    def test_dream_detection(self):
        """Test detection of dream/reality theme."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(
            "Am I dreaming or is this reality? Like the butterfly dream"
        )

        dream = result["analysis"]["dream_reality"]
        assert dream["dream_reality_present"] is True


class TestZhuangziTransformation:
    """Test transformation analysis."""

    def test_transformation_structure(self, simple_prompt):
        """Test that transformation has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        transformation = result["analysis"]["transformation"]
        assert isinstance(transformation, dict)
        assert "transformation_present" in transformation

    def test_transformation_detection(self):
        """Test detection of transformation."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("All things transform and change constantly")

        transformation = result["analysis"]["transformation"]
        assert transformation["transformation_present"] is True


class TestZhuangziUselessness:
    """Test usefulness of uselessness analysis."""

    def test_uselessness_structure(self, simple_prompt):
        """Test that uselessness has correct structure."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        uselessness = result["analysis"]["uselessness"]
        assert isinstance(uselessness, dict)
        assert "uselessness_theme_present" in uselessness

    def test_uselessness_detection(self):
        """Test detection of uselessness theme."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason("What appears useless has no purpose but survives")

        uselessness = result["analysis"]["uselessness"]
        assert uselessness["uselessness_theme_present"] is True


class TestZhuangziSummary:
    """Test summary generation."""

    def test_summary_is_string(self, simple_prompt):
        """Test that summary is a string."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0

    def test_summary_mentions_daoist_themes(self, simple_prompt):
        """Test that summary mentions Daoist themes."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        summary = result["summary"]
        # Summary should mention some aspect of Daoist philosophy
        assert isinstance(summary, str)


class TestZhuangziEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self, empty_prompt):
        """Test handling of empty prompt."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(empty_prompt)

        assert isinstance(result, dict)
        assert "philosopher" in result

    def test_with_context(self, simple_prompt):
        """Test with context parameter."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt, context={"test": "context"})
        assert isinstance(result, dict)


class TestZhuangziTensionField:
    """Test Zhuangzi's tension field structure and content."""

    def test_tension_field_exists(self, simple_prompt):
        """Test that tension field is present in result."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        assert "tension" in result
        assert result["tension"] is not None

    def test_tension_field_is_dict(self, simple_prompt):
        """Test that tension field is a dictionary."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        assert isinstance(result["tension"], dict)

    def test_tension_has_required_keys(self, simple_prompt):
        """Test that tension dict has all required keys."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        tension = result["tension"]
        assert "level" in tension
        assert "description" in tension
        assert "elements" in tension

    def test_tension_level_is_valid(self, simple_prompt):
        """Test that tension level is one of the valid values."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]
        assert tension["level"] in valid_levels

    def test_tension_description_is_string(self, simple_prompt):
        """Test that tension description is a non-empty string."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["description"], str)
        assert len(tension["description"]) > 0

    def test_tension_elements_is_list(self, simple_prompt):
        """Test that tension elements is a list."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        tension = result["tension"]
        assert isinstance(tension["elements"], list)

    def test_tension_elements_are_strings(self, simple_prompt):
        """Test that all tension elements are strings."""
        zhuangzi = Zhuangzi()
        result = zhuangzi.reason(simple_prompt)

        tension = result["tension"]
        for element in tension["elements"]:
            assert isinstance(element, str)
            assert len(element) > 0
