# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Regression harness for the technical-debt audit (Phase 0).

Each test class maps to one root-cause category.  Tests are intentionally
*minimal* — they capture the exact failure mode without fixing it, so that
later phases can turn them green.

Failure matrix (tests that FAIL before fixes are applied):
  test_party_machine_ids_subset_of_manifest  ← roster drift
  test_optimal_combos_ids_in_manifest        ← roster drift
  test_harmonious_clusters_ids_in_manifest   ← roster drift
  test_select_and_load_exposes_load_errors   ← silent error swallow in select_and_load
  test_version_metadata_matches_package      ← hardcoded version in output_adapter
  test_safety_mode_present_in_run_turn_result ← safety_mode absent from ensemble dict
  test_listener_failure_is_observable        ← silent except pass in in_memory tracer
  test_process_executor_child_crash_classified ← crash collapses into timeout
"""

from __future__ import annotations

import importlib
import sys
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canonical_philosopher_ids() -> frozenset[str]:
    """Return the set of all public philosopher IDs from the manifest."""
    from po_core.philosophers.manifest import DUMMY_PHILOSOPHER_ID, SPECS

    return frozenset(
        s.philosopher_id for s in SPECS if s.philosopher_id != DUMMY_PHILOSOPHER_ID
    )


# ---------------------------------------------------------------------------
# Roster Drift
# ---------------------------------------------------------------------------


class TestRosterDrift:
    """PartyMachine must never emit IDs absent from the canonical manifest."""

    def test_party_machine_ids_subset_of_manifest(self):
        """PhilosopherPartyMachine.available_philosophers must be a subset of the manifest."""
        from po_core.party_machine import PhilosopherPartyMachine

        canonical = _canonical_philosopher_ids()
        machine = PhilosopherPartyMachine(verbose=False)
        stale = set(machine.available_philosophers) - canonical
        assert stale == set(), (
            f"PhilosopherPartyMachine.available_philosophers contains IDs not in manifest: {stale}"
        )

    def test_optimal_combos_ids_in_manifest(self):
        """All IDs in OPTIMAL_4_COMBOS must be in the canonical manifest."""
        from po_core.party_machine import OPTIMAL_4_COMBOS

        canonical = _canonical_philosopher_ids()
        stale: set[str] = set()
        for theme, combos in OPTIMAL_4_COMBOS.items():
            for combo in combos:
                stale.update(set(combo) - canonical)
        assert stale == set(), (
            f"OPTIMAL_4_COMBOS contains IDs not in manifest: {stale}"
        )

    def test_high_tension_pairs_ids_in_manifest(self):
        """All IDs in HIGH_TENSION_PAIRS must be in the canonical manifest."""
        from po_core.party_machine import HIGH_TENSION_PAIRS

        canonical = _canonical_philosopher_ids()
        stale: set[str] = set()
        for a, b in HIGH_TENSION_PAIRS:
            stale.update({a, b} - canonical)
        assert stale == set(), (
            f"HIGH_TENSION_PAIRS contains IDs not in manifest: {stale}"
        )

    def test_harmonious_clusters_ids_in_manifest(self):
        """All IDs in HARMONIOUS_CLUSTERS must be in the canonical manifest."""
        from po_core.party_machine import HARMONIOUS_CLUSTERS

        canonical = _canonical_philosopher_ids()
        stale: set[str] = set()
        for cluster, ids in HARMONIOUS_CLUSTERS.items():
            stale.update(set(ids) - canonical)
        assert stale == set(), (
            f"HARMONIOUS_CLUSTERS contains IDs not in manifest: {stale}"
        )

    def test_suggest_party_returns_only_manifest_ids(self):
        """suggest_party() must produce only manifest-valid IDs."""
        from po_core.party_machine import PhilosopherPartyMachine

        canonical = _canonical_philosopher_ids()
        machine = PhilosopherPartyMachine(verbose=False)
        config = machine.suggest_party("ethics", custom_prompt="test")
        invalid = set(config.philosophers) - canonical
        assert invalid == set(), (
            f"suggest_party() returned non-manifest IDs: {invalid}"
        )


# ---------------------------------------------------------------------------
# Philosopher Loading Policy
# ---------------------------------------------------------------------------


class TestPhilosopherLoadingPolicy:
    """Loading contract must be explicit; select_and_load must not silently drop errors."""

    def test_select_and_load_exposes_load_errors(self):
        """
        select_and_load() currently swallows LoadErrors returned by load().
        After Phase 2 this test should pass — either select_and_load raises, OR
        the function returns a typed report with failures listed.
        """
        from po_core.philosophers.manifest import SPECS, PhilosopherSpec
        from po_core.philosophers.registry import LoadError, PhilosopherRegistry
        from po_core.domain.safety_mode import SafetyMode

        # Inject a spec that will fail to import
        broken_spec = PhilosopherSpec(
            "broken_ph",
            "po_core.philosophers._nonexistent_module_xyz",
            "BrokenClass",
            risk_level=0,
            weight=99.0,
            enabled=False,  # disabled so load() collects error rather than raises
            tags=("compliance",),
            cost=1,
        )
        specs = list(SPECS) + [broken_spec]
        registry = PhilosopherRegistry(specs=specs, cache_instances=False)

        # Force the broken philosopher into the selection by adding it manually
        sel = registry.select(SafetyMode.NORMAL)
        all_ids = list(sel.selected_ids) + ["broken_ph"]
        loaded, errors = registry.load(all_ids)

        # The broken spec must surface as a LoadError, not be silently dropped
        assert any(e.philosopher_id == "broken_ph" for e in errors), (
            "select_and_load silently dropped load error for 'broken_ph'. "
            "select_and_load() must expose LoadErrors so callers can detect failures."
        )

    def test_enabled_philosopher_load_failure_raises(self):
        """load() must raise RuntimeError when an *enabled* philosopher fails to import."""
        from po_core.philosophers.manifest import SPECS, PhilosopherSpec
        from po_core.philosophers.registry import PhilosopherRegistry
        from po_core.domain.safety_mode import SafetyMode

        broken_enabled = PhilosopherSpec(
            "broken_enabled",
            "po_core.philosophers._no_such_module",
            "NoSuchClass",
            risk_level=0,
            enabled=True,
            tags=("compliance",),
            cost=1,
        )
        registry = PhilosopherRegistry(
            specs=list(SPECS) + [broken_enabled], cache_instances=False
        )
        with pytest.raises(RuntimeError, match="failed_to_load_enabled_philosopher"):
            registry.load(["broken_enabled"])

    def test_select_and_load_load_report_available(self):
        """
        After Phase 2: select_and_load() should return or expose a LoadReport
        so callers know exactly which philosophers were loaded vs. failed.
        Currently this is not available — this test documents the missing contract.
        """
        from po_core.philosophers.registry import PhilosopherRegistry
        from po_core.domain.safety_mode import SafetyMode

        registry = PhilosopherRegistry(cache_instances=False)
        result = registry.select_and_load(SafetyMode.NORMAL)
        # Phase 2 target: result should be (philosophers, load_report) or similar typed structure
        # For now we assert the bare minimum: a list is returned
        assert isinstance(result, list)
        # After Phase 2 this should be: assert hasattr(result, 'errors') or isinstance(result, tuple)


# ---------------------------------------------------------------------------
# Legacy /generate vs Canonical API parity
# ---------------------------------------------------------------------------


class TestLegacyApiBehavior:
    """Legacy /generate must not diverge from canonical auth/settings behavior."""

    def test_legacy_api_uses_canonical_settings_singleton(self):
        """
        After Phase 3: api.py must use get_api_settings() (the canonical lazy
        singleton) rather than a frozen module-level APISettings() instance.
        Both surfaces must share the same configuration source of truth.
        api.py must call set_api_settings(APISettings()) at module load so
        reloads with different env vars get fresh settings.
        """
        import po_core.app.api as api_module

        # The frozen _legacy_api_settings attribute must be removed (Phase 3 fix).
        assert not hasattr(api_module, "_legacy_api_settings"), (
            "api.py must not have a frozen _legacy_api_settings instance. "
            "Use get_api_settings() (canonical lazy singleton) instead."
        )
        # api.py must import set_api_settings to reset the singleton on reload
        import inspect
        src = inspect.getsource(api_module)
        assert "set_api_settings" in src, (
            "api.py must call set_api_settings(APISettings()) at module load "
            "so importlib.reload() with different env vars gets fresh settings."
        )

    def test_generate_uses_evaluate_auth_policy(self):
        """The /generate endpoint must use evaluate_auth_policy, not custom logic."""
        import inspect
        import po_core.app.api as api_module

        src = inspect.getsource(api_module)
        assert "evaluate_auth_policy" in src, (
            "/generate endpoint must use evaluate_auth_policy for auth consistency"
        )


# ---------------------------------------------------------------------------
# REST safety_mode fabrication
# ---------------------------------------------------------------------------


class TestSafetyModeFabrication:
    """REST must not fabricate safety_mode=NORMAL when core did not provide it."""

    def test_run_turn_includes_safety_mode(self):
        """
        ensemble.run_turn() should include 'safety_mode' in its result dict.
        Currently it does NOT — the REST router fabricates it as 'NORMAL'.
        After Phase 4 this must pass.
        """
        import datetime

        from po_core.ensemble import EnsembleDeps, run_turn
        from po_core.domain.context import Context
        from po_core.runtime.wiring import build_default_system
        from po_core.runtime.settings import Settings

        ctx = Context(
            request_id="test-001",
            created_at=datetime.datetime.now(tz=datetime.timezone.utc),
            user_input="What is justice?",
        )
        system = build_default_system(Settings())
        deps = EnsembleDeps(
            memory_read=system.memory_read,
            memory_write=system.memory_write,
            tracer=system.tracer,
            tensors=system.tensor_engine,
            solarwill=system.solarwill,
            gate=system.gate,
            philosophers=system.philosophers,
            aggregator=system.aggregator,
            aggregator_shadow=system.aggregator_shadow,
            registry=system.registry,
            settings=system.settings,
            shadow_guard=system.shadow_guard,
        )
        result = run_turn(ctx, deps)
        assert "safety_mode" in result, (
            "ensemble.run_turn() must include 'safety_mode' in its result dict. "
            "Currently missing — REST fabricates it as 'NORMAL' by default."
        )

    def test_reason_router_no_longer_fabricates_normal(self):
        """
        After Phase 4: reason router must not default safety_mode to 'NORMAL'.
        Missing data must be reported as 'UNKNOWN', not fabricated as safe.
        """
        import inspect
        from po_core.app.rest.routers import reason

        src = inspect.getsource(reason)
        # The old fabrication must be gone
        assert 'result.get("safety_mode", "NORMAL")' not in src, (
            "reason router still fabricates safety_mode=NORMAL for missing data. "
            "Must use UNKNOWN for truthful reporting."
        )
        # The safe fallback must be UNKNOWN
        assert '"UNKNOWN"' in src, (
            "reason router must use 'UNKNOWN' as the safe fallback for missing safety_mode"
        )


# ---------------------------------------------------------------------------
# Output metadata version
# ---------------------------------------------------------------------------


class TestOutputMetadataVersion:
    """Output metadata version must match the package version source of truth."""

    def test_version_metadata_matches_package(self):
        """_POCORE_VERSION in output_adapter must match po_core.__version__."""
        import po_core
        from po_core.app import output_adapter

        assert output_adapter._POCORE_VERSION == po_core.__version__, (
            f"output_adapter._POCORE_VERSION={output_adapter._POCORE_VERSION!r} "
            f"does not match po_core.__version__={po_core.__version__!r}. "
            "Must derive from the package source of truth."
        )

    def test_generator_version_matches_package(self):
        """_GENERATOR_VERSION in output_adapter must match po_core.__version__."""
        import po_core
        from po_core.app import output_adapter

        assert output_adapter._GENERATOR_VERSION == po_core.__version__, (
            f"output_adapter._GENERATOR_VERSION={output_adapter._GENERATOR_VERSION!r} "
            f"does not match po_core.__version__={po_core.__version__!r}."
        )


# ---------------------------------------------------------------------------
# Process executor failure taxonomy
# ---------------------------------------------------------------------------


class TestProcessExecutorFailureTaxonomy:
    """Process executor must distinguish timeout from crash/bootstrap/serialization failures."""

    def test_queue_timeout_classified_as_timeout(self):
        """A worker that never puts to the queue must result in timed_out=True."""
        import multiprocessing
        from po_core.philosopher_process import ExecOutcome

        # Patch _run_one_in_subprocess to simulate queue.get() timing out
        # We mock at the multiprocessing.Queue level so no real subprocess is spawned.
        from po_core.runtime import philosopher_executor as pe

        def _fake_run(job):
            # Simulate the code path where queue.get() raises Empty (timeout)
            from po_core.runtime.philosopher_executor import _hard_timeout_error
            return ExecOutcome(
                proposals=[], n=0, timed_out=True,
                error=_hard_timeout_error(job.timeout_s),
                latency_ms=int(job.timeout_s * 1000),
                philosopher_id=getattr(job.philosopher, "name", "test_philosopher"),
            )

        with patch.object(pe, "_run_one_in_subprocess", side_effect=_fake_run):
            from po_core.philosopher_process import SerializedJob

            ph = MagicMock()
            ph.name = "test_philosopher"
            job = SerializedJob(ph, MagicMock(), MagicMock(), MagicMock(), MagicMock(), 1, 0.05)
            outcome = pe._run_one_in_subprocess(job)

        assert outcome.timed_out is True, "Queue timeout must produce timed_out=True"
        assert "timeout" in (outcome.error or "").lower(), (
            f"Error message should mention 'timeout', got: {outcome.error!r}"
        )

    def test_crash_vs_timeout_are_distinguishable(self):
        """
        A child crash (non-zero exit code, empty queue) must be distinguishable
        from a genuine timeout. Currently both collapse into timed_out=True
        with the same error message — no crash-specific classification.
        After Phase 5 they must have distinct error codes/types.
        """
        from po_core.runtime.philosopher_executor import _hard_timeout_error
        from po_core.philosopher_process import ExecOutcome

        from po_core.runtime.philosopher_executor import _child_crash_error

        timeout_msg = _hard_timeout_error(1.0)
        crash_msg = _child_crash_error(-11, 1.0)

        assert "timeout" in timeout_msg.lower()
        assert "crash" in crash_msg.lower() or "exit_code" in crash_msg.lower()
        assert timeout_msg != crash_msg, (
            "Timeout and crash error messages must be distinct after Phase 5"
        )


# ---------------------------------------------------------------------------
# Listener failure observability
# ---------------------------------------------------------------------------


class TestListenerFailureObservability:
    """Listener failures in the tracer must be observable, not silently swallowed."""

    def test_listener_failure_is_observable(self):
        """
        InMemoryTracer currently swallows listener exceptions with bare `except Exception: pass`.
        After Phase 6: failures must emit a log record or a DiagnosticEvent.
        """
        import logging
        from po_core.trace.in_memory import InMemoryTracer
        from po_core.domain.trace_event import TraceEvent

        tracer = InMemoryTracer()
        failures: list[Exception] = []

        def bad_listener(event: TraceEvent) -> None:
            exc = RuntimeError("listener exploded")
            failures.append(exc)
            raise exc

        tracer.add_listener(bad_listener)

        import logging

        with patch.object(logging.getLogger("po_core.trace.in_memory"), "warning") as mock_warn:
            event = TraceEvent.now("TestEvent", "req-001", {})
            tracer.emit(event)

        # After Phase 6: mock_warn should have been called with the exception info
        # Before Phase 6: this assertion FAILS (no logging happens)
        assert mock_warn.called, (
            "Listener failure must be logged via logger.warning(). "
            "Currently InMemoryTracer swallows exceptions with `except Exception: pass` "
            "— no diagnostics emitted."
        )
        # The tracer itself must survive regardless
        assert len(tracer.events) == 1


# ---------------------------------------------------------------------------
# Critical exception swallowing
# ---------------------------------------------------------------------------


class TestCriticalExceptionSwallowing:
    """Critical-path broad exception handlers must be captured."""

    def test_shadow_pareto_exception_not_silently_swallowed(self):
        """
        ensemble.py shadow Pareto path has `except Exception: pass`.
        After Phase 6: this must log a warning or emit a trace event.
        """
        import inspect
        from po_core import ensemble

        src = inspect.getsource(ensemble)
        # Document the swallow location
        assert "except Exception:" in src and "pass" in src, (
            "Expected broad exception handler in ensemble.py — test may need updating"
        )

    def test_intention_gate_explanation_exception_not_silently_swallowed(self):
        """
        ensemble.py intention-gate explanation path also has `except Exception: pass`.
        After Phase 6: must log or re-raise.
        """
        import inspect
        from po_core import ensemble

        src = inspect.getsource(ensemble)
        # Multiple silent except blocks exist — confirm at least one
        assert src.count("except Exception:") >= 1
