# Features v1 Catalog

This document defines input-derived features used by rule engines.
Features are observations, not recommendations.

## unknowns
- unknowns_count: int
  - len(case.unknowns) if list else 0
- unknowns_items: list[str] (optional)
  - normalized string list from case.unknowns

## stakeholders
- stakeholders_count: int
  - len(case.stakeholders) if list else 0
- stakeholder_roles: list[str] (optional)
  - normalized list from case.stakeholders[*].role

## deadline
- deadline_present: bool
  - deadline exists and non-empty
- deadline_iso: str|null (optional)
  - normalized ISO string if parseable
- days_to_deadline: int|null (recommended)
  - computed from meta.created_at(now) and deadline_iso
  - arithmetic only (no judgment thresholds here)
