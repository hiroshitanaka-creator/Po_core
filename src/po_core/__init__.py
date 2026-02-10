"""
Po_core: Philosophy-Driven AI System

A system that integrates philosophers as dynamic tensors
for responsible meaning generation.

Philosophy: Flying Pig - When Pigs Fly

Public API:
    from po_core.app.api import run          # Recommended entry point
    from po_core import PoSelf, PoSelfResponse  # High-level wrapper
"""

__version__ = "0.1.0-alpha"
__author__ = "Flying Pig Project"
__email__ = "flyingpig0229+github@gmail.com"

# ── Modern API (recommended) ──
from po_core.app.api import run

# ── Legacy exports (backward compat) ──
from po_core.ensemble import PHILOSOPHER_REGISTRY
from po_core.po_self import PoSelf, PoSelfResponse
from po_core.po_system_prompt import (
    EVALUATION_RUBRIC,
    PO_CORE_SYSTEM_PROMPT,
    STRESS_TEST_CONCEPTS,
    TEST_QUESTIONS,
    build_stress_test_prompt,
    build_user_prompt,
)
from po_core.po_test_runner import PoTestRunner, TestReport, TestResult
from po_core.po_trace import EventType, PoTrace

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
    # Testing
    "PO_CORE_SYSTEM_PROMPT",
    "TEST_QUESTIONS",
    "STRESS_TEST_CONCEPTS",
    "EVALUATION_RUBRIC",
    "build_user_prompt",
    "build_stress_test_prompt",
    "PoTestRunner",
    "TestResult",
    "TestReport",
]
