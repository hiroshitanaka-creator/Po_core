# Phase E: Baseline Claim vs Rerun Fact Diff

## Findings Table

Each finding has `evidence_source`:
- `baseline_repo`: claim found only in repo docs (docs/status.md, smoke_verification, etc.)
- `rerun_verified_here`: independently verified by running commands in this audit session
- `source_read_verified`: independently verified by reading source files

---

### A. Packaging / Import Defects

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| A1 | `src/pocore` NOT packaged in wheel | baseline_repo claims runtime package is `po_core*` only | Wheel inspection: `pocore` absent, only `po_core` present. CONFIRMED CORRECT. | OK | rerun_verified_here |
| A2 | `src/po_core/__init__.py` non-lazy import of `PHILOSOPHER_REGISTRY` | No baseline claim about import-time cost | Source: `from po_core.ensemble import PHILOSOPHER_REGISTRY` at module level triggers heavy import chain. Can delay first-import in production. | P3 | source_read_verified |
| A3 | `SetuptoolsDeprecationWarning` for `project.license` as TOML table | No baseline claim | Build rerun: Warning appears in `python -m build`. Will BREAK builds in 2027 unless `pyproject.toml` updated to `license = "AGPL-3.0-or-later"` string. | P2 | rerun_verified_here |
| A4 | `src/pocore/orchestrator.py` has `POCORE_VERSION = "1.0.0"` | No baseline claim | Source: internal scaffold version is 1.0.0, but packaged runtime is 1.0.3. These are DIFFERENT systems. Intentional by design but could confuse users. | P3 | source_read_verified |

---

### B. Broken Entrypoints / CLI / API Surface

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| B1 | All 5 console scripts work | `smoke_verification_v1.0.3.md`: all 5 scripts passed | `release_smoke.py --check-entrypoints` rerun: all 5 scripts RC=0. CONFIRMED. | OK | rerun_verified_here |
| B2 | `po-self --help` says "39 active" | No baseline claim | Source: `po_self.py` line 405: "42 philosophers integrated (39 active)". `philosophers_max_normal=39` confirms 3 philosophers excluded from NORMAL mode selection. Public count = 42. Not a defect but requires clear docs. | P3 | source_read_verified |
| B3 | REST endpoints (health/reason/stream) working | `smoke_verification_v1.0.3.md`: all REST endpoints passed | Rerun: health=200, reason(auth)=401, reason(no-auth)=200, stream=200. CONFIRMED. | OK | rerun_verified_here |
| B4 | `sentence-transformers` model not pre-downloaded | No baseline claim | Rerun: "No sentence-transformers model found with name sentence-transformers/all-MiniLM-L6-v2. Creating a new one with mean pooling." — emitted on every cold start. May cause slow first request. | P3 | rerun_verified_here |

---

### C. Version Drift / Docs Drift / Stale Claims

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| C1 | CLAUDE.md has stale version `0.2.0rc1` | CLAUDE.md references M1-M4 complete, but version shown is 0.2.0rc1 | Source: `src/po_core/__init__.py` __version__ = "1.0.3". CLAUDE.md is SIGNIFICANTLY stale. M1-M4 roadmap section shows outdated milestone state. | P2 | source_read_verified |
| C2 | `clients/typescript/README.md` says "1.0.2" | No baseline claim | Source: line 5 says `1.0.2 in this repo snapshot`. Package is now 1.0.3. Not caught by `DOCS_WITH_VERSION` list in `test_release_readiness.py`. | P2 | source_read_verified |
| C3 | `examples/README.md` references `po-core-flyingpig==1.0.2` | No baseline claim | Source: `pip install "po-core-flyingpig==1.0.2"` in examples README. Should say 1.0.3. Not caught by release readiness tests. | P2 | source_read_verified |
| C4 | `docs/release/pypi_publication_v1.0.2.md` claims `Development Status :: 5 - Production/Stable` on PyPI | Evidence captured from PyPI page (v1.0.2) | Source: `pyproject.toml` line 29 has `"Development Status :: 4 - Beta"`. CHANGELOG says classifier was DOWNGRADED for 1.0.3. The discrepancy is explained (1.0.2 was published with `5-Stable`, 1.0.3 will publish with `4-Beta`). Not a defect but important to note for users. | INFO | source_read_verified |
| C5 | CHANGELOG `[Unreleased]` section misplaced | No baseline claim | Source: CHANGELOG line 49 has `[Unreleased]` (empty) AFTER `[1.0.2]` entry. Per Keep a Changelog standard, `[Unreleased]` must be FIRST section before any version. Structure is non-standard. | P3 | source_read_verified |
| C6 | CHANGELOG has metadata banner debris | No baseline claim | Source: CHANGELOG lines 39-47 contain "最優先ルール（単一真実）" banner (copied from status doc). Not valid changelog content. | P3 | source_read_verified |

---

### D. Test Gaps / False Confidence

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| D1 | 2 benchmark tests FAILED in full suite | `smoke_verification_v1.0.3.md`: "3868/3869 passed ✅ (1 flaky benchmark timing)" | Rerun: `3867/3873 collected, 2 FAILED, 4 skipped`. Failed: `test_bench_critical_p50` (1.064s≥1.0s) and `test_bench_concurrent_warn_requests` (5.825s≥4.0s). COUNT MISMATCH: baseline claims 1 flaky, rerun finds 2 failed. | P1 | rerun_verified_here |
| D2 | Benchmark tests not excluded from full `pytest tests/ -v` | No baseline claim | Source: `pytest.ini` has no default deselection of `slow` or `benchmark` markers. CI workflows run `pytest tests/ -v` WITHOUT `-m "not slow"`. Both failing benchmarks are `@pytest.mark.slow` and `@pytest.mark.benchmark`. CI can fail on slow machines. | P1 | source_read_verified |
| D3 | `test_release_readiness.py` hardcodes `version == "1.0.3"` | No baseline claim | Source: line 111: `assert version == "1.0.3"`. If version changes, this test breaks. Not a current defect, but a maintenance debt. | P3 | source_read_verified |
| D4 | `clients/typescript/README.md` stale version not tested | No baseline claim | Source: `DOCS_WITH_VERSION` list does NOT include `clients/typescript/README.md`. The stale `1.0.2` reference passes all tests. | P2 | source_read_verified |
| D5 | `examples/README.md` stale version not tested | No baseline claim | Source: `DOCS_WITH_VERSION` does NOT include `examples/README.md`. | P2 | source_read_verified |
| D6 | Total test count mismatch | Baseline claims 3869 total collected | Rerun collected 3873 (4 more). Could indicate tests added after baseline recording. | P3 | rerun_verified_here |

---

### E. Security / Auth / Fail-Open Risks

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| E1 | `pickle.loads(sys.stdin.buffer.read())` in philosopher_worker.py | Bandit Medium baseline claim: "Medium=3 (non-critical)" | Source: B301 Medium, CWE-502. Worker receives pickled data from parent process over stdin pipe. Internal IPC only — parent controls stdin. Risk is low if not exposed externally. Bandit flags but in-process pipe IPC is common pattern. | P2 | source_read_verified |
| E2 | REST server binds `0.0.0.0` by default | `docs/status.md` says "localhost-only CORS" | Source: `rest/config.py` host="0.0.0.0". CORS is localhost-restricted but HOST is 0.0.0.0. CORS only restricts browser clients; direct `curl` bypasses CORS. Server is reachable on all interfaces unless firewalled. Status.md claim "localhost-only" is MISLEADING for the HOST binding. | P2 | source_read_verified |
| E3 | `PO_SKIP_AUTH=false` + empty `PO_API_KEY` causes startup abort | Baseline: "fail-closed by design" | Rerun + Source: startup abort confirmed. Auth enforcement verified. CONFIRMED CORRECT. | OK | rerun_verified_here |
| E4 | Bandit: High=0, Medium=3 confirmed | Baseline claimed "High=0, Medium=3 (non-critical)" | Rerun: High=0, Medium=3, Low=46. Three Medium issues: B301 (pickle), B104 (0.0.0.0), B310 (urlopen in release_smoke). MATCHES baseline. | OK | rerun_verified_here |

---

### F. Build / Publish Pipeline Mismatches

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| F1 | Build succeeds, twine check passes | Baseline: PASSED | Rerun: `python -m build` succeeded, both artifacts created (956KB whl, 977KB tar.gz). `twine check` PASSED both. CONFIRMED. | OK | rerun_verified_here |
| F2 | Full test suite with benchmarks could block publish workflow | No baseline claim | Source: `publish.yml` runs `pytest tests/ -v` without `-m "not slow"`. Benchmark failures would block CI publish. Combined with D1/D2. | P1 | source_read_verified |
| F3 | TestPyPI prerequisite required before PyPI publish | Baseline: "same-SHA TestPyPI prerequisite" | Source: `publish.yml` lines 99-177: verifies testpypi deployment for same SHA before allowing pypi publish. CONFIRMED CORRECT. Fail-closed. | OK | source_read_verified |
| F4 | SetuptoolsDeprecationWarning in build | No baseline claim | Rerun: `project.license` as TOML table deprecated, will break in 2027-Feb-18. Warning in build output. Not yet an error. | P2 | rerun_verified_here |
| F5 | Clean venv wheel install requires network (torch) | No baseline claim | Rerun: `--no-index` fails because `torch>=2.0.0` not available offline. Not tested as true clean install in this audit. | P3 | rerun_verified_here |

---

### G. Schema / Golden / Determinism Violations

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| G1 | All 103 schema/golden tests pass | Baseline: "103/103 passed ✅" | Rerun: cmd3 41/41 + cmd4 62/62 = 103/103. CONFIRMED. | OK | rerun_verified_here |
| G2 | All 43 acceptance tests pass | Baseline: "43/43 passed ✅" | Rerun: 43 passed. CONFIRMED. | OK | rerun_verified_here |
| G3 | All 24 release readiness tests pass | Baseline: "24/24 passed ✅" | Rerun: 24/24. CONFIRMED. | OK | rerun_verified_here |
| G4 | `src/pocore/orchestrator.py` uses `POCORE_VERSION = "1.0.0"` in golden output | No baseline claim | Source: golden files for case_001 and case_009 use `FROZEN_PROFILE_POCORE_VERSION = "0.1.0"`. Other cases use `1.0.0`. These are intentionally frozen and tested. Not a defect but clarifies that output JSON has different versioning from package version. | INFO | source_read_verified |

---

### H. `src/po_core` vs `src/pocore` Namespace Confusion

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| H1 | `src/pocore` NOT packaged | pyproject.toml: `include = ["po_core*"]` | Wheel inspection: only `po_core/` present. `pocore` absent. CONFIRMED. | OK | rerun_verified_here |
| H2 | `src/pocore` installed via pythonpath in pytest | `pytest.ini`: `pythonpath = src` | During tests, `src/pocore` is importable because pythonpath includes `src/`. This is test-only access. In production wheel install, `pocore` is NOT importable. | P2 | source_read_verified |
| H3 | `po_core` uses `pocore` indirectly via test imports | No baseline claim | Source: `src/pocore/runner.py` references `docs/spec/input_schema_v1.json` and `output_schema_v1.json` by walking up from file path. In production wheel, these schema files are NOT in `docs/spec/` path. They're in `src/po_core/schemas/`. The `pocore.runner` would FAIL to find schemas in a clean wheel install because the `docs/` directory is not packaged. | P1 | source_read_verified |

---

### I. Packaged vs Non-Packaged Asset Leakage

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| I1 | `config/*.yaml` files packaged | `pyproject.toml` package-data includes `config/*.yaml`, `config/*/*.yaml`, `config/*/*/*.yaml` | Wheel inspection: `config/` directory present. Resource check in smoke: `battalion_resource` and `pareto_resource` found. CONFIRMED. | OK | rerun_verified_here |
| I2 | `viewer/*.html` packaged | `pyproject.toml` package-data includes `viewer/*.html` | Smoke check: `viewer_html` found. CONFIRMED. | OK | rerun_verified_here |
| I3 | `docs/spec/` schemas NOT packaged | No baseline claim | Source: schemas are at `src/po_core/schemas/` (packaged) and `docs/spec/` (NOT packaged). `src/pocore/runner.py` reads from `docs/spec/` via filesystem path — this would break for users who install only the wheel (no `docs/` directory). | P1 | source_read_verified |
| I4 | Experimental prompt YAML files not packaged | `test_experimental_prompt_assets_are_isolated_from_runtime_package` test | Test verifies prompt YAMLs not in package. CONFIRMED. | OK | rerun_verified_here |

---

### J. Examples / SDK / Docs の誤誘導

| ID | Finding | Baseline Claim | Rerun / Source Fact | Severity | evidence_source |
|----|---------|---------------|---------------------|----------|----------------|
| J1 | TypeScript SDK version says "1.0.2" | No baseline claim | Source: `clients/typescript/README.md` line 5 says 1.0.2. User would install wrong version. | P2 | source_read_verified |
| J2 | TypeScript SDK `package.json` version "1.0.0" | No baseline claim | Source: `clients/typescript/package.json` has `"version": "1.0.0"`. Not aligned with Python package 1.0.3. No npm publish evidence. | P3 | source_read_verified |
| J3 | `examples/README.md` references old version | No baseline claim | Source: `pip install "po-core-flyingpig==1.0.2"`. User would install 1.0.2 when 1.0.3 is current. | P2 | source_read_verified |
| J4 | Duplicate PR templates with governance regression | No baseline claim | Source: `.github/pull_request_template.md` (lowercase) is missing M4 requirement traceability section that uppercase template has. GitHub uses PULL_REQUEST_TEMPLATE.md (uppercase) by convention but duplicate creates confusion. | P2 | source_read_verified |

---

## Summary of Contradictions (Baseline vs Rerun)

| Contradiction | Baseline | Rerun | Impact |
|-------------|---------|-------|--------|
| Full suite test count | 3869 total, 3868/3869 passed (1 flaky) | 3873 total, 3867 passed, 2 FAILED, 4 skipped | P1: 2 benchmark failures, not 1 |
| Benchmark failures | "1 flaky benchmark timing" | 2 distinct failed tests with clear thresholds exceeded | P1: could block CI publish |
| REST default host claim | "localhost-only CORS" (docs/status.md) | code binds 0.0.0.0 (all interfaces); CORS is localhost-only but HOST is not | P2: misleading docs |
