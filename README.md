# Po_core

最優先ルール（単一真実）：[docs/厳格固定ルール.md](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/status.md)

**Philosophy-Driven AI: When Pigs Fly**

> *A frog in a well may not know the ocean, but it can know the sky.*

[![PyPI version](https://img.shields.io/pypi/v/po-core-flyingpig)](https://pypi.org/project/po-core-flyingpig/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)
[![Status: Package%20metadata%20marks%20beta](https://img.shields.io/badge/Status-Package%20metadata%20marks%20beta-blue.svg)]()

---

## What is Po_core?

**Po_core is a philosophy-driven AI decision-support system.** You give it a question; it returns structured options, reasons, counterarguments, uncertainty labels, and follow-up questions — all grounded in ethical deliberation.

**What you get back:**

- `proposal` — the winning response after multi-philosopher deliberation
- `status` — `"ok"` or `"blocked"` (3-layer safety gate result)
- `options` / `questions` — alternative framings and uncertainty probes
- `trace` — full audit log of which reasoning paths were taken and why

**What Po_core is not:**

- Not a truth oracle — it does not claim factual correctness
- Not an emotional-care chatbot — it provides structured reasoning, not emotional support
- Not a replacement for medical, legal, or financial judgment

---

## Quick Start

```bash
pip install po-core-flyingpig
```

```python
from po_core import run

result = run("What is justice?")
print(result["proposal"])   # Winning philosopher's response
print(result["status"])     # "ok" or "blocked"
```

> **Install note:** Po_core pulls ML dependencies (`torch`, `sentence-transformers`, etc.). On a fresh environment the install may take several minutes. If `torch` or `sbert` are unavailable, the tensor backend falls back to `tfidf`/`basic` automatically — core deliberation still works.

**Local development checkout:**

```bash
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core
pip install -e ".[dev]"
```

---

## Key Links

| | |
|---|---|
| [Tutorial](./docs/TUTORIAL.md) | Step-by-step getting-started guide |
| [Python API reference](#python-api) | `run()` / `run_case()` / `PoSelf` / `PoSelfResponse` |
| [run_case API guide](./docs/RUN_CASE.md) | Structured case input → output_schema_v1 output |
| [REST API](#rest-api) | FastAPI server + curl examples |
| [Manifesto](./Po_core_Manifesto_When_Pigs_Fly.md) | Philosophy and motivation |
| [Release state](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/status.md) | Current version, evidence gaps, roadmap |
| [Safety Guide](./docs/SAFETY.md) | W-ethics gate system |
| [Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions) | Feedback welcome |

---

## Why the Deliberation Approach?

Current AI optimizes for statistical accuracy — a brilliant parrot that understands nothing. Po_core asks a different question: **what if AI reasoned from philosophy, not just data?**

The differentiator: **42 philosophers** (Western, Eastern, African, Canadian) run as interacting tensors through a 10-step hexagonal pipeline. Each brings its own reasoning module. They compete, interfere, and reconcile — producing a Pareto-optimal proposal with a measurable ethical pressure signal instead of a single confident prediction. (The internal `dummy` slot is a compliance sentinel helper and must not be counted as one of the 42.)

No matter how many relationships we have, decisions are made alone. That's why Po_core exists — **to stand beside you when you must say "Leave it to me."**

Read the full story: [Manifesto](./Po_core_Manifesto_When_Pigs_Fly.md)

---

## Architecture

**Hexagonal `run_turn` pipeline — 10 steps:**

```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

**Three tensor metrics** measure the deliberation:

| Metric | What it measures |
|---|---|
| FreedomPressureV2 (6D ML) | Choice, responsibility, urgency, ethics, social impact, authenticity |
| Semantic Delta | Novelty of the input vs. memory history (1.0 = never seen, 0.0 = familiar) |
| Blocked Tensor | Constraint / harm estimation |

**Safety** is three-layered: `IntentionGate` (pre-deliberation) → `PolicyPrecheck` (mid-pipeline) → `ActionGate` (post-deliberation). SafetyMode transitions NORMAL → WARN → CRITICAL based on freedom_pressure thresholds.

For full source layout and component detail → [Architecture docs](./02_architecture) · [CLAUDE.md](./CLAUDE.md)

---

## Release State

Repository target version is `1.1.0`; `1.0.3` is the latest published on PyPI. Package classifiers declare `Development Status :: 4 - Beta`.

For the complete evidence record, evidence gaps, and roadmap: **[docs/status.md](https://github.com/hiroshitanaka-creator/Po_core/blob/main/docs/status.md)**

---

## Installation

```bash
# From PyPI (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install po-core-flyingpig

# Specific version
pip install "po-core-flyingpig==1.0.3"

# Local development
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core
pip install -e ".[dev]"
```

> `requirements.txt` / `requirements-dev.txt` are repo-local convenience wrappers for a cloned checkout. External consumers should install from package metadata, not from those editable wrappers.

---

## Python API

Use `run_case(case: dict)` when you need output_schema_v1-conformant structured decision-support output. Use `run(user_input: str)` when you want the raw philosopher pipeline result.

### Simple API (Recommended)

```python
from po_core import run

result = run(user_input="Should AI have rights?")

print(result["status"])       # "ok" or "blocked"
print(result["request_id"])   # Unique request ID
print(result["proposal"])     # Winning philosopher's response

# Optional explicit philosopher allowlist
subset = run(user_input="Should AI have rights?", philosophers=["kant"])
```

### PoSelf API (Rich Response)

```python
from po_core import PoSelf, PoSelfResponse

po_self = PoSelf(philosophers=["aristotle", "confucius"])
response: PoSelfResponse = po_self.generate("Should AI have rights?")

print(response.text)               # Combined response text
print(response.consensus_leader)   # Winning philosopher name
print(response.philosophers)       # Selected philosopher list
print(response.metrics)            # {"freedom_pressure": ..., "semantic_delta": ..., ...}
print(response.metadata["status"]) # "ok" or "blocked"

# Trace inspection
print(response.log["events"])      # Full trace event stream

# Serialization
d = response.to_dict()
restored = PoSelfResponse.from_dict(d)
```

### Structured Output (synthesis_report)

```bash
export PO_STRUCTURED_OUTPUT=1
python scripts/observe_device.py "転職するべき？家族とキャリアのトレードオフが悩み"
```

### Legacy Note

`run_ensemble()` was removed in v0.3. Use `po_core.run()` or `PoSelf.generate()` instead.

---

## CLI

```bash
po-core version
po-core status
po-core --help

po-self --help
po-trace --help
po-interactive --help
po-experiment --help
```

Source checkout example:

```bash
python examples/po_party_demo.py --help
```

---

## REST API

```bash
# Start with recommended auth posture
export PO_API_KEY=dev-secret-key
python -m po_core.app.rest
# → http://localhost:8000  (OpenAPI docs at /docs)

# Reason
curl -X POST http://localhost:8000/v1/reason \
     -H "X-API-Key: dev-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"input": "What is justice?", "philosophers": ["kant"]}'

# Streaming (SSE)
curl -N http://localhost:8000/v1/reason/stream \
     -X POST -H "X-API-Key: dev-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"input": "What is freedom?"}'

# Philosopher manifest
curl -H "X-API-Key: dev-secret-key" http://localhost:8000/v1/philosophers

# Health (no auth required)
curl http://localhost:8000/v1/health
```

**Auth defaults:** Keep `PO_SKIP_AUTH=false` and set a non-empty `PO_API_KEY`. If both are unset, startup fails fast by design. `PO_SKIP_AUTH=true` is acceptable only for short-lived local development.

**Key env vars** (see `.env.example` for full list):

| Variable | Default | Description |
|---|---|---|
| `PO_API_KEY` | `""` | API key; blank causes startup failure when `PO_SKIP_AUTH=false` |
| `PO_SKIP_AUTH` | `false` | Set `true` only for short-lived local dev |
| `PO_CORS_ORIGINS` | `http://localhost,http://127.0.0.1,http://localhost:3000,http://127.0.0.1:3000` | Comma-separated allowed origins; localhost-only by default |
| `PO_RATE_LIMIT_PER_MINUTE` | `60` | Per-IP rate limit |
| `PO_PORT` | `8000` | Server port |
| `PO_PHILOSOPHER_EXECUTION_MODE` | `process` | Safe REST default; `thread` requires `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` |

---

## Docker

```bash
cp .env.example .env
docker compose up
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs
```

---

## A/B Experiments

```bash
po-experiment list
po-experiment analyze exp_001_safety_weight_sweep
po-experiment promote exp_001_safety_weight_sweep
po-experiment rollback
```

Po_core's Pareto weights are config-driven (`pareto_table.yaml`) and fully externalized. Tune philosophy without code changes; `config_version` is tracked in all TraceEvents for audit.

---

## Documentation

| Document | Description |
|---|---|
| [docs/spec/prd.md](./docs/spec/prd.md) | Product Requirements Document |
| [docs/spec/srs_v0.1.md](./docs/spec/srs_v0.1.md) | Software Requirements Specification (18 FR/NFR IDs) |
| [docs/spec/output_schema_v1.json](./docs/spec/output_schema_v1.json) | JSON Schema — contract for all structured output |
| [docs/spec/test_cases.md](./docs/spec/test_cases.md) | 10 acceptance tests (AT-001〜AT-010) |
| [docs/spec/traceability.md](./docs/spec/traceability.md) | Traceability matrix |
| [docs/ENGINE_TRACE_CONTRACT.md](./docs/ENGINE_TRACE_CONTRACT.md) | Engine trace event contract (TensorComputed, SafetyModeInferred, Pareto events, DecisionEmitted) |
| [docs/SAFETY.md](./docs/SAFETY.md) | W-ethics safety system |
| [docs/TUTORIAL.md](./docs/TUTORIAL.md) | Getting started guide |
| [docs/VISUALIZATION_GUIDE.md](./docs/VISUALIZATION_GUIDE.md) | Tension maps and pressure display |
| [01_specifications/](./01_specifications) | Technical specifications (120+ docs EN/JP) |
| [02_architecture/](./02_architecture) | System design documents |
| [04_modules/](./04_modules) | Component documentation |
| [05_research/](./05_research) | Academic papers and analysis |

---

## Contributing

We welcome philosophers, engineers, designers, and skeptics.

**Contribution tracks:**

- **AI Track** — Start with `/04_modules` and CLI. Labels: `ai-easy`, `good first issue`
- **Philosophy Track** — Start with `/05_research` and `/glossary`. Label: `phil-easy`
- **Bridge Track** — Translate checklists to scoring functions. Label: `bridge`

Flying Pig Philosophy applies: hypothesize boldly, verify rigorously, revise gracefully.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Research

- "Philosophical Tensor-Based AI Architecture" (in preparation)
- 120+ Technical Specifications in [/docs/](./docs/) and [/01_specifications/](./01_specifications/)

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

| Use case | License |
|---|---|
| Personal / Academic / Research / OSS (AGPLv3-compliant) | **Free** — [AGPLv3](./LICENSE) |
| Commercial / Proprietary / SaaS without source disclosure | **Commercial License required** |

For commercial licensing: flyingpig0229+github@gmail.com
See [COMMERCIAL_LICENSE.md](./COMMERCIAL_LICENSE.md) for details.

Copyright (c) 2024 Flying Pig Project

> "If you deny possibilities for pigs, don't eat pork."

---

## Author

**Flying Pig Philosopher** — Looking up at the sky from the bottom of a well

Built by an independent researcher who asked: *"What are AI's possibilities, not its limits?"*

- Contact: <flyingpig0229+github@gmail.com>
- Read the full story: [Manifesto](./Po_core_Manifesto_When_Pigs_Fly.md)

---

## Acknowledgments

- **ChatGPT, Gemini, Grok, Claude** — My companions throughout this journey
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

- DMCA申請中 (Reference ID: #4124875)
- Any full copy, license rewrite (MIT), or impersonation (flying_pig) will be reported and removed.
- Commercial use requires separate license. Unauthorized copies detected via tensor mania series.
