# Release Candidate Operator Handoff for v1.1.0

Purpose: give the maintainer a compact, maintainer-focused pre-publish handoff bundle for release candidate `1.1.0` without overstating publication status.

## 1. Machine-verified facts already fixed in-repo

- Repository target version is `1.1.0`.
- Latest public PyPI evidence points to `1.0.3` via `docs/release/pypi_publication_v1.0.3.md` (published 2026-03-22).
- `pyproject.toml` reads package version dynamically from `src/po_core/__init__.py`.
- Release readiness guardrails exist in `tests/test_release_readiness.py`.
- `docs/status.md` explicitly separates pre-publish candidate truth from post-publish evidence truth.
- `docs/release/smoke_verification_v1.1.0.md` is intentionally a pending placeholder, not publish evidence.
- Completion matrix: **164 pass / 0 fail / 0 not-yet** (as of 2026-04-30).

## 2. What v1.1.0 adds over v1.0.3

- `po_core.run_case(case)` / `async_run_case(case)` public API (RT-GAP-004)
- Scenario-aware philosopher selection via `CaseSignals` + `_SCENARIO_ROUTING` (RT-GAP-001/002/003)
- Full engine trace audit contract: `SafetyModeInferred`, `CaseSignalsApplied`, `PhilosophersSelected` rationale, `ParetoWinnerSelected` weights+weighted_score, `TensorComputed` metric_status (TENSOR-TR-1/2, MODE-TR-1/2, SEL-TR-1, AGG-TR-1/2/3/4, TR-1)
- `docs/ENGINE_TRACE_CONTRACT.md` — full field-level spec for all trace events
- `docs/viewer/sample_trace.json` aligned to contract (TRACE-VIEW-1)
- 53 new tests (completion matrix: 110 → 164)
- All changes are backward-compatible: existing `po_core.run()` callers unaffected.

## 3. Operator evidence still required before stronger public claims

Do **not** claim any of the following for `1.1.0` until exact operator evidence is recorded in-repo:

- successful GitHub Actions workflow run URL(s)
- TestPyPI package URL(s) and whether TestPyPI was actually used
- PyPI version page URL for `1.1.0`
- clean-environment install transcript for `po-core-flyingpig==1.1.0`
- clean-environment import transcript showing `po_core.__version__ == "1.1.0"`
- clean-environment smoke transcript for the minimum supported runtime path
- final classification of the publication path: `TestPyPI only` or `TestPyPI + PyPI`

## 4. Pre-publish checklist

- [x] `src/po_core/__init__.py` `__version__` = `"1.1.0"`
- [x] `CHANGELOG.md` `[1.1.0]` section added above `[1.0.3]`
- [x] `docs/status.md` Repository target version → `1.1.0`
- [x] All `DOCS_WITH_VERSION` files mention `1.1.0`
- [x] `tests/test_release_readiness.py` updated to expect `"1.1.0"`
- [x] `docs/release/release_candidate_handoff_v1.1.0.md` (this file) exists
- [x] `docs/release/smoke_verification_v1.1.0.md` exists (pending state)
- [ ] CI green on `main` (`pytest tests/ -v -m "not slow"`)
- [ ] Golden files regenerated after version bump
- [ ] TestPyPI publish and smoke
- [ ] PyPI publish
- [ ] Post-publish smoke (`scripts/release_smoke.py --check-entrypoints`)
