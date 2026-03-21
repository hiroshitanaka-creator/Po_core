# Po_core Quick Start 🐷🎈

A quick guide to get started with Po_core's philosophy-driven AI system.

## 📦 Installation

```bash
# Install the published PyPI package
pip install "po-core-flyingpig==1.0.2"
```



## 📦 Published package status

Version `1.0.2` should be described using the repository's evidence boundary. Today the repo evidences only **PyPI published** via `docs/release/pypi_publication_v1.0.2.md`; TestPyPI publication, workflow-run URLs, and clean post-publish smoke transcripts remain out of bounds until operator-supplied evidence is recorded.

## 🔐 REST runtime defaults

- Keep `PO_SKIP_AUTH=false` and set a non-empty `PO_API_KEY` for any non-trivial deployment.
- Default CORS is localhost-only; use `PO_CORS_ORIGINS=*` only as an explicit short-lived development override.
- The REST server now defaults `PO_PHILOSOPHER_EXECUTION_MODE=process` and refuses `thread` mode unless `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` is explicitly set for development.

## ⚡ Try it in 30 Seconds

### Minimal Code

```python
from po_core.po_self import PoSelf

# Create a Po_self instance
po = PoSelf()

# Execute philosophical reasoning on a question
response = po.generate("What is the meaning of life?")

# Display the results
print(f"Answer: {response.text}")
print(f"Leader: {response.consensus_leader}")
```

### Command Line Interface (CLI)

```bash
# Show help
po-core --help

# Check version
po-core version

# Reason about a question
po-core prompt "What is true freedom?"

# Output in JSON format
po-core prompt "What is ethics?" --format json
```

## 🎮 Try the Demos

### Interactive Demo

```bash
# Set PYTHONPATH and run
PYTHONPATH=src python examples/simple_demo.py
```

The demo lets you experience:

1. **Basic Demo** - Philosophical reasoning on a single question
2. **Philosopher Comparison Demo** - Compare perspectives from different philosopher groups
3. **Interactive Mode** - Continuous question-and-answer sessions

### API Usage Examples

```bash
# Run all API examples
PYTHONPATH=src python examples/api_demo.py
```

Seven practical usage examples will be executed.

## 🧠 Basic Usage

### 1. Reasoning with Default Philosophers

```python
from po_core.po_self import PoSelf

po = PoSelf()
response = po.generate("What is justice?")

print(response.text)
print(f"Metrics: {response.metrics}")
```

### 2. Select Custom Philosophers

```python
# Existentialist group (constructor = default allowlist)
default_philosophers = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=default_philosophers)

response = po.generate("What is existence?")
print(response.text)

# Per-call philosophers=... overrides constructor default
override = po.generate("What is existence?", philosophers=["nietzsche"])
print(override.text)
```

### 3. Get Results in JSON Format

```python
import json

po = PoSelf()
response = po.generate("What is beauty?")

# Convert to dictionary format
data = response.to_dict()

# JSON output
print(json.dumps(data, indent=2, ensure_ascii=False))
```

## 🎯 Available Philosophers

Po_core uses **42 integrated runtime personas**. That is the public roster count: one slot is reserved for compliance-sentinel behavior, so docs should not imply that all 42 slots are named human philosophers. Runtime selection budgets keep the default NORMAL path at **39 active** personas maximum per request, and the number mobilized varies by SafetyMode:

| Philosopher | Key | Specialty |
|------------|-----|-----------|
| Aristotle | `aristotle` | Virtue ethics, Teleology |
| Sartre | `sartre` | Existentialism |
| Heidegger | `heidegger` | Phenomenology, Ontology |
| Nietzsche | `nietzsche` | Will to power, Genealogy |
| Derrida | `derrida` | Deconstruction |
| Wittgenstein | `wittgenstein` | Philosophy of language |
| Jung | `jung` | Analytical psychology |
| Dewey | `dewey` | Pragmatism |
| Deleuze | `deleuze` | Philosophy of difference |
| Kierkegaard | `kierkegaard` | Existentialism |
| Lacan | `lacan` | Psychoanalysis |
| Levinas | `levinas` | Ethics of the Other |
| Badiou | `badiou` | Mathematical ontology |
| Peirce | `peirce` | Semiotics, Pragmatism |
| Merleau-Ponty | `merleau_ponty` | Phenomenology of the body |
| Arendt | `arendt` | Political philosophy |
| Watsuji Tetsurō | `watsuji` | Ethics of betweenness |
| Wabi-Sabi | `wabi_sabi` | Japanese aesthetics |
| Confucius | `confucius` | Confucianism |
| Zhuangzi | `zhuangzi` | Taoism |
| … 19 more | `GET /v1/philosophers` | for the full manifest |

## 📊 Output Structure

```python
response = po.generate("Your question")

# Accessible attributes
response.prompt              # The input question
response.text                # Reasoning result text
response.consensus_leader    # Consensus leader (most influential philosopher)
response.philosophers        # List of participating philosophers
response.metrics            # Philosophical tensor metrics
response.responses          # Detailed responses from each philosopher
response.log                # Trace log (Po_trace)
```

### Metrics Meaning

- **freedom_pressure**: Freedom Pressure - Measures responsibility weight of response (0.0-1.0)
- **semantic_delta**: Semantic Delta - Tracks meaning evolution (0.0-1.0)
- **blocked_tensor**: Blocked Tensor - Records what was not said (0.0-1.0)

## 🔧 Advanced Usage

### Using po_core.run() Directly

```python
from po_core import run

result = run(user_input="What is beauty?")

print(result['status'])       # "ok"
print(result['request_id'])   # Request ID
print(result['proposal'])     # Proposal content

# Public API facade also supports explicit subset selection
subset = run(user_input="What is justice?", philosophers=["kant"])
print(subset['status'])
```

### Controlling Trace Functionality

```python
# Trace enabled (default)
po = PoSelf(enable_trace=True)
response = po.generate("What is justice?")
print(response.log)  # Check trace log

# Trace disabled (lightweight mode)
po = PoSelf(enable_trace=False)
response = po.generate("What is justice?")
```

## 💡 Usage Example Scenarios

### Ethical Decision Support

```python
# Select ethics-specialized philosophers
ethical_philosophers = ["aristotle", "levinas", "confucius", "arendt"]
po = PoSelf(philosophers=ethical_philosophers)

response = po.generate("What is the right action in this situation?")
```

### Existential Questions

```python
# Select existentialists
existentialists = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=existentialists)

response = po.generate("What is freedom?")
```

### Aesthetic Analysis

```python
# Select aesthetic and art philosophers
aesthetics = ["nietzsche", "wabi_sabi", "dewey"]
po = PoSelf(philosophers=aesthetics)

response = po.generate("What is the beauty of this work?")
```

### Language and Meaning Exploration

```python
# Select language philosophers
language_philosophers = ["wittgenstein", "derrida", "peirce"]
po = PoSelf(philosophers=language_philosophers)

response = po.generate("What does this word mean?")
```

## 📚 Next Steps

- **Detailed API Examples**: See `examples/api_demo.py`
- **Interactive Demo**: Try `examples/simple_demo.py`
- **Complete Documentation**: Refer to `/docs` directory
- **Philosopher Details**: Check specs for each philosopher in `/04_modules`

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'po_core'

```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/Po_core/src:$PYTHONPATH

# Or install in development mode
pip install "po-core-flyingpig==1.0.2"
```

### ImportError: No module named 'click' or 'rich'

```bash
# Reinstall package-managed dependencies from the source checkout
pip install -e .
```

---

## 🚀 REST API (Phase 5)

### Start with Docker (Recommended)

```bash
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# Configure environment
cp .env.example .env
# Recommended default: keep `PO_SKIP_AUTH=false` and set a non-empty `PO_API_KEY`
# Use `PO_SKIP_AUTH=true` only for short-lived local development when you intentionally want no auth

# Launch
docker compose up

# Explore the interactive Swagger UI
open http://localhost:8000/docs
```

### Start Locally

```bash
pip install "po-core-flyingpig==1.0.2"
export PO_API_KEY=dev-secret-key

python -m po_core.app.rest
# → http://localhost:8000
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/reason` | Synchronous philosophical reasoning (42 integrated philosophers, max 39 active on the default NORMAL path, then Pareto aggregation) |
| `POST` | `/v1/reason/stream` | SSE streaming reasoning (true async offload) |
| `GET`  | `/v1/philosophers` | Full 42-philosopher integrated manifest |
| `GET`  | `/v1/trace/{session_id}` | Per-session trace events |
| `GET`  | `/v1/health` | Health check (version + uptime) |

> Note: `PO_LLM_PROVIDER` / `PO_LLM_MODEL` choose backend routing for each philosopher.
> They do **not** decide philosopher count (count is controlled by SafetyMode + allowlist).

### Examples

```bash
# Synchronous reasoning (recommended default: auth enabled)
curl -X POST http://localhost:8000/v1/reason \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"input": "What is justice?", "philosophers": ["kant"]}'

# SSE streaming (true async, non-blocking event loop)
curl -N -X POST http://localhost:8000/v1/reason/stream \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"input": "What is the good life?"}'

# List the integrated philosopher manifest
curl -H "X-API-Key: dev-secret-key" http://localhost:8000/v1/philosophers

# Health check
curl http://localhost:8000/v1/health

# With API key authentication
curl -X POST http://localhost:8000/v1/reason \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"input": "What is freedom?"}'
```

### Environment Variables

Copy `.env.example` to `.env` and configure as needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `PO_API_KEY` | `""` | API key required when `PO_SKIP_AUTH=false`; blank values are a startup misconfiguration |
| `PO_SKIP_AUTH` | `false` | Recommended default is `false`; set `true` only for short-lived local development without auth |
| `PO_API_KEY_HEADER` | `X-API-Key` | Optional advanced override for the primary API-key header; `X-API-Key` remains accepted for backwards compatibility |
| `PO_CORS_ORIGINS` | `"*"` | Allowed CORS origins (prod: comma-separated) |
| `PO_RATE_LIMIT_PER_MINUTE` | `60` | Per-IP rate limit (req/min) |
| `PO_PORT` | `8000` | Server port |
| `PO_WORKERS` | `1` | uvicorn worker count |
| `PO_LOG_LEVEL` | `info` | Log level |

### ⚡ Performance (Phase 5-E Measured)

| Mode | Philosophers | p50 Latency | req/s |
|------|-------------|-------------|-------|
| NORMAL | 39 | ~33 ms | ~30 |
| WARN | 5 | ~34 ms | ~30 |
| CRITICAL | 1 | ~35 ms | ~29 |

5 concurrent WARN requests (via `asyncio.gather`): **181 ms** wall-clock

Run the benchmark suite yourself:

```bash
pytest tests/benchmarks/ -v -s -m benchmark
```

---

## 🤝 Feedback

For questions or suggestions:

- [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)

---

**🐷🎈 Flying Pig Philosophy**

"Pigs can't fly," they say. But maybe they can if we attach a balloon called philosophy.

*A frog in a well may not know the ocean, but it can know the sky*
