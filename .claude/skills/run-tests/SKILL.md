---
name: run-tests
description: Run the correct Po_core test subset for the situation (pipeline must-pass, acceptance, red team, REST, full CI-equivalent). Use when the user asks to run tests, check the suite, verify nothing broke, or reproduce CI locally.
---

# Run Po_core Tests

CI requires **pipeline-marked tests to pass**; the full suite is best-effort.
Pick the narrowest subset that proves the change, then widen if needed.

## Decision guide

- **Touched the pipeline / philosophers / tensors / aggregator** → pipeline must-pass:
  ```bash
  pytest tests/test_run_turn_e2e.py tests/test_philosopher_bridge.py tests/test_smoke_pipeline.py -v
  ```

- **Touched output schema, engines, golden scenarios** → acceptance:
  ```bash
  pytest tests/acceptance/ -v          # all scenarios (~48+)
  pytest tests/acceptance/ -v -m acceptance
  ```
  If golden files now differ, do NOT hand-edit them — use the `regen-golden` skill.

- **Touched safety / intention gate / injection detection** → red team:
  ```bash
  pytest -m "redteam or phase4" -v
  ```

- **Touched REST layer** (`src/po_core/app/rest/`):
  ```bash
  pytest tests/unit/test_rest_api.py -v
  ```

- **Single philosopher**:
  ```bash
  pytest tests/unit/test_philosophers/test_<name>.py -v
  ```

- **Before commit / reproduce CI** (excludes slow/benchmark):
  ```bash
  pytest tests/ -v -m "not slow"
  ```

## Markers available

`unit`, `integration`, `pipeline`, `slow`, `philosophical`, `redteam`,
`phase4`, `phase5`, `acceptance`, `observability`.

## Reporting

- Report pass/fail counts honestly, with the failing output if any.
- Benchmarks (`tests/benchmarks/`) are informational only — a benchmark
  failure on a slow machine is not a blocker; say so explicitly.
- Never claim green without the actual run output.
