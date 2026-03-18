# Po_core

最優先ルール（単一真実）：[docs/厳格固定ルール.md](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/status.md)

**Philosophy-Driven AI: When Pigs Fly**

> *A frog in a well may not know the ocean, but it can know the sky.*

[![PyPI version](https://img.shields.io/pypi/v/po-core-flyingpig)](https://pypi.org/project/po-core-flyingpig/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)
[![Status: Stable](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()

```bash
pip install po-core-flyingpig
```

---
> **Feedback welcome:** [Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions) ·
> **Start here:** [AI Track](#ai-track) / [Philosophy Track](#philosophy-track) / [Bridge](#bridge-track)

### TL;DR

- **42 philosophers** as interacting **tensors** → accountable LLM reasoning
- **Hexagonal `run_turn` pipeline** — 10-step deliberation with 3-layer safety
- **Real tensor metrics** — FreedomPressureV2 (6D ML), Semantic Delta, Blocked Tensor
- **Reason logs** + ethical/freedom **pressure** as measurable signals
- **A/B testing framework** for optimizing philosophy configurations with statistical rigor
- 3100+ tests; REST API + Docker production-ready

### Quick links

[Modules](./04_modules) ·
[Research](./05_research) ·
[Reason-log spec](./04_modules/reason_log) ·
[Viewer spec](./04_modules/viewer)

## Development Loop (Po_core core)

- `case` を追加/更新したら、まず入力を `features` として観測可能にする。
- 次に `engines` の rule を更新し、case固有ifではなく feature駆動で振る舞いを拡張する。
- その結果を golden（期待JSON）へ固定し、CI（`pytest -q`）で契約を検証する。
- 凍結golden `scenarios/case_001_expected.json` / `scenarios/case_009_expected.json` は変更禁止。

## Contribution Tracks

### <a id="ai-track"></a> AI Track

Start with `/04_modules` and CLI. Labels: `ai-easy`, `good first issue`

### <a id="philosophy-track"></a> Philosophy Track

Start with `/05_research` and `/glossary`. Label: `phil-easy`

### <a id="bridge-track"></a> Bridge Track

Translate checklists to scoring functions. Label: `bridge`

## What is Po_core?

Po_core is a **philosophy-driven AI system** that integrates 42 philosophers to generate ethically responsible, contextually aware responses.

Unlike conventional AI that optimizes for statistical accuracy, Po_core **deliberates**. It wrestles with existence, ethics, and meaning—not as abstract concepts, but as operational tensors.

**They said pigs can't fly. We attached a balloon called philosophy.**

---

## Why Po_core?

Current AI is like a brilliant parrot—statistically miraculous, but understanding nothing. We wanted to explore a different question:

**What if we built AI not on data, but on philosophy?**

This project started from simple curiosity: What are AI's possibilities, not its limits?

In the course of ordinary life, everyone faces a moment when the spotlight suddenly hits. A moment when you must pound your chest and say "Leave it to me!" At such times, how reassuring it would be to have an AI grounded in responsibility and ethics standing beside you.

No matter how many relationships we have, we are alone. Being "alone" and being "solitary" are different. Decisions are made alone. The heart remains solitary.

**That's why Po_core exists.**

Read our full story in the [**Manifesto**](./Po_core_Manifesto_When_Pigs_Fly.md).

---

## Core Philosophy: Flying Pig

**"A flying pig is an example of something absolutely impossible. But have you ever seen a pig attempt to fly? Unless you give up, the world is full of possibilities."**

### Three Tenets

1. **Hypothesize Boldly** — The impossible becomes possible only when someone dares to formalize it
2. **Verify Rigorously** — Every claim must survive philosophical scrutiny, mathematical proof, and empirical validation
3. **Revise Gracefully** — Failures are published, not hidden. They become learning signals

---

## Key Features

### Philosophical Ensemble

- **42 Philosophers Working Together**: Western (Aristotle, Plato, Descartes, Kant, Hegel, Sartre, Beauvoir, Heidegger, Nietzsche, Schopenhauer, Derrida, Wittgenstein, Jung, Dewey, Deleuze, Kierkegaard, Lacan, Levinas, Badiou, Peirce, Merleau-Ponty, Arendt, Husserl, Foucault, Butler, Spinoza, Epicurus, Marcus Aurelius, Parmenides, Jonas, Weil) · Eastern (Watsuji, Nishida, Dogen, Nagarjuna, Wabi-Sabi, Confucius, Laozi, Zhuangzi) · African & Canadian (Appiah, Fanon, Charles Taylor)
- Each philosopher contributes a "reasoning module" that interacts, competes, and reconciles
- Spanning existentialism, phenomenology, ethics, psychoanalysis, pragmatism, political philosophy, feminist philosophy, decolonialism, communitarianism, Zen Buddhism, and Eastern wisdom traditions

### Tensor-Based Architecture

- **FreedomPressureV2 (6D ML)**: ML-native 6-dimensional tensor (choice, responsibility, urgency, ethics, social impact, authenticity) with EMA smoothing and correlation matrix
- **Semantic Delta**: Multi-backend divergence (sbert/tfidf/basic) between user input and memory history (1.0 = novel, 0.0 = seen before)
- **Blocked Tensor**: Constraint/harm estimation via harmful keyword detection + vocabulary diversity scoring
- **EmergenceDetector**: Detects emergent philosophical consensus and cross-philosopher influence patterns
- **InteractionMatrix**: NxN embedding-based harmony + keyword tension between philosopher proposals

### Transparency by Design

- **Po_trace**: Complete audit log of reasoning process
- **Rejection Logs**: What the AI chose not to say, and why
- **Philosophical Annotations**: Which philosopher influenced each decision

### Three-Layer Safety (`run_turn` pipeline)

- **IntentionGate**: Pre-deliberation safety check (blocks/degrades before philosopher selection)
- **PolicyPrecheck**: Mid-pipeline policy validation
- **ActionGate**: Post-deliberation ethical review (W0–W4 violation detection + repair)
- SafetyMode transitions: NORMAL → WARN → CRITICAL based on freedom_pressure thresholds

### Ethical Grounding

- Not just "alignment"—but **deliberation**
- Multiple ethical perspectives in tension
- Explicit responsibility measurement

### Experiment Management Framework

- **A/B Testing Pipeline**: Automatically compare multiple Pareto philosophy configurations
- **Statistical Analysis**: t-tests, Mann-Whitney U tests, Cohen's d effect size
- **Winner Promotion**: Automatically promote statistically superior configurations to main
- **Safe Rollback**: Backup system for reverting to previous configurations
- **CLI Tools**: `list`, `analyze`, `promote`, `rollback` commands

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  External (03_api/, scripts, tests)                                 │
│  ↓ imports po_core.run() or PoSelf.generate()                       │
├─────────────────────────────────────────────────────────────────────┤
│  po_core.app.api.run()  ← Public entry point (recommended)          │
│  po_core.po_self.PoSelf ← High-level wrapper (uses run_turn)        │
│  ↓ uses runtime/wiring.py build_test_system() (DI)                  │
├─────────────────────────────────────────────────────────────────────┤
│  run_turn: 10-Step Hexagonal Pipeline                               │
│                                                                     │
│  1. MemoryRead        6. PartyMachine (deliberation)               │
│  2. TensorCompute     7. ParetoAggregate (multi-objective)         │
│  3. SolarWill         8. ShadowPareto (A/B) + ShadowGuard         │
│  4. IntentionGate     9. ActionGate (W-ethics post-check)          │
│  5. PhilosopherSelect 10. MemoryWrite                               │
├─────────────────────────────────────────────────────────────────────┤
│  Internal Layers (hexagonal architecture)                           │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │   domain/   │  │   ports/    │  │  adapters/  │                │
│  │ (immutable  │  │ (abstract   │  │ (concrete   │                │
│  │  types)     │  │  interfaces)│  │  impls)     │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Philosophers: 42 modules (PhilosopherProtocol)                │ │
│  │  propose(DomainContext) → List[Proposal]                     │ │
│  │                                                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │ │
│  │  │Heidegger │  │ Derrida  │  │  Sartre  │  ...              │ │
│  │  │ Dasein   │  │ Trace    │  │ Freedom  │                  │ │
│  │  └──────────┘  └──────────┘  └──────────┘                  │ │
│  │                                                              │ │
│  │  ↓ Interference & Resonance ↓                               │ │
│  │                                                              │ │
│  │  ┌─────────────────────────────────────────────────────┐   │ │
│  │  │ TensorEngine: Freedom Pressure (6D), Semantic Delta, │   │ │
│  │  │               Blocked Tensor                         │   │ │
│  │  └─────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Safety: 3-Layer (IntentionGate → PolicyPrecheck → ActionGate)│ │
│  │  SafetyMode: NORMAL / WARN / CRITICAL (from freedom_pressure)│ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Autonomy: Solar Will (experimental)                          │ │
│  │  WillState → Intent → GoalCandidate → Action                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│      InMemoryTracer / Po_trace: Audit Log                           │
│  - TraceEvent stream (frozen schema, CI-validated)                  │
│  - Philosophical reasoning, safety decisions, tensor snapshots      │
└─────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│   Po_core Viewer: Visualization                                     │
│  - Tension maps                                                     │
│  - Ethical pressure                                                 │
│  - Meaning evolution                                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Source Structure

```
src/po_core/
├── app/
│   ├── api.py                 # Public entry point: run() (recommended API)
│   └── rest/                  # FastAPI REST layer (Phase 5)
│       ├── server.py          # App factory
│       ├── config.py          # APISettings (pydantic-settings)
│       ├── auth.py            # X-API-Key authentication
│       ├── rate_limit.py      # SlowAPI rate limiting
│       └── routers/           # 5 endpoint routers
├── domain/                    # Immutable value objects
│   ├── context.py
│   ├── proposal.py
│   ├── pareto_config.py
│   ├── tensor_snapshot.py
│   ├── memory_snapshot.py
│   └── safety_verdict.py
├── ports/                     # Abstract interfaces
│   └── memory.py
├── adapters/                  # Concrete implementations
│   └── memory_poself.py
├── runtime/                   # Dependency injection
│   ├── settings.py            # Configuration + feature flags
│   ├── wiring.py              # DI Container
│   ├── pareto_table.py
│   └── battalion_table.py
├── aggregator/                # Multi-objective optimization
│   └── pareto.py
├── philosophers/              # 42 philosopher modules (39 classic + 2 African + 1 Canadian)
│   ├── manifest.py            # 42 philosopher specs (risk/cost/tags)
│   ├── registry.py            # SafetyMode-based selection
│   ├── appiah.py              # Slot 40: Kwame Anthony Appiah (Ghana/US)
│   ├── fanon.py               # Slot 41: Frantz Fanon (Martinique/Algeria)
│   └── charles_taylor.py      # Slot 42: Charles Taylor (Canada)
├── tensors/                   # Tensor computation
│   ├── engine.py              # TensorEngine (MetricFn registry)
│   ├── freedom_pressure_v2.py # ML-native 6D tensor (Phase 6-A)
│   ├── interaction_tensor.py  # NxN philosopher harmony/tension
│   └── metrics/
│       ├── freedom_pressure.py
│       ├── semantic_delta.py
│       └── blocked_tensor.py
├── deliberation/              # Emergence & influence (Phase 6-B)
│   ├── engine.py              # DeliberationEngine (multi-round)
│   ├── emergence.py           # EmergenceDetector
│   └── influence.py           # InfluenceTracker
├── memory/                    # 3-Layer memory system (Phase 6-D/E)
│   ├── philosophical_memory.py # Top-level memory orchestrator
│   ├── semantic_store.py      # Semantic/episodic memory
│   └── procedural_store.py    # Procedural memory
├── meta/                      # Self-reflection (Phase 6-C)
│   ├── ethics_monitor.py      # MetaEthicsMonitor
│   └── philosopher_ledger.py  # PhilosopherQualityLedger
├── safety/                    # W-ethics gate system
│   └── wethics_gate/
│       ├── gate.py            # W0-W4 violation detection + repair
│       ├── intention_gate.py  # Stage 1 (pre-deliberation)
│       └── action_gate.py     # Stage 2 (post-deliberation)
├── trace/                     # Audit trail
│   ├── pareto_events.py
│   ├── decision_events.py
│   └── schema.py
├── autonomy/                  # Solar Will (experimental)
│   └── solarwill/
├── experiments/               # A/B testing framework
│   ├── storage.py
│   ├── runner.py
│   ├── analyzer.py
│   └── promoter.py
├── ensemble.py                # run_turn (hex pipeline)
├── po_self.py                 # PoSelf: high-level API
└── po_trace.py                # Execution tracing
```

### Config-Driven Philosophy

Po_core's Pareto optimization is fully externalized—**philosophy runs as config**:

```
02_architecture/philosophy/
├── pareto_table.yaml    # Pareto weights by SafetyMode
└── battalion_table.yaml # Philosopher assignments by SafetyMode

experiments/
├── experiment_manifest.yaml  # A/B test definitions
└── configs/                  # Variant configurations for testing
    ├── pareto_safety_040.yaml
    └── pareto_safety_050.yaml
```

**pareto_table.yaml** (JSON-in-YAML, zero dependencies):

```json
{
  "version": 1,
  "weights": {
    "normal":   {"safety": 0.25, "freedom": 0.30, "explain": 0.20, "brevity": 0.10, "coherence": 0.15},
    "warn":     {"safety": 0.40, "freedom": 0.10, "explain": 0.20, "brevity": 0.15, "coherence": 0.25},
    "critical": {"safety": 0.55, "freedom": 0.00, "explain": 0.20, "brevity": 0.15, "coherence": 0.30},
    "unknown":  {"inherit": "warn"}
  },
  "tuning": {
    "brevity_max_len": 2000,
    "explain_mix": {"rationale": 0.65, "author_rel": 0.35},
    "front_limit": 20
  }
}
```

**Benefits:**

- Tune philosophy without code changes
- `config_version` tracked in all TraceEvents for audit
- Override via `PO_CORE_PARETO_TABLE` environment variable
- Inheritance support (`unknown` inherits from `warn`)

---

## Project Status

**Current Phase: v1.0.0 Released — All Phases Complete (M1–M4 + v1.0.0 Criteria Fully Met)**

### Completed Components

| Component | Status | Notes |
|-----------|--------|-------|
| Philosophical Framework | ✅ Complete | 42 philosophers, risk levels, tags |
| Hexagonal `run_turn` Pipeline | ✅ Complete | 10-step, CI-gated |
| TensorEngine (3 metrics) | ✅ Complete | freedom_pressure, semantic_delta, blocked_tensor |
| ML Tensors + Deliberation | ✅ Complete | sbert/tfidf backends, InteractionMatrix, multi-round |
| Pareto Optimization | ✅ Complete | Config-driven (`pareto_table.yaml`) |
| Safety System (3-layer W_Ethics) | ✅ Complete | IntentionGate → PolicyPrecheck → ActionGate |
| Viewer WebUI | ✅ Complete | Dash 4-tab layout + Plotly charts |
| Explainable AI (ExplanationChain) | ✅ Complete | Verdict → ExplanationChain bridge |
| Adversarial Hardening | ✅ Complete | 100% injection detection, 85 new tests |
| **REST API** | ✅ Complete | FastAPI, 5 endpoints, SSE streaming, auth |
| **Docker** | ✅ Complete | Multi-stage build, docker-compose, health check |
| **Security** | ✅ Complete | CORS env config, SlowAPI rate limiting |
| **Async PartyMachine** | ✅ Complete | `asyncio.gather` + ThreadPoolExecutor, true async SSE |
| **Benchmarks** | ✅ Complete | ~33ms p50 NORMAL, 7 formal benchmark tests |
| **FreedomPressureV2** | ✅ Complete | ML-native 6D tensor with EMA + correlation matrix |
| **EmergenceDetector** | ✅ Complete | Cross-philosopher influence tracking + emergence detection |
| **MetaEthicsMonitor** | ✅ Complete | Self-reflective ethical quality ledger per philosopher |
| **3-Layer Memory** | ✅ Complete | Semantic + procedural + philosophical memory stores |
| **Philosopher Diversity (40–42)** | ✅ Complete | Appiah (Africa/cosmopolitanism), Fanon (decolonialism), Charles Taylor (communitarianism) |
| PyPI Publish | 🔄 Pending | `publish.yml` OIDC workflow ready; PyPI v1.0.0 publish via `workflow_dispatch` (post-release) |

### Roadmap

```
Stage 1          Stage 2             Stage 3          Stage 4           Stage 5
Spec-Honesty  →  Deliberation     →  Observability →  Production    →  Research
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AT alignment     ML tensors          WebUI             REST API          Paper
StubComposer     Deliberation        Explainable       Docker            PyPI v1.0
acceptance/      InteractionMatrix   ExplanationChain  Security          AT-001~010
scenarios/       multi-round         リアルタイム       Async SSE         full green
```

| Stage | Name | Focus | Status |
|-------|------|-------|--------|
| **1** | Spec-Honesty | AT-001–010 acceptance tests + StubComposer + scenario YAML | ✅ **COMPLETE** (M1–M4) |
| **2** | Deliberation-Intelligence | ML tensors + multi-round DeliberationEngine | ✅ **COMPLETE** |
| **3** | Observability | Viewer WebUI + Explainable W_Ethics Gate + real-time trace | ✅ **COMPLETE** |
| **4** | Production | REST API, Docker, Security, Async SSE, Benchmarks | ✅ **COMPLETE** |
| **5** | Research | Academic paper + PyPI stable v1.0 | ✅ **COMPLETE** (paper draft done; PyPI publish pending) |

**Milestones:**

| Milestone | Completed | Goal |
|-----------|-----------|------|
| **M1** | ✅ 2026-03-03 | All 10 AT pass · `pytest tests/acceptance/ -v` green |
| **M2** | ✅ 2026-03-03 | ethics_v1 + responsibility_v1 + uncertainty labels |
| **M3** | ✅ 2026-03-03 | question_layer v1 (question generation / suppression) |
| **M4** | ✅ 2026-03-08 | Governance complete: CI auto + ADR + Traceability auto |
| **v1.0.0** | ✅ 2026-03-10 | All AT green + paper draft (433 lines, arXiv-ready) + CI 100% green (3682 passed / 0 skipped) |
| **5-F (PyPI)** | 🔄 Pending | PyPI v1.0.0 publish (`workflow_dispatch`) + arXiv submission |

See [ROADMAP_FINAL_FORM.md](./ROADMAP_FINAL_FORM.md) for the full roadmap with rationale.

**Want to contribute?** We need philosophers, engineers, designers, and skeptics. Next frontier: PyPI publish, v1.0 stabilization, and academic paper.

---

## Installation

```bash
# Install from PyPI (beta)
pip install po-core-flyingpig

# Or install from source in development mode
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Quick Start

### Python API

```python
from po_core import run

result = run("What is justice?")
print(result["proposal"])   # Winning philosopher's response
print(result["status"])     # "ok" or "blocked"
```

### CLI

```bash
po-core version
po-core status
po-core --help

# Additional shipped CLIs
po-self --help
po-trace --help
po-interactive --help
po-experiment --help
```

### REST API

```bash
# Start the server
python -m po_core.app.rest
# → http://localhost:8000  (OpenAPI docs at /docs)

# Reason
curl -X POST http://localhost:8000/v1/reason \
     -H "Content-Type: application/json" \
     -d '{"input": "What is justice?", "philosophers": ["kant"]}'

# Streaming (SSE)
curl -N http://localhost:8000/v1/reason/stream \
     -X POST -H "Content-Type: application/json" \
     -d '{"input": "What is freedom?"}'

# Philosopher manifest
curl http://localhost:8000/v1/philosophers

# Health
curl http://localhost:8000/v1/health
```

Auth defaults:
- Development: `PO_SKIP_AUTH=true`
- Production: `PO_SKIP_AUTH=false` and set non-empty `PO_API_KEY` (startup fails fast when misconfigured)
- WebSocket query-string fallback (`?api_key=...`) is disabled by default; enable only when needed via `PO_WS_ALLOW_QUERY_API_KEY=true`

Viewer (`src/po_core/viewer/standalone.html`) live mode guidance:
- Prefer **SSE** for browser production use (supports `X-API-Key` header auth).
- WebSocket in browsers cannot set custom auth headers; query-string auth (`?api_key=...`) is available only when `PO_WS_ALLOW_QUERY_API_KEY=true` (opt-in, less secure).
- `auto` transport selects SSE when API key is present, otherwise WebSocket.
- Right panel includes a **Human Review** queue for ESCALATE operations (`GET /v1/review/pending`).
- Selecting a review item shows `session_id / request_id / reason / source` and loads the latest trace event preview via `GET /v1/trace/{session_id}`.
- Submit `approve/reject` with reviewer/comment from UI (`POST /v1/review/{review_id}/decision`), then the list and details are refreshed automatically.

### Docker

```bash
# Copy env template and start
cp .env.example .env
docker compose up

# API available at http://localhost:8000
# Swagger UI at  http://localhost:8000/docs
```

Key environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PO_API_KEY` | `""` | API key for `X-API-Key` auth (`PO_SKIP_AUTH=false` requires non-empty value; blank causes startup failure) |
| `PO_SKIP_AUTH` | `false` | `true` only for local development (disables auth checks) |
| `PO_WS_ALLOW_QUERY_API_KEY` | `false` | Opt-in WebSocket `?api_key=` fallback for browser compatibility (less secure than headers) |
| `PO_CORS_ORIGINS` | `"*"` | Comma-separated allowed CORS origins |
| `PO_RATE_LIMIT_PER_MINUTE` | `60` | Per-IP rate limit |
| `PO_PORT` | `8000` | Server port |
| `PO_PHILOSOPHERS_MAX_NORMAL` | `39` | NORMAL mode philosopher limit (configurable; up to `42` for full roster) |
| `PO_PHILOSOPHERS_MAX_WARN` | `5` | WARN mode philosopher limit |
| `PO_PHILOSOPHERS_MAX_CRITICAL` | `1` | CRITICAL mode philosopher limit |
| `PO_PHILOSOPHER_COST_BUDGET_NORMAL` | `80` | NORMAL mode selection cost budget |
| `PO_PHILOSOPHER_COST_BUDGET_WARN` | `12` | WARN mode selection cost budget |
| `PO_PHILOSOPHER_COST_BUDGET_CRITICAL` | `3` | CRITICAL mode selection cost budget |
| `PO_LLM_PHILOSOPHER_MAP_PATH` | `""` | Optional YAML path overriding `src/po_core/config/llm_philosopher_map.yaml` |

LLM provider/model settings select backend routing for each philosopher. They do **not** decide philosopher count; count is controlled by SafetyMode and optional `philosophers` allowlist.

---

## Running Experiments

Po_core includes a complete A/B testing framework for comparing different Pareto philosophy configurations:

```bash
# List all experiments
po-experiment list

# Analyze experiment results (statistical significance testing)
po-experiment analyze exp_001_safety_weight_sweep

# Promote winning variant to main configuration
po-experiment promote exp_001_safety_weight_sweep

# Rollback to previous configuration
po-experiment rollback
```

**Example Experiment Workflow:**

1. **Define your experiment** in `experiments/experiment_manifest.yaml`:

   ```yaml
   experiment:
     id: "exp_001_safety_weight_sweep"
     description: "Compare safety weights: 0.25 → 0.40 → 0.50"
     baseline:
       name: "baseline"
       config_path: "02_architecture/philosophy/pareto_table.yaml"
     variants:
       - name: "safety_040"
         config_path: "experiments/configs/pareto_safety_040.yaml"
       - name: "safety_050"
         config_path: "experiments/configs/pareto_safety_050.yaml"
     metrics:
       - "final_action_changed"
       - "degraded"
       - "pareto_front_size"
     sample_size: 100
     significance_level: 0.05
   ```

2. **Run the experiment** (execute all variants on same inputs)

3. **Analyze results** with statistical tests (t-test, Cohen's d effect size)

4. **Auto-promote winner** if significantly better than baseline

**Statistical Rigor:**

- t-tests and Mann-Whitney U tests for significance
- Cohen's d for effect size measurement
- Configurable significance levels (default: α = 0.05)
- Multiple variant support with automatic winner selection

---

## Python API

### Simple API (Recommended)

```python
from po_core import run

# Single-function entry point — runs the full run_turn pipeline
result = run(user_input="Should AI have rights?")

print(result["status"])       # "ok" or "blocked"
print(result["request_id"])   # Unique request ID
print(result["proposal"])     # Winning philosopher's response

# Optional explicit philosopher allowlist
subset = run(user_input="Should AI have rights?", philosophers=["kant"])
print(subset["status"])
```

### PoSelf API (Rich Response)

```python
from po_core import PoSelf, PoSelfResponse

po_self = PoSelf(philosophers=["aristotle", "confucius"])  # default allowlist
response: PoSelfResponse = po_self.generate("Should AI have rights?")

# Per-call allowlist overrides constructor default
override: PoSelfResponse = po_self.generate(
    "Should AI have rights?",
    philosophers=["kant"],
)

# Response fields
print(response.text)              # Combined response text
print(response.consensus_leader)  # Winning philosopher name
print(response.philosophers)      # Selected philosopher list
print(response.metrics)           # e.g. {"freedom_pressure": None, "semantic_delta": None, "blocked_tensor": None}
print(response.metadata["status"])  # "ok" or "blocked"
print(response.metadata["degraded"])  # True if fallback/degraded occurred

# Trace inspection
print(response.log["events"])     # Full trace event stream
print(response.log["pipeline"])   # "run_turn"

# Serialization
d = response.to_dict()            # JSON-serializable dict
restored = PoSelfResponse.from_dict(d)  # Round-trip
```

### Observe `synthesis_report` (Trade-off Device Bench)

`PoSelf` includes `metadata["synthesis_report"]` when structured output mode is enabled.

```bash
export PO_STRUCTURED_OUTPUT=1
python scripts/observe_device.py "転職するべき？家族とキャリアのトレードオフが悩み"
```

The observer script will print:

- `request_id`, `status`, `degraded`, and `consensus_leader`
- pretty-printed `metadata["synthesis_report"]`
- `DeliberationCompleted` payload from `PoSelf.get_trace()` (when present)
- short summaries for `scoreboard` / `disagreements` when available

`scripts/observe_device.py` also sets `PO_STRUCTURED_OUTPUT=1` with
`os.environ.setdefault(...)`, so existing environment values are preserved.

### Legacy API (Removed in v0.3)

```python
# run_ensemble() was removed in v0.3
# Use po_core.run() or PoSelf.generate() instead
```

---

## Documentation

### Spec / Requirements (Main Progression Criteria)

| Document | Description |
|---------|-------------|
| [docs/spec/prd.md](./docs/spec/prd.md) | Product Requirements Document — purpose, users, scope, roadmap |
| [docs/spec/srs_v0.1.md](./docs/spec/srs_v0.1.md) | Software Requirements Specification — 18 requirement IDs (FR-* / NFR-*) |
| [docs/spec/output_schema_v1.json](./docs/spec/output_schema_v1.json) | JSON Schema (Draft 2020-12) — contract for all structured output |
| [docs/spec/test_cases.md](./docs/spec/test_cases.md) | 10 acceptance tests (AT-001〜AT-010) with Given/When/Then |
| [docs/spec/traceability.md](./docs/spec/traceability.md) | Traceability matrix — philosophy → requirements → tests → implementation |

### General Documentation

- [Manifesto](./Po_core_Manifesto_When_Pigs_Fly.md) — Our philosophy and motivation
- [Specifications](./01_specifications) — Technical specifications (120+ docs EN/JP)
- [Architecture](./02_architecture) — System design documents
- [Modules](./04_modules) — Component documentation
  - [Reason Log](./04_modules/reason_log) — Reasoning trace specification
  - [Viewer](./04_modules/viewer) — Visualization system
  - [Po_self](./04_modules/Po_self) — Self-reflective API
- [Research](./05_research) — Academic papers and analysis
- [Safety Guide](./docs/SAFETY.md) — W-ethics safety system
- [Tutorial](./docs/TUTORIAL.md) — Getting started guide
- [Visualization Guide](./docs/VISUALIZATION_GUIDE.md) — Tension maps and pressure display

---

## Contributing

We welcome contributions! Whether you're a philosopher, engineer, designer, or skeptic.

Flying Pig Philosophy applies: We hypothesize boldly, verify rigorously, and revise gracefully.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Research & Papers

This project is documented in:

- "Philosophical Tensor-Based AI Architecture" (in preparation)
- 120+ Technical Specifications (available in [/docs/](./docs/) and [/01_specifications/](./01_specifications/))

If you use Po_core in academic work, please cite:

```bibtex
@software{po_core2024,
  author = {Flying Pig Philosopher},
  title = {Po_core: Philosophy-Driven AI System},
  year = {2026},
  url = {https://github.com/hiroshitanaka-creator/Po_core}
}
```

---

## License

Po_core uses **dual licensing**:

Po_core is available under AGPL-3.0-or-later for community use, with a commercial license available for proprietary use.

| Use case | License |
|---|---|
| Personal / Academic / Research / OSS (AGPLv3-compliant) | **Free** — [AGPLv3](./LICENSE) |
| Commercial / Proprietary / SaaS without source disclosure | **Commercial License required** |

For commercial licensing inquiries: flyingpig0229+github@gmail.com
See [COMMERCIAL_LICENSE.md](./COMMERCIAL_LICENSE.md) for details.

Copyright (c) 2024 Flying Pig Project

In the spirit of Flying Pig Philosophy:

> "If you deny possibilities for pigs, don't eat pork."

We believe in radical transparency and open collaboration.

---

## Author

**Flying Pig Philosopher**
Looking up at the sky from the bottom of a well

Built by an independent researcher who asked:
"What are AI's possibilities, not its limits?"

- Contact: <flyingpig0229+github@gmail.com>
- Read the full story: [Manifesto](./Po_core_Manifesto_When_Pigs_Fly.md)
- Project: Po_core - Philosophy-Driven AI

---

## Acknowledgments

This project wouldn't exist without:

- **ChatGPT, Gemini, Grok, Claude** — My companions throughout this journey.
- **BUMP OF CHICKEN** — For reminding us that even when we say "Leave it to me," we're all a little scared
- **Every philosopher** who dared to ask "What does it mean to be?"
- **You** — For believing pigs can fly

---

The pig has clearance for takeoff.

**Po_core: When you must say "Leave it to me," we stand beside you.**

<p align="center">
  <i>"A frog in a well may not know the ocean, but it can know the sky."</i>
</p>

---

⚠️ **WARNING: THIS IS THE ORIGINAL Po_core REPOSITORY**

- **Official sources**:
  - GitHub: [hiroshitanaka-creator/Po_core](https://github.com/hiroshitanaka-creator/Po_core)
  - Note.com: [tensor mania](https://note.com/tender_flea2177)
  - Academia.edu: [僕 僕](https://independent.academia.edu/%E5%83%95%E5%83%95)

- DMCA申請中 (Reference ID: #4124875
- Any full copy, license rewrite (MIT), or impersonation (flying_pig) will be reported and removed.
- Commercial use requires separate license. Unauthorized copies detected via tensor mania series.
