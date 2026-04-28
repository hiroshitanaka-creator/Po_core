"""
Po_core: Philosophy-Driven AI System

A system that integrates philosophers as dynamic tensors
for responsible meaning generation.

Philosophy: Flying Pig - When Pigs Fly

Public API:
    from po_core import run                     # Recommended entry point (lazy import)
    from po_core import PoSelf, PoSelfResponse  # High-level wrapper
"""

__version__ = "1.0.3"
__author__ = "Flying Pig Project"
__email__ = "flyingpig0229+github@gmail.com"


# ── Modern API (recommended, lazy wrapper to avoid heavy import-time side effects) ──
def run(*args, **kwargs):
    from po_core.app.api import run as _run

    return _run(*args, **kwargs)


def run_case(*args, **kwargs):
    from po_core.app.api import run_case as _run_case

    return _run_case(*args, **kwargs)


# ── Legacy exports (backward compat) ──
from po_core.ensemble import PHILOSOPHER_REGISTRY
from po_core.po_self import PoSelf, PoSelfResponse
from po_core.po_trace import EventType, PoTrace

__all__ = [
    "__version__",
    # Modern API (recommended)
    "run",
    "run_case",
    # Registry
    "PHILOSOPHER_REGISTRY",
    # Tracing
    "PoTrace",
    "EventType",
    # Self
    "PoSelf",
    "PoSelfResponse",
]
