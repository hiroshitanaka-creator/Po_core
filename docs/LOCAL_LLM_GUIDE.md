# Po_core with Local LLMs

**Run Po_core completely offline without API costs**

This guide shows you how to run Po_core with local LLM models instead of cloud APIs.

---

## Table of Contents

- [Why Local LLMs?](#why-local-llms)
- [Option 1: Mock Philosophers (No LLM)](#option-1-mock-philosophers-no-llm)
- [Option 2: Ollama (Recommended)](#option-2-ollama-recommended)
- [Option 3: llama.cpp](#option-3-llamacpp)
- [Option 4: HuggingFace Transformers](#option-4-huggingface-transformers)
- [Performance Comparison](#performance-comparison)
- [Troubleshooting](#troubleshooting)

---

## Why Local LLMs?

### Advantages

✅ **Zero API Costs** - No per-token charges
✅ **Complete Privacy** - Data never leaves your machine
✅ **Offline Operation** - No internet required
✅ **Deterministic Testing** - Reproducible results
✅ **Development Friendly** - Fast iteration without API limits

### Trade-offs

⚠️ **Hardware Requirements** - Needs decent GPU/CPU
⚠️ **Setup Complexity** - Initial configuration needed
⚠️ **Model Quality** - May vary vs GPT-4/Claude
⚠️ **Speed** - Slower than cloud APIs (but improving)

---

## Option 1: Mock Philosophers (No LLM)

**Best for:** Testing visualizations, development, demonstrations

The fastest and simplest option - uses deterministic mock responses.

### Installation

Already included in Po_core! No additional setup needed.

### Usage

```python
from po_core.mock_philosophers import MockPoSelf
from po_core.visualizations import PoVisualizer

# Create mock Po_self
mock_po = MockPoSelf(enable_trace=True)

# Generate responses (no API needed!)
result = mock_po.generate("What is freedom?")

# Visualize
visualizer = PoVisualizer(po_trace=mock_po.po_trace)
visualizer.create_tension_map(
    session_id=result["log"]["session_id"],
    output_path="tension.png"
)
```

### Quick Demo

```bash
python examples/no_api_visualization_demo.py
```

### Features

- ✅ 20 mock philosophers with unique perspectives
- ✅ Deterministic metrics (same input = same output)
- ✅ Full tracing support
- ✅ Works with all visualization tools
- ❌ No actual reasoning (pre-defined responses)

---

## Option 2: Ollama (Recommended)

**Best for:** Real reasoning without API costs, good quality

Ollama provides an easy-to-use local LLM server with great models.

### Installation

1. **Install Ollama:**

   ```bash
   # macOS
   brew install ollama

   # Linux
   curl -fsSL https://ollama.com/install.sh | sh

   # Windows
   # Download from https://ollama.com/download
   ```

2. **Download a model:**

   ```bash
   # Recommended models for Po_core
   ollama pull llama3.1:8b      # Good balance (8GB RAM)
   ollama pull mistral:7b       # Fast (6GB RAM)
   ollama pull phi3:medium      # Lightweight (4GB RAM)
   ollama pull qwen2.5:14b      # High quality (12GB RAM)
   ```

3. **Start Ollama server:**

   ```bash
   ollama serve
   ```

### Usage with Po_core

Create `src/po_core/ollama_backend.py`:

```python
"""Ollama backend for Po_core."""
import requests
from typing import Dict, Optional


class OllamaPhilosopher:
    """Philosopher powered by Ollama local LLM."""

    def __init__(
        self,
        name: str,
        perspective: str,
        model: str = "llama3.1:8b",
        base_url: str = "http://localhost:11434"
    ):
        self.name = name
        self.perspective = perspective
        self.model = model
        self.base_url = base_url

    def generate_response(self, prompt: str) -> Dict:
        """Generate response using Ollama."""
        system_prompt = f"""You are {self.name}, the philosopher.
Your philosophical perspective: {self.perspective}

Respond to the user's question from your philosophical viewpoint.
Be concise but insightful. Include tension metrics:
- Freedom Pressure (0-1): Responsibility weight
- Semantic Delta (0-1): Meaning evolution
- Blocked Tensor (0-1): What remains unsaid
"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": f"{system_prompt}\n\nQuestion: {prompt}",
                "stream": False
            }
        )

        data = response.json()
        text = data.get("response", "")

        # Extract or estimate metrics
        # (In practice, you'd parse these from the response or estimate)
        import random
        return {
            "philosopher": self.name,
            "perspective": self.perspective,
            "response": text,
            "freedom_pressure": random.uniform(0.6, 0.9),
            "semantic_delta": random.uniform(0.4, 0.8),
            "blocked_tensor": random.uniform(0.2, 0.5),
        }
```

### Example

```python
from po_core.ollama_backend import OllamaPhilosopher

# Create Ollama-powered philosopher
aristotle = OllamaPhilosopher(
    name="Aristotle",
    perspective="Virtue Ethics",
    model="llama3.1:8b"
)

# Generate response
result = aristotle.generate_response("What is the good life?")
print(result["response"])
```

### Recommended Models

| Model | Size | RAM | Quality | Speed | Best For |
|-------|------|-----|---------|-------|----------|
| llama3.1:8b | 8B | 8GB | ★★★★☆ | ★★★☆☆ | General use |
| mistral:7b | 7B | 6GB | ★★★☆☆ | ★★★★☆ | Fast responses |
| phi3:medium | 14B | 12GB | ★★★★★ | ★★☆☆☆ | Quality reasoning |
| qwen2.5:14b | 14B | 12GB | ★★★★★ | ★★☆☆☆ | Best quality |

---

## Option 3: llama.cpp

**Best for:** Maximum performance, custom model fine-tuning

Direct C++ inference - fastest option for local execution.

### Installation

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build
make

# Or with GPU support (CUDA)
make LLAMA_CUBLAS=1
```

### Download Models

```bash
# Download GGUF format models
# Example: Llama 3.1 8B
wget https://huggingface.co/Meta-Llama/Llama-3.1-8B-Instruct-GGUF/resolve/main/llama-3.1-8b-instruct-q4_k_m.gguf
```

### Usage

```bash
# Run llama.cpp server
./llama-server -m llama-3.1-8b-instruct-q4_k_m.gguf -c 4096

# Compatible with OpenAI API format
# Point Po_core to http://localhost:8080
```

---

## Option 4: HuggingFace Transformers

**Best for:** Maximum control, research, custom models

Use HuggingFace's Transformers library directly in Python.

### Installation

```bash
pip install transformers torch accelerate
```

### Usage

```python
from transformers import pipeline

# Load model
generator = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.1-8B-Instruct",
    device_map="auto"
)

# Generate
response = generator(
    "What is freedom?",
    max_new_tokens=500,
    temperature=0.7
)
```

### Recommended Models

- `meta-llama/Llama-3.1-8B-Instruct` - 8B params, excellent
- `mistralai/Mistral-7B-Instruct-v0.3` - 7B params, fast
- `microsoft/Phi-3-medium-4k-instruct` - 14B params, quality

---

## Performance Comparison

### Speed (Tokens/Second)

| Method | Hardware | Speed | Cost/Hour |
|--------|----------|-------|-----------|
| GPT5.2thinking | Cloud | ★★★★★ | $0.05+ |
| opus4.5 | Cloud | ★★★★★ | $0.015+ |
| grok4.1thinking | Cloud | ★★★★☆ | $0.008+ |
| gemini3pro | Cloud | ★★★★★ | $0.002+ |
| **Ollama (GPU)** | RTX 3090 | ★★★★☆ | $0.00 |
| **llama.cpp (GPU)** | RTX 3090 | ★★★★★ | $0.00 |
| HuggingFace (GPU) | RTX 3090 | ★★★☆☆ | $0.00 |
| **Mock** | Any | ★★★★★ | $0.00 |

### Quality (Reasoning Depth)

| Method | Quality | Deterministic |
|--------|---------|---------------|
| GPT5.2thinking | ★★★★★ | ❌ |
| opus4.5 | ★★★★★ | ❌ |
| grok4.1thinking | ★★★★☆ | ❌ |
| gemini3pro | ★★★★★ | ❌ |
| Ollama (qwen2.5:14b) | ★★★★☆ | ✅ (with seed) |
| llama.cpp | ★★★★☆ | ✅ (with seed) |
| **Mock** | ★☆☆☆☆ | ✅ |

---

## Complete Example: Ollama Integration

Here's a complete example integrating Ollama with Po_core:

```python
"""Po_core with Ollama integration."""
from po_core.po_trace import PoTrace, EventType
from po_core.visualizations import PoVisualizer
import requests


class OllamaPoSelf:
    """Po_self using Ollama for local inference."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        enable_trace: bool = True
    ):
        self.model = model
        self.enable_trace = enable_trace
        self.po_trace = PoTrace() if enable_trace else None
        self.base_url = "http://localhost:11434"

    def generate(self, prompt: str, philosophers: list = None):
        """Generate philosophical response using Ollama."""
        if philosophers is None:
            philosophers = ["aristotle", "nietzsche", "sartre"]

        # Create session
        session_id = None
        if self.enable_trace:
            session_id = self.po_trace.create_session(
                prompt=prompt,
                philosophers=philosophers
            )

        # Query each philosopher
        responses = []
        for phil in philosophers:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"As {phil}, answer: {prompt}",
                    "stream": False
                }
            ).json()

            text = response.get("response", "")
            responses.append(text)

            # Log event
            if self.enable_trace:
                self.po_trace.log_event(
                    session_id=session_id,
                    event_type=EventType.EXECUTION,
                    source=f"philosopher.{phil}",
                    data={
                        "philosopher": phil,
                        "response": text,
                        "freedom_pressure": 0.75,  # Estimate
                        "semantic_delta": 0.60,
                        "blocked_tensor": 0.30,
                    }
                )

        ensemble = "\n\n".join(responses)

        return {
            "text": ensemble,
            "log": {"session_id": session_id}
        }


# Usage
po = OllamaPoSelf(model="llama3.1:8b")
result = po.generate("What is wisdom?")
print(result["text"])

# Visualize
visualizer = PoVisualizer(po_trace=po.po_trace)
visualizer.create_tension_map(
    session_id=result["log"]["session_id"],
    output_path="tension_ollama.png"
)
```

---

## Troubleshooting

### Ollama Connection Error

**Problem:** `Connection refused to localhost:11434`

**Solution:**

```bash
# Start Ollama server
ollama serve

# Or check if already running
ps aux | grep ollama
```

### Out of Memory

**Problem:** Model crashes or runs very slowly

**Solutions:**

1. Use smaller model: `ollama pull phi3:mini`
2. Reduce context length in request
3. Close other applications
4. Use quantized models (Q4, Q5 instead of FP16)

### Slow Performance

**Problem:** Responses take too long

**Solutions:**

1. Use GPU: Install CUDA toolkit
2. Use smaller model
3. Reduce max_tokens in request
4. Use llama.cpp instead of Ollama

### Model Quality Issues

**Problem:** Responses not philosophical enough

**Solutions:**

1. Improve system prompt
2. Use larger model (14B+)
3. Fine-tune model on philosophical texts
4. Use multiple reasoning steps

---

## Recommended Setup for Development

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download fast model for testing
ollama pull phi3:medium

# 3. Start server
ollama serve &

# 4. Test with mock first
python examples/no_api_visualization_demo.py

# 5. Then try Ollama
# (Use the OllamaPoSelf example above)
```

---

## Next Steps

1. **Start with Mock** - Test visualizations without any setup
2. **Try Ollama** - Get real reasoning locally
3. **Optimize** - Fine-tune models for philosophical reasoning
4. **Contribute** - Share your local LLM integration!

---

**🐷🎈 Flying pigs don't need cloud APIs!**

*"A frog in a well may not know the ocean, but it can know the local LLM."*
