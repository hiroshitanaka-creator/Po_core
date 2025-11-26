# Po_core testing guide

This directory contains automated tests for the Po_core CLI and future modules. Use it to validate changes locally before opening a pull request and to mirror the checks run in CI.

## Environment setup

- Python: 3.9–3.12 (project is tested with 3.11 in CI).
- Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
- Install dependencies:
  - Recommended: `python -m pip install --upgrade pip`
  - Development extras: `python -m pip install -e .[dev]`
  - Alternatively, `python -m pip install -r requirements-dev.txt`

## Running tests

- All tests: `python -m pytest`
- Unit tests only: `python -m pytest -m unit`
- Include integration tests: `python -m pytest -m "unit or integration"`
- Run full suite including philosophical scenarios: `python -m pytest -m "unit or integration or philosophical"`

## Marker policy

- `unit`: Fast, deterministic checks suitable for every push and PR. CI runs these markers by default.
- `integration`: Broader surface tests that may touch external resources or larger flows. Run locally when you modify boundaries or integrations.
- `philosophical`: Narrative or exploratory scenarios that may be slower or have richer output. Opt-in locally.

## Notes

- Keep tests idempotent and free of network calls by default.
- Align new tests with existing markers so contributors can target the right scope.
