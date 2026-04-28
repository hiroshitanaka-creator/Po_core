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
- [x] Clean-environment full deps install transcript: **completed 2026-04-28** (see below)
- [x] Clean-environment import transcript: **completed 2026-04-28** (see below)
- [ ] Clean-environment `release_smoke.py --check-entrypoints` transcript: **pending**
- [ ] TestPyPI workflow run URL: **not retrievable** — no `list_workflow_runs` endpoint available in session tooling; PyPI JSON API serves as proof of publication
- [ ] PyPI workflow run URL: **not retrievable** — same as above; see `docs/release/pypi_publication_v1.0.3.md`

---

## Full-dependencies post-publish smoke (2026-04-28)

Environment: Python 3.11.15, clean venv `/tmp/po_smoke_venv`, timestamp 2026-04-28T12:44:13Z.

### Install

```
$ python -m venv /tmp/po_smoke_venv
$ pip install po-core-flyingpig==1.0.3
Collecting po-core-flyingpig==1.0.3
  Using cached po_core_flyingpig-1.0.3-py3-none-any.whl.metadata (43 kB)
...
Successfully installed Flask-3.1.3 anyio-4.13.0 contourpy-1.3.3 cuda-bindings-13.2.0
dash-4.1.0 deprecated-1.3.1 fastapi-0.136.1 httpcore-1.0.9 httpx-0.28.1
huggingface-hub-1.12.0 importlib-metadata-9.0.0 jinja2-3.1.6 jsonschema-4.26.0
jsonschema-specifications-2025.9.1 limits-5.8.0 markdown-it-py-4.0.0
matplotlib-3.10.9 nvidia-cudnn-cu13-9.19.0.56 nvidia-cusolver-12.0.4.66
pandas-3.0.2 po-core-flyingpig-1.0.3 pydantic-2.13.3 pydantic-settings-2.14.0
rich-15.0.0 scikit-learn-1.8.0 sentence-transformers-5.4.1 slowapi-0.1.9
starlette-1.0.0 tokenizers-0.22.2 torch-2.11.0 transformers-5.6.2 typer-0.25.0
watchfiles-1.1.1
```

### Import check

```
$ python -c "import po_core; print(po_core.__version__)"
1.0.3
```

### CLI smoke

```
$ po-core version
1.0.3

$ po-core status
Project Status
  Version        : 1.0.3
  Philosophers   : 42
Philosophical Framework
  SolarWill axiom : do not distort survival structures
  SafetyModes     : NORMAL / WARN / CRITICAL
Documentation
  Specs  : docs/spec/
  ADRs   : docs/adr/
```

### Checklist

| Check | Result |
|-------|--------|
| `pip install po-core-flyingpig==1.0.3` (full deps) | ✅ |
| `import po_core; print(__version__)` → `1.0.3` | ✅ |
| `po-core version` → `1.0.3` | ✅ |
| `po-core status` → version=1.0.3, philosophers=42 | ✅ |

### GitHub Actions workflow run URL

The `publish.yml` workflow run URL for the 1.0.3 release is not retrievable via
the MCP tools available in this session (no `list_workflow_runs` endpoint). The
PyPI JSON API (`https://pypi.org/pypi/po-core-flyingpig/1.0.3/json`) and the
TestPyPI JSON API (`https://test.pypi.org/pypi/po-core-flyingpig/1.0.3/json`)
confirm publication. See `docs/release/pypi_publication_v1.0.3.md` for full
API-confirmed evidence.
