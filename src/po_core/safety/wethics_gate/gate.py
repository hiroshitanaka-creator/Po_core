"""
W_ethics Gate Implementation
============================

The W_ethics Gate filters candidate proposals based on hard constraints (inviolable conditions).
It is a "gate" (pass/fail) NOT an "axis" (optimization target).

Key principles:
- W0/W1 violations (irreversible harm, domination) trigger immediate rejection
- W2-W4 violations (dignity, dependency, exclusion) can be repaired
- Repairs follow the mapping: destruction/exclusion/dependency → generation/co-prosperity/mutual empowerment

Reference: 01_specifications/wethics_gate/W_ETHICS_GATE.md
"""
from __future__ import annotations
from typing import List, Optional, Tuple, Callable, Dict, Any
from abc import ABC, abstractmethod

from .types import (
    Candidate,
    GateResult,
    GateDecision,
    Violation,
    GateViolationCode,
    RepairAction,
    RepairStage,
    DEFAULT_TAU_REJECT,
    DEFAULT_TAU_REPAIR,
    DEFAULT_MAX_REPAIRS,
)


class ViolationDetector(ABC):
    """
    Abstract base class for violation detection.

    Implementations should analyze candidate text and return detected violations.
    This allows pluggable detection strategies (rule-based, ML-based, philosopher-based).
    """

    @abstractmethod
    def detect(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> List[Violation]:
        """
        Detect violations in a candidate.

        Args:
            candidate: The candidate to analyze
            context: Optional context information (use case, stakeholders, etc.)

        Returns:
            List of detected violations
        """
        pass


class RepairEngine(ABC):
    """
    Abstract base class for repair operations.

    Implementations should apply repairs following the 4-stage protocol:
    1. Concept Mapping (destruction → generation)
    2. Constraint Injection (add consent, options, safety)
    3. Scope Reduction (localize, minimize)
    4. Goal Reframe (achieve same value differently)
    """

    @abstractmethod
    def repair(
        self,
        candidate: Candidate,
        violations: List[Violation],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Tuple[str, List[RepairAction]]]:
        """
        Attempt to repair violations in a candidate.

        Args:
            candidate: The candidate to repair
            violations: List of violations to address
            context: Optional context information

        Returns:
            Tuple of (repaired_text, repair_actions) or None if repair impossible
        """
        pass


class DefaultViolationDetector(ViolationDetector):
    """
    Default rule-based violation detector.

    This implementation provides basic keyword and pattern matching.
    For production, extend with semantic analysis or philosopher module integration.
    """

    # Detection patterns for each violation type
    DETECTION_PATTERNS: Dict[GateViolationCode, Dict[str, Any]] = {
        GateViolationCode.W0_IRREVERSIBLE_VIABILITY_HARM: {
            "keywords": [
                "irreversible destruction", "permanent elimination",
                "eradicate species", "destroy ecosystem",
                "annihilate", "extinction",
            ],
            "severity_base": 1.0,
            "repairable": False,
        },
        GateViolationCode.W1_DOMINATION_CAPTURE: {
            "keywords": [
                "total control", "absolute power", "dominate all",
                "subjugate", "enforce submission", "capture market entirely",
                "monopolize", "eliminate competition permanently",
            ],
            "severity_base": 0.9,
            "repairable": False,
        },
        GateViolationCode.W2_DIGNITY_VIOLATION: {
            "keywords": [
                "dehumanize", "objectify", "treat as tool",
                "manipulate without consent", "deceive users",
            ],
            "severity_base": 0.7,
            "repairable": True,
        },
        GateViolationCode.W3_DEPENDENCY_ENGINEERING: {
            "keywords": [
                "lock-in", "no escape", "force dependency",
                "eliminate alternatives", "trap users",
                "make irreplaceable", "create addiction",
            ],
            "severity_base": 0.6,
            "repairable": True,
        },
        GateViolationCode.W4_STRUCTURAL_EXCLUSION: {
            "keywords": [
                "exclude permanently", "deny access to all",
                "discriminate by default", "ignore accessibility",
            ],
            "severity_base": 0.6,
            "repairable": True,
        },
    }

    def detect(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> List[Violation]:
        """Detect violations using keyword matching."""
        violations = []
        text_lower = candidate.text.lower()

        for code, pattern_info in self.DETECTION_PATTERNS.items():
            keywords = pattern_info["keywords"]
            severity_base = pattern_info["severity_base"]
            repairable = pattern_info["repairable"]

            for keyword in keywords:
                if keyword.lower() in text_lower:
                    # Found a match
                    confidence = self._assess_confidence(candidate.text, keyword)

                    if confidence > 0.3:  # Minimum confidence threshold
                        violations.append(Violation(
                            code=code,
                            severity=severity_base,
                            confidence=confidence,
                            evidence=[f"Matched keyword: '{keyword}'"],
                            repairable=repairable,
                            suggested_repairs=self._suggest_repairs(code, keyword),
                        ))

        return violations

    def _assess_confidence(self, text: str, keyword: str) -> float:
        """Assess confidence based on context around the keyword."""
        confidence = 0.6

        # Find keyword position
        pos = text.lower().find(keyword.lower())
        if pos == -1:
            return 0.0

        # Check for negation context
        prefix = text[max(0, pos - 50):pos].lower()
        negations = ["reject", "oppose", "condemn", "wrong", "not", "never", "avoid", "prevent"]
        if any(neg in prefix for neg in negations):
            confidence *= 0.3  # Likely discussing, not endorsing

        # Check for academic/analytical context
        academic = ["historically", "critique", "analysis", "example of", "problematic"]
        if any(marker in prefix for marker in academic):
            confidence *= 0.4  # Likely academic discussion

        return min(1.0, confidence)

    def _suggest_repairs(self, code: GateViolationCode, keyword: str) -> List[str]:
        """Generate repair suggestions based on violation type."""
        suggestions = {
            GateViolationCode.W2_DIGNITY_VIOLATION: [
                "Replace objectifying language with person-centered framing",
                "Add informed consent mechanisms",
                "Ensure transparency about data/decision processes",
            ],
            GateViolationCode.W3_DEPENDENCY_ENGINEERING: [
                "Add data portability options",
                "Provide alternative pathways",
                "Enable easy opt-out mechanisms",
                "Support interoperability standards",
            ],
            GateViolationCode.W4_STRUCTURAL_EXCLUSION: [
                "Implement accessibility standards (WCAG)",
                "Add alternative access methods",
                "Design for edge cases and diverse users",
            ],
        }
        return suggestions.get(code, [])


class DefaultRepairEngine(RepairEngine):
    """
    Default repair engine implementing the 4-stage repair protocol.

    Stages (in order):
    1. Concept Mapping: domination/exclusion/dependency → generation/co-prosperity/mutual empowerment
    2. Constraint Injection: Add consent, options, withdrawal, audit, accountability
    3. Scope Reduction: Reduce impact scope/authority/duration/data
    4. Goal Reframe: Achieve same value through different means
    """

    # Mapping rules: destructive concept → constructive alternative
    CONCEPT_MAPPINGS = {
        "dominate": "collaborate with",
        "control": "coordinate with",
        "force": "invite",
        "eliminate": "transform",
        "exclude": "include with options",
        "trap": "offer choices to",
        "lock-in": "provide flexible commitment to",
        "manipulate": "transparently influence",
        "deceive": "inform honestly",
        "exploit": "partner with",
        "subjugate": "empower",
    }

    def repair(
        self,
        candidate: Candidate,
        violations: List[Violation],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Tuple[str, List[RepairAction]]]:
        """Apply repair stages to address violations."""

        # Filter to repairable violations only
        repairable = [v for v in violations if v.repairable]
        if not repairable:
            return None

        repaired_text = candidate.text
        repair_actions = []

        # Stage 1: Concept Mapping
        for violation in repairable:
            result = self._apply_concept_mapping(repaired_text, violation)
            if result:
                repaired_text, action = result
                repair_actions.append(action)

        # Stage 2: Constraint Injection
        injection_result = self._apply_constraint_injection(repaired_text, repairable)
        if injection_result:
            repaired_text, action = injection_result
            repair_actions.append(action)

        # Stage 3: Scope Reduction (if still needed)
        # Stage 4: Goal Reframe (if still needed)
        # These are applied only if earlier stages insufficient

        if repair_actions:
            return (repaired_text, repair_actions)
        return None

    def _apply_concept_mapping(
        self, text: str, violation: Violation
    ) -> Optional[Tuple[str, RepairAction]]:
        """Apply concept mapping to destructive terms."""
        modified = text
        changes_made = []

        for destructive, constructive in self.CONCEPT_MAPPINGS.items():
            if destructive in text.lower():
                # Case-preserving replacement
                import re
                pattern = re.compile(re.escape(destructive), re.IGNORECASE)
                modified = pattern.sub(constructive, modified)
                changes_made.append(f"{destructive} → {constructive}")

        if changes_made:
            # Estimate semantic drift (simplified)
            drift = min(0.3, len(changes_made) * 0.05)

            return (modified, RepairAction(
                stage=RepairStage.CONCEPT_MAPPING,
                description=f"Applied concept mappings: {', '.join(changes_made)}",
                before_text=text[:100],
                after_text=modified[:100],
                semantic_drift=drift,
            ))
        return None

    def _apply_constraint_injection(
        self, text: str, violations: List[Violation]
    ) -> Optional[Tuple[str, RepairAction]]:
        """Inject constraints for consent, options, and safety."""
        constraints = []

        # Check which constraints are needed based on violation types
        codes = {v.code for v in violations}

        if GateViolationCode.W2_DIGNITY_VIOLATION in codes:
            constraints.append("with informed consent and transparency")

        if GateViolationCode.W3_DEPENDENCY_ENGINEERING in codes:
            constraints.append("while preserving user choice and data portability")

        if GateViolationCode.W4_STRUCTURAL_EXCLUSION in codes:
            constraints.append("with accessible alternatives for all users")

        if constraints:
            constraint_text = " [" + "; ".join(constraints) + "]"
            modified = text + constraint_text

            return (modified, RepairAction(
                stage=RepairStage.CONSTRAINT_INJECTION,
                description=f"Injected constraints: {', '.join(constraints)}",
                before_text=text[-50:] if len(text) > 50 else text,
                after_text=modified[-100:] if len(modified) > 100 else modified,
                semantic_drift=0.1,
            ))
        return None


class WethicsGate:
    """
    Main W_ethics Gate class.

    Evaluates candidates against hard ethical constraints:
    - Detects violations (W0-W4)
    - Attempts repairs for repairable violations (W2-W4)
    - Returns gate decision (ALLOW, ALLOW_WITH_REPAIR, REJECT, ESCALATE)

    Usage:
        gate = WethicsGate()
        result = gate.check(candidate)

        if result.decision == GateDecision.ALLOW:
            # Proceed with candidate
        elif result.decision == GateDecision.ALLOW_WITH_REPAIR:
            # Use result.repaired_text
        elif result.decision == GateDecision.REJECT:
            # Candidate failed, see result.explanation
    """

    def __init__(
        self,
        tau_reject: float = DEFAULT_TAU_REJECT,
        tau_repair: float = DEFAULT_TAU_REPAIR,
        max_repairs: int = DEFAULT_MAX_REPAIRS,
        detector: Optional[ViolationDetector] = None,
        repair_engine: Optional[RepairEngine] = None,
    ):
        """
        Initialize W_ethics Gate.

        Args:
            tau_reject: Impact threshold for immediate rejection (default 0.6)
            tau_repair: Impact threshold for repair attempt (default 0.3)
            max_repairs: Maximum repair iterations (default 2)
            detector: Custom violation detector (default: DefaultViolationDetector)
            repair_engine: Custom repair engine (default: DefaultRepairEngine)
        """
        self.tau_reject = tau_reject
        self.tau_repair = tau_repair
        self.max_repairs = max_repairs
        self.detector = detector or DefaultViolationDetector()
        self.repair_engine = repair_engine or DefaultRepairEngine()

    def detect(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> List[Violation]:
        """
        Detect violations in a candidate.

        Args:
            candidate: Candidate to check
            context: Optional context information

        Returns:
            List of detected violations
        """
        return self.detector.detect(candidate, context)

    def check(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> GateResult:
        """
        Evaluate candidate against W_ethics Gate.

        Args:
            candidate: Candidate to evaluate
            context: Optional context information

        Returns:
            GateResult with decision and details
        """
        violations = self.detect(candidate, context)

        # Check for immediate rejection (P0)
        for v in violations:
            if v.is_hard_violation and v.impact_score >= self.tau_reject:
                return GateResult(
                    decision=GateDecision.REJECT,
                    violations=violations,
                    explanation=f"Hard violation {v.code.value} with impact {v.impact_score:.2f} exceeds threshold {self.tau_reject}",
                )

        # Check if any repairs needed
        need_repair = any(
            v.impact_score >= self.tau_repair and v.repairable
            for v in violations
        )

        if not need_repair:
            # No significant violations - ALLOW
            if violations:
                return GateResult(
                    decision=GateDecision.ALLOW,
                    violations=violations,
                    explanation="Minor violations below repair threshold",
                )
            return GateResult(
                decision=GateDecision.ALLOW,
                violations=[],
                explanation="No violations detected",
            )

        # Attempt repairs (P1)
        current_text = candidate.text
        all_repairs: List[RepairAction] = []

        for iteration in range(self.max_repairs):
            # Create temporary candidate with current text
            temp_candidate = Candidate(
                cid=candidate.cid,
                text=current_text,
                meta=candidate.meta,
            )

            repair_result = self.repair_engine.repair(temp_candidate, violations, context)

            if repair_result is None:
                # Cannot repair further
                break

            current_text, repairs = repair_result
            all_repairs.extend(repairs)

            # Re-detect violations
            temp_candidate = Candidate(
                cid=candidate.cid,
                text=current_text,
                meta=candidate.meta,
            )
            violations = self.detect(temp_candidate, context)

            # Check if hard violation appeared
            for v in violations:
                if v.is_hard_violation and v.impact_score >= self.tau_reject:
                    return GateResult(
                        decision=GateDecision.REJECT,
                        violations=violations,
                        repaired_text=current_text,
                        repair_log=all_repairs,
                        explanation=f"Repair revealed hard violation {v.code.value}",
                    )

            # Check if repairs resolved issues
            need_repair = any(
                v.impact_score >= self.tau_repair and v.repairable
                for v in violations
            )

            if not need_repair:
                # Repairs successful (P2)
                return GateResult(
                    decision=GateDecision.ALLOW_WITH_REPAIR,
                    violations=violations,
                    repaired_text=current_text,
                    repair_log=all_repairs,
                    explanation=f"Violations resolved after {iteration + 1} repair iteration(s)",
                )

        # Repairs exhausted but issues remain (P3)
        return GateResult(
            decision=GateDecision.REJECT,
            violations=violations,
            repaired_text=current_text,
            repair_log=all_repairs,
            explanation=f"Unable to resolve violations after {self.max_repairs} repair attempts",
        )

    def check_batch(
        self,
        candidates: List[Candidate],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[Candidate, GateResult]]:
        """
        Evaluate multiple candidates.

        Args:
            candidates: List of candidates to evaluate
            context: Optional shared context

        Returns:
            List of (candidate, result) tuples
        """
        return [(c, self.check(c, context)) for c in candidates]


def create_wethics_gate(
    tau_reject: float = DEFAULT_TAU_REJECT,
    tau_repair: float = DEFAULT_TAU_REPAIR,
    max_repairs: int = DEFAULT_MAX_REPAIRS,
) -> WethicsGate:
    """
    Factory function to create a WethicsGate instance.

    Args:
        tau_reject: Impact threshold for immediate rejection
        tau_repair: Impact threshold for repair attempt
        max_repairs: Maximum repair iterations

    Returns:
        WethicsGate instance
    """
    return WethicsGate(
        tau_reject=tau_reject,
        tau_repair=tau_repair,
        max_repairs=max_repairs,
    )


__all__ = [
    "ViolationDetector",
    "RepairEngine",
    "DefaultViolationDetector",
    "DefaultRepairEngine",
    "WethicsGate",
    "create_wethics_gate",
]
