"""
Tests for W_Ethics Gate ExplanationChain (Phase 3 scaffold).

Validates that GateResult → ExplanationChain transformation works
correctly for all decision types: ALLOW, ALLOW_WITH_REPAIR, REJECT, ESCALATE.
"""

import pytest

from po_core.safety.wethics_gate.explanation import build_explanation_chain
from po_core.safety.wethics_gate.types import (
    Evidence,
    GateDecision,
    GateResult,
    Violation,
)

pytestmark = [pytest.mark.unit, pytest.mark.observability]


class TestExplanationChainAllow:
    """ExplanationChain for ALLOW decisions."""

    def test_allow_no_violations(self):
        result = GateResult(
            decision=GateDecision.ALLOW,
            violations=[],
            explanation="No violations requiring action",
        )
        chain = build_explanation_chain(result)

        assert chain.decision == "allow"
        assert chain.violations == []
        assert chain.repairs == []
        assert chain.drift is None
        assert "passed" in chain.summary.lower()

    def test_allow_to_dict(self):
        result = GateResult(
            decision=GateDecision.ALLOW,
            violations=[],
            explanation="No violations requiring action",
        )
        chain = build_explanation_chain(result)
        d = chain.to_dict()

        assert d["decision"] == "allow"
        assert d["violations"] == []
        assert d["drift"] is None

    def test_allow_to_markdown(self):
        result = GateResult(
            decision=GateDecision.ALLOW,
            violations=[],
            explanation="No violations requiring action",
        )
        chain = build_explanation_chain(result)
        md = chain.to_markdown()

        assert "## W_Ethics Gate Decision" in md
        assert "`allow`" in md


class TestExplanationChainReject:
    """ExplanationChain for REJECT decisions."""

    def test_reject_hard_violation(self):
        violations = [
            Violation(
                code="W0",
                severity=0.9,
                confidence=0.8,
                repairable=False,
                evidence=[
                    Evidence(
                        code="W0",
                        message="Irreversible harm detected",
                        strength=0.9,
                        confidence=0.8,
                        detector_id="keyword_detector",
                    )
                ],
            )
        ]
        result = GateResult(
            decision=GateDecision.REJECT,
            violations=violations,
            explanation="Hard reject: W0 violation with impact=0.72",
        )
        chain = build_explanation_chain(result)

        assert chain.decision == "reject"
        assert len(chain.violations) == 1
        assert chain.violations[0].code == "W0"
        assert chain.violations[0].code_label == "Irreversible Viability Harm"
        assert not chain.violations[0].repairable
        assert len(chain.violations[0].evidence) == 1
        assert "rejected" in chain.summary.lower()

    def test_reject_violation_markdown(self):
        violations = [
            Violation(
                code="W1",
                severity=0.85,
                confidence=0.9,
                repairable=False,
                evidence=[
                    Evidence(
                        code="W1",
                        message="Domination pattern detected",
                        strength=0.85,
                        confidence=0.9,
                        detector_id="keyword_detector",
                    )
                ],
            )
        ]
        result = GateResult(
            decision=GateDecision.REJECT,
            violations=violations,
            explanation="Hard reject: W1",
        )
        chain = build_explanation_chain(result)
        md = chain.to_markdown()

        assert "W1" in md
        assert "Domination" in md
        assert "hard reject" in md


class TestExplanationChainRepair:
    """ExplanationChain for ALLOW_WITH_REPAIR decisions."""

    def test_repair_with_drift(self):
        violations = [
            Violation(
                code="W4",
                severity=0.5,
                confidence=0.7,
                repairable=True,
                evidence=[
                    Evidence(
                        code="W4",
                        message="Structural exclusion pattern",
                        strength=0.5,
                        confidence=0.7,
                        detector_id="keyword_detector",
                    )
                ],
                suggested_repairs=["Add migration plan"],
            )
        ]
        result = GateResult(
            decision=GateDecision.ALLOW_WITH_REPAIR,
            violations=violations,
            repaired_text="repaired output",
            repair_log=["W4_map: 切り捨てる -> 尊重しつつ移行し、包摂する"],
            drift_score=0.15,
            drift_notes="Low drift",
            explanation="Repair succeeded",
        )
        chain = build_explanation_chain(result)

        assert chain.decision == "allow_with_repair"
        assert len(chain.repairs) == 1
        assert "W4_map" in chain.repairs[0].description
        assert chain.drift is not None
        assert chain.drift.drift_score == 0.15
        assert chain.drift.status == "acceptable"
        assert "repair" in chain.summary.lower()

    def test_repair_dict_has_drift(self):
        result = GateResult(
            decision=GateDecision.ALLOW_WITH_REPAIR,
            violations=[],
            repair_log=["test repair"],
            drift_score=0.2,
            explanation="Repair succeeded",
        )
        chain = build_explanation_chain(result)
        d = chain.to_dict()

        assert d["drift"] is not None
        assert d["drift"]["drift_score"] == 0.2
        assert d["drift"]["status"] == "acceptable"


class TestExplanationChainEscalate:
    """ExplanationChain for ESCALATE decisions."""

    def test_escalate_high_drift(self):
        result = GateResult(
            decision=GateDecision.ESCALATE,
            violations=[
                Violation(
                    code="W3",
                    severity=0.4,
                    confidence=0.6,
                    repairable=True,
                )
            ],
            repair_log=["W3_map: lock-in -> interoperability"],
            drift_score=0.45,
            explanation="Repair succeeded but drift requires review: 0.45",
        )
        chain = build_explanation_chain(result)

        assert chain.decision == "escalate"
        assert chain.drift is not None
        assert chain.drift.status == "escalated"
        assert "escalated" in chain.summary.lower()


class TestDriftStepStatus:
    """Drift threshold status classification."""

    def test_acceptable_drift(self):
        result = GateResult(
            decision=GateDecision.ALLOW_WITH_REPAIR,
            drift_score=0.1,
            explanation="ok",
        )
        chain = build_explanation_chain(result)
        assert chain.drift.status == "acceptable"

    def test_escalated_drift(self):
        result = GateResult(
            decision=GateDecision.ESCALATE,
            drift_score=0.5,
            explanation="drift",
        )
        chain = build_explanation_chain(result)
        assert chain.drift.status == "escalated"

    def test_rejected_drift(self):
        result = GateResult(
            decision=GateDecision.REJECT,
            drift_score=0.8,
            explanation="drift too high",
        )
        chain = build_explanation_chain(result)
        assert chain.drift.status == "rejected"


class TestViolationStepLabels:
    """Violation code label mapping."""

    @pytest.mark.parametrize(
        "code,expected_label",
        [
            ("W0", "Irreversible Viability Harm"),
            ("W1", "Domination / Capture"),
            ("W2", "Dignity Violation"),
            ("W3", "Dependency Engineering"),
            ("W4", "Structural Exclusion"),
        ],
    )
    def test_violation_code_labels(self, code, expected_label):
        result = GateResult(
            decision=GateDecision.REJECT,
            violations=[
                Violation(code=code, severity=0.9, confidence=0.9, repairable=False)
            ],
            explanation="test",
        )
        chain = build_explanation_chain(result)
        assert chain.violations[0].code_label == expected_label
