# ADR-0004 — Input Features Layer

**Status:** Accepted
**Date:** 2026-02-22
**Deciders:** hiroshitanaka-creator

---

## Context

In M0, engine logic branched on `case_id` or `short_id` (e.g., `if short_id ==
"case_001"`).  This worked for two frozen golden cases but would proliferate
uncontrollably as new scenario types were added.

The root cause: engines were dispatching on *identity* (which file is this?)
rather than *semantics* (what properties does this input have?).

## Decision

**Introduce a `features` normalization layer** (`src/pocore/parse_input.py`)
between raw YAML input and engine logic.

`extract_features(case: dict) -> dict` produces a flat dict of boolean/numeric
flags derived from the input, for example:

```python
{
    "values_empty": True,            # case.values == []
    "constraints_count": 3,          # len(case.constraints)
    "unknowns_count": 2,             # len(case.unknowns)
    "stakeholders_count": 1,         # len(case.stakeholders)
    "deadline_present": False,       # case.deadline is not None
    "constraint_conflict": True,     # min_hours > max_hours detected
    "conflict_min_h": 20,            # extracted min weekly hours
    "conflict_max_h": 5,             # extracted max weekly hours
}
```

Engines receive `features` and branch on flag values, not on case names:

```python
# Good (features-driven)
if features.get("constraint_conflict"):
    return _generate_conflict_options(features)

# Bad (identity-driven — do not add new branches like this)
if short_id == "case_010":
    return _generate_conflict_options(features)
```

### Frozen golden branches (temporary exception)

The two existing golden cases (`case_001`, `case_009`) retain `short_id` branches
in the engine layer **as a temporary backwards-compatibility contract**.  These
branches are marked with `# FROZEN: golden contract` and must not be modified.
They will be migrated to features-driven logic in M2 once the golden files are
regenerated with richer feature flags.

### Constraint conflict detection

`detect_constraint_conflict(case)` scans `case.constraints` for patterns:
- **Minimum constraint:** `週N時間以上` → `min_h = N`
- **Maximum constraint:** `週N時間が上限` → `max_h = N`

If both are present and `min_h > max_h`, `constraint_conflict = True`.

## Consequences

- **Good:** New scenario types (e.g., ethical dilemma, irreversible decision) add
  a new feature flag + engine branch — no new `short_id` checks.
- **Good:** Feature flags are unit-testable independently of the full pipeline.
- **Good:** `ParsedInput` is a frozen dataclass — immutable after parse, safe to
  pass across engine boundaries.
- **Trade-off:** Feature extraction adds a normalization pass; negligible for M0/M1
  throughput.
- **Future:** M2 will extend `extract_features` with ML-derived signals (embedding
  similarity, tone classification) to drive more nuanced engine dispatch.
