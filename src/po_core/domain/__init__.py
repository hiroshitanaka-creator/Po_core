"""
Po_core Domain Layer
====================

This module contains the shared data types (value objects, DTOs) that form
the common language between all Po_core subsystems.

CRITICAL RULE: This module has NO DEPENDENCIES on other po_core modules.
It only uses standard library, typing, and dataclasses.

Dependency Direction (INVIOLABLE):
    domain/ <- philosophers/
    domain/ <- tensors/
    domain/ <- safety/
    domain/ <- trace/
    domain/ <- ensemble.py

    domain/ -> NOTHING (except stdlib)

This is the "ground" that all other modules stand on.

Contents:
- Context: Input context for reasoning
- Proposal: Philosopher proposals
- TensorSnapshot: Tensor measurement snapshots
- SafetyVerdict: Safety gate verdicts
- TraceEvent: Trace events for audit trail
"""

from po_core.domain.context import (
    Context,
    ContextBuilder,
)
from po_core.domain.proposal import (
    Proposal,
    ProposalSource,
    Rationale,
)
from po_core.domain.tensor_snapshot import (
    TensorSnapshot,
    TensorValue,
)
from po_core.domain.safety_verdict import (
    SafetyVerdict,
    VerdictType,
    ViolationInfo,
)
from po_core.domain.trace_event import (
    TraceEvent,
    TraceEventType,
)


__all__ = [
    # Context
    "Context",
    "ContextBuilder",
    # Proposals
    "Proposal",
    "ProposalSource",
    "Rationale",
    # Tensors
    "TensorSnapshot",
    "TensorValue",
    # Safety
    "SafetyVerdict",
    "VerdictType",
    "ViolationInfo",
    # Trace
    "TraceEvent",
    "TraceEventType",
]
