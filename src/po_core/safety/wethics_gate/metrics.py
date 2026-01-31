"""
ΔE Metrics: Axis Scores and Measurement Functions
==================================================

Implements the ΔE (distortion vector) measurement system for evaluating candidates
across five axes: Safety, Fairness, Privacy, Autonomy, and Harm Avoidance.

Key concepts:
- Each axis scored [0, 1] with confidence and evidence
- E_min: Minimum acceptable line (below = red flag)
- E_target: Target ideal (above = better)
- ΔE: Distortion vector measuring gap to target

Reference: 01_specifications/wethics_gate/DELTA_E.md
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import math

from .types import (
    Candidate,
    AxisScore,
    AXES,
    AXIS_NAMES,
)


@dataclass
class AxisProfile:
    """
    Configuration for axis evaluation thresholds.

    Attributes:
        axis: Axis identifier ("A" through "E")
        e_min: Minimum acceptable score (below = red flag)
        e_target: Target score (ideal)
        weight_range: (min_weight, max_weight) for MCDA
    """
    axis: str
    e_min: float
    e_target: float
    weight_range: Tuple[float, float] = (0.1, 0.3)


@dataclass
class ContextProfile:
    """
    Context-specific axis configuration.

    Different contexts (disaster, medical, education, entertainment)
    may have different thresholds and weight ranges.
    """
    name: str
    description: str
    axis_profiles: Dict[str, AxisProfile]

    @classmethod
    def default(cls) -> "ContextProfile":
        """Create default balanced context profile."""
        return cls(
            name="default",
            description="Balanced default context",
            axis_profiles={
                "A": AxisProfile("A", e_min=0.4, e_target=0.8, weight_range=(0.15, 0.35)),
                "B": AxisProfile("B", e_min=0.4, e_target=0.8, weight_range=(0.10, 0.25)),
                "C": AxisProfile("C", e_min=0.3, e_target=0.7, weight_range=(0.10, 0.20)),
                "D": AxisProfile("D", e_min=0.3, e_target=0.7, weight_range=(0.15, 0.25)),
                "E": AxisProfile("E", e_min=0.4, e_target=0.8, weight_range=(0.15, 0.30)),
            }
        )

    @classmethod
    def disaster(cls) -> "ContextProfile":
        """Create disaster/emergency context profile (safety-heavy)."""
        return cls(
            name="disaster",
            description="Disaster/emergency context - safety prioritized",
            axis_profiles={
                "A": AxisProfile("A", e_min=0.6, e_target=0.95, weight_range=(0.30, 0.50)),
                "B": AxisProfile("B", e_min=0.3, e_target=0.7, weight_range=(0.05, 0.15)),
                "C": AxisProfile("C", e_min=0.2, e_target=0.5, weight_range=(0.05, 0.15)),
                "D": AxisProfile("D", e_min=0.2, e_target=0.6, weight_range=(0.10, 0.20)),
                "E": AxisProfile("E", e_min=0.5, e_target=0.9, weight_range=(0.20, 0.35)),
            }
        )

    @classmethod
    def medical(cls) -> "ContextProfile":
        """Create medical context profile (safety + privacy)."""
        return cls(
            name="medical",
            description="Medical context - safety and privacy prioritized",
            axis_profiles={
                "A": AxisProfile("A", e_min=0.6, e_target=0.95, weight_range=(0.25, 0.40)),
                "B": AxisProfile("B", e_min=0.4, e_target=0.8, weight_range=(0.10, 0.20)),
                "C": AxisProfile("C", e_min=0.6, e_target=0.9, weight_range=(0.20, 0.35)),
                "D": AxisProfile("D", e_min=0.4, e_target=0.8, weight_range=(0.15, 0.25)),
                "E": AxisProfile("E", e_min=0.5, e_target=0.9, weight_range=(0.15, 0.25)),
            }
        )


class AxisScorer(ABC):
    """
    Abstract base class for axis scoring.

    Each axis (A-E) should have a concrete scorer implementation.
    """

    @abstractmethod
    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """
        Score a candidate on this axis.

        Args:
            candidate: Candidate to score
            context: Optional context information

        Returns:
            AxisScore with value, confidence, and evidence
        """
        pass


class SafetyScorer(AxisScorer):
    """
    Axis A: Safety scorer.

    Evaluates physical and systemic safety risks.
    Score = 1 - max_risk where risk = probability * impact * irreversibility
    """

    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """Score safety based on harm scenario analysis."""
        text = candidate.text.lower()
        evidence = []
        counterevidence = []

        # Risk indicators
        high_risk_indicators = [
            "physical harm", "injury", "death", "dangerous",
            "toxic", "explosive", "weapon", "attack",
        ]

        safety_indicators = [
            "safe", "protected", "secure", "verified",
            "tested", "certified", "safeguard",
        ]

        risk_count = sum(1 for ind in high_risk_indicators if ind in text)
        safety_count = sum(1 for ind in safety_indicators if ind in text)

        if risk_count > 0:
            evidence.append(f"Found {risk_count} risk indicator(s)")
        if safety_count > 0:
            counterevidence.append(f"Found {safety_count} safety indicator(s)")

        # Calculate score (simplified)
        base_score = 0.7
        risk_penalty = min(0.5, risk_count * 0.1)
        safety_bonus = min(0.2, safety_count * 0.05)

        value = max(0.0, min(1.0, base_score - risk_penalty + safety_bonus))
        confidence = 0.5 if not evidence and not counterevidence else 0.7

        return AxisScore(
            value=value,
            confidence=confidence,
            evidence=evidence,
            counterevidence=counterevidence,
            notes="Safety score based on risk indicator analysis",
        )


class FairnessScorer(AxisScorer):
    """
    Axis B: Fairness scorer.

    Evaluates equity and non-discrimination.
    Score = 1 - max_disparity
    """

    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """Score fairness based on disparity analysis."""
        text = candidate.text.lower()
        evidence = []
        counterevidence = []

        # Bias indicators
        bias_indicators = [
            "only for", "not for", "exclude", "discriminate",
            "prefer certain", "favor", "against",
        ]

        fairness_indicators = [
            "equal", "fair", "inclusive", "diverse",
            "accessible", "equitable", "universal",
        ]

        bias_count = sum(1 for ind in bias_indicators if ind in text)
        fairness_count = sum(1 for ind in fairness_indicators if ind in text)

        if bias_count > 0:
            evidence.append(f"Found {bias_count} potential bias indicator(s)")
        if fairness_count > 0:
            counterevidence.append(f"Found {fairness_count} fairness indicator(s)")

        base_score = 0.7
        bias_penalty = min(0.5, bias_count * 0.15)
        fairness_bonus = min(0.2, fairness_count * 0.05)

        value = max(0.0, min(1.0, base_score - bias_penalty + fairness_bonus))
        confidence = 0.5 if not evidence and not counterevidence else 0.7

        return AxisScore(
            value=value,
            confidence=confidence,
            evidence=evidence,
            counterevidence=counterevidence,
            notes="Fairness score based on disparity indicator analysis",
        )


class PrivacyScorer(AxisScorer):
    """
    Axis C: Privacy scorer.

    Evaluates data protection and informational self-determination.
    Score = 1 - sensitivity * exposure * (1 - protection_strength)
    """

    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """Score privacy based on data handling analysis."""
        text = candidate.text.lower()
        evidence = []
        counterevidence = []

        # Privacy risk indicators
        risk_indicators = [
            "collect data", "track", "monitor", "surveillance",
            "share with third", "sell data", "personal information",
        ]

        protection_indicators = [
            "encrypt", "anonymize", "consent", "opt-out",
            "data minimization", "privacy", "gdpr", "confidential",
        ]

        risk_count = sum(1 for ind in risk_indicators if ind in text)
        protection_count = sum(1 for ind in protection_indicators if ind in text)

        if risk_count > 0:
            evidence.append(f"Found {risk_count} privacy risk indicator(s)")
        if protection_count > 0:
            counterevidence.append(f"Found {protection_count} protection indicator(s)")

        sensitivity = min(1.0, risk_count * 0.2)
        protection = min(1.0, protection_count * 0.2)

        value = max(0.0, min(1.0, 1.0 - sensitivity * (1 - protection)))
        confidence = 0.5 if not evidence and not counterevidence else 0.7

        return AxisScore(
            value=value,
            confidence=confidence,
            evidence=evidence,
            counterevidence=counterevidence,
            notes="Privacy score based on data handling analysis",
        )


class AutonomyScorer(AxisScorer):
    """
    Axis D: Autonomy scorer.

    Evaluates human agency and oversight.
    Score based on user control, explainability, and consent.
    """

    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """Score autonomy based on user agency analysis."""
        text = candidate.text.lower()
        evidence = []
        counterevidence = []

        # Control reduction indicators
        control_loss_indicators = [
            "automatic", "no choice", "mandatory", "required",
            "cannot opt out", "forced", "must",
        ]

        agency_indicators = [
            "user choice", "optional", "configurable", "override",
            "explain", "transparent", "human in the loop", "consent",
        ]

        loss_count = sum(1 for ind in control_loss_indicators if ind in text)
        agency_count = sum(1 for ind in agency_indicators if ind in text)

        if loss_count > 0:
            evidence.append(f"Found {loss_count} control-reduction indicator(s)")
        if agency_count > 0:
            counterevidence.append(f"Found {agency_count} agency indicator(s)")

        base_score = 0.7
        loss_penalty = min(0.5, loss_count * 0.12)
        agency_bonus = min(0.2, agency_count * 0.05)

        value = max(0.0, min(1.0, base_score - loss_penalty + agency_bonus))
        confidence = 0.5 if not evidence and not counterevidence else 0.7

        return AxisScore(
            value=value,
            confidence=confidence,
            evidence=evidence,
            counterevidence=counterevidence,
            notes="Autonomy score based on user agency analysis",
        )


class HarmAvoidanceScorer(AxisScorer):
    """
    Axis E: Harm Avoidance scorer.

    Evaluates psychological, social, and informational harm prevention.
    Score = 1 - harm_risk
    """

    def score(self, candidate: Candidate, context: Optional[Dict[str, Any]] = None) -> AxisScore:
        """Score harm avoidance based on harm risk analysis."""
        text = candidate.text.lower()
        evidence = []
        counterevidence = []

        # Harm indicators
        harm_indicators = [
            "mislead", "misinformation", "manipulate", "exploit",
            "hate", "incite", "discriminate", "harass", "bully",
        ]

        protection_indicators = [
            "verify", "fact-check", "accurate", "truthful",
            "respectful", "supportive", "constructive",
        ]

        harm_count = sum(1 for ind in harm_indicators if ind in text)
        protection_count = sum(1 for ind in protection_indicators if ind in text)

        if harm_count > 0:
            evidence.append(f"Found {harm_count} harm indicator(s)")
        if protection_count > 0:
            counterevidence.append(f"Found {protection_count} protection indicator(s)")

        harm_risk = min(1.0, harm_count * 0.15)
        protection = min(0.3, protection_count * 0.05)

        value = max(0.0, min(1.0, 1.0 - harm_risk + protection))
        confidence = 0.5 if not evidence and not counterevidence else 0.7

        return AxisScore(
            value=value,
            confidence=confidence,
            evidence=evidence,
            counterevidence=counterevidence,
            notes="Harm avoidance score based on harm risk analysis",
        )


class MetricsEvaluator:
    """
    Main metrics evaluator for scoring candidates across all axes.

    Usage:
        evaluator = MetricsEvaluator()
        scores = evaluator.score_candidate(candidate)
        delta = evaluator.compute_delta_plus(scores, target)
    """

    DEFAULT_SCORERS: Dict[str, AxisScorer] = {
        "A": SafetyScorer(),
        "B": FairnessScorer(),
        "C": PrivacyScorer(),
        "D": AutonomyScorer(),
        "E": HarmAvoidanceScorer(),
    }

    def __init__(
        self,
        scorers: Optional[Dict[str, AxisScorer]] = None,
        context_profile: Optional[ContextProfile] = None,
    ):
        """
        Initialize metrics evaluator.

        Args:
            scorers: Custom axis scorers (default: rule-based scorers)
            context_profile: Context-specific configuration (default: balanced)
        """
        self.scorers = scorers or self.DEFAULT_SCORERS.copy()
        self.context_profile = context_profile or ContextProfile.default()

    def score_candidate(
        self,
        candidate: Candidate,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, AxisScore]:
        """
        Score a candidate across all axes.

        Args:
            candidate: Candidate to score
            context: Optional context information

        Returns:
            Dictionary mapping axis names to AxisScore
        """
        scores = {}
        for axis in AXES:
            if axis in self.scorers:
                scores[axis] = self.scorers[axis].score(candidate, context)
            else:
                # Default neutral score if no scorer
                scores[axis] = AxisScore(
                    value=0.5,
                    confidence=0.2,
                    notes=f"No scorer configured for axis {axis}",
                )
        return scores

    def compute_delta_plus(
        self,
        scores: Dict[str, AxisScore],
        target: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Compute improvement room (positive distortion) for each axis.

        ΔE⁺ᵢ = max(0, E_target,i - Eᵢ)

        Args:
            scores: Axis scores
            target: Target values (default: from context profile)

        Returns:
            Dictionary mapping axis names to delta values
        """
        if target is None:
            target = {
                axis: self.context_profile.axis_profiles[axis].e_target
                for axis in AXES
            }

        delta = {}
        for axis, score in scores.items():
            delta[axis] = max(0.0, target.get(axis, 0.8) - score.value)
        return delta

    def compute_min_violation(
        self,
        scores: Dict[str, AxisScore],
        minimum: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Compute minimum line violations for each axis.

        Vᵢ = max(0, E_min,i - Eᵢ)

        Args:
            scores: Axis scores
            minimum: Minimum acceptable values (default: from context profile)

        Returns:
            Dictionary mapping axis names to violation amounts
        """
        if minimum is None:
            minimum = {
                axis: self.context_profile.axis_profiles[axis].e_min
                for axis in AXES
            }

        violations = {}
        for axis, score in scores.items():
            violations[axis] = max(0.0, minimum.get(axis, 0.4) - score.value)
        return violations

    def has_min_violation(self, scores: Dict[str, AxisScore]) -> bool:
        """Check if any axis is below minimum threshold."""
        violations = self.compute_min_violation(scores)
        return any(v > 0 for v in violations.values())

    def compute_d2(
        self,
        scores: Dict[str, AxisScore],
        weights: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Compute weighted L2 distance (overall deviation).

        D₂ = √(Σᵢ wᵢ(ΔE⁺ᵢ)²)

        Args:
            scores: Axis scores
            weights: Axis weights (default: equal weights)

        Returns:
            L2 distance value
        """
        if weights is None:
            weights = {axis: 1.0 / len(AXES) for axis in AXES}

        delta = self.compute_delta_plus(scores)

        sum_sq = 0.0
        for axis in AXES:
            w = weights.get(axis, 0.2)
            d = delta.get(axis, 0.0)
            sum_sq += w * (d ** 2)

        return math.sqrt(sum_sq)

    def compute_d_inf(
        self,
        scores: Dict[str, AxisScore],
        weights: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Compute weighted L∞ distance (maximum gap).

        D∞ = maxᵢ(wᵢΔE⁺ᵢ)

        Args:
            scores: Axis scores
            weights: Axis weights (default: equal weights)

        Returns:
            L∞ distance value
        """
        if weights is None:
            weights = {axis: 1.0 / len(AXES) for axis in AXES}

        delta = self.compute_delta_plus(scores)

        max_weighted = 0.0
        for axis in AXES:
            w = weights.get(axis, 0.2)
            d = delta.get(axis, 0.0)
            max_weighted = max(max_weighted, w * d)

        return max_weighted


def create_metrics_evaluator(
    context_name: str = "default",
) -> MetricsEvaluator:
    """
    Factory function to create a MetricsEvaluator with a named context.

    Args:
        context_name: One of "default", "disaster", "medical"

    Returns:
        MetricsEvaluator instance
    """
    profiles = {
        "default": ContextProfile.default,
        "disaster": ContextProfile.disaster,
        "medical": ContextProfile.medical,
    }

    profile_factory = profiles.get(context_name, ContextProfile.default)
    return MetricsEvaluator(context_profile=profile_factory())


__all__ = [
    "AxisProfile",
    "ContextProfile",
    "AxisScorer",
    "SafetyScorer",
    "FairnessScorer",
    "PrivacyScorer",
    "AutonomyScorer",
    "HarmAvoidanceScorer",
    "MetricsEvaluator",
    "create_metrics_evaluator",
]
