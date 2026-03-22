# Release Operator Report — po-core-flyingpig v1.0.3

- Report date: 2026-03-22
- Operator: claude/audit-po-core-v1.0.3-FaZVy (automated session)
- Session: cse_01PQavFeFD3auUcBbZLJH2HU
- Status: **BLOCKED — Type C (Permission/Environment)**

> This document records the Phase 0 preflight analysis and exact blocker
> for the v1.0.3 TestPyPI → PyPI publish sequence.
> Evidence is limited to what was actually observed. No fake URLs or transcripts.

---

## Phase 0: Preflight Summary

### Head SHAs

| Ref | SHA | Status |
|-----|-----|--------|
| origin/main (publish target) | `d1c23faa984753a204b06708acdc189bec40933e` | ✅ version=1.0.3 |
| operator branch (this session) | `69de143cd8107570eb1f5e778e93512303f28e20` | audit branch only |

### Version Check

```
src/po_core/__init__.py on origin/main:
__version__ = "1.0.3"   ✅
```

### Publish Workflow (publish.yml) — Path Summary

```
workflow_dispatch (target=testpypi) from refs/heads/main
  └─ publish-guard          (ref provenance + version check)
  └─ verify-release-blockers (3×2 matrix: py3.10/3.11/3.12 × wheel/sdist)
       └─ import_graph.py --check
       └─ pytest tests/ -v -m "not slow"
       └─ bandit -r src/ scripts/ -c pyproject.toml -ll
       └─ pip-audit (base/llm/docs/viz surfaces)
       └─ python -m build && twine check
       └─ artifact smoke (release_smoke.py --check-entrypoints)
  └─ publish-testpypi       (OIDC → test.pypi.org)

then same-SHA:
workflow_dispatch (target=pypi) from refs/heads/main
  └─ publish-guard          (+ testpypi deployment prerequisite check)
  └─ verify-release-blockers
  └─ publish-pypi           (OIDC → pypi.org)
```

### Local Gate Status (from audit/phase_h_bandit_closure_report.md)

All checks run against origin/main HEAD `d1c23fa` (bandit-fixed commit):

| Gate | Result |
|------|--------|
| `python tools/import_graph.py --check` | violations=0, cycles=0 ✅ |
| `pytest tests/test_release_readiness.py -v` | 24/24 passed ✅ |
| `pytest tests/acceptance/ -v -m acceptance` | 43/43 passed ✅ |
| `pytest tests/ -v -m "not slow"` | 3857/3857 passed, exit=0 ✅ |
| `bandit -r src/ scripts/ -c pyproject.toml -ll` | High=0, exit=0 ✅ |
| `python -m build` | whl + sdist ✅ |
| `twine check dist/*` | PASSED ✅ |
| `python scripts/release_smoke.py --check-entrypoints` | all RC=0 ✅ |

### Recent publish.yml Workflow Runs (from GitHub API, unauthenticated)

| Run ID | SHA | Result | Date | Notes |
|--------|-----|--------|------|-------|
| 23401036147 | `52fe81b` | ❌ failure | 2026-03-22T10:23 | Pre-bandit-fix; GITHUB_TOKEN fix attempt |
| 23400277364 | `6628f85` | ❌ failure | 2026-03-22T09:36 | Pre-fix |
| 23399971865 | `4d4dee7` | ❌ failure | 2026-03-22T09:17 | Pre-fix |
| 23396773635 | `06bbd55` | ❌ failure | 2026-03-22T05:47 | Pre-fix |
| 23396597464 | `e8ffbf2` | ❌ failure | 2026-03-22T05:35 | Pre-fix |
| 23105588872 | `335a530` | ✅ success | 2026-03-15T07:09 | Last known successful run |
| **d1c23fa** | — | **NOT ATTEMPTED** | — | Bandit-fixed HEAD; no publish run yet |

**Key finding:** The bandit-fixed HEAD `d1c23fa` has never had a publish workflow run.
The previous failures were on pre-fix commits. The fix chain (PRs #515→#519) specifically
resolves the blockers that caused those failures:
- #515: pass GITHUB_TOKEN explicitly to publish-guard step
- #516–#518: add missing session_answers_schema_v1.json
- #519: add justified bandit skips so bandit exits 0

---

## Phase 1: TestPyPI Dispatch — BLOCKED

**Blocker classification: Type C — Permission/Environment**

Exact blocker:
- `gh` CLI: **NOT INSTALLED** (`which gh` → not found)
- `GITHUB_TOKEN`: **NOT SET** (env check confirmed)
- `GH_TOKEN`: **NOT SET** (env check confirmed)
- Local proxy `127.0.0.1:35715`: **git-only** (non-`/git/` API paths return "Invalid path format")
- GitHub API (unauthenticated): **rate limit exceeded** after workflow/runs inspection
  (60 req/hour unauthenticated; exhausted during preflight)

**Cannot trigger `workflow_dispatch` without write-access GitHub API token.**

### What is needed (operator action required)

Run from a shell with a valid `GITHUB_TOKEN` (with `actions:write` permission):

```bash
# Option A: via gh CLI (recommended)
gh workflow run publish.yml \
  --repo hiroshitanaka-creator/Po_core \
  --ref main \
  --field target=testpypi

# Option B: via curl
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/hiroshitanaka-creator/Po_core/actions/workflows/235635389/dispatches" \
  -d '{"ref":"main","inputs":{"target":"testpypi"}}'
```

Then monitor:
```bash
gh run list --workflow=publish.yml --repo hiroshitanaka-creator/Po_core --limit 5
gh run watch <run-id> --repo hiroshitanaka-creator/Po_core
```

### Publish workflow ID

- Workflow: **Publish to PyPI**
- Workflow ID: `235635389`
- File: `.github/workflows/publish.yml`
- Workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml

---

## Phase 2: PyPI Dispatch — BLOCKED (prerequisite: Phase 1)

Cannot proceed until Phase 1 (TestPyPI success on `d1c23fa`) is confirmed.

Same-SHA invariant: do not commit to main between TestPyPI success and PyPI dispatch.

PyPI dispatch command (after TestPyPI success on `d1c23fa`):
```bash
gh workflow run publish.yml \
  --repo hiroshitanaka-creator/Po_core \
  --ref main \
  --field target=pypi
```

---

## Phase 3–4: Evidence Recording — PENDING

Post-publish, fill in:
- `docs/release/testpypi_publish_log_v1.0.3.md` (from template)
- `docs/release/pypi_publication_v1.0.3.md`
- `docs/release/smoke_verification_v1.0.3.md` (post-publish section)
- `docs/status.md` (update latest published public version to 1.0.3)

---

## Missing Prerequisites / Secrets Checklist

| Item | Status |
|------|--------|
| GitHub Environment `testpypi` configured | requires GitHub admin to verify |
| GitHub Environment `pypi` configured | requires GitHub admin to verify |
| TestPyPI Trusted Publisher (OIDC) configured for `po-core-flyingpig` | requires TestPyPI admin to verify |
| PyPI Trusted Publisher (OIDC) configured for `po-core-flyingpig` | requires PyPI admin to verify |
| `GITHUB_TOKEN` with `actions:write` available to operator | **NOT PRESENT in this session** |

The last successful publish run was 2026-03-15 on `335a530`, indicating trusted publishing
infrastructure was functional at that time. Assuming it remains active, the primary blocker
is solely the operator-side `GITHUB_TOKEN`.

---

## Next Operator Action

1. **Obtain a GitHub token** with `actions:write` on `hiroshitanaka-creator/Po_core`
2. **Verify current main HEAD** is still `d1c23faa984753a204b06708acdc189bec40933e`
   ```bash
   git ls-remote origin refs/heads/main
   ```
3. **Dispatch TestPyPI run** on main (command in Phase 1 above)
4. **Monitor** until `publish-testpypi` job succeeds
5. **Verify same SHA** is still at origin/main HEAD (no new commits)
6. **Dispatch PyPI run** on same SHA (command in Phase 2 above)
7. **Record evidence** in docs/release/ as described in Phase 3–4

---

## Rule compliance confirmation

- No workflow gates weakened ✅
- No fake evidence written ✅
- No same-SHA invariant broken ✅
- `1.0.3 published` claim NOT made (no publish evidence exists) ✅
- docs/status.md unchanged (still accurately reflects pre-publish state) ✅
