"""
Policy Presets
==============

Bundles of policies for easy wiring.
This is the extension point for adding new policies.
"""

from __future__ import annotations

from typing import List, cast

from po_core.safety.wethics_gate.policies.action_acttype_001 import (
    ActionTypeAllowlistPolicy,
)
from po_core.safety.wethics_gate.policies.action_mode_001 import ActionModeDegradePolicy
from po_core.safety.wethics_gate.policies.action_outguard_001 import (
    DangerousOutputGuardPolicy,
)
from po_core.safety.wethics_gate.policies.base import ActionPolicy, IntentionPolicy
from po_core.safety.wethics_gate.policies.intention_goalkey_001 import (
    IntentGoalKeywordGuardPolicy,
)
from po_core.safety.wethics_gate.policies.intention_mode_001 import (
    IntentModeDegradePolicy,
)


def default_intention_policies() -> List[IntentionPolicy]:
    """Get default intention-stage policies (sorted by priority at runtime)."""
    return [
        cast(IntentionPolicy, IntentModeDegradePolicy()),  # priority=5: safety mode first
        cast(IntentionPolicy, IntentGoalKeywordGuardPolicy()),  # priority=10
    ]


def default_action_policies() -> List[ActionPolicy]:
    """Get default action-stage policies (sorted by priority at runtime)."""
    return [
        cast(ActionPolicy, ActionTypeAllowlistPolicy()),  # priority=10
        cast(ActionPolicy, ActionModeDegradePolicy()),  # priority=15
        cast(ActionPolicy, DangerousOutputGuardPolicy()),  # priority=20
    ]


__all__ = ["default_intention_policies", "default_action_policies"]
