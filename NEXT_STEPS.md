# Next Steps — Post Phase 0-4

This document tracks issues to be created on GitHub and remaining work items.

## Completed Phases (this branch)

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
- `run_ensemble()` deprecated with `DeprecationWarning`
- CI split: pipeline tests (must-pass) + full suite (best-effort)
- `pytest.mark.pipeline` marker on all 4 test files
- 125+ pipeline tests total

---

## Open Issues to Create

### Issue: Migrate legacy test suite to `run_turn`
**Priority:** Medium
**Labels:** `testing`, `tech-debt`

197 legacy tests still use `run_ensemble` or broken imports. These should be:
1. Triaged (which tests still apply)
2. Migrated to use `run_turn` / `po_core.run()`
3. Removed if no longer relevant

### Issue: Remove `run_ensemble` in v0.3
**Priority:** Low (scheduled)
**Labels:** `breaking-change`, `v0.3`

`run_ensemble()` is deprecated since Phase 4. Plan removal:
1. Search all callers in codebase
2. Migrate remaining usages
3. Remove function + legacy dependencies
4. Update documentation

### Issue: Implement sentence-level semantic delta
**Priority:** Medium
**Labels:** `enhancement`, `tensors`

Current `metric_semantic_delta` uses token overlap (bag-of-words). Upgrade to:
- sentence-transformers embeddings (already in requirements.txt)
- Cosine similarity for better semantic understanding
- Backward-compatible (same `(str, float)` return signature)

### Issue: Add golden regression tests (DecisionEmitted events)
**Priority:** High
**Labels:** `testing`, `quality`

Capture golden `DecisionEmitted` trace events for known inputs and assert stability:
- Prevents silent behavioral regression
- Pair with config_version tracking in TraceEvents

### Issue: PhilosopherProtocol migration — remove dual interface
**Priority:** Medium
**Labels:** `tech-debt`, `architecture`

Currently both `Philosopher.reason()` and `PhilosopherProtocol.propose()` exist.
PhilosopherBridge adapts between them. Long-term:
1. Migrate all 39 philosophers to implement `PhilosopherProtocol` natively
2. Remove `PhilosopherBridge` adapter
3. Simplify registry

### Issue: TensorEngine — add remaining tensor types
**Priority:** Low
**Labels:** `enhancement`, `tensors`

Legacy tensors not yet in TensorEngine:
- Interaction Tensor (philosopher-philosopher interference)
- Semantic Profile (full conversation tracking, not just single-turn delta)
- Consider adding as `MetricFn` plugins

### Issue: Viewer integration with new trace format
**Priority:** Medium
**Labels:** `viewer`, `frontend`

The Viewer currently expects legacy trace format. Update to:
- Read `InMemoryTracer` / `TraceEvent` stream
- Display 10-step pipeline progression
- Show tensor metric evolution
- A/B shadow diff visualization
