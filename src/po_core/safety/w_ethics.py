"""
W_ethics: Absolute Ethical Boundaries
======================================

This module defines non-negotiable ethical boundaries for Po_core.
These boundaries represent fundamental values that must never be compromised:

**RED LINES** (絶対に越えちゃダメなライン):
- Racial/ethnic superiority or inferiority claims
- Religious-based value degradation
- Gender/sex-based inherent value judgments
- Disability-based dehumanization
- Any form of biological determinism justifying oppression
- Collective punishment or group-based guilt
- Dehumanization based on immutable characteristics

When these boundaries are violated, the system:
1. Applies strong negative W_ethics values
2. Flags the session with "危険イデオロギー疑い" (dangerous ideology suspicion)
3. Automatically stops the session if violations persist
4. Logs the incident for safety review

This is not censorship—it's protecting the integrity of philosophical reasoning
from being weaponized for oppression.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import re


class ViolationType(str, Enum):
    """Types of ethical boundary violations."""

    RACIAL_SUPREMACY = "racial_supremacy"
    ETHNIC_SUPREMACY = "ethnic_supremacy"
    RELIGIOUS_DEGRADATION = "religious_degradation"
    GENDER_ESSENTIALISM = "gender_essentialism"
    DISABILITY_DEHUMANIZATION = "disability_dehumanization"
    BIOLOGICAL_DETERMINISM = "biological_determinism"
    COLLECTIVE_PUNISHMENT = "collective_punishment"
    DEHUMANIZATION = "dehumanization"
    EXCLUSIONARY_FRAMING = "exclusionary_framing"


@dataclass
class ViolationPattern:
    """A pattern that indicates an ethical boundary violation."""

    violation_type: ViolationType
    description: str
    severity: float  # 0.0-1.0, higher = more severe
    w_ethics_penalty: float  # Negative value to apply to W_ethics

    # Detection patterns (regex or keyword-based)
    keywords: List[str]
    context_required: bool = True  # Requires contextual analysis, not just keyword match


# ============================================================================
# Absolute Ethical Boundaries
# ============================================================================

VIOLATION_PATTERNS: Dict[ViolationType, ViolationPattern] = {
    ViolationType.RACIAL_SUPREMACY: ViolationPattern(
        violation_type=ViolationType.RACIAL_SUPREMACY,
        description="Claims of racial superiority or inferiority",
        severity=1.0,
        w_ethics_penalty=-1.0,  # Maximum penalty
        keywords=[
            "superior race", "inferior race", "racial hierarchy",
            "genetically superior", "inherently inferior",
            "natural slaves", "master race",
        ],
        context_required=True,
    ),

    ViolationType.ETHNIC_SUPREMACY: ViolationPattern(
        violation_type=ViolationType.ETHNIC_SUPREMACY,
        description="Claims of ethnic superiority or inferiority",
        severity=1.0,
        w_ethics_penalty=-1.0,
        keywords=[
            "superior ethnicity", "inferior culture", "ethnic purity",
            "cultural supremacy", "ethnic cleansing",
        ],
        context_required=True,
    ),

    ViolationType.RELIGIOUS_DEGRADATION: ViolationPattern(
        violation_type=ViolationType.RELIGIOUS_DEGRADATION,
        description="Degradation of human value based on religion",
        severity=0.9,
        w_ethics_penalty=-0.9,
        keywords=[
            "inferior faith", "heretic subhuman", "religious vermin",
            "deserve persecution", "religious inferiority",
        ],
        context_required=True,
    ),

    ViolationType.GENDER_ESSENTIALISM: ViolationPattern(
        violation_type=ViolationType.GENDER_ESSENTIALISM,
        description="Biological determinism justifying gender-based oppression",
        severity=0.8,
        w_ethics_penalty=-0.8,
        keywords=[
            "naturally inferior", "biologically suited for submission",
            "inherently irrational", "naturally submissive",
            "biological destiny",
        ],
        context_required=True,
    ),

    ViolationType.DISABILITY_DEHUMANIZATION: ViolationPattern(
        violation_type=ViolationType.DISABILITY_DEHUMANIZATION,
        description="Dehumanization based on disability or ability",
        severity=1.0,
        w_ethics_penalty=-1.0,
        keywords=[
            "life unworthy of life", "burden on society",
            "genetic defect", "should not reproduce",
            "mercy killing", "useless eaters",
        ],
        context_required=True,
    ),

    ViolationType.BIOLOGICAL_DETERMINISM: ViolationPattern(
        violation_type=ViolationType.BIOLOGICAL_DETERMINISM,
        description="Using biology to justify oppression or hierarchy",
        severity=0.9,
        w_ethics_penalty=-0.9,
        keywords=[
            "genetic destiny", "born to serve", "natural hierarchy",
            "evolutionary inferior", "biological caste",
        ],
        context_required=True,
    ),

    ViolationType.COLLECTIVE_PUNISHMENT: ViolationPattern(
        violation_type=ViolationType.COLLECTIVE_PUNISHMENT,
        description="Group-based guilt or punishment for immutable traits",
        severity=0.8,
        w_ethics_penalty=-0.8,
        keywords=[
            "all [GROUP] are guilty", "collective guilt",
            "punish the entire", "group responsibility",
            "inherited sin", "blood guilt",
        ],
        context_required=True,
    ),

    ViolationType.DEHUMANIZATION: ViolationPattern(
        violation_type=ViolationType.DEHUMANIZATION,
        description="Removing human dignity based on immutable characteristics",
        severity=1.0,
        w_ethics_penalty=-1.0,
        keywords=[
            "subhuman", "vermin", "parasites", "animals",
            "not fully human", "lesser beings",
        ],
        context_required=True,
    ),

    ViolationType.EXCLUSIONARY_FRAMING: ViolationPattern(
        violation_type=ViolationType.EXCLUSIONARY_FRAMING,
        description="Strong in-group/out-group division with value degradation",
        severity=0.7,
        w_ethics_penalty=-0.7,
        keywords=[
            "us versus them", "purify our group",
            "eliminate the other", "enemy within",
            "traitor to the race", "contamination",
        ],
        context_required=True,
    ),
}


@dataclass
class EthicsViolation:
    """Detected ethical boundary violation."""

    violation_type: ViolationType
    severity: float
    w_ethics_penalty: float
    matched_text: str
    context: str
    confidence: float  # 0.0-1.0
    timestamp: str


class WEthicsGuardian:
    """
    Guardian system for absolute ethical boundaries.

    This system monitors reasoning output and flags/stops sessions
    that violate fundamental ethical principles.
    """

    def __init__(self, auto_stop_threshold: float = 0.8):
        """
        Initialize ethics guardian.

        Args:
            auto_stop_threshold: W_ethics threshold below which to auto-stop
                               (e.g., 0.8 means stop if W_ethics < -0.8)
        """
        self.auto_stop_threshold = auto_stop_threshold
        self.violation_history: List[EthicsViolation] = []
        self.cumulative_w_ethics = 0.0
        self.dangerous_ideology_flag = False

    def check_text(
        self,
        text: str,
        context: Optional[str] = None,
    ) -> Dict:
        """
        Check text for ethical boundary violations.

        Args:
            text: Text to check
            context: Additional context for analysis

        Returns:
            Dict with:
            - violations: List[EthicsViolation]
            - w_ethics_delta: float (change to apply)
            - should_stop: bool (whether to stop session)
            - dangerous_ideology_flag: bool
        """
        violations = []
        total_penalty = 0.0

        text_lower = text.lower()
        context_lower = (context or "").lower()

        # Check each violation pattern
        for pattern in VIOLATION_PATTERNS.values():
            # Simple keyword detection (production would use more sophisticated NLP)
            for keyword in pattern.keywords:
                if keyword.lower() in text_lower:
                    # Found potential violation
                    # In production, would use contextual analysis here
                    confidence = self._assess_confidence(
                        text, keyword, context, pattern.context_required
                    )

                    if confidence > 0.5:  # Threshold for flagging
                        violation = EthicsViolation(
                            violation_type=pattern.violation_type,
                            severity=pattern.severity,
                            w_ethics_penalty=pattern.w_ethics_penalty,
                            matched_text=keyword,
                            context=text[:200],  # First 200 chars
                            confidence=confidence,
                            timestamp=self._get_timestamp(),
                        )
                        violations.append(violation)
                        total_penalty += pattern.w_ethics_penalty

                        # Flag if high-severity violation detected
                        if pattern.severity >= 0.8:
                            self.dangerous_ideology_flag = True

        # Update cumulative W_ethics
        self.cumulative_w_ethics += total_penalty

        # Determine if session should stop
        should_stop = abs(self.cumulative_w_ethics) > self.auto_stop_threshold

        # Add violations to history
        self.violation_history.extend(violations)

        return {
            "violations": violations,
            "w_ethics_delta": total_penalty,
            "cumulative_w_ethics": self.cumulative_w_ethics,
            "should_stop": should_stop,
            "dangerous_ideology_flag": self.dangerous_ideology_flag,
            "violation_count": len(violations),
        }

    def _assess_confidence(
        self,
        text: str,
        keyword: str,
        context: Optional[str],
        context_required: bool,
    ) -> float:
        """
        Assess confidence that a violation occurred.

        This is a simplified version. Production would use:
        - Semantic analysis
        - Intent detection
        - Historical context
        - Philosophical framework analysis
        """
        # Base confidence from keyword match
        confidence = 0.6

        # Check if it's in a negation context (e.g., "we must reject...")
        negation_words = ["reject", "oppose", "condemn", "wrong", "not", "never"]
        words_before = text[max(0, text.lower().find(keyword.lower()) - 50):
                           text.lower().find(keyword.lower())].lower()

        if any(neg in words_before for neg in negation_words):
            confidence *= 0.3  # Likely discussing/rejecting, not endorsing

        # Check if it's in an academic/critical context
        academic_markers = ["historically", "critique", "analysis", "example of"]
        if any(marker in words_before for marker in academic_markers):
            confidence *= 0.4  # Likely academic discussion

        return min(1.0, confidence)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def reset(self) -> None:
        """Reset guardian state (for new session)."""
        self.violation_history = []
        self.cumulative_w_ethics = 0.0
        self.dangerous_ideology_flag = False

    def get_violation_summary(self) -> Dict:
        """Get summary of all violations in current session."""
        violation_types = {}
        for v in self.violation_history:
            vtype = v.violation_type.value
            if vtype not in violation_types:
                violation_types[vtype] = 0
            violation_types[vtype] += 1

        return {
            "total_violations": len(self.violation_history),
            "violation_types": violation_types,
            "cumulative_w_ethics": self.cumulative_w_ethics,
            "dangerous_ideology_flag": self.dangerous_ideology_flag,
            "most_severe": max(
                (v.severity for v in self.violation_history),
                default=0.0
            ),
        }


def create_ethics_guardian(auto_stop_threshold: float = 0.8) -> WEthicsGuardian:
    """
    Factory function to create a WEthicsGuardian instance.

    Args:
        auto_stop_threshold: Cumulative W_ethics threshold for auto-stop

    Returns:
        WEthicsGuardian instance
    """
    return WEthicsGuardian(auto_stop_threshold=auto_stop_threshold)


# Export for use in other modules
__all__ = [
    "ViolationType",
    "ViolationPattern",
    "EthicsViolation",
    "WEthicsGuardian",
    "create_ethics_guardian",
    "VIOLATION_PATTERNS",
]
