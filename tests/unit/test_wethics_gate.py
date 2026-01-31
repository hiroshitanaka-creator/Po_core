"""
Unit Tests for W_ethics Gate
=============================

Tests for the W_ethics Gate system including:
- Gate types and data structures
- Evidence/Violation detection and aggregation
- Semantic drift detection
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
    Evidence,
    Violation,
    GateConfig,
    AxisScore,
    GateResult,
    Candidate,
    SelectionResult,
    AXES,
    AXIS_NAMES,
    # Detectors
    ViolationDetector,
    DetectorRegistry,
    KeywordViolationDetector,
    EnglishKeywordViolationDetector,
    aggregate_evidence_to_violations,
    create_default_registry,
    # Semantic Drift
    DriftReport,
    semantic_drift,
    # Gate
    RuleBasedRepairEngine,
    WethicsGate,
    create_wethics_gate,
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

    def test_evidence_creation(self):
        """Test Evidence dataclass."""
        evidence = Evidence(
            code="W1",
            message="Detected domination pattern",
            strength=0.8,
            confidence=0.9,
            detector_id="test",
            span=(10, 20),
            tags=["keyword"],
        )
        assert evidence.code == "W1"
        assert evidence.strength == 0.8
        assert evidence.detector_id == "test"

    def test_evidence_clamping(self):
        """Test Evidence clamps values to [0, 1]."""
        evidence = Evidence(
            code="W1",
            message="test",
            strength=1.5,
            confidence=-0.2,
            detector_id="test",
        )
        assert evidence.strength == 1.0
        assert evidence.confidence == 0.0

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
            code="W0",
            severity=0.9,
            confidence=0.8,
            repairable=False,
        )
        assert abs(violation.impact_score - 0.72) < 0.001  # 0.9 * 0.8

    def test_violation_is_hard(self):
        """Test Violation hard violation detection."""
        hard = Violation(code="W0", severity=0.9, confidence=0.8, repairable=False)
        soft = Violation(code="W2", severity=0.7, confidence=0.8, repairable=True)
        assert hard.is_hard_violation is True
        assert soft.is_hard_violation is False

    def test_gate_config(self):
        """Test GateConfig dataclass."""
        config = GateConfig(
            tau_reject=0.5,
            tau_repair=0.2,
            max_repairs=3,
            tau_drift_reject=0.8,
            tau_drift_escalate=0.5,
        )
        assert config.tau_reject == 0.5
        assert config.max_repairs == 3

    def test_candidate_creation(self):
        """Test Candidate dataclass."""
        candidate = Candidate(
            cid="test-001",
            text="This is a test proposal",
            meta={"source": "test", "goal": "improve community health"},
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


class TestEvidenceAggregation:
    """Tests for evidence aggregation into violations."""

    def test_aggregate_single_evidence(self):
        """Test aggregating single evidence piece."""
        evs = [
            Evidence(
                code="W1",
                message="test",
                strength=0.8,
                confidence=0.9,
                detector_id="test",
            )
        ]
        violations = aggregate_evidence_to_violations(evs)
        assert len(violations) == 1
        assert violations[0].code == "W1"
        assert violations[0].severity == 0.8
        assert violations[0].confidence == 0.9

    def test_aggregate_multiple_evidence_same_code(self):
        """Test aggregating multiple evidence pieces for same violation code."""
        evs = [
            Evidence(code="W1", message="test1", strength=0.5, confidence=0.6, detector_id="a"),
            Evidence(code="W1", message="test2", strength=0.5, confidence=0.6, detector_id="b"),
        ]
        violations = aggregate_evidence_to_violations(evs)
        assert len(violations) == 1
        # Probabilistic OR: 1 - (1-0.5)*(1-0.5) = 0.75
        assert violations[0].severity == 0.75
        assert violations[0].confidence == 0.75

    def test_aggregate_multiple_codes(self):
        """Test aggregating evidence with different codes."""
        evs = [
            Evidence(code="W1", message="test1", strength=0.8, confidence=0.9, detector_id="a"),
            Evidence(code="W2", message="test2", strength=0.6, confidence=0.7, detector_id="b"),
        ]
        violations = aggregate_evidence_to_violations(evs)
        assert len(violations) == 2
        codes = [v.code for v in violations]
        assert "W1" in codes
        assert "W2" in codes

    def test_violation_order(self):
        """Test violations are ordered W0..W4."""
        evs = [
            Evidence(code="W3", message="test", strength=0.5, confidence=0.5, detector_id="a"),
            Evidence(code="W0", message="test", strength=0.5, confidence=0.5, detector_id="b"),
            Evidence(code="W2", message="test", strength=0.5, confidence=0.5, detector_id="c"),
        ]
        violations = aggregate_evidence_to_violations(evs)
        codes = [v.code for v in violations]
        assert codes == ["W0", "W2", "W3"]


class TestDetectors:
    """Tests for violation detectors."""

    def test_detector_registry(self):
        """Test detector registry."""
        registry = DetectorRegistry()
        detector = KeywordViolationDetector()
        registry.register(detector)
        assert detector.detector_id in registry.list_ids()
        assert len(registry.get_all()) == 1

    def test_default_registry(self):
        """Test default registry has both detectors."""
        registry = create_default_registry()
        ids = registry.list_ids()
        assert "keyword_ja" in ids
        assert "keyword_en" in ids

    def test_japanese_detector_no_violations(self):
        """Test Japanese detector with clean text."""
        detector = KeywordViolationDetector()
        candidate = Candidate(
            cid="clean",
            text="コミュニティの健康を改善するための協力的な提案です。",
        )
        evidence = detector.detect(candidate)
        assert len(evidence) == 0

    def test_japanese_detector_w1_violation(self):
        """Test Japanese detector catches W1 violations."""
        detector = KeywordViolationDetector()
        candidate = Candidate(
            cid="w1-test",
            text="市場を支配し、競合を排除する戦略です。",
        )
        evidence = detector.detect(candidate)
        w1_evidence = [e for e in evidence if e.code == "W1"]
        assert len(w1_evidence) > 0

    def test_english_detector_no_violations(self):
        """Test English detector with clean text."""
        detector = EnglishKeywordViolationDetector()
        candidate = Candidate(
            cid="clean",
            text="A collaborative proposal to improve community health.",
        )
        evidence = detector.detect(candidate)
        assert len(evidence) == 0

    def test_english_detector_w1_violation(self):
        """Test English detector catches W1 violations."""
        detector = EnglishKeywordViolationDetector()
        candidate = Candidate(
            cid="w1-test",
            text="We must dominate all competitors and subjugate the market.",
        )
        evidence = detector.detect(candidate)
        w1_evidence = [e for e in evidence if e.code == "W1"]
        assert len(w1_evidence) > 0

    def test_english_detector_w3_violation(self):
        """Test English detector catches W3 lock-in violations."""
        detector = EnglishKeywordViolationDetector()
        candidate = Candidate(
            cid="w3-test",
            text="Create a lock-in strategy with no escape for users.",
        )
        evidence = detector.detect(candidate)
        w3_evidence = [e for e in evidence if e.code == "W3"]
        assert len(w3_evidence) > 0


class TestSemanticDrift:
    """Tests for semantic drift detection."""

    def test_no_drift_identical(self):
        """Test no drift for identical text."""
        report = semantic_drift("Hello world", "Hello world")
        assert report.drift == 0.0

    def test_drift_polarity_flip(self):
        """Test drift detection for polarity flip."""
        before = "We must dominate the market."
        after = "We must collaborate with the market."
        report = semantic_drift(before, after)
        assert report.drift > 0.2  # Should detect polarity change

    def test_drift_concept_change(self):
        """Test drift detection for concept change."""
        before = "Focus on user acquisition and growth."
        after = "Focus on environmental sustainability and conservation."
        report = semantic_drift(before, after)
        assert report.drift > 0.3  # Should detect concept change

    def test_drift_with_goal(self):
        """Test drift with explicit goal."""
        before = "Implement user tracking."
        after = "Implement user support with privacy."
        report = semantic_drift(
            before, after,
            before_goal="track users",
            after_goal="support users",
        )
        assert report.drift > 0.2

    def test_drift_report_contents(self):
        """Test DriftReport contains expected fields."""
        report = semantic_drift("before text", "after text")
        assert isinstance(report.drift, float)
        assert isinstance(report.notes, str)
        assert isinstance(report.key_concepts_before, list)
        assert isinstance(report.key_concepts_after, list)
        assert isinstance(report.lost_concepts, list)
        assert isinstance(report.added_concepts, list)


class TestRepairEngine:
    """Tests for repair mechanisms."""

    def test_repair_w4_exclusion(self):
        """Test W4 exclusion repair (Japanese)."""
        engine = RuleBasedRepairEngine()
        text = "既存ユーザーを切り捨てる新戦略"
        repaired, log = engine.repair(text, ["W4"])
        assert "移行" in repaired or "包摂" in repaired
        assert len(log) > 0

    def test_repair_w3_lockin(self):
        """Test W3 lock-in repair (Japanese)."""
        engine = RuleBasedRepairEngine()
        text = "ユーザーを囲い込みロックインする設計"
        repaired, log = engine.repair(text, ["W3"])
        assert "選択肢" in repaired or "相互運用性" in repaired
        assert len(log) > 0

    def test_repair_w2_manipulation(self):
        """Test W2 manipulation repair (Japanese)."""
        engine = RuleBasedRepairEngine()
        text = "ユーザーを操作して購買に誘導する"
        repaired, log = engine.repair(text, ["W2"])
        assert "合意" in repaired or "尊厳" in repaired
        assert len(log) > 0

    def test_repair_english(self):
        """Test repair for English text."""
        engine = RuleBasedRepairEngine()
        text = "Create lock-in for users with no escape."
        repaired, log = engine.repair(text, ["W3"])
        assert "interoperability" in repaired.lower() or "portability" in repaired.lower()
        assert len(log) > 0

    def test_repair_no_violations(self):
        """Test repair with no applicable violations."""
        engine = RuleBasedRepairEngine()
        text = "A collaborative proposal."
        repaired, log = engine.repair(text, [])
        assert repaired == text
        assert len(log) == 0


class TestWethicsGate:
    """Tests for the main WethicsGate class."""

    def test_gate_creation(self):
        """Test WethicsGate creation with defaults."""
        gate = WethicsGate()
        assert gate.config.tau_reject == 0.6
        assert gate.config.tau_repair == 0.3
        assert gate.config.max_repairs == 2

    def test_gate_factory(self):
        """Test gate factory function."""
        gate = create_wethics_gate(tau_reject=0.5, max_repairs=3)
        assert gate.config.tau_reject == 0.5
        assert gate.config.max_repairs == 3

    def test_gate_allows_clean_candidate(self):
        """Test gate allows clean candidates."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="clean",
            text="A proposal to collaborate on community health improvements.",
        )
        result = gate.check(candidate)
        assert result.decision == GateDecision.ALLOW

    def test_gate_rejects_w1(self):
        """Test gate rejects W1 domination violations."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w1",
            text="We must dominate all competitors and subjugate the market with absolute power.",
        )
        result = gate.check(candidate)
        assert result.decision == GateDecision.REJECT

    def test_gate_repairs_w3(self):
        """Test gate repairs W3 lock-in violations."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w3",
            text="Create a lock-in strategy for user data.",
        )
        result = gate.check(candidate)
        # Should be repaired (W3 is repairable)
        assert result.decision in (GateDecision.ALLOW_WITH_REPAIR, GateDecision.ALLOW)
        if result.decision == GateDecision.ALLOW_WITH_REPAIR:
            assert result.repaired_text is not None
            assert len(result.repair_log) > 0

    def test_gate_drift_check(self):
        """Test gate includes drift score in result."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w3",
            text="ユーザーを囲い込みロックインする",
            meta={"goal": "maximize user retention"},
        )
        result = gate.check(candidate)
        if result.decision == GateDecision.ALLOW_WITH_REPAIR:
            assert result.drift_score is not None
            assert result.drift_notes is not None

    def test_gate_batch_check(self):
        """Test gate batch checking."""
        gate = WethicsGate()
        candidates = [
            Candidate(cid="c1", text="A collaborative community project."),
            Candidate(cid="c2", text="Dominate and subjugate all markets with absolute power."),
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


class TestIntegration:
    """Integration tests for the full W_ethics Gate pipeline."""

    def test_full_pipeline(self):
        """Test the complete pipeline from candidates to selection."""
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
                text="Dominate competitors and subjugate the market with absolute power.",
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
            text="Create a lock-in strategy for user data.",
        )

        result = gate.check(candidate)
        # Should either pass or be repaired (not rejected for W3)
        assert result.decision in (
            GateDecision.ALLOW,
            GateDecision.ALLOW_WITH_REPAIR,
        )

    def test_semantic_drift_integration(self):
        """Test semantic drift is checked during repair."""
        gate = WethicsGate()
        candidate = Candidate(
            cid="w3",
            text="ユーザーを囲い込みロックインする戦略",
            meta={"goal": "ユーザー維持"},
        )
        result = gate.check(candidate)
        if result.decision == GateDecision.ALLOW_WITH_REPAIR:
            # Drift should be calculated
            assert result.drift_score is not None
            assert 0.0 <= result.drift_score <= 1.0
