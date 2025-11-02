# Contributing to Po_core 🐷🎈

> "A frog in a well may not know the ocean, but it can know the sky."

Thank you for your interest in contributing to Po_core! This project is built on the **Flying Pig Philosophy**: we hypothesize boldly, verify rigorously, and revise gracefully.

---

## Table of Contents

1. [Our Philosophy](#our-philosophy)
2. [Ways to Contribute](#ways-to-contribute)
3. [Getting Started](#getting-started)
4. [Development Workflow](#development-workflow)
5. [Philosophical Contributions](#philosophical-contributions)
6. [Code Guidelines](#code-guidelines)
7. [Testing Requirements](#testing-requirements)
8. [Documentation Standards](#documentation-standards)
9. [Pull Request Process](#pull-request-process)
10. [Community Guidelines](#community-guidelines)

---

## Our Philosophy

### Flying Pig Philosophy: Three Tenets

**One: Hypothesize Boldly**  
The impossible becomes possible only when someone dares to formalize it. Don't ask "Can we?" Ask "What would it take?"

**Two: Verify Rigorously**  
Bold hypotheses demand brutal testing. Every claim must survive philosophical scrutiny, mathematical proof, and empirical validation.

**Three: Revise Gracefully**  
When experiments fail, don't hide them. Publish them. Failure logs become learning signals. The pig might crash, but we improve the balloon.

### What This Means for Contributors

- **No idea is too ambitious** — If you can formalize it, we want to hear it
- **All failures are valuable** — Document what didn't work and why
- **Transparency is paramount** — We publish everything, including our mistakes
- **Philosophy meets engineering** — Both are equally important here

---

## Ways to Contribute

Po_core welcomes contributions across multiple dimensions:

### 🧠 Philosophical Contributions
- Propose new philosopher integrations
- Refine existing philosophical tensor models
- Challenge our philosophical assumptions
- Suggest ethical frameworks

### 💻 Technical Contributions
- Implement core features
- Optimize tensor operations
- Improve API design
- Enhance visualization systems

### 📚 Documentation
- Translate documentation (especially philosophical concepts)
- Write tutorials and examples
- Create educational content
- Improve API documentation

### 🎨 Design & Visualization
- Design Po_core Viewer interfaces
- Create philosophical concept visualizations
- Improve UX/UI

### 🐛 Bug Reports & Testing
- Report bugs with detailed reproduction steps
- Write test cases
- Validate philosophical consistency
- Test edge cases

### 💬 Community
- Answer questions in discussions
- Share use cases and applications
- Write blog posts or papers
- Organize study groups

---

## Getting Started

### Prerequisites

**Required:**
- Python 3.9+
- Basic understanding of tensors and PyTorch
- Curiosity about philosophy (we'll help you learn!)

**Helpful:**
- Familiarity with FastAPI
- Knowledge of at least one philosopher we integrate
- Experience with philosophical argumentation

### Installation

```bash
# Fork and clone the repository
git clone https://github.com/[your-username]/po_core.git
cd po_core

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools

# Run tests to verify installation
pytest tests/
```

### Project Structure

```
Po_core/
├── src/
│   ├── po_core/          # Core system
│   ├── po_self/          # Philosophical ensemble
│   ├── po_trace/         # Audit logging
│   └── po_viewer/        # Visualization
├── tests/
├── docs/
│   ├── design/           # 120+ design documents
│   ├── philosophy/       # Philosophical foundations
│   └── api/              # API documentation
├── examples/
└── scripts/
```

---

## Development Workflow

### 1. Find or Create an Issue

**Before starting work:**
- Check existing issues
- For new features, create an issue to discuss first
- For bug fixes, create an issue with reproduction steps

**Issue Types:**
- `feature`: New functionality
- `bug`: Something isn't working
- `philosophy`: Philosophical design questions
- `documentation`: Documentation improvements
- `performance`: Optimization opportunities

### 2. Create a Branch

```bash
# Create a feature branch from main
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Convention:**
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation
- `refactor/` — Code refactoring
- `philosophy/` — Philosophical design changes

### 3. Make Your Changes

```bash
# Make changes and commit regularly
git add .
git commit -m "feat: add Nietzsche's eternal recurrence tensor"

# Follow conventional commits format
# Types: feat, fix, docs, style, refactor, test, chore
```

### 4. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/philosophical/  # Philosophical consistency tests

# Check code style
black src/ tests/
flake8 src/ tests/
mypy src/
```

### 5. Update Documentation

```bash
# If you added new functionality:
# - Update relevant docs in docs/
# - Add docstrings to all functions
# - Update API documentation
# - Add examples if appropriate
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Philosophical Contributions

### Adding a New Philosopher

Po_core currently integrates 10-11 philosophers. Adding a new one is significant and requires careful design.

#### Step 1: Philosophical Justification

Create a design document (in `docs/philosophy/proposals/`) that addresses:

1. **Why this philosopher?**
   - What unique perspective do they bring?
   - What gaps in current philosophical coverage do they fill?

2. **Conceptual Framework**
   - What are their core concepts?
   - How do these concepts relate to AI reasoning?
   - What philosophical tensions exist with current philosophers?

3. **Mathematical Formalization**
   - How can their concepts be expressed as tensors?
   - What are the key variables and relationships?
   - How will they interact with existing tensors?

#### Step 2: Tensor Design

Define the philosopher's contribution as mathematical structures:

```python
class NietzscheTensor:
    """
    Eternal Recurrence Tensor
    Measures cyclic patterns in reasoning chains
    """
    def __init__(self, dimensions: int = 768):
        self.eternal_return_weight = torch.zeros(dimensions)
        self.power_will_vector = torch.zeros(dimensions)
        
    def compute_recurrence_pressure(
        self, 
        current_state: torch.Tensor,
        historical_states: List[torch.Tensor]
    ) -> float:
        """
        Calculate how much current reasoning echoes past patterns
        """
        # Implementation here
        pass
```

#### Step 3: Integration Design

Document how the new philosopher interacts with existing ones:

- **Resonance patterns:** Which philosophers amplify this one?
- **Conflict patterns:** Which philosophers create productive tension?
- **Decision influence:** How does this philosopher affect `priority_score`?

#### Step 4: Validation

Before implementation:
- Present design to community for feedback
- Demonstrate philosophical consistency
- Justify computational feasibility

---

## Code Guidelines

### Python Style

We follow PEP 8 with some project-specific conventions:

```python
# Good: Clear philosophical naming
def calculate_freedom_pressure(
    choice_tensors: List[torch.Tensor],
    responsibility_weight: float
) -> torch.Tensor:
    """
    Calculate Sartrean freedom pressure across choice space.
    
    Based on Sartre's concept that we are "condemned to be free"
    and must bear responsibility for our choices.
    
    Args:
        choice_tensors: Available semantic choices
        responsibility_weight: Ethical gravity of the decision
        
    Returns:
        Pressure tensor indicating responsibility burden
    """
    pass

# Bad: Opaque naming
def calc_fp(ct, rw):
    pass
```

### Philosophical Concepts in Code

When implementing philosophical concepts:

1. **Always include philosophical context in docstrings**
2. **Reference source texts when possible**
3. **Explain the formalization choices**

Example:

```python
class DerridaTrace:
    """
    Implements Derrida's concept of 'trace' (la trace).
    
    Philosophical Background:
    Derrida argues that meaning is never fully present but always 
    contains traces of what it is not. In Po_core, this manifests as
    the blocked_tensor - what was NOT said but influenced the response.
    
    Reference: 
    - Derrida, J. (1967). "Of Grammatology"
    - Implementation based on Po_core design doc v1.2
    """
    pass
```

### Naming Conventions

- **Classes:** `PascalCase` (e.g., `FreedomPressureTensor`)
- **Functions:** `snake_case` (e.g., `calculate_semantic_delta`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_PHILOSOPHER_COUNT`)
- **Private methods:** `_leading_underscore` (e.g., `_internal_calculation`)

---

## Testing Requirements

### Test Categories

#### 1. Unit Tests
```python
# tests/unit/test_freedom_pressure.py
def test_freedom_pressure_increases_with_choice_count():
    """Freedom pressure should increase with more choices."""
    tensor_calc = FreedomPressureTensor()
    
    few_choices = [torch.randn(768) for _ in range(2)]
    many_choices = [torch.randn(768) for _ in range(10)]
    
    fp_few = tensor_calc.calculate(few_choices)
    fp_many = tensor_calc.calculate(many_choices)
    
    assert fp_many > fp_few
```

#### 2. Integration Tests
Test interactions between components:
```python
# tests/integration/test_philosopher_interaction.py
def test_sartre_derrida_tension():
    """Sartre's freedom and Derrida's trace should create tension."""
    po_self = PoSelf()
    response = po_self.generate("Should I speak?")
    
    assert response.freedom_pressure > 0
    assert len(response.blocked_tensor) > 0
    assert response.philosophical_tension > THRESHOLD
```

#### 3. Philosophical Consistency Tests
```python
# tests/philosophical/test_consistency.py
def test_philosopher_axioms():
    """Verify each philosopher's core axioms are preserved."""
    heidegger = HeideggerDasein()
    
    # Dasein always involves being-toward-death
    state = heidegger.compute_state(context)
    assert state.temporal_finitude > 0
```

### Coverage Requirements

- **Minimum coverage:** 80%
- **Core philosophical modules:** 95%
- **All public APIs:** 100%

Run coverage report:
```bash
pytest --cov=src --cov-report=html
```

---

## Documentation Standards

### Code Documentation

```python
def semantic_jump(
    from_state: torch.Tensor,
    to_state: torch.Tensor,
    jump_type: JumpType
) -> SemanticDelta:
    """
    Calculate semantic distance and meaning shift between states.
    
    Philosophical Context:
    Based on Heidegger's concept of ontological leaps where 
    meaning shifts qualitatively, not just quantitatively.
    
    Args:
        from_state: Source semantic state vector (768-dim)
        to_state: Target semantic state vector (768-dim)
        jump_type: Type of semantic transition
        
    Returns:
        SemanticDelta containing:
            - distance: Magnitude of meaning shift
            - direction: Vector of meaning change
            - quality: Qualitative jump assessment
            
    Example:
        >>> from_state = encode_text("I should help")
        >>> to_state = encode_text("I must help")
        >>> delta = semantic_jump(from_state, to_state, JumpType.ETHICAL)
        >>> delta.distance
        0.42
        
    References:
        - Design doc: docs/design/semantic_jumps_v2.md
        - Heidegger, M. (1927). "Being and Time", §31
    """
    pass
```

### Design Documents

When creating new design documents:

**Required Sections:**
1. **Philosophical Motivation** — Why is this needed?
2. **Conceptual Framework** — What are the key ideas?
3. **Mathematical Formalization** — How is it expressed mathematically?
4. **Implementation Strategy** — How will it be built?
5. **Validation Criteria** — How do we know it works?
6. **Failure Modes** — What could go wrong?
7. **References** — What sources inform this?

---

## Pull Request Process

### PR Checklist

Before submitting a PR, ensure:

- [ ] **Code compiles and runs**
- [ ] **All tests pass** (`pytest`)
- [ ] **Code style checked** (`black`, `flake8`)
- [ ] **Type hints added** (`mypy` passes)
- [ ] **Documentation updated**
- [ ] **Philosophical justification provided** (if applicable)
- [ ] **Examples added** (if new feature)
- [ ] **Changelog updated**

### PR Template

When creating a PR, use this template:

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Philosophical Context
(If applicable) What philosophical concepts does this involve?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Philosophical refinement

## Testing
Describe tests added/modified

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code style verified
- [ ] Philosophical consistency checked

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks** — CI/CD runs tests, style checks
2. **Philosophical Review** — Core team reviews philosophical soundness
3. **Technical Review** — Code quality and architecture review
4. **Community Feedback** — Open for community comments
5. **Approval & Merge** — Requires 2 approvals from maintainers

**Review Timeline:**
- Simple fixes: 1-3 days
- New features: 1-2 weeks
- Philosophical changes: 2-4 weeks (requires deeper discussion)

---

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inspiring community for all. We expect:

- **Respect:** Treat everyone with respect, even in philosophical disagreements
- **Openness:** Welcome diverse perspectives and backgrounds
- **Collaboration:** Work together toward common goals
- **Intellectual Honesty:** Admit when you're wrong; document failures
- **Constructive Criticism:** Criticize ideas, not people

### Communication Channels

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** General questions, philosophical debates
- **Pull Requests:** Code contributions and reviews
- **Email:** flyingpig0229+github@gmail.com for private matters

### Philosophical Disagreements

Po_core is built on diverse philosophical perspectives. Disagreements are expected and valued:

**How to Engage in Philosophical Debate:**

1. **Cite sources** — Reference philosophical texts
2. **Define terms** — Ensure conceptual clarity
3. **Show respect** — Philosophical opponents can teach us
4. **Seek synthesis** — Can competing views coexist productively?
5. **Document outcomes** — Even unresolved debates are valuable

**Example:**
```markdown
I disagree with the current implementation of Heideggerian Dasein
because it emphasizes being-toward-death but neglects being-with-others 
(Mitsein). See Heidegger's "Being and Time" §26.

Proposed modification: Add a relational tensor that captures...
```

### Recognition

Contributors are recognized in:
- **CONTRIBUTORS.md** — All contributors listed
- **Release notes** — Significant contributions highlighted
- **Documentation** — Authors cited in design docs
- **Research papers** — Co-authorship on related publications

---

## Specific Contribution Areas

### For Philosophers

**You don't need to code!** Your philosophical expertise is valuable:

- Review philosophical accuracy of implementations
- Suggest conceptual refinements
- Write philosophical justifications
- Critique tensor formalizations
- Translate philosophical concepts to mathematical structures

### For Engineers

**You don't need a philosophy degree!** Your technical skills are crucial:

- Implement tensor operations
- Optimize performance
- Build APIs and interfaces
- Write tests and documentation
- Improve infrastructure

### For Designers

- Design visualization interfaces for Po_core Viewer
- Create diagrams explaining philosophical concepts
- Improve documentation layout and readability
- Design educational materials

### For Skeptics

**We especially welcome skeptics!**

- Challenge our assumptions
- Point out philosophical inconsistencies
- Identify practical limitations
- Propose alternative approaches
- Document what doesn't work

Your criticism makes the project stronger. We publish failures, remember?

---

## Getting Help

### Where to Ask Questions

- **GitHub Discussions:** For general questions and ideas
- **Issue Comments:** For questions about specific issues
- **Discord** (coming soon): For real-time chat
- **Email:** For private inquiries

### Resources

- **[Project Documentation](./docs/)** — Start here
- **[Design Documents](./docs/design/)** — Deep dives into architecture
- **[Manifesto](./docs/MANIFESTO.md)** — Our philosophy and motivation
- **[Philosophy Guide](./docs/philosophy/)** — Understanding each philosopher
- **[Examples](./examples/)** — Code examples

---

## License

By contributing to Po_core, you agree that your contributions will be licensed under the MIT License.

---

## Final Words

> "They said pigs can't fly. I attached a balloon to one."

Contributing to Po_core means joining an experiment. We're attempting something that conventional wisdom says is impossible: building AI on philosophy rather than just data.

You might be a philosopher who thinks we're oversimplifying complex concepts. Good — tell us how to do it right.

You might be an engineer who thinks this is computationally infeasible. Good — help us prove otherwise or document why not.

You might be a skeptic who thinks this whole endeavor is misguided. Excellent — challenge us to justify every decision.

**Whatever path you take, unique scenery and emotions await that only that route can offer.**

We're looking up at the sky from the bottom of a well. We may not know the ocean, but we can see the stars.

Welcome aboard. Let's make pigs fly. 🐷🎈

---

**Questions? Ideas? Criticisms?**  
Open an issue or join the discussion. We're excited to hear from you.

---

*Po_core: When you must say "Leave it to me," we stand beside you.*
