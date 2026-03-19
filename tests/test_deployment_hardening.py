from __future__ import annotations

from pathlib import Path
from typing import Final
import re

import yaml

ROOT: Final = Path(__file__).resolve().parents[1]
WORKFLOW_FILES: Final[tuple[str, ...]] = (
    ".github/workflows/ci.yml",
    ".github/workflows/publish.yml",
    ".github/workflows/typescript-sdk.yml",
    ".github/workflows/pr-governance.yml",
    ".github/workflows/import-guard.yml",
    ".github/workflows/policy_lab.yml",
)
SHA_PIN_PATTERN: Final = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")


def _load_yaml(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _iter_uses_entries(node: object) -> list[str]:
    matches: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uses" and isinstance(value, str):
                matches.append(value)
            matches.extend(_iter_uses_entries(value))
    elif isinstance(node, list):
        for item in node:
            matches.extend(_iter_uses_entries(item))
    return matches


def test_external_workflow_uses_entries_are_sha_pinned() -> None:
    violations: list[str] = []
    pinned_entries = 0

    for relative_path in WORKFLOW_FILES:
        workflow = _load_yaml(ROOT / relative_path)
        uses_entries = _iter_uses_entries(workflow)
        for entry in uses_entries:
            if entry.startswith("./"):
                continue
            if not SHA_PIN_PATTERN.fullmatch(entry):
                violations.append(f"{relative_path}: {entry}")
            else:
                pinned_entries += 1

    assert not violations, "Unpinned external GitHub Actions:\n" + "\n".join(violations)
    assert pinned_entries == 35


def test_compose_healthcheck_uses_configurable_port() -> None:
    compose_path = ROOT / "docker-compose.yml"
    compose_text = compose_path.read_text(encoding="utf-8")

    assert "http://localhost:${PO_PORT:-8000}/v1/health" in compose_text

    compose_config = _load_yaml(compose_path)
    assert isinstance(compose_config, dict)

    services = compose_config.get("services")
    assert isinstance(services, dict)

    api_service = services.get("api")
    assert isinstance(api_service, dict)

    healthcheck = api_service.get("healthcheck")
    assert isinstance(healthcheck, dict)

    test_command = healthcheck.get("test")
    assert isinstance(test_command, list)
    assert test_command[:3] == ["CMD", "python", "-c"]

    python_snippet = test_command[3]
    assert isinstance(python_snippet, str)
    assert "urllib.request.urlopen('http://localhost:${PO_PORT:-8000}/v1/health')" in python_snippet
