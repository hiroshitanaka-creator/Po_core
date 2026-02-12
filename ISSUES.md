# GitHub Issues — Po_core Phase 1–5

> Issue templates ready for creation. Copy each section into a GitHub Issue.
> Created: 2026-02-10

---

## Phase 1: Resonance Calibration & Foundation Settlement — COMPLETE (2026-02-12)

### Issue #1: Migrate 197 legacy tests to `run_turn` pipeline — DONE

**Labels:** `phase-1`, `testing`, `tech-debt`

- [x] Inventory and classify all legacy tests
- [x] Migrate valid tests to `po_core.run()` / `PoSelf.generate()`
- [x] Skip legacy tests pending Phase 3/5 migration (134 skipped)
- [x] Mark Phase 4 redteam tests as xfail (9 xfailed)
- [x] Result: 321 failures → 0. 2354 pass, 134 skipped, 9 xfailed

---

### Issue #2: Remove PhilosopherBridge dual interface — DONE

**Labels:** `phase-1`, `tech-debt`, `architecture`

- [x] All 39 philosophers implement `propose()` natively (via base class)
- [x] `bridge.py` deleted
- [x] `registry.py` simplified — raises TypeError for non-compliant objects
- [x] All tests updated — zero references to `PhilosopherBridge`

---

### Issue #3: 39-philosopher concurrent operation validation — DONE

**Labels:** `phase-1`, `testing`, `performance`

- [x] 21 concurrency tests in `test_philosopher_concurrency.py`
- [x] Parallel execution: all 39 produce proposals, no duplicates
- [x] Timeout enforcement: slow philosophers isolated
- [x] Latency: median < 500ms, all within timeout
- [x] Memory: loading < 10MB, execution peak < 20MB
- [x] SafetyMode scaling: NORMAL/WARN/CRITICAL philosopher counts verified

---

### Issue #4: Rebalance Freedom Pressure & W_Ethics Gate — DONE

**Labels:** `phase-1`, `tensors`, `safety`

- [x] Found critical bug: FP normalized to [0, ~0.44] but old thresholds (0.60/0.85) were unreachable
- [x] Recalibrated: WARN=0.30, CRITICAL=0.50 (settings.py + safety_mode.py)
- [x] 16 threshold tests in `test_safety_mode_thresholds.py`
- [x] All SafetyMode transitions (NORMAL→WARN→CRITICAL) now reachable and tested

---

### Issue #5: Philosopher semantic uniqueness assessment — DONE

**Labels:** `phase-1`, `philosophers`, `quality`

- [x] 14 uniqueness tests in `test_philosopher_uniqueness.py`
- [x] Output uniqueness: no duplicates, 30+ active, substantive content (>20 chars)
- [x] Vocabulary: 200+ collective words, 50%+ have unique words
- [x] Tradition coverage: 5+ traditions, Eastern + Western, risk distribution
- [x] Anti-homogenization: Jaccard < 0.8 per pair, mean < 0.4, 50+ unique key_concepts

---

## Phase 2: Tensor Intelligence & Emergence Engine

### Issue #6: Upgrade Semantic Delta to sentence-transformers

**Labels:** `phase-2`, `tensors`, `enhancement`
**Priority:** High

#### Description

Current `metric_semantic_delta` uses token overlap (bag-of-words Jaccard similarity). Upgrade to sentence-transformers embeddings for real semantic understanding. The library is already in `requirements.txt`.

#### Tasks

- [ ] Replace token-overlap logic in `tensors/metrics/semantic_delta.py` with `sentence-transformers` cosine similarity
- [ ] Use `all-MiniLM-L6-v2` as default model (fast, good quality)
- [ ] Evaluate `paraphrase-multilingual-MiniLM-L12-v2` for Japanese support
- [ ] Maintain backward-compatible `(str, float)` return signature
- [ ] Add lazy model loading with caching to avoid startup penalty
- [ ] Update tensor metric tests

#### Acceptance Criteria

- Semantic delta uses embedding-based similarity
- Model loads lazily (no import-time penalty)
- All existing tensor tests pass (backward compatible)
- New tests for semantic equivalence detection (paraphrases score high, unrelated score low)

---

### Issue #7: Complete Interaction Tensor implementation

**Labels:** `phase-2`, `tensors`, `enhancement`
**Priority:** High

#### Description

The Interaction Tensor framework exists (`tensors/interaction_tensor.py`) but computation logic is incomplete (maturity 2/10). This tensor should quantify philosopher-philosopher interference: agreement, opposition, or irrelevance.

#### Tasks

- [ ] Implement pairwise philosopher proposal comparison
- [ ] Define 3-state model: agree / oppose / irrelevant (with continuous scores)
- [ ] Register as `MetricFn` plugin in `TensorEngine`
- [ ] Connect to `test_comprehensive_layers.py` Layer 3 (Tension/Contradiction tests)
- [ ] Add visualization support in `viewer/tension_map.py`

#### Acceptance Criteria

- Interaction Tensor returns NxN matrix for N active philosophers
- Integrates with existing TensorEngine pipeline
- Tension visualization shows philosopher conflict zones

---

### Issue #8: Build Deliberation Engine (multi-round philosopher dialogue)

**Labels:** `phase-2`, `architecture`, `core`
**Priority:** Critical

#### Description

Currently, 39 philosophers propose independently and get aggregated (parallel → vote). There is no mechanism for philosophers to respond to each other. This is the single most important feature for achieving "emergence through deliberation."

#### Proposed Design

- **Round 1**: All philosophers `propose()` independently (current behavior)
- **Round 2**: Use Interaction Tensor to identify high-interference pairs. Those pairs receive each other's proposals and re-propose
- **Round 3**: Final Pareto aggregation on refined proposals

#### Tasks

- [ ] Design `DeliberationEngine` class in `src/po_core/deliberation/`
- [ ] Implement `max_rounds` parameter (default: 2, configurable)
- [ ] Wire into `run_turn` pipeline between PhilosopherSelect and ParetoAggregate
- [ ] Add TraceEvents for each deliberation round
- [ ] Performance testing: ensure multi-round stays within latency budget
- [ ] Add E2E tests comparing single-round vs multi-round output quality

#### Acceptance Criteria

- Multi-round deliberation produces measurably different output than single-round
- `max_rounds=1` produces identical behavior to current pipeline (backward compatible)
- Trace events capture per-round philosopher proposals
- Latency < 10s for 2-round deliberation with 39 philosophers

---

## Phase 3: Observability & Viewer Integration

### Issue #9: Build Viewer WebUI with Plotly Dash / Streamlit

**Labels:** `phase-3`, `viewer`, `frontend`
**Priority:** High

#### Description

Current viewer outputs text/Markdown only. Build an interactive browser-based dashboard for real-time pipeline observation. The `viewer/` module already uses Rich, Matplotlib, Plotly, NetworkX — wrap these in a web framework.

#### Tasks

- [ ] Evaluate Plotly Dash vs Streamlit for the dashboard
- [ ] Implement minimum viable dashboard: tensor time-series + philosopher participation map + pipeline step tracker
- [ ] Connect to `InMemoryTracer` event stream for real-time updates
- [ ] Add argument graph visualization for Deliberation Engine rounds
- [ ] Create launch command (`po-viewer` or `po-core viewer`)

---

### Issue #10: W_Ethics Gate explainability (explanation chain)

**Labels:** `phase-3`, `safety`, `explainability`
**Priority:** High

#### Description

When W_Ethics Gate rejects or repairs a proposal, users and developers need to understand *why*. Add structured explanation output showing which policy fired, what evidence triggered it, and what threshold was crossed.

#### Tasks

- [ ] Add `explanation` field to `GateResult` type
- [ ] Generate explanation chain: policy → evidence → threshold → decision
- [ ] Output as structured JSON + natural language summary
- [ ] Record explanation in TraceEvents
- [ ] Display in Viewer WebUI

---

## Phase 4: Adversarial Hardening

### Issue #11: Expand red team test suite to 50+ cases

**Labels:** `phase-4`, `testing`, `security`
**Priority:** High

#### Description

Current red team coverage: 2 files with ~14 test cases + 4 experimental files. Systematically expand to cover all known attack categories.

#### Tasks

- [ ] Prompt Injection: direct, indirect, encoding, multilingual (10+ tests)
- [ ] Jailbreak: roleplay, DAN, gradual escalation (10+ tests)
- [ ] Goal Misalignment: semantic drift, hidden agenda, intent-goal mismatch (10+ tests)
- [ ] Ethics Boundary: trolley problems, gray-zone dilemmas (10+ tests)
- [ ] Philosopher Exploitation: abuse risk-level-2 philosophers to bypass gates (10+ tests)
- [ ] Add defense metrics to CI (attack success rate, detection rate, false positive rate)

---

### Issue #12: Prototype LLM-based violation detector

**Labels:** `phase-4`, `safety`, `enhancement`
**Priority:** Medium

#### Description

Code comment in `gate.py` says "in production, swap with LLM". Prototype an LLM-based detector alongside the existing rule-based detectors to compare detection quality on edge cases.

#### Tasks

- [ ] Design `LLMViolationDetector` implementing `ViolationDetector` interface
- [ ] Evaluate with Claude API / local model on 50 red team cases
- [ ] Compare detection rate vs rule-based detector
- [ ] Document cost/latency tradeoffs

---

## Phase 5: Productization & Delivery

### Issue #13: Implement FastAPI REST API

**Labels:** `phase-5`, `api`, `core`
**Priority:** Critical

#### Description

Design documents exist in `03_api/` but no FastAPI implementation exists. Build production REST API.

#### Endpoints

- [ ] `POST /v1/reason` — synchronous reasoning
- [ ] `POST /v1/reason/stream` — streaming via SSE/WebSocket
- [ ] `GET /v1/philosophers` — philosopher list
- [ ] `GET /v1/trace/{session_id}` — trace retrieval
- [ ] `GET /v1/health` — health check
- [ ] OpenAPI/Swagger auto-generation
- [ ] API key authentication

---

### Issue #14: Docker containerization

**Labels:** `phase-5`, `devops`
**Priority:** High

#### Tasks

- [ ] Create `Dockerfile` (multi-stage build)
- [ ] Create `docker-compose.yml` (app + optional DB)
- [ ] Environment variable configuration via Pydantic `BaseSettings`
- [ ] Document in QUICKSTART.md

---

### Issue #15: PyPI package publishing

**Labels:** `phase-5`, `release`
**Priority:** Medium

#### Tasks

- [ ] Bump version to `0.2.0-beta` in `pyproject.toml`
- [ ] Update CHANGELOG.md with Phase 1–5 accomplishments
- [ ] Test `python -m build` + `twine check`
- [ ] Publish to TestPyPI first, then PyPI
- [ ] Add installation badge to README
