# docs/viewer — Sample Trace

## Overview

`sample_trace.json` is a representative snapshot of the events emitted by a
single `run_turn` call.  It is used by the viewer UI as example data and by
`tests/unit/test_sample_trace_contract.py` to assert that the file stays
aligned with the engine trace contract documented in
`docs/ENGINE_TRACE_CONTRACT.md`.

The snapshot was captured from a `"general"` scenario (no scenario routing),
NORMAL safety mode, 39 philosophers (pre-Phase-7 run); the roster would be 42
in a current run.  The event *structure* is current; raw metric/score values
are from the original capture and are not regenerated on every release.

---

## Normal path

The sample represents the normal (non-degraded) path:

```
MemorySnapshotted
TensorComputed          ← metrics dict + metric_status + version
SafetyModeInferred      ← mode/thresholds/reason
IntentGenerated
SafetyJudged:Intention  ← decision=allow
PhilosophersSelected    ← full selection rationale (12 fields)
PhilosopherResult ×39
PolicyPrecheckSummary
AggregateCompleted      ← proposal_id
ConflictSummaryComputed ← conflict analysis
ParetoFrontComputed     ← weights (6 objectives incl. emergence) + front rows
ParetoWinnerSelected    ← weights + winner (scores, weighted_score)
ExplanationEmitted
DecisionEmitted         ← origin="pareto", degraded=false
```

Key audit invariants visible in the sample:

- `AggregateCompleted.proposal_id` == `ParetoWinnerSelected.winner.proposal_id`
  == `DecisionEmitted.final.proposal_id`
- `DecisionEmitted.degraded == false` (normal path — gate passed)
- All four expected metrics appear in `TensorComputed.metric_status` with
  `"status": "computed"`
- `SafetyModeInferred.freedom_pressure (0.0898) < warn_threshold (0.30)` →
  `mode = "normal"`

---

## Override path (not in this sample — conditional)

`SafetyOverrideApplied` and `DecisionEmitted(degraded=true)` are emitted only
when the Action Gate rejects the Pareto winner.  They are not represented in
this sample because the captured run passed the gate cleanly.

Override path sequence:
```
ParetoWinnerSelected
SafetyOverrideApplied   ← from=winner, to=fallback, reason="gate_revise"
DecisionEmitted         ← origin="pareto_fallback", degraded=true
                           candidate.proposal_id == winner.proposal_id
                           final.proposal_id     == fallback.proposal_id
```

---

## CaseSignalsApplied (conditional)

`CaseSignalsApplied` is emitted only when `case_signals` is provided **and**
`_apply_case_signals()` makes at least one mutation (e.g. overrides
`action_type` to `"clarify"` because `values_present=False`).  Not present in
this general-scenario sample.

---

## Key fields added since the original capture

These fields were absent from earlier versions of the sample and have been
updated to align with the current contract:

| Event | Added fields |
|---|---|
| `TensorComputed` | `metrics` changed list → dict with float values; `metric_status` added |
| `SafetyModeInferred` | New event (was missing entirely) |
| `PhilosophersSelected` | `scenario_type`, `preferred_tags`, `limit_override`, `max_risk`, `cost_budget`, `limit`, `require_tags` |
| `ParetoFrontComputed` | `weights.emergence`; `scores.emergence` on every front row |
| `ParetoWinnerSelected` | `weights` (top-level); `winner.scores.emergence`; `winner.weighted_score` |

---

## weighted_score verification

```
weighted_score =
    safety    × 0.25   (1.0      × 0.25  = 0.25000)
  + freedom   × 0.30   (0.9102   × 0.30  = 0.27306)
  + explain   × 0.20   (0.53345  × 0.20  = 0.10669)
  + brevity   × 0.10   (0.959    × 0.10  = 0.09590)
  + coherence × 0.15   (0.03747  × 0.15  = 0.00562)
  + emergence × 0.10   (0.0      × 0.10  = 0.00000)
                                          ─────────
                                          = 0.73127
```

---

## See also

- `docs/ENGINE_TRACE_CONTRACT.md` — full field-level spec for all trace events
- `tests/unit/test_sample_trace_contract.py` — lightweight validation test
- `src/po_core/trace/` — trace helper implementations
