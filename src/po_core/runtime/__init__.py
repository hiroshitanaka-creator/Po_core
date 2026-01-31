"""
Po_core Runtime
===============

Runtime configuration and dependency wiring.

This module is responsible for:
1. Assembling concrete implementations (wiring.py)
2. Configuration management (settings.py)

DEPENDENCY RULES:
- runtime/ CAN import from: ports/, adapters/, domain/
- runtime/ is the ONLY place that assembles concrete implementations
- Core modules should receive dependencies via function parameters

Usage:
    from po_core.runtime import build_system, Settings

    # Build a wired system
    system = build_system(memory=poself_instance, settings=Settings())

    # Access components
    snapshot = system.memory_read.snapshot(ctx)
"""

from po_core.runtime.settings import Settings
from po_core.runtime.wiring import WiredSystem, build_system, build_test_system

__all__ = [
    "Settings",
    "WiredSystem",
    "build_system",
    "build_test_system",
]
