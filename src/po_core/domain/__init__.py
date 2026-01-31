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
    domain/ <- autonomy/
    domain/ <- ensemble.py

    domain/ -> NOTHING (except stdlib)

This is the "ground" that all other modules stand on.

Contents:
- Context: 意思決定1回分のコンテキスト（監査の単位）
- Intent: SolarWillの出力（意図・目標候補）
- Proposal: philosopher/aggregatorの成果物
- TensorSnapshot: tensors層の出力スナップショット
- SafetyVerdict: Gateの判定結果
- TraceEvent: 観測可能性の単位
- MemorySnapshot: 読み取り専用メモリビュー
"""

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemoryItem, MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.domain.trace_event import TraceEvent


__all__ = [
    # Context
    "Context",
    # Intent (SolarWill output)
    "Intent",
    # Memory
    "MemoryItem",
    "MemorySnapshot",
    # Proposals
    "Proposal",
    # Tensors
    "TensorSnapshot",
    # Safety
    "Decision",
    "SafetyVerdict",
    # Trace
    "TraceEvent",
]
