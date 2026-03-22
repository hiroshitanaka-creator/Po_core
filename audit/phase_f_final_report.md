# Phase F: Final Audit Report — po-core-flyingpig v1.0.3

**Audit branch:** `claude/audit-po-core-v1.0.3-FaZVy`
**Audit date:** 2026-03-22
**Audited HEAD (at audit start):** `39803f8`
**Phases completed:** A (Baseline Freeze) → B (Inventory) → C (Command Rerun) → D (Rerun Logs) → E (Findings) → F (This Report)

---

## Executive Summary

The audit covered 6 categories (Packaging, API Surface, Docs/Version, Tests, Security, Build/Publish)
across 1070 tracked files. 103 schema/golden tests and 43 acceptance tests pass cleanly.
The critical path to publishing v1.0.3 is **blocked by 3 P1 findings** that must be resolved before PyPI publish.
An additional 11 P2 findings should be addressed before or immediately after publish.

**Verdict: NOT READY FOR PYPI PUBLISH as-is. Resolve P1 items first.**

---

## Finding Severity Counts

| Severity | Count | Description |
|----------|-------|-------------|
| P1 (Blocker) | 3 | Must fix before publish |
| P2 (Important) | 10 | Should fix before or shortly after publish |
| P3 (Minor) | 9 | Technical debt, non-blocking |
| INFO | 2 | Informational, no action required |
| OK | 14 | Confirmed correct |

---

## P1 Blockers (Must Fix Before PyPI Publish)

### P1-D1/D2/F2: Benchmark Tests Failing + CI Publish Blocked

**Finding IDs:** D1, D2, F2

**What happened:**
- Baseline claimed "3868/3869 passed ✅ (1 flaky benchmark timing)"
- Rerun collected 3873 tests; **2 FAILED**:
  - `test_bench_critical_p50` — 1.064s ≥ 1.0s threshold
  - `test_bench_concurrent_warn_requests` — 5.825s ≥ 4.0s threshold
- Both failing tests are `@pytest.mark.slow` and `@pytest.mark.benchmark`
- `publish.yml` runs `pytest tests/ -v` without `-m "not slow"` — benchmark failures **will block CI publish**

**Root cause:** Benchmark thresholds are hard-coded, environment-sensitive, and not excluded from CI.

**Fix options (choose one):**
1. Add `-m "not slow"` to `publish.yml` pytest invocation (fastest, recommended)
2. Raise benchmark thresholds to tolerate slower CI runners (e.g., p50 < 2.0s, concurrent < 10.0s)
3. Mark benchmarks as `xfail` with a lenient threshold

**Recommended action:** Option 1 — add `-m "not slow"` to `publish.yml`. Also add to `pytest.ini` as default
`addopts` so `pytest tests/ -v` does not run slow tests by default.

---

### P1-H3/I3: `src/pocore` Schema Path Breaks in Clean Wheel Install

**Finding IDs:** H3, I3

**What happened:**
- `src/pocore/runner.py` resolves schema files using `Path(__file__).parents[N] / "docs/spec/input_schema_v1.json"`
- This path assumes the `docs/spec/` directory exists alongside the Python file (i.e., full repo checkout)
- In a wheel install, `docs/` is **NOT packaged** — only `src/po_core/schemas/*.json` is packaged
- Any user who does `pip install po-core-flyingpig` and imports from `pocore.runner` will get a `FileNotFoundError`

**Note:** `src/pocore` is not itself packaged (`po_core*` only). However, during pytest with `pythonpath = src`,
`pocore` IS importable, meaning this code path IS exercised in tests but from a different file layout than
a real install. Tests pass; production install would fail.

**Fix options:**
1. Update `src/pocore/runner.py` to use `importlib.resources` or `pkg_resources` to load schemas from
   `po_core.schemas` package (which IS packaged)
2. Add `pocore` to `pyproject.toml` `include = ["po_core*", "pocore*"]` AND add `docs/spec/` to package-data
3. Remove/deprecate `src/pocore/runner.py` if it's internal scaffolding not intended for end users

**Recommended action:** Option 3 first — determine if `pocore.runner` is part of the public API or internal
scaffolding. If internal only, add a `# NOT FOR END USERS` docstring and exclusion from wheel. If public,
apply Option 1.

---

## P2 Findings (Important — Fix Before/Shortly After Publish)

### P2-A3 / F4: `SetuptoolsDeprecationWarning` in Build (Will Break in 2027)

`pyproject.toml` uses `project.license` as TOML table (old format). Will become a **hard error** on
2027-02-18 per setuptools roadmap. Fix: change to `license = "AGPL-3.0-or-later"` string format.

```toml
# Before (TOML table — deprecated)
[project]
license = {text = "AGPL-3.0-or-later"}

# After (inline string — new standard)
[project]
license = "AGPL-3.0-or-later"
```

---

### P2-C1: `CLAUDE.md` Stale Version (0.2.0rc1 vs actual 1.0.3)

`CLAUDE.md` header says `Version: 0.2.0rc1` while `src/po_core/__init__.py` says `1.0.3`.
The roadmap/milestone table in CLAUDE.md shows stale M1-M4 history as "current status".
This does not affect functionality but misleads contributors and CI bot context.

**Fix:** Update `CLAUDE.md` "Current Status" section and version references.

---

### P2-C2 / D4 / J1: TypeScript SDK README says "1.0.2"

`clients/typescript/README.md` line 5 says version 1.0.2. Users following the README would install
the wrong version. Not caught by `test_release_readiness.py` `DOCS_WITH_VERSION` list.

**Fix:** Update `clients/typescript/README.md` to `1.0.3` AND add it to `DOCS_WITH_VERSION` in
`tests/test_release_readiness.py`.

---

### P2-C3 / D5 / J3: `examples/README.md` References `po-core-flyingpig==1.0.2`

Same issue as above for examples directory. Users doing `pip install "po-core-flyingpig==1.0.2"` would
get the old version.

**Fix:** Update to `1.0.3` AND add `examples/README.md` to `DOCS_WITH_VERSION`.

---

### P2-E1: `pickle.loads` in `philosopher_worker.py` (Bandit B301)

Internal IPC only (parent-controlled stdin pipe). Low real-world risk but flagged by Bandit as Medium/CWE-502.
Consider adding a `# nosec B301` comment with justification, or switching to `json`/`msgpack` for IPC
to eliminate the finding permanently.

---

### P2-E2: REST Server Binds `0.0.0.0` While Docs Claim "localhost-only"

`rest/config.py` host defaults to `0.0.0.0` (all interfaces). `docs/status.md` says "localhost-only CORS"
which is technically true for CORS but misleading for the HOST binding. `curl` bypasses CORS entirely.

**Fix:** Either change default host to `127.0.0.1` OR update docs to accurately state
"all-interface bind (firewall externally; CORS restricts browser clients only)".

---

### P2-H2: `src/pocore` Importable in Tests but NOT in Production Wheel

`pytest.ini` adds `src/` to `pythonpath`, so tests can import `pocore.*`. The production wheel does NOT
include `pocore`. If any test imports `pocore.*` and those code paths are only valid with repo checkout,
a CI green result does not guarantee production correctness.

**Fix:** Either package `pocore` explicitly, or add a test that verifies `pocore` is NOT importable in
the installed wheel context (similar to how experimental prompts are tested for exclusion).

---

### P2-J4: Duplicate PR Templates with Governance Regression

`.github/pull_request_template.md` (lowercase) is missing the M4 requirement traceability section
that `.github/PULL_REQUEST_TEMPLATE.md` (uppercase) has. GitHub uses the uppercase file by convention,
so the lowercase one may never be shown. But having two templates creates confusion and a maintenance hazard.

**Fix:** Delete `.github/pull_request_template.md` (lowercase) and keep only the uppercase one.

---

## P3 Findings (Minor Technical Debt)

| ID | Issue | Recommended Action |
|----|-------|-------------------|
| A2 | Non-lazy import of `PHILOSOPHER_REGISTRY` at module level | Defer to lazy property; reduces cold-start time |
| A4 | `src/pocore/orchestrator.py` has `POCORE_VERSION = "1.0.0"` (vs package 1.0.3) | Add comment clarifying this is internal scaffold version; consider unifying |
| B2 | `po-self --help` says "39 active" (3 excluded from NORMAL mode) | Clarify in docs; `philosophers_max_normal=39` is a config value |
| B4 | `sentence-transformers` model downloaded on cold start | Pre-download in Docker build stage; add to `Dockerfile` |
| C5 | CHANGELOG `[Unreleased]` section after `[1.0.2]` (non-standard placement) | Move `[Unreleased]` to top per Keep a Changelog standard |
| C6 | CHANGELOG contains Japanese metadata banner (not changelog content) | Remove lines 39-47 from CHANGELOG |
| D3 | `test_release_readiness.py` hardcodes `version == "1.0.3"` | Use `po_core.__version__` dynamically |
| D6 | Test count mismatch (baseline 3869 vs rerun 3873) | Document when tests were added; update baseline |
| J2 | `clients/typescript/package.json` version "1.0.0" (not aligned with 1.0.3) | Align or document intentional divergence |
| F5 | Clean venv wheel install requires network for `torch` | Add `--extra-index-url` or note offline install limitation |

---

## INFO (No Action Required)

| ID | Note |
|----|------|
| C4 | v1.0.2 published with `5-Production/Stable` classifier; v1.0.3 intentionally downgrades to `4-Beta`. Explain in release notes. |
| G4 | Golden files use `FROZEN_PROFILE_POCORE_VERSION = "0.1.0"` / `"1.0.0"` (not 1.0.3). Intentional frozen snapshot versioning. |

---

## Confirmed OK (Verified Correct)

| ID | Claim | Verification |
|----|-------|-------------|
| A1 | Wheel contains only `po_core` (not `pocore`) | Confirmed |
| B1 | All 5 console scripts work | Confirmed (all RC=0) |
| B3 | REST health/reason/stream endpoints working | Confirmed |
| E3 | Auth fail-closed (`PO_SKIP_AUTH=false` + empty key → startup abort) | Confirmed |
| E4 | Bandit: High=0, Medium=3, Low=46 | Confirmed |
| F1 | Build + twine check pass | Confirmed |
| F3 | TestPyPI prerequisite gate works (same-SHA check) | Confirmed |
| G1 | 103/103 schema/golden tests pass | Confirmed |
| G2 | 43/43 acceptance tests pass | Confirmed |
| G3 | 24/24 release readiness tests pass | Confirmed |
| H1 | `src/pocore` not in wheel | Confirmed |
| I1 | `config/*.yaml` packaged and accessible | Confirmed |
| I2 | `viewer/*.html` packaged and accessible | Confirmed |
| I4 | Experimental prompt YAMLs not in wheel | Confirmed |

---

## Recommended Resolution Order

### Before PyPI Publish (P1 — Blockers)

1. **Fix publish.yml / pytest.ini** — exclude `slow`/`benchmark` tests from CI publish job (P1-D1/D2/F2)
2. **Resolve `src/pocore` schema path** — determine if `pocore.runner` is public API or internal scaffold;
   either fix path resolution or explicitly exclude from wheel (P1-H3/I3)

### Before or at PyPI Publish (P2 — Important)

3. Update `pyproject.toml` license format (P2-A3/F4) — 5 min fix, avoids future build break
4. Update `clients/typescript/README.md` + `examples/README.md` version refs → 1.0.3 (P2-C2/C3/J1/J3)
5. Add missing docs to `DOCS_WITH_VERSION` in `test_release_readiness.py` (P2-D4/D5)
6. Delete duplicate lowercase PR template (P2-J4)
7. Fix REST host binding docs accuracy (P2-E2) — 1-line docs fix

### Shortly After Publish (P2 — Post-publish cleanup)

8. Add `# nosec B301` to `philosopher_worker.py` pickle usage with justification (P2-E1)
9. Clarify `pocore` test-vs-production importability; add exclusion test (P2-H2)
10. Update `CLAUDE.md` version references (P2-C1)

---

## Baseline vs Rerun Contradiction Summary

| Claim | Baseline | Rerun Result |
|-------|---------|--------------|
| Test count | 3869 collected | 3873 collected (+4 tests added after baseline) |
| Failures | "1 flaky benchmark timing" | **2 FAILED** (distinct threshold violations) |
| REST host | "localhost-only CORS" (status.md) | Code binds `0.0.0.0`; CORS is localhost-only but host is not |

---

## Audit Completeness

| Phase | Status | Evidence |
|-------|--------|----------|
| A: Baseline Freeze | ✅ Complete | `audit/00_baseline/baseline_truth.md` |
| B: File Inventory | ✅ Complete | `audit/01_inventory/tracked_files_sorted.txt` (1070 files) |
| C/D: Command Rerun + Logs | ✅ Complete | `audit/02_rerun_logs/` (12 command logs + environment_info.txt) |
| E: Findings Diff | ✅ Complete | `audit/phase_e_findings.md` (categories A–J, 38 findings) |
| F: Final Report | ✅ Complete | This file |

**Total findings:** 38 (3 P1 + 10 P2 + 9 P3 + 2 INFO + 14 OK)
