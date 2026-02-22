"""
src/pocore/runner.py
====================

Po_core public runner API.

Public API
----------
    run_case_file(path, *, seed, now, deterministic) -> dict

Pipeline (without golden replay):
    1. Load YAML
    2. Validate against input_schema_v1.json
    3. orchestrator.run_case() — deterministic pipeline
    4. Validate against output_schema_v1.json
    5. Return dict

Design stance:
    Golden files (*_expected.json) are executable specifications used by tests.
    This runner never reads golden files — it produces output deterministically.
    If test output differs from golden, the test catches it (not the runner).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from .orchestrator import run_case
from .utils import to_json_compatible


def _repo_root() -> Path:
    # src/pocore/runner.py → src/pocore → src → repo root
    return Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise TypeError(f"JSON must be an object at top-level: {path}")
    return data


def _load_yaml_case(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data = to_json_compatible(data)
    if not isinstance(data, dict):
        raise TypeError(f"Case YAML must be an object at top-level: {path}")
    return data


def _get_validator(schema_name: str) -> Draft202012Validator:
    schema_path = _repo_root() / "docs" / "spec" / schema_name
    schema = _load_json(schema_path)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _validate_or_raise(
    validator: Draft202012Validator, instance: Dict[str, Any], label: str
) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        return
    lines = [f"{label} failed schema validation ({len(errors)} error(s))."]
    for i, err in enumerate(errors[:10], start=1):
        path = "$" + "".join(
            f"[{p}]" if isinstance(p, int) else f".{p}" for p in err.path
        )
        lines.append(f"[{i}] {path}: {err.message}")
    raise ValueError("\n".join(lines))


def run_case_file(
    path: Union[str, Path],
    *,
    seed: int = 0,
    now: Union[str, Any] = "2026-02-22T00:00:00Z",
    deterministic: bool = True,
) -> Dict[str, Any]:
    """
    Run a scenario YAML file through the Po_core deterministic pipeline.

    Args:
        path:          Path to a case YAML file.
        seed:          Determinism seed (reserved for future use).
        now:           ISO-8601 UTC datetime for trace timestamps.
        deterministic: When True, run_id is derived from case_id.

    Returns:
        Output dict conforming to output_schema_v1.json.

    Raises:
        FileNotFoundError: If path does not exist.
        ValueError:        If schema validation fails.
    """
    case_path = Path(path)
    if not case_path.exists():
        raise FileNotFoundError(f"Case file not found: {case_path}")

    case = _load_yaml_case(case_path)
    _validate_or_raise(
        _get_validator("input_schema_v1.json"),
        case,
        label=f"Input case {case_path.name}",
    )

    out = run_case(
        case, case_path=case_path, seed=seed, now=now, deterministic=deterministic
    )

    _validate_or_raise(
        _get_validator("output_schema_v1.json"),
        out,
        label=f"Output for {case_path.name}",
    )

    return out
