---
name: new-adr
description: Create a new Architectural Decision Record for Po_core with correct numbering, the project's section format, and an updated ADR index. Use when a change alters architecture, contracts, policy thresholds, or responsibility boundaries.
---

# New ADR

Architectural decisions in Po_core are recorded in `docs/adr/` and indexed in
`docs/adr/index.md`. Create an ADR whenever a change touches output/trace
contracts, policy arbitration, rule placement boundaries, the roster, or any
cross-cutting responsibility split.

## Steps

1. **Find the next number**: list `docs/adr/NNNN-*.md` and increment the
   highest (zero-padded 4 digits). Latest existing is `0014`.

2. **Create `docs/adr/NNNN-<kebab-title>.md`** using this exact section
   structure (match existing ADRs like `0013-two-track-plan-v1.md`):

   ```markdown
   # ADR NNNN: <Title>

   **Date:** YYYY-MM-DD
   **Status:** Accepted        # or Proposed
   **Deciders:** Po_core project

   ---

   ## Context
   ## Decision
   ## Rationale
   ## Consequences
   ## Non-Goals
   ```

   Write Context/Decision in the project's bilingual style (Japanese prose is
   the norm here). Be concrete: name the rule_id, trigger conditions, and any
   trace fields affected, as the existing ADRs do.

3. **Update `docs/adr/index.md`**: add a table row
   `| NNNN | <Title> | <Status> | <one-line key point> |` in number order, and
   update the footer note about Proposed/Accepted counts if it changed.

4. **Cross-reference**: if the ADR supersedes/relates to another, say so in
   Context, matching how ADR-0010/0011 reference each other.

5. If the decision changes behavior, pair it with code + tests and (if output
   changes) the `regen-golden` skill.

6. Run the `update-status` skill to record the ADR in `docs/status.md`.

## Non-negotiable

- Do not renumber or rewrite existing Accepted ADRs — add a new one that
  supersedes instead.
- Changes to `docs/厳格固定ルール.md` are special: they require change reason,
  impact, tests run, and a CHANGELOG entry (see that file's 変更統制 section).
