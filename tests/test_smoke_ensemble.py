"""
Smoke Tests for Ensemble
========================

These tests lock the minimal expected behavior of the ensemble system.
They ensure that refactoring doesn't break the core contract.

Purpose:
- Lock output structure and types
- Verify exception conditions
- Ensure deterministic behavior with same inputs
"""
import pytest
from typing import Any, Dict, List


@pytest.fixture
def sample_prompt() -> str:
    """Simple prompt for testing."""
    return "What does it mean to live authentically?"


class TestEnsembleSmoke:
    """Smoke tests to lock ensemble behavior before refactoring."""

    def test_ensemble_returns_required_keys(self, sample_prompt: str) -> None:
        """Ensemble must always return these keys."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        required_keys = {"prompt", "philosophers", "responses", "aggregate", "consensus", "log"}
        assert required_keys <= set(result.keys()), f"Missing keys: {required_keys - set(result.keys())}"

    def test_ensemble_responses_have_required_fields(self, sample_prompt: str) -> None:
        """Each philosopher response must have these fields."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        required_fields = {"name", "reasoning", "perspective", "freedom_pressure", "semantic_delta", "blocked_tensor"}
        for response in result["responses"]:
            assert required_fields <= set(response.keys()), f"Missing fields in response: {required_fields - set(response.keys())}"

    def test_ensemble_aggregate_metrics_are_floats(self, sample_prompt: str) -> None:
        """Aggregate metrics must be floats in valid ranges."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)
        aggregate = result["aggregate"]

        for key in ["freedom_pressure", "semantic_delta", "blocked_tensor"]:
            assert key in aggregate, f"Missing aggregate key: {key}"
            assert isinstance(aggregate[key], float), f"{key} must be float"
            assert 0.0 <= aggregate[key] <= 1.0, f"{key} must be in [0, 1]"

    def test_ensemble_consensus_has_leader(self, sample_prompt: str) -> None:
        """Consensus must have a leader (or None for empty)."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)
        consensus = result["consensus"]

        assert "leader" in consensus
        assert "text" in consensus
        # Leader should be a string (philosopher name) or None
        assert consensus["leader"] is None or isinstance(consensus["leader"], str)

    def test_ensemble_rejects_unknown_philosopher(self) -> None:
        """Ensemble must reject unknown philosopher names."""
        from po_core.ensemble import run_ensemble

        with pytest.raises(ValueError, match="Unknown philosopher"):
            run_ensemble("test", philosophers=["nonexistent_philosopher"])

    def test_ensemble_accepts_single_philosopher(self, sample_prompt: str) -> None:
        """Ensemble must work with a single philosopher."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt, philosophers=["aristotle"])

        assert len(result["responses"]) == 1
        assert result["consensus"]["leader"] is not None

    def test_ensemble_default_philosophers_are_three(self, sample_prompt: str) -> None:
        """Default ensemble uses 3 philosophers."""
        from po_core.ensemble import run_ensemble, DEFAULT_PHILOSOPHERS

        result = run_ensemble(sample_prompt)

        assert len(result["philosophers"]) == len(DEFAULT_PHILOSOPHERS)
        assert len(result["responses"]) == len(DEFAULT_PHILOSOPHERS)

    def test_ensemble_is_deterministic(self, sample_prompt: str) -> None:
        """Same input should produce same metrics (deterministic reasoning)."""
        from po_core.ensemble import run_ensemble

        result1 = run_ensemble(sample_prompt, enable_tracer=False)
        result2 = run_ensemble(sample_prompt, enable_tracer=False)

        # Metrics should be identical
        assert result1["aggregate"] == result2["aggregate"]
        # Philosophers should be in same order
        assert [r["name"] for r in result1["responses"]] == [r["name"] for r in result2["responses"]]

    def test_ensemble_handles_empty_prompt(self) -> None:
        """Ensemble must handle empty prompt without crashing."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble("")

        assert "responses" in result
        assert "aggregate" in result

    def test_ensemble_log_has_events(self, sample_prompt: str) -> None:
        """Log must contain start and completion events."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)
        log = result["log"]

        assert "events" in log
        events = log["events"]
        event_names = [e.get("event") for e in events]
        assert "ensemble_started" in event_names
        assert "ensemble_completed" in event_names


class TestEnsembleMetricsContract:
    """Tests to verify metrics computation contract."""

    def test_freedom_pressure_range(self, sample_prompt: str) -> None:
        """Freedom pressure must be in [0.35, 1.0] based on computation."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        for response in result["responses"]:
            fp = response["freedom_pressure"]
            assert 0.35 <= fp <= 1.0, f"Freedom pressure {fp} out of expected range [0.35, 1.0]"

    def test_semantic_delta_range(self, sample_prompt: str) -> None:
        """Semantic delta must be in [0.0, 1.0]."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        for response in result["responses"]:
            sd = response["semantic_delta"]
            assert 0.0 <= sd <= 1.0, f"Semantic delta {sd} out of range [0, 1]"

    def test_blocked_tensor_range(self, sample_prompt: str) -> None:
        """Blocked tensor must be in [0.0, 1.0]."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        for response in result["responses"]:
            bt = response["blocked_tensor"]
            assert 0.0 <= bt <= 1.0, f"Blocked tensor {bt} out of range [0, 1]"

    def test_consensus_leader_has_highest_freedom_pressure(self, sample_prompt: str) -> None:
        """Consensus leader should have highest freedom pressure."""
        from po_core.ensemble import run_ensemble

        result = run_ensemble(sample_prompt)

        if result["responses"]:
            max_fp = max(r["freedom_pressure"] for r in result["responses"])
            leader_name = result["consensus"]["leader"]
            leader_fp = next(r["freedom_pressure"] for r in result["responses"] if r["name"] == leader_name)
            assert leader_fp == max_fp


class TestPhilosopherRegistry:
    """Tests to verify philosopher registry integrity."""

    def test_all_39_philosophers_in_registry(self) -> None:
        """Registry must contain all 39 philosophers."""
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        assert len(PHILOSOPHER_REGISTRY) == 39, f"Expected 39 philosophers, got {len(PHILOSOPHER_REGISTRY)}"

    def test_all_philosophers_can_be_loaded(self) -> None:
        """All registered philosophers must be loadable."""
        from po_core.ensemble import PHILOSOPHER_REGISTRY, _load_philosophers

        philosophers = _load_philosophers(PHILOSOPHER_REGISTRY.keys())
        assert len(philosophers) == 39

    def test_all_philosophers_have_reason_method(self) -> None:
        """All philosophers must have a reason method."""
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        for name, philosopher_class in PHILOSOPHER_REGISTRY.items():
            instance = philosopher_class()
            assert hasattr(instance, "reason"), f"{name} missing reason method"
            assert callable(instance.reason), f"{name}.reason is not callable"

    def test_all_philosophers_return_dict(self) -> None:
        """All philosophers must return a dict from reason().

        NOTE: The actual keys returned are inconsistent across philosophers.
        This is a known issue that Step 1 of the refactoring (base.py hardening)
        will address by enforcing a contract.
        """
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        test_prompt = "What is truth?"

        for name, philosopher_class in PHILOSOPHER_REGISTRY.items():
            instance = philosopher_class()
            result = instance.reason(test_prompt)
            assert isinstance(result, dict), f"{name}.reason() must return dict"
            # Note: Keys are currently inconsistent - some use 'reasoning'/'perspective',
            # others use 'analysis'/'description'. This is documented for later fix.
            assert len(result) > 0, f"{name}.reason() must return non-empty dict"
