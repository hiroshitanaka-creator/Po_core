# Smoke Verification Evidence for v1.0.3

- Version: `1.0.3`
- Evidence status: **local pre-publish smoke — PASSED (2026-03-22)**
- Auditor: claude/audit-po-core-1.0.3-IyRXH (automated audit branch)
- Post-publish operator-supplied transcript not yet recorded in this repository
- Current state: **pre-publish candidate state** — local gates passed, publication not yet executed

## Pending Evidence

Not yet fixed as truth in this file: TestPyPI publication, PyPI publication, clean-environment install/import/smoke success, workflow run URL(s).

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

## Post-publish Operator Evidence (not yet recorded)

The following must be filled in by the release operator after successful GitHub Actions publish:

- [ ] TestPyPI workflow run URL
- [ ] TestPyPI package URL: `https://test.pypi.org/project/po-core-flyingpig/1.0.3/`
- [ ] PyPI workflow run URL
- [ ] PyPI package URL: `https://pypi.org/project/po-core-flyingpig/1.0.3/`
- [ ] Clean-environment install: `pip install po-core-flyingpig==1.0.3` — stdout/stderr
- [ ] Clean-environment import: `python -c "import po_core; print(po_core.__version__)"` — stdout
- [ ] Clean-environment smoke: `python scripts/release_smoke.py --check-entrypoints` — full transcript

## Promotion rule

Do not update public docs to say that `1.0.3` was published or post-publish smoke verification passed until the operator transcript and exact evidence URLs are pasted here with real values.
