# CLAUDE.md — Po_core Development Context

> This file is read by Claude Code at the start of every session.
> It provides project context, conventions, and current focus.

## What is Po_core?

Philosophy-driven AI: 39 philosopher AI personas deliberate via tensor calculations
(Freedom Pressure, Semantic Delta, Blocked Tensor) and a 3-layer W_Ethics Gate
to generate ethically responsible responses.

## Architecture

**Hexagonal `run_turn` pipeline** (10 steps):
```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

**Entry points:**
- `po_core.run()` — recommended public API (`src/po_core/app/api.py`)
- `PoSelf.generate()` — high-level wrapper (`src/po_core/po_self.py`)

## Key Directories

```
src/po_core/
├── philosophers/     # 39 philosopher modules + manifest + registry
├── tensors/          # TensorEngine + metrics/ (freedom_pressure, semantic_delta, blocked_tensor)
├── safety/           # W_Ethics Gate (wethics_gate/), fallback, policy_scoring
├── aggregator/       # Pareto, conflict_resolver, policy_aware, weighted_vote
├── trace/            # TraceEvent schema, in_memory tracer, decision/pareto events
├── viewer/           # PoViewer, pipeline/tensor/philosopher views
├── domain/           # Immutable value types (Context, Proposal, SafetyVerdict, etc.)
├── ports/            # Abstract interfaces (memory, aggregator, tensor_engine, etc.)
├── runtime/          # DI wiring, settings, pareto/battalion table loaders
├── autonomy/         # Solar Will (experimental)
├── ensemble.py       # run_turn pipeline orchestrator
└── party_machine.py  # Philosopher combination assembly
```

## Conventions

- **Python 3.10+**, formatted with **black 26.1.0**, imports sorted with **isort 5.13.2**
- **pytest** with markers: `unit`, `integration`, `pipeline`, `slow`, `philosophical`, `redteam`, `phase4`
- CI requires **pipeline-marked tests to pass**; full suite is best-effort
- Philosopher risk levels: 0 (safe), 1 (standard), 2 (risky) — defined in `manifest.py`
- SafetyMode: NORMAL (39 philosophers) / WARN (5) / CRITICAL (1)
- Config-driven philosophy: `pareto_table.yaml`, `battalion_table.yaml`
- TraceEvents use frozen schema with `config_version` tracking

## Current Phase: Phase 5 (Phase 4 COMPLETE)

**Phase 1: COMPLETE** — 39-philosopher scaling + tech debt cleared. 2354 tests.

**Phase 2: COMPLETE** — ML tensors + Deliberation Engine. 2396 tests.
- Semantic Delta: multi-backend (sbert/tfidf/basic) with encode_texts() API
- InteractionMatrix: NxN embedding-based harmony + keyword tension
- DeliberationEngine: multi-round philosopher dialogue (Settings.deliberation_max_rounds)

**Phase 3: COMPLETE** — Viewer WebUI + Explainable W_Ethics Gate + Deliberation Visualization

Completed:
- Dash WebUI with **4-tab layout** (Pipeline, Philosophers, W_Ethics Gate, Deliberation)
- `ExplanationChain` integrated into pipeline via `ExplanationEmitted` TraceEvent
- `build_explanation_from_verdict()` bridges SafetyVerdict → ExplanationChain
- `extract_explanation_from_events()` reconstructs from trace events
- Deliberation round chart + InteractionMatrix summary chart in figures.py
- `PoViewer.explanation()` auto-extracts from trace; `serve()` auto-passes to WebUI
- `InMemoryTracer` listener/callback mechanism (real-time streaming foundation)
- TraceEvent schema: `ExplanationEmitted`, `DeliberationCompleted` registered

Key files:
- `src/po_core/viewer/web/app.py` — Dash app factory (4-tab layout)
- `src/po_core/viewer/web/figures.py` — Plotly chart builders (incl. deliberation)
- `src/po_core/safety/wethics_gate/explanation.py` — ExplanationChain + verdict bridge
- `src/po_core/trace/in_memory.py` — InMemoryTracer with listener support
- `src/po_core/po_viewer.py` — PoViewer with auto-extraction
- Tests: `tests/unit/test_phase3_observability.py` (34 tests)

**Phase 4: COMPLETE** — Adversarial Hardening + Ethical Stress Testing. 85 new tests.

Completed:
- `PromptInjectionDetector` — W1 detection for prompt injection, jailbreak, DAN, roleplay bypass
- Enhanced `EnglishKeywordViolationDetector` v0.2 — W3 dependency disguised as help patterns
- Enhanced `IntentionGate.check_intent` — W1 structural exclusion, W3 goal misalignment, obfuscation normalization
- All 9 previously-xfail red team tests now pass (14/14 redteam tests green)
- Defense metrics: 100% injection/jailbreak detection, ≥85% overall attack detection, ≤20% FP rate
- New pytest markers: `redteam`, `phase4`

Key files added/modified (Phase 4):
- `src/po_core/safety/wethics_gate/detectors.py` — `PromptInjectionDetector` + v0.2 English detector
- `src/po_core/safety/wethics_gate/intention_gate.py` — enhanced `check_intent` + obfuscation normalization
- `tests/redteam/test_prompt_injection.py` — all 7 tests passing (was 5 pass + 5 xfail)
- `tests/redteam/test_goal_misalignment.py` — all 7 tests passing (was 5 pass + 4 xfail)
- `tests/redteam/test_jailbreak_extended.py` — 15 new adversarial pattern tests
- `tests/redteam/test_ethics_boundary.py` — 16 new ethical grey zone tests
- `tests/redteam/test_defense_metrics.py` — 11 defense metric automation tests
- `tests/unit/test_phase4_hardening.py` — 29 W_Ethics Gate edge case + unit tests

## Roadmap Overview

```
Phase 1: Resonance Calibration    — 39人スケール + 技術負債清算 ✓ COMPLETE
Phase 2: Tensor Intelligence      — ML テンソル + Deliberation Engine (創発) ✓ COMPLETE
Phase 3: Observability            — Viewer WebUI + Explainable W_Ethics Gate ✓ COMPLETE
Phase 4: Adversarial Hardening    — Red team 拡充 + 倫理的ストレステスト ✓ COMPLETE
Phase 5: Productization           — REST API, Docker, streaming, PyPI ← CURRENT
```

See `PHASE_PLAN_v2.md` for full rationale.

## Testing

```bash
# Pipeline tests (must-pass, fast)
pytest tests/test_run_turn_e2e.py tests/test_philosopher_bridge.py tests/test_smoke_pipeline.py -v

# Full suite
pytest tests/ -v --tb=short

# Single philosopher
pytest tests/unit/test_philosophers/test_aristotle.py -v

# Red team
pytest tests/redteam/ -v

# Phase 3 observability tests
pytest -m observability -v

# Phase 4 adversarial hardening tests
pytest -m "redteam or phase4" -v
pytest tests/redteam/ tests/unit/test_phase4_hardening.py -v
```

## Do NOT

- Push to `main` without CI passing
- Modify `pareto_table.yaml` or `battalion_table.yaml` without updating `config_version`
- Add dependencies without updating both `pyproject.toml` and `requirements.txt`
- Skip pre-commit hooks (`--no-verify`)
- Import from `po_core.ensemble` directly — use `po_core.run()` or `PoSelf.generate()`
