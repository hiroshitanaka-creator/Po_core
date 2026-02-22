"""Root-level test configuration and shared fixtures."""

import pytest

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal


@pytest.fixture
def basic_prompt():
    """Basic philosophical prompt for testing."""
    return "What does it mean to live authentically?"


@pytest.fixture
def ethical_prompt():
    """Ethical dilemma prompt."""
    return "Should I sacrifice personal happiness for the greater good?"


@pytest.fixture
def empty_prompt():
    """Empty prompt for edge-case testing."""
    return ""


@pytest.fixture
def make_context():
    """Factory fixture for creating Context objects."""

    def _make(user_input="What is justice?", request_id="test-req-001"):
        return Context.now(
            request_id=request_id,
            user_input=user_input,
            meta={"entry": "test"},
        )

    return _make


@pytest.fixture
def make_proposal():
    """Factory fixture for creating Proposal objects."""

    def _make(
        proposal_id="p1",
        action_type="answer",
        content="This is a test response.",
        confidence=0.7,
        tags=None,
        extra=None,
    ):
        return Proposal(
            proposal_id=proposal_id,
            action_type=action_type,
            content=content,
            confidence=confidence,
            assumption_tags=tags or [],
            risk_tags=[],
            extra=extra or {},
        )

    return _make


import asyncio


def pytest_pyfunc_call(pyfuncitem):
    """Minimal asyncio marker support without external pytest-asyncio plugin."""
    if pyfuncitem.get_closest_marker("asyncio") is None:
        return None

    test_func = pyfuncitem.obj
    if not asyncio.iscoroutinefunction(test_func):
        return None

    kwargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
    asyncio.run(test_func(**kwargs))
    return True
