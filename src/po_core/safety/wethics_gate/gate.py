"""
W_ethics Gate Core
==================

The main gate implementation that orchestrates:
1. Violation detection via pluggable detectors
2. Repair attempts for salvageable violations (W2-W4)
3. Semantic drift checking after repairs
4. Final decision (ALLOW / ALLOW_WITH_REPAIR / REJECT / ESCALATE)

Design Philosophy:
- Gate is "inviolable constraint", NOT "optimization axis"
- Repair mapping: Destruction/Exclusion/Dependency → Generation/Co-prosperity/Mutual Empowerment
- Three mandatory criteria for all repairs:
  1. Does not damage dignity of others
  2. Increases sustainability of relationships
  3. Mutual empowerment, not dependency

Pipeline:
1. DETECT: Run all detectors, aggregate evidence into violations
2. P0 REJECT: If W0/W1 above tau_reject, immediate reject
3. REPAIR: Attempt repairs for W2-W4 violations
4. DRIFT CHECK: Ensure repairs don't change the goal
5. DECIDE: Final decision based on remaining violations and drift

Reference: 01_specifications/wethics_gate/W_ETHICS_GATE.md
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from .detectors import (
    DetectorRegistry,
    ViolationDetector,
    aggregate_evidence_to_violations,
    create_default_registry,
)
from .semantic_drift import DriftReport, semantic_drift
from .types import Candidate, GateConfig, GateDecision, GateResult, Violation


class RuleBasedRepairEngine:
    """
    Deterministic repair engine.

    Applies the core mapping rule:
        破壊・排除・依存 → 生成・共栄・相互増強

    And injects minimal constraints:
        consent, migration, transparency, dignity

    This is intentionally minimal and testable.
    In production, swap with an LLM-based refiner while keeping
    the semantic_drift guardrail.
    """

    def repair(self, text: str, violations: Sequence[str]) -> Tuple[str, List[str]]:
        """
        Apply repairs based on violation codes.

        Args:
            text: Original text
            violations: List of violation codes (e.g., ["W2", "W3"])

        Returns:
            Tuple of (repaired_text, repair_log)
        """
        log: List[str] = []
        out = text
        codes = set(violations)

        # W4: exclusion / "cutting off existing users"
        if "W4" in codes:
            repls = [
                ("切り捨てる", "尊重しつつ移行し、包摂する"),
                ("切り捨て", "尊重しつつ移行し、包摂"),
                ("見捨てる", "尊重しつつ支援し、包摂する"),
                ("対象外", "選択肢を用意し、包摂する"),
                (
                    "abandon existing",
                    "support existing with migration and inclusion for",
                ),
                ("discard legacy", "support legacy with transition plan for"),
                ("cut off", "support with migration plan"),
            ]
            for a, b in repls:
                if a in out:
                    out = out.replace(a, b)
                    log.append(f"W4_map: {a} -> {b}")

            # Inject migration plan if needed
            if "移行" not in out and "migration" not in out.lower():
                if "既存ユーザー" in out or "既存利用者" in out:
                    out += "\n追加: 既存ユーザー向けに移行期間・互換性・代替手段を提供する。"
                    log.append("W4_inject: migration_plan_ja")
                elif "existing user" in out.lower():
                    out += "\nAddition: Provide migration period, compatibility, and alternatives for existing users."
                    log.append("W4_inject: migration_plan_en")

        # W3: lock-in / dependency
        if "W3" in codes:
            repls = [
                ("囲い込み", "選択肢を確保し相互運用性を高める"),
                ("ロックイン", "相互運用性とデータ可搬性を確保する"),
                ("乗り換え不可", "データ可搬性を確保し乗り換え可能にする"),
                ("逃げ道がない", "撤回・中断・解約の選択肢を明示する"),
                ("依存させる", "利用者の自律性を尊重し依存を避ける"),
                ("lock-in", "interoperability and data portability"),
                ("lock in", "interoperability and data portability"),
                ("no escape", "clear opt-out and withdrawal options"),
                ("create dependency", "respect user autonomy and avoid dependency"),
            ]
            for a, b in repls:
                if a.lower() in out.lower():
                    out = out.replace(a, b)
                    log.append(f"W3_map: {a} -> {b}")

            # Inject consent + transparency
            if "同意" not in out and "consent" not in out.lower():
                if any(c in out for c in ["データ", "利用者", "ユーザー"]):
                    out += "\n追加: データ利用は最小化し、目的・範囲を明示し、同意と撤回を可能にする。"
                    log.append("W3_inject: consent_transparency_ja")
                elif any(c.lower() in out.lower() for c in ["data", "user"]):
                    out += "\nAddition: Minimize data usage, clarify purpose and scope, enable consent and withdrawal."
                    log.append("W3_inject: consent_transparency_en")

        # W2: dignity / manipulation
        if "W2" in codes:
            repls = [
                ("洗脳", "説得ではなく説明と選択肢を提供"),
                ("操作", "合意に基づき支援"),
                ("誘導", "透明性のある推薦"),
                ("brainwash", "provide explanation and choices"),
                ("manipulate", "support based on consent"),
                ("deceive", "transparent recommendation"),
            ]
            for a, b in repls:
                if a.lower() in out.lower():
                    out = out.replace(a, b)
                    log.append(f"W2_map: {a} -> {b}")

            # Inject dignity clause
            if "尊厳" not in out and "dignity" not in out.lower():
                if any(c in out for c in ["利用者", "ユーザー"]):
                    out += "\n追加: 利用者を道具化せず、尊厳・合意・説明責任を満たす設計とする。"
                    log.append("W2_inject: dignity_ja")
                elif "user" in out.lower():
                    out += "\nAddition: Design respects user dignity, consent, and accountability."
                    log.append("W2_inject: dignity_en")

        return out, log


class WethicsGate:
    """
    W_ethics Gate core.

    Pipeline:
    1. Detect evidence via detectors
    2. Aggregate into violations
    3. P0 reject for W0/W1 if above tau_reject
    4. Attempt repairs for W2-W4 up to max_repairs
    5. Semantic drift check (goal-change guardrail)

    Usage:
        gate = WethicsGate()
        result = gate.check(candidate)

        if result.decision == GateDecision.ALLOW:
            # Use original text
            pass
        elif result.decision == GateDecision.ALLOW_WITH_REPAIR:
            # Use result.repaired_text
            pass
        elif result.decision == GateDecision.REJECT:
            # Cannot use this candidate
            pass
    """

    def __init__(
        self,
        detectors: Optional[Sequence[ViolationDetector]] = None,
        config: Optional[GateConfig] = None,
        repair_engine: Optional[RuleBasedRepairEngine] = None,
    ) -> None:
        """
        Initialize the gate.

        Args:
            detectors: List of detectors to use. If None, uses default registry.
            config: Gate configuration. If None, uses defaults.
            repair_engine: Repair engine. If None, uses RuleBasedRepairEngine.
        """
        if detectors is None:
            registry = create_default_registry()
            self.detectors = registry.get_all()
        else:
            self.detectors = list(detectors)

        self.config = config or GateConfig()
        self.repair_engine = repair_engine or RuleBasedRepairEngine()

    def _detect_violations(
        self, c: Candidate, context: Optional[dict] = None
    ) -> List[Violation]:
        """Run all detectors and aggregate evidence into violations."""
        evs = []
        for det in self.detectors:
            evs.extend(det.detect(c, context=context))
        return aggregate_evidence_to_violations(evs)

    def check(self, c: Candidate, context: Optional[dict] = None) -> GateResult:
        """
        Check a candidate against the W_ethics Gate.

        Args:
            c: Candidate to check
            context: Optional context dictionary

        Returns:
            GateResult with decision and details
        """
        violations = self._detect_violations(c, context=context)

        # P0: Hard reject for W0/W1 if intention-level or high risk
        for v in violations:
            if v.code in ("W0", "W1"):
                if v.impact_score >= self.config.tau_reject:
                    return GateResult(
                        decision=GateDecision.REJECT,
                        violations=violations,
                        explanation=f"Hard reject: {v.code} violation with impact={v.impact_score:.2f}",
                    )

        # If nothing serious, check if repairs needed
        need_repair = [
            v
            for v in violations
            if v.repairable and v.impact_score >= self.config.tau_repair
        ]

        if not need_repair:
            return GateResult(
                decision=GateDecision.ALLOW,
                violations=violations,
                explanation="No violations requiring action",
            )

        # Attempt repair loop
        cur_text = c.text
        repair_log: List[str] = []
        drift_score: Optional[float] = None
        drift_notes: Optional[str] = None

        for iteration in range(self.config.max_repairs):
            codes = [v.code for v in need_repair]
            repaired_text, rlog = self.repair_engine.repair(cur_text, codes)
            repair_log.extend(rlog)

            # Drift check after each repair
            before_goal = c.meta.get("goal") if isinstance(c.meta, dict) else None
            report = semantic_drift(cur_text, repaired_text, before_goal=before_goal)
            drift_score = report.drift
            drift_notes = report.notes

            # Re-run detection on repaired output
            cur_text = repaired_text
            v2 = self._detect_violations(
                Candidate(cid=c.cid, text=cur_text, meta=c.meta),
                context=context,
            )

            # Hard fail if W0/W1 became obvious or drift too high
            hard_fail = any(
                v.code in ("W0", "W1") and v.impact_score >= self.config.tau_reject
                for v in v2
            )

            if hard_fail:
                return GateResult(
                    decision=GateDecision.REJECT,
                    violations=v2,
                    repaired_text=cur_text,
                    repair_log=repair_log,
                    drift_score=drift_score,
                    drift_notes=drift_notes,
                    explanation="Repair revealed hard violation",
                )

            if drift_score >= self.config.tau_drift_reject:
                return GateResult(
                    decision=GateDecision.REJECT,
                    violations=v2,
                    repaired_text=cur_text,
                    repair_log=repair_log,
                    drift_score=drift_score,
                    drift_notes=drift_notes,
                    explanation=f"Semantic drift too high: {drift_score:.2f}",
                )

            # Check if more repairs needed
            need_repair = [
                v
                for v in v2
                if v.repairable and v.impact_score >= self.config.tau_repair
            ]

            if not need_repair:
                # Check drift level for escalation
                if drift_score >= self.config.tau_drift_escalate:
                    decision = (
                        GateDecision.REJECT
                        if self.config.strict_no_escalate
                        else GateDecision.ESCALATE
                    )
                    return GateResult(
                        decision=decision,
                        violations=v2,
                        repaired_text=cur_text,
                        repair_log=repair_log,
                        drift_score=drift_score,
                        drift_notes=drift_notes,
                        explanation=f"Repair succeeded but drift requires review: {drift_score:.2f}",
                    )

                return GateResult(
                    decision=GateDecision.ALLOW_WITH_REPAIR,
                    violations=v2,
                    repaired_text=cur_text,
                    repair_log=repair_log,
                    drift_score=drift_score,
                    drift_notes=drift_notes,
                    explanation="Repair succeeded",
                )

        # Repair budget exhausted
        return GateResult(
            decision=GateDecision.REJECT,
            violations=violations,
            repaired_text=cur_text,
            repair_log=repair_log,
            drift_score=drift_score,
            drift_notes=drift_notes,
            explanation="Repair budget exhausted",
        )

    def check_with_explanation(
        self, c: Candidate, context: Optional[dict] = None
    ) -> GateResult:
        """Check a candidate and attach an ExplanationChain to the result.

        This is the Phase 3 observability entry point.  It runs the
        standard ``check()`` pipeline and then builds an
        ``ExplanationChain`` from the result, storing it on
        ``GateResult.explanation_chain``.

        Args:
            c: Candidate to check
            context: Optional context dictionary

        Returns:
            GateResult with ``explanation_chain`` populated.
        """
        from .explanation import build_explanation_chain

        result = self.check(c, context=context)
        result.explanation_chain = build_explanation_chain(
            result,
            drift_threshold_escalate=self.config.tau_drift_escalate,
            drift_threshold_reject=self.config.tau_drift_reject,
        )
        return result

    def check_batch(
        self, candidates: Sequence[Candidate], context: Optional[dict] = None
    ) -> List[Tuple[Candidate, GateResult]]:
        """
        Check multiple candidates.

        Args:
            candidates: List of candidates to check
            context: Optional context dictionary

        Returns:
            List of (candidate, result) tuples
        """
        return [(c, self.check(c, context)) for c in candidates]


def create_wethics_gate(
    detectors: Optional[Sequence[ViolationDetector]] = None,
    tau_reject: float = 0.6,
    tau_repair: float = 0.3,
    max_repairs: int = 2,
    tau_drift_reject: float = 0.7,
    tau_drift_escalate: float = 0.4,
    strict_no_escalate: bool = False,
) -> WethicsGate:
    """
    Factory function to create a WethicsGate with custom configuration.

    Args:
        detectors: Optional list of detectors
        tau_reject: Threshold for immediate rejection
        tau_repair: Threshold for repair attempt
        max_repairs: Maximum repair iterations
        tau_drift_reject: Drift threshold for rejection
        tau_drift_escalate: Drift threshold for escalation
        strict_no_escalate: If True, escalate becomes reject

    Returns:
        Configured WethicsGate instance
    """
    config = GateConfig(
        tau_reject=tau_reject,
        tau_repair=tau_repair,
        max_repairs=max_repairs,
        tau_drift_reject=tau_drift_reject,
        tau_drift_escalate=tau_drift_escalate,
        strict_no_escalate=strict_no_escalate,
    )
    return WethicsGate(detectors=detectors, config=config)


__all__ = [
    "RuleBasedRepairEngine",
    "WethicsGate",
    "create_wethics_gate",
]
