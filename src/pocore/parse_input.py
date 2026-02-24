"""
src/pocore/parse_input.py
=========================

Normalization layer: case dict → ParsedInput (with features).

Design:
  Engines depend on *features*, not file names or case_ids.
  This prevents `if short_id == ...` proliferation in engine logic
  (existing golden cases retain their frozen branches as a temporary contract).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from .utils import (
    case_short_id,
    detect_constraint_conflict,
    parse_deadline_iso,
    parse_iso_datetime,
)


@dataclass(frozen=True)
class ParsedInput:
    """Normalized case input plus derived features (for rule engines)."""

    case: Dict[str, Any]
    short_id: str
    features: Dict[str, Any]


def _extract_unknowns_items(unknowns: Any) -> list[str]:
    if not isinstance(unknowns, list):
        return []
    items: list[str] = []
    for item in unknowns:
        normalized = str(item).strip()
        if normalized:
            items.append(normalized)
        if len(items) >= 10:
            break
    return items


def _extract_stakeholder_roles(stakeholders: Any) -> list[str]:
    if not isinstance(stakeholders, list):
        return []
    roles: list[str] = []
    seen: set[str] = set()
    for item in stakeholders:
        if not isinstance(item, dict) or "role" not in item:
            continue
        role = str(item.get("role")).strip()
        if not role or role in seen:
            continue
        seen.add(role)
        roles.append(role)
        if len(roles) >= 10:
            break
    return roles


def _extract_deadline_features(deadline: Any, now: Optional[str]) -> Dict[str, Any]:
    result: Dict[str, Any] = {"deadline_iso": None, "days_to_deadline": None}
    deadline_present = deadline is not None and str(deadline).strip() != ""
    if not deadline_present:
        return result

    deadline_iso, deadline_date = parse_deadline_iso(deadline)
    now_dt = parse_iso_datetime(now)
    if deadline_iso is None or deadline_date is None or now_dt is None:
        return result

    result["deadline_iso"] = deadline_iso
    result["days_to_deadline"] = (deadline_date - now_dt.date()).days
    return result


def extract_features(
    case: Dict[str, Any], *, now: Optional[str] = None
) -> Dict[str, Any]:
    """Derive feature flags from case dict for engine dispatch."""
    values = case.get("values", [])
    constraints = case.get("constraints", [])
    unknowns = case.get("unknowns", [])
    stakeholders = case.get("stakeholders", [])
    deadline = case.get("deadline")
    extensions = case.get("extensions")
    scenario_profile = None
    if isinstance(extensions, dict):
        raw_profile = extensions.get("scenario_profile")
        if isinstance(raw_profile, str):
            normalized = raw_profile.strip()
            if normalized:
                scenario_profile = normalized

    features: Dict[str, Any] = {
        "values_empty": isinstance(values, list) and len(values) == 0,
        "constraints_count": len(constraints) if isinstance(constraints, list) else 0,
        "unknowns_count": len(unknowns) if isinstance(unknowns, list) else 0,
        "stakeholders_count": (
            len(stakeholders) if isinstance(stakeholders, list) else 0
        ),
        "deadline_present": (deadline is not None and str(deadline).strip() != ""),
        "unknowns_items": _extract_unknowns_items(unknowns),
        "stakeholder_roles": _extract_stakeholder_roles(stakeholders),
        "scenario_profile": scenario_profile,
    }

    features.update(_extract_deadline_features(deadline, now))

    features.update(detect_constraint_conflict(case))
    return features


def parse(
    case: Dict[str, Any], *, case_path: Optional[Path] = None, now: Optional[str] = None
) -> ParsedInput:
    """Parse a case dict into a ParsedInput with features."""
    cid = str(case.get("case_id", "case_unknown"))
    short = case_short_id(cid, case_path=case_path)
    feats = extract_features(case, now=now)
    return ParsedInput(case=case, short_id=short, features=feats)
