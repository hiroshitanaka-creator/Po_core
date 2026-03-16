from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11
    import tomli as tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_version_stays_on_current_line() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    assert project["version"] == "1.0.2"
    assert "Development Status :: 5 - Production/Stable" in project["classifiers"]


def test_quickstart_has_release_build_commands() -> None:
    quickstart = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    assert "python -m build" in quickstart
    assert "twine check dist/*" in quickstart


def test_quickstart_install_examples_are_valid_for_current_release() -> None:
    quickstart = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    assert 'pip install "po-core-flyingpig==1.0.2"' in quickstart
    assert 'pip install -e ".[api]"' not in quickstart
