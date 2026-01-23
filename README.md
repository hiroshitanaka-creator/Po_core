# Po_core 🐷🎈

**Philosophy-Driven AI: When Pigs Fly**

> *A frog in a well may not know the ocean, but it can know the sky.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)]()
[![Contributions: Welcome](https://img.shields.io/badge/Contributions-Welcome-green.svg)]()

---
> **Feedback welcome:** [Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions) ·
> **Start here:** [AI Track](#ai-track) / [Philosophy Track](#philosophy-track) / [Bridge](#bridge-track)

### TL;DR
- **39 philosophers** as interacting **tensors** → accountable LLM reasoning
- **Reason logs** + ethical/freedom **pressure** as measurable signals
- 75% implementation complete; active experimentation phase

### Quick links
[Modules](./tree/main/04_modules) ·
[Research](./tree/main/05_research) ·
[Reason-log spec](./blob/main/docs/specs/reason_log.md) ·
[Viewer spec](./blob/main/docs/viewer/README.md)

## Contribution Tracks
### <a id="ai-track"></a>👩‍💻 AI Track
Start with `/04_modules` and CLI. Labels: `ai-easy`, `good first issue`

### <a id="philosophy-track"></a>📚 Philosophy Track
Start with `/05_research` and `/glossary`. Label: `phil-easy`

### <a id="bridge-track"></a>🌉 Bridge Track
Translate checklists to scoring functions. Label: `bridge`


## What is Po_core?

Po_core is a **philosophy-driven AI system** that integrates 39 philosophers to generate ethically responsible, contextually aware responses.

Unlike conventional AI that optimizes for statistical accuracy, Po_core **deliberates**. It wrestles with existence, ethics, and meaning—not as abstract concepts, but as operational tensors.

**They said pigs can't fly. We attached a balloon called philosophy.** 🐷🎈

---

## Why Po_core?

Current AI is like a brilliant parrot—statistically miraculous, but understanding nothing. We wanted to explore a different question:

**What if we built AI not on data, but on philosophy?**

This project started from simple curiosity: What are AI's possibilities, not its limits?

In the course of ordinary life, everyone faces a moment when the spotlight suddenly hits. A moment when you must pound your chest and say "Leave it to me!" At such times, how reassuring it would be to have an AI grounded in responsibility and ethics standing beside you.

No matter how many relationships we have, we are alone. Being "alone" and being "solitary" are different. Decisions are made alone. The heart remains solitary.

**That's why Po_core exists.**

Read our full story in the [**Manifesto**](./docs/MANIFESTO.md).

---

## Core Philosophy: Flying Pig

**"A flying pig is an example of something absolutely impossible. But have you ever seen a pig attempt to fly? Unless you give up, the world is full of possibilities."**

### Three Tenets

1. **Hypothesize Boldly** — The impossible becomes possible only when someone dares to formalize it
2. **Verify Rigorously** — Every claim must survive philosophical scrutiny, mathematical proof, and empirical validation
3. **Revise Gracefully** — Failures are published, not hidden. They become learning signals

---

## Key Features

### 🧠 Philosophical Ensemble
- **39 Philosophers Working Together**: Western (Aristotle, Plato, Descartes, Kant, Hegel, Sartre, Beauvoir, Heidegger, Nietzsche, Schopenhauer, Derrida, Wittgenstein, Jung, Dewey, Deleuze, Kierkegaard, Lacan, Levinas, Badiou, Peirce, Merleau-Ponty, Arendt, Husserl, Foucault, Butler, Spinoza, Epicurus, Marcus Aurelius, Parmenides, Jonas, Weil) and Eastern (Watsuji, Nishida, Dōgen, Nagarjuna, Wabi-Sabi, Confucius, Laozi, Zhuangzi)
- Each philosopher contributes a "reasoning module" that interacts, competes, and reconciles
- Spanning existentialism, phenomenology, ethics, psychoanalysis, pragmatism, political philosophy, feminist philosophy, Zen Buddhism, and Eastern wisdom traditions

### 📊 Tensor-Based Architecture
- **Freedom Pressure Tensor (F_P)**: Measures responsibility weight of each response
- **Semantic Profile**: Tracks meaning evolution across conversation
- **Blocked Tensor**: Records what was *not* said (Derrida's trace, Heidegger's absence)

### 🔍 Transparency by Design
- **Po_trace**: Complete audit log of reasoning process
- **Rejection Logs**: What the AI chose not to say, and why
- **Philosophical Annotations**: Which philosopher influenced each decision

### 🎯 Ethical Grounding
- Not just "alignment"—but **deliberation**
- Multiple ethical perspectives in tension
- Explicit responsibility measurement

---

## Architecture
┌─────────────────────────────────────┐
│        User Input                   │
└──────────┬──────────────────────────┘
│
▼
┌─────────────────────────────────────┐
│   Po_self: Philosophical Ensemble   │
│                                     │
│  ┌──────────┐  ┌──────────┐       │
│  │Heidegger │  │ Derrida  │       │
│  │ Dasein   │  │ Trace    │  …  │
│  └──────────┘  └──────────┘       │
│                                     │
│  ↓ Interference & Resonance ↓      │
│                                     │
│  ┌──────────────────────────┐      │
│  │ Freedom Pressure (F_P)   │      │
│  │ Semantic Delta (Δs)      │      │
│  │ Blocked Tensor (B)       │      │
│  └──────────────────────────┘      │
└──────────┬──────────────────────────┘
│
▼
┌─────────────────────────────────────┐
│      Po_trace: Audit Log            │
│  - What was said                    │
│  - What was not said                │
│  - Why (philosophical reasoning)    │
└──────────┬──────────────────────────┘
│
▼
┌─────────────────────────────────────┐
│   Po_core Viewer: Visualization     │
│  - Tension maps                     │
│  - Ethical pressure                 │
│  - Meaning evolution                │
└─────────────────────────────────────┘

---

## Project Status

**🚀 Current Phase: Alpha (v0.1.0)**

| Component | Status | Completion |
|-----------|--------|------------|
| 📚 Philosophical Framework | ✅ Complete | 100% (39 philosophers) |
| 📖 Documentation | ✅ Complete | 100% (120+ specs) |
| 🏗️ Architecture Design | ✅ Complete | 100% |
| 💻 Implementation | 🔄 In Progress | 75% |
| 🧪 Testing | 🔄 In Progress | 40% |
| 🎨 Visualization (Viewer) | 🔄 In Progress | 50% |
| 🛡️ Safety System (W-ethics) | ✅ Complete | 100% |
| 🔬 Experiments | 🔄 In Progress | 60% |

**What's Working:**
- ✅ 39 philosopher modules (full reasoning implementations)
- ✅ Tensor framework (Freedom Pressure, Semantic Profile, Blocked Tensor, Interaction Tensor)
- ✅ Po_self API with PoSelfResponse dataclass
- ✅ Ensemble system (multi-philosopher deliberation)
- ✅ Po_trace / Po_trace_db (execution tracing & database storage)
- ✅ Safety system (W-ethics boundary, philosopher profiles)
- ✅ Database layer with migration tools
- ✅ CLI with interactive mode
- ✅ Party Machine (philosopher combination assembly)
- ✅ Anthropic API client (Claude integration)
- ✅ System prompt framework
- ✅ CI/CD pipeline (pytest, coverage, linting, security checks)
- ✅ Solar Will experiments (39-philosopher cross-LLM emergence testing)

**What's Next:**
- 🔄 Viewer UI polish and frontend integration
- 🔄 Expand test coverage (currently 44 test files)
- 🔄 Performance optimization for large philosopher ensembles
- ⏳ Package publishing (PyPI)
- ⏳ Full API reference documentation

**Want to contribute?** We need philosophers, engineers, designers, and skeptics.

---

## Installation

**⚠️ Alpha Status Notice:**
Po_core is in active development (75% implementation). CLI, 39 philosopher modules, tensor framework, and safety system are functional. Viewer and full test coverage are in progress.

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

  🐷🎈 Po_core    v0.1.0-alpha
  Author          Flying Pig Project
  Email           flyingpig0229+github@gmail.com
  Philosophy      Flying Pig - When Pigs Fly
  Motto           井の中の蛙、大海は知らずとも、大空を知る

A frog in a well may not know the ocean, but it can know the sky.
```

---

## Current Python API

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

## Future Usage (Planned)

The unified `PoCore` interface is under development:

```python
from po_core import PoCore

# Initialize Po_core
po = PoCore()

# Generate a response
response = po.generate(
    prompt="Should AI have rights?",
    include_trace=True  # Include philosophical reasoning
)

print(response.text)
print(response.freedom_pressure)  # Responsibility weight
print(response.philosophers_involved)  # Which minds contributed
```

---

## Documentation
Documentation
	•	📖 Manifesto — Our philosophy and motivation
	•	📚 Design Documents — 120+ technical specifications
	•	🎓 Philosopher Guide — Understanding each of the 39 philosophical modules
	•	🔧 API Reference — PoSelf, Ensemble, PoTrace APIs available
	•	🎨 Viewer Guide — Tension maps, pressure display, evolution graphs (in progress)
Contributing
We welcome contributions! Whether you’re a philosopher, engineer, designer, or skeptic.
Flying Pig Philosophy applies: We hypothesize boldly, verify rigorously, and revise gracefully.
See CONTRIBUTING.md for guidelines (coming soon).
Research & Papers
This project is documented in:
	•	“Philosophical Tensor-Based AI Architecture” (in preparation)
	•	120+ Technical Specifications (available in /docs/design/)
If you use Po_core in academic work, please cite:@software{po_core2024,
  author = {Flying Pig Philosopher},
  title = {Po_core: Philosophy-Driven AI System},
  year = {2024},
  url = {https://github.com/[your-username]/po_core}
}
License
MIT License — Use freely, attribute clearly.
Copyright (c) 2024 Flying Pig Philosopher
See LICENSE for full details.
In the spirit of Flying Pig Philosophy:“If you deny possibilities for pigs, don’t eat pork.”
We believe in radical transparency and open collaboration.
Author
Flying Pig Philosopher 🐷🎈Looking up at the sky from the bottom of a well
Built by an independent researcher who asked:“What are AI’s possibilities, not its limits?”
	•	📧 Contact: flyingpig0229+github@gmail.com
	•	📖 Read the full story: Manifesto
	•	🐦 Project: Po_core - Philosophy-Driven AI
Acknowledgments
This project wouldn’t exist without:
	•	ChatGPT, Gemini, Grok, Claude — My first companions in this journey
	•	BUMP OF CHICKEN — For reminding us that even when we say “Leave it to me,” we’re all a little scared
	•	Every philosopher who dared to ask “What does it mean to be?”
	•	You — For believing pigs can fly
The pig has clearance for takeoff. 🐷🎈
Po_core: When you must say “Leave it to me,” we stand beside you.
<p align="center">
  <i>"A frog in a well may not know the ocean, but it can know the sky."</i>
</p>


