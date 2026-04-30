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
| Head commit | `5c4bd7f` (docs: update completion_matrix Source to main @ 3d1d657) |
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

## Summary

| Step | Command | Result |
|------|---------|--------|
| 1. Version check | `python -c "import po_core; print(po_core.__version__)"` | ✅ `1.1.0` |
| 2. Build | `python -m build` | ✅ sdist + wheel produced |
| 3. Twine check | `twine check dist/*` | ✅ both PASSED |
| 4. Release readiness | `pytest tests/test_release_readiness.py -q` | ✅ 24 passed |
| 5. Smoke | `python scripts/release_smoke.py --check-entrypoints` | ✅ run_status=ok |

**Overall verdict: ✅ v1.1.0 release candidate is locally verified and ready for publish.**

---

## Explicit Non-Actions

- ❌ No TestPyPI publish
- ❌ No PyPI publish
- ❌ No git tag created
- ❌ No GitHub Release created

These actions are deferred to the operator publish runbook (`docs/operations/publish_playbook.md`).
