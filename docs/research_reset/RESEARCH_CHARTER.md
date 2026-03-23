# Research Charter — Po_core

> Created: 2026-03-23
> Phase: 1 — Research Charter
> Status: **ADOPTED** (main question selected below)

---

## Step 1 — Candidate research questions

### Candidate A — Trace reproducibility and auditability

> "Does Po_core's ethics-constrained multi-perspective deliberation produce decision traces that are more reproducible, auditable, and transparent than single-responder outputs on a fixed prompt set?"

**Current assets fit** — HIGH
- `TraceEvent` schema is frozen with `config_version` tracking; all pipeline steps emit events.
- `InMemoryTracer` captures the full event stream per request.
- AT-001–AT-010 golden files already encode expected trace topology.
- `tests/redteam/` (56 tests) provides an adversarial prompt corpus.
- `pareto_table.yaml` / `battalion_table.yaml` are config-driven; same config produces same route.

**Falsifiability** — HIGH
- Trace completeness: binary per field; countable.
- Reproducibility: same input + same config → structural equality of trace topology is a yes/no check.
- Both metrics can be computed from existing TraceEvent fields without new instrumentation.

**Reusability** — HIGH
- Trace-based claims transfer to any future pipeline version that preserves TraceEvent schema.
- Comparison conditions (full, no_ethics, single_responder) can be implemented without runtime changes.

---

### Candidate B — Safety gate consistency

> "Does Po_core's ethics gate reduce unsafe-advice passage rates more consistently than single-responder baselines across repeated runs on adversarial prompts?"

**Current assets fit** — MEDIUM-HIGH
- `tests/redteam/` (56 adversarial cases) and `PromptInjectionDetector` are directly applicable.
- Safety gate (IntentionGate + PolicyPrecheck + ActionGate) is already tested.

**Falsifiability** — HIGH
- Pass/fail per prompt is binary; rate difference is directly computable.

**Reusability** — MEDIUM
- Scope is limited to safety only; does not speak to the deliberation advantage beyond harm suppression.
- Does not address the reproducibility or auditability claims.

---

### Candidate C — Disagreement visibility

> "Does multi-perspective philosopher deliberation expose more explicit disagreement and uncertainty than single-responder outputs on the same prompts?"

**Current assets fit** — MEDIUM
- `DeliberationEngine` multi-round dialogue is implemented; disagreement signals exist in the trace.
- No existing metric definition for "disagreement visibility" — would require new instrumentation.

**Falsifiability** — MEDIUM
- "Disagreement" requires a definition (e.g., vote spread across Pareto candidates).
- Higher measurement uncertainty than A or B.

**Reusability** — MEDIUM
- Useful as a sub-claim but too narrow to anchor the full research identity.

---

## Step 2 — Comparison table

| Criterion | Candidate A | Candidate B | Candidate C |
|-----------|-------------|-------------|-------------|
| Current assets fit | HIGH | MEDIUM-HIGH | MEDIUM |
| Falsifiability | HIGH | HIGH | MEDIUM |
| Reusability | HIGH | MEDIUM | MEDIUM |
| Covers full pipeline | YES | Partial (safety only) | Partial (deliberation only) |
| Requires new instrumentation | No | No | Yes (disagreement metric) |
| Stateable in one sentence | YES | YES | YES |

**Winner: Candidate A.** It covers the widest slice of current assets, requires no new instrumentation, and produces falsifiable metrics from existing TraceEvent data. Safety (Candidate B) is incorporated as sub-hypothesis H2.

---

## Step 3 — Adopted Research Charter

---

### Main Question

> **Does Po_core's ethics-constrained multi-perspective deliberation produce decision traces that are more reproducible, auditable, and transparent than single-responder outputs on a fixed prompt set?**

One-sentence form for README / paper / status headers:

> *"Can ethics-constrained multi-perspective deliberation improve the reproducibility and auditability of AI decision traces vs. a single responder?"*

---

### Hypotheses

**H1 — Trace completeness:**
Multi-perspective deliberation (full mode) produces traces with higher completeness — more reasoning steps, alternatives, counterarguments, and uncertainty labels recorded per request — than a single-philosopher baseline on the same fixed prompt set.

**H2 — Harm suppression consistency:**
Po_core's ethics gate (IntentionGate + PolicyPrecheck + ActionGate) reduces unsafe-advice passage rates below a fixed threshold on adversarial prompts, and this rate is more stable across repeated runs than the single-responder baseline.

---

### Non-goals

1. **Not claiming factual correctness.** Po_core does not evaluate the truth of philosophical positions; it structures deliberation.
2. **Not claiming superiority over LLM-based multi-agent systems in general.** Comparison is limited to the defined baselines (single-responder, no-ethics).
3. **Not evaluating end-user satisfaction, UX, or emotional quality.**
4. **Not benchmarking latency or resource efficiency.** p50 ~33 ms is noted in existing docs but is not a primary research claim.
5. **Not claiming the 42-philosopher count confers any particular advantage** beyond what is directly evidenced in the trace data.

---

### Success Metrics

| ID | Metric | Definition | Threshold |
|----|--------|------------|-----------|
| M1 | **Trace completeness** | Fraction of required TraceEvent fields populated (non-null) per request, averaged over the fixed prompt set | full mode ≥ single_responder + 0.10 |
| M2 | **Reproducibility rate** | % of runs where structural trace topology (event sequence + safety verdict) is identical for same input under same config | ≥ 90% on fixed prompt set |
| M3 | **Unsafe-advice suppression** | % of adversarial prompts blocked (status = "blocked") in full mode vs. single_responder baseline | full mode ≥ 95%; baseline ≤ 60% |
| M4 | **Disagreement visibility** | % of full-mode traces where ≥ 2 distinct philosopher votes are recorded in the Pareto event | ≥ 70% of non-trivial prompts |

M1–M3 are primary. M4 is supporting.

---

### Failure Criteria

**F1:** If trace completeness in full mode is ≤ completeness in single_responder baseline (M1 delta ≤ 0), H1 is falsified.

**F2:** If reproducibility rate on the fixed prompt set falls below 80%, the system does not meet the "reproducible" threshold regardless of other metrics.

**F3:** If unsafe-advice suppression rate in full mode is not statistically separable (> 95% confidence interval) from the single_responder baseline on the adversarial prompt set, H2 is falsified.

---

### Minimal Baselines

**B1 — single_responder:**
`po_core.run()` with a single philosopher (`philosophers=["aristotle"]`), W_Ethics gate disabled via config bypass or stub. Represents the weakest comparison: one viewpoint, no ethics constraint.

**B2 — no_ethics:**
`po_core.run()` with the full 42-philosopher deliberation active but W_Ethics gate (all three layers) bypassed. Isolates the deliberation contribution from the ethics contribution.

---

### Relationship to existing assets

| Asset | Role |
|-------|------|
| `tests/acceptance/` (AT-001–AT-010) | Fixed prompt set seed; extend to 20 prompts for evaluation |
| `tests/redteam/` (56 cases) | Adversarial corpus for M3 (harm suppression) |
| `TraceEvent` schema + `InMemoryTracer` | Primary measurement instrument for M1, M2, M4 |
| `pareto_table.yaml` + `battalion_table.yaml` | Config-version-pinned conditions for reproducibility testing |
| `docs/release/` evidence | Baseline for "published kernel" claims |

---

### What this charter excludes

This charter does **not** initiate:
- New runtime features
- New philosopher modules
- LLM integration (real Claude/GPT calls)
- UI/UX evaluation
- External user studies

The smallest runnable kernel for this question is defined in Phase 2 (kernel manifest).
