# Acceptance Proof for v0.3.0 Contract Updates

- Purpose: Verify acceptance contract consistency for the `0.3.0` version bump and acceptance expected metadata updates.
- Execution time (UTC): 2026-03-06T11:52:13Z
- Commit SHA (HEAD at execution): `180de9b`

## Required must-pass command

- Command: `pytest tests/acceptance/ -v -m acceptance`
- Result summary: `43 passed, 9 deselected, 0 failed`

## Additional recommended checks

- Command: `pytest tests/test_output_schema.py -v`
- Result summary: `41 passed, 0 failed`

- Command: `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v`
- Result summary: `62 passed, 0 failed`
