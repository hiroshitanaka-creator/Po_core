import pytest

from po_core.ensemble import DEFAULT_PHILOSOPHERS


@pytest.fixture()
def expected_philosophers():
    """Default set of philosophers used in deterministic tests."""

    return DEFAULT_PHILOSOPHERS
