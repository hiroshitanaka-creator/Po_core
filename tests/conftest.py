import sys
from pathlib import Path

# Ensure src directory is importable for tests without installation
ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))


def pytest_addoption(parser):
    """Provide stubs for coverage options when pytest-cov is unavailable."""

    parser.addoption("--cov", action="append", default=[])
    parser.addoption("--cov-report", action="append", default=[])
