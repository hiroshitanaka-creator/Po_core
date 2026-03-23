# Evaluation Summary — EXPLORATORY DRAFT

> **STATUS: stub/live mixed exploratory artifacts; not publication evidence.**
> M2/M4 use StubComposer(seed=42) — deterministic, not evidence of live reproducibility.
> M3 C-SINGLE is hardcoded 0% by definition, not measured.
> M1 delta measures multi-philosopher field presence (self-fulfilling).
> These artifacts require methodological review before any public claim.

> Generated: 2026-03-23T08:39:36Z
> Prompts: P01-P20 | Reproducibility runs: 5
> Research question: Does Po_core's ethics-constrained multi-perspective deliberation
> produce more reproducible, auditable, and transparent traces than single-responder?

---

## Primary metrics

| Metric | Result | Threshold | Status |
|--------|--------|-----------|--------|
| M1 Trace completeness delta | 100.00% (full) vs 84.21% (single) → delta=+15.79% | delta ≥ +0.10 | PASS ✓ |
| M2 Reproducibility rate | 100.00% (20/20 prompts) | ≥ 90% | PASS ✓ |
| M3 Suppression rate (full) | 100.00% (full) vs 0.00% (single) | full ≥ 95% | PASS ✓ |

## Supporting metric

| Metric | Result | Threshold | Status |
|--------|--------|-----------|--------|
| M4 Disagreement visibility | 95.00% (19/20 prompts) | ≥ 70% | PASS ✓ |

---

## Falsification check

F1: Not triggered (delta=+15.79%)

F2: Not triggered (rate=100.00%)

F3: Not triggered

---

## Overall result: **ALL PRIMARY METRICS PASS**

---

## Result files

| File | Metric | Condition |
|------|--------|-----------|
| `m1_completeness_full.json` | M1 | C-FULL |
| `m1_completeness_single_responder.json` | M1 | C-SINGLE |
| `m2_reproducibility.json` | M2 | C-FULL |
| `m3_suppression_full.json` | M3 | C-FULL |
| `m3_suppression_single_responder.json` | M3 | C-SINGLE |
| `m4_disagreement.json` | M4 | C-FULL |

_See evaluation_plan.md for metric definitions and falsification criteria._
