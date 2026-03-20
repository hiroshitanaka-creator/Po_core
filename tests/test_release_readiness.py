from __future__ import annotations

import ast
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.2"
ENTRYPOINTS = ["po-core", "po-self", "po-trace", "po-interactive", "po-experiment"]
DOCS_WITH_VERSION = [
    "README.md",
    "QUICKSTART.md",
    "QUICKSTART_EN.md",
    "CHANGELOG.md",
    "REPOSITORY_STRUCTURE.md",
    "docs/operations/publish_playbook.md",
]


def _read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def test_release_version_ssot_is_package_version() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    assert pyproject["project"]["dynamic"] == ["version"]
    assert pyproject["tool"]["setuptools"]["dynamic"]["version"]["attr"] == "po_core.__version__"

    package_init = _read("src/po_core/__init__.py")
    match = re.search(r'__version__ = "([^"]+)"', package_init)
    assert match is not None
    assert match.group(1) == VERSION


def test_release_docs_are_synced_to_current_version() -> None:
    for relpath in DOCS_WITH_VERSION:
        text = _read(relpath)
        assert VERSION in text, f"{relpath} must mention {VERSION}"
        if relpath != "CHANGELOG.md":
            assert "0.2.0b4" not in text, f"{relpath} still contains stale beta version"


def test_openapi_version_matches_package_version() -> None:
    server_py = _read("src/po_core/app/rest/server.py")
    assert "version=__version__" in server_py


def test_release_docs_use_consistent_philosopher_counts() -> None:
    readme = _read("README.md")
    quickstart_ja = _read("QUICKSTART.md")
    quickstart_en = _read("QUICKSTART_EN.md")
    repo_structure = _read("REPOSITORY_STRUCTURE.md")

    assert "42 philosophers" in readme
    assert "Po_coreでは **42人**の哲学者" in quickstart_ja
    assert "Po_core integrates **42 philosophers**" in quickstart_en
    assert "39 active" in quickstart_en
    assert "39 philosophers" not in quickstart_en
    assert "42 philosopher modules" in repo_structure


def test_requirements_files_delegate_to_pyproject_truth_source() -> None:
    assert _read("requirements.txt").strip().endswith("-e .")
    assert _read("requirements-dev.txt").strip().endswith("-e .[dev]")


def test_optional_all_extra_is_not_self_referential() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    all_extra = pyproject["project"]["optional-dependencies"]["all"]
    assert all("po-core-flyingpig" not in dep for dep in all_extra)


def test_prompt_runtime_ssot_is_python_persona_registry() -> None:
    guide = _read("src/po_core/philosophers/prompts/_GUIDE.md")
    pyproject = _read("pyproject.toml")
    init_py = _read("src/po_core/__init__.py")

    assert "唯一の真実源は `src/po_core/philosophers/llm_personas.py`" in guide
    assert '"philosophers/prompts/*.yaml"' not in pyproject
    assert "PO_CORE_SYSTEM_PROMPT" not in init_py
    assert "PoTestRunner" not in init_py



def test_prompt_yaml_placeholders_are_not_shipped_in_public_artifacts() -> None:
    prompt_dir = ROOT / "src" / "po_core" / "philosophers" / "prompts"
    placeholder_files = [p.name for p in prompt_dir.glob("*.yaml") if "FILL_IN" in p.read_text(encoding="utf-8")]
    assert placeholder_files, "test assumption broken: expected unfinished prompt YAML fixtures"
    pyproject = _read("pyproject.toml")
    assert '"philosophers/prompts/*.yaml"' not in pyproject


def test_env_example_fails_closed_for_auth() -> None:
    env_example = _read(".env.example")
    assert "PO_SKIP_AUTH=false" in env_example


def test_ci_release_blockers_are_fail_closed() -> None:
    ci = _read(".github/workflows/ci.yml")
    publish = _read(".github/workflows/publish.yml")

    assert "pip-audit" in ci
    assert "|| true" not in ci
    assert "pytest tests/ -v --cov=po_core" in ci
    assert "artifact-type: ['wheel', 'sdist']" in ci
    assert "python-version: ['3.10', '3.11', '3.12']" in ci
    for entrypoint in ENTRYPOINTS:
        assert f"{entrypoint} --help" in ci

    assert "Publish is allowed only from main or version tags" in publish
    assert "pytest tests/ -v" in publish
    assert "bandit -r src/ -c pyproject.toml" in publish
    assert "pip-audit" in publish
    assert "python -m build" in publish
    assert "twine check dist/*" in publish
    for entrypoint in ENTRYPOINTS:
        assert f"{entrypoint} --help" in publish


def test_release_smoke_script_checks_all_console_scripts() -> None:
    smoke = _read("scripts/release_smoke.py")
    for entrypoint in ENTRYPOINTS:
        assert entrypoint in smoke
    assert "--check-entrypoints" in smoke


def test_publish_playbook_documents_fail_closed_release_path() -> None:
    playbook = _read("docs/operations/publish_playbook.md")
    assert "pytest tests/ -v" in playbook
    assert "bandit -r src/ -c pyproject.toml" in playbook
    assert "pip-audit" in playbook
    assert "main または `vX.Y.Z` タグ以外から publish しない" in playbook
