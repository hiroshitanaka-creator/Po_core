from __future__ import annotations

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
REPO_STRUCTURE_STALE_PHRASES = [
    "[39 philosopher .py files]",
    "39 philosopher unit tests",
    "M1 In Progress",
    "actual production state (Phase 5 complete)",
    "v0.2.0b4",
    "39 philosopher modules",
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
    assert "42 integrated" in readme
    assert "Po_coreでは **42人**の哲学者" in quickstart_ja
    assert "最大39人" in quickstart_ja
    assert "Po_core integrates **42 philosophers**" in quickstart_en
    assert "39 active" in quickstart_en
    assert "39 philosophers" not in quickstart_en
    assert "42 integrated philosophers" in repo_structure
    assert "39 active philosophers" in repo_structure


def test_repository_structure_is_fully_resynced() -> None:
    repo_structure = _read("REPOSITORY_STRUCTURE.md")
    required_phrases = [
        "actual repository layout and release-critical files only",
        "experiments/claude_testing/",
        "Prompt runtime SSOT:",
        "repo-local editable-install convenience wrappers",
    ]
    for phrase in required_phrases:
        assert phrase in repo_structure
    for phrase in REPO_STRUCTURE_STALE_PHRASES:
        assert phrase not in repo_structure, f"stale phrase remains in REPOSITORY_STRUCTURE.md: {phrase}"


def test_requirements_files_are_documented_as_repo_local_convenience_wrappers() -> None:
    requirements = _read("requirements.txt")
    requirements_dev = _read("requirements-dev.txt")
    readme = _read("README.md")

    assert "Repo-local only" in requirements
    assert requirements.strip().endswith("-e .")
    assert "Repo-local only" in requirements_dev
    assert requirements_dev.strip().endswith("-e .[dev]")
    assert "repo-local convenience wrappers" in readme


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


def test_experimental_prompt_assets_are_isolated_from_runtime_package() -> None:
    runtime_removed = [
        ROOT / "src" / "po_core" / "po_system_prompt.py",
        ROOT / "src" / "po_core" / "po_claude_client.py",
        ROOT / "src" / "po_core" / "po_test_runner.py",
    ]
    experimental_present = [
        ROOT / "experiments" / "claude_testing" / "po_system_prompt.py",
        ROOT / "experiments" / "claude_testing" / "po_claude_client.py",
        ROOT / "experiments" / "claude_testing" / "po_test_runner.py",
        ROOT / "experiments" / "claude_testing" / "README.md",
    ]

    assert all(not path.exists() for path in runtime_removed)
    assert all(path.exists() for path in experimental_present)
    assert "not included in the published wheel/sdist" in _read("experiments/claude_testing/README.md")


def test_prompt_yaml_placeholders_are_not_shipped_in_public_artifacts() -> None:
    prompt_dir = ROOT / "src" / "po_core" / "philosophers" / "prompts"
    placeholder_files = [
        p.name for p in prompt_dir.glob("*.yaml") if "FILL_IN" in p.read_text(encoding="utf-8")
    ]
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


def test_tutorial_does_not_reference_old_alpha_version() -> None:
    tutorial = _read("docs/TUTORIAL.md")
    assert "v0.1.0-alpha" not in tutorial


def test_typescript_sdk_readme_uses_canonical_env_var() -> None:
    ts_readme = _read("clients/typescript/README.md")
    assert "PO_CORE_API_KEY" not in ts_readme
    assert "PO_API_KEY" in ts_readme


def test_typescript_generated_types_are_not_all_unknown() -> None:
    openapi_ts = _read("clients/typescript/src/generated/openapi.ts")
    assert "input:" in openapi_ts
    assert "response:" in openapi_ts


def test_examples_web_api_server_has_legacy_warning() -> None:
    server_py = _read("examples/web_api_server.py")
    assert "LEGACY" in server_py
