"""
src/pocore/utils.py
===================

Shared utilities for the pocore decision engine.

Determinism contract:
- No wall-clock time.  All time is derived from injected `now`.
- Hashes are SHA-256 over canonical JSON.
- run_id is deterministic given (short_id, flavor).
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

# ── Type converters ───────────────────────────────────────────────────────


def to_json_compatible(obj: Any) -> Any:
    """Normalize YAML-loaded values into JSON-compatible values."""
    if isinstance(obj, _dt.datetime):
        return obj.isoformat()
    if isinstance(obj, _dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): to_json_compatible(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_json_compatible(v) for v in obj]
    if isinstance(obj, tuple):
        return [to_json_compatible(v) for v in obj]
    if isinstance(obj, set):
        raise TypeError("YAML contains a 'set' which is not JSON-compatible.")
    return obj


# ── Digest ────────────────────────────────────────────────────────────────


def canonical_json(obj: Any) -> str:
    """Canonical JSON: sorted keys, no whitespace, UTF-8 characters preserved."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_hex_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def input_digest(case_obj: Dict[str, Any]) -> str:
    """SHA-256 of canonical JSON of the case dict."""
    return sha256_hex_text(canonical_json(case_obj))


# ── Time ──────────────────────────────────────────────────────────────────


def normalize_now(now: Union[str, _dt.datetime]) -> str:
    """Normalize `now` to ISO8601 UTC string (trailing Z)."""
    if isinstance(now, _dt.datetime):
        if now.tzinfo is None:
            now = now.replace(tzinfo=_dt.timezone.utc)
        s = now.isoformat()
        return s.replace("+00:00", "Z")
    if not isinstance(now, str) or not now:
        return "2026-02-22T00:00:00Z"
    return now


def add_seconds(iso_dt: str, seconds: int) -> str:
    """Add seconds to ISO datetime string."""
    s = iso_dt
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = _dt.datetime.fromisoformat(s)
    dt2 = dt + _dt.timedelta(seconds=seconds)
    return dt2.isoformat().replace("+00:00", "Z")


# ── ID helpers ────────────────────────────────────────────────────────────

_CASE_SHORT_RE = re.compile(r"^(case_\d{3})\b")


def case_short_id(case_id: str, case_path: Optional[Path] = None) -> str:
    """Derive a stable short id (e.g., 'case_001') from case_id or file stem."""
    if case_path is not None and case_path.stem:
        m = _CASE_SHORT_RE.match(case_path.stem)
        if m:
            return m.group(1)
    m2 = _CASE_SHORT_RE.match(case_id)
    if m2:
        return m2.group(1)
    return case_id


def deterministic_run_id(
    short_id: str, flavor: str = "expected_stub_compact_v1"
) -> str:
    """Deterministic run_id matching golden contract."""
    return f"{short_id}_{flavor}"


# ── Feature extraction helpers ────────────────────────────────────────────

_WEEK_HOURS_RE = re.compile(r"週\s*(\d+)\s*時間")
_MIN_HINTS = ("以上", "最低", "下限", "少なくとも")
_MAX_HINTS = ("上限", "以下", "まで", "以内")


def _extract_week_hours_bounds(
    constraints: list,
) -> Tuple[Optional[int], Optional[int]]:
    mins: list = []
    maxs: list = []
    for c in constraints:
        if not isinstance(c, str):
            continue
        m = _WEEK_HOURS_RE.search(c)
        if not m:
            continue
        hours = int(m.group(1))
        if any(h in c for h in _MIN_HINTS):
            mins.append(hours)
        if any(h in c for h in _MAX_HINTS):
            maxs.append(hours)
    min_req = max(mins) if mins else None
    max_allow = min(maxs) if maxs else None
    return min_req, max_allow


def detect_constraint_conflict(case: Dict[str, Any]) -> Dict[str, Any]:
    """Detect structural conflicts in constraints."""
    constraints = case.get("constraints", [])
    if not isinstance(constraints, list):
        return {"constraint_conflict": False}

    min_req, max_allow = _extract_week_hours_bounds([str(x) for x in constraints])
    time_conflict = (
        min_req is not None and max_allow is not None and min_req > max_allow
    )

    income_drop_forbidden = any(
        isinstance(c, str)
        and ("収入" in c)
        and any(k in c for k in ("一切", "不可", "下回", "落とせない"))
        for c in constraints
    )

    relocation_forbidden = any(
        isinstance(c, str)
        and ("引っ越し" in c or "転居" in c)
        and ("不可" in c or "できない" in c)
        for c in constraints
    )

    return {
        "constraint_conflict": bool(time_conflict),
        "time_min_hours_per_week": min_req,
        "time_max_hours_per_week": max_allow,
        "income_drop_forbidden": bool(income_drop_forbidden),
        "relocation_forbidden": bool(relocation_forbidden),
    }
