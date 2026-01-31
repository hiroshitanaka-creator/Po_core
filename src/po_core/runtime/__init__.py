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
    from po_core.runtime import get_container

    # Get the wired container
    container = get_container()

    # Access components
    memory = container.memory
    gate = container.gate
"""

from po_core.runtime.wiring import (
    Container,
    get_container,
    configure,
)
from po_core.runtime.settings import (
    Settings,
    get_settings,
)

__all__ = [
    "Container",
    "get_container",
    "configure",
    "Settings",
    "get_settings",
]
