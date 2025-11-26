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
- Philosophers as interacting **tensors** → accountable LLM reasoning
- **Reason logs** + ethical/freedom **pressure** as measurable signals
- ✅ **Working prototypes** with Web API, batch processing, and visualization
- Alpha release with 20 philosophers, complete tracing, and 60% core implementation

### Quick links
[Examples & Demos](./examples/README.md) ·
[Prototypes Guide](./examples/MEDIUM_PROTOTYPES.md) ·
[Modules](./tree/main/04_modules) ·
[Research](./tree/main/05_research) ·
[Po_trace spec](./blob/main/docs/specs/reason_log.md) ·
[Po_viewer spec](./blob/main/docs/viewer/README.md)

## Contribution Tracks
### <a id="ai-track"></a>👩‍💻 AI Track
Start with `/04_modules` and CLI. Labels: `ai-easy`, `good first issue`

### <a id="philosophy-track"></a>📚 Philosophy Track
Start with `/05_research` and `/glossary`. Label: `phil-easy`

### <a id="bridge-track"></a>🌉 Bridge Track
Translate checklists to scoring functions. Label: `bridge`


## What is Po_core?

Po_core is a **philosophy-driven AI system** that integrates 10+ philosophers to generate ethically responsible, contextually aware responses.

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
- **20 Philosophers Working Together**: Western (Aristotle, Sartre, Heidegger, Nietzsche, Derrida, Wittgenstein, Jung, Dewey, Deleuze, Kierkegaard, Lacan, Levinas, Badiou, Peirce, Merleau-Ponty, Arendt) and Eastern (Watsuji Tetsurō, Wabi-Sabi, Confucius, Zhuangzi)
- Each philosopher contributes a "reasoning module" that interacts, competes, and reconciles
- Spanning existentialism, phenomenology, ethics, psychoanalysis, pragmatism, political philosophy, and Eastern wisdom traditions

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
| 📚 Philosophical Framework | ✅ Complete | 100% |
| 📖 Documentation | ✅ Complete | 100% (120+ specs) |
| 🏗️ Architecture Design | ✅ Complete | 100% |
| 💻 Core Implementation | 🔄 In Progress | 60% |
| 🚀 Working Prototypes | ✅ Complete | 100% |
| 🔍 Po_trace (Audit Log) | ✅ Complete | 100% |
| 🎨 Po_viewer (Visualization) | ✅ Complete | 100% |
| 🧪 Testing | 🔄 In Progress | 40% |

**What's Working:**
- ✅ Po_self API with 20 philosophers
- ✅ Philosophical tensor calculations (Freedom Pressure, Semantic Delta, Blocked Tensor)
- ✅ Po_trace audit logging system
- ✅ Po_viewer visualization system
- ✅ Web API Server (FastAPI-based)
- ✅ Batch Analyzer for large-scale processing
- ✅ Philosopher Comparison Tool
- ✅ Complete design specifications

**What's Next:**
- 🔄 Enhanced testing coverage
- 🔄 Performance optimization
- ⏳ Production deployment guides
- ⏳ Advanced visualization features

**Want to contribute?** We need philosophers, engineers, designers, and skeptics.

---

## Installation

**⚠️ Alpha Status Notice:**
Po_core is in early development. The CLI is functional, but core AI functionality is still being implemented.

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

## Working Prototypes & Examples

Po_core includes fully functional prototypes demonstrating real-world applications:

### 🌐 Web API Server

FastAPI-based RESTful API server with beautiful web interface.

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Start server
python examples/web_api_server.py
```

**Access:**
- Web Interface: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Features:**
- 🌐 Beautiful web-based chat interface
- 📡 RESTful API endpoints
- 💾 Session history management
- 📊 Statistics and analytics
- 🎨 Responsive gradient UI

### 📦 Batch Analyzer

Process multiple questions efficiently and export results.

```bash
python examples/batch_analyzer.py
```

**Capabilities:**
- Process 10+ questions in one run
- Export to JSON/CSV formats
- Statistical analysis (avg metrics, leader distribution)
- Progress tracking
- Customizable philosopher groups

### 🔍 Philosopher Comparison Tool

Compare different philosophical perspectives on the same question.

```bash
python examples/philosopher_comparison.py
```

**Features:**
- Group comparison (Existentialism, Ethics, Eastern Philosophy, etc.)
- Individual philosopher comparison
- Metrics comparison tables
- Detailed response analysis

### 📚 Basic Demos

**Simple Demo** - Interactive philosophical reasoning:
```bash
python examples/simple_demo.py
```

**API Demo** - 7 usage examples:
```bash
python examples/api_demo.py
```

**Quick Test** - Verify functionality:
```bash
python examples/quick_test.py
```

**📖 Full documentation:** See [examples/README.md](./examples/README.md) and [examples/MEDIUM_PROTOTYPES.md](./examples/MEDIUM_PROTOTYPES.md)

---

## Future Usage (Planned)

The full philosophical AI system is under development:

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

- 📖 [**Manifesto**](./docs/MANIFESTO.md) — Our philosophy and motivation
- 📚 [**Design Documents**](./docs/design/) — 120+ technical specifications
- 🎓 [**Philosopher Guide**](./docs/philosophers/) — Understanding each philosophical module
- 🚀 [**Examples & Prototypes**](./examples/README.md) — Working demos and usage examples
- 🌐 [**Medium Prototypes Guide**](./examples/MEDIUM_PROTOTYPES.md) — Web API, Batch Analyzer, Comparison Tool
- 🔍 [**Po_trace Specification**](./docs/specs/reason_log.md) — Audit logging system
- 🎨 [**Po_viewer Specification**](./docs/viewer/README.md) — Visualization system
- 🔧 **API Reference** — Complete API documentation (in progress)
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


