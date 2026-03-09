from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11
    import tomli as tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_version_is_stable_030() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    assert project["version"] == "0.3.0"
    assert "Development Status :: 5 - Production/Stable" in project["classifiers"]


def test_quickstart_has_release_build_commands() -> None:
    quickstart = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    assert "python -m build" in quickstart
    assert "twine check dist/*" in quickstart


def test_pytest_config_single_source_of_truth() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    tool_config = pyproject.get("tool", {})

    pytest_config = tool_config.get("pytest")
    assert pytest_config is None or "ini_options" not in pytest_config

    pytest_ini = ROOT / "pytest.ini"
    assert pytest_ini.exists()
    assert "[pytest]" in pytest_ini.read_text(encoding="utf-8")
