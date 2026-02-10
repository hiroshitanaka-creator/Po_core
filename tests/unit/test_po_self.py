"""
Tests for Po_self Module

Comprehensive tests for the Po_self philosophical ensemble system.
"""

import json

import pytest

from po_core.po_self import PoSelf


class TestPoSelfBasicFunctionality:
    """Test basic Po_self functionality."""

    def test_po_self_generate_returns_structured_response(self, sample_prompt):
        """Test that generate returns a properly structured response."""
        response = PoSelf().generate(sample_prompt)

        assert response.prompt == sample_prompt
        assert response.consensus_leader == "Aristotle (Ἀριστοτέλης)"
        # Updated values for DEFAULT_PHILOSOPHERS = ["aristotle", "confucius", "wittgenstein"]
        assert response.metrics["freedom_pressure"] == 0.67
        assert response.metrics["semantic_delta"] == 0.9
        assert response.metrics["blocked_tensor"] == 0.62
        assert response.responses
        assert response.log["prompt"] == sample_prompt

    def test_po_self_respects_custom_philosophers(self, sample_prompt):
        """Test that custom philosophers list is respected."""
        response = PoSelf(philosophers=["wittgenstein"]).generate(sample_prompt)

        assert response.philosophers == ["wittgenstein"]
        assert response.consensus_leader == "Ludwig Wittgenstein"
        assert len(response.responses) == 1

    def test_po_self_default_initialization(self):
        """Test Po_self initializes with default philosophers."""
        po = PoSelf()
        # Default philosophers are used (not None)
        assert po.philosophers is not None
        assert isinstance(po.philosophers, list)
        assert len(po.philosophers) > 0
        assert po.enable_trace is True  # Trace enabled by default

    def test_po_self_with_trace_disabled(self, sample_prompt):
        """Test Po_self with tracing disabled."""
        po = PoSelf(enable_trace=False)
        response = po.generate(sample_prompt)

        assert response.prompt == sample_prompt
        assert response.log.get("session_id") is None
        assert po.po_trace is None

    def test_po_self_with_trace_enabled(self, sample_prompt):
        """Test Po_self with tracing enabled."""
        po = PoSelf(enable_trace=True)
        response = po.generate(sample_prompt)

        assert response.log.get("session_id") is not None
        assert po.po_trace is not None


class TestPoSelfPhilosopherSelection:
    """Test philosopher selection functionality."""

    def test_single_philosopher(self):
        """Test with a single philosopher."""
        po = PoSelf(philosophers=["aristotle"])
        response = po.generate("What is virtue?")

        assert len(response.philosophers) == 1
        assert response.philosophers[0] == "aristotle"
        assert len(response.responses) == 1

    def test_multiple_philosophers(self):
        """Test with multiple philosophers."""
        philosophers = ["aristotle", "confucius", "wittgenstein"]
        po = PoSelf(philosophers=philosophers)
        response = po.generate("What is truth?")

        assert set(response.philosophers) == set(philosophers)
        assert len(response.responses) == len(philosophers)

    def test_eastern_philosophers(self):
        """Test with Eastern philosophers."""
        po = PoSelf(philosophers=["confucius", "zhuangzi", "wabi_sabi"])
        response = po.generate("What is harmony?")

        assert len(response.philosophers) == 3
        assert "confucius" in response.philosophers
        assert len(response.responses) == 3

    def test_mixed_philosophical_traditions(self):
        """Test mixing Western and Eastern philosophers."""
        philosophers = ["aristotle", "confucius", "sartre", "watsuji"]
        po = PoSelf(philosophers=philosophers)
        response = po.generate("What is the good life?")

        assert len(response.philosophers) == 4
        assert len(response.responses) == 4


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

        # All metrics should be between 0 and 1
        assert 0 <= response.metrics["freedom_pressure"] <= 1
        assert 0 <= response.metrics["semantic_delta"] <= 1
        assert 0 <= response.metrics["blocked_tensor"] <= 1

    def test_metrics_consistency_across_calls(self):
        """Test that metrics are consistent for same prompt."""
        po = PoSelf(philosophers=["aristotle"])
        prompt = "What is virtue?"

        response1 = po.generate(prompt)
        response2 = po.generate(prompt)

        # Should get same metrics for deterministic mock
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

    def test_consensus_leader_is_valid(self):
        """Test that consensus leader is a valid philosopher name."""
        po = PoSelf(philosophers=["aristotle", "confucius", "sartre"])
        response = po.generate("What is freedom?")

        # Consensus leader should be one of the full philosopher names
        expected_leaders = [
            "Aristotle (Ἀριστοτέλης)",
            "Confucius (孔子)",
            "Jean-Paul Sartre",
        ]
        assert response.consensus_leader in expected_leaders

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

        # Should not raise exception
        json_str = json.dumps(response_dict, ensure_ascii=False)
        assert isinstance(json_str, str)
        assert len(json_str) > 0


class TestPoSelfEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_prompt(self):
        """Test handling of empty prompt."""
        po = PoSelf()
        response = po.generate("")

        # Should still return a valid response
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
        response = po.generate("真理とは何か？")  # Japanese: What is truth?

        assert response is not None
        assert "真理とは何か？" in response.prompt

    def test_special_characters_prompt(self):
        """Test handling of special characters."""
        po = PoSelf()
        response = po.generate('What is <truth> & "beauty"?')

        assert response is not None
        assert response.prompt == 'What is <truth> & "beauty"?'


class TestPoSelfIntegration:
    """Test integration with other modules."""

    def test_integration_with_trace(self):
        """Test that Po_self properly integrates with Po_trace."""
        po = PoSelf(enable_trace=True)
        response = po.generate("What is existence?")

        session_id = response.log["session_id"]
        session = po.po_trace.get_session(session_id)

        assert session is not None
        assert session.prompt == "What is existence?"
        assert len(session.events) > 0
        assert session.metrics == response.metrics

    def test_trace_records_all_philosophers(self):
        """Test that trace records events for all philosophers."""
        philosophers = ["aristotle", "nietzsche", "sartre"]
        po = PoSelf(philosophers=philosophers, enable_trace=True)
        response = po.generate("What is will?")

        session_id = response.log["session_id"]
        session = po.po_trace.get_session(session_id)

        # Should have events for: start + each philosopher + completion
        expected_events = 2 + len(philosophers)
        assert len(session.events) == expected_events

    def test_multiple_generations_same_instance(self):
        """Test multiple generate calls on same instance."""
        po = PoSelf(enable_trace=True)

        response1 = po.generate("What is truth?")
        response2 = po.generate("What is beauty?")

        assert response1.prompt != response2.prompt
        assert response1.log["session_id"] != response2.log["session_id"]

        # Both sessions should be recorded
        sessions = po.po_trace.list_sessions()
        assert len(sessions) >= 2


class TestPoSelfConsistency:
    """Test consistency and determinism."""

    def test_same_philosophers_same_structure(self):
        """Test that same philosophers always produce same structure."""
        philosophers = ["aristotle", "nietzsche"]
        po = PoSelf(philosophers=philosophers)

        response1 = po.generate("What is virtue?")
        response2 = po.generate("What is vice?")

        # Structure should be the same
        assert len(response1.philosophers) == len(response2.philosophers)
        assert len(response1.responses) == len(response2.responses)
        assert set(response1.metrics.keys()) == set(response2.metrics.keys())

    def test_log_contains_expected_fields(self):
        """Test that log contains all expected fields."""
        po = PoSelf(enable_trace=True)
        response = po.generate("What is consciousness?")

        assert "prompt" in response.log
        assert "philosophers" in response.log
        assert "session_id" in response.log
        assert "created_at" in response.log
        assert "events" in response.log
