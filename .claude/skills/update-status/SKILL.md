---
name: update-status
description: Update docs/status.md after completing work on Po_core, as mandated by docs/厳格固定ルール.md. Use at the end of any task that changes code, docs, config, or release state. This is a required project ritual, not optional.
---

# Update status.md

`docs/厳格固定ルール.md` (the single source of truth) mandates: after any work,
record **what moved in Next/Completed** in `docs/status.md`. Skipping this
violates the project's multi-agent operating rule.

## Steps

1. **Read** `docs/status.md` first — it is the release-facing SSOT. Note its
   current structure (Current Release State, Runtime Acceptance Status,
   completion matrix totals, etc.).

2. **Identify what changed** in this session: code, tests, ADRs, golden files,
   config_version, version numbers, release evidence.

3. **Edit the matching section** of `docs/status.md`:
   - Move/append the relevant item under the right heading.
   - If you changed acceptance/runtime test outcomes, update the totals line
     (e.g. "completion_matrix.md totals: N pass / N fail").
   - If you changed the package version, keep `src/po_core/__init__.py`
     `__version__` (the version SSOT) and status.md consistent.
   - Keep claims inside the evidence boundary — only assert release facts that
     a file in `docs/release/` actually supports.

4. **Respect the canonical wording**: roster is "42 philosophers" (the `dummy`
   sentinel is never counted); Po_core is decision-support, not a truth oracle.

5. **Keep it factual and dated**. Add a date stamp consistent with existing
   entries. Do not inflate status (no "DONE" without test/evidence).

6. If you also touched `docs/厳格固定ルール.md`, that file's 変更統制 rule
   additionally requires a CHANGELOG.md entry.
