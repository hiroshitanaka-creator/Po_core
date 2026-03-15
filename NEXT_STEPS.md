# Next Steps — Po_core Roadmap (Phases 1–7 Complete)

> Updated: 2026-02-22
> See [PHASE_PLAN_v2.md](./PHASE_PLAN_v2.md) for full rationale.
> See [ISSUES.md](./ISSUES.md) for GitHub Issue templates.
> See [docs/spec/](./docs/spec/) for PRD / SRS / Schema / TestCases / Traceability.

**Current status (2026-02-22): Phases 1–7 COMPLETE. v0.2.0b3 (po-core-flyingpig).**
PyPI publish pending. Spec/acceptance-test scaffolding in progress (M0).

---

## Summary: All Completed Phases

| Phase | Name | Status | Tests |
|-------|------|--------|-------|
| Foundation (0–4) | Bridge removal, E2E, pipeline integration | ✅ COMPLETE | 125+ pipeline |
| Phase 1 | Resonance Calibration | ✅ COMPLETE | 2354 pass |
| Phase 2 | Tensor Intelligence | ✅ COMPLETE | 2396 pass |
| Phase 3 | Observability | ✅ COMPLETE | +34 observability |
| Phase 4 | Adversarial Hardening | ✅ COMPLETE | +85 redteam |
| Phase 5 | Productization | ✅ COMPLETE (5-A〜E) | +24 REST API |
| Phase 6 | Autonomous Evolution | ✅ COMPLETE | FP-V2, Emergence, Memory |
| Phase 7 | AI Philosopher Slots | ✅ COMPLETE | Slots 40–43 |

**Remaining:** 5-F (PyPI publish) · Spec M0–M4 scaffolding · v1.0

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

## Phase 3 (COMPLETE): Observability & Viewer Integration

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

**Remaining Work (main実装同期済み):**

- Interaction heatmap (NxN philosopher tensor visualization)
- Human review queue persistence (current `review_store` is in-memory only)
- ESCALATE UI: pending review list + approve/reject action flow in viewer
- Streaming observability hardening (WS/SSE connection metrics, lag, disconnect telemetry)

**Exit Criteria:**

- Browser-based dashboard showing tensors, philosophers, pipeline ← **DONE**
- W_Ethics Gate decisions include structured explanation chain ← **DONE**

---

## Phase 4 (COMPLETE): Adversarial Hardening

- 85 new adversarial tests across 5 categories ✓
- 100% injection/jailbreak detection, ≤20% FP ✓
- All 14 redteam green ✓

---

## Phase 5 (COMPLETE — 5-A to 5-E): Productization & Delivery

- FastAPI 5 endpoints + SSE streaming + auth ✓
- Docker multi-stage + docker-compose ✓
- SlowAPI rate limiting + CORS config ✓
- AsyncPartyMachine (asyncio.gather) ✓
- Benchmarks: NORMAL p50 ~33ms ✓
- **5-F (PyPI publish): 🔲 PENDING** — `publish.yml` ready, not yet executed

---

## Phase 6 (COMPLETE): Autonomous Evolution

- FreedomPressureV2: ML-native 6D tensor + EMA + correlation ✓
- EmergenceDetector + InfluenceTracker ✓
- MetaEthicsMonitor + PhilosopherQualityLedger ✓
- 3-Layer Philosophical Memory (semantic + procedural + philosophical) ✓

---

## Phase 7 (COMPLETE): AI Philosopher Slots

- Slot 40: `claude_anthropic.py` (Constitutional AI) ✓
- Slot 41: `gpt_chatgpt.py` (RLHF reasoning) ✓
- Slot 42: `gemini_google.py` (Responsible AI) ✓
- Slot 43: `grok_xai.py` (Radical curiosity) ✓
- Total philosophers: 43 ✓

---

## Spec Scaffolding (M0 — Current Focus)

**Main progression criteria** as of 2026-02-22:

| Deliverable | File | Status |
|------------|------|--------|
| PRD | `docs/spec/prd.md` | ✅ v0.2 |
| SRS (with requirement IDs) | `docs/spec/srs_v0.1.md` | ✅ v0.2 |
| Output schema | `docs/spec/output_schema_v1.json` | ✅ v1.0 |
| Acceptance tests (10) | `docs/spec/test_cases.md` | ✅ v0.2 |
| Traceability (philosophy→req→test) | `docs/spec/traceability.md` | ✅ v0.2 |

**Next milestones:**

| Milestone | Focus |
|-----------|-------|
| M1 (2026-03-15) | Stub composer + E2E acceptance test runner (no LLM) |
| M2 (2026-04-05) | ethics_v1 + responsibility_v1 implementation |
| M3 (2026-04-26) | question_layer v1 |
| M4 (2026-05-10) | CI governance + ADR operations |
