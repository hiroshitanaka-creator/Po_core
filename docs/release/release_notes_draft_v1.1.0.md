# Release Notes Draft — Po_core v1.1.0

Status: **DRAFT** — version not yet bumped; no PyPI publish initiated.  
Base: `v1.0.3` (published 2026-03-22)  
Draft prepared from `main @ 5938c40` (2026-04-30)  
SemVer rationale: minor bump — backward-compatible new functionality
(new public API entry point, new trace events, new audit fields).

---

## Summary

v1.1.0 delivers a structured output API, a complete engine trace audit
contract, and 53 new tests.  All changes are backward-compatible:
existing `po_core.run()` callers are unaffected.

Completion matrix pass count increased from 110 to 164 (164 pass / 0 fail / 0 not-yet).

---

## New features

### `run_case(case: dict)` public API  (RT-GAP-004)

`po_core.run_case()` and `po_core.async_run_case()` are now exported from
the top-level package.  They accept a structured case dict and return an
`output_schema_v1`-conformant result — the same shape produced by the
acceptance test suite and `StubComposer`.

```python
import po_core
result = po_core.run_case(case)   # → output_schema_v1 dict
```

- `run()` return shape is unchanged (`{status, request_id, proposal, proposals}`).
- `run_case()` return shape is governed by `output_schema_v1.json`.
- `async_run_case()` is the async counterpart.

### Scenario-aware philosopher selection  (RT-GAP-001/002/003)

`CaseSignals` and `_SCENARIO_ROUTING` route each `scenario_type` to a
dedicated `(preferred_tags, limit_override)` pair, guaranteeing
archetype-appropriate rosters:

| `scenario_type` | `preferred_tags` | `limit_override` |
|---|---|---|
| `values_clarification` | clarify, creative, compliance | 3 |
| `conflicting_constraints` | critic, redteam, planner | 3 |
| `general` (default) | — | — |

When `values_present=False`, the primary proposal `action_type` is
overridden to `"clarify"`.  When `has_constraint_conflict=True`,
`constraint_conflict: true` is injected into the result dict.

---

## Engine trace improvements

All changes are additive.  Existing event consumers are unaffected unless
they check for absence of new keys.

### `TensorComputed` — metric provenance  (TENSOR-TR-1, TENSOR-TR-2)

`TensorComputed.metrics` is documented and sample-validated as
`dict[str, float]`.  A new `metric_status` field records per-metric provenance:

```json
"metric_status": {
  "freedom_pressure":    {"status": "computed", "source": "freedom_pressure"},
  "semantic_delta":      {"status": "computed", "source": "semantic_delta"},
  "blocked_tensor":      {"status": "computed", "source": "blocked_tensor"},
  "interaction_tensor":  {"status": "missing",  "source": null}
}
```

- `"computed"` — value is `int` or `float`.
- `"missing"` — value is absent, `None`, or non-numeric.
- All four expected metrics always appear, even when absent from the engine snapshot.
- Extra metrics beyond the four expected are classified by the same rule.
- `TensorEngine.compute()` now also populates `TensorSnapshot.values`
  with `TensorValue(source=module_name)` for each metric function.

### `SafetyModeInferred` — new trace event  (MODE-TR-1, MODE-TR-2)

A new `SafetyModeInferred` event is emitted immediately after
`infer_safety_mode()`, before philosopher selection:

```json
{
  "event_type": "SafetyModeInferred",
  "payload": {
    "mode": "normal",
    "freedom_pressure": 0.09,
    "warn_threshold": 0.30,
    "critical_threshold": 0.50,
    "missing_mode": "warn",
    "source_metric": "freedom_pressure",
    "reason": "freedom_pressure < warn_threshold"
  }
}
```

The `reason` field is one of four values covering the full branch space
(missing / below warn / between warn and critical / at or above critical).

### `PhilosophersSelected` — full selection rationale  (SEL-TR-1)

Seven new fields in `PhilosophersSelected` expose the effective constraints
used to build the roster:

| New field | Description |
|---|---|
| `scenario_type` | Routing scenario (`"general"`, `"values_clarification"`, `"conflicting_constraints"`) |
| `preferred_tags` | Tags that drove first-pass slot fill; `null` in general scenario |
| `limit_override` | Caller-supplied roster cap; `null` in general scenario |
| `limit` | **Effective** roster cap used (equals `limit_override` when set) |
| `require_tags` | **Effective** required tags used in slot fill |
| `max_risk` | Maximum individual philosopher risk level allowed |
| `cost_budget` | Maximum cost budget for the selection |

### Pareto trace — `weighted_score`, `emergence`, and `weights`  (AGG-TR-1/2/3)

- `ParetoWinnerSelected` now includes a top-level `weights` dict alongside
  `winner`, making `weighted_score` recomputable from the trace alone.
- `ParetoWinnerSelected.winner.weighted_score` — scalar score (6 sig. fig.)
  recomputable as `Σ score_i × weight_i` within 1e-4.
- All six objectives now appear in every scores dict: `safety`, `freedom`,
  `explain`, `brevity`, `coherence`, `emergence`.
- `ParetoWeights` gains an `emergence` field (default: NORMAL=0.10,
  WARN=0.05, CRITICAL=0.00).

### `DecisionEmitted` / `SafetyOverrideApplied` — decision audit chain  (AGG-TR-4)

The full decision audit chain is now assertion-locked:

- Normal path: `AggregateCompleted.proposal_id` ==
  `ParetoWinnerSelected.winner.proposal_id` ==
  `DecisionEmitted.final.proposal_id`, `degraded=false`.
- Override path: `SafetyOverrideApplied` is emitted between
  `ParetoWinnerSelected` and `DecisionEmitted`; `degraded=true`,
  `candidate.proposal_id` traces back to the rejected winner.

`ProposalFingerprint` carries `content_hash` / `content_len` only — no raw
content is exposed (security boundary).

### `CaseSignalsApplied` — pipeline mutation audit  (TR-1)

`CaseSignalsApplied` is emitted when `_apply_case_signals()` mutates the
result dict, recording `action_type_before`, `action_type_after`, and a
list of `applied_changes`.  Not emitted when no mutation occurs.

---

## Documentation

- **`docs/ENGINE_TRACE_CONTRACT.md`** — new; full field-level spec for all
  trace events, normal-path and override-path sequence examples, known
  non-goals, and `weighted_score` recomputation formula.
- **`docs/viewer/README.md`** — new; explains normal path, override path
  (conditional), conditional events, key field changes since original
  sample capture.
- **`docs/viewer/sample_trace.json`** — updated; aligned to current
  contract (metrics dict, metric_status, SafetyModeInferred, PhilosophersSelected
  rationale, ParetoFrontComputed emergence, ParetoWinnerSelected
  weighted_score/weights).

---

## Test coverage

| Test class / file | New tests | Gate |
|---|---|---|
| `TestRunCaseSchemaConformance` | 7 | acceptance |
| `TestCaseSignalsTraceVisibility` | 5 | acceptance |
| `TestParetoWinnerTraceContract` | 3 | acceptance |
| `TestParetoWinnerScoreExplainability` | 3 | acceptance |
| `TestParetoSafetyModeWeights` + loader | 4 | acceptance + packaging |
| `TestActionGateTraceContract` | 2 | acceptance |
| `TestSafetyModeInferredTrace` | 3 | acceptance |
| `TestSafetyModeInferredBranches` | 7 | unit (pure function) |
| `TestPhilosopherSelectionRationale` | 4 | acceptance |
| `TestTensorComputedTrace` | 3 | acceptance |
| `TestTensorComputedStatusTrace` | 4 | acceptance |
| `TestSampleTraceContract` | 8 | unit (JSON parse) |
| **Total new** | **53** | |

`completion_matrix.md` total: **164 pass / 0 fail / 0 not-yet**  
(was 110 at v1.0.3 close)

---

## Backward compatibility

| Change | Impact |
|---|---|
| `run()` return shape | **Unchanged** |
| `TensorComputed.metrics` | **Viewer sample alignment only** — older `docs/viewer/sample_trace.json` represented `metrics` as a list of names; the current engine trace contract defines it as `dict[str, float]`, and the sample now matches. Runtime `run()` and `run_case()` return shapes are unchanged. Consumers of the sample file or custom trace viewers that assumed the old list shape should update their parsers. |
| New trace event `SafetyModeInferred` | Additive — consumers ignoring unknown events are unaffected |
| New fields in `PhilosophersSelected` | Additive |
| New fields in `ParetoWinnerSelected` (`weights`, `winner.weighted_score`) | Additive |
| `ParetoWeights.emergence` | Additive — existing `to_dict()` callers gain one new key |
| `run_case()` / `async_run_case()` | New export — no existing code affected |

**Note**: older versions of `docs/viewer/sample_trace.json` represented
`TensorComputed.metrics` as a list of metric names.  The sample has been
updated to match the contract (`dict[str, float]`).  Consumers of that
sample file or custom trace viewers that assumed the old list shape should
update their parsers.  Production `run()` and `run_case()` return shapes
are unchanged.

---

## Pre-release checklist

- [ ] Version bump: `src/po_core/__init__.py` `__version__` → `"1.1.0"`
- [ ] `pyproject.toml` dynamic version reads from `__version__`  (already configured)
- [ ] CHANGELOG: add `[1.1.0]` section above `[1.0.3]`
- [ ] `docs/status.md`: update `Repository target version` and `Latest published public version`
- [ ] Golden files: regenerate if `TensorComputed.metrics` dict change
  breaks `at_*_expected.json` diffs
- [ ] CI green on `main` (`pytest tests/ -v -m "not slow"`)
- [ ] TestPyPI publish and smoke
- [ ] PyPI publish
- [ ] Post-publish smoke (`scripts/release_smoke.py --check-entrypoints`)

---

## Files changed since v1.0.3

**Production code:**
- `src/po_core/__init__.py` — export `run_case`, `async_run_case`
- `src/po_core/app/api.py` — `run_case` / `async_run_case` implementation
- `src/po_core/ensemble.py` — `SafetyModeInferred`, `CaseSignalsApplied`,
  `_SCENARIO_ROUTING`, `_apply_case_signals`, `_build_safety_mode_inferred_payload`,
  `TensorComputed.metric_status`, `_tensor_metric_status_entry`,
  `PhilosophersSelected` rationale fields
- `src/po_core/aggregator/pareto.py` — `weighted_score`, `emergence` objective
- `src/po_core/domain/pareto_config.py` — `ParetoWeights.emergence`
- `src/po_core/philosophers/registry.py` — `Selection` dataclass with rationale fields
- `src/po_core/philosophers/allowlist.py` — pass-through of new `Selection` fields
- `src/po_core/tensors/engine.py` — `TensorSnapshot.values` population
- `src/po_core/trace/pareto_events.py` — `weights` in `ParetoWinnerSelected`
- `src/po_core/config/runtime/pareto_table.yaml` — emergence weights added

**Tests (new):**
- `tests/acceptance/test_runtime_acceptance.py` — 37 new acceptance tests
- `tests/unit/test_safety_mode_inferred_branches.py` — 7 unit tests
- `tests/unit/test_sample_trace_contract.py` — 8 unit tests

**Docs (new/updated):**
- `docs/ENGINE_TRACE_CONTRACT.md` — new
- `docs/viewer/README.md` — new
- `docs/viewer/sample_trace.json` — updated
- `docs/completion_matrix.md` — updated
- `docs/status.md` — updated
