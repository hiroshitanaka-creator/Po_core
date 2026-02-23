# Features v1 Catalog

This document defines deterministic, input-derived features used by rule engines.
Features are **observations only** (no recommendation or ethics judgment).

## unknowns

- `unknowns_count: int`
  - `len(case["unknowns"])` when `case["unknowns"]` is a list, otherwise `0`.
- `unknowns_items: list[str]`
  - Extract only when `case["unknowns"]` is a list.
  - For each element: convert to `str`, then `strip()`.
  - Drop empty strings.
  - Preserve original input order.
  - Maximum 10 items (if more than 10, keep first 10).
  - If missing/empty/non-list: `[]`.

## stakeholders

- `stakeholders_count: int`
  - `len(case["stakeholders"])` when list, otherwise `0`.
- `stakeholder_roles: list[str]`
  - Extract only when `case["stakeholders"]` is a list.
  - Use only elements that are `dict` and have `role`.
  - `role` is converted to `str`, then `strip()`.
  - Drop empty strings.
  - Remove duplicates while preserving first-seen order.
  - Maximum 10 items (if more than 10 unique roles, keep first 10).
  - If missing/empty/non-list: `[]`.

## deadline

- `deadline_present: bool`
  - `True` when `case["deadline"]` exists and is non-empty after `str(...).strip()`.
- `deadline_iso: str | null`
  - Parsed/normalized deadline string when parseable, else `null`.
  - Supported input formats:
    - `YYYY-MM-DD`
    - ISO 8601 datetime (including trailing `Z`)
- `days_to_deadline: int | null`
  - Compute only when `deadline_present` is `True`.
  - `now` is provided externally from `meta.created_at` as ISO 8601 datetime string (trailing `Z` allowed).
  - Date-diff rule (UTC basis):
    - `now_date = date(now)`
    - `deadline_date = date(deadline)`
    - `days_to_deadline = (deadline_date - now_date).days`
  - If `deadline` parsing fails (or `now` is unparsable):
    - `deadline_iso = null`
    - `days_to_deadline = null`
