# Release Candidate Operator Handoff for v1.1.1

Purpose: give the maintainer a compact, maintainer-focused pre-publish handoff bundle for
release candidate `1.1.1` without overstating publication status.

> ⚠️ **PRE-PUBLISH PLACEHOLDER — this is not publication evidence.**

## 1. Machine-verified facts already fixed in-repo

- Repository target version is `1.1.1`.
- Latest public PyPI evidence points to `1.0.3` via `docs/release/pypi_publication_v1.0.3.md` (published 2026-03-22).
- `pyproject.toml` reads package version dynamically from `src/po_core/__init__.py`.
- Release readiness guardrails exist in `tests/test_release_readiness.py`.
- `docs/status.md` explicitly separates pre-publish candidate truth from post-publish evidence truth.
- `docs/release/smoke_verification_v1.1.1.md` is intentionally a pending placeholder, not publish evidence.

## 2. What v1.1.1 adds over v1.1.0

- fix(schemas): import `Traversable` from `importlib.resources.abc` instead of the deprecated
  `importlib.abc` path (PR #553). Prevents `ImportError` on Python 3.14.
- Acceptance golden files updated for AT-001/007/008/009/011 after philosopher roster expansion (PR #552).
- All changes are backward-compatible.

## 3. Why v1.1.0 was not published to PyPI

`1.1.0` was published to TestPyPI (SHA `c94a390`, 2026-04-30) but NOT to PyPI production.
The `c94a390` wheel contains `from importlib.abc import Traversable` which is removed in Python 3.14.
Since `requires-python = ">=3.10"` does not exclude Python 3.14 installs, publishing that wheel
would cause `ImportError` for Python 3.14 users. `1.1.1` from current `main` (`e590752`)
includes the fix and is the correct production publish target. See `docs/release/release_decision_v1.1.0.md`.

## 4. Pre-publish checklist

- [x] `src/po_core/__init__.py` `__version__` = `"1.1.1"`
- [x] `CHANGELOG.md` `[1.1.1]` section added above `[1.1.0]`
- [x] `docs/status.md` Repository target version → `1.1.1`
- [x] All `DOCS_WITH_VERSION` files mention `1.1.1`
- [x] `tests/test_release_readiness.py` version assertion updated to `"1.1.1"`
- [x] `docs/release/release_candidate_handoff_v1.1.1.md` (this file) exists
- [x] `docs/release/smoke_verification_v1.1.1.md` exists (pending state)
- [ ] TestPyPI publish (`workflow_dispatch target=testpypi` from current `main`)
- [ ] PyPI publish (same-SHA as TestPyPI, via GitHub Release trigger or `workflow_dispatch target=pypi`)
- [ ] Post-publish smoke (`scripts/release_smoke.py --check-entrypoints` in clean venv)
