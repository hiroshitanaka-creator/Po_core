"""
Po_core: Philosophy-Driven AI System

A system that integrates philosophers as dynamic tensors
for responsible meaning generation.

Philosophy: Flying Pig - When Pigs Fly
"""

__version__ = "0.1.0-alpha"
__author__ = "Flying Pig Project"
__email__ = "flyingpig0229+github@gmail.com"

# Core exports
from po_core.ensemble import run_ensemble, PHILOSOPHER_REGISTRY
from po_core.po_trace import PoTrace, EventType
from po_core.po_self import PoSelf, PoSelfResponse
from po_core.po_system_prompt import (
    PO_CORE_SYSTEM_PROMPT,
    TEST_QUESTIONS,
    STRESS_TEST_CONCEPTS,
    EVALUATION_RUBRIC,
    build_user_prompt,
    build_stress_test_prompt,
)
from po_core.po_test_runner import PoTestRunner, TestResult, TestReport

__all__ = [
    "__version__",
    # Ensemble
    "run_ensemble",
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
