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
RT-GAP-001  pipeline always returns action_type='answer'; values-clarification
            signal is not surfaced by run_turn even when values=[]
RT-GAP-002  AT-009 and AT-010 produce byte-identical proposal content despite
            representing distinct scenario types
RT-GAP-003  run() output carries no constraint-conflict signal for AT-010
RT-GAP-004  po_core.run() output shape does not conform to output_schema_v1;
            the StubComposer/output_adapter layer is required to bridge it

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

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "RT-GAP-004 (known architectural gap): po_core.run() output shape is "
            "{status, request_id, proposal, proposals}; it does not return "
            "output_schema_v1 keys natively. The output_adapter bridge is required. "
            "XFAIL while gap persists; XPASS alerts to update completion_matrix.md."
        ),
    )
    def test_run_output_conforms_to_output_schema_v1(
        self, at001_result: dict[str, Any]
    ) -> None:
        """RT-GAP-004 (xfail): po_core.run() output shape ≠ output_schema_v1.

        output_schema_v1 requires top-level keys: meta, case_ref, options,
        recommendation, ethics, responsibility, questions, uncertainty, trace.
        po_core.run() returns only: status, request_id, proposal, proposals.

        The output_adapter (adapt_to_schema) bridges this gap by using case
        metadata to construct most structural fields independently of pipeline
        content.  The pipeline's philosophical reasoning populates only
        options[0].description in the final schema-compliant output.

        This test ASSERTS the gap exists and will fail once the pipeline is
        extended to return schema-compliant output natively.
        """
        schema_v1_required = {
            "meta", "case_ref", "options", "recommendation",
            "ethics", "responsibility", "questions", "uncertainty", "trace",
        }
        missing = schema_v1_required - set(at001_result)
        assert not missing, (
            f"RT-GAP-004: po_core.run() output missing output_schema_v1 keys: {missing}"
        )
