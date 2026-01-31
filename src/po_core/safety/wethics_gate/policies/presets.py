"""
Policy Presets
==============

Bundles of policies for easy wiring.
This is the extension point for adding new policies.
"""
from __future__ import annotations

from typing import List

from po_core.safety.wethics_gate.policies.base import ActionPolicy, IntentionPolicy
from po_core.safety.wethics_gate.policies.intention_goalkey_001 import IntentGoalKeywordGuardPolicy
from po_core.safety.wethics_gate.policies.action_acttype_001 import ActionTypeAllowlistPolicy
from po_core.safety.wethics_gate.policies.action_outguard_001 import DangerousOutputGuardPolicy


def default_intention_policies() -> List[IntentionPolicy]:
    """Get default intention-stage policies."""
    return [
        IntentGoalKeywordGuardPolicy(),
    ]


def default_action_policies() -> List[ActionPolicy]:
    """Get default action-stage policies."""
    return [
        ActionTypeAllowlistPolicy(),
        DangerousOutputGuardPolicy(),
    ]


__all__ = ["default_intention_policies", "default_action_policies"]
