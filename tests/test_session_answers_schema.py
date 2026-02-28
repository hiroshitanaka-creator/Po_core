"""session_answers_v1 schema contract tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "docs" / "spec" / "session_answers_schema_v1.json"
VALID_YAML_PATH = ROOT_DIR / "tests" / "fixtures" / "session_answers_valid.yaml"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path} must contain a mapping at top-level"
    return data


def test_session_answers_schema_file_exists() -> None:
    assert SCHEMA_PATH.exists(), f"Schema not found: {SCHEMA_PATH}"


def test_session_answers_yaml_conforms_to_schema() -> None:
    schema = _load_json(SCHEMA_PATH)
    payload = _load_yaml(VALID_YAML_PATH)
    validator = Draft202012Validator(schema)

    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        details = "\n".join(
            f"- {err.message} at path={list(err.path)} schema_path={list(err.schema_path)}"
            for err in errors
        )
        pytest.fail(f"Schema validation failed:\n{details}")


def test_session_answers_rejects_missing_required_field() -> None:
    schema = _load_json(SCHEMA_PATH)
    payload = _load_yaml(VALID_YAML_PATH)
    del payload["patch"]

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    assert errors, "Expected validation errors when patch is missing"
