# Phase 0 Baseline (2026-04-24)

## Scope checked before execution
- `pyproject.toml`
- `pytest.ini`
- `tests/`
- `scripts/release_smoke.py`
- `.github/workflows/ci.yml`

## Pre-change issue summary
- Editable install in a clean virtual environment fails in this environment due to proxy/network access to package index (cannot fetch `setuptools>=69.0.0`).
- Even without editable install, local pytest commands can run via the repository Python environment.
- `scripts/release_smoke.py --check-entrypoints` fails without package install because `po_core` is not importable from the clean venv.

## Environment
- OS: container Linux
- Python: `3.10.19`
- Virtualenv: `.venv_phase0`

## Commands and results

1. `python -m pip install --upgrade pip`
   - exit code: `0`
   - note: upgrade check executed; proxy retries occurred.

2. `python -m pip install -e ".[dev]"`
   - exit code: `1`
   - first failure: build dependency resolution for setuptools
   - stderr summary: `ProxyError ... Tunnel connection failed: 403 Forbidden`, then `No matching distribution found for setuptools>=69.0.0`

3. `pytest tests/test_release_readiness.py -v`
   - exit code: `0`
   - result: `24 passed`

4. `pytest tests/test_output_schema.py tests/test_golden_e2e.py tests/test_input_schema.py -v`
   - exit code: `0`
   - result: `103 passed`

5. `pytest tests/acceptance/ -v -m acceptance`
   - exit code: `0`
   - result: `43 passed, 9 deselected`

6. `python scripts/release_smoke.py --check-entrypoints`
   - exit code: `1`
   - first failure: import at startup
   - stderr summary: `ModuleNotFoundError: No module named 'po_core'`

## Baseline conclusion
- Release-critical pytest gates pass in this environment.
- Release smoke entrypoint check is blocked by package installation failure in clean venv.
- No production code/config/schema/golden files were changed for this phase.
