"""
Po_core: Philosophy-Driven AI System

A system that integrates philosophers as dynamic tensors
for responsible meaning generation.

Philosophy: Flying Pig - When Pigs Fly

Public API:
    from po_core.app.api import run          # Recommended entry point
    from po_core import PoSelf, PoSelfResponse  # High-level wrapper
"""

__version__ = "1.0.2"
__author__ = "Flying Pig Project"
__email__ = "flyingpig0229+github@gmail.com"

# ── Modern API (recommended) ──
from po_core.app.api import run

# ── Core exports ──
from po_core.ensemble import PHILOSOPHER_REGISTRY
from po_core.po_self import PoSelf, PoSelfResponse
from po_core.po_test_runner import PoTestRunner, TestReport, TestResult
from po_core.po_trace import EventType, PoTrace

# NOTE: po_system_prompt (20-philosopher test framework for Claude API evaluation)
# is intentionally NOT exported here. Import directly from po_core.po_system_prompt
# if needed for testing/evaluation purposes.

__all__ = [
    "__version__",
    # Modern API (recommended)
    "run",
    # Registry
    "PHILOSOPHER_REGISTRY",
    # Tracing
    "PoTrace",
    "EventType",
    # Self
    "PoSelf",
    "PoSelfResponse",
    # Testing utilities
    "PoTestRunner",
    "TestResult",
    "TestReport",
]
