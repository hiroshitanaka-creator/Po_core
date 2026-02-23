# ADR 0007: Trace Metrics Observability for parse_input

- Status: Accepted
- Date: 2026-02-23

## Context
Task C requires observability for input-side uncertainty and stakeholder pressure without
mixing policy decisions into trace generation.

Po_core already fixes trace determinism via ADR-0003:
- timestamps are derived from injected `now` (`meta.created_at`) with fixed offsets
- no wall-clock randomness is allowed
- frozen golden cases (`case_001`, `case_009`) must remain unchanged

## Decision

### Metrics to add (generic trace only)
In `src/pocore/tracer.py`, for non-frozen cases (`case_001` / `case_009` 以外),
`parse_input` step `metrics` includes:
- `unknowns_count` (int)
- `stakeholders_count` (int)
- `days_to_deadline` (int, optional)

### Source of truth
All values are observational and must come from `features` (from `parse_input`):
- tracer does not compute recommendation or ethics logic
- orchestrator remains wiring only

### Null/omission policy
`days_to_deadline` is **omitted** when feature value is unavailable (`None`).
We do not emit `null` for this key in trace metrics.

### Frozen golden exception
`case_001` and `case_009` trace payloads remain frozen and unchanged.
The new metrics apply only to generic trace branches.

## Consequences
- parse_input observability increases for debugging/monitoring.
- Determinism is preserved because metrics are pure values from deterministic features,
  and trace time behavior remains `now + fixed offset`.
- Existing frozen contracts remain intact while allowing generic golden evolution.
