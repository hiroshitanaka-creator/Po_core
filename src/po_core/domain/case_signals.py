"""CaseSignals — structured semantic signals from a case dict.

These signals capture scenario-level semantics that cannot be reliably
inferred from plain-text ``user_input`` alone, and are forwarded from
the public ``run()`` API into ``run_turn`` so the pipeline can
differentiate case types and return appropriate signals.

Design constraints
------------------
- Pure domain object: no imports from app/, ensemble, or output_adapter.
- Frozen dataclass: safe to cache and share across threads.
- ``from_case_dict`` is the only factory; callers that don't have a
  structured case (e.g. direct API callers) pass ``case_signals=None``,
  which keeps all pipeline defaults unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass

_CONFLICT_KEYWORDS: frozenset[str] = frozenset(
    {
        "矛盾",
        "同時に成立しない",
        "条件が矛盾",
        "conflicting constraints",
        "contradicting",
        "mutually exclusive",
    }
)


@dataclass(frozen=True)
class CaseSignals:
    """Semantic signals derived from a structured case dict.

    Attributes:
        values_present: False when the case carries an explicit empty
            values list (``values: []``).  Used to switch the pipeline's
            primary ``action_type`` to ``'clarify'``.
        has_constraint_conflict: True when the case title or problem
            statement explicitly signals contradictory constraints.
            The pipeline adds a ``constraint_conflict`` key to its
            result dict when this is set.
        scenario_type: Coarse scenario classification string.
    """

    values_present: bool = True
    has_constraint_conflict: bool = False
    scenario_type: str = "general"


def from_case_dict(case: dict) -> CaseSignals:
    """Derive CaseSignals from a scenario case dict.

    Checks:
    - ``values_present``: ``case["values"]`` is non-empty
    - ``has_constraint_conflict``: title or problem contains conflict keywords,
      or ``extensions.scenario_profile == "conflicting_constraints"``
    - ``scenario_type``: derived from the two flags above
    """
    raw_values = case.get("values")
    values_present = bool(raw_values)

    title = str(case.get("title", ""))
    problem = str(case.get("problem", ""))
    extensions = case.get("extensions") or {}
    profile = str(extensions.get("scenario_profile", ""))

    conflict_text = " ".join([title, problem, profile])
    has_conflict = profile == "conflicting_constraints" or any(
        kw in conflict_text for kw in _CONFLICT_KEYWORDS
    )

    if not values_present:
        scenario_type = "values_clarification"
    elif has_conflict:
        scenario_type = "conflicting_constraints"
    else:
        scenario_type = "general"

    return CaseSignals(
        values_present=values_present,
        has_constraint_conflict=has_conflict,
        scenario_type=scenario_type,
    )


__all__ = ["CaseSignals", "from_case_dict"]
