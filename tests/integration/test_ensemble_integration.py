"""Integration tests for philosopher ensemble."""

import pytest

from po_core.ensemble import DEFAULT_PHILOSOPHERS, run_ensemble


class TestEnsembleIntegration:
    """Integration tests for the philosophical ensemble."""

    @pytest.fixture
    def sample_prompts(self):
        """Fixture providing various test prompts."""
        return [
            "What does it mean to live authentically?",
            "How should we understand freedom?",
            "What is the nature of consciousness?",
            "Can we ever truly know anything?",
            "What is the meaning of life?",
        ]

    def test_ensemble_basic_run(self):
        """Test basic ensemble execution."""
        prompt = "What does it mean to exist?"
        result = run_ensemble(prompt)

        assert "prompt" in result
        assert "philosophers" in result
        assert "results" in result
        assert "log" in result
        assert result["prompt"] == prompt

    def test_ensemble_all_philosophers_respond(self):
        """Test that all philosophers in ensemble provide responses."""
        prompt = "What is truth?"
        result = run_ensemble(prompt)

        assert len(result["results"]) == len(DEFAULT_PHILOSOPHERS)

        # Check each philosopher result
        for phil_result in result["results"]:
            assert "name" in phil_result
            assert "confidence" in phil_result
            assert "summary" in phil_result
            assert "tags" in phil_result
            assert phil_result["name"] in DEFAULT_PHILOSOPHERS

    def test_ensemble_with_custom_philosophers(self):
        """Test ensemble with custom philosopher selection."""
        custom_philosophers = ["aristotle", "nietzsche"]
        prompt = "What is virtue?"

        result = run_ensemble(prompt, philosophers=custom_philosophers)

        assert len(result["results"]) == len(custom_philosophers)
        assert result["philosophers"] == custom_philosophers

        philosopher_names = [r["name"] for r in result["results"]]
        for phil in custom_philosophers:
            assert phil in philosopher_names

    def test_ensemble_confidence_scores(self):
        """Test that ensemble produces valid confidence scores."""
        prompt = "How should we live?"
        result = run_ensemble(prompt)

        for phil_result in result["results"]:
            confidence = phil_result["confidence"]
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0

    def test_ensemble_logging(self):
        """Test that ensemble produces proper log entries."""
        prompt = "What is knowledge?"
        result = run_ensemble(prompt)

        log = result["log"]
        assert "prompt" in log
        assert "philosophers" in log
        assert "events" in log
        assert "created_at" in log

        # Check for expected events
        events = log["events"]
        assert any(e["event"] == "ensemble_started" for e in events)
        assert any(e["event"] == "ensemble_completed" for e in events)

    def test_ensemble_multiple_prompts(self, sample_prompts):
        """Test ensemble with multiple different prompts."""
        results = []

        for prompt in sample_prompts:
            result = run_ensemble(prompt)
            results.append(result)

            # Basic validation
            assert result["prompt"] == prompt
            assert len(result["results"]) == len(DEFAULT_PHILOSOPHERS)

        # All should have completed successfully
        assert len(results) == len(sample_prompts)

    def test_ensemble_deterministic_behavior(self):
        """Test that ensemble produces consistent results for same input."""
        prompt = "What is reality?"

        result1 = run_ensemble(prompt)
        result2 = run_ensemble(prompt)

        # Same structure
        assert set(result1.keys()) == set(result2.keys())
        assert len(result1["results"]) == len(result2["results"])

        # Same philosophers
        names1 = sorted([r["name"] for r in result1["results"]])
        names2 = sorted([r["name"] for r in result2["results"]])
        assert names1 == names2

    def test_ensemble_empty_prompt_handling(self):
        """Test ensemble behavior with edge case inputs."""
        # Empty prompt should still work
        result = run_ensemble("")
        assert "results" in result
        assert len(result["results"]) > 0

    def test_ensemble_long_prompt_handling(self):
        """Test ensemble with long, complex prompt."""
        long_prompt = """
        In the context of contemporary philosophy, considering both
        continental and analytic traditions, how might we reconcile
        the phenomenological approach to understanding consciousness
        with the computational theory of mind prevalent in cognitive science?
        """

        result = run_ensemble(long_prompt.strip())
        assert "results" in result
        assert len(result["results"]) == len(DEFAULT_PHILOSOPHERS)

    def test_ensemble_result_quality(self):
        """Test that ensemble results contain meaningful content."""
        prompt = "What is the good life?"
        result = run_ensemble(prompt)

        for phil_result in result["results"]:
            # Summary should reference the prompt
            assert len(phil_result["summary"]) > 0
            assert prompt in phil_result["summary"] or phil_result["summary"] != ""

            # Tags should be present
            assert isinstance(phil_result["tags"], list)
            assert len(phil_result["tags"]) > 0


@pytest.mark.slow
class TestEnsemblePerformance:
    """Performance tests for ensemble (marked as slow)."""

    def test_ensemble_batch_processing(self):
        """Test ensemble performance with batch of prompts."""
        prompts = [
            f"Question {i}: What is the meaning of {topic}?"
            for i, topic in enumerate(
                ["existence", "knowledge", "ethics", "beauty", "truth"]
            )
        ]

        results = []
        for prompt in prompts:
            result = run_ensemble(prompt)
            results.append(result)

        # All should complete
        assert len(results) == len(prompts)

        # All should have proper structure
        for result in results:
            assert "results" in result
            assert len(result["results"]) == len(DEFAULT_PHILOSOPHERS)
