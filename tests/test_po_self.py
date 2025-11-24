"""Unit tests for Po_self ensemble and design signals."""

from po_core.philosophers.base import Philosopher
from po_core.po_self import (
    EnsembleResult,
    compute_design_signals,
    compute_freedom_pressure_tensor,
    compute_meaning_profile,
    run_ensemble,
)


class MockPhilosopher(Philosopher):
    """Lightweight mock philosopher for ensemble tests."""

    def __init__(self, name: str, reasoning: str):
        super().__init__(name=name, description="mock")
        self._reasoning = reasoning

    def reason(self, prompt: str, context=None):  # type: ignore[override]
        return {
            "reasoning": f"{self._reasoning}-{prompt}",
            "perspective": "test",
            "tension": ["mock tension"],
            "metadata": {"mock": True},
        }


def test_meaning_profile_contains_expected_keys() -> None:
    profile = compute_meaning_profile("Acting together with curiosity and responsibility")

    assert set(profile.keys()) == {"poetic_granularity", "action_intent", "relational_density"}
    assert all(0.0 <= value <= 1.0 for value in profile.values())


def test_freedom_pressure_tensor_is_bounded() -> None:
    freedom_pressure = compute_freedom_pressure_tensor("What should I do?", observation_pressure=0.25)

    assert 0.0 <= freedom_pressure <= 1.0


def test_run_ensemble_with_mock_philosophers() -> None:
    philosophers = [
        MockPhilosopher("Mock A", "reasoning-A"),
        MockPhilosopher("Mock B", "reasoning-B"),
    ]

    result = run_ensemble(
        "prompt",
        observation_pressure=0.4,
        weights={"Mock A": 2.0, "Mock B": 1.0},
        philosophers=philosophers,
    )

    assert isinstance(result, EnsembleResult)
    assert len(result.philosopher_signals) == 2
    assert result.weights["Mock A"] > result.weights["Mock B"]
    assert "Mock A" in result.response
    assert result.design_signals.responsibility_pressure <= 1.0

