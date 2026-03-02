# Acceptance tests (M1-A)

`tests/acceptance/` hosts AT-001〜AT-010 acceptance tests for the M1 milestone.

## Execution model

- The suite runs against `StubComposer` (`po_core.app.composer.StubComposer`).
- Scenarios are loaded from `scenarios/case_*.yaml` via shared fixtures in `conftest.py`.
- Every acceptance test enforces `AT-OUT-001` by validating output against `docs/spec/output_schema_v1.json` through the shared `validate_output_schema` fixture.

## Run

```bash
pytest tests/acceptance/ -v -m acceptance
```

This command is the required gate for Phase M1-A.
