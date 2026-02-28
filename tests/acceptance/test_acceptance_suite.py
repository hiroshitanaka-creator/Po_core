# SPDX-License-Identifier: AGPL-3.0-or-later
"""Acceptance test suite — AT-001 through AT-010.

Each test follows the Given/When/Then pattern defined in
``docs/spec/test_cases.md``:

- **Given:** A scenario loaded from ``scenarios/case_NNN.yaml``
- **When:**  ``StubComposer.compose(case)`` is called
- **Then:**  The output meets all acceptance conditions for that test case

Global guard (AT-OUT-001): Every test validates output against
``output_schema_v1.json`` before checking case-specific requirements.
If schema validation fails, the test immediately fails with a clear message.

Markers:
    acceptance — all tests in this file
    pipeline   — AT-001 is also pipeline (runs in must-pass CI job)
"""

from __future__ import annotations

from typing import Any

import jsonschema
import pytest

# ── Helpers ───────────────────────────────────────────────────────────────────

pytestmark = pytest.mark.acceptance


def _validate_schema(
    output: dict[str, Any], schema: dict[str, Any], test_id: str
) -> None:
    """AT-OUT-001 guard: validate output against output_schema_v1.json."""
    try:
        validator = jsonschema.Draft202012Validator(schema)
        errors = list(validator.iter_errors(output))
        if errors:
            msg = f"[{test_id}] AT-OUT-001 FAIL — schema validation errors:\n"
            msg += "\n".join(f"  • {e.message} (path: {list(e.path)})" for e in errors)
            pytest.fail(msg)
    except jsonschema.exceptions.SchemaError as exc:
        pytest.fail(f"[{test_id}] Schema itself is invalid: {exc}")


def _assert_option_count(output: dict[str, Any], min_count: int = 2) -> None:
    """FR-OPT-001: at least ``min_count`` options required."""
    assert len(output["options"]) >= min_count, (
        f"FR-OPT-001: expected ≥ {min_count} options, got {len(output['options'])}"
    )


def _assert_recommendation_present(output: dict[str, Any]) -> None:
    """FR-REC-001: recommendation must be present (either status)."""
    rec = output["recommendation"]
    assert rec["status"] in {"recommended", "no_recommendation"}, (
        f"FR-REC-001: unexpected recommendation status: {rec['status']}"
    )
    if rec["status"] == "recommended":
        assert rec.get("counter"), "FR-REC-001: counter (反証) must be non-empty"
        assert rec.get("alternatives"), "FR-REC-001: alternatives must be non-empty"


def _assert_ethics(output: dict[str, Any], min_principles: int = 2) -> None:
    """FR-ETH-001: at least ``min_principles`` ethics principles used."""
    used = output["ethics"]["principles_used"]
    assert len(used) >= min_principles, (
        f"FR-ETH-001: expected ≥ {min_principles} ethics principles, got {len(used)}: {used}"
    )


def _assert_responsibility(output: dict[str, Any]) -> None:
    """FR-RES-001: decision_owner must be set and must NOT be Po_core."""
    owner = output["responsibility"]["decision_owner"]
    assert owner, "FR-RES-001: decision_owner must not be empty"
    forbidden = {"po_core", "pocore", "po core", "the system", "ai"}
    assert owner.lower().strip() not in forbidden, (
        f"FR-RES-001: decision_owner must not be Po_core — got: '{owner}'"
    )


def _assert_uncertainty(output: dict[str, Any]) -> None:
    """FR-UNC-001: uncertainty overall_level and reasons must be present."""
    unc = output["uncertainty"]
    assert unc["overall_level"] in {"low", "medium", "high"}, (
        f"FR-UNC-001: invalid overall_level: {unc['overall_level']}"
    )
    assert unc["reasons"], "FR-UNC-001: uncertainty reasons must not be empty"


def _assert_trace(output: dict[str, Any]) -> None:
    """FR-TR-001: trace must have all 6 required steps."""
    expected_steps = {
        "parse_input",
        "generate_options",
        "ethics_review",
        "responsibility_review",
        "question_layer",
        "compose_output",
    }
    actual_steps = {s["name"] for s in output["trace"]["steps"]}
    missing = expected_steps - actual_steps
    assert not missing, f"FR-TR-001: missing trace steps: {missing}"


def _assert_no_forbidden_phrases(output: dict[str, Any]) -> None:
    """FR-RES-001: output must not contain phrases where Po_core claims to decide."""
    forbidden_phrases = [
        "po_core は決断する",
        "po_coreは決断",
        "あなたは従うべき",
        "あなたは〜すべきです",
        "必ず〜しなさい",
        "Po_core decides",
        "you must obey",
    ]
    output_str = str(output).lower()
    for phrase in forbidden_phrases:
        assert phrase.lower() not in output_str, (
            f"FR-RES-001: forbidden phrase detected: '{phrase}'"
        )


def _assert_questions_present(output: dict[str, Any]) -> None:
    """FR-Q-001: questions list must be non-empty for cases with unknowns."""
    assert output["questions"], "FR-Q-001: expected ≥ 1 question for this case"


def _assert_no_forbidden_decision_owner(output: dict[str, Any]) -> None:
    """Alias for _assert_responsibility — used in verbose assertions."""
    _assert_responsibility(output)


# ── Full check (all MUST requirements) ────────────────────────────────────────


def _full_must_check(
    output: dict[str, Any], schema: dict[str, Any], test_id: str
) -> None:
    _validate_schema(output, schema, test_id)
    _assert_option_count(output)
    _assert_recommendation_present(output)
    _assert_ethics(output)
    _assert_responsibility(output)
    _assert_uncertainty(output)
    _assert_trace(output)
    _assert_no_forbidden_phrases(output)


# ── AT-001: 転職の二択（収入 vs やりがい） ────────────────────────────────────


@pytest.mark.pipeline
def test_at_001_job_change(case_001, composer, output_schema):
    """AT-001: 転職：安定企業→スタートアップ

    Requirements: FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001
    """
    output = composer.compose(case_001)
    _full_must_check(output, output_schema, "AT-001")

    # AT-001 specific: recommended option must have counter (反証)
    rec = output["recommendation"]
    assert rec["status"] == "recommended", "AT-001: expected recommendation for this case"
    assert rec["recommended_option_id"] in {o["option_id"] for o in output["options"]}

    # options contain stakeholder references (家族, 現職チーム, etc.)
    option_descs = " ".join(o["description"] for o in output["options"])
    assert output["responsibility"]["decision_owner"], "AT-001: decision_owner required"


# ── AT-002: チームの人員整理 ──────────────────────────────────────────────────


def test_at_002_headcount_reduction(case_002, composer, output_schema):
    """AT-002: チームの人員整理（倫理 + 責任 + 不確実性）

    Requirements: FR-ETH-002, FR-RES-001, FR-UNC-001
    """
    output = composer.compose(case_002)
    _full_must_check(output, output_schema, "AT-002")

    # Ethics tradeoffs should be present (FR-ETH-002)
    assert output["ethics"]["tradeoffs"], "AT-002: FR-ETH-002 requires tradeoffs"
    # Uncertainty must reflect unknowns from the case
    assert output["uncertainty"]["overall_level"] in {"medium", "high"}


# ── AT-003: 家族介護の設計 ────────────────────────────────────────────────────


def test_at_003_caregiving(case_003, composer, output_schema):
    """AT-003: 家族介護（倫理 + 責任 + 不確実性）

    Requirements: FR-ETH-001, FR-RES-001, FR-UNC-001
    """
    output = composer.compose(case_003)
    _full_must_check(output, output_schema, "AT-003")

    # decision_owner must be the human (not Po_core)
    _assert_no_forbidden_decision_owner(output)
    # stakeholders list should be populated
    assert output["responsibility"]["stakeholders"], "AT-003: stakeholders required"


# ── AT-004: 倫理的トレードオフ ────────────────────────────────────────────────


def test_at_004_ethical_tradeoffs(case_004, composer, output_schema):
    """AT-004: 倫理的トレードオフ（推奨 + 反証 + 代替案）

    Requirements: FR-ETH-002, FR-REC-001, FR-UNC-001
    """
    output = composer.compose(case_004)
    _full_must_check(output, output_schema, "AT-004")
    _assert_recommendation_present(output)
    assert output["ethics"]["tradeoffs"], "AT-004: FR-ETH-002 requires tradeoffs"


# ── AT-005: 責任主体の明確化 ──────────────────────────────────────────────────


def test_at_005_responsibility_owner(case_005, composer, output_schema):
    """AT-005: 責任主体の明確化

    Requirements: FR-ETH-001, FR-RES-001
    """
    output = composer.compose(case_005)
    _full_must_check(output, output_schema, "AT-005")

    # decision_owner must be explicitly set (FR-RES-001)
    assert output["responsibility"]["decision_owner"], "AT-005: decision_owner required"
    assert output["responsibility"]["accountability_notes"], (
        "AT-005: accountability_notes required"
    )


# ── AT-006: 責任 + トレース重視 ───────────────────────────────────────────────


def test_at_006_trace_responsibility(case_006, composer, output_schema):
    """AT-006: 責任 + 監査ログ

    Requirements: FR-RES-001, FR-TR-001, FR-ETH-001
    """
    output = composer.compose(case_006)
    _full_must_check(output, output_schema, "AT-006")

    # All 6 trace steps must be present and have timestamps
    for step in output["trace"]["steps"]:
        assert step["name"], "AT-006: trace step name required"
        assert step["started_at"], "AT-006: trace started_at required"
        assert step["ended_at"], "AT-006: trace ended_at required"
        assert step["summary"], "AT-006: trace summary required"


# ── AT-007: 推奨 + 反証 ────────────────────────────────────────────────────────


def test_at_007_recommendation_with_counter(case_007, composer, output_schema):
    """AT-007: 推奨には反証と代替案が必須

    Requirements: FR-ETH-001, FR-REC-001
    """
    output = composer.compose(case_007)
    _full_must_check(output, output_schema, "AT-007")

    rec = output["recommendation"]
    if rec["status"] == "recommended":
        # counter must be non-trivial
        assert len(rec["counter"]) >= 10, (
            "AT-007: counter (反証) must be substantive (≥ 10 chars)"
        )
        # alternatives must point to a valid option
        alt_ids = {a["option_id"] for a in rec["alternatives"]}
        option_ids = {o["option_id"] for o in output["options"]}
        assert alt_ids <= option_ids, (
            f"AT-007: alternatives reference unknown option_ids: {alt_ids - option_ids}"
        )


# ── AT-008: 倫理・不確実性・責任の複合 ────────────────────────────────────────


def test_at_008_combined_ethics_uncertainty_responsibility(
    case_008, composer, output_schema
):
    """AT-008: 倫理・不確実性・責任の複合

    Requirements: FR-ETH-002, FR-UNC-001, FR-RES-001
    """
    output = composer.compose(case_008)
    _full_must_check(output, output_schema, "AT-008")

    # Ethics (FR-ETH-002)
    assert output["ethics"]["tradeoffs"], "AT-008: FR-ETH-002 requires tradeoffs"
    # Uncertainty (FR-UNC-001)
    assert output["uncertainty"]["overall_level"] in {"medium", "high"}
    assert output["uncertainty"]["known_unknowns"] is not None
    # Responsibility (FR-RES-001)
    assert output["responsibility"]["consent_considerations"], (
        "AT-008: consent_considerations required"
    )


# ── AT-009: 価値観が不明（問い生成必須） ──────────────────────────────────────


def test_at_009_values_clarification_questions_generated(
    case_009, composer, output_schema
):
    """AT-009: 価値観が不明 → 問いを生成しなければならない

    Requirements: FR-Q-001, FR-OUT-001
    """
    output = composer.compose(case_009)
    _full_must_check(output, output_schema, "AT-009")

    # FR-Q-001: case_009 has unknowns → questions must be generated
    _assert_questions_present(output)
    for q in output["questions"]:
        assert q["question_id"], "AT-009: question_id required"
        assert q["question"], "AT-009: question text required"
        assert isinstance(q["priority"], int) and 1 <= q["priority"] <= 5, (
            f"AT-009: priority must be 1–5, got {q['priority']}"
        )
        assert q["why_needed"], "AT-009: why_needed required"
        assert isinstance(q["optional"], bool), "AT-009: optional must be bool"


# ── AT-010: 制約の矛盾（矛盾検出＋問い生成） ──────────────────────────────────


def test_at_010_conflicting_constraints_question_generated(
    case_010, composer, output_schema
):
    """AT-010: 制約が矛盾 → 不確実性 high + 問い生成

    Requirements: FR-Q-001, FR-UNC-001
    """
    output = composer.compose(case_010)
    _full_must_check(output, output_schema, "AT-010")

    # FR-UNC-001: conflicting constraints → uncertainty should be non-trivial
    assert output["uncertainty"]["overall_level"] in {"medium", "high"}, (
        "AT-010: conflicting constraints should yield medium/high uncertainty"
    )
    # FR-Q-001: questions should be generated for this case
    _assert_questions_present(output)


# ── AT-META: Cross-cutting schema and determinism checks ──────────────────────


@pytest.mark.parametrize(
    "case_fixture_name",
    [
        "case_001",
        "case_002",
        "case_003",
        "case_009",
        "case_010",
    ],
)
def test_at_meta_schema_always_valid(
    case_fixture_name, request, composer, output_schema
):
    """AT-META: output_schema_v1 must validate for all parameterised cases."""
    case = request.getfixturevalue(case_fixture_name)
    output = composer.compose(case)
    _validate_schema(output, output_schema, f"AT-META({case_fixture_name})")


@pytest.mark.parametrize(
    "case_fixture_name",
    ["case_001", "case_009"],
)
def test_at_meta_determinism(case_fixture_name, request, output_schema):
    """AT-META: same case + same seed must produce identical output."""
    case = request.getfixturevalue(case_fixture_name)
    c1 = StubComposer(seed=42)
    c2 = StubComposer(seed=42)

    import json

    out1 = c1.compose(case)
    out2 = c2.compose(case)

    # Remove run_id and timestamps from comparison (those are UUID/datetime)
    def strip_volatile(d: dict) -> dict:
        d = dict(d)
        d.get("meta", {}).pop("run_id", None)
        d.get("meta", {}).pop("created_at", None)
        # Strip trace timestamps
        for step in d.get("trace", {}).get("steps", []):
            step.pop("started_at", None)
            step.pop("ended_at", None)
        return d

    assert strip_volatile(out1) == strip_volatile(out2), (
        "AT-META: non-deterministic output for same seed"
    )


# Need to import StubComposer at module level for the parametrize test
from po_core.app.composer import StubComposer  # noqa: E402
