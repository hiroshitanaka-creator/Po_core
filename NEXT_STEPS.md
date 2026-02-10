# Next Steps — Phase 1–5 Roadmap

> Updated: 2026-02-10
> See [PHASE_PLAN_v2.md](./PHASE_PLAN_v2.md) for full rationale.
> See [ISSUES.md](./ISSUES.md) for GitHub Issue templates.

---

## Completed (Phase 0–4, Foundation)

### Phase 0: PhilosopherBridge (Blocker Removal)
- `PhilosopherBridge` adapter: wraps legacy `Philosopher.reason()` → `PhilosopherProtocol.propose()`
- Auto-bridge in `registry.py`: all 39 philosophers now work with `run_turn`
- 19 bridge tests

### Phase 1: E2E Test Foundation
- 37 E2E tests for `run_turn` pipeline
- Covers: happy path, safety mode transitions, degradation, blocking, red-team, trace contract
- `FixedTensorEngine` test utility for controlled freedom_pressure injection

### Phase 2: Pipeline Integration
- `PoSelf.generate()` migrated from `run_ensemble` → `run_turn` internally
- `po_core.run()` added as recommended public API entry point
- `PhilosophicalEnsemble` deprecated with `DeprecationWarning`
- 40 PoSelf tests

### Phase 3: Tensor Deepening
- `metric_freedom_pressure`: real 6D keyword analysis (was stub returning 0.0)
- `metric_semantic_delta`: token-overlap divergence vs memory
- `metric_blocked_tensor`: harm keyword + constraint scoring
- All 3 registered in `TensorEngine` via `wiring.py`
- 29 tensor metric tests

### Phase 4: Production Readiness
- `run_ensemble()` removed. All callers migrated to `po_core.run()` / `PoSelf.generate()`
- CI split: pipeline tests (must-pass) + full suite (best-effort)
- `pytest.mark.pipeline` marker on all 4 test files
- 125+ pipeline tests total

---

## Phase 1 (Next): Resonance Calibration & Foundation Settlement

**Status: ACTIVE**

| # | Task | Issue | Priority |
|---|------|-------|----------|
| 1 | Migrate 197 legacy tests to `run_turn` | ISSUES.md #1 | High |
| 2 | Remove PhilosopherBridge dual interface | ISSUES.md #2 | High |
| 3 | 39-philosopher concurrent operation validation | ISSUES.md #3 | High |
| 4 | Rebalance Freedom Pressure / W_Ethics Gate for 39-person scale | ISSUES.md #4 | Medium |
| 5 | Philosopher semantic uniqueness assessment | ISSUES.md #5 | Medium |

**Exit Criteria:**
- Zero references to `run_ensemble` in tests
- `PhilosopherBridge` deleted
- 39-philosopher NORMAL mode < 5s
- Coverage >= 60%
- No philosopher pair > 0.85 semantic similarity

---

## Phase 2 (Planned): Tensor Intelligence & Emergence Engine

| # | Task | Issue | Priority |
|---|------|-------|----------|
| 6 | Upgrade Semantic Delta to sentence-transformers | ISSUES.md #6 | High |
| 7 | Complete Interaction Tensor implementation | ISSUES.md #7 | High |
| 8 | Build Deliberation Engine (multi-round dialogue) | ISSUES.md #8 | Critical |

**Exit Criteria:**
- Semantic delta uses embedding-based similarity
- Interaction Tensor returns NxN philosopher interference matrix
- Deliberation Engine with `max_rounds` parameter integrated into `run_turn`

---

## Phase 3 (Planned): Observability & Viewer Integration

| # | Task | Issue | Priority |
|---|------|-------|----------|
| 9 | Build Viewer WebUI (Plotly Dash / Streamlit) | ISSUES.md #9 | High |
| 10 | W_Ethics Gate explainability (explanation chain) | ISSUES.md #10 | High |

**Exit Criteria:**
- Browser-based dashboard showing tensors, philosophers, pipeline
- W_Ethics Gate decisions include structured explanation chain

---

## Phase 4 (Planned): Adversarial Hardening

| # | Task | Issue | Priority |
|---|------|-------|----------|
| 11 | Expand red team test suite to 50+ cases | ISSUES.md #11 | High |
| 12 | Prototype LLM-based violation detector | ISSUES.md #12 | Medium |

**Exit Criteria:**
- 50+ red team tests across 5 attack categories
- Defense metrics automated in CI

---

## Phase 5 (Planned): Productization & Delivery

| # | Task | Issue | Priority |
|---|------|-------|----------|
| 13 | Implement FastAPI REST API | ISSUES.md #13 | Critical |
| 14 | Docker containerization | ISSUES.md #14 | High |
| 15 | PyPI package publishing | ISSUES.md #15 | Medium |

**Exit Criteria:**
- REST API with 5+ endpoints, OpenAPI docs
- Docker image published
- PyPI package installable via `pip install po-core`
- Version bumped to `0.2.0-beta`
