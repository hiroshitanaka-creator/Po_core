# Phase 0 — Freeze and Inventory

> Created: 2026-03-23
> Purpose: classify every top-level item and major `docs/` sub-item into
> **current / historical / experimental / redundant**, surface contradictions,
> and propose a move/keep/relabel/archive action for each.
>
> Constraint: no src/ logic changed at this phase. No files moved yet.
> This document is read-only analysis + proposals.

---

## Legend

| Layer | Meaning |
|-------|---------|
| **current** | Active, release-facing, or kernel-critical. Keep and maintain. |
| **historical** | Was true at some past state; no longer reflects the repo's current published facts. Must be clearly labeled. |
| **experimental** | Lab/research artifacts. Not part of the publishable kernel. Allowed to stay in `experiments/` or `docs/experiments/`. |
| **redundant** | Covered by another file; adds confusion without adding information. Archive candidate. |

| Action | Meaning |
|--------|---------|
| **keep** | No change required. |
| **relabel** | Add a historical banner or update stale header text. |
| **move-to-history** | Move to `docs/history/` (plan created in Phase 4). |
| **archive-candidate** | Move to `docs/archive/` or delete after confirming no cross-links. |

---

## Part 1 — Root-level files inventory

| File | Layer | Version / State Referenced | Reader Target | Purpose | Action |
|------|-------|---------------------------|---------------|---------|--------|
| `README.md` | current | 1.0.3, beta | general / external | Project overview, install, API reference | keep |
| `QUICKSTART.md` | current | 1.0.3 | JA developer | Step-by-step JA quickstart | keep |
| `QUICKSTART_EN.md` | current | 1.0.3 | EN developer | Step-by-step EN quickstart | keep |
| `CLAUDE.md` | current | 1.0.3 | AI coding agents | Per-session context, conventions, current phase | keep |
| `CHANGELOG.md` | current | 1.0.3 | developers / release | Version history | keep |
| `REPOSITORY_STRUCTURE.md` | current | 1.0.3 | maintainers / release | Actual repo layout and release-critical files | keep |
| `pyproject.toml` | current | 1.0.3 | packaging / CI | Package metadata and tooling config | keep |
| `pytest.ini` | current | — | CI / developers | Test markers and default pytest config | keep |
| `Makefile` | current | — | developers | Convenience targets | keep |
| `requirements.txt` | current | — | developers (checkout) | Repo-local editable install wrapper | keep |
| `requirements-dev.txt` | current | — | developers (checkout) | Repo-local dev install wrapper | keep |
| `.env.example` | current | — | operators | Reference env var config | keep |
| `Dockerfile` / `docker-compose.yml` | current | — | operators | Container deployment | keep |
| `CONTRIBUTING.md` | current | — | contributors | Contribution guidelines | keep |
| `CODE_OF_CONDUCT.md` | current | — | contributors | Community norms | keep |
| `LICENSE` / `COMMERCIAL_LICENSE.md` | current | — | users / legal | Licensing terms | keep |
| `AGENTS.md` | current | — | AI coding agents | Agent operation rules (supplements CLAUDE.md) | keep |
| `ISSUES.md` | supporting | — | maintainers | GitHub issue templates | keep |
| `Po_core_Manifesto_When_Pigs_Fly.md` | supporting | — | general | Mission and philosophy narrative | keep |
| `ROADMAP_FINAL_FORM.md` | historical | v0.2.0b3 → v1.0.0 | internal planning | Original 5-stage roadmap with milestone detail | relabel (add historical banner; referenced in CLAUDE.md) |
| `NEXT_STEPS.md` | **historical** | v0.2.0b3, PyPI pending | stakeholders | Phase 1–7 completion summary + remaining tasks | relabel → move-to-history |
| `PHASE_PLAN_v2.md` | **historical** | v0.2.0b3, 39-philosopher refs | architects | Detailed phase matrix including "AI vendor slots" plan (superseded by ADR-0006) | relabel → move-to-history |
| `PHASE_PLAN_tournament.md` | historical | pre-v1.0 | internal | Tournament-style phase planning artifact | archive-candidate |
| `GRAND_ARCHITECT_ASSESSMENT.md` | historical | v0.2.0-beta | internal | Pre-v1.0 architectural review | archive-candidate |
| `PROJECT_SUMMARY.md` | **redundant** | 2025-02-05 (very stale) | GitHub readers | Progress snapshot; outdated and superseded by README + status.md | archive-candidate |
| `Po_core_spec_doc_v1.0.md` | historical | v1.0 spec | internal | Combined spec document; contents covered by `docs/spec/` | archive-candidate |
| `regenerate_golden.py` | supporting | — | developers | Script to regenerate golden test fixtures | keep |

---

## Part 2 — `docs/` sub-directory inventory

| Path | Layer | Version / State | Purpose | Action |
|------|-------|-----------------|---------|--------|
| `docs/status.md` | **current** | 1.0.3 published | Release SSOT | keep |
| `docs/厳格固定ルール.md` | current | — | Strict single-truth rules | keep |
| `docs/adr/` (0001–0010) | current | — | Architecture Decision Records | keep |
| `docs/spec/` | current | M1–M4 complete | PRD, SRS, schema, test cases, traceability | keep |
| `docs/release/` | current | 1.0.3 evidence | PyPI/TestPyPI publication evidence, smoke verification | keep |
| `docs/operations/publish_playbook.md` | current | 1.0.3 | Release runbook | keep |
| `docs/traceability/` | current | — | Traceability matrix | keep |
| `docs/viewer/` | supporting | — | WebUI viewer docs | keep |
| `docs/SAFETY.md` | supporting | — | W-Ethics gate system docs | keep |
| `docs/TUTORIAL.md` | supporting | — | Getting-started guide | keep |
| `docs/VISUALIZATION_GUIDE.md` | supporting | — | Tension maps / pressure display docs | keep |
| `docs/CONTRIBUTING_PHILOSOPHER.md` | supporting | — | Philosopher contribution guide | keep |
| `docs/LOCAL_LLM_GUIDE.md` | supporting | — | Local LLM usage guide | keep |
| `docs/MANUAL_LLM_TESTING.md` | supporting | — | Manual LLM testing guide | keep |
| `docs/philosopher_prompt_drafts/` | supporting | — | Non-runtime draft prompt assets | keep (draft, not runtime) |
| `docs/community/` | supporting | — | Community docs | keep |
| `docs/paper/paper.md` | **historical** | v0.3.0 (2026-03) | academic | Research paper with v0.3 benchmarks; not aligned to 1.0.3 kernel | relabel |
| `docs/paper/paper_next.docs` | experimental | — | academic drafts | Draft notes for next paper version | relabel |
| `docs/paper/benchmarks/` | experimental | — | benchmark results | Raw benchmark data | relabel |
| `docs/paper/experiments/` | experimental | — | experiment docs | Experiment documentation | relabel |
| `docs/papers/` | historical | pre-v1.0 | academic | Solar Will papers; not directly tied to current main research question | archive-candidate |
| `docs/archive/` | historical | various | internal | Already-archived items | keep-in-archive |
| `docs/experiments/` | experimental | — | developers | Experiment documentation | keep-as-lab |
| `docs/plan/` | historical | pre-v1.0 | internal | Historical planning docs | archive-candidate |
| `docs/results/` | experimental | — | research | Evaluation result artifacts | keep-as-lab |
| `docs/release.md` | redundant | — | ? | Appears to duplicate `docs/release/` evidence; check for content | archive-candidate |
| `docs/calibration_axis_scoring.md` | experimental | — | research | Calibration axis scoring spec | keep-as-lab |
| `docs/decision_axis_spec.md` | experimental | — | research | Decision axis specification | keep-as-lab |
| `docs/philosopher_plugin_spec.md` | supporting | — | developers | Philosopher plugin specification | keep |

---

## Part 3 — Top-level research/experiment directories

| Path | Layer | Purpose | Action |
|------|-------|---------|--------|
| `src/` | **current** (kernel) | Runtime Python packages | keep |
| `tests/` | **current** (kernel) | Full test suite | keep |
| `scripts/` | current | Release, export, maintenance scripts | keep |
| `tools/` | current | Repo maintenance tooling | keep |
| `clients/` | current | Generated TypeScript SDK | keep |
| `examples/` | supporting | Usage examples | keep |
| `scenarios/` | current | Golden-contract scenario inputs/outputs | keep |
| `experiments/` | **experimental** (lab) | Non-runtime experimental code and prompt tests | keep-as-lab |
| `papers/` | historical | Academic paper drafts (Po_core Academia Paper, Solar Will) | archive-candidate |
| `reports/` | experimental | Experimental lab reports | keep-as-lab |
| `sessions/` | supporting | Acceptance test session fixtures | keep |
| `calibration/` | experimental | Calibration experiments | keep-as-lab |
| `audit/` | current | Audit reports (phase_g_closure, finding_resolution) | keep |
| `01_specifications/` | historical | 120+ technical spec docs (pre-M0) | archive-candidate |
| `02_architecture/` | supporting | System design documents | keep |
| `03_api/` | supporting | API design docs | keep |
| `04_modules/` | supporting | Component documentation | keep |
| `05_research/` | historical / experimental | Academic papers and analysis | relabel |

---

## Part 4 — Contradiction table

| # | Contradiction | Location A | Location B | Severity |
|---|---------------|-----------|-----------|---------|
| C-01 | Version: `NEXT_STEPS.md` says `v0.2.0b3` / "PyPI pending"; repo is at `1.0.3` published | `NEXT_STEPS.md` line 8 | `docs/status.md` | **HIGH** — stale document reads as current state |
| C-02 | Version: `PHASE_PLAN_v2.md` says `v0.2.0b3` as "現在地"; roadmap shows "5-F: PyPI publish pending" | `PHASE_PLAN_v2.md` header | `docs/status.md` | **HIGH** — stale roadmap reads as live plan |
| C-03 | Philosopher count: `PHASE_PLAN_v2.md` still describes Phase 7 as "AI vendor slots (Claude/GPT/Gemini/Grok)" (superseded by ADR-0006) | `PHASE_PLAN_v2.md` | `docs/adr/` ADR-0006, `CLAUDE.md` | **HIGH** — contradicts published architecture |
| C-04 | Paper version: `docs/paper/paper.md` references `v0.3.0` benchmark data (e.g. `po-core-flyingpig v0.3`); repo is `1.0.3` | `docs/paper/paper.md` header | `src/po_core/__init__.py` | **MEDIUM** — paper not pinned to any release branch |
| C-05 | `PROJECT_SUMMARY.md` date 2025-02-05 with very old state; no update path visible | `PROJECT_SUMMARY.md` | `README.md`, `docs/status.md` | **MEDIUM** — creates confusion about repo history |
| C-06 | `GRAND_ARCHITECT_ASSESSMENT.md` targets `v0.2.0-beta → v1.0.0-final` as future state; v1.0.0 is already complete | `GRAND_ARCHITECT_ASSESSMENT.md` | `docs/status.md` | **MEDIUM** — historical plan reads as pending work |
| C-07 | `docs/papers/` Solar Will papers describe pre-v1.0 experimental claims with no stated relationship to current kernel | `docs/papers/` | `src/po_core/autonomy/` | **LOW** — scope unclear; not directly contradictory |
| C-08 | `ROADMAP_FINAL_FORM.md` milestones include "5-F: PyPI publish pending" — this is complete | `ROADMAP_FINAL_FORM.md` | `docs/status.md` | **MEDIUM** — referenced from CLAUDE.md, stale milestone state |

---

## Part 5 — Summary: move/keep proposal

### Keep as-is (current, no action needed)

```
README.md, QUICKSTART.md, QUICKSTART_EN.md, CLAUDE.md, CHANGELOG.md,
REPOSITORY_STRUCTURE.md, pyproject.toml, pytest.ini, Makefile,
requirements.txt, requirements-dev.txt, .env.example, Dockerfile,
docker-compose.yml, CONTRIBUTING.md, CODE_OF_CONDUCT.md, LICENSE,
COMMERCIAL_LICENSE.md, AGENTS.md, ISSUES.md,
Po_core_Manifesto_When_Pigs_Fly.md, regenerate_golden.py,
docs/status.md, docs/厳格固定ルール.md, docs/adr/, docs/spec/,
docs/release/, docs/operations/, docs/traceability/, docs/viewer/,
docs/SAFETY.md, docs/TUTORIAL.md, docs/VISUALIZATION_GUIDE.md,
docs/community/, docs/archive/, docs/philosopher_prompt_drafts/,
docs/philosopher_plugin_spec.md, src/, tests/, scripts/, tools/,
clients/, examples/, scenarios/, sessions/, audit/,
02_architecture/, 03_api/, 04_modules/
```

### Relabel (add historical banner, update stale header)

```
NEXT_STEPS.md              → add "[HISTORICAL]" banner; target: move-to-history in Phase 4
PHASE_PLAN_v2.md           → add "[HISTORICAL]" banner; target: move-to-history in Phase 4
ROADMAP_FINAL_FORM.md      → add "[HISTORICAL — milestones superseded]" banner
GRAND_ARCHITECT_ASSESSMENT.md → add "[HISTORICAL]" banner
docs/paper/paper.md        → add "[HISTORICAL — v0.3.0 benchmark; not pinned to 1.0.x]" banner
docs/paper/paper_next.docs → add "[DRAFT / LAB]" banner
05_research/               → add "[HISTORICAL / EXPERIMENTAL]" banner in index
```

### Archive candidate (move to `docs/history/` or `docs/archive/` in Phase 4)

```
PHASE_PLAN_tournament.md
PROJECT_SUMMARY.md
Po_core_spec_doc_v1.0.md
docs/papers/               (Solar Will pre-v1.0 papers)
docs/plan/                 (historical planning docs)
docs/release.md            (check for duplicated content first)
01_specifications/         (120+ pre-M0 spec docs; large; check for cross-links)
papers/                    (root-level academic drafts)
```

### Keep as lab / experimental (no promotion to current layer)

```
experiments/               (non-runtime code; stays in lab)
reports/                   (lab reports)
calibration/               (calibration experiments)
docs/experiments/          (experiment docs)
docs/results/              (evaluation data)
docs/calibration_axis_scoring.md
docs/decision_axis_spec.md
docs/paper/benchmarks/
docs/paper/experiments/
```

---

## Part 6 — Recommended Phase 4 action sequence

1. Create `docs/history/index.md` listing all items proposed for `move-to-history`.
2. Add `[HISTORICAL]` banners to `NEXT_STEPS.md`, `PHASE_PLAN_v2.md`, `ROADMAP_FINAL_FORM.md`, `GRAND_ARCHITECT_ASSESSMENT.md` (Phase 4 task — do NOT move yet to avoid link breakage).
3. Add version pin note to `docs/paper/paper.md` ("v0.3.0 benchmark data; not updated for 1.x series").
4. Verify no CI/build steps reference `01_specifications/` before archiving.
5. Verify `docs/release.md` content; merge into `docs/release/` or delete.
6. Add `[HISTORICAL]` banner to `PROJECT_SUMMARY.md`.
7. After banners are stable (≥1 sprint), move to `docs/history/` with redirect comments.

---

*This inventory is a snapshot as of 2026-03-23. It is read-only analysis; no files have been moved or modified by this document.*
