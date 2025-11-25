# Testing guide

This repository uses `pytest` with a small set of deterministic fixtures to validate the CLI, core tensor ensemble, and Po_trace logging. Coverage is configured via `pytest-cov` and a default fail-under threshold of 80%.

## Test layout
- `tests/unit/`: fast feedback on CLI wiring, Po_trace output, and deterministic ensemble behavior.
- `tests/integration/`: scenario-style runs of the three-philosopher pipeline, including audit trace assertions.
- `tests/conftest.py`: shared fixtures such as `sample_prompt` and a reusable `CliRunner`.

## Running tests
Install the development dependencies first:

```bash
pip install -r requirements-dev.txt
```

Run the entire suite (unit + integration) with coverage:

```bash
pytest
```

To focus on a subset:

```bash
pytest -m unit       # only unit tests
pytest -m integration # only integration tests
```

Coverage reports are written to `htmlcov/` and `coverage.xml`; the run will fail if coverage drops below 80%.
