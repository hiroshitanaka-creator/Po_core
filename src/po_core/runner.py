"""
src/po_core/runner.py
=====================

Po_core scenario runner — drives the real philosophical pipeline.

Public API
----------
    run_case_file(path, seed, now, deterministic) -> dict

Pipeline (executed in order):
    1. Load YAML
    2. Validate against input_schema_v1.json
    3. Compute input_digest  = sha256(canonical_json(case))
    4. Run po_core.run() → philosophical proposal from 39 philosophers
    5. Adapt proposal → output_schema_v1 via output_adapter
    6. Validate against output_schema_v1.json
    7. Return dict

Determinism contract (ADR-0002):
    Same path + same seed + same now + deterministic=True → identical JSON.
    (proposal content is deterministic given the same user_input)

Dependencies: PyYAML, jsonschema (runtime requirements)
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Optional, Union

try:
    import yaml  # type: ignore[import-untyped]
except ImportError as _e:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for po_core.runner. pip install pyyaml"
    ) from _e

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as _e:  # pragma: no cover
    raise ImportError(
        "jsonschema is required for po_core.runner. pip install jsonschema"
    ) from _e

# ── Packaged resources ──────────────────────────────────────────────────────

_INPUT_SCHEMA_RESOURCE = "input_schema_v1.json"
_OUTPUT_SCHEMA_RESOURCE = "output_schema_v1.json"
_DEFAULT_NOW = "2026-02-22T00:00:00Z"

# ── Helpers ───────────────────────────────────────────────────────────────


def _to_json_compat(obj: object) -> object:
    """Recursively convert PyYAML types (date/datetime) to JSON-safe types."""
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    if isinstance(obj, dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): _to_json_compat(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_json_compat(v) for v in obj]
    return obj


def _canonical_json(data: dict) -> str:
    """Canonical JSON: sorted keys, no whitespace, UTF-8 characters preserved."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(data: dict) -> str:
    """SHA-256 hex digest of canonical JSON."""
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def _load_schema(resource_name: str) -> dict[str, object]:
    from po_core.schemas import resource_path

    schema_resource = resource_path(resource_name)
    with schema_resource.open("r", encoding="utf-8") as schema_file:
        loaded = json.load(schema_file)
    return dict(loaded)


def _validate(data: dict, schema_resource: str, label: str) -> None:
    schema = _load_schema(schema_resource)
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(v.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        msgs = [f"  [{i}] {e.message}" for i, e in enumerate(errors, 1)]
        raise ValueError(f"{label} schema validation failed:\n" + "\n".join(msgs))


# ── Public API ────────────────────────────────────────────────────────────


# ── Public API ────────────────────────────────────────────────────────────


def run_case_file(
    path: Union[str, Path],
    seed: int = 0,
    now: Optional[str] = None,
    deterministic: bool = True,
) -> dict:
    """
    Run a scenario YAML file through the Po_core pipeline.

    Args:
        path:          Path to case YAML file (``scenarios/*.yaml``).
        seed:          Determinism seed (reserved; not yet used internally).
        now:           ISO-8601 UTC datetime for trace timestamps.
                       Defaults to ``"2026-02-22T00:00:00Z"``.
        deterministic: When True, ``run_id`` is derived from ``case_id``
                       (same input → same run_id).

    Returns:
        Output dict conforming to ``output_schema_v1.json``.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError:        If input or output schema validation fails.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Case file not found: {path}")

    if now is None:
        now = _DEFAULT_NOW

    # 1. Load YAML
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    case: dict = _to_json_compat(raw)  # type: ignore[assignment]

    # 2. Validate input
    _validate(case, _INPUT_SCHEMA_RESOURCE, "Input")

    # 3. Compute input_digest
    digest = _digest(case)

    # 4. Run philosophical pipeline
    import uuid as _uuid

    from po_core.app.api import run as _po_run
    from po_core.app.output_adapter import adapt_to_schema, build_user_input

    run_id = f"{case['case_id']}_v1" if deterministic else _uuid.uuid4().hex
    user_input = build_user_input(case)
    run_result = _po_run(user_input)

    # 5. Adapt to output_schema_v1
    output = adapt_to_schema(
        case,
        run_result,
        run_id=run_id,
        digest=digest,
        now=now,
        seed=seed,
        deterministic=deterministic,
    )

    # 6. Validate output
    _validate(output, _OUTPUT_SCHEMA_RESOURCE, "Output")

    # 7. Return
    return output
