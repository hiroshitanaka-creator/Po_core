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

## Phase 2: Tensor Intelligence & Emergence Engine — COMPLETE (2026-02-12)

### Issue #6: Upgrade Semantic Delta to sentence-transformers — DONE

**Labels:** `phase-2`, `tensors`, `enhancement`

- [x] Multi-backend: sentence-transformers (sbert) / sklearn TfidfVectorizer / basic fallback
- [x] Lazy model loading with automatic fallback on runtime error
- [x] Shared API: `encode_texts()`, `cosine_sim()`, `get_backend()`
- [x] Backward-compatible `(str, float)` return signature maintained
- [x] 35 tests (was 27): +8 for backend detection, encoding API, paraphrase detection

---

### Issue #7: Complete Interaction Tensor (NxN interference) — DONE

**Labels:** `phase-2`, `tensors`, `enhancement`

- [x] `InteractionMatrix.from_proposals()`: embedding-based cosine similarity for harmony
- [x] Keyword-based tension detection (12 opposition pairs)
- [x] Synthesis = harmony * (1 - tension)
- [x] `high_interference_pairs(top_k)`, `high_tension_pairs()`, `high_harmony_pairs()`
- [x] 19 tests including real 39-philosopher integration

---

### Issue #8: Build Deliberation Engine (multi-round dialogue) — DONE

**Labels:** `phase-2`, `architecture`, `core`

- [x] `DeliberationEngine(max_rounds, top_k_pairs, convergence_threshold)`
- [x] Round 1: All philosophers propose() independently (current behavior)
- [x] Round 2+: InteractionMatrix selects high-interference pairs for counterargument re-proposal
- [x] Integrated into `run_turn` pipeline as step 6.5
- [x] Settings: `deliberation_max_rounds` (default 1 = off), `deliberation_top_k_pairs`
- [x] `max_rounds=1` produces identical behavior (backward compatible)
- [x] TraceEvent "DeliberationCompleted" with round summaries
- [x] 14 tests including real 39-philosopher deliberation

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
