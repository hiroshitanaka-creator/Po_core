# Po_core Quick Start 🐷🎈

A quick guide to get started with Po_core's philosophy-driven AI system.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# Install required dependencies
pip install click rich

# Install in development mode (recommended)
pip install -e .
```

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
# Existentialist group
philosophers = ["sartre", "heidegger", "kierkegaard"]
po = PoSelf(philosophers=philosophers)

response = po.generate("What is existence?")
print(response.text)
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

Po_core provides 20 philosophers:

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
pip install -e .
```

### ImportError: No module named 'click' or 'rich'

```bash
# Install required dependencies
pip install click rich
```

## 🤝 Feedback

For questions or suggestions:
- [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)

---

**🐷🎈 Flying Pig Philosophy**

"Pigs can't fly," they say. But maybe they can if we attach a balloon called philosophy.

*A frog in a well may not know the ocean, but it can know the sky*
