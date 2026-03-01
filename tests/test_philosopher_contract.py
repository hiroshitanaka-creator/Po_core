"""
Philosopher Output Contract Tests
===================================

Enforces the standard output contract for ALL philosophers' reason() method.
If a new philosopher is added that doesn't conform, these tests will catch it.

Standard contract (from base.py):
    Required keys: reasoning (str), perspective (str)
    Optional keys: tension (dict), metadata (dict)
    Additional philosopher-specific keys are allowed.

DummyPhilosopher is excluded — it uses PhilosopherProtocol directly
and doesn't implement reason().
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from po_core.philosophers.base import Context
from po_core.philosophers.manifest import SPECS, PhilosopherSpec

# All specs except dummy (which uses PhilosopherProtocol, not reason())
REASON_SPECS = [s for s in SPECS if s.philosopher_id != "dummy"]

TEST_PROMPTS = [
    "What is truth?",
    "The benevolent leader acted with proper ritual respect, making righteous moral choices for the community's shared freedom.",
]


def _load_philosopher(spec: PhilosopherSpec) -> Any:
    """Load a philosopher instance from its spec."""
    mod = importlib.import_module(spec.module)
    cls = getattr(mod, spec.symbol)
    return cls()


# ── Contract compliance for all reason()-based philosophers ──────────


@pytest.mark.parametrize(
    "spec", REASON_SPECS, ids=[s.philosopher_id for s in REASON_SPECS]
)
class TestPhilosopherContract:
    """Every philosopher's reason() must return the standard contract keys."""

    def test_returns_reasoning_key(self, spec: PhilosopherSpec) -> None:
        """reason() must return a 'reasoning' key with a non-empty string."""
        phil = _load_philosopher(spec)
        result = phil.reason(TEST_PROMPTS[0])
        assert "reasoning" in result, f"{spec.philosopher_id}: missing 'reasoning' key"
        assert isinstance(
            result["reasoning"], str
        ), f"{spec.philosopher_id}: 'reasoning' must be str"
        assert (
            len(result["reasoning"]) > 0
        ), f"{spec.philosopher_id}: 'reasoning' must be non-empty"

    def test_returns_perspective_key(self, spec: PhilosopherSpec) -> None:
        """reason() must return a 'perspective' key with a non-empty string."""
        phil = _load_philosopher(spec)
        result = phil.reason(TEST_PROMPTS[0])
        assert (
            "perspective" in result
        ), f"{spec.philosopher_id}: missing 'perspective' key"
        assert isinstance(
            result["perspective"], str
        ), f"{spec.philosopher_id}: 'perspective' must be str"
        assert (
            len(result["perspective"]) > 0
        ), f"{spec.philosopher_id}: 'perspective' must be non-empty"

    def test_returns_metadata_key(self, spec: PhilosopherSpec) -> None:
        """reason() must return a 'metadata' key with a dict containing 'philosopher'."""
        phil = _load_philosopher(spec)
        result = phil.reason(TEST_PROMPTS[0])
        assert "metadata" in result, f"{spec.philosopher_id}: missing 'metadata' key"
        assert isinstance(
            result["metadata"], dict
        ), f"{spec.philosopher_id}: 'metadata' must be dict"
        assert (
            "philosopher" in result["metadata"]
        ), f"{spec.philosopher_id}: metadata must contain 'philosopher'"

    def test_tension_format_if_present(self, spec: PhilosopherSpec) -> None:
        """If 'tension' is a dict, it must have level/description/elements."""
        phil = _load_philosopher(spec)
        result = phil.reason(TEST_PROMPTS[0])
        if "tension" not in result:
            pytest.skip(f"{spec.philosopher_id}: no tension key (optional)")
        tension = result["tension"]
        # Tension can be dict (rich format) or numeric (legacy format)
        if isinstance(tension, dict):
            assert "level" in tension, f"{spec.philosopher_id}: tension missing 'level'"
            assert (
                "description" in tension
            ), f"{spec.philosopher_id}: tension missing 'description'"
            assert (
                "elements" in tension
            ), f"{spec.philosopher_id}: tension missing 'elements'"
            assert isinstance(
                tension["elements"], list
            ), f"{spec.philosopher_id}: tension['elements'] must be list"
        else:
            # Legacy format: numeric tension value
            assert isinstance(
                tension, (int, float)
            ), f"{spec.philosopher_id}: tension must be dict or numeric, got {type(tension)}"

    def test_reason_contract_unchanged_after_card_generation(
        self, spec: PhilosopherSpec
    ) -> None:
        """Calling propose_card() must not alter legacy reason() contract."""
        phil = _load_philosopher(spec)
        if not hasattr(phil, "propose_card"):
            pytest.skip(f"{spec.philosopher_id}: no propose_card")

        _ = phil.propose_card(Context.from_prompt(TEST_PROMPTS[0]))
        result = phil.reason(TEST_PROMPTS[0])

        assert (
            "reasoning" in result
        ), f"{spec.philosopher_id}: missing 'reasoning' after propose_card"
        assert (
            "perspective" in result
        ), f"{spec.philosopher_id}: missing 'perspective' after propose_card"

    def test_reason_is_deterministic(self, spec: PhilosopherSpec) -> None:
        """reason() with same prompt should return consistent results."""
        phil = _load_philosopher(spec)
        r1 = phil.reason(TEST_PROMPTS[0])
        r2 = phil.reason(TEST_PROMPTS[0])
        assert r1 == r2, f"{spec.philosopher_id}: non-deterministic output"


# ── Aggregate compliance check ───────────────────────────────────────


class TestAggregateCompliance:
    """Aggregate tests to verify overall system compliance."""

    def test_all_philosophers_have_reason_method(self) -> None:
        """All non-dummy philosophers must have a reason() method."""
        for spec in REASON_SPECS:
            phil = _load_philosopher(spec)
            assert hasattr(
                phil, "reason"
            ), f"{spec.philosopher_id}: missing reason() method"
            assert callable(
                phil.reason
            ), f"{spec.philosopher_id}: reason is not callable"

    def test_no_philosopher_returns_only_old_keys(self) -> None:
        """No philosopher should return ONLY old-format keys without standard ones."""
        for spec in REASON_SPECS:
            phil = _load_philosopher(spec)
            result = phil.reason("What is truth?")
            # Must have standard keys, not just old format
            assert (
                "reasoning" in result
            ), f"{spec.philosopher_id}: still using old format (no 'reasoning' key)"
            assert (
                "perspective" in result
            ), f"{spec.philosopher_id}: still using old format (no 'perspective' key)"

    def test_philosopher_count_matches_manifest(self) -> None:
        """Ensure we're testing the right number of philosophers."""
        assert len(REASON_SPECS) == len(SPECS) - 1  # all except dummy
        assert len(SPECS) >= 39  # at least 39 philosophers + dummy


__all__ = ["TestPhilosopherContract", "TestAggregateCompliance"]
