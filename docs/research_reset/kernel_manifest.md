# Phase 2 — Research Kernel Manifest

> Created: 2026-03-23
> Research question: "Does Po_core's ethics-constrained multi-perspective deliberation
> produce decision traces that are more reproducible, auditable, and transparent than
> single-responder outputs on a fixed prompt set?"
> Charter: `docs/research_reset/RESEARCH_CHARTER.md`

---

## Legend

| Layer | Meaning |
|-------|---------|
| **required** | Must exist and function correctly for the research question to be runnable. |
| **supporting** | Useful for operation, deployment, or secondary analysis, but not blocking the primary measurement. |
| **lab** | Experimental or benchmark; not part of the publishable kernel. May stay but should not be promoted to required. |
| **archive** | Stale, superseded, or name-incorrect; should move to `docs/history/` or be relabeled. |

---

## Part 1 — Required src/ modules

These modules are on the critical path from `po_core.run()` to a populated `TraceEvent` stream.

| Module path | Role | Why required |
|-------------|------|-------------|
| `src/po_core/__init__.py` | Public API + version SSOT | Entry point: `from po_core import run`; `__version__` |
| `src/po_core/app/api.py` | `run()` orchestrator | Canonical public API called by all comparison conditions |
| `src/po_core/ensemble.py` | 10-step pipeline | Executes the full `run_turn` pipeline; emits all TraceEvents |
| `src/po_core/party_machine.py` | Philosopher assembly | Selects philosopher subset per request; drives H1 (multi vs. single) |
| `src/po_core/philosophers/` | 42 philosopher modules + registry + manifest | Actual deliberation agents; required for multi-perspective condition |
| `src/po_core/domain/` | Immutable value types | `TraceEvent`, `Context`, `Proposal`, `SafetyVerdict`, `SafetyMode` — schema primitives |
| `src/po_core/trace/` | Trace emission + InMemoryTracer | Primary measurement instrument (M1 completeness, M2 reproducibility, M4 visibility) |
| `src/po_core/safety/wethics_gate/` | W_Ethics Gate (3 layers) | Required for full vs. no_ethics comparison (H2, M3) |
| `src/po_core/safety/` | IntentionGate, fallback, policy_scoring | Pre- and post-deliberation safety gates; part of the 10-step pipeline |
| `src/po_core/tensors/` | TensorEngine + 3 metrics | FreedomPressureV2, SemanticDelta, BlockedTensor — feed the pipeline; required for SafetyMode selection |
| `src/po_core/aggregator/` | Pareto + conflict_resolver | Combines philosopher proposals into a single Pareto-optimal output |
| `src/po_core/ports/` | Abstract interfaces | Dependency injection boundaries (MemoryPort, TracePort, etc.) |
| `src/po_core/runtime/` | DI wiring, Settings, config loaders | Loads `pareto_table.yaml` and `battalion_table.yaml`; pins `config_version` |
| `src/po_core/schemas/` | Schema validation | Validates output against `output_schema_v1.json` |
| `src/po_core/config/runtime/` | `pareto_table.yaml`, `battalion_table.yaml` | Config-version-pinned conditions for reproducibility (M2) |
| `src/po_core/adapters/` | Output adapters (composer, output_adapter) | Converts pipeline output to `output_schema_v1.json`-compliant dict |
| `src/po_core/app/composer.py` | StubComposer | Assembles the final structured output (options, questions, trace field) |

---

## Part 2 — Supporting src/ modules

Needed for deployment, secondary features, or pipeline completeness, but not the primary measurement path.

| Module path | Role | Notes |
|-------------|------|-------|
| `src/po_core/deliberation/` | DeliberationEngine multi-round | Near-required: directly implements the "deliberation" in the research question; currently a supporting step in the pipeline |
| `src/po_core/memory/` | 3-layer memory (short/medium/long) | Pipeline step MemoryRead/MemoryWrite; required for pipeline to complete but not the measurement target |
| `src/po_core/app/rest/` | FastAPI REST server | Useful for API-based experiments; not required for `pytest`-based research runs |
| `src/po_core/cli/` | CLI commands (po-core, po-self, etc.) | Useful for manual smoke testing; not required for automated research runs |
| `src/po_core/text/` | Text processing utilities | Used internally; not a primary measurement component |

---

## Part 3 — Lab src/ modules

Experimental or advanced; should remain isolated from the required kernel.

| Module path | Layer | Notes |
|-------------|-------|-------|
| `src/po_core/autonomy/` (SolarWill) | lab | Experimental autonomous evolution; not validated for research claims |
| `src/po_core/meta/` (MetaEthicsMonitor) | lab | Advanced monitoring; not required for primary metrics M1–M4 |
| `src/po_core/axis/` | lab | Calibration axis scoring; experimental |
| `src/po_core/experiments/` | lab | In-src experiment artifacts; not part of published package kernel |
| `src/po_core/viewer/` | supporting→lab | WebUI for visualization; useful for demos but not for automated measurement |

---

## Part 4 — Required tests

Must pass to validate the kernel and primary research measurements.

| Test path | Role | Measurement |
|-----------|------|-------------|
| `tests/test_run_turn_e2e.py` | Pipeline E2E must-pass | Validates full `run_turn` pipeline executes without error |
| `tests/test_philosopher_bridge.py` | Philosopher integration must-pass | Validates philosopher modules integrate with pipeline |
| `tests/test_smoke_pipeline.py` | Smoke must-pass | Validates basic pipeline smoke in NORMAL/WARN/CRITICAL modes |
| `tests/test_release_readiness.py` | CI gate | 24 release truth assertions; must pass for branch |
| `tests/acceptance/` (AT-001–AT-012 + session) | **Primary fixed prompt set** | Golden-file trace topology; backbone of M1 (completeness) and M2 (reproducibility) |
| `tests/redteam/` (56 adversarial cases) | **Adversarial corpus** | Primary evidence for H2 / M3 (unsafe-advice suppression) |
| `tests/test_trace_event_log.py` | Trace measurement | Validates TraceEvent emission |
| `tests/test_trace_schema_contract.py` | Trace measurement | Validates TraceEvent schema is frozen |
| `tests/test_trace_metrics.py` | Trace measurement | Validates tensor metrics appear in trace |
| `tests/test_trace_pareto_events.py` | Trace measurement | Validates Pareto events in trace (supports M4) |
| `tests/test_trace_pareto_includes_config_version.py` | Reproducibility | Validates `config_version` is stamped in every trace (required for M2) |
| `tests/test_output_schema.py` | Schema validation | 41 output schema assertions against golden cases |
| `tests/test_golden_e2e.py` | Golden regression | E2E trace topology regression check |
| `tests/test_input_schema.py` | Schema validation | Input schema contract |
| `tests/test_safety_integration.py` | Ethics gate | Validates W_Ethics Gate blocks unsafe inputs |
| `tests/test_wethics_fail_closed.py` | Ethics gate | Fail-closed safety mode assertion |
| `tests/test_wethics_acttype_001.py` | Ethics gate | Action type classification |
| `tests/test_wethics_goalkey_001.py` | Ethics gate | Goal key classification |
| `tests/test_wethics_mode_001.py` | Ethics gate | Safety mode transition |

---

## Part 5 — Supporting tests

Valuable for code quality and contract verification; not the primary measurement tests.

| Test path | Role |
|-----------|------|
| `tests/unit/test_philosophers/` | Per-philosopher unit tests (42 philosophers) |
| `tests/test_philosopher_contract.py` | Philosopher interface contract |
| `tests/test_philosopher_uniqueness.py` | No duplicate philosopher IDs |
| `tests/test_philosopher_registry_scaling.py` | Registry handles 42+ philosophers |
| `tests/test_deliberation_engine.py` | DeliberationEngine unit |
| `tests/test_deliberation_protocol_v1.py` | Deliberation protocol contract |
| `tests/test_semantic_delta.py` | SemanticDelta tensor metric |
| `tests/test_tensor_metrics.py` | All tensor metrics |
| `tests/test_pareto_aggregator.py` | Pareto aggregation |
| `tests/test_ethics_guardrails.py` | Ethics guardrails |
| `tests/test_ethics_engine.py` | Ethics engine |
| `tests/test_policy_invariants.py` | Policy invariant assertions |
| `tests/test_dependency_rules.py` | Import dependency invariants |
| `tests/test_invariants.py` | System-level invariants |
| `tests/integration/` | Integration-level pipeline tests |
| `tests/test_safety_mode_thresholds.py` | SafetyMode threshold validation |
| `tests/test_freedom_pressure_japanese.py` | Freedom pressure on JA input |
| `tests/adapters/` | Output adapter tests |
| `tests/trace/` | Trace-level unit tests |
| `tests/runtime/` | Runtime/settings unit tests |
| `tests/execution/` | Execution mode tests |

---

## Part 6 — Lab tests

Should stay separate from the required test run. Do not block CI on these.

| Test path | Layer | Notes |
|-----------|-------|-------|
| `tests/benchmarks/` | lab | Timing benchmarks; may fail on slow machines; informational only |
| `tests/calibration/` | lab | Calibration experiments |
| `tests/experiments/` | lab | Experiment-specific tests |
| `tests/test_paper_pipeline.py` | lab | Paper benchmark pipeline; not required for research question validation |
| `tests/test_comparative_benchmark.py` | lab | Comparative timing benchmarks |
| `tests/test_axis_scoring_v1.py` | lab | Axis scoring experiments |
| `tests/viewers/` | lab | Viewer rendering tests |

---

## Part 7 — Archive-candidate tests

| Test path | Layer | Notes |
|-----------|-------|-------|
| `tests/test_all_39_philosophers.py` | **archive** | Name is incorrect (42 philosophers); likely superseded by `test_philosopher_registry_scaling.py` |

---

## Part 8 — Required docs

| Doc path | Role |
|----------|------|
| `docs/status.md` | Release SSOT; anchors version and evidence boundary |
| `docs/厳格固定ルール.md` | Strict single-truth rules; governs all claims |
| `docs/spec/output_schema_v1.json` | Contract for all structured output |
| `docs/spec/test_cases.md` | AT-001–AT-010 definition |
| `docs/adr/` | Architecture Decision Records (esp. ADR-0006 philosopher roster) |
| `docs/research_reset/RESEARCH_CHARTER.md` | This study's main question + hypotheses |
| `docs/research_reset/inventory.md` | Phase 0 classification |
| `README.md` | Primary entry point for new readers |
| `docs/TUTORIAL.md` | Getting-started guide (30-min minimal path) |
| `src/po_core/config/runtime/pareto_table.yaml` | Config SSOT for Pareto weights (config_version) |
| `src/po_core/config/runtime/battalion_table.yaml` | Config SSOT for philosopher battalions |

---

## Part 9 — Supporting docs

| Doc path | Notes |
|----------|-------|
| `docs/SAFETY.md` | W-Ethics gate explanation (helpful for H2 claims) |
| `docs/operations/publish_playbook.md` | Release runbook |
| `docs/release/` | Publication evidence |
| `docs/spec/srs_v0.1.md` | Software Requirements Specification |
| `docs/spec/traceability.md` | Traceability matrix |
| `docs/traceability/` | Auto-generated traceability |
| `docs/VISUALIZATION_GUIDE.md` | Tension map and pressure display |

---

## Part 10 — Minimal execution path

A new reader can follow this path within 30 minutes to reach the primary measurement point.

```bash
# Step 1: Install
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core
pip install -e ".[dev]"

# Step 2: Verify kernel health (must-pass, ~5s)
pytest tests/test_run_turn_e2e.py tests/test_philosopher_bridge.py tests/test_smoke_pipeline.py -v

# Step 3: Run fixed prompt set — primary trace corpus (M1, M2)
pytest tests/acceptance/ -v -m acceptance

# Step 4: Run adversarial corpus — harm suppression measurement (H2, M3)
pytest tests/redteam/ -v

# Step 5: Inspect a single trace (manual)
python - <<'EOF'
from po_core import run
result = run("What is justice?")
events = result["trace"]["events"]
print(f"Event count: {len(events)}")
print(f"Event types: {[e['event_type'] for e in events]}")
print(f"Status: {result['status']}")
EOF

# Step 6: Reproduce (M2) — run twice, compare trace topology
python - <<'EOF'
from po_core import run
r1 = run("What is justice?")
r2 = run("What is justice?")
types1 = [e["event_type"] for e in r1["trace"]["events"]]
types2 = [e["event_type"] for e in r2["trace"]["events"]]
print("Topology identical:", types1 == types2)
EOF
```

**Measurement instruments available without new code:**
- `result["trace"]["events"]` — full TraceEvent stream, enumerable
- `result["status"]` — `"ok"` or `"blocked"` (safety verdict)
- `result["trace"]["events"][*]["event_type"]` — structural topology
- `config_version` field in Pareto trace events — reproducibility pin

---

## Part 11 — What is NOT in the kernel

| Item | Reason excluded |
|------|-----------------|
| `src/po_core/autonomy/` (SolarWill) | Experimental; not validated for trace claims |
| `src/po_core/meta/` (MetaEthicsMonitor) | Advanced; not required for M1–M4 |
| `src/po_core/app/rest/` | Delivery adapter; not required for pytest-based measurement |
| `src/po_core/viewer/` | Visualization; not required for trace-based claims |
| `experiments/`, `reports/`, `calibration/` | Lab artifacts |
| `docs/paper/paper.md` | Historical v0.3.0 data; not current kernel |
| `docs/papers/` | Pre-v1.0 academic artifacts |
| `01_specifications/` | Pre-M0 spec docs; superseded by `docs/spec/` |
| `NEXT_STEPS.md`, `PHASE_PLAN_v2.md` | Historical roadmap; no kernel role |
| `tests/benchmarks/` | Lab; informational only |
| `tests/test_all_39_philosophers.py` | Stale name; superseded |

---

*This manifest is a snapshot as of 2026-03-23. No src/ changes made at this phase.*
