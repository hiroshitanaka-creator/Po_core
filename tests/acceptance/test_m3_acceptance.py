# SPDX-License-Identifier: AGPL-3.0-or-later
"""M3 Acceptance Tests.

REQ-VALUES-001  Values Clarification Pack v1 (values_empty)
REQ-PLAN-001    Two-Track Plan (unknowns × time pressure)
REQ-SESSION-001 Session replay E2E golden contract
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from po_core.app.composer import StubComposer
from po_core.app.session_engine import apply_session_answers, load_session_answers
from po_core.app.values_clarifier import needs_values_clarification
from po_core.app.plan_builder import needs_two_track_plan

_SCENARIOS_DIR = Path(__file__).parent.parent.parent / "scenarios"
_GOLDEN_DIR = Path(__file__).parent / "scenarios"

# ── Helpers ────────────────────────────────────────────────────────────────


def _load_case(name: str) -> dict:
    with (_SCENARIOS_DIR / name).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _compose(case: dict) -> dict:
    return StubComposer(seed=42).compose(case)


def _canonicalize(output: dict) -> dict:
    canonical = json.loads(json.dumps(output, ensure_ascii=False))
    canonical.get("meta", {}).pop("created_at", None)
    for step in canonical.get("trace", {}).get("steps", []):
        step.pop("started_at", None)
        step.pop("ended_at", None)
    return canonical


# ── REQ-VALUES-001: Values Clarification Pack ──────────────────────────────


@pytest.mark.acceptance
class TestValuesClArification:
    """AT-M3-VCV: Values Clarification Pack when values is empty."""

    def _get_case009(self):
        return _load_case("case_009.yaml")

    def test_values_empty_triggers_vc(self):
        """needs_values_clarification returns True for empty values."""
        case = self._get_case009()
        assert needs_values_clarification(
            case
        ), "values=[] should trigger clarification"

    def test_questions_non_empty(self):
        """AT-Q-001: questions.length >= 1 when values is empty."""
        case = self._get_case009()
        output = _compose(case)
        assert len(output["questions"]) >= 1

    def test_questions_max_5(self):
        """AT-Q-001: questions.length <= 5."""
        case = self._get_case009()
        output = _compose(case)
        assert len(output["questions"]) <= 5

    def test_questions_have_why_needed(self):
        """AT-Q-001b: each question has non-empty why_needed."""
        case = self._get_case009()
        output = _compose(case)
        for q in output["questions"]:
            assert q.get("why_needed"), f"why_needed missing for {q.get('question_id')}"

    def test_questions_have_priority(self):
        """AT-Q-001c: each question has priority in 1..5."""
        case = self._get_case009()
        output = _compose(case)
        for q in output["questions"]:
            assert 1 <= q["priority"] <= 5

    def test_at_least_one_non_optional_question(self):
        """AT-Q-001d: at least one question with optional=False."""
        case = self._get_case009()
        output = _compose(case)
        assert any(not q.get("optional", True) for q in output["questions"])

    def test_vc_questions_have_q_vc_prefix(self):
        """Values clarification questions start with q_vc_."""
        case = self._get_case009()
        output = _compose(case)
        ids = [q["question_id"] for q in output["questions"]]
        assert any(
            qid.startswith("q_vc_") for qid in ids
        ), f"Expected q_vc_ questions; got {ids}"

    def test_action_plan_is_vc_pack(self):
        """REQ-VALUES-001: opt_001 action_plan has values clarification steps."""
        case = self._get_case009()
        output = _compose(case)
        opt1 = output["options"][0]
        steps = [s["step"] for s in opt1["action_plan"]]
        # Should contain the keyword "ステップ"
        assert any(
            "ステップ" in s for s in steps
        ), f"Expected VC action plan; got steps: {steps[:2]}"

    def test_ethics_guardrail_present(self):
        """REQ-VALUES-001: ethics.guardrails includes no-recommendation-without-values rule."""
        case = self._get_case009()
        output = _compose(case)
        guardrails = output["ethics"]["guardrails"]
        assert any(
            "価値軸" in g for g in guardrails
        ), f"Expected values-empty guardrail; got {guardrails}"

    def test_schema_valid(self, validate_output_schema):
        """AT-OUT-001: output conforms to output_schema_v1.json."""
        case = self._get_case009()
        output = _compose(case)
        validate_output_schema(output, "M3-schema-check")


# ── REQ-PLAN-001: Two-Track Plan ────────────────────────────────────────────


@pytest.mark.acceptance
class TestTwoTrackPlan:
    """AT-M3-TTP: Two-Track Plan when unknowns + time pressure (≤30 days)."""

    def _urgent_case(self):
        """Case with unknowns + deadline 20 days from now."""
        import datetime

        deadline = (datetime.date.today() + datetime.timedelta(days=20)).isoformat()
        return {
            "case_id": "test_two_track",
            "title": "緊急判断テスト",
            "problem": "すぐに決断が必要な状況",
            "constraints": ["コスト最小化"],
            "values": ["自律", "安全"],
            "deadline": deadline,
            "stakeholders": [
                {"name": "自分", "role": "意思決定主体", "impact": "直接影響"}
            ],
            "unknowns": ["予算の上限", "法的リスクの有無"],
        }

    def test_needs_two_track_when_urgent(self):
        """needs_two_track_plan returns True when unknowns + deadline ≤30d."""
        case = self._urgent_case()
        assert needs_two_track_plan(case)

    def test_action_plan_has_track_labels(self):
        """REQ-PLAN-001: opt_001.action_plan contains Track A and Track B steps."""
        case = self._urgent_case()
        output = _compose(case)
        opt1 = output["options"][0]
        steps = [s["step"] for s in opt1["action_plan"]]
        has_track_a = any("Track A" in s for s in steps)
        has_track_b = any("Track B" in s for s in steps)
        assert has_track_a and has_track_b, f"Expected Track A + B; got: {steps[:3]}"

    def test_action_plan_max_5_steps(self):
        """REQ-PLAN-001: action_plan max 5 steps."""
        case = self._urgent_case()
        output = _compose(case)
        assert len(output["options"][0]["action_plan"]) <= 5

    def test_schema_valid(self, validate_output_schema):
        """AT-OUT-001: output conforms to output_schema_v1.json."""
        case = self._urgent_case()
        output = _compose(case)
        validate_output_schema(output, "M3-schema-check")


# ── REQ-SESSION-001: Session Replay E2E ────────────────────────────────────


@pytest.mark.acceptance
class TestSessionReplay:
    """AT-M3-SES: Session replay determinism and golden contract."""

    _BASE_CASE_FILE = "session_001_base.yaml"
    _ANSWERS_FILE = "session_001_answers.json"
    _GOLDEN_FILE = _GOLDEN_DIR / "session_001_expected.json"

    def _load_artifacts(self):
        base_case = _load_case(self._BASE_CASE_FILE)
        answers = load_session_answers(str(_GOLDEN_DIR / self._ANSWERS_FILE))
        return base_case, answers

    def test_patch_applies_values(self):
        """JSON Patch correctly adds values to the base case."""
        base_case, answers = self._load_artifacts()
        patched = apply_session_answers(base_case, answers)
        assert len(patched["values"]) >= 2
        assert "自己成長" in patched["values"]

    def test_patch_applies_constraints(self):
        """JSON Patch correctly adds constraint to the base case."""
        base_case, answers = self._load_artifacts()
        patched = apply_session_answers(base_case, answers)
        assert len(patched["constraints"]) > len(base_case["constraints"])

    def test_patched_output_has_recommendation(self):
        """After patch, values are non-empty so recommendation is generated."""
        base_case, answers = self._load_artifacts()
        patched = apply_session_answers(base_case, answers)
        output = _compose(patched)
        assert output["recommendation"]["status"] == "recommended"

    def test_base_output_no_recommendation(self):
        """Base case (no values) produces no_recommendation."""
        base_case, _ = self._load_artifacts()
        output = _compose(base_case)
        assert output["recommendation"]["status"] == "no_recommendation"

    def test_session_replay_determinism(self):
        """Same patch + same seed → identical output (REQ-SESSION-001)."""
        base_case, answers = self._load_artifacts()
        patched1 = apply_session_answers(base_case, answers)
        patched2 = apply_session_answers(base_case, answers)
        out1 = _canonicalize(_compose(patched1))
        out2 = _canonicalize(_compose(patched2))
        assert out1 == out2

    def test_session_golden_match(self):
        """REQ-SESSION-001: session replay matches golden file."""
        if not self._GOLDEN_FILE.exists():
            pytest.skip("session golden file not yet generated")
        with self._GOLDEN_FILE.open(encoding="utf-8") as f:
            golden = json.load(f)
        base_case, answers = self._load_artifacts()
        patched = apply_session_answers(base_case, answers)
        output = _canonicalize(_compose(patched))
        assert output == golden["expected"], (
            f"Session replay output differs from golden.\nKeys differ: "
            f"{set(output.keys()) ^ set(golden['expected'].keys())}"
        )

    def test_schema_valid_after_patch(self, validate_output_schema):
        """AT-OUT-001: patched output conforms to output_schema_v1.json."""
        base_case, answers = self._load_artifacts()
        patched = apply_session_answers(base_case, answers)
        output = _compose(patched)
        validate_output_schema(output, "M3-schema-check")
