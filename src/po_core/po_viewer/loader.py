"""Utilities for loading Po_core trace files."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def resolve_traces_dir(traces_dir: Optional[Path] = None) -> Path:
    """Return the directory containing stored traces.

    Resolution order:
    1. Explicit ``traces_dir`` argument
    2. ``PO_CORE_TRACES_DIR`` environment variable
    3. ``data/traces`` relative to the current working directory
    """

    if traces_dir is not None:
        return traces_dir

    env_dir = os.environ.get("PO_CORE_TRACES_DIR")
    if env_dir:
        return Path(env_dir)

    return Path.cwd() / "data" / "traces"


def load_trace(trace_id: str, traces_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Load a stored trace from disk.

    Args:
        trace_id: Identifier of the trace (file name without extension).
        traces_dir: Optional directory override.

    Returns:
        Parsed trace dictionary.

    Raises:
        FileNotFoundError: If the trace JSON file cannot be located.
        ValueError: If the JSON cannot be parsed.
    """

    base_dir = resolve_traces_dir(traces_dir)
    trace_path = base_dir / f"{trace_id}.json"

    if not trace_path.exists():
        raise FileNotFoundError(f"Trace '{trace_id}' not found at {trace_path}")

    try:
        return json.loads(trace_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid trace JSON for '{trace_id}': {exc}") from exc
