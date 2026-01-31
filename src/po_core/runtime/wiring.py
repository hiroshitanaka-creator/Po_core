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

from po_core.ports.memory_read import MemoryReadPort
from po_core.ports.memory_write import MemoryWritePort
from po_core.runtime.settings import Settings


@dataclass(frozen=True)
class WiredSystem:
    """
    Wired dependency container.

    ここに engine/gate/registry/tracer などを束ねる（後で増える）。
    ensembleは"面"しか見ない。
    """

    memory_read: MemoryReadPort
    memory_write: MemoryWritePort
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

    mem = PoSelfMemoryAdapter(memory)

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
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

    settings = settings or Settings()
    mem = InMemoryAdapter()

    return WiredSystem(
        memory_read=mem,
        memory_write=mem,
        settings=settings,
    )


__all__ = [
    "WiredSystem",
    "build_system",
    "build_test_system",
]
