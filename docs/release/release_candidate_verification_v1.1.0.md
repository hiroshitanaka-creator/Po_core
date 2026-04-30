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
