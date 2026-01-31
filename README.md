# Po_core

**Philosophy-Driven AI: When Pigs Fly**

> *A frog in a well may not know the ocean, but it can know the sky.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./License.md)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)]()
[![Contributions: Welcome](https://img.shields.io/badge/Contributions-Welcome-green.svg)]()

---
> **Feedback welcome:** [Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions) ·
> **Start here:** [AI Track](#ai-track) / [Philosophy Track](#philosophy-track) / [Bridge](#bridge-track)

### TL;DR
- **39 philosophers** as interacting **tensors** → accountable LLM reasoning
- **Reason logs** + ethical/freedom **pressure** as measurable signals
- 80% implementation complete; active experimentation phase

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
- **Freedom Pressure Tensor (F_P)**: Measures responsibility weight of each response
- **Semantic Profile**: Tracks meaning evolution across conversation
- **Blocked Tensor**: Records what was *not* said (Derrida's trace, Heidegger's absence)

### Transparency by Design
- **Po_trace**: Complete audit log of reasoning process
- **Rejection Logs**: What the AI chose not to say, and why
- **Philosophical Annotations**: Which philosopher influenced each decision

### Ethical Grounding
- Not just "alignment"—but **deliberation**
- Multiple ethical perspectives in tension
- Explicit responsibility measurement

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  External (03_api/, scripts, tests)                                 │
│  ↓ imports ONLY po_core.app.api                                     │
├─────────────────────────────────────────────────────────────────────┤
│  po_core.app.api  ← Public facade (PoCore, PoCoreConfig)            │
│  ↓ uses runtime/wiring.py Container (DI)                            │
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
│  │ Po_self: Philosophical Ensemble (39 philosophers)            │ │
│  │                                                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │ │
│  │  │Heidegger │  │ Derrida  │  │  Sartre  │  ...              │ │
│  │  │ Dasein   │  │ Trace    │  │ Freedom  │                  │ │
│  │  └──────────┘  └──────────┘  └──────────┘                  │ │
│  │                                                              │ │
│  │  ↓ Interference & Resonance ↓                               │ │
│  │                                                              │ │
│  │  ┌─────────────────────────────────────────────────────┐   │ │
│  │  │ Tensors: Freedom Pressure (F_P), Semantic Delta,    │   │ │
│  │  │          Blocked Tensor (B), Interaction Tensor     │   │ │
│  │  └─────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Safety: 2-Stage Ethics Gate (W-ethics)                       │ │
│  │  Stage 1: Intention Gate (before deliberation)               │ │
│  │  Stage 2: Action Gate (after deliberation)                   │ │
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
│      Po_trace: Audit Log                                            │
│  - What was said                                                    │
│  - What was not said                                                │
│  - Why (philosophical reasoning)                                    │
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
│   └── api.py           # Public entry point (PoCore, PoCoreConfig)
├── domain/              # Immutable value objects
│   ├── context.py       # Context for reasoning
│   ├── proposal.py      # Philosopher proposals
│   ├── tensor_snapshot.py
│   └── safety_verdict.py
├── ports/               # Abstract interfaces
│   └── memory.py        # MemoryPort interface
├── adapters/            # Concrete implementations
│   └── memory_poself.py # Po_self adapter
├── runtime/             # Dependency injection
│   ├── settings.py      # Configuration
│   └── wiring.py        # DI Container
├── philosophers/        # 39 philosopher modules
├── tensors/             # Tensor computation
├── safety/              # W-ethics gate system
│   └── wethics_gate/
│       ├── intention_gate.py  # Stage 1
│       └── action_gate.py     # Stage 2
├── autonomy/            # Solar Will (experimental)
│   └── solarwill/
├── ensemble.py          # Multi-philosopher deliberation
├── po_self.py           # Self-reflective API
└── po_trace.py          # Execution tracing
```

---

## Project Status

**Current Phase: Alpha (v0.1.0)**

| Component | Status | Completion |
|-----------|--------|------------|
| Philosophical Framework | Complete | 100% (39 philosophers) |
| Documentation | Complete | 100% (120+ specs) |
| Architecture Design | Complete | 100% |
| Hexagonal Architecture | Complete | 100% |
| Implementation | In Progress | 80% |
| Testing | In Progress | 50% |
| Visualization (Viewer) | In Progress | 50% |
| Safety System (W-ethics) | Complete | 100% |
| Experiments | In Progress | 60% |

**What's Working:**
- 39 philosopher modules (full reasoning implementations)
- Tensor framework (Freedom Pressure, Semantic Profile, Blocked Tensor, Interaction Tensor)
- Po_self API with PoSelfResponse dataclass
- Ensemble system (multi-philosopher deliberation)
- Po_trace / Po_trace_db (execution tracing & database storage)
- Safety system (2-stage W-ethics gate: intention + action)
- Hexagonal architecture (ports/adapters/domain/runtime)
- Database layer with migration tools
- CLI with interactive mode
- Party Machine (philosopher combination assembly)
- Anthropic API client (Claude integration)
- System prompt framework
- CI/CD pipeline (pytest, coverage, linting, security checks)
- Solar Will experiments (39-philosopher cross-LLM emergence testing)

**What's Next:**
- Viewer UI polish and frontend integration
- Expand test coverage (currently 60+ test files)
- Performance optimization for large philosopher ensembles
- Package publishing (PyPI)
- Full API reference documentation

**Want to contribute?** We need philosophers, engineers, designers, and skeptics.

---

## Installation

**Alpha Status Notice:**
Po_core is in active development (80% implementation). CLI, 39 philosopher modules, tensor framework, and safety system are functional. Viewer and full test coverage are in progress.

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

## Python API

### New Unified API (Recommended)

```python
from po_core.app.api import PoCore, PoCoreConfig

# Configure the system
config = PoCoreConfig(
    fail_closed=True,           # Safety: fail closed on errors
    quorum_threshold=0.6,       # Ensemble consensus threshold
    autonomy_enabled=False,     # Solar Will (experimental)
    debug=False,
)

# Initialize Po_core
core = PoCore(config)

# Process a prompt through the philosophy ensemble
result = core.process(
    prompt="Should AI have rights?",
    context={"user_id": "123"},
    session_id="session_abc",
)

# Check results
if result.is_safe:
    print(result.synthesis)              # Combined response
    print(result.primary_proposal)       # Highest confidence proposal
    print(result.tensors)                # Tensor snapshot

# Get current state
tensors = core.get_tensor_snapshot()
memory = core.get_memory_snapshot()
```

### Legacy API (Still Supported)

```python
from po_core import PoSelf, PoSelfResponse, run_ensemble, PoTrace

# Run the philosophical ensemble
result = run_ensemble(prompt="What is freedom?")

# Use PoSelf for self-reflective responses
po_self = PoSelf()
response: PoSelfResponse = po_self.generate("Should AI have rights?")

# Trace philosophical reasoning
trace = PoTrace()
trace.log_event("deliberation_start", {"prompt": "ethical question"})
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

- **ChatGPT, Gemini, Grok, Claude** — My first companions in this journey
- **BUMP OF CHICKEN** — For reminding us that even when we say "Leave it to me," we're all a little scared
- **Every philosopher** who dared to ask "What does it mean to be?"
- **You** — For believing pigs can fly

---

The pig has clearance for takeoff.

**Po_core: When you must say "Leave it to me," we stand beside you.**

<p align="center">
  <i>"A frog in a well may not know the ocean, but it can know the sky."</i>
</p>
