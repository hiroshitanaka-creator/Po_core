# ADR-0003 — Trace Contract

**Status:** Accepted
**Date:** 2026-02-22
**Deciders:** hiroshitanaka-creator

---

## Context

Po_core's output schema (`output_schema_v1.json`) includes a `trace` field that
records the pipeline steps with `started_at` / `ended_at` timestamps and optional
`metrics`.  Without a determinism contract, every run would produce different
timestamps, breaking golden diff tests.

## Decision

**All trace timestamps are derived from the injected `now` parameter using fixed
integer-second offsets.** No wall-clock calls (`datetime.utcnow()`, `time.time()`,
etc.) are allowed inside the pipeline.

### Step-to-offset mapping (current)

| Step name             | `started_at` offset (s) | `ended_at` offset (s) |
|-----------------------|-------------------------|-----------------------|
| `parse_input`         | +0                      | +1                    |
| `generate_options`    | +1                      | +2                    |
| `ethics_review`       | +2                      | +3                    |
| `responsibility_review` | +2                    | +3                    |
| `question_layer`      | +2                      | +3                    |
| `compose_output`      | last step start + 1     | last step start + 2   |

The exact offsets are chosen so that the 3-step and 4-step traces in the current
frozen golden files remain stable.

### `trace.version`

Always `"1.0"` in M0/M1.  A version bump requires a new ADR.

### Step names

Only names listed in `output_schema_v1.json → $defs.trace_step.name.enum` are
valid:
- `parse_input`
- `generate_options`
- `ethics_review`
- `responsibility_review`
- `question_layer`
- `compose_output`

Adding a new step requires updating both the schema and this ADR.

## Consequences

- **Good:** Golden diff tests (`test_golden_e2e.py`) are stable across runs.
- **Good:** Any accidental wall-clock usage becomes immediately visible as a test
  failure.
- **Trade-off:** Real elapsed time is not recorded in M0/M1; performance is
  measured separately (benchmarks).
- **Future:** M2+ may record real elapsed time in a `metrics.elapsed_ms` field
  while keeping `started_at` / `ended_at` deterministic.
