# Release Candidate Verification — v1.1.0

> ⚠️ **LOCAL PRE-PUBLISH VERIFICATION ONLY**
>
> This document records local verification of the v1.1.0 release candidate.
> No TestPyPI publish, no PyPI publish, no git tag, and no GitHub Release
> have been performed as part of this verification.

---

## Verification Context

| Field | Value |
|-------|-------|
| Date | 2026-04-30 |
| Branch | `main` |
| Verified tree commit | `5c4bd7f` (docs: update completion_matrix Source to main @ 3d1d657) |
| Evidence document commit | `254afd5` (docs(release): add release_candidate_verification_v1.1.0.md) |
| Release commit | `3d1d657` (release: prepare v1.1.0 — PR #548 squash merge) |
| Python | 3.11.15 |
| Verified by | Claude Code (RELEASE-CANDIDATE-VERIFY-1) |

---

## Step 1 — Version Check

**Command:**
```
python -c "import po_core; print(po_core.__version__)"
```

**Result:**
```
1.1.0
```

**Status:** ✅ PASS — `po_core.__version__ == "1.1.0"` confirmed.

---

## Step 2 — Build Artifacts

**Command:**
```
python -m build
```

**Artifacts produced:**
```
dist/po_core_flyingpig-1.1.0-py3-none-any.whl
dist/po_core_flyingpig-1.1.0.tar.gz
```

**Status:** ✅ PASS — both sdist and wheel built without errors.

---

## Step 3 — Artifact Validation

**Command:**
```
twine check dist/*
```

**Result:**
```
Checking dist/po_core_flyingpig-1.1.0-py3-none-any.whl: PASSED
Checking dist/po_core_flyingpig-1.1.0.tar.gz: PASSED
```

**Status:** ✅ PASS — both artifacts pass twine metadata validation.

---

## Step 4 — Release Readiness Tests

**Command:**
```
pytest tests/test_release_readiness.py -q
```

**Result:**
```
24 passed in 0.14s
```

**Status:** ✅ PASS — all 24 release readiness assertions pass.

---

## Step 5 — Smoke Script

**Command:**
```
python scripts/release_smoke.py --check-entrypoints
```

**Result:**
```
pkg_version=1.1.0
dist_metadata=ignoring unrelated installed distribution metadata at /usr/local/lib/python3.11/dist-packages/po_core/__init__.py (imported checkout uses /home/user/Po_core/src/po_core/__init__.py)
dist_version=skipped
battalion_resource=.../src/po_core/config/runtime/battalion_table.yaml
pareto_resource=.../src/po_core/config/runtime/pareto_table.yaml
viewer_html=.../src/po_core/viewer/standalone.html
runtime_config_source=package:runtime/pareto_table.yaml
run_status=ok
cli_name=main
```

**Status:** ✅ PASS — `pkg_version=1.1.0`, `run_status=ok`, `cli_name=main`.

Note: `dist_version=skipped` is expected — the installed system-site package is unrelated to this checkout; the checkout's `src/` layout takes precedence via editable install.

---

## Step 6 — Clean Wheel Install Smoke

**Venv:** `/tmp/po-core-v1.1.0-wheel-smoke` (Python 3.11, freshly created, no dev checkout on `sys.path`)

**Commands:**
```
python -m venv /tmp/po-core-v1.1.0-wheel-smoke
/tmp/po-core-v1.1.0-wheel-smoke/bin/python -m pip install --upgrade pip
/tmp/po-core-v1.1.0-wheel-smoke/bin/python -m pip install dist/po_core_flyingpig-1.1.0-py3-none-any.whl
/tmp/po-core-v1.1.0-wheel-smoke/bin/python -c "import po_core; print(po_core.__version__)"
/tmp/po-core-v1.1.0-wheel-smoke/bin/po-core version
/tmp/po-core-v1.1.0-wheel-smoke/bin/po-core status
/tmp/po-core-v1.1.0-wheel-smoke/bin/python scripts/release_smoke.py --check-entrypoints
```

**Install result:**
```
Successfully installed po-core-flyingpig-1.1.0 (and dependencies)
```

**Version check:**
```
1.1.0
```

**`po-core version`:**
```
1.1.0
```

**`po-core status`:**
```
Project Status
  Version        : 1.1.0
  Philosophers   : 42
Philosophical Framework
  SolarWill axiom : do not distort survival structures
  SafetyModes     : NORMAL / WARN / CRITICAL
Documentation
  Specs  : docs/spec/
  ADRs   : docs/adr/
```

**`scripts/release_smoke.py --check-entrypoints` (key lines):**
```
pkg_version=1.1.0
dist_metadata=matched import path /tmp/po-core-v1.1.0-wheel-smoke/lib/python3.11/site-packages/po_core/__init__.py
dist_version=1.1.0
battalion_resource=/tmp/.../site-packages/po_core/config/runtime/battalion_table.yaml
pareto_resource=/tmp/.../site-packages/po_core/config/runtime/pareto_table.yaml
viewer_html=/tmp/.../site-packages/po_core/viewer/standalone.html
runtime_config_source=package:runtime/pareto_table.yaml
run_status=ok
cli_name=main
```

All six CLI entrypoints (`po-core`, `po-self`, `po-trace`, `po-interactive`, `po-experiment`, `po-core version/status`) resolved and ran successfully from the wheel-installed path. REST server smoke (health + reason + stream) passed. `po-core prompt smoke` timed out after 15 s (expected — requires LLM backend not present in a clean venv; not a packaging defect).

**Key distinction from Step 5:** `dist_version=1.1.0` (confirmed from wheel metadata), not `skipped`. The installed package path is the venv site-packages, not the dev checkout.

**Status:** ✅ PASS — wheel installs cleanly, all entrypoints resolve from wheel, `dist_version=1.1.0` confirmed.

---

## Summary

| Step | Command | Result |
|------|---------|--------|
| 1. Version check | `python -c "import po_core; print(po_core.__version__)"` | ✅ `1.1.0` |
| 2. Build | `python -m build` | ✅ sdist + wheel produced |
| 3. Twine check | `twine check dist/*` | ✅ both PASSED |
| 4. Release readiness | `pytest tests/test_release_readiness.py -q` | ✅ 24 passed |
| 5. Smoke (dev checkout) | `python scripts/release_smoke.py --check-entrypoints` | ✅ run_status=ok |
| 6. Clean wheel smoke | venv install + CLI + smoke script | ✅ dist_version=1.1.0, all entrypoints ok |

**Overall verdict: ✅ v1.1.0 release candidate is locally verified and ready for publish.**

---

## Explicit Non-Actions

- ❌ No TestPyPI publish
- ❌ No PyPI publish
- ❌ No git tag created
- ❌ No GitHub Release created

These actions are deferred to the operator publish runbook (`docs/operations/publish_playbook.md`).

---

## Appendix — Post-PR#552/#553 Re-verification (2026-05-14)

| Field | Value |
|-------|-------|
| Date | 2026-05-14 |
| Branch | `main` |
| Verified tree commit | `bb60897` (fix(schemas): import Traversable from importlib.resources.abc #553) |
| PRs merged | #552 (acceptance golden update), #553 (Traversable import fix) |
| Python | 3.11.15 (primary) / 3.13.12 (supplementary) |
| Verified by | Claude Code (audit-v1.1.0-release) |

### Context

After the initial RC verification (2026-04-30), two fixes were merged:

- **PR #552** — Regenerated acceptance golden files (AT-001/007/008/009/011) after philosopher roster expansion from 39 → 42 (Phase 7). Only `options[0].description` (philosopher proposal content) changed; all other fields were confirmed identical by code comparison.
- **PR #553** — Changed `src/po_core/schemas/__init__.py` to import `Traversable` from `importlib.resources.abc` (Python 3.9+) instead of deprecated `importlib.abc`. Python 3.13 confirms the old path emits `DeprecationWarning: slated for removal in Python 3.14`.

### Re-verification Results (Python 3.11.15, commit `bb60897`)

| Command | Result |
|---------|--------|
| `pytest tests/ -v -m "not slow"` | ✅ **3973 passed**, 16 deselected (6m 28s) |
| `pytest tests/acceptance/ -v -m acceptance` | ✅ 43 passed |
| `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v` | ✅ 62 passed |
| `pytest tests/test_release_readiness.py -v` | ✅ 24 passed |
| `bandit -r src/ scripts/ -c pyproject.toml -ll` | ✅ No issues (CI gate PASS) |
| `bandit -r src/ scripts/ -c pyproject.toml -l` | 2 Low B110 (`ensemble.py:311`, `tracer.py:237`); non-CI-gate |
| `python -m build` | ✅ wheel + sdist produced |
| `twine check dist/*` | ✅ PASSED |
| `python scripts/release_smoke.py --check-entrypoints` | ✅ All entry points RC=0 |

### Python 3.13.12 Supplementary Verification

| Check | Result |
|-------|--------|
| `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v` | ✅ **62 passed** |
| `from importlib.resources.abc import Traversable` (post-PR#553 path) | ✅ OK — no DeprecationWarning |
| `from importlib.abc import Traversable` (pre-PR#553 path) | ❌ `DeprecationWarning: slated for removal in Python 3.14` |
| `-W error::DeprecationWarning` mode | ⚠️ 52 passed, 10 errors — errors caused by `src/pocore/` legacy shim DeprecationWarning, **unrelated to Traversable** |

Note on 10 errors: `src/pocore/__init__.py` intentionally emits a DeprecationWarning at import (documented in CLAUDE.md: "test-only scaffold... will be deleted in a future release"). This is a separate, known issue, not introduced by PR #552 or #553.

### Bandit Low Severity Detail (non-CI-gate)

| # | Rule | File:Line | Note |
|---|------|-----------|------|
| 1 | B110 try_except_pass | `src/po_core/ensemble.py:311` | Silent fallback returning empty string for philosopher author extraction |
| 2 | B110 try_except_pass | `src/po_core/trace/tracer.py:237` | Intentional swallow of PoTrace logging failures; comment present explaining rationale |

Per `pyproject.toml` bandit policy: B110 is not globally skipped; intentional occurrences should carry `# nosec B110`. These two sites lack the annotation. Non-blocking for this release; tracked as next-PR candidate.

### Python 3.14 Status

Python 3.14 is not available in this environment. Python 3.13 proxy verification confirms the `importlib.resources.abc.Traversable` fix is correct and warning-free. Full test suite on Python 3.14 remains **unverified**.

### Explicit Non-Actions (Appendix)

- ❌ No PyPI publish
- ❌ No git tag created
- ❌ No GitHub Release created
- ❌ No `pocore` shim DeprecationWarning suppressed (tracked separately)
