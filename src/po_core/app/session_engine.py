# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Flying Pig Project
"""Session engine v1 — JSON Patch application for session replay.

REQ-SESSION-001: session answers（JSON Patch）を適用した再実行結果が、
    session golden expected JSON と一致すること。

Usage::

    from po_core.app.session_engine import apply_session_answers

    patched_case = apply_session_answers(base_case, session_answers)
    output = StubComposer(seed=42).compose(patched_case)
"""

from __future__ import annotations

import copy
import json
from typing import Any, TypeVar, cast

T = TypeVar("T")


class SessionPatchError(ValueError):
    """Raised when a JSON Patch operation fails."""


def _apply_patch(obj: T, operations: list[dict[str, Any]]) -> T:
    """Apply RFC6902-compatible JSON Patch operations to a Python object.

    Supports: add, remove, replace.
    ``move``, ``copy``, ``test`` are validated but silently skipped to keep
    the engine dependency-free (no ``jsonpatch`` library required).

    Args:
        obj:        Deep-copied target object (modified in-place).
        operations: List of patch operation dicts.

    Returns:
        The patched object.

    Raises:
        SessionPatchError: When an operation is invalid or the path is wrong.
    """
    for op_dict in operations:
        op: str = str(op_dict.get("op", "")).lower()
        path: str = str(op_dict.get("path", ""))
        value: Any = op_dict.get("value")

        if not path.startswith("/"):
            raise SessionPatchError(f"Invalid path (must start with /): {path!r}")

        parts = path[1:].split("/") if path != "/" else []
        parts = [p.replace("~1", "/").replace("~0", "~") for p in parts]

        if op in {"move", "copy", "test"}:
            continue  # not needed for session replay

        if op == "add":
            _patch_add(obj, parts, value)
        elif op == "remove":
            _patch_remove(obj, parts)
        elif op == "replace":
            _patch_replace(obj, parts, value)
        else:
            raise SessionPatchError(f"Unsupported op: {op!r}")

    return obj


def _navigate(obj: Any, parts: list[str]) -> tuple[Any, str | int]:
    """Navigate to the parent of the target, returning (parent, last_key)."""
    current = obj
    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                raise SessionPatchError(
                    f"Path not found: {part!r} in {list(current.keys())}"
                )
            current = current[part]
        elif isinstance(current, list):
            try:
                idx = int(part)
            except ValueError:
                raise SessionPatchError(f"Expected array index, got: {part!r}")
            current = current[idx]
        else:
            raise SessionPatchError(f"Cannot navigate into {type(current).__name__}")

    last = parts[-1]
    return current, last


def _patch_add(obj: Any, parts: list[str], value: Any) -> None:
    if not parts:
        raise SessionPatchError("Cannot add to root")
    parent, key = _navigate(obj, parts)
    if isinstance(parent, dict):
        parent[key] = value
    elif isinstance(parent, list):
        if key == "-":
            parent.append(value)
        else:
            try:
                parent.insert(int(key), value)
            except ValueError:
                raise SessionPatchError(f"Invalid array index: {key!r}")
    else:
        raise SessionPatchError(f"Cannot add to {type(parent).__name__}")


def _patch_remove(obj: Any, parts: list[str]) -> None:
    if not parts:
        raise SessionPatchError("Cannot remove root")
    parent, key = _navigate(obj, parts)
    if isinstance(parent, dict):
        if key not in parent:
            raise SessionPatchError(f"Key not found for remove: {key!r}")
        del parent[key]
    elif isinstance(parent, list):
        try:
            parent.pop(int(key))
        except (ValueError, IndexError) as exc:
            raise SessionPatchError(f"Array remove failed: {exc}") from exc
    else:
        raise SessionPatchError(f"Cannot remove from {type(parent).__name__}")


def _patch_replace(obj: Any, parts: list[str], value: Any) -> None:
    if not parts:
        raise SessionPatchError("Cannot replace root")
    parent, key = _navigate(obj, parts)
    if isinstance(parent, dict):
        if key not in parent:
            raise SessionPatchError(f"Key not found for replace: {key!r}")
        parent[key] = value
    elif isinstance(parent, list):
        try:
            parent[int(key)] = value
        except (ValueError, IndexError) as exc:
            raise SessionPatchError(f"Array replace failed: {exc}") from exc
    else:
        raise SessionPatchError(f"Cannot replace in {type(parent).__name__}")


def apply_session_answers(
    base_case: dict[str, Any],
    session_answers: dict[str, Any],
) -> dict[str, Any]:
    """Apply session answers (JSON Patch) to a base case dict.

    REQ-SESSION-001: The patched case is then passed to StubComposer for
    deterministic re-evaluation.

    Args:
        base_case:       Original case dict (not mutated).
        session_answers: Dict conforming to session_answers_schema_v1.json.

    Returns:
        New case dict with patches applied.

    Raises:
        SessionPatchError: When patch application fails.
        ValueError:        When session_answers structure is invalid.
    """
    version = session_answers.get("version")
    if version != "1.0":
        raise ValueError(f"Unsupported session_answers version: {version!r}")

    patch_ops: list[dict[str, Any]] = list(session_answers.get("patch", []))
    patched = copy.deepcopy(base_case)
    return _apply_patch(patched, patch_ops)


def load_session_answers(path: str) -> dict[str, Any]:
    """Load session answers from a JSON file.

    Args:
        path: File system path to the session answers JSON file.

    Returns:
        Parsed session answers dict.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Session answers JSON must be an object")

    return cast(dict[str, Any], data)
