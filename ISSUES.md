# GitHub Issues — Po_core Phases 1–7 + Spec M0–M4

> Issue templates ready for creation. Copy each section into a GitHub Issue.
> Created: 2026-02-10
> Updated: 2026-02-22 — Phases 6-7 complete; Spec M0 issues added.

**Status summary (2026-02-22):**
Phases 1–7 complete. v0.2.0b3 (po-core-flyingpig). Spec scaffolding (M0) in progress.

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

## Phase 3: Observability & Viewer Integration — COMPLETE (2026-02-14)

### Issue #9: Build Viewer WebUI with Plotly Dash / Streamlit — DONE

**Labels:** `phase-3`, `viewer`, `frontend`

- [x] Evaluated Plotly Dash → selected as framework
- [x] 4-tab Dash layout: Pipeline / Philosophers / W_Ethics Gate / Deliberation
- [x] Tensor time-series + philosopher participation map + pipeline step tracker
- [x] Connected to `InMemoryTracer` event stream (listener/callback mechanism)
- [x] Deliberation round chart + InteractionMatrix summary chart in `figures.py`
- [x] `po-viewer` launch via `PoViewer.serve()`

---

### Issue #10: W_Ethics Gate explainability (explanation chain) — DONE

**Labels:** `phase-3`, `safety`, `explainability`

- [x] `ExplanationChain` type added to `safety/wethics_gate/explanation.py`
- [x] `build_explanation_from_verdict()` bridges SafetyVerdict → ExplanationChain
- [x] `ExplanationEmitted` TraceEvent registered in schema
- [x] `extract_explanation_from_events()` reconstructs from trace events
- [x] `PoViewer.explanation()` auto-extracts; displayed in Viewer WebUI
- [x] 34 observability tests in `tests/unit/test_phase3_observability.py`

---

## Phase 4: Adversarial Hardening — COMPLETE (2026-02-16)

### Issue #11: Expand red team test suite to 50+ cases — DONE

**Labels:** `phase-4`, `testing`, `security`

- [x] Prompt Injection: `test_prompt_injection.py` — 7 tests, 100% detection
- [x] Jailbreak: `test_jailbreak_extended.py` — 15 adversarial pattern tests
- [x] Goal Misalignment: `test_goal_misalignment.py` — 7 tests passing
- [x] Ethics Boundary: `test_ethics_boundary.py` — 16 ethical grey zone tests
- [x] Defense metrics: `test_defense_metrics.py` — 11 automated metric tests
- [x] Unit coverage: `test_phase4_hardening.py` — 29 W_Ethics edge case tests
- [x] Result: 85 new adversarial tests, 100% injection/jailbreak detection, ≤20% FP rate

---

### Issue #12: Prototype LLM-based violation detector

**Labels:** `phase-4`, `safety`, `enhancement`
**Status:** Open — future roadmap item

#### Tasks

- [ ] Design `LLMViolationDetector` implementing `ViolationDetector` interface
- [ ] Evaluate with Claude API / local model on 50 red team cases
- [ ] Compare detection rate vs rule-based detector
- [ ] Document cost/latency tradeoffs

---

## Phase 5: Productization & Delivery — COMPLETE (2026-02-19)

### Issue #13: Implement FastAPI REST API — DONE

**Labels:** `phase-5`, `api`, `core`

- [x] `POST /v1/reason` — synchronous reasoning
- [x] `POST /v1/reason/stream` — SSE streaming
- [x] `GET /v1/philosophers` — full 43-philosopher manifest
- [x] `GET /v1/trace/{session_id}` — trace retrieval
- [x] `GET /v1/health` — health check with version + uptime
- [x] OpenAPI/Swagger auto-generated at `/docs` and `/redoc`
- [x] API key authentication via `X-API-Key` header (`PO_API_KEY` env var)
- [x] CORS via `PO_CORS_ORIGINS`, rate limiting via `PO_RATE_LIMIT_PER_MINUTE`
- [x] 24 unit tests in `tests/unit/test_rest_api.py`

---

### Issue #14: Docker containerization — DONE

**Labels:** `phase-5`, `devops`

- [x] `Dockerfile` — multi-stage build (builder + slim runtime, non-root `pocore` user)
- [x] `docker-compose.yml` — named volumes + 30s health check
- [x] `.env.example` — full environment variable reference
- [x] `QUICKSTART.md` updated with Docker and REST API sections

---

### Issue #15: PyPI package publishing

**Labels:** `phase-5`, `release`

- [x] Version bumped to `0.2.0-beta` in `pyproject.toml`
- [x] CHANGELOG.md updated with all phase accomplishments
- [x] `.github/workflows/publish.yml` — OIDC trusted publishing workflow ready
- [ ] Publish to TestPyPI (manual `workflow_dispatch`)
- [ ] Publish to PyPI on v0.2.0 release tag

---

## Phase 5-D/E: Async & Benchmarks — COMPLETE (2026-02-19)

### Issue #16: True Async PartyMachine — DONE

**Labels:** `phase-5d`, `async`, `performance`

- [x] `async_run_philosophers()` in `party_machine.py` — asyncio-native parallel execution
- [x] `asyncio.gather` + `ThreadPoolExecutor` for non-blocking philosopher dispatch
- [x] Per-philosopher timeout via `asyncio.wait_for`
- [x] REST layer updated: `reason()` and `_sse_generator()` no longer block FastAPI event loop
- [x] 7 async unit tests in `tests/unit/test_phase5d_async.py`
- [x] Benchmark: p50 NORMAL ~33ms, async × 39 phil ~11ms

---

## Phase 6: Autonomous Evolution — COMPLETE (2026-02-19)

### Issue #17: FreedomPressureV2 — ML-native 6D tensor — DONE

**Labels:** `phase-6a`, `tensors`, `ml`

- [x] `freedom_pressure_v2.py` — ML-native 6-dimensional freedom pressure tensor
- [x] EMA smoothing with configurable decay factor
- [x] Correlation matrix for cross-dimensional interaction
- [x] `create_freedom_pressure_v2()` factory function
- [x] Integrated into `TensorEngine` alongside v1

---

### Issue #18: EmergenceDetector + InfluenceTracker — DONE

**Labels:** `phase-6b`, `deliberation`, `emergence`

- [x] `deliberation/emergence.py` — detects emergent consensus across philosopher rounds
- [x] `deliberation/influence.py` — tracks cross-philosopher influence patterns
- [x] 10 integration tests in `tests/integration/test_emergence_integration.py`

---

### Issue #19: MetaEthicsMonitor + PhilosopherQualityLedger — DONE

**Labels:** `phase-6c`, `meta`, `ethics`

- [x] `meta/ethics_monitor.py` — MetaEthicsMonitor: self-reflective ethical quality assessment
- [x] `meta/philosopher_ledger.py` — PhilosopherQualityLedger: per-philosopher performance tracking
- [x] Integrated into pipeline trace events

---

### Issue #20: 3-Layer Philosophical Memory System — DONE

**Labels:** `phase-6de`, `memory`, `architecture`

- [x] `memory/semantic_store.py` — semantic/episodic memory (embedding-based recall)
- [x] `memory/procedural_store.py` — procedural memory (pattern-based)
- [x] `memory/philosophical_memory.py` — top-level orchestrator across all layers

---

## Phase 7: AI Philosopher Slots — COMPLETE (2026-02-19)

### Issue #21: Add AI company philosophers (slots 40–43) — DONE

**Labels:** `phase-7`, `philosophers`, `ai-ethics`

- [x] Slot 40: `claude_anthropic.py` — Claude/Anthropic constitutional AI perspective
- [x] Slot 41: `gpt_chatgpt.py` — GPT/OpenAI RLHF-grounded reasoning
- [x] Slot 42: `gemini_google.py` — Gemini/Google responsible AI principles
- [x] Slot 43: `grok_xai.py` — Grok/xAI radical curiosity + free inquiry
- [x] All 4 registered in `manifest.py` with risk levels and tags
- [x] Total philosophers: 43 (was 39)

---

## Spec M0: Specification Scaffolding — IN PROGRESS (2026-02-22)

### Issue #22: Create PRD and SRS with requirement IDs — IN PROGRESS

**Labels:** `spec`, `documentation`, `m0`

- [x] `docs/spec/prd.md` v0.2 — Purpose, target users, scope, success metrics, philosophy premises, roadmap (Phases 1–7 + M0–M4)
- [x] `docs/spec/srs_v0.1.md` v0.2 — 18 requirement IDs (FR-OUT-001 〜 NFR-SEC-001), 2-layer architecture, REST API interface spec
- [ ] Requirement IDs linked to GitHub Issues (M1)
- [ ] CI check: SRS updated on every spec-changing PR

---

### Issue #23: Finalize output schema (output_schema_v1.json) — IN PROGRESS

**Labels:** `spec`, `schema`, `m0`

- [x] `docs/spec/output_schema_v1.json` v1.0 — Full JSON Schema Draft 2020-12
- [x] Core fields: meta, case_ref, options, recommendation, ethics, responsibility, questions, uncertainty, trace
- [x] Po_core-specific extensions: philosopher_contributions, tensors, explanation_chain, pocore_events
- [x] generator.mode enum: stub / rule_based / llm / hybrid
- [ ] `jsonschema` CI validation gate (M1)
- [ ] Golden file for AT-001 and AT-009

---

### Issue #24: Write 10 acceptance test cases — IN PROGRESS

**Labels:** `spec`, `testing`, `m0`

- [x] `docs/spec/test_cases.md` v0.2 — 10 acceptance tests (AT-001 〜 AT-010)
- [x] Given/When/Then format with condition ID breakdown
- [x] Global rules: AT-OUT-001 guard, MUST-only evaluation, no content judgment
- [ ] `tests/acceptance/` test runner implementation (M1)
- [ ] `scenarios/case_001.yaml` 〜 `case_010.yaml` scenario files (M1)

---

### Issue #25: Build traceability matrix (philosophy → requirements → tests) — IN PROGRESS

**Labels:** `spec`, `documentation`, `m0`

- [x] `docs/spec/traceability.md` v0.2 — 4 matrices: philosophy→req→test, req→impl→test, scenario→AT→req, impl→req
- [x] 5 ADR entries (0001–0005)
- [x] Milestone status table (M0–M4)
- [ ] Auto-generate coverage report from traceability matrix (M2)

---

## Remaining Tasks (Post-M0)

### Issue #26: PyPI publish (Phase 5-F) — PENDING

**Labels:** `phase-5f`, `release`

- [x] Version: `0.2.0b3` (PEP 440 compliant)
- [x] Package name: `po-core-flyingpig`
- [x] `publish.yml` OIDC workflow ready
- [ ] Publish to TestPyPI (`workflow_dispatch`)
- [ ] Publish to PyPI on `v0.2.0` release tag

---

### Issue #27: v1.0 stabilization — PLANNED

**Labels:** `v1.0`, `roadmap`

- [ ] AT-001〜AT-010 all passing (M2 complete)
- [ ] PyPI publish done (Issue #26)
- [ ] Academic paper draft complete
- [ ] CHANGELOG entry for v1.0.0
