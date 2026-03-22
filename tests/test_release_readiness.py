from __future__ import annotations

import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = ["po-core", "po-self", "po-trace", "po-interactive", "po-experiment"]
DOCS_WITH_VERSION = [
    "README.md",
    "QUICKSTART.md",
    "QUICKSTART_EN.md",
    "CHANGELOG.md",
    "REPOSITORY_STRUCTURE.md",
    "docs/operations/publish_playbook.md",
    "docs/status.md",
    "clients/typescript/README.md",
    "examples/README.md",
]
TARGET_PUBLIC_VERSION = "1.0.2"
REPO_STRUCTURE_STALE_PHRASES = [
    "[39 philosopher .py files]",
    "39 philosopher unit tests",
    "M1 In Progress",
    "actual production state (Phase 5 complete)",
    "v0.2.0b4",
    "39 philosopher modules",
]
README_STALE_PHRASES = [
    "Current Phase: v1.0.0 Released",
    "Install from PyPI (beta)",
    "PyPI v1.0.0 publish pending",
    "pending external publish; this repository does not currently contain ",
    "TestPyPI/PyPI publication evidence",
]
QUICKSTART_STALE_PHRASES = [
    "公開済みstable",
    "pip install click rich",
    "39 philosophers",
    "39 phil",
    "Full 39-philosopher manifest",
    "API key (empty = no auth)",
    "APIキー（空の場合は認証スキップ）",
    "APIキー不要",
]


STATUS_STALE_PHRASES = [
    "PyPI公開とスモーク検証の証跡を固定。`docs/release/pypi_publish_log_v0.3.0.md` を追加し",
    "PyPI `0.3.0` 公開証跡・acceptance proof・publish playbook は整備済み。",
    "v1.0.0 リリース完了",
    "pending external publish",
]


def _read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def _canonical_dev_dependencies() -> list[str]:
    lines = _read("tools/dev-requirements.txt").splitlines()
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _package_version() -> str:
    package_init = _read("src/po_core/__init__.py")
    match = re.search(r'__version__ = "([^"]+)"', package_init)
    assert match is not None
    return match.group(1)


def _release_evidence_relpath(
    prefix: str, version: str, *, must_exist: bool = True
) -> str:
    relpath = f"docs/release/{prefix}{version}.md"
    if must_exist:
        assert (ROOT / relpath).exists(), f"missing release evidence file: {relpath}"
    return relpath


def test_release_version_ssot_is_package_version() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    assert pyproject["project"]["dynamic"] == ["version"]
    assert (
        pyproject["tool"]["setuptools"]["dynamic"]["version"]["attr"]
        == "po_core.__version__"
    )

    version = _package_version()
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[A-Za-z0-9.-]+)?", version)


def test_release_docs_are_synced_to_current_version() -> None:
    version = _package_version()
    for relpath in DOCS_WITH_VERSION:
        text = _read(relpath)
        assert version in text, f"{relpath} must mention {version}"
        if relpath != "CHANGELOG.md":
            assert "0.2.0b4" not in text, f"{relpath} still contains stale beta version"


def test_release_state_split_is_explicit_and_honest() -> None:
    version = _package_version()
    published_version = TARGET_PUBLIC_VERSION
    status_doc = _read("docs/status.md")

    assert version == "1.0.3"
    assert published_version == "1.0.2"
    assert f"Repository target version: `{version}`" in status_doc
    assert f"Latest published public version: `{published_version}`" in status_doc
    assert (
        f"latest published public version can remain `{published_version}` until `{version}` is actually published"
        in status_doc
    )
    assert f"do not claim `{version}` is already published" in status_doc


def test_openapi_version_matches_package_version() -> None:
    server_py = _read("src/po_core/app/rest/server.py")
    assert "version=__version__" in server_py


def test_release_docs_use_consistent_philosopher_counts() -> None:
    readme = _read("README.md")
    quickstart_ja = _read("QUICKSTART.md")
    quickstart_en = _read("QUICKSTART_EN.md")
    repo_structure = _read("REPOSITORY_STRUCTURE.md")

    assert "42 philosophers" in readme
    assert "compliance sentinel" in readme
    assert "42人の哲学者" in quickstart_ja
    assert "最大39" in quickstart_ja
    assert "42 philosophers" in quickstart_en
    assert "39 active" in quickstart_en
    for phrase in ["39 philosophers", "39 phil", "Full 39-philosopher manifest"]:
        assert phrase not in quickstart_en
    assert "42 philosophers" in repo_structure
    assert "dummy" in repo_structure
    assert "must not be counted as one of the 42" in repo_structure


def test_release_docs_fail_closed_on_stale_wording() -> None:
    version = _package_version()
    readme = _read("README.md")
    quickstart_ja = _read("QUICKSTART.md")
    quickstart_en = _read("QUICKSTART_EN.md")
    status_doc = _read("docs/status.md")
    repo_structure = _read("REPOSITORY_STRUCTURE.md")
    published_version = TARGET_PUBLIC_VERSION
    pypi_evidence_relpath = _release_evidence_relpath(
        "pypi_publication_v", published_version
    )
    pypi_evidence = _read(pypi_evidence_relpath)
    candidate_handoff_relpath = _release_evidence_relpath(
        "release_candidate_handoff_v", version
    )
    candidate_handoff = _read(candidate_handoff_relpath)
    candidate_smoke_relpath = _release_evidence_relpath("smoke_verification_v", version)
    candidate_smoke = _read(candidate_smoke_relpath)

    for phrase in README_STALE_PHRASES:
        assert phrase not in readme, f"stale README phrase remains: {phrase}"

    for phrase in QUICKSTART_STALE_PHRASES:
        assert (
            phrase not in quickstart_ja
        ), f"stale QUICKSTART.md phrase remains: {phrase}"
        assert (
            phrase not in quickstart_en
        ), f"stale QUICKSTART_EN.md phrase remains: {phrase}"

    for phrase in STATUS_STALE_PHRASES:
        assert (
            phrase not in status_doc
        ), f"stale docs/status.md phrase remains: {phrase}"

    assert "PO_SKIP_AUTH=true" in quickstart_ja
    assert "PO_SKIP_AUTH=true" in quickstart_en
    assert "非空の `PO_API_KEY`" in quickstart_ja
    assert "non-empty `PO_API_KEY`" in quickstart_en
    assert "PO_CORS_ORIGINS=*" in quickstart_ja
    assert "PO_CORS_ORIGINS=*" in quickstart_en
    assert "PO_ALLOW_UNSAFE_THREAD_EXECUTION=true" in quickstart_ja
    assert "PO_ALLOW_UNSAFE_THREAD_EXECUTION=true" in quickstart_en
    assert "43 integrated runtime personas" not in readme
    assert "43 integrated runtime personas" not in quickstart_en
    assert "43の統合済みランタイム・ペルソナ" not in quickstart_ja
    assert "43 integrated runtime personas" not in repo_structure
    assert "43 integrated runtime personas" not in status_doc
    assert f"Repository target version: `{version}`" in status_doc
    assert f"Latest published public version: `{published_version}`" in status_doc
    assert pypi_evidence_relpath in status_doc
    assert candidate_handoff_relpath in status_doc
    assert f"published on PyPI for `{published_version}`" in status_doc
    assert f"published on PyPI for `{version}`" not in status_doc
    assert "Canonical evidence boundary" in status_doc
    assert (
        f"https://pypi.org/project/po-core-flyingpig/{published_version}/"
        in pypi_evidence
    )
    assert "Publication result evidenced here: **PyPI published**" in pypi_evidence
    assert f"Version: `{published_version}`" in pypi_evidence
    assert "TestPyPI publication state" in pypi_evidence
    assert "workflow run URL" in pypi_evidence or "workflow run URL(s)" in pypi_evidence
    assert f"Version: `{version}`" in candidate_smoke
    assert "operator-supplied transcript not yet recorded" in candidate_smoke
    assert "pre-publish candidate state" in candidate_smoke
    assert "Not yet fixed as truth in this file" in candidate_smoke
    assert f"Repository target version is `{version}`" in candidate_handoff
    assert (
        f"Latest public PyPI evidence still points to `{published_version}`"
        in candidate_handoff
    )
    assert "## Next" in status_doc
    assert "## Completed" in status_doc
    next_section = status_doc.split("## Next", 1)[1].split("## Completed", 1)[0]
    assert "- Record the real TestPyPI publication state" in next_section
    assert "- Record the real PyPI publication evidence" in next_section
    assert "- Record the actual GitHub Actions workflow run URL(s)" in next_section
    assert "- Record the clean install / import / smoke transcript" in next_section


def test_repository_structure_is_fully_resynced() -> None:
    repo_structure = _read("REPOSITORY_STRUCTURE.md")
    required_phrases = [
        "actual repository layout and release-critical files only",
        "experiments/claude_testing/",
        "Prompt runtime SSOT:",
        "Non-runtime prompt drafts:",
        "repo-local editable-install convenience wrappers",
    ]
    for phrase in required_phrases:
        assert phrase in repo_structure
    for phrase in REPO_STRUCTURE_STALE_PHRASES:
        assert (
            phrase not in repo_structure
        ), f"stale phrase remains in REPOSITORY_STRUCTURE.md: {phrase}"


def test_requirements_files_are_documented_as_repo_local_convenience_wrappers() -> None:
    requirements = _read("requirements.txt")
    requirements_dev = _read("requirements-dev.txt")
    readme = _read("README.md")

    assert "Repo-local only" in requirements
    assert requirements.strip().endswith("-e .")
    assert "Repo-local only" in requirements_dev
    assert "tools/dev-requirements.txt" in requirements_dev
    assert requirements_dev.strip().endswith("-e .[dev]")
    assert "repo-local convenience wrappers" in readme


def test_dev_dependencies_are_single_sourced() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    canonical_dev = _canonical_dev_dependencies()
    optional_dev = pyproject["project"]["optional-dependencies"]["dev"]
    dependency_group_dev = pyproject["dependency-groups"]["dev"]

    assert canonical_dev
    assert optional_dev == canonical_dev
    assert dependency_group_dev == canonical_dev
    script = _read("scripts/check_dev_dependencies.py")
    assert "tools/dev-requirements.txt" in script
    assert "dependency-groups.dev" in script
    assert "project.optional-dependencies.dev" in script


def test_optional_all_extra_is_not_self_referential() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    optional = pyproject["project"]["optional-dependencies"]
    all_extra = optional["all"]
    combined = optional["llm"] + optional["dev"] + optional["docs"] + optional["viz"]
    combined_deduped = list(dict.fromkeys(combined))
    assert all("po-core-flyingpig" not in dep for dep in all_extra)
    assert all_extra == combined_deduped


def test_prompt_runtime_ssot_is_python_persona_registry() -> None:
    guide = _read("docs/philosopher_prompt_drafts/_GUIDE.md")
    pyproject = _read("pyproject.toml")
    init_py = _read("src/po_core/__init__.py")

    assert "唯一の真実源は `src/po_core/philosophers/llm_personas.py`" in guide
    assert "非runtimeドラフト資産" in guide
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
    assert "not included in the published wheel/sdist" in _read(
        "experiments/claude_testing/README.md"
    )


def test_prompt_yaml_placeholders_live_only_in_docs_drafts() -> None:
    runtime_prompt_dir = ROOT / "src" / "po_core" / "philosophers" / "prompts"
    draft_prompt_dir = ROOT / "docs" / "philosopher_prompt_drafts"

    assert not runtime_prompt_dir.exists()

    placeholder_files = [
        p.name
        for p in draft_prompt_dir.glob("*.yaml")
        if "FILL_IN" in p.read_text(encoding="utf-8")
    ]
    assert (
        placeholder_files
    ), "test assumption broken: expected unfinished prompt YAML draft fixtures"
    pyproject = _read("pyproject.toml")
    assert '"philosophers/prompts/*.yaml"' not in pyproject
    assert '"docs/philosopher_prompt_drafts/*.yaml"' not in pyproject


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
    assert "python scripts/release_smoke.py --check-entrypoints" in ci
    assert "bandit -r src/ scripts/ -c pyproject.toml" in ci
    for surface in ['base ""', 'llm "llm"', 'docs "docs"', 'viz "viz"']:
        assert f"audit_surface {surface}" in ci
    assert "po-core --help" not in ci

    assert "Publish is allowed only from refs/heads/main or refs/tags/vX.Y.Z" in publish
    assert "Tagged commit $SHA is not reachable from origin/main" in publish
    assert (
        "Tag version $REF_NAME does not match package version $PACKAGE_VERSION"
        in publish
    )
    assert "deployments: read" in publish
    assert (
        "PyPI publish requires a prior successful TestPyPI deployment for this exact commit SHA"
        in publish
    )
    assert "Run workflow_dispatch with target=testpypi first" in publish
    assert "successful TestPyPI deployment status for this exact commit SHA" in publish
    assert 'environment": "testpypi"' in publish
    assert "git merge-base --is-ancestor" in publish
    assert "python tools/import_graph.py --check --print" in publish
    assert "pytest tests/ -v" in publish
    assert "bandit -r src/ scripts/ -c pyproject.toml" in publish
    assert "pip-audit" in publish
    for surface in ['base ""', 'llm "llm"', 'docs "docs"', 'viz "viz"']:
        assert f"audit_surface {surface}" in publish
    assert "python -m build" in publish
    assert "twine check dist/*" in publish
    assert "python scripts/release_smoke.py --check-entrypoints" in publish
    assert "po-core --help" not in publish


def test_release_smoke_script_checks_all_console_scripts() -> None:
    smoke = _read("scripts/release_smoke.py")
    for entrypoint in ENTRYPOINTS:
        assert entrypoint in smoke
    assert "--check-entrypoints" in smoke
    assert "ENTRYPOINT_TIMEOUT_SECONDS = 15" in smoke
    assert "create_app" not in smoke
    assert "urllib.request" in smoke
    assert "uvicorn" in smoke
    assert "TestClient" not in smoke
    assert 'version_cmd = ["po-core", "version"]' in smoke
    assert 'status_cmd = ["po-core", "status"]' in smoke
    assert 'prompt_cmd = ["po-core", "prompt", "smoke", "--format", "json"]' in smoke
    assert 'experiment_cmd = ["po-experiment", "list"]' in smoke
    assert "/v1/health" in smoke
    assert "/v1/reason" in smoke
    assert "/v1/reason/stream" in smoke


def test_publish_playbook_documents_fail_closed_release_path() -> None:
    playbook = _read("docs/operations/publish_playbook.md")
    assert "python scripts/check_dev_dependencies.py" in playbook
    assert "tools/dev-requirements.txt" in playbook
    assert "pytest tests/ -v" in playbook
    assert "bandit -r src/ scripts/ -c pyproject.toml" in playbook
    assert "pip-audit" in playbook
    assert "base / `llm` / `docs` / `viz`" in playbook
    assert (
        "`refs/heads/main` または `refs/tags/vX.Y.Z` 以外から publish しない"
        in playbook
    )
    assert "`origin/main` 到達可能" in playbook
    assert "`__version__` と一致" in playbook
    assert "same commit SHA" in playbook
    assert "successful TestPyPI deployment" in playbook
    assert "workflow_dispatch target=testpypi → release=<tag>" in playbook
    assert "python tools/import_graph.py --check --print" in playbook
    assert "po-core version" in playbook
    assert "timeout" in playbook
    assert "PO_PHILOSOPHER_EXECUTION_MODE" in playbook


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


def test_release_metadata_status_is_consistent() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    readme = _read("README.md")
    changelog = _read("CHANGELOG.md")
    status_doc = _read("docs/status.md")
    repo_structure = _read("REPOSITORY_STRUCTURE.md")

    assert "Development Status :: 4 - Beta" in pyproject["project"]["classifiers"]
    assert pyproject["tool"]["po_core"]["project"]["status"] == "beta"
    for text in (readme, changelog, status_doc):
        assert "Development Status :: 5 - Production/Stable" not in text
        assert "✅ Stable" not in text
        assert (
            "Development Status :: 4 - Beta" in text
            or "status = `beta`" in text
            or 'status = "beta"' in text
        )


def test_release_count_metadata_is_consistent() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    readme = _read("README.md")
    quickstart_ja = _read("QUICKSTART.md")
    quickstart_en = _read("QUICKSTART_EN.md")

    assert pyproject["tool"]["po_core"]["project"]["philosophers_integrated"] == 42
    assert "42 philosophers" in readme
    assert "dummy" in readme
    assert "42人の哲学者" in quickstart_ja
    assert "42 philosophers" in quickstart_en


def test_rest_default_docs_are_fully_synchronized() -> None:
    readme = _read("README.md")
    quickstart_ja = _read("QUICKSTART.md")
    quickstart_en = _read("QUICKSTART_EN.md")
    env_example = _read(".env.example")

    localhost_default = (
        "http://localhost,http://127.0.0.1,http://localhost:3000,http://127.0.0.1:3000"
    )
    for text in (readme, quickstart_ja, quickstart_en, env_example):
        assert localhost_default in text
        assert (
            "PO_PHILOSOPHER_EXECUTION_MODE=process" in text
            or "| `PO_PHILOSOPHER_EXECUTION_MODE` | `process` |" in text
        )
        assert "PO_ALLOW_UNSAFE_THREAD_EXECUTION" in text
