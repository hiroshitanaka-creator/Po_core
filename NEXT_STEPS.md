# Next Steps — Phase 1–5 Roadmap

> Updated: 2026-02-12
> See [PHASE_PLAN_v2.md](./PHASE_PLAN_v2.md) for full rationale.
> See [ISSUES.md](./ISSUES.md) for GitHub Issue templates.

---

## Completed (Foundation + Phase 1)

### Foundation Phase 0: PhilosopherBridge (Blocker Removal)

- `PhilosopherBridge` adapter: wraps legacy `Philosopher.reason()` → `PhilosopherProtocol.propose()`
- Auto-bridge in `registry.py`: all 39 philosophers now work with `run_turn`
- 19 bridge tests

### Foundation Phase 1: E2E Test Foundation

- 37 E2E tests for `run_turn` pipeline
- Covers: happy path, safety mode transitions, degradation, blocking, red-team, trace contract
- `FixedTensorEngine` test utility for controlled freedom_pressure injection

### Foundation Phase 2: Pipeline Integration

- `PoSelf.generate()` migrated from `run_ensemble` → `run_turn` internally
- `po_core.run()` added as recommended public API entry point
- `PhilosophicalEnsemble` deprecated with `DeprecationWarning`
- 40 PoSelf tests

### Foundation Phase 3: Tensor Deepening

- `metric_freedom_pressure`: real 6D keyword analysis (was stub returning 0.0)
- `metric_semantic_delta`: token-overlap divergence vs memory
- `metric_blocked_tensor`: harm keyword + constraint scoring
- All 3 registered in `TensorEngine` via `wiring.py`
- 29 tensor metric tests

### Foundation Phase 4: Production Readiness

- `run_ensemble()` removed. All callers migrated to `po_core.run()` / `PoSelf.generate()`
- CI split: pipeline tests (must-pass) + full suite (best-effort)
- `pytest.mark.pipeline` marker on all 4 test files
- 125+ pipeline tests total

### Phase 1: Resonance Calibration & Foundation Settlement — COMPLETE

| # | Task | Status | Summary |
|---|------|--------|---------|
| 1 | Migrate 197 legacy tests to `run_turn` | **DONE** | 321 failures → 0. 2354 tests pass, 134 skipped (legacy), 9 xfailed (Phase 4) |
| 2 | Remove PhilosopherBridge dual interface | **DONE** | `bridge.py` deleted, registry simplified, all 39 use native `propose()` |
| 3 | 39-philosopher concurrent operation validation | **DONE** | 21 concurrency tests: parallel exec, timeout, latency, memory, SafetyMode scaling |
| 4 | Rebalance Freedom Pressure / W_Ethics Gate | **DONE** | FP thresholds recalibrated: WARN=0.30, CRITICAL=0.50 (was 0.60/0.85 — unreachable). 16 threshold tests |
| 5 | Philosopher semantic uniqueness assessment | **DONE** | 14 uniqueness tests: output diversity, vocabulary, tradition coverage, anti-homogenization |

**Exit Criteria — All Met:**

- Zero references to `run_ensemble` in tests ✓
- `PhilosopherBridge` deleted ✓
- 39-philosopher NORMAL mode < 5s (median < 500ms) ✓
- No philosopher pair > 0.85 semantic similarity (Jaccard < 0.8, mean < 0.4) ✓
- Full suite: 2354 passed, 134 skipped, 9 xfailed ✓

---

## Phase 2: Tensor Intelligence & Emergence Engine — COMPLETE

| # | Task | Status | Summary |
|---|------|--------|---------|
| 6 | Upgrade Semantic Delta to sentence-transformers | **DONE** | Multi-backend: sbert/tfidf/basic. encode_texts() + cosine_sim() shared API. 35 tests |
| 7 | Complete Interaction Tensor (NxN interference) | **DONE** | InteractionMatrix.from_proposals(): embedding harmony + keyword tension. 19 tests |
| 8 | Build Deliberation Engine (multi-round dialogue) | **DONE** | DeliberationEngine(max_rounds, top_k_pairs). Integrated into run_turn step 6.5. 14 tests |

**Exit Criteria — All Met:**

- Semantic delta uses embedding-based cosine similarity (with backend fallback) ✓
- InteractionMatrix returns NxN philosopher interference matrix ✓
- DeliberationEngine with `max_rounds` parameter integrated into `run_turn` ✓
- Full suite: 2396 passed, 134 skipped, 9 xfailed ✓

---

## Phase 3 (Current): Observability & Viewer Integration

| # | Task | Issue | Priority | Status |
|---|------|-------|----------|--------|
| 9 | Build Viewer WebUI (Dash) | ISSUES.md #9 | High | **IN PROGRESS** — Dash app + Plotly figures (pipeline, tensors, philosophers, drift gauge) |
| 10 | W_Ethics Gate explainability (explanation chain) | ISSUES.md #10 | High | **IN PROGRESS** — `ExplanationChain` + WebUI rendering (violation tree, repair log, drift gauge) |

**Phase 3 Implementation Progress:**

- `observability` pytest marker registered
- **ExplanationChain** data model: GateResult → structured chain (violations, repairs, drift)
  - `build_explanation_chain()` with `to_markdown()` and `to_dict()` outputs
  - Violation tree with code labels and evidence attribution
  - Drift status classification (acceptable / escalated / rejected)
- **Viewer WebUI** (Dash app):
  - 3-tab layout: Pipeline & Tensors / Philosophers / W_Ethics Gate
  - Plotly figures: tensor bar chart, pipeline step chart, philosopher latency chart, drift gauge
  - Decision badge with color coding (ALLOW/REPAIR/REJECT/ESCALATE)
  - ExplanationChain rendering: violations, repairs, drift, raw markdown
  - Collapsible raw text views for detailed inspection
- **E2E Integration**:
  - `PoViewer.from_run("prompt")` — one-liner pipeline → viewer
  - `PoViewer.serve()` — launch Dash dashboard from viewer
  - `create_app(events, explanation)` — full app factory
- 53 new Phase 3 tests (2477 total, 0 failures)
- Legacy `test_visualizer_with_po_self_session` skipped (Phase 3 scope)

**Remaining Work:**

- Trace database (SQLite) for historical query support
- Interaction heatmap (NxN philosopher tensor visualization)
- WebSocket streaming for real-time event delivery
- Human review interface for ESCALATE decisions

**Exit Criteria:**

- Browser-based dashboard showing tensors, philosophers, pipeline ← **DONE**
- W_Ethics Gate decisions include structured explanation chain ← **DONE**

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
