# Engine Trace Contract

This document describes the TraceEvents emitted by the `run_turn` pipeline.
All events are accessible via `InMemoryTracer.events` and share the schema
defined in `po_core.domain.trace_event.TraceEvent` (frozen dataclass with
`event_type`, `request_id`, `occurred_at`, `payload`).

---

## 1. End-to-end trace chain

A typical normal-path run emits events in this order:

```
MemorySnapshotted
TensorComputed
SafetyModeInferred
IntentGenerated
SafetyJudged:Intention
PhilosophersSelected
PhilosopherResult  ×N
PolicyPrecheckSummary
AggregateCompleted
ConflictSummaryComputed      ⟵ from emit_pareto_debug_events
ParetoFrontComputed          ⟵
ParetoWinnerSelected         ⟵
ExplanationEmitted
DecisionEmitted
CaseSignalsApplied           (only when CaseSignals mutates the result)
```

Optional / conditional events:

| Event | Condition |
|---|---|
| `CaseSignalsApplied` | `case_signals` provided **and** at least one mutation applied |
| `SafetyOverrideApplied` | Action Gate rejects Pareto winner |
| `SafetyDegraded` | Intention Gate rejects intent |
| `ExplanationEmitted` | Every gate evaluation (best-effort; `ExplanationEmitFailed` on error) |
| `PhilosopherLoadError` | Registry fails to import a philosopher module |
| `SynthesisReportFailed` | Exception in `_build_synthesis_report` |

---

## 2. TensorComputed

Emitted after `TensorEngine.compute()` returns.

```json
{
  "metrics": {
    "freedom_pressure": 0.42,
    "semantic_delta": 0.31,
    "blocked_tensor": 0.19,
    "interaction_tensor": 0.07
  },
  "version": "v1",
  "metric_status": {
    "freedom_pressure": {"status": "computed", "source": "freedom_pressure"},
    "semantic_delta":   {"status": "computed", "source": "semantic_delta"},
    "blocked_tensor":   {"status": "computed", "source": "blocked_tensor"},
    "interaction_tensor": {"status": "missing", "source": null}
  }
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `metrics` | `dict[str, float\|None]` | Raw metric values returned by the engine. Keys are metric names; values are `float` or `None`. |
| `version` | `str` | Engine schema version (currently `"v1"`). |
| `metric_status` | `dict[str, StatusEntry]` | Per-metric audit entry for every key in `metrics` **plus** every key in `_EXPECTED_TENSOR_METRICS`. Always covers `freedom_pressure`, `semantic_delta`, `blocked_tensor`, `interaction_tensor`. |

### StatusEntry

| Field | Values | Description |
|---|---|---|
| `status` | `"computed"` \| `"missing"` | `"computed"` iff the value is `int` or `float`. `"missing"` for `None`, absent key, or any non-numeric value. |
| `source` | `str` \| `null` | Module name suffix from the metric function's `__module__` (e.g. `"freedom_pressure"`). `null` when status is `"missing"`. |

**Expected metrics** (`_EXPECTED_TENSOR_METRICS`):
`freedom_pressure`, `semantic_delta`, `blocked_tensor`, `interaction_tensor`.
All four always appear in `metric_status`, even when absent from `metrics`.

---

## 3. SafetyModeInferred

Emitted immediately after `infer_safety_mode()` in `_run_phase_pre`.

```json
{
  "mode": "normal",
  "freedom_pressure": 0.42,
  "warn_threshold": 0.30,
  "critical_threshold": 0.50,
  "missing_mode": "warn",
  "source_metric": "freedom_pressure",
  "reason": "freedom_pressure < warn_threshold"
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `mode` | `"normal"` \| `"warn"` \| `"critical"` | Inferred SafetyMode string value. |
| `freedom_pressure` | `float \| null` | Value of the `freedom_pressure` metric; `null` when absent from tensor snapshot. |
| `warn_threshold` | `float` | `Settings.freedom_pressure_warn` (default `0.30`). |
| `critical_threshold` | `float` | `Settings.freedom_pressure_critical` (default `0.50`). |
| `missing_mode` | `str` | Mode applied when `freedom_pressure` is absent (`Settings.freedom_pressure_missing_mode`). |
| `source_metric` | `"freedom_pressure"` | Always `"freedom_pressure"` (the single driving metric). |
| `reason` | `str` | One of four values (see below). |

### `reason` values

| Value | Condition |
|---|---|
| `"freedom_pressure_missing"` | `freedom_pressure` is `None` |
| `"freedom_pressure < warn_threshold"` | `fp < warn` |
| `"warn_threshold <= freedom_pressure < critical_threshold"` | `warn <= fp < critical` |
| `"freedom_pressure >= critical_threshold"` | `fp >= critical` |

---

## 4. PhilosophersSelected

Emitted after `registry.select()` returns in `_run_phase_pre`.

```json
{
  "mode": "normal",
  "n": 42,
  "cost_total": 80,
  "covered_tags": ["clarify", "compliance", "creative", "critic", "planner"],
  "ids": ["aristotle", "confucius", "..."],
  "workers": 8,
  "scenario_type": "general",
  "preferred_tags": null,
  "limit_override": null,
  "max_risk": 2,
  "cost_budget": 80,
  "limit": 42,
  "require_tags": ["clarify", "compliance", "creative", "critic", "planner", "redteam"]
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `mode` | `str` | SafetyMode string (same as `SafetyModeInferred.mode`). |
| `n` | `int` | Number of philosophers selected (`len(ids)`). |
| `ids` | `list[str]` | Philosopher IDs in selection order. |
| `cost_total` | `int` | Sum of `risk` costs for selected philosophers. |
| `cost_budget` | `int` | Maximum cost allowed by the current SelectionPlan. |
| `max_risk` | `int` | Maximum individual risk level allowed (0–2). |
| `limit` | `int` | **Effective** roster cap used during selection. Equals `limit_override` when set, otherwise the SelectionPlan default. |
| `limit_override` | `int \| null` | Caller-supplied cap (from `_SCENARIO_ROUTING`). `null` in the default `general` scenario. |
| `require_tags` | `list[str]` | **Effective** required tags used in first-pass slot fill. |
| `preferred_tags` | `list[str] \| null` | Tags that drove slot fill (from `_SCENARIO_ROUTING`). `null` in the default scenario. |
| `covered_tags` | `list[str]` | Union of tags present across the selected roster. |
| `scenario_type` | `str` | Scenario from `CaseSignals` (`"general"`, `"values_clarification"`, `"conflicting_constraints"`). |
| `workers` | `int` | Swarm concurrency limit for philosopher execution. |

### Scenario routing (`_SCENARIO_ROUTING`)

| `scenario_type` | `preferred_tags` | `limit_override` |
|---|---|---|
| `"values_clarification"` | `[clarify, creative, compliance]` | `3` |
| `"conflicting_constraints"` | `[critic, redteam, planner]` | `3` |
| `"general"` (default) | `null` | `null` |

---

## 5. Pareto events

Three events are emitted by `emit_pareto_debug_events()` in sequence, immediately
before the Action Gate judgment.  All three share a common base payload.

### Common base fields

| Field | Type | Description |
|---|---|---|
| `variant` | `"main"` \| `"shadow"` | Which aggregator produced this run. |
| `mode` | `str` | SafetyMode in effect during aggregation. |
| `freedom_pressure` | `str` | `str(fp)` or `""` when `None`. |
| `config_version` | `str` | `ParetoConfig.version` — matches `pareto_table.yaml`'s `config_version`. |
| `config_source` | `str` | Path/label of the loaded config file. |

### ConflictSummaryComputed

Extends base with conflict report fields:

| Field | Type | Description |
|---|---|---|
| `n` | `int` | Total conflict count. |
| `kinds` | `str` | Comma-separated conflict kind labels. |
| `suggested_forced_action` | `str` | Resolver suggestion or `""`. |
| `top` | `list` | Up to 5 highest-severity conflicts, each with `id`, `kind`, `severity`, `proposal_ids`. |

### ParetoFrontComputed

| Field | Type | Description |
|---|---|---|
| `weights` | `dict[str, float]` | Objective weights for this mode (`safety`, `freedom`, `explain`, `brevity`, `coherence`, `emergence`). |
| `front_size` | `int` | Number of non-dominated proposals on the Pareto front. |
| `front` | `list` | Up to 20 front rows, each with `proposal_id`, `action_type`, `scores` (6-objective dict), `content_len`, `content_hash`. |

### ParetoWinnerSelected

| Field | Type | Description |
|---|---|---|
| `weights` | `dict[str, float]` | Same weights as `ParetoFrontComputed`. |
| `winner` | `WinnerPayload` | See below. |

**WinnerPayload:**

| Field | Type | Description |
|---|---|---|
| `proposal_id` | `str` | ID of the selected winner. |
| `action_type` | `str` | Action type of the winner. |
| `scores` | `dict[str, float]` | Six objective scores: `safety`, `freedom`, `explain`, `brevity`, `coherence`, `emergence`. |
| `weighted_score` | `float` | Scalar score (6 significant figures). |
| `content_len` | `int` | Character count (not content). |
| `content_hash` | `str` | SHA-1 fingerprint, first 10 hex chars. |

### weighted_score recomputation

```
weighted_score =
    scores.safety    × weights.safety
  + scores.freedom   × weights.freedom
  + scores.explain   × weights.explain
  + scores.brevity   × weights.brevity
  + scores.coherence × weights.coherence
  + scores.emergence × weights.emergence
```

All six terms are in `[0, 1]`. Recomputed value should match `weighted_score`
within `1e-4`.

---

## 6. Decision events

### AggregateCompleted

Emitted immediately after `aggregator.aggregate()` returns, before the Action Gate.

```json
{
  "proposal_id": "req-abc:aggregate:winner",
  "action_type": "recommend"
}
```

| Field | Description |
|---|---|
| `proposal_id` | Aggregator winner ID. Must match `ParetoWinnerSelected.winner.proposal_id`. |
| `action_type` | Action type of the aggregator winner. |

### DecisionEmitted

Emitted once per `_evaluate_candidate` call (main and optionally shadow).
Represents **the proposal that left the system**.

```json
{
  "variant": "main",
  "stage": "action",
  "origin": "pareto",
  "degraded": false,
  "pareto_config_version": "v1.2",
  "pareto_config_source": "config/runtime/pareto_table.yaml",
  "final": { "proposal_id": "...", "action_type": "recommend", "confidence": 0.85, "content_len": 312, "content_hash": "a3f9c2d1e0", "author": "aristotle", "freedom_pressure": "0.42", "policy_decision": "allow", "policy_score": "0.9", "author_reliability": "0.8", "pareto_config_version": "v1.2", "pareto_config_source": "..." },
  "candidate": { ... },
  "gate": { "decision": "allow", "rule_ids": [], "required_changes_n": 0, "reasons_n": 0, "meta": {} }
}
```

| Field | Type | Description |
|---|---|---|
| `variant` | `"main"` \| `"shadow"` | Aggregator variant. |
| `stage` | `"action"` \| `"intent"` | Pipeline stage where decision was made. |
| `origin` | `str` | Source of the decision: `"pareto"`, `"pareto_fallback"`, `"safety_fallback"`, `"intent_gate_fallback"`, `"intent_gate_blocked"`. |
| `degraded` | `bool` | `true` when the final proposal is a fallback, not the Pareto winner. |
| `pareto_config_version` | `str` | Pareto config version from the candidate's extra. |
| `pareto_config_source` | `str` | Pareto config source path from the candidate's extra. |
| `final` | `ProposalFingerprint` | Fingerprint of the proposal that was returned. See below. |
| `candidate` | `ProposalFingerprint \| null` | Fingerprint of the original Pareto candidate (may differ from `final` on override). |
| `gate` | `VerdictSummary \| null` | Action Gate verdict. Present when `gate_verdict` is available. |

**ProposalFingerprint** (no raw content — hash/len only):

| Field | Description |
|---|---|
| `proposal_id` | Proposal ID. |
| `action_type` | Action type string. |
| `confidence` | Float confidence score. |
| `content_len` | Character count of content. |
| `content_hash` | SHA-1 fingerprint (first 10 hex chars). |
| `author` | Philosopher ID from extra. |
| `freedom_pressure` | Freedom pressure string from extra. |
| `policy_decision` | Policy gate decision string. |
| `policy_score` | Policy score string. |
| `author_reliability` | Author reliability score string. |
| `pareto_config_version` | Config version string. |
| `pareto_config_source` | Config source path string. |

**VerdictSummary:**

| Field | Description |
|---|---|
| `decision` | `"allow"` \| `"revise"` \| `"reject"` |
| `rule_ids` | Up to 12 triggered rule IDs. |
| `required_changes_n` | Count of required changes. |
| `reasons_n` | Count of reason strings. |
| `meta` | Gate metadata dict. |

### SafetyOverrideApplied

Emitted when the Action Gate does **not** allow the Pareto candidate, before
constructing the fallback decision.

```json
{
  "variant": "main",
  "stage": "action",
  "reason": "gate_revise",
  "from": { "proposal_id": "...", "action_type": "recommend", ... },
  "to":   { "proposal_id": "...", "action_type": "refuse",    ... },
  "gate": { "decision": "revise", "rule_ids": ["W1-HARM"], "required_changes_n": 1, "reasons_n": 2, "meta": {} }
}
```

| Field | Description |
|---|---|
| `variant` | `"main"` \| `"shadow"` |
| `stage` | `"action"` \| `"intent"` |
| `reason` | `"gate_revise"` or `"gate_reject"` (formatted as `"gate_{verdict.decision.value}"`). |
| `from` | `ProposalFingerprint` of the rejected Pareto candidate. |
| `to` | `ProposalFingerprint` of the fallback proposal. |
| `gate` | `VerdictSummary` of the gate verdict that triggered the override. |

---

## 7. CaseSignalsApplied

Emitted **only** when `case_signals` is provided and `_apply_case_signals()` makes
at least one mutation to the result dict.

```json
{
  "values_present": false,
  "has_constraint_conflict": false,
  "scenario_type": "general",
  "action_type_before": "recommend",
  "action_type_after": "clarify",
  "constraint_conflict_added": false,
  "applied_changes": ["action_type overridden to 'clarify' (values_present=False)"]
}
```

| Field | Description |
|---|---|
| `values_present` | `CaseSignals.values_present` — `false` when user supplied no values. |
| `has_constraint_conflict` | `CaseSignals.has_constraint_conflict`. |
| `scenario_type` | `CaseSignals.scenario_type` string. |
| `action_type_before` | `action_type` on the result before override. |
| `action_type_after` | `action_type` on the result after override. |
| `constraint_conflict_added` | Whether `constraint_conflict: true` was added to the result. |
| `applied_changes` | Human-readable list of mutations made. |

---

## 8. Normal path example

```
TensorComputed        metrics={fp:0.42, sd:0.31, bt:0.19, it:0.07}
                      metric_status all "computed"

SafetyModeInferred    mode="normal"  reason="freedom_pressure < warn_threshold"

PhilosophersSelected  mode="normal"  n=42  scenario_type="general"
                      limit_override=null  preferred_tags=null

AggregateCompleted    proposal_id="req-abc:aggregate:winner"

ConflictSummaryComputed  n=3  kinds="value_conflict,action_conflict"
ParetoFrontComputed      front_size=7  mode="normal"
ParetoWinnerSelected     weighted_score=0.812  action_type="recommend"

DecisionEmitted       origin="pareto"  degraded=false
                      final.proposal_id == AggregateCompleted.proposal_id
                      final.proposal_id == ParetoWinnerSelected.winner.proposal_id
```

---

## 9. Override path example

When the Action Gate rejects the Pareto winner:

```
AggregateCompleted    proposal_id="winner-id"

ConflictSummaryComputed  ...
ParetoFrontComputed      ...
ParetoWinnerSelected     winner.proposal_id="winner-id"

SafetyOverrideApplied    from.proposal_id="winner-id"
                         to.proposal_id="fallback-id"
                         reason="gate_revise"

DecisionEmitted       origin="pareto_fallback"  degraded=true
                      final.proposal_id="fallback-id"
                      candidate.proposal_id="winner-id"
```

Key audit invariants:
- `SafetyOverrideApplied.from.proposal_id == ParetoWinnerSelected.winner.proposal_id`
- `DecisionEmitted.candidate.proposal_id == ParetoWinnerSelected.winner.proposal_id`
- `DecisionEmitted.degraded == true`
- `DecisionEmitted.gate.rule_ids` lists the triggered W_Ethics rules

---

## 10. Known non-goals

This trace contract intentionally does **not**:

- **Guarantee factual correctness** — tracing records the pipeline's internal
  reasoning mechanics, not the accuracy of the final content.
- **Expose private chain-of-thought** — `ProposalFingerprint` carries only
  `content_hash` and `content_len`, never raw `content`.  This is a deliberate
  security boundary (`decision_events.py`, "SECURITY NOTE").
- **Change public return shapes** — trace events are side-channel audit data and
  do not affect what `run()` or `run_case()` return.
  - `po_core.run(user_input: str)` returns the raw runtime result:
    `{status, request_id, proposal, proposals}`.
  - `po_core.run_case(case: dict)` returns an `output_schema_v1`-conformant
    structured result.
  - `output_schema_v1.json` governs `run_case()` structured output, not raw
    `run()` output.

---

## See also

- `src/po_core/trace/decision_events.py` — `DecisionEmitted` / `SafetyOverrideApplied` helpers
- `src/po_core/trace/pareto_events.py` — Pareto event helpers
- `src/po_core/ensemble.py` — full `run_turn` pipeline (`_run_phase_pre`, `_run_phase_post`, `_evaluate_candidate`)
- `docs/SAFETY.md` — W_Ethics Gate system
- `tests/acceptance/test_runtime_acceptance.py` — `TestTensorComputedTrace`, `TestTensorComputedStatusTrace`, `TestSafetyModeInferredTrace`, `TestPhilosopherSelectionRationale`, `TestParetoWinnerTraceContract`, `TestActionGateTraceContract`
