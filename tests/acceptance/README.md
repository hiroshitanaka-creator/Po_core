# Acceptance tests (M1–M4 / v1.0.0)

`tests/acceptance/` hosts AT-001〜AT-012 acceptance tests. M1–M4 milestones are all complete (✅ 2026-03-10).

## Execution model

- The suite runs against `StubComposer` (`po_core.app.composer.StubComposer`).
- Scenarios are loaded from `scenarios/case_*.yaml` via shared fixtures in `conftest.py`.
- Every acceptance test enforces `AT-OUT-001` by validating output against `docs/spec/output_schema_v1.json` through the shared `validate_output_schema` fixture.

## Run

```bash
pytest tests/acceptance/ -v -m acceptance
```

**Current status:** 52 passed / 0 failed / 0 skipped (v1.0.0).
