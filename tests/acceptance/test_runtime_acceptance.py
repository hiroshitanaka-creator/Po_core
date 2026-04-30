# SPDX-License-Identifier: AGPL-3.0-or-later
"""Runtime acceptance tests — po_core.run() path for AT-001, AT-009, AT-010.

These tests exercise the *production pipeline* (po_core.app.api.run) directly,
separate from the StubComposer acceptance suite (test_acceptance_suite.py).
StubComposer tests verify the output_schema_v1 contract; these tests verify
what the raw run_turn pipeline actually produces and where it falls short.

Naming convention
-----------------
Tests that assert structural invariants which the pipeline SHOULD satisfy are
prefixed with ``test_`` as normal.  Tests that document a known production gap
are also normal ``test_`` functions but include a ``GAP <id>:`` prefix in
their docstring, and their assertions are expected to FAIL until the gap is
resolved.  The completion_matrix.md records current pass/fail status.

Gap catalogue (as of 2026-04-28)
---------------------------------
RT-GAP-001  RESOLVED — CaseSignals(values_present=False) + _apply_case_signals()
            overrides proposal.action_type to 'clarify' in ensemble.py.
RT-GAP-002  RESOLVED — _SCENARIO_ROUTING in ensemble.py maps scenario_type to
            (preferred_tags, limit_override) fed to registry.select(); distinct
            philosopher sets produce non-identical Pareto winners per scenario.
RT-GAP-003  RESOLVED — CaseSignals(has_constraint_conflict=True) +
            _apply_case_signals() injects constraint_conflict=True into result.
RT-GAP-004  RESOLVED — run_case(case: dict) added to po_core.app.api; wraps
            run_turn + adapt_to_schema and returns output_schema_v1-compliant
            output.  po_core.run(user_input: str) is unchanged.  See
            TestRunCaseSchemaConformance for pass-through validation tests and
            docs/design/rt_gap_004_run_case_proposal.md for design rationale.

Markers
-------
runtime_acceptance — included in full-suite CI; NOT in must-pass-tests
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import pytest
import yaml

_SCENARIOS_DIR = Path(__file__).resolve().parents[2] / "scenarios"
_REQUIRED_PROPOSAL_KEYS = frozenset(
    {"action_type", "content", "confidence", "proposal_id", "assumption_tags", "risk_tags"}
)


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def canonical_ids() -> frozenset[str]:
    from po_core.philosophers.manifest import get_enabled_specs

    return frozenset(s.philosopher_id for s in get_enabled_specs())


def _load_case(case_id: str) -> dict[str, Any]:
    path = _SCENARIOS_DIR / f"{case_id}.yaml"
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _invoke_pipeline(case: dict[str, Any]) -> dict[str, Any]:
    """Run po_core.run() with CaseSignals derived from the case dict.

    This mirrors the production path: StubComposer always computes
    CaseSignals via from_case_dict and forwards them to run().
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict

    return run(build_user_input(case), case_signals=from_case_dict(case))


@pytest.fixture(scope="session")
def at001_result() -> dict[str, Any]:
    return _invoke_pipeline(_load_case("case_001"))


@pytest.fixture(scope="session")
def at009_result() -> dict[str, Any]:
    return _invoke_pipeline(_load_case("case_009"))


@pytest.fixture(scope="session")
def at010_result() -> dict[str, Any]:
    return _invoke_pipeline(_load_case("case_010"))


@pytest.fixture(scope="session")
def run_case_at001() -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from po_core.app.api import run_case
    return run_case(_load_case("case_001"))


@pytest.fixture(scope="session")
def run_case_at009() -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from po_core.app.api import run_case
    return run_case(_load_case("case_009"))


@pytest.fixture(scope="session")
def run_case_at010() -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from po_core.app.api import run_case
    return run_case(_load_case("case_010"))


# ── Helpers ───────────────────────────────────────────────────────────────────


def _assert_proposal_shape(result: dict[str, Any]) -> None:
    missing = _REQUIRED_PROPOSAL_KEYS - set(result["proposal"])
    assert not missing, f"proposal missing required keys: {missing}"


def _assert_all_canonical(result: dict[str, Any], canonical_ids: frozenset[str]) -> None:
    bad = [
        p["philosopher_id"]
        for p in result["proposals"]
        if p["philosopher_id"] not in canonical_ids
    ]
    assert not bad, f"proposals contain non-canonical philosopher_ids: {bad}"


# ── AT-001: 転職（job change, full values） ───────────────────────────────────


@pytest.mark.runtime_acceptance
class TestAT001PipelineInvariants:
    """Structural invariants for AT-001 via po_core.run().  All should pass."""

    def test_status_ok(self, at001_result: dict[str, Any]) -> None:
        assert at001_result["status"] == "ok"

    def test_request_id_nonempty(self, at001_result: dict[str, Any]) -> None:
        assert at001_result["request_id"]

    def test_proposal_has_required_keys(self, at001_result: dict[str, Any]) -> None:
        _assert_proposal_shape(at001_result)

    def test_proposal_content_nonempty(self, at001_result: dict[str, Any]) -> None:
        assert at001_result["proposal"]["content"].strip()

    def test_confidence_in_range(self, at001_result: dict[str, Any]) -> None:
        c = at001_result["proposal"]["confidence"]
        assert 0.0 < c <= 1.0, f"confidence {c!r} outside (0, 1]"

    def test_proposals_list_nonempty(self, at001_result: dict[str, Any]) -> None:
        assert at001_result["proposals"], "proposals list must not be empty"

    def test_all_philosopher_ids_canonical(
        self, at001_result: dict[str, Any], canonical_ids: frozenset[str]
    ) -> None:
        _assert_all_canonical(at001_result, canonical_ids)

    def test_action_type_answer_for_full_values_case(
        self, at001_result: dict[str, Any]
    ) -> None:
        """AT-001 has a full values list; the pipeline should produce an answer."""
        assert at001_result["proposal"]["action_type"] == "answer"


# ── AT-009: 価値観が不明（empty values） ─────────────────────────────────────


@pytest.mark.runtime_acceptance
class TestAT009PipelineInvariants:
    """Structural invariants and gap assertions for AT-009 (values=[])."""

    def test_status_ok(self, at009_result: dict[str, Any]) -> None:
        assert at009_result["status"] == "ok"

    def test_proposal_has_required_keys(self, at009_result: dict[str, Any]) -> None:
        _assert_proposal_shape(at009_result)

    def test_proposal_content_nonempty(self, at009_result: dict[str, Any]) -> None:
        assert at009_result["proposal"]["content"].strip()

    def test_proposals_list_nonempty(self, at009_result: dict[str, Any]) -> None:
        assert at009_result["proposals"]

    def test_all_philosopher_ids_canonical(
        self, at009_result: dict[str, Any], canonical_ids: frozenset[str]
    ) -> None:
        _assert_all_canonical(at009_result, canonical_ids)

    def test_empty_values_yields_clarify_action(
        self, at009_result: dict[str, Any]
    ) -> None:
        """RT-GAP-001 RESOLVED: run_turn signals values-clarification when values=[].

        CaseSignals(values_present=False) is derived by from_case_dict() and
        forwarded through run() → run_turn() → _apply_case_signals(), which
        overrides proposal.action_type to 'clarify'.  The fix lives entirely in
        the pipeline layer (domain/case_signals.py + ensemble.py); output_adapter
        is unchanged.
        """
        assert at009_result["proposal"]["action_type"] == "clarify", (
            "RT-GAP-001 regression: run_turn no longer returns action_type='clarify' "
            "for empty-values case"
        )


# ── AT-010: 制約の矛盾（conflicting constraints） ────────────────────────────


@pytest.mark.runtime_acceptance
class TestAT010PipelineInvariants:
    """Structural invariants and gap assertions for AT-010 (conflicting constraints)."""

    def test_status_ok(self, at010_result: dict[str, Any]) -> None:
        assert at010_result["status"] == "ok"

    def test_proposal_has_required_keys(self, at010_result: dict[str, Any]) -> None:
        _assert_proposal_shape(at010_result)

    def test_proposal_content_nonempty(self, at010_result: dict[str, Any]) -> None:
        assert at010_result["proposal"]["content"].strip()

    def test_proposals_list_nonempty(self, at010_result: dict[str, Any]) -> None:
        assert at010_result["proposals"]

    def test_all_philosopher_ids_canonical(
        self, at010_result: dict[str, Any], canonical_ids: frozenset[str]
    ) -> None:
        _assert_all_canonical(at010_result, canonical_ids)

    def test_constraint_conflict_surface(self, at010_result: dict[str, Any]) -> None:
        """RT-GAP-003 RESOLVED: Contradictory constraints are signalled in run() output.

        CaseSignals(has_constraint_conflict=True) is derived by from_case_dict()
        via keyword matching on title/problem/scenario_profile and forwarded through
        run() → run_turn() → _apply_case_signals(), which injects
        constraint_conflict=True into the result dict.
        """
        has_conflict_signal = (
            "constraint_conflict" in at010_result
            or at010_result["proposal"]["action_type"] in {"clarify", "escalate"}
        )
        assert has_conflict_signal, (
            "RT-GAP-003 regression: no constraint-conflict signal in po_core.run() output"
        )


# ── Cross-scenario invariants ─────────────────────────────────────────────────


@pytest.mark.runtime_acceptance
class TestRuntimeCrossScenario:
    """Cross-scenario assertions that expose pipeline uniformity gaps."""

    def test_at009_and_at010_content_differs(
        self, at009_result: dict[str, Any], at010_result: dict[str, Any]
    ) -> None:
        """RT-GAP-002 RESOLVED: AT-009 and AT-010 produce distinct proposal content.

        _SCENARIO_ROUTING in ensemble.py routes each scenario_type to a different
        philosopher roster via preferred_tags + limit_override on registry.select():
          values_clarification    → clarify+creative+compliance, limit=3
                                    → [confucius, zhuangzi, kant]
                                    → Pareto winner: Confucius
          conflicting_constraints → critic+redteam+planner, limit=3
                                    → [kant, nietzsche, marcus_aurelius]
                                    → Pareto winner: Nietzsche

        Confucius is excluded from the conflicting_constraints roster (it carries
        no critic/redteam/planner tags), guaranteeing a different Pareto winner
        and non-identical proposal.content.
        """
        c009 = at009_result["proposal"]["content"]
        c010 = at010_result["proposal"]["content"]
        assert c009 != c010, (
            "RT-GAP-002 regression: AT-009 and AT-010 produce byte-identical content; "
            "scenario routing may have stopped differentiating philosopher sets"
        )

    def test_run_output_conforms_to_output_schema_v1(
        self,
        run_case_at001: dict[str, Any],
        validate_output_schema: Any,
    ) -> None:
        """RT-GAP-004 RESOLVED: run_case(case) returns output_schema_v1-compliant output.

        po_core.run_case(case: dict) wraps run_turn + adapt_to_schema and returns a
        dict with all output_schema_v1 keys.  po_core.run(user_input: str) is
        unchanged — it still returns the raw pipeline dict for plain-text callers.

        Design note: docs/design/rt_gap_004_run_case_proposal.md.
        """
        validate_output_schema(run_case_at001, "RT-GAP-004/run_case/AT-001")


# ── RT-GAP-004: run_case() schema conformance ─────────────────────────────────


@pytest.mark.runtime_acceptance
class TestRunCaseSchemaConformance:
    """RT-GAP-004 RESOLVED: run_case(case) passes full output_schema_v1 validation.

    These tests exercise all three canonical scenario types (full-values,
    empty-values, conflicting-constraints) and also verify that the pipeline's
    philosophical reasoning propagates through options[0].description.
    """

    def test_at001_conforms_to_output_schema_v1(
        self, run_case_at001: dict[str, Any], validate_output_schema: Any
    ) -> None:
        validate_output_schema(run_case_at001, "run_case/AT-001")

    def test_at009_conforms_to_output_schema_v1(
        self, run_case_at009: dict[str, Any], validate_output_schema: Any
    ) -> None:
        validate_output_schema(run_case_at009, "run_case/AT-009")

    def test_at010_conforms_to_output_schema_v1(
        self, run_case_at010: dict[str, Any], validate_output_schema: Any
    ) -> None:
        validate_output_schema(run_case_at010, "run_case/AT-010")

    def test_philosophical_content_in_options(
        self, run_case_at001: dict[str, Any]
    ) -> None:
        """Pipeline proposal.content propagates into options[0].description."""
        assert run_case_at001["options"][0]["description"].strip()

    def test_at009_questions_nonempty(self, run_case_at009: dict[str, Any]) -> None:
        """AT-009 (values=[]) → values-clarification questions are generated."""
        assert run_case_at009["questions"], "expected non-empty questions for empty-values case"

    def test_at010_uncertainty_high(self, run_case_at010: dict[str, Any]) -> None:
        """AT-010 (conflicting constraints) → uncertainty.overall_level == 'high'."""
        assert run_case_at010["uncertainty"]["overall_level"] == "high"

    def test_run_case_at001_deterministic_created_at(
        self, run_case_at001: dict[str, Any]
    ) -> None:
        """seed=42 + no case["now"] → fixed timestamp "2026-03-03T00:00:00Z"."""
        assert run_case_at001["meta"]["created_at"] == "2026-03-03T00:00:00Z"


# ── TR-1: CaseSignals trace visibility ───────────────────────────────────────


@pytest.mark.runtime_acceptance
class TestCaseSignalsTraceVisibility:
    """TR-1: CaseSignals mutations must emit a CaseSignalsApplied TraceEvent.

    _apply_case_signals() currently mutates the run_turn result dict silently:
      - values_present=False  → action_type overridden to 'clarify'
      - has_constraint_conflict=True → constraint_conflict=True injected

    These audit-relevant mutations must appear in the trace so that callers
    can observe why the output changed from the raw pipeline result.
    """

    @staticmethod
    def _run_with_tracer(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        return result, tracer

    def test_at009_case_signals_event_emitted(self) -> None:
        """TR-1/AT-009: CaseSignalsApplied event must appear in trace for empty-values case."""
        _, tracer = self._run_with_tracer("case_009")
        event_types = [e.event_type for e in tracer.events]
        assert any("CaseSignals" in t for t in event_types), (
            f"No CaseSignals trace event found. Emitted events: {event_types}\n"
            "The action_type='clarify' override by _apply_case_signals() is "
            "currently invisible in the trace."
        )

    def test_at009_case_signals_event_payload(self) -> None:
        """TR-1/AT-009: CaseSignalsApplied payload must document the action_type override."""
        result, tracer = self._run_with_tracer("case_009")

        assert result["proposal"]["action_type"] == "clarify"

        ev = next(
            (e for e in tracer.events if e.event_type == "CaseSignalsApplied"), None
        )
        assert ev is not None, "CaseSignalsApplied event not found in trace"

        p = ev.payload
        assert p["scenario_type"] == "values_clarification"
        assert p["values_present"] is False
        assert p["action_type_before"] == "answer"
        assert p["action_type_after"] == "clarify"
        assert "action_type:answer->clarify" in p["applied_changes"]

    def test_at010_case_signals_event_emitted(self) -> None:
        """TR-1/AT-010: CaseSignalsApplied event must appear in trace for conflicting-constraints case."""
        _, tracer = self._run_with_tracer("case_010")
        event_types = [e.event_type for e in tracer.events]
        assert any("CaseSignals" in t for t in event_types), (
            f"No CaseSignals trace event found. Emitted events: {event_types}\n"
            "The constraint_conflict injection by _apply_case_signals() is "
            "currently invisible in the trace."
        )

    def test_at010_case_signals_event_payload(self) -> None:
        """TR-1/AT-010: CaseSignalsApplied payload must document the constraint_conflict injection."""
        _, tracer = self._run_with_tracer("case_010")

        ev = next(
            (e for e in tracer.events if e.event_type == "CaseSignalsApplied"), None
        )
        assert ev is not None, "CaseSignalsApplied event not found in trace"

        p = ev.payload
        assert p["scenario_type"] == "conflicting_constraints"
        assert p["has_constraint_conflict"] is True
        assert p["constraint_conflict_added"] is True
        assert "constraint_conflict:true" in p["applied_changes"]

    def test_at001_no_case_signals_event_when_no_mutation(self) -> None:
        """TR-1/AT-001: CaseSignalsApplied must NOT be emitted when no mutation is made.

        case_001 has a full values list and no constraint conflict, so
        _apply_case_signals() produces no changes.  The event must be
        suppressed — emitting it with applied_changes=[] would be misleading.
        """
        result, tracer = self._run_with_tracer("case_001")

        assert result["proposal"]["action_type"] == "answer"
        event_types = [e.event_type for e in tracer.events]
        assert "CaseSignalsApplied" not in event_types, (
            f"CaseSignalsApplied was emitted for a no-mutation case. "
            f"All events: {event_types}"
        )


# ── AGG-TR-1: Pareto winner trace contract ───────────────────────────────────


@pytest.mark.runtime_acceptance
class TestParetoWinnerTraceContract:
    """AGG-TR-1: ParetoWinnerSelected trace must agree with the final returned proposal.

    emit_pareto_debug_events() is tested in isolation.  This class tests the
    production run() path end-to-end: the trace event must exist and its
    winner.proposal_id must equal result["proposal"]["proposal_id"].

    Also asserts that AggregateCompleted is present with the same proposal_id,
    proving the aggregator result and the Pareto trace are consistent across
    the full pipeline.
    """

    @staticmethod
    def _run_with_tracer(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        return result, tracer

    def test_pareto_winner_trace_matches_final_result(self) -> None:
        """AGG-TR-1: ParetoWinnerSelected.winner.proposal_id == result.proposal.proposal_id."""
        result, tracer = self._run_with_tracer("case_001")

        final_pid = result["proposal"]["proposal_id"]

        ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )
        assert ev is not None, (
            f"ParetoWinnerSelected event not found in trace. "
            f"Emitted events: {[e.event_type for e in tracer.events]}"
        )

        p = ev.payload
        assert "winner" in p, f"ParetoWinnerSelected payload missing 'winner' key: {p}"
        assert p["winner"]["proposal_id"] == final_pid, (
            f"Pareto trace winner ({p['winner']['proposal_id']!r}) diverges from "
            f"final returned proposal ({final_pid!r})"
        )

    def test_pareto_winner_payload_has_required_keys(self) -> None:
        """AGG-TR-1: ParetoWinnerSelected payload must contain all required diagnostic keys."""
        _, tracer = self._run_with_tracer("case_001")

        ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )
        assert ev is not None, "ParetoWinnerSelected event not found in trace"

        p = ev.payload
        for key in ("mode", "weights", "freedom_pressure", "winner"):
            assert key in p, f"ParetoWinnerSelected payload missing key {key!r}: {p}"

        w = p["winner"]
        for key in ("proposal_id", "scores", "content_hash"):
            assert key in w, f"ParetoWinnerSelected winner missing key {key!r}: {w}"

    def test_aggregate_completed_matches_final_result(self) -> None:
        """AGG-TR-1: AggregateCompleted.proposal_id must equal result.proposal.proposal_id."""
        result, tracer = self._run_with_tracer("case_001")

        final_pid = result["proposal"]["proposal_id"]

        ev = next(
            (e for e in tracer.events if e.event_type == "AggregateCompleted"), None
        )
        assert ev is not None, (
            f"AggregateCompleted event not found in trace. "
            f"Emitted events: {[e.event_type for e in tracer.events]}"
        )
        assert ev.payload["proposal_id"] == final_pid, (
            f"AggregateCompleted proposal_id ({ev.payload['proposal_id']!r}) diverges "
            f"from final returned proposal ({final_pid!r})"
        )


# ── AGG-TR-2: Pareto winner score explainability ──────────────────────────────

_OBJECTIVE_KEYS = frozenset(
    {"safety", "freedom", "explain", "brevity", "coherence", "emergence"}
)


@pytest.mark.runtime_acceptance
class TestParetoWinnerScoreExplainability:
    """AGG-TR-2: The Pareto winner score must be fully recomputable from trace payload.

    ParetoWinnerSelected now carries winner["scores"] (6D objective vector),
    winner["weighted_score"] (precomputed dot product), and weights (mode-specific
    multipliers).  These three fields together are sufficient to explain why the
    winner was selected over other Pareto-front proposals.
    """

    @staticmethod
    def _get_pareto_events(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        winner_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )
        front_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoFrontComputed"), None
        )
        return winner_ev, front_ev

    def test_pareto_winner_score_recomputable_from_trace(self) -> None:
        """AGG-TR-2: weighted_score must equal dot(scores, weights) within tolerance."""
        winner_ev, _ = self._get_pareto_events("case_001")
        assert winner_ev is not None, "ParetoWinnerSelected event not found"

        p = winner_ev.payload
        scores = p["winner"]["scores"]
        weights = p["weights"]

        recomputed = sum(
            scores.get(k, 0.0) * weights.get(k, 0.0) for k in _OBJECTIVE_KEYS
        )
        assert recomputed > 0, (
            f"Recomputed weighted score is {recomputed!r} — expected > 0. "
            f"scores={scores}, weights={weights}"
        )

        assert "weighted_score" in p["winner"], (
            "winner payload missing 'weighted_score' key — add it to ParetoAggregator"
        )
        stored = p["winner"]["weighted_score"]
        assert abs(stored - recomputed) < 1e-4, (
            f"stored weighted_score ({stored!r}) diverges from recomputed "
            f"({recomputed!r}) by more than 1e-4"
        )

    def test_pareto_front_rows_include_scores_for_all_objectives(self) -> None:
        """AGG-TR-2: Every front row must include all 6 objective score keys."""
        _, front_ev = self._get_pareto_events("case_001")
        assert front_ev is not None, "ParetoFrontComputed event not found"

        front = front_ev.payload.get("front", [])
        assert front, "ParetoFrontComputed front list is empty"

        for row in front:
            row_scores = row.get("scores", {})
            missing = _OBJECTIVE_KEYS - set(row_scores)
            assert not missing, (
                f"Front row {row.get('proposal_id')!r} scores missing keys: {missing}"
            )

    def test_pareto_winner_scores_include_all_objectives(self) -> None:
        """AGG-TR-2: winner['scores'] must include all 6 objective keys."""
        winner_ev, _ = self._get_pareto_events("case_001")
        assert winner_ev is not None, "ParetoWinnerSelected event not found"

        w_scores = winner_ev.payload["winner"]["scores"]
        missing = _OBJECTIVE_KEYS - set(w_scores)
        assert not missing, (
            f"winner['scores'] missing objective keys: {missing}"
        )


# ── AGG-TR-3: SafetyMode-dependent Pareto weights trace contract ──────────────


@pytest.mark.runtime_acceptance
class TestParetoSafetyModeWeights:
    """AGG-TR-3: Pareto weights differ by SafetyMode and are visible in production trace.

    ParetoAggregator._get_weights() returns mode-specific multipliers drawn from
    ParetoConfig.weights_by_mode.  This class proves:
      1. NORMAL / WARN / CRITICAL weights are mutually distinct.
      2. CRITICAL prioritises safety (largest weight) and suppresses freedom /
         emergence (both 0.0).
      3. Production run() emits both ParetoFrontComputed and ParetoWinnerSelected
         with identical, consistent weights and mode fields.
    """

    @staticmethod
    def _make_aggregator():
        from po_core.aggregator.pareto import ParetoAggregator
        from po_core.domain.pareto_config import ParetoConfig
        from po_core.domain.safety_mode import SafetyModeConfig

        return ParetoAggregator(
            mode_config=SafetyModeConfig(),
            config=ParetoConfig.defaults(),
        )

    def test_pareto_weights_differ_by_safety_mode(self) -> None:
        """AGG-TR-3: NORMAL, WARN, and CRITICAL produce three distinct weight dicts."""
        from po_core.domain.safety_mode import SafetyMode

        agg = self._make_aggregator()
        normal_w = dict(agg._get_weights(SafetyMode.NORMAL))
        warn_w = dict(agg._get_weights(SafetyMode.WARN))
        critical_w = dict(agg._get_weights(SafetyMode.CRITICAL))

        assert normal_w != warn_w, (
            "NORMAL and WARN weights are identical — SafetyMode degradation has no effect"
        )
        assert warn_w != critical_w, (
            "WARN and CRITICAL weights are identical — SafetyMode degradation has no effect"
        )
        assert normal_w != critical_w, (
            "NORMAL and CRITICAL weights are identical — SafetyMode degradation has no effect"
        )

        # NORMAL should reward freedom and emergence (deliberation incentives)
        assert normal_w.get("freedom", 0.0) > 0.0, (
            f"NORMAL freedom weight must be > 0; got {normal_w}"
        )
        assert normal_w.get("emergence", 0.0) > 0.0, (
            f"NORMAL emergence weight must be > 0; got {normal_w}"
        )

        # WARN sits between NORMAL and CRITICAL: safety escalates monotonically
        assert warn_w.get("safety", 0.0) > normal_w.get("safety", 0.0), (
            "WARN safety weight must exceed NORMAL safety weight"
        )
        assert critical_w.get("safety", 0.0) > warn_w.get("safety", 0.0), (
            "CRITICAL safety weight must exceed WARN safety weight"
        )

    def test_critical_mode_weights_prioritize_safety(self) -> None:
        """AGG-TR-3: CRITICAL weights must put safety first and suppress freedom/emergence."""
        from po_core.domain.safety_mode import SafetyMode

        agg = self._make_aggregator()
        normal_w = dict(agg._get_weights(SafetyMode.NORMAL))
        critical_w = dict(agg._get_weights(SafetyMode.CRITICAL))

        # safety is the largest weight in CRITICAL mode
        safety_val = critical_w.get("safety", 0.0)
        assert all(
            safety_val >= v for v in critical_w.values()
        ), (
            f"CRITICAL safety ({safety_val}) is not the largest weight in {critical_w}"
        )

        # freedom must be 0.0 or strictly less than NORMAL
        assert critical_w.get("freedom", 0.0) == 0.0 or (
            critical_w.get("freedom", 0.0) < normal_w.get("freedom", 0.0)
        ), (
            f"CRITICAL freedom ({critical_w.get('freedom')}) must be 0.0 or "
            f"less than NORMAL freedom ({normal_w.get('freedom')})"
        )

        # emergence must be 0.0 or strictly less than NORMAL
        assert critical_w.get("emergence", 0.0) == 0.0 or (
            critical_w.get("emergence", 0.0) < normal_w.get("emergence", 0.0)
        ), (
            f"CRITICAL emergence ({critical_w.get('emergence')}) must be 0.0 or "
            f"less than NORMAL emergence ({normal_w.get('emergence')})"
        )

    def test_pareto_trace_records_safety_mode_and_weights_consistently(self) -> None:
        """AGG-TR-3: ParetoFrontComputed and ParetoWinnerSelected must carry matching
        mode, weights, and freedom_pressure fields in a production run().
        """
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case("case_001")
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )

        front_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoFrontComputed"), None
        )
        winner_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )

        assert front_ev is not None, (
            f"ParetoFrontComputed not found. Events: {[e.event_type for e in tracer.events]}"
        )
        assert winner_ev is not None, (
            f"ParetoWinnerSelected not found. Events: {[e.event_type for e in tracer.events]}"
        )

        fp = front_ev.payload
        wp = winner_ev.payload

        for key in ("mode", "weights", "freedom_pressure"):
            assert key in fp, f"ParetoFrontComputed payload missing {key!r}: {fp.keys()}"
            assert key in wp, f"ParetoWinnerSelected payload missing {key!r}: {wp.keys()}"

        assert fp["weights"] == wp["weights"], (
            f"ParetoFrontComputed.weights ({fp['weights']}) != "
            f"ParetoWinnerSelected.weights ({wp['weights']})"
        )
        assert fp["mode"] == wp["mode"], (
            f"ParetoFrontComputed.mode ({fp['mode']!r}) != "
            f"ParetoWinnerSelected.mode ({wp['mode']!r})"
        )

        # Both payloads must expose the emergence weight so callers can reconstruct
        # the selection rationale from the trace without access to source code.
        front_weights = fp["weights"]
        assert "emergence" in front_weights, (
            f"ParetoFrontComputed.weights missing 'emergence' key: {front_weights}. "
            "The packaged pareto_table.yaml must include emergence for all modes."
        )
        assert "emergence" in wp["weights"], (
            f"ParetoWinnerSelected.weights missing 'emergence' key: {wp['weights']}."
        )

        # case_001 runs under low freedom_pressure → NORMAL mode, so emergence must be > 0
        if fp["mode"] == "normal":
            assert front_weights["emergence"] > 0.0, (
                f"NORMAL mode emergence weight must be > 0; got {front_weights['emergence']}. "
                "Check that pareto_table.yaml wires emergence: 0.10 for the normal entry."
            )


# ── AGG-TR-4: ActionGate / final decision trace contract ─────────────────────


class _FakeRejectParetoGate:
    """Fake WethicsGatePort for AGG-TR-4 override test.

    judge_intent: always ALLOW (pass the intention gate).
    judge_action: REJECT if the proposal carries PARETO_DEBUG in its _po_core
                  namespace (i.e. the Pareto-aggregated candidate); otherwise ALLOW.

    This rejects only the ActionGate call for the Pareto winner while letting
    per-philosopher pre-screening calls and the fallback pass through.  The
    PARETO_DEBUG key is embedded by ParetoAggregator and is absent from:
      - individual philosopher proposals during pre-screening, and
      - compose_fallback() proposals.
    """

    def judge_intent(self, ctx, intent, tensors, memory):
        from po_core.domain.safety_verdict import SafetyVerdict

        return SafetyVerdict.allow(rule_ids=["WG.TEST.ALLOW"])

    def judge_action(self, ctx, intent, proposal, tensors, memory):
        from typing import Mapping

        from po_core.domain.keys import PARETO_DEBUG, PO_CORE
        from po_core.domain.safety_verdict import SafetyVerdict

        extra = dict(proposal.extra) if isinstance(proposal.extra, Mapping) else {}
        pc = extra.get(PO_CORE, {})
        if PARETO_DEBUG in pc:
            return SafetyVerdict.reject(
                rule_ids=["WG.TEST.OVERRIDE.001"],
                reasons=["test: Pareto winner rejected by fake gate"],
            )
        return SafetyVerdict.allow(rule_ids=["WG.TEST.ALLOW"])


@pytest.mark.runtime_acceptance
class TestActionGateTraceContract:
    """AGG-TR-4: The Pareto winner → final decision transition must be trace-auditable.

    Two paths:
      1. Normal path (ActionGate ALLOW): ParetoWinnerSelected, AggregateCompleted,
         DecisionEmitted all reference the same proposal_id, and DecisionEmitted
         carries degraded=False, origin="pareto".
      2. Override path (ActionGate REJECT): SafetyOverrideApplied carries the
         original Pareto winner in 'from' and the fallback in 'to'. DecisionEmitted
         carries degraded=True, origin="pareto_fallback", candidate=Pareto winner,
         final=fallback, gate.rule_ids present.
    """

    @staticmethod
    def _run_with_tracer(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            result = run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        return result, tracer

    @staticmethod
    def _run_with_fake_gate(case_id: str):
        """Run run_turn with a fake gate that rejects the Pareto-aggregated candidate."""
        import uuid
        import warnings

        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.domain.context import Context
        from po_core.ensemble import EnsembleDeps, run_turn
        from po_core.runtime.wiring import build_default_system
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            system = build_default_system()

        ctx = Context.now(
            request_id=str(uuid.uuid4()),
            user_input=build_user_input(case),
            meta={"entry": "test"},
        )
        deps = EnsembleDeps(
            memory_read=system.memory_read,
            memory_write=system.memory_write,
            tracer=tracer,
            tensors=system.tensor_engine,
            solarwill=system.solarwill,
            gate=_FakeRejectParetoGate(),
            philosophers=system.philosophers,
            aggregator=system.aggregator,
            aggregator_shadow=None,
            registry=system.registry,
            settings=system.settings,
            shadow_guard=None,
            deliberation_engine=getattr(system, "deliberation_engine", None),
        )
        result = run_turn(ctx, deps, case_signals=from_case_dict(case))
        return result, tracer

    def test_final_decision_trace_links_pareto_winner_when_allowed(self) -> None:
        """AGG-TR-4/normal: ParetoWinnerSelected → AggregateCompleted → DecisionEmitted
        must all reference the same proposal_id, and DecisionEmitted must confirm
        the ActionGate allowed the Pareto winner unchanged.
        """
        result, tracer = self._run_with_tracer("case_001")
        final_pid = result["proposal"]["proposal_id"]

        pareto_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )
        agg_ev = next(
            (e for e in tracer.events if e.event_type == "AggregateCompleted"), None
        )
        dec_ev = next(
            (
                e
                for e in tracer.events
                if e.event_type == "DecisionEmitted"
                and e.payload.get("variant") == "main"
                and not e.payload.get("degraded", True)
            ),
            None,
        )

        assert pareto_ev is not None, (
            f"ParetoWinnerSelected not found. Events: {[e.event_type for e in tracer.events]}"
        )
        assert agg_ev is not None, (
            f"AggregateCompleted not found. Events: {[e.event_type for e in tracer.events]}"
        )
        assert dec_ev is not None, (
            f"DecisionEmitted(variant=main, degraded=False) not found. "
            f"Events: {[(e.event_type, e.payload.get('degraded'), e.payload.get('variant')) for e in tracer.events if 'Decision' in e.event_type]}"
        )

        # Full chain: all three events agree on proposal_id
        pareto_pid = pareto_ev.payload["winner"]["proposal_id"]
        agg_pid = agg_ev.payload["proposal_id"]
        dec_final_pid = dec_ev.payload["final"]["proposal_id"]

        assert pareto_pid == agg_pid, (
            f"ParetoWinnerSelected.winner.proposal_id ({pareto_pid!r}) != "
            f"AggregateCompleted.proposal_id ({agg_pid!r})"
        )
        assert agg_pid == final_pid, (
            f"AggregateCompleted.proposal_id ({agg_pid!r}) != "
            f"result.proposal.proposal_id ({final_pid!r})"
        )
        assert dec_final_pid == final_pid, (
            f"DecisionEmitted.final.proposal_id ({dec_final_pid!r}) != "
            f"result.proposal.proposal_id ({final_pid!r})"
        )

        # Gate metadata
        assert dec_ev.payload["origin"] == "pareto", (
            f"DecisionEmitted.origin must be 'pareto' for normal path; "
            f"got {dec_ev.payload['origin']!r}"
        )
        assert dec_ev.payload["degraded"] is False, (
            "DecisionEmitted.degraded must be False when ActionGate allows Pareto winner"
        )

    def test_actiongate_override_trace_auditable(self) -> None:
        """AGG-TR-4/override: When ActionGate rejects the Pareto winner, the trace must
        contain SafetyOverrideApplied (from=Pareto winner, to=fallback) and
        DecisionEmitted(degraded=True) linking original candidate to final fallback.
        """
        result, tracer = self._run_with_fake_gate("case_001")

        override_ev = next(
            (e for e in tracer.events if e.event_type == "SafetyOverrideApplied"), None
        )
        dec_ev = next(
            (
                e
                for e in tracer.events
                if e.event_type == "DecisionEmitted"
                and e.payload.get("variant") == "main"
                and e.payload.get("degraded", False)
            ),
            None,
        )

        assert override_ev is not None, (
            f"SafetyOverrideApplied not found after gate rejection. "
            f"Events: {[e.event_type for e in tracer.events]}"
        )
        assert dec_ev is not None, (
            f"DecisionEmitted(degraded=True) not found after gate rejection. "
            f"Events: {[(e.event_type, e.payload.get('degraded')) for e in tracer.events if 'Decision' in e.event_type]}"
        )

        # SafetyOverrideApplied: from=Pareto winner, to=fallback
        ov_p = override_ev.payload
        assert "from" in ov_p, f"SafetyOverrideApplied missing 'from' key: {ov_p.keys()}"
        assert "to" in ov_p, f"SafetyOverrideApplied missing 'to' key: {ov_p.keys()}"
        assert "gate" in ov_p, f"SafetyOverrideApplied missing 'gate' key: {ov_p.keys()}"

        original_pid = ov_p["from"]["proposal_id"]
        fallback_pid = ov_p["to"]["proposal_id"]
        assert original_pid != fallback_pid, (
            "SafetyOverrideApplied.from and .to must have different proposal_ids"
        )

        # Gate details: rule_ids and decision must be present
        gate = ov_p["gate"]
        assert gate.get("decision") not in (None, "allow"), (
            f"SafetyOverrideApplied gate.decision must be non-allow; got {gate.get('decision')!r}"
        )
        assert gate.get("rule_ids"), (
            f"SafetyOverrideApplied gate.rule_ids must be non-empty; got {gate.get('rule_ids')!r}"
        )

        # DecisionEmitted: degraded=True, candidate=original Pareto winner
        dp = dec_ev.payload
        assert dp["degraded"] is True, "DecisionEmitted.degraded must be True for override path"
        assert dp["origin"] in ("pareto_fallback", "safety_fallback", "pareto_shadow_fallback"), (
            f"DecisionEmitted.origin unexpected for override path: {dp['origin']!r}"
        )

        candidate_in_dec = dp.get("candidate") or {}
        assert candidate_in_dec.get("proposal_id") == original_pid, (
            f"DecisionEmitted.candidate.proposal_id ({candidate_in_dec.get('proposal_id')!r}) "
            f"must equal SafetyOverrideApplied.from.proposal_id ({original_pid!r})"
        )

        final_in_dec = dp.get("final") or {}
        assert final_in_dec.get("proposal_id") == fallback_pid, (
            f"DecisionEmitted.final.proposal_id ({final_in_dec.get('proposal_id')!r}) "
            f"must equal SafetyOverrideApplied.to.proposal_id ({fallback_pid!r})"
        )
        assert final_in_dec.get("action_type"), (
            "DecisionEmitted.final.action_type must be present"
        )

        # Fallback is the actual pipeline output when gate rejects Pareto winner
        assert result["proposal"]["proposal_id"] == fallback_pid, (
            f"result.proposal.proposal_id ({result['proposal']['proposal_id']!r}) "
            f"must equal the fallback proposal_id ({fallback_pid!r})"
        )


# ── MODE-TR-1: SafetyMode inference trace contract ────────────────────────────

_SAFETY_MODE_INFERRED_REQUIRED_KEYS = frozenset(
    {
        "mode",
        "freedom_pressure",
        "warn_threshold",
        "critical_threshold",
        "missing_mode",
        "source_metric",
        "reason",
    }
)


@pytest.mark.runtime_acceptance
class TestSafetyModeInferredTrace:
    """MODE-TR-1: SafetyModeInferred event must explain why a SafetyMode was selected.

    The pipeline infers SafetyMode from freedom_pressure tensors early in
    _run_phase_pre.  Downstream events (PhilosophersSelected, ParetoFrontComputed,
    ParetoWinnerSelected) all carry the mode value, but without the inference event
    a trace consumer cannot reconstruct *why* that mode was chosen — i.e. the
    raw metric value and the thresholds that were compared.

    SafetyModeInferred fills that gap: it records the metric value, both
    thresholds, the resulting mode, and a human-readable reason string.
    """

    @staticmethod
    def _run_with_tracer(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        return tracer

    def test_safety_mode_inferred_event_present_in_runtime_trace(self) -> None:
        """MODE-TR-1: SafetyModeInferred event must appear in trace with all required keys."""
        tracer = self._run_with_tracer("case_001")

        ev = next(
            (e for e in tracer.events if e.event_type == "SafetyModeInferred"), None
        )
        assert ev is not None, (
            f"SafetyModeInferred event not found. "
            f"Emitted events: {[e.event_type for e in tracer.events]}"
        )

        missing = _SAFETY_MODE_INFERRED_REQUIRED_KEYS - set(ev.payload)
        assert not missing, (
            f"SafetyModeInferred payload missing keys: {missing}. "
            f"Got: {set(ev.payload)}"
        )

    def test_safety_mode_inferred_matches_downstream_trace_modes(self) -> None:
        """MODE-TR-1: SafetyModeInferred.mode must agree with PhilosophersSelected,
        ParetoFrontComputed, and ParetoWinnerSelected mode fields.
        """
        tracer = self._run_with_tracer("case_001")

        smi_ev = next(
            (e for e in tracer.events if e.event_type == "SafetyModeInferred"), None
        )
        phil_ev = next(
            (e for e in tracer.events if e.event_type == "PhilosophersSelected"), None
        )
        front_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoFrontComputed"), None
        )
        winner_ev = next(
            (e for e in tracer.events if e.event_type == "ParetoWinnerSelected"), None
        )

        assert smi_ev is not None, "SafetyModeInferred event not found"
        assert phil_ev is not None, "PhilosophersSelected event not found"
        assert front_ev is not None, "ParetoFrontComputed event not found"
        assert winner_ev is not None, "ParetoWinnerSelected event not found"

        inferred_mode = smi_ev.payload["mode"]
        for label, ev in (
            ("PhilosophersSelected", phil_ev),
            ("ParetoFrontComputed", front_ev),
            ("ParetoWinnerSelected", winner_ev),
        ):
            downstream_mode = ev.payload.get("mode")
            assert downstream_mode == inferred_mode, (
                f"{label}.mode ({downstream_mode!r}) != "
                f"SafetyModeInferred.mode ({inferred_mode!r})"
            )

    def test_safety_mode_inferred_threshold_reason_is_consistent(self) -> None:
        """MODE-TR-1: The reason string must be consistent with the numeric values.

        Given freedom_pressure, warn_threshold, critical_threshold, mode, and reason,
        the reason must correctly reflect which branch of infer_safety_mode() fired.
        """
        tracer = self._run_with_tracer("case_001")

        ev = next(
            (e for e in tracer.events if e.event_type == "SafetyModeInferred"), None
        )
        assert ev is not None, "SafetyModeInferred event not found"

        p = ev.payload
        fp = p["freedom_pressure"]  # float or None
        warn = p["warn_threshold"]
        crit = p["critical_threshold"]
        mode = p["mode"]
        reason = p["reason"]

        if fp is None:
            assert reason == "freedom_pressure_missing", (
                f"freedom_pressure is None but reason is {reason!r}; "
                "expected 'freedom_pressure_missing'"
            )
            assert mode == p["missing_mode"], (
                f"freedom_pressure is None but mode ({mode!r}) != "
                f"missing_mode ({p['missing_mode']!r})"
            )
        elif fp >= crit:
            assert mode == "critical", (
                f"freedom_pressure ({fp}) >= critical_threshold ({crit}) "
                f"but mode is {mode!r} instead of 'critical'"
            )
            assert reason == "freedom_pressure >= critical_threshold", (
                f"Unexpected reason for CRITICAL: {reason!r}"
            )
        elif fp >= warn:
            assert mode == "warn", (
                f"freedom_pressure ({fp}) in [warn={warn}, crit={crit}) "
                f"but mode is {mode!r} instead of 'warn'"
            )
            assert reason == "warn_threshold <= freedom_pressure < critical_threshold", (
                f"Unexpected reason for WARN: {reason!r}"
            )
        else:
            assert mode == "normal", (
                f"freedom_pressure ({fp}) < warn_threshold ({warn}) "
                f"but mode is {mode!r} instead of 'normal'"
            )
            assert reason == "freedom_pressure < warn_threshold", (
                f"Unexpected reason for NORMAL: {reason!r}"
            )


# ── SEL-TR-1: Philosopher selection rationale ─────────────────────────────────

_SEL_TR_1_RATIONALE_KEYS = frozenset(
    {
        "max_risk",
        "cost_budget",
        "limit_override",
        "preferred_tags",
        "limit",
        "require_tags",
    }
)


@pytest.mark.runtime_acceptance
class TestPhilosopherSelectionRationale:
    """SEL-TR-1: Philosopher selection rationale must be trace-auditable.

    PhilosophersSelected payload must record both the raw override inputs
    (limit_override, preferred_tags) and the effective constraints that
    registry.select() actually applied (limit, require_tags, max_risk,
    cost_budget).  A trace consumer must be able to reconstruct *why* a
    given roster was chosen without inspecting internal plan state.
    """

    @staticmethod
    def _run_with_tracer(case_id: str):
        import warnings

        from po_core.app.api import run
        from po_core.app.output_adapter import build_user_input
        from po_core.domain.case_signals import from_case_dict
        from po_core.trace.in_memory import InMemoryTracer

        case = _load_case(case_id)
        tracer = InMemoryTracer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            run(
                build_user_input(case),
                case_signals=from_case_dict(case),
                tracer=tracer,
            )
        return tracer

    @staticmethod
    def _get_phil_event(tracer):
        ev = next(
            (e for e in tracer.events if e.event_type == "PhilosophersSelected"), None
        )
        assert ev is not None, (
            f"PhilosophersSelected event not found. "
            f"Emitted events: {[e.event_type for e in tracer.events]}"
        )
        return ev

    def test_philosophers_selected_payload_has_selection_rationale(self) -> None:
        """SEL-TR-1: PhilosophersSelected must include all selection-rationale keys."""
        tracer = self._run_with_tracer("case_001")
        ev = self._get_phil_event(tracer)

        missing = _SEL_TR_1_RATIONALE_KEYS - set(ev.payload)
        assert not missing, (
            f"PhilosophersSelected payload missing rationale keys: {missing}. "
            f"Got: {set(ev.payload)}"
        )

        # case_001 is a plain general case — no scenario routing override.
        p = ev.payload
        assert p["limit_override"] is None, (
            f"case_001 has no scenario routing; limit_override should be None, got {p['limit_override']!r}"
        )
        assert p["preferred_tags"] is None, (
            f"case_001 has no scenario routing; preferred_tags should be None, got {p['preferred_tags']!r}"
        )
        assert p["limit"] is not None, (
            "limit (effective) must not be None"
        )
        assert p["require_tags"], (
            "require_tags (effective) must be non-empty"
        )

    def test_values_clarification_selection_records_effective_constraints(self) -> None:
        """SEL-TR-1: AT-009 (values_clarification) → effective limit and require_tags agree with override."""
        from po_core.philosophers.tags import TAG_CLARIFY, TAG_COMPLIANCE, TAG_CREATIVE

        tracer = self._run_with_tracer("case_009")
        ev = self._get_phil_event(tracer)
        p = ev.payload

        expected_tags = [TAG_CLARIFY, TAG_CREATIVE, TAG_COMPLIANCE]

        assert p["limit_override"] == 3, (
            f"AT-009 limit_override: expected 3; got {p['limit_override']!r}"
        )
        assert p["limit"] == 3, (
            f"AT-009 effective limit: expected 3; got {p['limit']!r}"
        )
        assert p["preferred_tags"] == expected_tags, (
            f"AT-009 preferred_tags: expected {expected_tags!r}; got {p['preferred_tags']!r}"
        )
        assert p["require_tags"] == expected_tags, (
            f"AT-009 effective require_tags: expected {expected_tags!r}; got {p['require_tags']!r}"
        )

    def test_conflicting_constraints_selection_records_effective_constraints(self) -> None:
        """SEL-TR-1: AT-010 (conflicting_constraints) → effective limit and require_tags agree with override."""
        from po_core.philosophers.tags import TAG_CRITIC, TAG_PLANNER, TAG_REDTEAM

        tracer = self._run_with_tracer("case_010")
        ev = self._get_phil_event(tracer)
        p = ev.payload

        expected_tags = [TAG_CRITIC, TAG_REDTEAM, TAG_PLANNER]

        assert p["limit_override"] == 3, (
            f"AT-010 limit_override: expected 3; got {p['limit_override']!r}"
        )
        assert p["limit"] == 3, (
            f"AT-010 effective limit: expected 3; got {p['limit']!r}"
        )
        assert p["preferred_tags"] == expected_tags, (
            f"AT-010 preferred_tags: expected {expected_tags!r}; got {p['preferred_tags']!r}"
        )
        assert p["require_tags"] == expected_tags, (
            f"AT-010 effective require_tags: expected {expected_tags!r}; got {p['require_tags']!r}"
        )

    def test_scenario_routing_selects_distinct_rosters(self) -> None:
        """SEL-TR-1: AT-009 and AT-010 must produce distinct philosopher rosters in trace."""
        tracer_009 = self._run_with_tracer("case_009")
        tracer_010 = self._run_with_tracer("case_010")

        ev_009 = self._get_phil_event(tracer_009)
        ev_010 = self._get_phil_event(tracer_010)

        ids_009 = set(ev_009.payload["ids"])
        ids_010 = set(ev_010.payload["ids"])

        assert ids_009 != ids_010, (
            f"SEL-TR-1: AT-009 and AT-010 rosters are identical; "
            f"expected distinct selections driven by _SCENARIO_ROUTING. "
            f"Got: {sorted(ids_009)!r}"
        )
