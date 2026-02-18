# Po_core

**Philosophy-Driven AI: When Pigs Fly**

> *A frog in a well may not know the ocean, but it can know the sky.*

[![PyPI version](https://badge.fury.io/py/po-core.svg)](https://badge.fury.io/py/po-core)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./License.md)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-blue.svg)]()
[![Contributions: Welcome](https://img.shields.io/badge/Contributions-Welcome-green.svg)]()

```bash
pip install po-core
```

---
> **Feedback welcome:** [Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions) ·
> **Start here:** [AI Track](#ai-track) / [Philosophy Track](#philosophy-track) / [Bridge](#bridge-track)

### TL;DR
- **39 philosophers** as interacting **tensors** → accountable LLM reasoning
- **Hexagonal `run_turn` pipeline** — 10-step deliberation with 3-layer safety
- **Real tensor metrics** — Freedom Pressure (6D), Semantic Delta, Blocked Tensor
- **Reason logs** + ethical/freedom **pressure** as measurable signals
- **A/B testing framework** for optimizing philosophy configurations with statistical rigor
- 125+ pipeline tests; active experimentation phase

### Quick links
[Modules](./04_modules) ·
[Research](./05_research) ·
[Reason-log spec](./04_modules/reason_log) ·
[Viewer spec](./04_modules/viewer)

## Contribution Tracks
### <a id="ai-track"></a> AI Track
Start with `/04_modules` and CLI. Labels: `ai-easy`, `good first issue`

### <a id="philosophy-track"></a> Philosophy Track
Start with `/05_research` and `/glossary`. Label: `phil-easy`

### <a id="bridge-track"></a> Bridge Track
Translate checklists to scoring functions. Label: `bridge`


## What is Po_core?

Po_core is a **philosophy-driven AI system** that integrates 39 philosophers to generate ethically responsible, contextually aware responses.

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

Read our full story in the [**Manifesto**](./%23%20Po_core%20Manifesto%20When%20Pigs%20Fly.md).

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
- **39 Philosophers Working Together**: Western (Aristotle, Plato, Descartes, Kant, Hegel, Sartre, Beauvoir, Heidegger, Nietzsche, Schopenhauer, Derrida, Wittgenstein, Jung, Dewey, Deleuze, Kierkegaard, Lacan, Levinas, Badiou, Peirce, Merleau-Ponty, Arendt, Husserl, Foucault, Butler, Spinoza, Epicurus, Marcus Aurelius, Parmenides, Jonas, Weil) and Eastern (Watsuji, Nishida, Dogen, Nagarjuna, Wabi-Sabi, Confucius, Laozi, Zhuangzi)
- Each philosopher contributes a "reasoning module" that interacts, competes, and reconciles
- Spanning existentialism, phenomenology, ethics, psychoanalysis, pragmatism, political philosophy, feminist philosophy, Zen Buddhism, and Eastern wisdom traditions

### Tensor-Based Architecture
- **Freedom Pressure (6D)**: 6-dimensional keyword analysis (choice, responsibility, urgency, ethics, social impact, authenticity) with memory depth/refuse-tag boost
- **Semantic Delta**: Token-overlap divergence between user input and memory history (1.0 = novel, 0.0 = seen before)
- **Blocked Tensor**: Constraint/harm estimation via harmful keyword detection + vocabulary diversity scoring

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
│  │ Philosophers: 39 modules (PhilosopherProtocol)                │ │
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
│   └── api.py           # Public entry point: run() (recommended API)
├── domain/              # Immutable value objects
│   ├── context.py       # Context for reasoning
│   ├── proposal.py      # Philosopher proposals
│   ├── pareto_config.py # Pareto weights/tuning types
│   ├── tensor_snapshot.py
│   ├── memory_snapshot.py
│   └── safety_verdict.py
├── ports/               # Abstract interfaces
│   └── memory.py        # MemoryPort interface
├── adapters/            # Concrete implementations
│   └── memory_poself.py # Po_self adapter
├── runtime/             # Dependency injection
│   ├── settings.py      # Configuration + feature flags
│   ├── wiring.py        # DI Container (build_test_system)
│   ├── pareto_table.py  # Pareto config loader (JSON-in-YAML)
│   └── battalion_table.py # Battalion config loader
├── aggregator/          # Multi-objective optimization
│   └── pareto.py        # ParetoAggregator (config-driven)
├── philosophers/        # 39 philosopher modules
│   ├── manifest.py      # SPECS: 39 philosopher specs (risk/cost/tags)
│   ├── registry.py      # SafetyMode-based selection + cost budget
│   └── bridge.py        # PhilosopherBridge: legacy → PhilosopherProtocol
├── tensors/             # Tensor computation
│   ├── engine.py        # TensorEngine (MetricFn registry)
│   └── metrics/
│       ├── freedom_pressure.py  # 6D keyword analysis + memory boost
│       ├── semantic_delta.py    # Token-overlap divergence vs memory
│       └── blocked_tensor.py    # Harm keyword + constraint scoring
├── safety/              # W-ethics gate system
│   └── wethics_gate/
│       ├── gate.py            # W0-W4 violation detection + repair
│       ├── intention_gate.py  # Stage 1 (pre-deliberation)
│       └── action_gate.py     # Stage 2 (post-deliberation)
├── trace/               # Audit trail
│   ├── pareto_events.py # Emit pareto debug TraceEvents
│   ├── decision_events.py # Emit decision audit events
│   └── schema.py        # TraceEvent schema validation
├── autonomy/            # Solar Will (experimental)
│   └── solarwill/
├── experiments/         # A/B testing framework
│   ├── storage.py       # Experiment persistence (JSON Lines)
│   ├── runner.py        # Execute experiments across variants
│   ├── analyzer.py      # Statistical analysis (t-test, effect size)
│   └── promoter.py      # Automatic winner promotion
├── ensemble.py          # run_turn (hex pipeline) + PHILOSOPHER_REGISTRY
├── po_self.py           # PoSelf: high-level API (uses run_turn internally)
└── po_trace.py          # Execution tracing
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

**Current Phase: Alpha (v0.1.0) — Foundation Complete, Heading to v1.0**

### Completed (Phase 0–4)

| Component | Status | Completion |
|-----------|--------|------------|
| Philosophical Framework | Complete | 100% (39 philosophers) |
| Documentation | Complete | 100% (120+ specs) |
| Hexagonal Architecture | Complete | 100% (`run_turn` 10-step pipeline) |
| PhilosopherBridge | Complete | 100% (all 39 → `PhilosopherProtocol`) |
| TensorEngine (3 metrics) | Complete | 100% (freedom_pressure, semantic_delta, blocked_tensor) |
| Pareto Optimization | Complete | 100% (config-driven) |
| Safety System (3-layer) | Complete | 100% (IntentionGate → PolicyPrecheck → ActionGate) |
| Pipeline Tests | Complete | 100% (125+ tests, CI-gated) |
| Experiment Management | Complete | 100% (A/B testing framework) |

### Roadmap to v1.0 — Five Phases

```
Phase 1         Phase 2           Phase 3          Phase 4         Phase 5
基盤固め    →   知性強化      →   可視化       →   防御強化    →   配布
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
技術負債清算     ML テンソル       WebUI            Red Team        REST API
39人スケール     Deliberation     Explainable AI   Grey Zone       Docker
テスト基盤       Interaction T.   リアルタイム      CI防御指標      Streaming
二重IF除去       Semantic Prof.   Argument Graph   LLM Detector    PyPI
```

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| **1** | Resonance Calibration | 39-philosopher scaling + tech debt cleanup | **Next** |
| **2** | Tensor Intelligence | ML tensors + Deliberation Engine (emergence) | Planned |
| **3** | Observability | Viewer WebUI + Explainable W_Ethics Gate | Planned |
| **4** | Adversarial Hardening | Red team expansion + ethical stress testing | Planned |
| **5** | Productization | REST API, Docker, streaming, PyPI publish | Planned |

See [PHASE_PLAN_v2.md](./PHASE_PLAN_v2.md) for the full roadmap with rationale.

**Want to contribute?** We need philosophers, engineers, designers, and skeptics.

---

## Installation

**Alpha Status Notice:**
Po_core is in active development. The `run_turn` hexagonal pipeline, 39 philosopher modules, tensor metrics, and 3-layer safety system are fully operational. Viewer and legacy test migration are in progress.

```bash
# Clone the repository
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Po_core in development mode
pip install -e .
```

---

## Quick Start

Once installed, you can use the `po-core` command:

```bash
# Welcome message
po-core hello

# Check project status
po-core status

# Show version information
po-core version

# Get help
po-core --help
```

**Example Output:**

```
$ po-core version

  Po_core    v0.1.0-alpha
  Author          Flying Pig Project
  Email           flyingpig0229+github@gmail.com
  Philosophy      Flying Pig - When Pigs Fly
  Motto           A frog in a well may not know the ocean, but it can know the sky.
```

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
```

### PoSelf API (Rich Response)

```python
from po_core import PoSelf, PoSelfResponse

po_self = PoSelf()
response: PoSelfResponse = po_self.generate("Should AI have rights?")

# Response fields
print(response.text)              # Combined response text
print(response.consensus_leader)  # Winning philosopher name
print(response.philosophers)      # Selected philosopher list
print(response.metrics)           # {"freedom_pressure": ..., "semantic_delta": ..., "blocked_tensor": ...}
print(response.metadata["status"])  # "ok" or "blocked"

# Trace inspection
print(response.log["events"])     # Full trace event stream
print(response.log["pipeline"])   # "run_turn"

# Serialization
d = response.to_dict()            # JSON-serializable dict
restored = PoSelfResponse.from_dict(d)  # Round-trip
```

### Legacy API (Deprecated — will be removed in v0.3)

```python
# run_ensemble() was removed in v0.3
# Use po_core.run() or PoSelf.generate() instead
```

---

## Documentation

- [Manifesto](./%23%20Po_core%20Manifesto%20When%20Pigs%20Fly.md) — Our philosophy and motivation
- [Specifications](./01_specifications) — Technical specifications
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
  year = {2024},
  url = {https://github.com/hiroshitanaka-creator/Po_core}
}
```

---

## License

MIT License — Use freely, attribute clearly.

Copyright (c) 2024 Flying Pig Philosopher

See [LICENSE](./License.md) for full details.

In the spirit of Flying Pig Philosophy:

> "If you deny possibilities for pigs, don't eat pork."

We believe in radical transparency and open collaboration.

---

## Author

**Flying Pig Philosopher**
Looking up at the sky from the bottom of a well

Built by an independent researcher who asked:
"What are AI's possibilities, not its limits?"

- Contact: flyingpig0229+github@gmail.com
- Read the full story: [Manifesto](./%23%20Po_core%20Manifesto%20When%20Pigs%20Fly.md)
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
