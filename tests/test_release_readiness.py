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


def test_quickstart_en_install_examples_are_valid_for_current_release() -> None:
    quickstart_en = (ROOT / "QUICKSTART_EN.md").read_text(encoding="utf-8")
    assert 'pip install "po-core-flyingpig==1.0.2"' in quickstart_en
    assert 'pip install -e ".[api]"' not in quickstart_en


def test_quickstart_en_allowlist_semantics_are_documented() -> None:
    quickstart_en = (ROOT / "QUICKSTART_EN.md").read_text(encoding="utf-8")
    assert "constructor = default allowlist" in quickstart_en
    assert "overrides constructor default" in quickstart_en
    assert '"philosophers": ["kant"]' in quickstart_en


def test_tutorial_does_not_reference_old_alpha_version() -> None:
    """docs/TUTORIAL.md must not show the stale v0.1.0-alpha version string."""
    tutorial = (ROOT / "docs" / "TUTORIAL.md").read_text(encoding="utf-8")
    assert "v0.1.0-alpha" not in tutorial, (
        "docs/TUTORIAL.md still references v0.1.0-alpha — update to current version"
    )


def test_examples_readme_does_not_claim_20_philosophers() -> None:
    """examples/README.md must not claim only 20 philosophers (now 42 integrated)."""
    readme = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    assert "20人の哲学者" not in readme, (
        "examples/README.md still claims '20人の哲学者' — update to reflect 42 integrated"
    )
    assert "20 philosophers" not in readme, (
        "examples/README.md still claims '20 philosophers' — update to reflect 42 integrated"
    )


def test_typescript_sdk_readme_uses_canonical_env_var() -> None:
    """clients/typescript/README.md must use PO_API_KEY (not the old PO_CORE_API_KEY)."""
    ts_readme = (ROOT / "clients" / "typescript" / "README.md").read_text(encoding="utf-8")
    assert "PO_CORE_API_KEY" not in ts_readme, (
        "clients/typescript/README.md still references PO_CORE_API_KEY — "
        "use PO_API_KEY to match the canonical env var name"
    )
    assert "PO_API_KEY" in ts_readme, (
        "clients/typescript/README.md should mention PO_API_KEY"
    )


def test_typescript_generated_types_are_not_all_unknown() -> None:
    """clients/typescript/src/generated/openapi.ts must not have unknown request/response."""
    openapi_ts = (
        ROOT / "clients" / "typescript" / "src" / "generated" / "openapi.ts"
    ).read_text(encoding="utf-8")
    # The file should define typed fields, not just 'unknown'
    assert "input:" in openapi_ts, (
        "generated openapi.ts is missing typed 'input' field — regenerate or fix manually"
    )
    assert "response:" in openapi_ts, (
        "generated openapi.ts is missing typed 'response' field — regenerate or fix manually"
    )


def test_examples_web_api_server_has_legacy_warning() -> None:
    """examples/web_api_server.py must have a LEGACY warning so users aren't confused."""
    server_py = (ROOT / "examples" / "web_api_server.py").read_text(encoding="utf-8")
    assert "LEGACY" in server_py, (
        "examples/web_api_server.py has no LEGACY marker — "
        "add a warning that this is not the official API"
    )
