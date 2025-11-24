"""Test configuration shims for offline environments."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register noop coverage options so pytest runs without pytest-cov installed."""

    parser.addoption("--cov", action="store", default=None, help="No-op coverage option")
    parser.addoption("--cov-report", action="append", default=[], help="No-op coverage report option")
