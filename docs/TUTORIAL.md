# Po_core Tutorial: Your First Philosophy-Driven AI 🐷🎈

**Welcome to Po_core!** This hands-on tutorial will guide you through creating your first philosophy-driven AI application, step by step.

## What You'll Build

By the end of this tutorial, you'll have built:

1. A basic philosophical reasoning system
2. A custom philosopher selector
3. A simple ethical decision-making tool
4. An interactive philosophy explorer

**Time Required:** 30-45 minutes

---

## Prerequisites

- Python 3.9 or higher
- Basic Python knowledge
- Terminal/command line familiarity

---

## Part 1: Installation & Setup (5 minutes)

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/hiroshitanaka-creator/Po_core.git
cd Po_core

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Po_core
pip install -e .
```

### Step 2: Verify Installation

```bash
# Check the version
po-core version

# You should see something like:
# 🐷🎈 Po_core    v0.1.0-alpha
```

**✅ Checkpoint:** If you see the version output, you're ready to proceed!

---

## Part 2: Your First Philosophical Query (10 minutes)

### Step 3: Create Your First Script

Create a new file called `my_first_po.py`:

```python
#!/usr/bin/env python3
"""
My First Po_core Application
"""

from po_core.po_self import PoSelf

def main():
    # Step 1: Create a Po_self instance
    print("Initializing Po_core...")
    po = PoSelf()

    # Step 2: Ask a philosophical question
    question = "What is the nature of consciousness?"
    print(f"\nQuestion: {question}")

    # Step 3: Generate a response
    print("\nPhilosophers are deliberating...\n")
    response = po.generate(question)

    # Step 4: Display the results
    print("=" * 70)
    print(f"Consensus Leader: {response.consensus_leader}")
    print("=" * 70)
    print(f"\nAnswer:\n{response.text}\n")

    # Step 5: Examine the metrics
    print("Philosophical Metrics:")
    print(f"  Freedom Pressure: {response.metrics['freedom_pressure']:.3f}")
    print(f"  Semantic Delta:   {response.metrics['semantic_delta']:.3f}")
    print(f"  Blocked Tensor:   {response.metrics['blocked_tensor']:.3f}")

    print(f"\nParticipating Philosophers: {', '.join(response.philosophers)}")

if __name__ == "__main__":
    main()
```

### Step 4: Run It

```bash
python my_first_po.py
```

**🎉 Congratulations!** You've just run your first philosophy-driven AI query!

### Understanding the Output

- **Consensus Leader**: The philosopher whose perspective dominated the response
- **Freedom Pressure**: How much "responsibility weight" the response carries (0-1)
- **Semantic Delta**: How much meaning evolved during deliberation (0-1)
- **Blocked Tensor**: What was intentionally *not* said (0-1)

---

## Part 3: Customizing Philosopher Groups (10 minutes)

Now let's explore how different philosophers approach the same question differently.

### Step 5: Create a Comparison Script

Create `philosopher_comparison.py`:

```python
#!/usr/bin/env python3
"""
Comparing Different Philosophical Perspectives
"""

from po_core.po_self import PoSelf

def compare_perspectives(question):
    """Compare how different philosopher groups approach the same question"""

    # Define philosopher groups
    groups = {
        "Existentialists": ["sartre", "heidegger", "kierkegaard"],
        "Ethicists": ["aristotle", "confucius", "levinas"],
        "Pragmatists": ["dewey", "peirce"],
        "Eastern Wisdom": ["watsuji", "wabi_sabi", "zhuangzi"]
    }

    print(f"Question: {question}\n")
    print("=" * 70)

    for group_name, philosophers in groups.items():
        print(f"\n{group_name} Perspective:")
        print("-" * 70)

        # Create Po_self with specific philosophers
        po = PoSelf(philosophers=philosophers)
        response = po.generate(question)

        print(f"Leader: {response.consensus_leader}")
        print(f"Answer: {response.text[:200]}...")
        print(f"Freedom Pressure: {response.metrics['freedom_pressure']:.3f}")
        print()

def main():
    questions = [
        "How should we make ethical decisions?",
        "What is the meaning of happiness?",
        "What is authentic existence?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 70}")
        print(f"QUESTION {i}")
        print(f"{'=' * 70}\n")
        compare_perspectives(question)

        if i < len(questions):
            input("\nPress Enter to continue to the next question...")

if __name__ == "__main__":
    main()
```

### Step 6: Run the Comparison

```bash
python philosopher_comparison.py
```

**💡 Observation Exercise:**

- Notice how different groups emphasize different aspects
- Which group's "Freedom Pressure" is highest? Why might that be?
- Does the consensus leader change across groups?

---

## Part 4: Building an Ethical Decision Tool (10 minutes)

Let's build something practical: an ethical decision-making assistant.

### Step 7: Create an Ethical Advisor

Create `ethical_advisor.py`:

```python
#!/usr/bin/env python3
"""
Ethical Decision-Making Assistant
"""

from po_core.po_self import PoSelf
import json

class EthicalAdvisor:
    """An AI assistant for ethical decision-making"""

    def __init__(self):
        # Focus on ethics-specialized philosophers
        ethics_philosophers = [
            "aristotle",   # Virtue ethics
            "confucius",   # Moral cultivation
            "levinas",     # Ethics of the Other
            "arendt",      # Political ethics
            "dewey"        # Pragmatic ethics
        ]
        self.po = PoSelf(philosophers=ethics_philosophers)

    def analyze_situation(self, situation: str, options: list) -> dict:
        """Analyze an ethical dilemma"""

        # Construct the prompt
        prompt = f"""
        Ethical Situation: {situation}

        Available Options:
        {chr(10).join(f'{i+1}. {opt}' for i, opt in enumerate(options))}

        Please analyze this situation from multiple ethical frameworks
        and provide guidance on how to approach this decision.
        """

        # Get philosophical analysis
        response = self.po.generate(prompt)

        return {
            "situation": situation,
            "options": options,
            "analysis": response.text,
            "consensus_leader": response.consensus_leader,
            "ethical_weight": response.metrics['freedom_pressure'],
            "participating_philosophers": response.philosophers
        }

    def display_analysis(self, result: dict):
        """Display the ethical analysis"""
        print("\n" + "=" * 70)
        print("ETHICAL ANALYSIS")
        print("=" * 70)

        print(f"\nSituation: {result['situation']}\n")

        print("Options under consideration:")
        for i, opt in enumerate(result['options'], 1):
            print(f"  {i}. {opt}")

        print(f"\nPhilosophical Analysis:")
        print("-" * 70)
        print(result['analysis'])

        print(f"\n{'=' * 70}")
        print(f"Consensus Leader: {result['consensus_leader']}")
        print(f"Ethical Weight: {result['ethical_weight']:.3f}")
        print(f"Philosophers Consulted: {', '.join(result['participating_philosophers'])}")
        print("=" * 70)

def main():
    advisor = EthicalAdvisor()

    # Example ethical dilemma
    situation = """
    You are a software engineer and discover that your company's AI system
    has a bias that disadvantages certain demographic groups. Reporting it
    might delay the product launch and affect quarterly results.
    """

    options = [
        "Report the bias immediately to management and stakeholders",
        "Quietly fix it and say nothing to avoid causing alarm",
        "Wait until after launch and address it in the next version",
        "Document it thoroughly but let management decide the timing"
    ]

    print("\n🤔 Ethical Decision Assistant")
    print("Consulting with philosophical experts...\n")

    result = advisor.analyze_situation(situation, options)
    advisor.display_analysis(result)

    # Save the analysis
    with open('ethical_analysis.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n✅ Analysis saved to 'ethical_analysis.json'")

if __name__ == "__main__":
    main()
```

### Step 8: Run Your Ethical Advisor

```bash
python ethical_advisor.py
```

**🎯 Challenge:** Modify the script to analyze your own ethical dilemma!

---

## Part 5: Interactive Philosophy Explorer (5 minutes)

Let's create an interactive tool where you can ask any question.

### Step 9: Create an Interactive Explorer

Create `philosophy_explorer.py`:

```python
#!/usr/bin/env python3
"""
Interactive Philosophy Explorer
"""

from po_core.po_self import PoSelf
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

def display_welcome():
    """Display welcome message"""
    console.print("\n" + "=" * 70, style="bold blue")
    console.print("🐷🎈 Po_core Philosophy Explorer", style="bold blue", justify="center")
    console.print("=" * 70, style="bold blue")
    console.print("\n[italic]'A frog in a well may not know the ocean,")
    console.print("but it can know the sky.'[/italic]\n", justify="center")

def get_philosopher_choice():
    """Let user choose philosophers or use defaults"""
    choices = {
        "1": ("Default", None),
        "2": ("Existentialists", ["sartre", "heidegger", "kierkegaard"]),
        "3": ("Ethicists", ["aristotle", "confucius", "levinas", "arendt"]),
        "4": ("Eastern Wisdom", ["watsuji", "wabi_sabi", "confucius", "zhuangzi"]),
        "5": ("Language & Meaning", ["wittgenstein", "derrida", "peirce"]),
        "6": ("Aesthetics", ["nietzsche", "wabi_sabi", "dewey"])
    }

    console.print("\n[bold cyan]Choose a philosopher group:[/bold cyan]")
    for key, (name, _) in choices.items():
        console.print(f"  {key}. {name}")

    choice = Prompt.ask("\nYour choice", choices=list(choices.keys()), default="1")
    return choices[choice][1]

def main():
    display_welcome()

    # Choose philosophers
    philosophers = get_philosopher_choice()
    po = PoSelf(philosophers=philosophers) if philosophers else PoSelf()

    console.print("\n[green]✓[/green] Philosophy engine initialized!\n")

    while True:
        # Get question from user
        question = Prompt.ask("\n[bold yellow]Your philosophical question[/bold yellow]")

        if not question or question.lower() in ['exit', 'quit', 'q']:
            console.print("\n[dim]Thank you for exploring philosophy with Po_core![/dim]\n")
            break

        # Generate response
        console.print("\n[dim]Philosophers are deliberating...[/dim]\n")
        response = po.generate(question)

        # Display results
        console.print(Panel(
            f"[bold green]Leader:[/bold green] {response.consensus_leader}\n\n"
            f"[bold white]Answer:[/bold white]\n{response.text}",
            title="Philosophical Analysis",
            border_style="green"
        ))

        # Display metrics
        console.print(f"\n[dim]Freedom Pressure: {response.metrics['freedom_pressure']:.3f} | "
                     f"Semantic Delta: {response.metrics['semantic_delta']:.3f} | "
                     f"Blocked Tensor: {response.metrics['blocked_tensor']:.3f}[/dim]")

        # Ask if user wants to continue
        if not Confirm.ask("\n[cyan]Ask another question?[/cyan]", default=True):
            console.print("\n[dim]Thank you for exploring philosophy with Po_core![/dim]\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[dim]Goodbye![/dim]\n")
```

### Step 10: Launch the Explorer

```bash
python philosophy_explorer.py
```

**🚀 Try asking:**

- "What is the relationship between freedom and responsibility?"
- "How should we define justice in the digital age?"
- "What makes a life meaningful?"

---

## What You've Learned

Congratulations! You've learned how to:

✅ Initialize and use Po_core
✅ Generate philosophical responses
✅ Customize philosopher groups
✅ Compare different philosophical perspectives
✅ Build practical applications (ethical advisor)
✅ Create interactive philosophy tools

---

## Next Steps

### Explore More Features

1. **Web API Server**

   ```bash
   python examples/web_api_server.py
   # Visit http://localhost:8000
   ```

2. **Batch Processing**

   ```bash
   python examples/batch_analyzer.py
   ```

3. **Po_Party - Interactive Party Machine**

   ```bash
   po-core party
   ```

### Dive Deeper

- 📚 Read the [Complete Documentation](../README.md)
- 🎓 Study [Philosopher Specifications](../04_modules/)
- 🔬 Explore [Research Papers](../05_research/)
- 🛠️ Check [Advanced Examples](../examples/)

### Contribute

Found a bug? Have an idea? We'd love your contribution!

- [GitHub Issues](https://github.com/hiroshitanaka-creator/Po_core/issues)
- [Contributing Guide](../CONTRIBUTING.md)

---

## Troubleshooting

### Issue: Import errors

**Solution:**

```bash
# Make sure you're in the Po_core directory
export PYTHONPATH=$PWD/src:$PYTHONPATH
# Or reinstall
pip install -e .
```

### Issue: Philosophers not responding as expected

**Solution:** Check that you're using valid philosopher keys. See the [philosopher list](../QUICKSTART_EN.md#available-philosophers).

### Issue: Performance is slow

**Solution:** Disable tracing for faster responses:

```python
po = PoSelf(enable_trace=False)
```

---

## Get Help

- 📧 Email: <flyingpig0229+github@gmail.com>
- 💬 [GitHub Discussions](https://github.com/hiroshitanaka-creator/Po_core/discussions)
- 📚 [Documentation](../README.md)

---

**🐷🎈 Flying Pig Philosophy**

*"If you deny possibilities for pigs, don't eat pork."*

Welcome to the community of philosophers and engineers building AI that thinks deeply!
