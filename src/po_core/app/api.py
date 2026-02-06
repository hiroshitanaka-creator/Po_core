"""
Po_core Public API
==================

This is the ONLY public entry point for the Po_core system.
All external consumers (03_api/*, examples/*, tests) should import from here.

入口はここに統一。03_api/* と examples/* はこの関数を呼ぶだけにする。

Usage:
    from po_core.app.api import run

    result = run(
        user_input="What is justice?",
        memory_backend=poself_instance,
        settings=Settings(),
    )

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  External (03_api/, examples/*, tests)                  │
    │  ↓ ONLY imports po_core.app.api                         │
    ├─────────────────────────────────────────────────────────┤
    │  po_core.app.api  ← THIS FILE (facade)                  │
    │  ↓ uses runtime/wiring.py → ensemble.run_turn           │
    ├─────────────────────────────────────────────────────────┤
    │  Internal (philosophers, tensors, safety, autonomy)     │
    │  ↓ never imported directly from outside                 │
    └─────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import uuid

from po_core.domain.context import Context
from po_core.ensemble import EnsembleDeps, run_turn
from po_core.runtime.settings import Settings
from po_core.runtime.wiring import build_system, build_test_system


def run(
    user_input: str,
    *,
    memory_backend: object | None = None,
    settings: Settings | None = None,
) -> dict:
    """
    Main entry point for Po_core.

    入口はここに統一。03_api/* と examples/* はこの関数を呼ぶだけにする。

    Args:
        user_input: The user's input prompt
        memory_backend: Po_self or compatible memory backend (None for testing)
        settings: Application settings (None for defaults)

    Returns:
        Result dictionary with request_id, status, and proposal or verdict
    """
    settings = settings or Settings()

    # Build wired system
    if memory_backend is not None:
        system = build_system(memory=memory_backend, settings=settings)
    else:
        system = build_test_system(settings=settings)

    # Create context
    ctx = Context.now(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        meta={"entry": "app.api"},
    )

    # Build dependencies for run_turn
    deps = EnsembleDeps(
        memory_read=system.memory_read,
        memory_write=system.memory_write,
        tracer=system.tracer,
        tensors=system.tensor_engine,
        solarwill=system.solarwill,
        gate=system.gate,
        philosophers=system.philosophers,  # Backward compat
        aggregator=system.aggregator,
        aggregator_shadow=system.aggregator_shadow,  # Shadow Pareto A/B
        registry=system.registry,  # SafetyMode-based selection
        settings=system.settings,  # Worker/timeout config
        shadow_guard=system.shadow_guard,  # ShadowGuard (自律ブレーキ)
    )

    # Run the full pipeline
    return run_turn(ctx, deps)


__all__ = ["run"]
