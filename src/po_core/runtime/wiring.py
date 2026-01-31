"""
Dependency Wiring
=================

Assembles concrete implementations and provides dependency injection.

This is the ONLY file that should:
1. Import concrete implementations from adapters/
2. Create instances with specific configurations
3. Wire dependencies together

Core modules receive dependencies as parameters, not through imports.

IMPORTANT: wiring.py 以外で adapter/具象を import し始めたら、即スパゲッティ再発。

Usage:
    from po_core.runtime.wiring import build_system

    system = build_system(memory=poself_instance, settings=Settings())
    result = system.memory_read.snapshot(ctx)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from po_core.ports.aggregator import AggregatorPort
from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryWritePort
from po_core.ports.solarwill import SolarWillPort
from po_core.ports.tensor_engine import TensorEnginePort
from po_core.ports.trace import TracePort
from po_core.ports.wethics_gate import WethicsGatePort
from po_core.philosophers.base import PhilosopherProtocol
from po_core.runtime.settings import Settings


@dataclass(frozen=True)
class WiredSystem:
    """
    Wired dependency container.

    Contains all dependencies needed for the vertical slice pipeline.
    """

    memory_read: MemoryReadPort
    memory_write: MemoryWritePort
    tracer: TracePort
    tensor_engine: TensorEnginePort
    solarwill: SolarWillPort
    gate: WethicsGatePort
    philosophers: Sequence[PhilosopherProtocol]
    aggregator: AggregatorPort
    settings: Settings


def build_system(*, memory: object, settings: Settings) -> WiredSystem:
    """
    Build a wired system with all dependencies.

    Args:
        memory: Po_self などの具象（adapterで包む）
        settings: Application settings

    Returns:
        WiredSystem with all dependencies wired
    """
    from po_core.adapters.memory_poself import PoSelfMemoryAdapter
    from po_core.trace.noop import NoopTracer
    from po_core.tensors.engine import TensorEngine
    from po_core.autonomy.solarwill.engine import SolarWillEngine
    from po_core.safety.wethics_gate.policy_gate import PolicyWethicsGate
    from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
    from po_core.safety.wethics_gate.action_gate import PolicyActionGate
    from po_core.safety.wethics_gate.policies.presets import (
        default_intention_policies,
        default_action_policies,
    )
    from po_core.philosophers.registry import build_philosophers
    from po_core.aggregator.weighted_vote import WeightedVoteAggregator

    mem = PoSelfMemoryAdapter(memory)

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
        tracer=NoopTracer(),
        tensor_engine=TensorEngine(metrics=()),
        solarwill=SolarWillEngine(),
        gate=PolicyWethicsGate(
            intention=PolicyIntentionGate(policies=default_intention_policies()),
            action=PolicyActionGate(policies=default_action_policies()),
        ),
        philosophers=build_philosophers(),
        aggregator=WeightedVoteAggregator(),
        settings=settings,
    )


def build_test_system(settings: Settings | None = None) -> WiredSystem:
    """
    Build a wired system for testing (uses in-memory adapters).

    Args:
        settings: Optional settings override

    Returns:
        WiredSystem with in-memory implementations
    """
    from po_core.adapters.memory_poself import InMemoryAdapter
    from po_core.trace.in_memory import InMemoryTracer
    from po_core.tensors.engine import TensorEngine
    from po_core.autonomy.solarwill.engine import SolarWillEngine
    from po_core.safety.wethics_gate.policy_gate import PolicyWethicsGate
    from po_core.safety.wethics_gate.intention_gate import PolicyIntentionGate
    from po_core.safety.wethics_gate.action_gate import PolicyActionGate
    from po_core.safety.wethics_gate.policies.presets import (
        default_intention_policies,
        default_action_policies,
    )
    from po_core.philosophers.registry import build_philosophers
    from po_core.aggregator.weighted_vote import WeightedVoteAggregator

    settings = settings or Settings()
    mem = InMemoryAdapter()

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
        tracer=InMemoryTracer(),
        tensor_engine=TensorEngine(metrics=()),
        solarwill=SolarWillEngine(),
        gate=PolicyWethicsGate(
            intention=PolicyIntentionGate(policies=default_intention_policies()),
            action=PolicyActionGate(policies=default_action_policies()),
        ),
        philosophers=build_philosophers(),
        aggregator=WeightedVoteAggregator(),
        settings=settings,
    )


__all__ = [
    "WiredSystem",
    "build_system",
    "build_test_system",
]
