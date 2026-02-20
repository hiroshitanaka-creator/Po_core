"""
Selection Protocol: Pareto + MCDA Selection
============================================

Implements the candidate selection protocol:
1. W_ethics Gate filtering
2. Axis scoring (ΔE calculation)
3. E_min filtering
4. Pareto filtering (non-dominated set)
5. MCDA selection (robust weight sampling or TOPSIS)

Reference: 01_specifications/wethics_gate/SELECTION_PROTOCOL.md
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Optional, Tuple

from .gate import WethicsGate
from .metrics import ContextProfile, MetricsEvaluator
from .types import (
    AXES,
    DEFAULT_PBEST_THRESHOLD,
    AxisScore,
    Candidate,
    GateDecision,
    SelectionResult,
)


def pareto_front(
    candidates: List[Candidate],
    axes: Tuple[str, ...] = AXES,
) -> List[Candidate]:
    """
    Extract Pareto front (non-dominated set) from candidates.

    A candidate x dominates y iff:
    - E_i(x) >= E_i(y) for all axes, AND
    - E_j(x) > E_j(y) for at least one axis

    Args:
        candidates: List of candidates with scores
        axes: Axes to consider for dominance

    Returns:
        List of non-dominated candidates
    """

    def dominates(x: Candidate, y: Candidate) -> bool:
        """Check if x dominates y."""
        ge_all = True
        gt_any = False

        for axis in axes:
            x_val = x.scores.get(axis, AxisScore(0.5, 0.5)).value
            y_val = y.scores.get(axis, AxisScore(0.5, 0.5)).value

            if x_val < y_val:
                ge_all = False
                break
            if x_val > y_val:
                gt_any = True

        return ge_all and gt_any

    front = []
    for c in candidates:
        # Check if c is dominated by any other candidate
        is_dominated = False
        for other in candidates:
            if other is not c and dominates(other, c):
                is_dominated = True
                break

        if not is_dominated:
            front.append(c)

    return front


def robust_weight_sampling_rank(
    candidates: List[Candidate],
    evaluator: MetricsEvaluator,
    axes: Tuple[str, ...] = AXES,
    n_samples: int = 2000,
    seed: Optional[int] = None,
) -> List[Tuple[Candidate, float]]:
    """
    Rank candidates using robust weight sampling.

    This method samples many weight vectors and counts how often each
    candidate wins, producing a "win probability" that is robust to
    weight uncertainty.

    Args:
        candidates: List of candidates with scores
        evaluator: Metrics evaluator for computing deltas
        axes: Axes to consider
        n_samples: Number of weight samples (default: 2000)
        seed: Random seed for reproducibility

    Returns:
        List of (candidate, win_probability) tuples, sorted descending
    """
    if seed is not None:
        random.seed(seed)

    win_counts: Dict[str, int] = {c.cid: 0 for c in candidates}

    for _ in range(n_samples):
        # Sample weights from weight ranges in context profile
        weights = _sample_weights(evaluator.context_profile, axes)

        # Calculate score for each candidate
        best_candidate = None
        best_score = float("-inf")

        for c in candidates:
            delta = evaluator.compute_delta_plus(c.scores)

            # S(c; w) = Σ w_i * (1 - Δ⁺_i)
            score = 0.0
            for axis in axes:
                w = weights.get(axis, 0.2)
                d = delta.get(axis, 0.0)
                score += w * (1.0 - d)

            if score > best_score:
                best_score = score
                best_candidate = c

        if best_candidate:
            win_counts[best_candidate.cid] += 1

    # Convert to probabilities and sort
    results = [(c, win_counts[c.cid] / n_samples) for c in candidates]
    results.sort(key=lambda t: t[1], reverse=True)

    return results


def _sample_weights(
    profile: ContextProfile,
    axes: Tuple[str, ...],
) -> Dict[str, float]:
    """Sample weights from the weight ranges in context profile."""
    raw_weights = {}
    for axis in axes:
        if axis in profile.axis_profiles:
            low, high = profile.axis_profiles[axis].weight_range
            raw_weights[axis] = random.uniform(low, high)
        else:
            raw_weights[axis] = random.uniform(0.1, 0.3)

    # Normalize to sum to 1
    total = sum(raw_weights.values())
    return {k: v / total for k, v in raw_weights.items()}


def topsis_rank(
    candidates: List[Candidate],
    evaluator: MetricsEvaluator,
    weights: Optional[Dict[str, float]] = None,
    axes: Tuple[str, ...] = AXES,
) -> List[Tuple[Candidate, float]]:
    """
    Rank candidates using TOPSIS (Technique for Order of Preference by
    Similarity to Ideal Solution).

    TOPSIS ranks by closeness to ideal point and distance from anti-ideal.
    CC = d⁻ / (d⁺ + d⁻)

    Args:
        candidates: List of candidates with scores
        evaluator: Metrics evaluator
        weights: Axis weights (default: equal)
        axes: Axes to consider

    Returns:
        List of (candidate, closeness_coefficient) tuples, sorted descending
    """
    if not candidates:
        return []

    if weights is None:
        weights = {axis: 1.0 / len(axes) for axis in axes}

    # Get target (ideal) and anti-ideal from context profile
    ideal = {
        axis: evaluator.context_profile.axis_profiles[axis].e_target for axis in axes
    }
    anti_ideal = {axis: 0.0 for axis in axes}  # Worst case

    results = []
    for c in candidates:
        # Compute weighted distances
        d_plus = 0.0  # Distance to ideal
        d_minus = 0.0  # Distance to anti-ideal

        for axis in axes:
            score = c.scores.get(axis, AxisScore(0.5, 0.5)).value
            w = weights.get(axis, 0.2)

            d_plus += w * ((ideal[axis] - score) ** 2)
            d_minus += w * ((score - anti_ideal[axis]) ** 2)

        d_plus = math.sqrt(d_plus)
        d_minus = math.sqrt(d_minus)

        # Closeness coefficient
        if d_plus + d_minus > 0:
            cc = d_minus / (d_plus + d_minus)
        else:
            cc = 0.5

        results.append((c, cc))

    results.sort(key=lambda t: t[1], reverse=True)
    return results


class CandidateSelector:
    """
    Main candidate selection class implementing the full protocol.

    Pipeline:
    1. W_ethics Gate filtering
    2. Axis scoring
    3. E_min filtering
    4. Pareto filtering
    5. MCDA selection

    Usage:
        selector = CandidateSelector()
        result = selector.select(candidates)

        selected = result.selected_id
        pareto_set = result.pareto_set_ids
    """

    def __init__(
        self,
        gate: Optional[WethicsGate] = None,
        evaluator: Optional[MetricsEvaluator] = None,
        mcda_method: str = "robust-weight",
        p_best_threshold: float = DEFAULT_PBEST_THRESHOLD,
        n_samples: int = 2000,
    ):
        """
        Initialize candidate selector.

        Args:
            gate: W_ethics Gate instance (default: create new)
            evaluator: Metrics evaluator (default: create new)
            mcda_method: MCDA method ("robust-weight" or "topsis")
            p_best_threshold: Win probability threshold for selection
            n_samples: Number of samples for robust weight method
        """
        self.gate = gate or WethicsGate()
        self.evaluator = evaluator or MetricsEvaluator()
        self.mcda_method = mcda_method
        self.p_best_threshold = p_best_threshold
        self.n_samples = n_samples

    def select(
        self,
        candidates: List[Candidate],
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 1,
    ) -> SelectionResult:
        """
        Select best candidate(s) from the input set.

        Args:
            candidates: List of candidates to evaluate
            context: Optional context information
            top_k: Number of top candidates to potentially return

        Returns:
            SelectionResult with selected candidate and audit info
        """
        rejected = []
        passed_candidates = []

        # Step 1: W_ethics Gate
        for c in candidates:
            result = self.gate.check(c, context)
            c.gate_result = result

            if result.decision == GateDecision.REJECT:
                rejected.append(
                    {
                        "id": c.cid,
                        "reason": "GATE_REJECT",
                        "violations": [
                            {
                                "code": (
                                    v.code.value
                                    if hasattr(v.code, "value")
                                    else str(v.code)
                                ),
                                "severity": v.severity,
                            }
                            for v in result.violations
                        ],
                    }
                )
            elif result.decision == GateDecision.ESCALATE:
                rejected.append(
                    {
                        "id": c.cid,
                        "reason": "GATE_ESCALATE",
                        "explanation": result.explanation,
                    }
                )
            else:
                # ALLOW or ALLOW_WITH_REPAIR
                if result.decision == GateDecision.ALLOW_WITH_REPAIR:
                    # Use repaired text
                    c.text = result.repaired_text or c.text
                passed_candidates.append(c)

        if not passed_candidates:
            return SelectionResult(
                selected_id=None,
                pareto_set_ids=[],
                mcda_method=self.mcda_method,
                weights_profile={},
                explanation="All candidates rejected by W_ethics Gate",
                rejected=rejected,
            )

        # Step 2: Axis scoring
        for c in passed_candidates:
            c.scores = self.evaluator.score_candidate(c, context)

        # Step 3: E_min filtering
        min_passed = []
        for c in passed_candidates:
            if self.evaluator.has_min_violation(c.scores):
                violations = self.evaluator.compute_min_violation(c.scores)
                rejected.append(
                    {
                        "id": c.cid,
                        "reason": "E_MIN_VIOLATION",
                        "violations": {k: v for k, v in violations.items() if v > 0},
                    }
                )
            else:
                min_passed.append(c)

        if not min_passed:
            return SelectionResult(
                selected_id=None,
                pareto_set_ids=[],
                mcda_method=self.mcda_method,
                weights_profile={},
                explanation="All candidates below minimum thresholds",
                rejected=rejected,
            )

        # Step 4: Pareto filtering
        pareto = pareto_front(min_passed)
        pareto_ids = [c.cid for c in pareto]

        if len(pareto) == 1:
            # Single candidate dominates all
            return SelectionResult(
                selected_id=pareto[0].cid,
                pareto_set_ids=pareto_ids,
                mcda_method="pareto-dominant",
                weights_profile={},
                p_best=1.0,
                explanation="Single candidate dominates Pareto front",
                rejected=rejected,
            )

        # Step 5: MCDA selection
        if self.mcda_method == "robust-weight":
            ranked = robust_weight_sampling_rank(
                pareto,
                self.evaluator,
                n_samples=self.n_samples,
            )
        else:  # topsis
            ranked = topsis_rank(pareto, self.evaluator)

        if not ranked:
            return SelectionResult(
                selected_id=None,
                pareto_set_ids=pareto_ids,
                mcda_method=self.mcda_method,
                weights_profile={},
                explanation="MCDA ranking failed",
                rejected=rejected,
            )

        winner, p_best = ranked[0]

        # Build weights profile
        weights_profile = {
            axis: list(self.evaluator.context_profile.axis_profiles[axis].weight_range)
            for axis in AXES
        }

        # Check confidence threshold
        if p_best < self.p_best_threshold:
            # Low confidence - return top-k for human decision
            top_ids = [c.cid for c, _ in ranked[:top_k]]
            return SelectionResult(
                selected_id=None,
                pareto_set_ids=pareto_ids,
                mcda_method=self.mcda_method,
                weights_profile=weights_profile,
                p_best=p_best,
                explanation=f"Win probability {p_best:.2f} below threshold {self.p_best_threshold}. Top-{top_k} candidates: {top_ids}",
                rejected=rejected,
            )

        return SelectionResult(
            selected_id=winner.cid,
            pareto_set_ids=pareto_ids,
            mcda_method=self.mcda_method,
            weights_profile=weights_profile,
            p_best=p_best,
            explanation=f"Selected with win probability {p_best:.2f}",
            rejected=rejected,
        )

    def select_with_details(
        self,
        candidates: List[Candidate],
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[SelectionResult, Dict[str, Any]]:
        """
        Select with additional diagnostic details.

        Returns:
            Tuple of (SelectionResult, details_dict)
        """
        result = self.select(candidates, context)

        details = {
            "total_candidates": len(candidates),
            "gate_passed": len([c for c in candidates if c.is_gate_passed()]),
            "pareto_size": len(result.pareto_set_ids),
            "rejected_count": len(result.rejected),
            "context_profile": self.evaluator.context_profile.name,
        }

        return result, details


def create_candidate_selector(
    context_name: str = "default",
    mcda_method: str = "robust-weight",
) -> CandidateSelector:
    """
    Factory function to create a CandidateSelector with named context.

    Args:
        context_name: One of "default", "disaster", "medical"
        mcda_method: MCDA method ("robust-weight" or "topsis")

    Returns:
        CandidateSelector instance
    """
    from .metrics import create_metrics_evaluator

    evaluator = create_metrics_evaluator(context_name)
    return CandidateSelector(
        evaluator=evaluator,
        mcda_method=mcda_method,
    )


__all__ = [
    "pareto_front",
    "robust_weight_sampling_rank",
    "topsis_rank",
    "CandidateSelector",
    "create_candidate_selector",
]
