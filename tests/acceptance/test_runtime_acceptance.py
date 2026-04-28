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
