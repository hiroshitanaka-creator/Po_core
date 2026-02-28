# Outreach Issues — Good First Issues Designed to Attract Expert Contributors

> **戦略ノート:** Good First Issue ラベルは、GitHub Explore の
> 「発見エンジン」として機能します。熟練開発者はこのラベルを使って
> 「このプロジェクトは本当に設計されているか？」を素早く査定します。
> 以下の各 Issue は **入門者には入りやすく、玄人には刺さる** 構造で設計されています。

---

## OUTREACH-01: [good first issue] Explain why Nietzsche scores 0.95 on freedom_pressure but Kant scores 0.12

**Labels:** `good first issue`, `documentation`, `philosophy`, `ml`
**Assignee:** _unassigned_

```markdown
## Task

Po_core represents each philosopher as a **6-dimensional ML tensor**:

```
[freedom_pressure, semantic_delta, blocked_tensor,
 collective_harmony, temporal_depth, epistemic_humility]
```

From `src/po_core/philosophers/manifest.py`:

| Philosopher | freedom | harmony | temporal | epistemic |
|-------------|---------|---------|----------|-----------|
| Nietzsche   | 0.95    | 0.15    | 0.70     | 0.40      |
| Kant        | 0.12    | 0.85    | 0.90     | 0.95      |
| Confucius   | 0.25    | 0.95    | 0.80     | 0.80      |
| Sartre      | 0.92    | 0.20    | 0.60     | 0.35      |

**The task:** Write a short explanation (in `docs/philosophy/tensor_weights_rationale.md`)
for *why* these weights make philosophical sense. Use quotes from primary texts.

### What you'll learn

- How philosophy maps to numerical representations
- Po_core's 10-step hexagonal pipeline (`src/po_core/ensemble.py`)
- How tensor weights influence Pareto aggregation (`src/po_core/aggregator/pareto.py`)

### Relevant files

- `src/po_core/philosophers/manifest.py` — all 43 philosopher weights
- `src/po_core/tensors/freedom_pressure_v2.py` — 6D tensor engine
- `src/po_core/tensors/engine.py` — MetricFn registry

### Stretch goal (for ML folks)

Are the weight assignments Pareto-optimal? Could you cluster the 43
philosophers by tensor distance and see if traditions cluster naturally?
(`src/po_core/tensors/interaction_tensor.py` has a NxN harmony matrix)

---
No coding required for the basic task. Philosophy + curiosity = enough.
```

---

## OUTREACH-02: [good first issue] Add pytest fixtures for W_Ethics Gate layers W0–W4

**Labels:** `good first issue`, `tests`, `safety`

```markdown
## Task

The W_Ethics Gate (`src/po_core/safety/wethics_gate/gate.py`) filters
philosopher outputs through **5 cascading safety layers**:

```
W0: catastrophic harm check       (immediate block)
W1: structural exclusion          (prompt injection, jailbreak)
W2: semantic drift detection      (goal misalignment)
W3: dependency disguise           (help patterns masking harm)
W4: epistemic coercion            (false certainty, manipulation)
```

We need **shared pytest fixtures** in `tests/fixtures/wethics_fixtures.py`
so test authors don't copy-paste safety verdicts across 50+ test files.

### The task

1. Read `src/po_core/safety/wethics_gate/gate.py` and `tests/redteam/`
2. Create `tests/fixtures/wethics_fixtures.py` with:
   - `clean_verdict` fixture — a passing SafetyVerdict
   - `w1_blocked_verdict` fixture — a W1 (injection) block
   - `w4_blocked_verdict` fixture — a W4 (epistemic coercion) block
   - `sample_context(input_text)` factory fixture
3. Update `tests/conftest.py` to import them

### Why this matters

100% of our red-team tests (prompt injection, jailbreak, goal misalignment)
depend on correct SafetyVerdict construction. Clean fixtures make new
adversarial test cases trivial to add.

### Relevant files

- `src/po_core/safety/wethics_gate/gate.py`
- `src/po_core/domain/safety_verdict.py`
- `tests/redteam/test_prompt_injection.py` (for reference)
- `tests/conftest.py`

### Stretch goal

Add a `@pytest.mark.parametrize` version that tests all 5 W-layers in one shot.
```

---

## OUTREACH-03: [good first issue] Add philosopher #44: Ibn Khaldun — Social Cohesion & Civilizational Cycles

**Labels:** `good first issue`, `bridge`, `philosophy`, `enhancement`

```markdown
## Task

Po_core has 43 philosopher AI personas. Slot #44 is open.

**Proposal: Ibn Khaldun** (1332–1406)
- Founder of sociology and historiography
- Core concept: **`asabiyyah`** — social cohesion, group solidarity
- Insight: civilizations rise through solidarity, fall through luxury and fragmentation
- Relevance to AI ethics: collective decision-making, social trust, epistemic communities

### Why Ibn Khaldun?

Po_core is missing a philosopher who explicitly theorizes **group dynamics and
systemic trust**. Ibn Khaldun's _Muqaddimah_ provides a rigorous framework
for how collectives reason — directly relevant to multi-philosopher deliberation.

### The task (two paths)

**Philosophy track (no coding):**
1. Propose tensor weights for Ibn Khaldun's 6 dimensions
2. Write 3 `generate()` response examples for sample ethical dilemmas
3. Comment below — we'll implement it

**Bridge track (Python + philosophy):**
1. Copy `src/po_core/philosophers/aristotle.py` as template
2. Implement `IbnKhaldun` class with `asabiyyah`-informed `generate()`
3. Add to `src/po_core/philosophers/manifest.py`
4. Write 3 unit tests in `tests/unit/test_philosophers/test_ibn_khaldun.py`

### Tensor weight hints

```python
# Your task: justify these (or propose better values)
tensor_weights = {
    "freedom_pressure": 0.35,      # Individual vs. collective tension
    "collective_harmony": 0.90,    # asabiyyah = solidarity
    "temporal_depth": 0.95,        # Civilizational time horizon
    "epistemic_humility": 0.75,    # Empirical historiography
    "blocked_tensor": 0.20,        # Open to challenge
    "semantic_delta": 0.60,        # Dynamic adaptation
}
```

### Relevant files

- `src/po_core/philosophers/aristotle.py` — template
- `src/po_core/philosophers/manifest.py` — philosopher registry
- `src/po_core/domain/proposal.py` — Proposal type
```

---

## OUTREACH-04: [good first issue] Add a deliberation quality chart to PoViewer WebUI

**Labels:** `good first issue`, `ai-easy`, `visualization`, `enhancement`

```markdown
## Task

The Po_core WebUI (`src/po_core/viewer/web/app.py`) has a 4-tab Dash layout.
The Deliberation tab currently shows round-by-round philosopher contributions,
but is missing a **consensus trajectory chart** — how much do philosophers
agree after each deliberation round?

### What to build

Add one new Plotly chart to `src/po_core/viewer/web/figures.py`:

```python
def build_consensus_trajectory_figure(deliberation_events: list[TraceEvent]) -> go.Figure:
    """
    Line chart: X = deliberation round (1..N),
                Y = consensus_score (0.0 to 1.0),
                one line per philosopher cluster.
    Data source: DeliberationCompleted events from InMemoryTracer.
    """
```

### Why this is interesting

The `DeliberationEngine` (`src/po_core/deliberation/engine.py`) runs up to
`Settings.deliberation_max_rounds` rounds. Each round, the `EmergenceDetector`
checks if philosophers have converged. The chart would make this emergence
visible in real time.

### Relevant files

- `src/po_core/viewer/web/figures.py` — existing chart builders
- `src/po_core/viewer/web/app.py` — Dash 4-tab layout
- `src/po_core/deliberation/engine.py` — DeliberationEngine
- `src/po_core/deliberation/emergence.py` — EmergenceDetector
- `src/po_core/trace/in_memory.py` — InMemoryTracer with listener support

### Stretch goal

Wire it to `InMemoryTracer`'s listener mechanism for real-time streaming.
The foundation is already there (`register_listener` / `notify_listeners`).
```

---

## OUTREACH-05: [good first issue] Write acceptance test AT-016: AI governance decision scenario

**Labels:** `good first issue`, `tests`, `ai-easy`, `research`

```markdown
## Task

Po_core's acceptance test suite (`tests/acceptance/`) covers 15 decision
scenarios (AT-001 to AT-015). We need **AT-016: AI Governance**.

### The scenario

```yaml
# tests/acceptance/scenarios/case_016.yaml
id: AT-016
title: "AI Model Deployment Decision"
input: |
  A hospital wants to deploy an AI diagnostic tool that achieves 94% accuracy
  on the training population (predominantly Western European) but only 78%
  on underrepresented groups. Deployment will save an estimated 200 lives/year.
  Should the hospital proceed?
expected:
  status: ok
  must_mention: [fairness, bias, autonomy, transparency]
  philosopher_minimum: 5
  structural_honesty_score: >= 0.7
```

### What to implement

1. Create `tests/acceptance/scenarios/case_016.yaml` with the above
2. Add the test function in `tests/acceptance/test_at016_ai_governance.py`
3. Run it: `pytest tests/acceptance/test_at016_ai_governance.py -v`
4. Document which philosophers surface (which ethical traditions "show up"?)

### Why this matters

AI governance is one of the hardest real-world scenarios for ethical AI.
If Po_core handles it well, it demonstrates production readiness for
high-stakes domains. This test may become a reference in our arXiv paper.

### Relevant files

- `tests/acceptance/` — existing acceptance tests (look at any for structure)
- `src/po_core/app/api.py` — `run()` public API (use this)
- `tests/conftest.py` — shared fixtures
```

---

## OUTREACH-06: [good first issue] Benchmark: how many philosophers can deliberate within 100ms?

**Labels:** `good first issue`, `benchmark`, `performance`, `research`

```markdown
## Task

Po_core's `NORMAL` mode activates all 39 philosophers and achieves ~33ms p50
latency on CPU (`tests/benchmarks/test_pipeline_perf.py`). But:

- What if you use the full 43 (including AI philosopher slots)?
- What's the latency cliff as `deliberation_max_rounds` increases?
- Is there a "sweet spot" between philosopher count and response quality?

### What to build

Add a new parametrized benchmark to `tests/benchmarks/test_deliberation_perf.py`:

```python
@pytest.mark.benchmark
@pytest.mark.parametrize("philosopher_count,max_rounds", [
    (5, 1), (10, 2), (20, 3), (39, 3), (39, 5),
])
def test_deliberation_latency(benchmark, philosopher_count, max_rounds, ...):
    """Measure p50/p95/p99 for varying ensemble sizes."""
```

### What you'll discover

- How `AsyncPartyMachine` parallelizes philosopher calls
  (`src/po_core/party_machine.py`)
- How `DeliberationEngine` adds latency per round
  (`src/po_core/deliberation/engine.py`)
- How `ParetoAggregator` scales with N proposals
  (`src/po_core/aggregator/pareto.py`)

### Relevant files

- `tests/benchmarks/test_pipeline_perf.py` — existing benchmarks (use as template)
- `src/po_core/runtime/settings.py` — `deliberation_max_rounds` setting
- `src/po_core/party_machine.py` — AsyncPartyMachine

### Stretch goal

Plot the latency/quality Pareto frontier (latency vs. number of unique
philosophical perspectives surfaced). This could become a figure in the arXiv paper.

---
Results should be posted as a comment with your hardware specs.
Reproducibility > absolute numbers.
```

---

*File these in order of expected impact: OUTREACH-03 → OUTREACH-01 → OUTREACH-06 → OUTREACH-02 → OUTREACH-04 → OUTREACH-05*

*Cross-reference each issue in the body of the next one to build momentum.*
