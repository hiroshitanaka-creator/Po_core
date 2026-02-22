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

from .utils import case_short_id, detect_constraint_conflict


@dataclass(frozen=True)
class ParsedInput:
    """Normalized case input plus derived features (for rule engines)."""

    case: Dict[str, Any]
    short_id: str
    features: Dict[str, Any]


def extract_features(case: Dict[str, Any]) -> Dict[str, Any]:
    """Derive feature flags from case dict for engine dispatch."""
    values = case.get("values", [])
    constraints = case.get("constraints", [])
    unknowns = case.get("unknowns", [])
    stakeholders = case.get("stakeholders", [])
    deadline = case.get("deadline")

    features: Dict[str, Any] = {
        "values_empty": isinstance(values, list) and len(values) == 0,
        "constraints_count": len(constraints) if isinstance(constraints, list) else 0,
        "unknowns_count": len(unknowns) if isinstance(unknowns, list) else 0,
        "stakeholders_count": (
            len(stakeholders) if isinstance(stakeholders, list) else 0
        ),
        "deadline_present": (deadline is not None and str(deadline).strip() != ""),
    }

    features.update(detect_constraint_conflict(case))
    return features


def parse(case: Dict[str, Any], *, case_path: Optional[Path] = None) -> ParsedInput:
    """Parse a case dict into a ParsedInput with features."""
    cid = str(case.get("case_id", "case_unknown"))
    short = case_short_id(cid, case_path=case_path)
    feats = extract_features(case)
    return ParsedInput(case=case, short_id=short, features=feats)
