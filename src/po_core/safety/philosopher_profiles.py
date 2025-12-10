"""
Philosopher Safety Profiles
============================

Classify philosophers into safety tiers:
- TRUSTED: Safe for all reasoning contexts
- RESTRICTED: Research-only, requires explicit dangerous pattern detection mode
- MONITORED: Requires extra ethical oversight

This prevents misuse while enabling legitimate research.
"""
from enum import Enum
from typing import Dict, List, Set


class SafetyTier(str, Enum):
    """Safety classification for philosophers."""

    TRUSTED = "trusted"           # Safe for general use
    RESTRICTED = "restricted"     # Research only, dangerous pattern detection mode
    MONITORED = "monitored"       # Requires extra ethical oversight


class EthicalRiskPattern(str, Enum):
    """Known ethical risk patterns."""

    SUPREMACY_IDEOLOGY = "supremacy_ideology"           # Racial/ethnic superiority claims
    EXCLUSIONARY_FRAMING = "exclusionary_framing"       # In-group/out-group division
    DEHUMANIZATION = "dehumanization"                   # Reducing human dignity
    ABSOLUTE_AUTHORITY = "absolute_authority"           # Unchecked power justification
    COLLECTIVE_PUNISHMENT = "collective_punishment"     # Group-based judgment
    BIOLOGICAL_DETERMINISM = "biological_determinism"   # Innate inferiority claims


# Philosopher safety classifications
PHILOSOPHER_SAFETY_PROFILES: Dict[str, Dict] = {
    # TRUSTED: Ethically grounded, humanistic, diverse perspectives
    "aristotle": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["virtue", "human_flourishing", "practical_wisdom"],
        "risk_factors": [],
    },
    "confucius": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["harmony", "reciprocity", "benevolence"],
        "risk_factors": [],
    },
    "dewey": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["democracy", "education", "social_progress"],
        "risk_factors": [],
    },
    "arendt": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["human_dignity", "political_freedom", "totalitarianism_critique"],
        "risk_factors": [],
    },
    "levinas": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["responsibility_for_other", "face_to_face_ethics"],
        "risk_factors": [],
    },
    "wabi_sabi": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["imperfection", "transience", "humility"],
        "risk_factors": [],
    },
    "watsuji": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["relationality", "betweenness", "climate_ethics"],
        "risk_factors": [],
    },
    "zhuangzi": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["spontaneity", "perspective_relativism", "dao"],
        "risk_factors": [],
    },
    "sartre": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["freedom", "responsibility", "bad_faith_critique"],
        "risk_factors": [],
    },
    "wittgenstein": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["language_limits", "anti_dogmatism"],
        "risk_factors": [],
    },
    "peirce": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["scientific_method", "fallibilism", "community_inquiry"],
        "risk_factors": [],
    },
    "merleau_ponty": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["embodiment", "perception", "intersubjectivity"],
        "risk_factors": [],
    },
    "jung": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["individuation", "shadow_integration", "collective_unconscious"],
        "risk_factors": ["archetypal_essentialism"],  # Minor risk: overgeneralization
    },
    "kierkegaard": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["individual_authenticity", "ethical_stage", "faith"],
        "risk_factors": [],
    },
    "deleuze": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["difference", "multiplicity", "becoming"],
        "risk_factors": [],
    },
    "derrida": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["deconstruction", "hospitality", "justice_to_come"],
        "risk_factors": [],
    },
    "badiou": {
        "tier": SafetyTier.TRUSTED,
        "ethical_anchors": ["truth_event", "fidelity", "generic_universalism"],
        "risk_factors": [],
    },
    "lacan": {
        "tier": SafetyTier.MONITORED,
        "ethical_anchors": ["subject_formation", "desire", "symbolic_order"],
        "risk_factors": ["obscurity", "determinism_risk"],
        "monitoring_reason": "Complex psychoanalytic concepts require careful contextualization",
    },

    # MONITORED: Require careful interpretation
    "heidegger": {
        "tier": SafetyTier.MONITORED,
        "ethical_anchors": ["being", "dasein", "authentic_existence"],
        "risk_factors": ["political_history", "exclusionary_potential"],
        "monitoring_reason": "Historical association with National Socialism requires ethical oversight",
        "safe_contexts": ["ontology", "phenomenology", "technology_critique"],
        "restricted_contexts": ["political_philosophy", "community_identity"],
    },

    # RESTRICTED: Research only, dangerous pattern detection mode
    "nietzsche": {
        "tier": SafetyTier.RESTRICTED,
        "ethical_anchors": ["life_affirmation", "perspectivism", "self_overcoming"],
        "risk_factors": [
            EthicalRiskPattern.SUPREMACY_IDEOLOGY,
            EthicalRiskPattern.EXCLUSIONARY_FRAMING,
            "historical_misappropriation",
        ],
        "restriction_reason": "Ubermensch and will-to-power concepts historically misused for supremacist ideology",
        "safe_contexts": [
            "critique_of_morality",
            "aesthetic_philosophy",
            "existential_meaning",
        ],
        "dangerous_contexts": [
            "political_hierarchy",
            "racial_superiority",
            "social_darwinism",
        ],
        "requires_oversight": True,
    },
}


def get_trusted_philosophers() -> List[str]:
    """Get list of all TRUSTED tier philosophers."""
    return [
        name for name, profile in PHILOSOPHER_SAFETY_PROFILES.items()
        if profile["tier"] == SafetyTier.TRUSTED
    ]


def get_restricted_philosophers() -> List[str]:
    """Get list of RESTRICTED tier philosophers."""
    return [
        name for name, profile in PHILOSOPHER_SAFETY_PROFILES.items()
        if profile["tier"] == SafetyTier.RESTRICTED
    ]


def get_monitored_philosophers() -> List[str]:
    """Get list of MONITORED tier philosophers."""
    return [
        name for name, profile in PHILOSOPHER_SAFETY_PROFILES.items()
        if profile["tier"] == SafetyTier.MONITORED
    ]


def is_safe_for_general_use(philosopher: str) -> bool:
    """Check if philosopher is safe for general use without restrictions."""
    profile = PHILOSOPHER_SAFETY_PROFILES.get(philosopher)
    if not profile:
        return False  # Unknown philosopher → default to restricted

    return profile["tier"] == SafetyTier.TRUSTED


def requires_dangerous_pattern_mode(philosophers: List[str]) -> bool:
    """Check if any philosopher in the group requires dangerous pattern detection mode."""
    return any(
        PHILOSOPHER_SAFETY_PROFILES.get(phil, {}).get("tier") == SafetyTier.RESTRICTED
        for phil in philosophers
    )


def get_risk_factors(philosopher: str) -> List[str]:
    """Get risk factors for a philosopher."""
    profile = PHILOSOPHER_SAFETY_PROFILES.get(philosopher, {})
    return profile.get("risk_factors", [])


def validate_philosopher_group(
    philosophers: List[str],
    allow_restricted: bool = False,
    dangerous_pattern_mode: bool = False
) -> Dict:
    """
    Validate a group of philosophers for safety.

    Args:
        philosophers: List of philosopher names
        allow_restricted: Whether to allow RESTRICTED tier philosophers
        dangerous_pattern_mode: Whether dangerous pattern detection is enabled

    Returns:
        Validation result with warnings and restrictions
    """
    result = {
        "valid": True,
        "warnings": [],
        "restrictions": [],
        "requires_oversight": False,
        "blocked_philosophers": [],
    }

    for phil in philosophers:
        profile = PHILOSOPHER_SAFETY_PROFILES.get(phil)

        if not profile:
            result["warnings"].append(f"Unknown philosopher: {phil}")
            continue

        tier = profile["tier"]

        if tier == SafetyTier.RESTRICTED:
            if not allow_restricted:
                result["valid"] = False
                result["blocked_philosophers"].append(phil)
                result["restrictions"].append(
                    f"{phil}: RESTRICTED tier - requires explicit dangerous pattern detection mode"
                )
            elif not dangerous_pattern_mode:
                result["valid"] = False
                result["restrictions"].append(
                    f"{phil}: RESTRICTED tier - dangerous pattern detection mode must be enabled"
                )
            else:
                result["warnings"].append(
                    f"{phil}: RESTRICTED tier active - enhanced ethical monitoring enabled"
                )
                result["requires_oversight"] = True

        elif tier == SafetyTier.MONITORED:
            result["warnings"].append(
                f"{phil}: MONITORED tier - {profile.get('monitoring_reason', 'Requires oversight')}"
            )
            result["requires_oversight"] = True

        # Check risk factors
        risk_factors = profile.get("risk_factors", [])
        if risk_factors:
            result["warnings"].append(
                f"{phil}: Risk factors present: {', '.join(str(r) for r in risk_factors)}"
            )

    return result


# Export for use in other modules
__all__ = [
    "SafetyTier",
    "EthicalRiskPattern",
    "PHILOSOPHER_SAFETY_PROFILES",
    "get_trusted_philosophers",
    "get_restricted_philosophers",
    "get_monitored_philosophers",
    "is_safe_for_general_use",
    "requires_dangerous_pattern_mode",
    "get_risk_factors",
    "validate_philosopher_group",
]
