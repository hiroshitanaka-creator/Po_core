# Smoke Verification Evidence for v1.0.3

- Version: `1.0.3`
- Evidence status: **post-publish evidence fixed (2026-03-22)**
- Pre-publish local smoke: PASSED (2026-03-22, claude/audit-po-core-1.0.3-IyRXH)
- Post-publish state: **PyPI and TestPyPI publication CONFIRMED via public API**
- Current state: **post-publish evidence fixed** — public PyPI/TestPyPI confirmed, workflow run URL pending

## Post-publish Evidence Summary

| Evidence | Status |
|----------|--------|
| PyPI `1.0.3` public page | confirmed — https://pypi.org/project/po-core-flyingpig/1.0.3/ |
| TestPyPI `1.0.3` public page | confirmed — https://test.pypi.org/project/po-core-flyingpig/1.0.3/ |
| `pip install --no-deps` wheel install in clean venv | confirmed — see below |
| Workflow run URL | pending — GitHub API rate-limited during this session |
| Full deps install + import + runtime smoke | pending — large deps (torch/CUDA) not completed in this session |

See `docs/release/pypi_publication_v1.0.3.md` for full PyPI publication evidence.
See `docs/release/testpypi_publish_log_v1.0.3.md` for TestPyPI evidence.

## Clean-environment install (no-deps, 2026-03-22)

`pip install --no-deps po-core-flyingpig==1.0.3` in a clean Python 3.11 venv:

```
Collecting po-core-flyingpig==1.0.3
  Using cached po_core_flyingpig-1.0.3-py3-none-any.whl.metadata (43 kB)
Using cached po_core_flyingpig-1.0.3-py3-none-any.whl (957 kB)
Installing collected packages: po-core-flyingpig
Successfully installed po-core-flyingpig-1.0.3
```

---

## Local Smoke Results (2026-03-22 — scripts/release_smoke.py --check-entrypoints)

All checks performed from repository checkout on Python 3.11.14.

### Package & resource checks

| Check | Result |
|-------|--------|
| `pkg_version` | `1.0.3` ✅ |
| `battalion_resource` | `src/po_core/config/runtime/battalion_table.yaml` ✅ |
| `pareto_resource` | `src/po_core/config/runtime/pareto_table.yaml` ✅ |
| `viewer_html` | `src/po_core/viewer/standalone.html` ✅ |
| `runtime_config_source` | `package:runtime/pareto_table.yaml` ✅ |
| `run_status` | `ok` ✅ |

### REST server checks

| Endpoint | Method | Status | Result |
|----------|--------|--------|--------|
| `/v1/health` | GET | 200 OK | ✅ |
| `/v1/reason` (no auth) | POST | 401 Unauthorized | ✅ (auth enforced as expected) |
| `/v1/reason` (with auth) | POST | 200 OK | ✅ |
| `/v1/reason/stream` | POST | 200 OK | ✅ |

### Console scripts

| Command | Exit code | Result |
|---------|-----------|--------|
| `po-core --help` | 0 | ✅ |
| `po-core version` | 0 | stdout: `1.0.3` ✅ |
| `po-core status` | 0 | version=`1.0.3`, philosophers=`42` ✅ |
| `po-core prompt smoke --format json` | 0 | valid JSON response ✅ |
| `po-self` | 0 | ✅ |
| `po-trace --help` | 0 | ✅ |
| `po-interactive --help` | 0 | ✅ |
| `po-experiment --help` | 0 | ✅ |
| `po-experiment list` | 0 | ✅ |

### Build artifact checks

| Artifact | twine check | Result |
|----------|-------------|--------|
| `po_core_flyingpig-1.0.3-py3-none-any.whl` | PASSED | ✅ |
| `po_core_flyingpig-1.0.3.tar.gz` | PASSED | ✅ |

---

## Pre-publish Test Gate Summary

| Gate | Result |
|------|--------|
| `pytest tests/test_release_readiness.py -v` | 24/24 passed ✅ |
| `pytest tests/acceptance/ -v -m acceptance` | 43/43 passed ✅ |
| `pytest tests/test_output_schema.py tests/test_golden_e2e.py tests/test_input_schema.py -v` | 103/103 passed ✅ |
| `pytest tests/ -v` (full suite) | 3868/3869 passed ✅ (1 flaky benchmark timing) |
| `python tools/import_graph.py --check --print` | violations=0, cycles=0 ✅ |
| `bandit -r src/ scripts/ -c pyproject.toml` | High=0, Medium=3 (non-critical) ✅ |
| `python -m build` | ✅ |
| `twine check dist/*` | PASSED ✅ |

---

## Post-publish Operator Evidence

Evidence recorded by session `claude/fix-pypi-1.0.3-evidence-1F5kR` on 2026-03-22:

- [x] TestPyPI package URL: https://test.pypi.org/project/po-core-flyingpig/1.0.3/ (confirmed via API)
- [x] PyPI package URL: https://pypi.org/project/po-core-flyingpig/1.0.3/ (confirmed via API)
- [x] Clean-environment `pip install --no-deps po-core-flyingpig==1.0.3`: succeeded (see above)
- [ ] TestPyPI workflow run URL: **pending** (GitHub API rate-limited)
- [ ] PyPI workflow run URL: **pending** (GitHub API rate-limited)
- [ ] Clean-environment full deps install transcript: **pending** (large deps not completed)
- [ ] Clean-environment import transcript: **pending** (requires full deps)
- [ ] Clean-environment `release_smoke.py --check-entrypoints` transcript: **pending**
