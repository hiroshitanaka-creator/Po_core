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
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Union

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


def _load_yaml_payload(path: Path, *, label: str) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data = to_json_compatible(data)
    if not isinstance(data, dict):
        raise TypeError(f"{label} YAML must be an object at top-level: {path}")
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


def _decode_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def _parse_json_pointer(path: str) -> List[str]:
    if not path.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {path}")
    if path == "/":
        return [""]
    return [_decode_pointer_token(part) for part in path.lstrip("/").split("/")]


def _resolve_parent(container: Any, tokens: List[str], *, path: str) -> tuple[Any, str]:
    if not tokens:
        raise ValueError(f"Root replacement is not supported in patch path: {path}")

    current = container
    for tok in tokens[:-1]:
        if isinstance(current, list):
            if not tok.isdigit():
                raise ValueError(f"List index must be integer in patch path: {path}")
            idx = int(tok)
            if idx < 0 or idx >= len(current):
                raise ValueError(f"List index out of range in patch path: {path}")
            current = current[idx]
        elif isinstance(current, dict):
            if tok not in current:
                raise ValueError(f"Missing object key in patch path: {path}")
            current = current[tok]
        else:
            raise ValueError(f"Cannot traverse patch path: {path}")
    return current, tokens[-1]


def _apply_patch(
    case: Dict[str, Any], patch_ops: List[Dict[str, Any]]
) -> Dict[str, Any]:
    updated = deepcopy(case)
    for op in patch_ops:
        op_name = str(op.get("op"))
        path = str(op.get("path", ""))
        tokens = _parse_json_pointer(path)
        parent, leaf = _resolve_parent(updated, tokens, path=path)
        value = deepcopy(op.get("value"))

        if isinstance(parent, list):
            if leaf == "-" and op_name == "add":
                parent.append(value)
                continue
            if not leaf.isdigit():
                raise ValueError(f"List index must be integer in patch path: {path}")
            index = int(leaf)
            if op_name == "add":
                if index < 0 or index > len(parent):
                    raise ValueError(
                        f"List add index out of range in patch path: {path}"
                    )
                parent.insert(index, value)
            elif op_name == "replace":
                if index < 0 or index >= len(parent):
                    raise ValueError(
                        f"List replace index out of range in patch path: {path}"
                    )
                parent[index] = value
            elif op_name == "remove":
                if index < 0 or index >= len(parent):
                    raise ValueError(
                        f"List remove index out of range in patch path: {path}"
                    )
                del parent[index]
            elif op_name == "test":
                if index < 0 or index >= len(parent):
                    raise ValueError(
                        f"List test index out of range in patch path: {path}"
                    )
                if parent[index] != value:
                    raise ValueError(f"JSON patch test failed at {path}")
            else:
                raise ValueError(f"Unsupported patch operation: {op_name}")
            continue

        if not isinstance(parent, dict):
            raise ValueError(f"Patch target parent must be object or array: {path}")

        if op_name == "add":
            parent[leaf] = value
        elif op_name == "replace":
            if leaf not in parent:
                raise ValueError(f"Replace target does not exist in patch path: {path}")
            parent[leaf] = value
        elif op_name == "remove":
            if leaf not in parent:
                raise ValueError(f"Remove target does not exist in patch path: {path}")
            del parent[leaf]
        elif op_name == "test":
            if parent.get(leaf) != value:
                raise ValueError(f"JSON patch test failed at {path}")
        else:
            raise ValueError(f"Unsupported patch operation: {op_name}")
    return updated


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


def run_session_replay(
    case_path: Union[str, Path],
    answers_path: Union[str, Path],
    *,
    seed: int = 0,
    now: Union[str, Any] = "2026-02-22T00:00:00Z",
    deterministic: bool = True,
) -> Dict[str, Any]:
    """Apply Decision Session answers patch to a case and run deterministic pipeline."""
    case_file = Path(case_path)
    answers_file = Path(answers_path)
    if not case_file.exists():
        raise FileNotFoundError(f"Case file not found: {case_file}")
    if not answers_file.exists():
        raise FileNotFoundError(f"Session answers file not found: {answers_file}")

    case = _load_yaml_case(case_file)
    _validate_or_raise(
        _get_validator("input_schema_v1.json"),
        case,
        label=f"Input case {case_file.name}",
    )

    answers = _load_yaml_payload(answers_file, label="Session answers")
    _validate_or_raise(
        _get_validator("session_answers_schema_v1.json"),
        answers,
        label=f"Session answers {answers_file.name}",
    )

    case_ref = str(answers.get("case_ref", ""))
    if case_ref and case_ref != str(case.get("case_id", "")):
        raise ValueError(
            f"Session answers case_ref mismatch: {case_ref} != {case.get('case_id')}"
        )

    patch_ops = answers.get("patch", [])
    if not isinstance(patch_ops, list):
        raise ValueError("Session answers patch must be an array")

    replay_case = _apply_patch(case, patch_ops)
    _validate_or_raise(
        _get_validator("input_schema_v1.json"),
        replay_case,
        label=f"Patched case for {case_file.name}",
    )

    out = run_case(
        replay_case,
        case_path=case_file,
        seed=seed,
        now=now,
        deterministic=deterministic,
    )
    _validate_or_raise(
        _get_validator("output_schema_v1.json"),
        out,
        label=f"Output for replay {case_file.name}",
    )
    return out
