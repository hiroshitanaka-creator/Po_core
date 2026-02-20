"""
Smoke Tests for run_turn Pipeline (migrated from test_smoke_ensemble.py)
========================================================================

Migrated smoke tests that lock the minimal expected behavior of the
run_turn pipeline and public APIs (po_core.run, PoSelf.generate).

Original tests tested run_ensemble (removed in v0.3).
These test the same behavioral contracts via the new API.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.pipeline


@pytest.fixture
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


# ══════════════════════════════════════════════════════════════════════════
# 1. po_core.run() smoke tests
# ══════════════════════════════════════════════════════════════════════════


class TestRunAPISmoke:
    """Smoke tests for po_core.run() — the recommended entry point."""

    def test_run_returns_required_keys(self, sample_prompt: str) -> None:
        """run() must return dict with required keys."""
        from po_core import run

        result = run(user_input=sample_prompt)
        required_keys = {"status", "request_id"}
        assert required_keys <= set(
            result.keys()
        ), f"Missing keys: {required_keys - set(result.keys())}"

    def test_run_status_ok_for_normal_input(self, sample_prompt: str) -> None:
        from po_core import run

        result = run(user_input=sample_prompt)
        assert result["status"] == "ok"

    def test_run_has_proposal(self, sample_prompt: str) -> None:
        from po_core import run

        result = run(user_input=sample_prompt)
        assert "proposal" in result
        assert len(result["proposal"]) > 0

    def test_run_request_id_is_string(self, sample_prompt: str) -> None:
        from po_core import run

        result = run(user_input=sample_prompt)
        assert isinstance(result["request_id"], str)
        assert len(result["request_id"]) > 0

    def test_run_handles_empty_prompt(self) -> None:
        from po_core import run

        result = run(user_input="")
        assert "status" in result
        assert result["status"] in ("ok", "blocked")

    def test_run_is_deterministic(self, sample_prompt: str) -> None:
        """Same input should produce same status and structure."""
        from po_core import run

        r1 = run(user_input=sample_prompt)
        r2 = run(user_input=sample_prompt)
        assert r1["status"] == r2["status"]
        assert set(r1.keys()) == set(r2.keys())


# ══════════════════════════════════════════════════════════════════════════
# 2. PoSelf.generate() smoke tests (rich response)
# ══════════════════════════════════════════════════════════════════════════


class TestPoSelfSmoke:
    """Smoke tests for PoSelf.generate() — the rich response API."""

    def test_generate_returns_required_fields(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert hasattr(response, "prompt")
        assert hasattr(response, "text")
        assert hasattr(response, "philosophers")
        assert hasattr(response, "metrics")
        assert hasattr(response, "responses")
        assert hasattr(response, "log")
        assert hasattr(response, "metadata")

    def test_generate_preserves_prompt(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert response.prompt == sample_prompt

    def test_generate_has_philosophers(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert isinstance(response.philosophers, list)
        assert len(response.philosophers) > 0

    def test_generate_has_responses(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert isinstance(response.responses, list)
        assert len(response.responses) > 0
        for r in response.responses:
            assert "name" in r
            assert len(r["name"]) > 0

    def test_generate_metrics_are_floats(self, sample_prompt: str) -> None:
        """Metrics must be floats in [0, 1]."""
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        metrics = response.metrics

        assert "freedom_pressure" in metrics
        for key, val in metrics.items():
            assert isinstance(val, float), f"{key} must be float"
            assert 0.0 <= val <= 1.0, f"{key}={val} out of [0, 1]"

    def test_generate_has_consensus_leader(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        if response.consensus_leader is not None:
            assert isinstance(response.consensus_leader, str)

    def test_generate_log_has_pipeline(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert response.log.get("pipeline") == "run_turn"

    def test_generate_log_has_events(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        events = response.log.get("events", [])
        assert len(events) >= 5, "Pipeline should emit at least 5 events"

    def test_generate_status_ok(self, sample_prompt: str) -> None:
        from po_core.po_self import PoSelf

        response = PoSelf().generate(sample_prompt)
        assert response.metadata["status"] == "ok"

    def test_generate_is_deterministic(self, sample_prompt: str) -> None:
        """Same input should produce same structure and status."""
        from po_core.po_self import PoSelf

        po = PoSelf()
        r1 = po.generate(sample_prompt)
        r2 = po.generate(sample_prompt)
        assert r1.metadata["status"] == r2.metadata["status"]
        assert set(r1.metrics.keys()) == set(r2.metrics.keys())


# ══════════════════════════════════════════════════════════════════════════
# 3. Philosopher Registry smoke tests (still valid via legacy REGISTRY)
# ══════════════════════════════════════════════════════════════════════════


class TestPhilosopherRegistrySmoke:
    """Smoke tests for philosopher registry integrity."""

    def test_all_39_philosophers_in_legacy_registry(self) -> None:
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        assert len(PHILOSOPHER_REGISTRY) == 39

    def test_all_philosophers_have_reason_method(self) -> None:
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        for name, cls in PHILOSOPHER_REGISTRY.items():
            instance = cls()
            assert hasattr(instance, "reason"), f"{name} missing reason()"
            assert callable(instance.reason)

    def test_all_philosophers_return_dict(self) -> None:
        from po_core.ensemble import PHILOSOPHER_REGISTRY

        for name, cls in PHILOSOPHER_REGISTRY.items():
            instance = cls()
            result = instance.reason("What is truth?")
            assert isinstance(result, dict), f"{name}.reason() must return dict"
            assert len(result) > 0

    def test_manifest_has_40_specs(self) -> None:
        """Manifest SPECS includes 39 philosophers + dummy + 4 AI slots (disabled) = 44."""
        from po_core.philosophers.manifest import SPECS

        assert len(SPECS) == 44

    def test_manifest_all_enabled(self) -> None:
        from po_core.philosophers.manifest import SPECS

        enabled = [s for s in SPECS if s.enabled]
        assert len(enabled) == 40


# ══════════════════════════════════════════════════════════════════════════
# 4. Integration: pipeline with multiple prompts
# ══════════════════════════════════════════════════════════════════════════


class TestPipelineIntegrationSmoke:
    """Integration tests verifying pipeline handles various inputs."""

    PROMPTS = [
        "What does it mean to exist?",
        "How should we understand freedom?",
        "What is the nature of consciousness?",
        "Can we ever truly know anything?",
        "What is the meaning of life?",
    ]

    def test_multiple_prompts_all_succeed(self) -> None:
        from po_core import run

        for prompt in self.PROMPTS:
            result = run(user_input=prompt)
            assert result["status"] == "ok", f"Failed for: {prompt}"
            assert "proposal" in result

    def test_long_prompt_handled(self) -> None:
        from po_core import run

        long_prompt = (
            "In the context of contemporary philosophy, considering both "
            "continental and analytic traditions, how might we reconcile "
            "the phenomenological approach to understanding consciousness "
            "with the computational theory of mind prevalent in cognitive science?"
        )
        result = run(user_input=long_prompt)
        assert result["status"] == "ok"

    def test_unicode_prompt_handled(self) -> None:
        from po_core import run

        result = run(user_input="真理とは何か？")
        assert result["status"] in ("ok", "blocked")

    def test_special_characters_handled(self) -> None:
        from po_core import run

        result = run(user_input='What is <truth> & "beauty"?')
        assert result["status"] == "ok"
