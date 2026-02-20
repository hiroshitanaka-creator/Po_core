"""
Tests for Po_self Module — aligned with run_turn pipeline.

PoSelf.generate() delegates to run_turn, which uses SafetyMode-based selection.
The `philosophers` parameter is informational only; all 39 philosophers
participate in NORMAL mode.
"""

import json

from po_core.po_self import PoSelf


class TestPoSelfBasicFunctionality:
    """Test basic Po_self functionality."""

    def test_po_self_generate_returns_structured_response(self, sample_prompt):
        """Test that generate returns a properly structured response."""
        response = PoSelf().generate(sample_prompt)

        assert response.prompt == sample_prompt
        assert response.text
        assert response.consensus_leader
        assert response.responses
        assert "freedom_pressure" in response.metrics
        assert "semantic_delta" in response.metrics
        assert "blocked_tensor" in response.metrics

    def test_po_self_philosophers_is_informational(self, sample_prompt):
        """PoSelf(philosophers=[...]) is informational; run_turn uses all 39."""
        response = PoSelf(philosophers=["wittgenstein"]).generate(sample_prompt)

        # run_turn selects philosophers via SafetyMode, not PoSelf constructor
        assert response.text
        assert response.consensus_leader

    def test_po_self_default_initialization(self):
        """Test Po_self initializes with default philosophers."""
        po = PoSelf()
        assert po.philosophers is not None
        assert isinstance(po.philosophers, list)
        assert len(po.philosophers) > 0
        assert po.enable_trace is True

    def test_po_self_with_trace_disabled(self, sample_prompt):
        """Test Po_self with tracing disabled."""
        po = PoSelf(enable_trace=False)
        response = po.generate(sample_prompt)

        assert response.prompt == sample_prompt
        assert po.po_trace is None

    def test_po_self_with_trace_enabled(self, sample_prompt):
        """Test Po_self with tracing enabled."""
        po = PoSelf(enable_trace=True)
        response = po.generate(sample_prompt)

        assert "pipeline" in response.log
        assert response.log["pipeline"] == "run_turn"
        assert "events" in response.log


class TestPoSelfMetrics:
    """Test metrics calculation."""

    def test_metrics_structure(self):
        """Test that metrics have correct structure."""
        po = PoSelf()
        response = po.generate("What is justice?")

        assert "freedom_pressure" in response.metrics
        assert "semantic_delta" in response.metrics
        assert "blocked_tensor" in response.metrics

    def test_metrics_values_range(self):
        """Test that metrics are within expected ranges."""
        po = PoSelf()
        response = po.generate("What is beauty?")

        assert 0 <= response.metrics["freedom_pressure"] <= 1
        assert 0 <= response.metrics["semantic_delta"] <= 1
        assert 0 <= response.metrics["blocked_tensor"] <= 1

    def test_metrics_consistency_across_calls(self):
        """Test that metrics are consistent for same prompt."""
        po = PoSelf()
        prompt = "What is virtue?"

        response1 = po.generate(prompt)
        response2 = po.generate(prompt)

        assert response1.metrics == response2.metrics


class TestPoSelfResponse:
    """Test response structure and content."""

    def test_response_has_all_fields(self):
        """Test that response has all required fields."""
        po = PoSelf()
        response = po.generate("What is wisdom?")

        assert hasattr(response, "prompt")
        assert hasattr(response, "text")
        assert hasattr(response, "consensus_leader")
        assert hasattr(response, "philosophers")
        assert hasattr(response, "metrics")
        assert hasattr(response, "responses")
        assert hasattr(response, "log")

    def test_response_text_not_empty(self):
        """Test that response text is not empty."""
        po = PoSelf()
        response = po.generate("What is courage?")

        assert response.text is not None
        assert len(response.text) > 0

    def test_consensus_leader_is_string(self):
        """Test that consensus leader is a non-empty string."""
        po = PoSelf()
        response = po.generate("What is freedom?")

        assert isinstance(response.consensus_leader, str)
        assert len(response.consensus_leader) > 0

    def test_to_dict_conversion(self):
        """Test converting response to dictionary."""
        po = PoSelf()
        response = po.generate("What is knowledge?")

        response_dict = response.to_dict()

        assert isinstance(response_dict, dict)
        assert response_dict["prompt"] == response.prompt
        assert response_dict["text"] == response.text
        assert response_dict["consensus_leader"] == response.consensus_leader
        assert response_dict["metrics"] == response.metrics

    def test_to_dict_json_serializable(self):
        """Test that to_dict result is JSON serializable."""
        po = PoSelf()
        response = po.generate("What is meaning?")

        response_dict = response.to_dict()

        json_str = json.dumps(response_dict, ensure_ascii=False)
        assert isinstance(json_str, str)
        assert len(json_str) > 0


class TestPoSelfEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self):
        """Test handling of empty prompt."""
        po = PoSelf()
        response = po.generate("")

        assert response is not None
        assert response.prompt == ""

    def test_very_long_prompt(self):
        """Test handling of very long prompt."""
        po = PoSelf()
        long_prompt = "What is truth? " * 100
        response = po.generate(long_prompt)

        assert response is not None
        assert response.prompt == long_prompt

    def test_unicode_prompt(self):
        """Test handling of unicode characters in prompt."""
        po = PoSelf()
        response = po.generate("真理とは何か？")

        assert response is not None
        assert "真理とは何か？" in response.prompt

    def test_special_characters_prompt(self):
        """Test handling of special characters."""
        po = PoSelf()
        response = po.generate('What is <truth> & "beauty"?')

        assert response is not None
        assert response.prompt == 'What is <truth> & "beauty"?'


class TestPoSelfIntegration:
    """Test integration with run_turn pipeline."""

    def test_log_has_pipeline_info(self):
        """Test that log contains run_turn pipeline info."""
        po = PoSelf(enable_trace=True)
        response = po.generate("What is existence?")

        assert "pipeline" in response.log
        assert response.log["pipeline"] == "run_turn"
        assert "request_id" in response.log
        assert "events" in response.log
        assert "status" in response.log

    def test_multiple_generations_same_instance(self):
        """Test multiple generate calls on same instance."""
        po = PoSelf()

        response1 = po.generate("What is truth?")
        response2 = po.generate("What is beauty?")

        assert response1.prompt != response2.prompt
        assert response1.log["request_id"] != response2.log["request_id"]


class TestPoSelfConsistency:
    """Test consistency and determinism."""

    def test_same_structure_across_calls(self):
        """Test that same call always produces same structure."""
        po = PoSelf()

        response1 = po.generate("What is virtue?")
        response2 = po.generate("What is vice?")

        assert set(response1.metrics.keys()) == set(response2.metrics.keys())

    def test_log_contains_expected_fields(self):
        """Test that log contains expected fields."""
        po = PoSelf(enable_trace=True)
        response = po.generate("What is consciousness?")

        assert "pipeline" in response.log
        assert "events" in response.log
        assert "request_id" in response.log
        assert "status" in response.log
