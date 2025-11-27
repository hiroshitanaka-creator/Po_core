"""
Po_core Safety System
=====================

Comprehensive safety framework for philosophical reasoning:

1. **Philosopher Profiles** (philosopher_profiles.py)
   - Safety tier classification (TRUSTED, RESTRICTED, MONITORED)
   - Risk factor identification
   - Usage validation

2. **W_ethics Boundaries** (w_ethics.py)
   - Absolute ethical red lines
   - Automatic violation detection
   - Session auto-stop on severe violations

Purpose: Enable legitimate research while preventing misuse.
"""

from po_core.safety.philosopher_profiles import (
    SafetyTier,
    EthicalRiskPattern,
    PHILOSOPHER_SAFETY_PROFILES,
    get_trusted_philosophers,
    get_restricted_philosophers,
    get_monitored_philosophers,
    is_safe_for_general_use,
    requires_dangerous_pattern_mode,
    get_risk_factors,
    validate_philosopher_group,
)

from po_core.safety.w_ethics import (
    ViolationType,
    ViolationPattern,
    EthicsViolation,
    WEthicsGuardian,
    create_ethics_guardian,
    VIOLATION_PATTERNS,
)

__all__ = [
    # Philosopher profiles
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

    # W_ethics boundaries
    "ViolationType",
    "ViolationPattern",
    "EthicsViolation",
    "WEthicsGuardian",
    "create_ethics_guardian",
    "VIOLATION_PATTERNS",
]
