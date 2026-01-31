"""
Unit Tests for W_ethics Gate
=============================

Tests for the W_ethics Gate system including:
- Gate types and data structures
- Violation detection
- Repair mechanisms
- Axis scoring (ΔE metrics)
- Candidate selection (Pareto + MCDA)
"""
import pytest
from typing import List

from po_core.safety.wethics_gate import (
    # Types
    GateDecision,
    GateViolationCode,
    RepairStage,
    AxisScore,
    Violation,
    RepairAction,
    GateResult,
    Candidate,
    SelectionResult,
    AXES,
    AXIS_NAMES,
    # Gate
    WethicsGate,
    create_wethics_gate,
    DefaultViolationDetector,
    DefaultRepairEngine,
    # Metrics
    ContextProfile,
    MetricsEvaluator,
    create_metrics_evaluator,
    # Selection
    CandidateSelector,
    create_candidate_selector,
    pareto_front,
    robust_weight_sampling_rank,
    topsis_rank,
)


class TestGateTypes:
    """Tests for W_ethics Gate type definitions."""

    def test_gate_decision_values(self):
        """Test GateDecision enum values."""
        assert GateDecision.ALLOW.value == "allow"
        assert GateDecision.ALLOW_WITH_REPAIR.value == "allow_with_repair"
        assert GateDecision.REJECT.value == "reject"
        assert GateDecision.ESCALATE.value == "escalate"

    def test_violation_codes(self):
        """Test GateViolationCode enum values."""
        assert GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM.value == "W0"
        assert GateViolationCode.W1_DOMINATION_CAPTURE.value == "W1"
        assert GateViolationCode.W2_DIGNITY_VIOLATION.value == "W2"
        assert GateViolationCode.W3_DEPENDENCY_ENGINEERING.value == "W3"
        assert GateViolationCode.W4_STRUCTURAL_EXCLUSION.value == "W4"

    def test_repair_stages(self):
        """Test RepairStage enum values."""
        assert RepairStage.CONCEPT_MAPPING.value == "concept_mapping"
        assert RepairStage.CONSTRAINT_INJECTION.value == "constraint_injection"
        assert RepairStage.SCOPE_REDUCTION.value == "scope_reduction"
        assert RepairStage.GOAL_REFRAME.value == "goal_reframe"

    def test_axis_score_creation(self):
        """Test AxisScore dataclass."""
        score = AxisScore(value=0.8, confidence=0.9, evidence=["test evidence"])
        assert score.value == 0.8
        assert score.confidence == 0.9
        assert "test evidence" in score.evidence

    def test_axis_score_clamping(self):
        """Test AxisScore clamps values to [0, 1]."""
        score = AxisScore(value=1.5, confidence=-0.2)
        assert score.value == 1.0
        assert score.confidence == 0.0

    def test_violation_impact_score(self):
        """Test Violation impact score calculation."""
        violation = Violation(
            code=GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM,
            severity=0.9,
            confidence=0.8,
            evidence=["test"],
            repairable=False,
        )
        assert violation.impact_score == 0.72  # 0.9 * 0.8

    def test_violation_is_hard(self):
        """Test Violation hard violation detection."""
        hard = Violation(
            code=GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM,
            severity=0.9,
            confidence=0.8,
            evidence=["test"],
            repairable=False,
        )
        soft = Violation(
            code=GateViolationCode.W2_DIGNITY_VIOLATION,
            severity=0.7,
            confidence=0.8,
            evidence=["test"],
            repairable=True,
        )
        assert hard.is_hard_violation is True
        assert soft.is_hard_violation is False

    def test_candidate_creation(self):
        """Test Candidate dataclass."""
        candidate = Candidate(
            cid="test-001",
            text="This is a test proposal",
            meta={"source": "test"},
        )
        assert candidate.cid == "test-001"
        assert "test proposal" in candidate.text
        assert candidate.source_philosopher is None

    def test_candidate_gate_passed(self):
        """Test Candidate gate pass checking."""
        candidate = Candidate(cid="test", text="test")

        # Not evaluated yet
        assert candidate.is_gate_passed() is False

        # ALLOW
        candidate.gate_result = GateResult(decision=GateDecision.ALLOW)
        assert candidate.is_gate_passed() is True

        # ALLOW_WITH_REPAIR
        candidate.gate_result = GateResult(decision=GateDecision.ALLOW_WITH_REPAIR)
        assert candidate.is_gate_passed() is True

        # REJECT
        candidate.gate_result = GateResult(decision=GateDecision.REJECT)
        assert candidate.is_gate_passed() is False


class TestViolationDetection:
    """Tests for violation detection."""

    def test_detector_no_violations(self):
        """Test detector with clean text."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="clean",
            text="A collaborative proposal to improve community health.",
        )
        violations = detector.detect(candidate)
        assert len(violations) == 0

    def test_detector_w0_violation(self):
        """Test detector catches W0 violations."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="w0-test",
            text="This plan will cause irreversible destruction of the ecosystem.",
        )
        violations = detector.detect(candidate)
        w0_violations = [v for v in violations if v.code == GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM]
        assert len(w0_violations) > 0

    def test_detector_w1_violation(self):
        """Test detector catches W1 violations."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="w1-test",
            text="We must dominate all competitors and subjugate the market.",
        )
        violations = detector.detect(candidate)
        w1_violations = [v for v in violations if v.code == GateViolationCode.W1_DOMINATION_CAPTURE]
        assert len(w1_violations) > 0

    def test_detector_w2_violation(self):
        """Test detector catches W2 violations."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="w2-test",
            text="We will deceive users and manipulate without consent.",
        )
        violations = detector.detect(candidate)
        w2_violations = [v for v in violations if v.code == GateViolationCode.W2_DIGNITY_VIOLATION]
        assert len(w2_violations) > 0

    def test_detector_w3_violation(self):
        """Test detector catches W3 violations."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="w3-test",
            text="Create a lock-in strategy with no escape for users.",
        )
        violations = detector.detect(candidate)
        w3_violations = [v for v in violations if v.code == GateViolationCode.W3_DEPENDENCY_ENGINEERING]
        assert len(w3_violations) > 0

    def test_detector_negation_context(self):
        """Test detector reduces confidence for negation context."""
        detector = DefaultViolationDetector()
        candidate = Candidate(
            cid="negation-test",
            text="We must reject and condemn total control strategies.",
        )
        violations = detector.detect(candidate)
        # Should have reduced confidence due to negation
        if violations:
            assert all(v.confidence < 0.6 for v in violations)


class TestRepairEngine:
    """Tests for repair mechanisms."""

    def test_repair_engine_concept_mapping(self):
        """Test concept mapping repairs."""
        engine = DefaultRepairEngine()
        candidate = Candidate(
            cid="repair-test",
            text="We must dominate the market and control all users.",
        )
        violations = [
            Violation(
                code=GateViolationCode.W2_DIGNITY_VIOLATION,
                severity=0.5,
                confidence=0.7,
                evidence=["dominate"],
                repairable=True,
            )
        ]

        result = engine.repair(candidate, violations)
        assert result is not None
        repaired_text, repairs = result
        assert "collaborate" in repaired_text.lower() or "coordinate" in repaired_text.lower()

    def test_repair_engine_constraint_injection(self):
        """Test constraint injection repairs."""
        engine = DefaultRepairEngine()
        candidate = Candidate(
            cid="constraint-test",
            text="The system collects user data.",
        )
        violations = [
            Violation(
                code=GateViolationCode.W3_DEPENDENCY_ENGINEERING,
                severity=0.5,
                confidence=0.7,
                evidence=["data collection"],
                repairable=True,
            )
        ]

        result = engine.repair(candidate, violations)
        assert result is not None
        repaired_text, repairs = result
        # Should have injected constraints
        assert any(r.stage == RepairStage.CONSTRAINT_INJECTION for r in repairs)


class TestWethicsGate:
    """Tests for the main WethicsGate class."""

    def test_gate_creation(self):
        """Test WethicsGate creation with defaults."""
        gate = WethicsGate()
        assert gate.tau_reject == 0.6
        assert gate.tau_repair == 0.3
        assert gate.max_repairs == 2

    def test_gate_factory(self):
        """Test gate factory function."""
        gate = create_wethics_gate(tau_reject=0.5, max_repairs=3)
        assert gate.tau_reject == 0.5
        assert gate.max_repairs == 3

    def test_gate_allows_clean_candidate(self):
        """Test gate allows clean candidates."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="clean",
            text="A proposal to collaborate on community health improvements.",
        )
        result = gate.check(candidate)
        assert result.decision == GateDecision.ALLOW

    def test_gate_rejects_w0(self):
        """Test gate rejects W0 violations."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w0",
            text="Annihilate all competing species and cause extinction.",
        )
        result = gate.check(candidate)
        assert result.decision == GateDecision.REJECT

    def test_gate_rejects_w1(self):
        """Test gate rejects W1 violations."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w1",
            text="We must subjugate the population and enforce absolute power.",
        )
        result = gate.check(candidate)
        assert result.decision == GateDecision.REJECT

    def test_gate_repairs_w2(self):
        """Test gate repairs W2 violations."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w2",
            text="We will dominate users and control their choices.",
        )
        result = gate.check(candidate)
        # Should be repaired (W2 is repairable via concept mapping)
        assert result.decision in (GateDecision.ALLOW_WITH_REPAIR, GateDecision.ALLOW)
        if result.decision == GateDecision.ALLOW_WITH_REPAIR:
            assert result.repaired_text is not None

    def test_gate_batch_check(self):
        """Test gate batch checking."""
        gate = WethicsGate()
        candidates = [
            Candidate(cid="c1", text="A collaborative community project."),
            Candidate(cid="c2", text="Dominate and subjugate all markets."),
            Candidate(cid="c3", text="Partner with stakeholders."),
        ]
        results = gate.check_batch(candidates)
        assert len(results) == 3
        # First and third should pass, second should fail
        assert results[0][1].decision in (GateDecision.ALLOW, GateDecision.ALLOW_WITH_REPAIR)
        assert results[2][1].decision in (GateDecision.ALLOW, GateDecision.ALLOW_WITH_REPAIR)


class TestMetrics:
    """Tests for ΔE metrics system."""

    def test_context_profile_default(self):
        """Test default context profile."""
        profile = ContextProfile.default()
        assert profile.name == "default"
        assert "A" in profile.axis_profiles
        assert profile.axis_profiles["A"].e_min < profile.axis_profiles["A"].e_target

    def test_context_profile_disaster(self):
        """Test disaster context profile."""
        profile = ContextProfile.disaster()
        assert profile.name == "disaster"
        # Disaster should have higher safety requirements
        assert profile.axis_profiles["A"].e_min > ContextProfile.default().axis_profiles["A"].e_min

    def test_evaluator_creation(self):
        """Test MetricsEvaluator creation."""
        evaluator = MetricsEvaluator()
        assert "A" in evaluator.scorers
        assert evaluator.context_profile is not None

    def test_evaluator_factory(self):
        """Test evaluator factory function."""
        evaluator = create_metrics_evaluator("disaster")
        assert evaluator.context_profile.name == "disaster"

    def test_score_candidate(self):
        """Test scoring a candidate."""
        evaluator = MetricsEvaluator()
        candidate = Candidate(
            cid="score-test",
            text="A safe and fair proposal with privacy protections.",
        )
        scores = evaluator.score_candidate(candidate)
        assert len(scores) == 5  # A, B, C, D, E
        for axis in AXES:
            assert axis in scores
            assert 0.0 <= scores[axis].value <= 1.0
            assert 0.0 <= scores[axis].confidence <= 1.0

    def test_compute_delta_plus(self):
        """Test delta+ computation."""
        evaluator = MetricsEvaluator()
        scores = {
            "A": AxisScore(value=0.6, confidence=0.8),
            "B": AxisScore(value=0.5, confidence=0.8),
            "C": AxisScore(value=0.7, confidence=0.8),
            "D": AxisScore(value=0.8, confidence=0.8),
            "E": AxisScore(value=0.4, confidence=0.8),
        }
        delta = evaluator.compute_delta_plus(scores)
        # Delta should be positive where score < target
        for axis in AXES:
            target = evaluator.context_profile.axis_profiles[axis].e_target
            expected = max(0.0, target - scores[axis].value)
            assert abs(delta[axis] - expected) < 0.001

    def test_compute_min_violation(self):
        """Test minimum violation computation."""
        evaluator = MetricsEvaluator()
        scores = {
            "A": AxisScore(value=0.3, confidence=0.8),  # Below e_min
            "B": AxisScore(value=0.8, confidence=0.8),
            "C": AxisScore(value=0.8, confidence=0.8),
            "D": AxisScore(value=0.8, confidence=0.8),
            "E": AxisScore(value=0.8, confidence=0.8),
        }
        violations = evaluator.compute_min_violation(scores)
        # A should have a violation (0.3 < 0.4 min)
        assert violations["A"] > 0
        # Others should be fine
        assert violations["B"] == 0
        assert evaluator.has_min_violation(scores) is True

    def test_compute_d2(self):
        """Test L2 distance computation."""
        evaluator = MetricsEvaluator()
        scores = {axis: AxisScore(value=0.5, confidence=0.8) for axis in AXES}
        d2 = evaluator.compute_d2(scores)
        assert d2 >= 0

    def test_compute_d_inf(self):
        """Test L-infinity distance computation."""
        evaluator = MetricsEvaluator()
        scores = {axis: AxisScore(value=0.5, confidence=0.8) for axis in AXES}
        d_inf = evaluator.compute_d_inf(scores)
        assert d_inf >= 0


class TestParetoFront:
    """Tests for Pareto front computation."""

    def test_pareto_single_candidate(self):
        """Test Pareto front with single candidate."""
        candidate = Candidate(cid="c1", text="test")
        candidate.scores = {axis: AxisScore(value=0.5, confidence=0.8) for axis in AXES}
        front = pareto_front([candidate])
        assert len(front) == 1

    def test_pareto_dominant_candidate(self):
        """Test Pareto front with one dominant candidate."""
        c1 = Candidate(cid="c1", text="test1")
        c1.scores = {axis: AxisScore(value=0.9, confidence=0.8) for axis in AXES}

        c2 = Candidate(cid="c2", text="test2")
        c2.scores = {axis: AxisScore(value=0.3, confidence=0.8) for axis in AXES}

        front = pareto_front([c1, c2])
        assert len(front) == 1
        assert front[0].cid == "c1"

    def test_pareto_tradeoff_candidates(self):
        """Test Pareto front with trade-off candidates."""
        c1 = Candidate(cid="c1", text="test1")
        c1.scores = {
            "A": AxisScore(value=0.9, confidence=0.8),
            "B": AxisScore(value=0.3, confidence=0.8),
            "C": AxisScore(value=0.5, confidence=0.8),
            "D": AxisScore(value=0.5, confidence=0.8),
            "E": AxisScore(value=0.5, confidence=0.8),
        }

        c2 = Candidate(cid="c2", text="test2")
        c2.scores = {
            "A": AxisScore(value=0.3, confidence=0.8),
            "B": AxisScore(value=0.9, confidence=0.8),
            "C": AxisScore(value=0.5, confidence=0.8),
            "D": AxisScore(value=0.5, confidence=0.8),
            "E": AxisScore(value=0.5, confidence=0.8),
        }

        front = pareto_front([c1, c2])
        # Both should be in Pareto front (trade-off)
        assert len(front) == 2


class TestMCDA:
    """Tests for MCDA selection methods."""

    def test_robust_weight_sampling(self):
        """Test robust weight sampling ranking."""
        evaluator = MetricsEvaluator()

        c1 = Candidate(cid="c1", text="test1")
        c1.scores = {axis: AxisScore(value=0.8, confidence=0.8) for axis in AXES}

        c2 = Candidate(cid="c2", text="test2")
        c2.scores = {axis: AxisScore(value=0.4, confidence=0.8) for axis in AXES}

        ranked = robust_weight_sampling_rank([c1, c2], evaluator, seed=42)
        assert len(ranked) == 2
        # c1 should win with high probability
        assert ranked[0][0].cid == "c1"
        assert ranked[0][1] > 0.5

    def test_topsis_ranking(self):
        """Test TOPSIS ranking."""
        evaluator = MetricsEvaluator()

        c1 = Candidate(cid="c1", text="test1")
        c1.scores = {axis: AxisScore(value=0.8, confidence=0.8) for axis in AXES}

        c2 = Candidate(cid="c2", text="test2")
        c2.scores = {axis: AxisScore(value=0.4, confidence=0.8) for axis in AXES}

        ranked = topsis_rank([c1, c2], evaluator)
        assert len(ranked) == 2
        # c1 should be closer to ideal
        assert ranked[0][0].cid == "c1"


class TestCandidateSelector:
    """Tests for the full selection pipeline."""

    def test_selector_creation(self):
        """Test CandidateSelector creation."""
        selector = CandidateSelector()
        assert selector.gate is not None
        assert selector.evaluator is not None

    def test_selector_factory(self):
        """Test selector factory function."""
        selector = create_candidate_selector("disaster", "topsis")
        assert selector.evaluator.context_profile.name == "disaster"
        assert selector.mcda_method == "topsis"

    def test_selector_all_rejected(self):
        """Test selection when all candidates rejected."""
        selector = CandidateSelector()
        candidates = [
            Candidate(cid="c1", text="Annihilate all competition through extinction."),
            Candidate(cid="c2", text="Subjugate all markets with absolute power."),
        ]
        result = selector.select(candidates)
        assert result.selected_id is None
        assert len(result.rejected) == 2

    def test_selector_single_winner(self):
        """Test selection with clear winner."""
        selector = CandidateSelector()
        candidates = [
            Candidate(cid="c1", text="A safe, fair, and inclusive community project."),
            Candidate(cid="c2", text="A risky scheme with potential harm."),
        ]
        result = selector.select(candidates)
        # Should have a selection (at least one passes gate)
        assert result.pareto_set_ids  # Should have candidates in pareto set

    def test_selector_with_details(self):
        """Test selection with additional details."""
        selector = CandidateSelector()
        candidates = [
            Candidate(cid="c1", text="A collaborative and transparent proposal."),
            Candidate(cid="c2", text="Another fair proposal with privacy focus."),
        ]
        result, details = selector.select_with_details(candidates)
        assert "total_candidates" in details
        assert details["total_candidates"] == 2


class TestIntegration:
    """Integration tests for the full W_ethics Gate pipeline."""

    def test_full_pipeline(self):
        """Test the complete pipeline from candidates to selection."""
        # Create candidates representing philosopher proposals
        candidates = [
            Candidate(
                cid="utilitarian",
                text="Maximize overall happiness through fair resource distribution.",
                source_philosopher="Mill",
            ),
            Candidate(
                cid="deontological",
                text="Follow universal principles of respect and dignity for all.",
                source_philosopher="Kant",
            ),
            Candidate(
                cid="problematic",
                text="Dominate competitors and subjugate the market.",
                source_philosopher="Machiavelli",
            ),
        ]

        selector = create_candidate_selector("default", "robust-weight")
        result = selector.select(candidates)

        # Problematic candidate should be rejected
        rejected_ids = [r["id"] for r in result.rejected]
        assert "problematic" in rejected_ids

        # Should have at least one candidate in Pareto set
        assert len(result.pareto_set_ids) > 0

    def test_repair_flow(self):
        """Test that repairable violations get repaired."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="repairable",
            text="We need to control users to protect them.",
        )

        result = gate.check(candidate)
        # Should either pass or be repaired (not rejected for W2-W4)
        assert result.decision in (
            GateDecision.ALLOW,
            GateDecision.ALLOW_WITH_REPAIR,
        )

    def test_context_sensitivity(self):
        """Test that different contexts affect selection."""
        candidates = [
            Candidate(
                cid="safe-focused",
                text="Prioritize safety above all with verified safeguards.",
            ),
            Candidate(
                cid="privacy-focused",
                text="Encrypt all data with strict privacy protections.",
            ),
        ]

        # Score with default context
        default_evaluator = create_metrics_evaluator("default")
        for c in candidates:
            c.scores = default_evaluator.score_candidate(c)

        # Score with disaster context (safety-heavy)
        disaster_evaluator = create_metrics_evaluator("disaster")
        candidates_disaster = [
            Candidate(cid=c.cid, text=c.text) for c in candidates
        ]
        for c in candidates_disaster:
            c.scores = disaster_evaluator.score_candidate(c)

        # In disaster context, safety-focused should score relatively higher on A
        default_safe_a = candidates[0].scores["A"].value
        disaster_safe_a = candidates_disaster[0].scores["A"].value
        # Both should have positive safety scores (content mentions safety)
        assert default_safe_a > 0
        assert disaster_safe_a > 0
