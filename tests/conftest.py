"""Test configuration for Po_core.

Provides a lightweight fallback for coverage flags when pytest-cov is not
installed in constrained environments.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def pytest_addoption(parser: Any) -> None:  # pragma: no cover - helper
    if importlib.util.find_spec("pytest_cov") is not None:
        return

    parser.addoption("--cov", action="append", default=[], help="(stub) coverage target")
    parser.addoption(
        "--cov-report", action="append", default=[], help="(stub) coverage report"
    )
