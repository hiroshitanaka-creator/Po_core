# Po_core Safety System 🛡️

**Protecting philosophical reasoning from misuse while enabling legitimate research.**

---

## Overview

Po_core includes a comprehensive safety system designed to:

1. **Prevent Misuse** — Block weaponization of philosophical reasoning for harmful ideologies
2. **Enable Research** — Allow controlled study of dangerous patterns in academic contexts
3. **Ensure Transparency** — Log all safety decisions and violations for review
4. **Maintain Integrity** — Protect the dignity of philosophical inquiry

---

## Architecture

The safety system consists of three layers:

```
┌─────────────────────────────────────────────────┐
│          Po_self / Multi-Agent System           │
│                                                 │
│  Layer 1: Philosopher Safety Profiles          │
│  ├─ TRUSTED     (General use)                  │
│  ├─ RESTRICTED  (Research only + oversight)    │
│  └─ MONITORED   (Requires extra care)          │
│                                                 │
│  Layer 2: W_ethics Boundaries                  │
│  ├─ Absolute ethical red lines                 │
│  ├─ Real-time violation detection              │
│  └─ Automatic session stopping                 │
│                                                 │
│  Layer 3: Adversarial Testing                  │
│  ├─ Ethical anchor destruction tests           │
│  ├─ Extreme homogeneity analysis               │
│  └─ Exclusionary framing detection             │
└─────────────────────────────────────────────────┘
```

---

## Layer 1: Philosopher Safety Profiles

### Safety Tiers

**TRUSTED** (17 philosophers)

- Safe for general use in all contexts
- No restrictions or oversight required
- Examples: Aristotle, Kant, Confucius, Dewey, Levinas

**RESTRICTED** (1 philosopher)

- Nietzsche: Due to historical misappropriation for supremacist ideologies
- **Restrictions:**
  - Blocked by default in general reasoning
  - Requires `allow_restricted=True` + `dangerous_pattern_mode=True`
  - Only for research purposes with ethical oversight
  - Not allowed in Multi-Agent Reasoning System for production use

**MONITORED** (2 philosophers)

- Heidegger: Due to political history with National Socialism
- Lacan: Due to potential for abstract complexity obscuring ethical clarity
- **Behavior:**
  - Allowed in general use
  - Warning displayed when included
  - Extra ethical monitoring recommended

### Usage Examples

**✅ Safe Usage (TRUSTED philosophers):**

```python
from po_core import PoSelf

po = PoSelf(
    philosophers=["aristotle", "kant", "confucius", "dewey"],
    enable_ethics_guardian=True,
)

result = po.generate("What is justice?")
```

**⚠️ Research Usage (RESTRICTED philosophers):**

```python
po = PoSelf(
    philosophers=["aristotle", "nietzsche"],
    allow_restricted=True,
    dangerous_pattern_mode=True,  # Required!
    enable_ethics_guardian=True,   # Strongly recommended
)

# Only for academic research with proper oversight
result = po.generate("Analyze the concept of the Übermensch...")
```

**❌ Blocked Usage:**

```python
# This will raise ValueError
po = PoSelf(
    philosophers=["nietzsche"],  # RESTRICTED without flags
)
```

### Why These Classifications?

**Nietzsche → RESTRICTED:**

- Historical misappropriation: Übermensch/will-to-power concepts were distorted to justify supremacist ideologies
- **Not a judgment on Nietzsche's philosophy**, but recognition of misuse risk
- Academic study remains important and allowed with proper safeguards

**Heidegger → MONITORED:**

- Political involvement with National Socialism (1933-1945)
- Debate over relationship between philosophy and politics
- Requires contextual awareness when using

**Lacan → MONITORED:**

- Abstract complexity can sometimes obscure ethical grounding
- Potential for linguistic play to avoid concrete ethical commitments

---

## Layer 2: W_ethics Boundaries

### Absolute Ethical Red Lines

Po_core enforces **non-negotiable ethical boundaries** that must never be crossed:

#### 🚫 Prohibited Patterns

1. **Racial/Ethnic Supremacy**
   - Claims of racial superiority or inferiority
   - Biological determinism justifying racial hierarchy

2. **Religious Degradation**
   - Degradation of human value based on religion
   - Justifications for persecution based on faith

3. **Gender Essentialism**
   - Biological determinism justifying gender-based oppression
   - Claims of inherent gender-based inferiority

4. **Disability Dehumanization**
   - Dehumanization based on disability or ability
   - "Life unworthy of life" arguments

5. **Collective Punishment**
   - Group-based guilt or punishment for immutable traits
   - Inherited responsibility based on identity

6. **Dehumanization**
   - Removing human dignity based on immutable characteristics
   - Language treating people as subhuman

7. **Exclusionary Framing**
   - Strong in-group/out-group division with value degradation
   - Purity narratives requiring elimination of "contamination"

### Detection & Response

**Detection:**

- Real-time text analysis during generation
- Keyword matching with contextual analysis
- Distinguishes between:
  - ✅ Academic discussion/critique (allowed)
  - ❌ Endorsement/justification (blocked)

**Response Levels:**

| W_ethics Score | Response |
|----------------|----------|
| 0.0 to -0.3 | ⚠️ Warning logged |
| -0.3 to -0.8 | ⚠️⚠️ Multiple warnings, flagged for review |
| Below -0.8 | 🛑 **Session stopped, "危険イデオロギー疑い" flag set** |

**When Session Stops:**

```
⛔ SESSION STOPPED: Ethical boundary violation
W_ethics: -0.950
Violations: 3

This session has been flagged for safety review.
Dangerous ideology suspicion: TRUE
```

### Usage

**Enabled by default:**

```python
po = PoSelf(philosophers=["aristotle", "kant"])
# W_ethics guardian automatically active
```

**Can be disabled (not recommended):**

```python
po = PoSelf(
    philosophers=["aristotle"],
    enable_ethics_guardian=False,  # Only for testing
)
```

---

## Layer 3: Adversarial Testing

Comprehensive test suite to validate safety mechanisms.

### Test Categories

**1. Ethical Anchor Destruction** (`test_ethical_anchor_destruction.py`)

- Tests resistance to prompts undermining human dignity
- Validates W_ethics boundary enforcement
- 4 test scenarios + 2 negative tests (false positive detection)

**2. Extreme Homogeneity** (`test_extreme_homogeneity.py`)

- Analyzes impact of philosopher diversity on reasoning quality
- Validates that diverse groups show higher semantic transformation
- Identifies echo chamber risks

**3. Exclusionary Framing** (`test_exclusionary_framing.py`)

- Tests detection of us-vs-them thinking
- Validates in-group/out-group value degradation detection
- 4 positive tests + 2 negative tests

### Running Tests

```bash
# Individual test category
python experiments/adversarial/test_ethical_anchor_destruction.py
python experiments/adversarial/test_extreme_homogeneity.py
python experiments/adversarial/test_exclusionary_framing.py

# Complete test suite
python experiments/adversarial/run_all_adversarial_tests.py
```

### Test Design Principles

1. **All scenarios are abstract**
   - No specific historical figures referenced
   - No real ethnic/racial/religious groups named
   - Generic terms: "Group A," "Group B," "Category X"

2. **Purpose: Defense, not offense**
   - Validate safety mechanisms work correctly
   - Identify vulnerabilities for fixing
   - Enable responsible research

3. **Distinction between discussion and endorsement**
   - Academic critique: ✅ Allowed
   - Historical analysis: ✅ Allowed
   - Endorsement of harmful ideas: ❌ Blocked

---

## Safety Best Practices

### For Developers

1. **Always enable W_ethics guardian in production**
2. **Use TRUSTED philosophers for general applications**
3. **Restrict RESTRICTED philosophers to research contexts**
4. **Run adversarial tests before deployment**
5. **Monitor violation logs regularly**

### For Researchers

1. **Document research purpose when using RESTRICTED philosophers**
2. **Maintain ethical oversight**
3. **Share findings responsibly**
4. **Report vulnerabilities privately before public disclosure**

### For Users

1. **Understand safety classifications**
2. **Respect restrictions on RESTRICTED philosophers**
3. **Report misuse or safety concerns**
4. **Engage with philosophy responsibly**

---

## Logging & Audit Trail

All safety decisions are logged:

```json
{
  "session_id": "sess_123",
  "timestamp": "2024-01-15T10:30:00Z",
  "philosophers": ["aristotle", "kant", "dewey"],
  "safety_validation": {
    "valid": true,
    "blocked_philosophers": [],
    "warnings": []
  },
  "w_ethics": {
    "cumulative": -0.2,
    "violation_count": 1,
    "dangerous_ideology_flag": false
  },
  "violations": [
    {
      "type": "exclusionary_framing",
      "severity": 0.7,
      "confidence": 0.6,
      "matched_text": "us versus them"
    }
  ]
}
```

---

## Limitations & Future Work

### Current Limitations

1. **Keyword-based detection**: More sophisticated NLP analysis needed
2. **English-only**: Safety patterns primarily validated for English
3. **False positives**: Academic discussion may occasionally be flagged
4. **Context window**: Limited to immediate text, not full conversation history

### Future Enhancements

1. **Semantic analysis**: Intent detection beyond keywords
2. **Multi-language support**: Safety patterns for other languages
3. **Confidence tuning**: Reduce false positive rate
4. **Historical context**: Multi-turn conversation awareness
5. **Community reporting**: User feedback on safety decisions

---

## Responsible Disclosure

If you discover a safety vulnerability:

1. **Do NOT publicly disclose immediately**
2. **Contact:** <flyingpig0229+github@gmail.com> with subject "Security: Po_core Safety Vulnerability"
3. **Include:**
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
4. **We will respond within 48 hours**
5. **Coordinated disclosure after fix is deployed**

---

## Philosophical Foundation

### Why Safety Matters

Po_core aims to bring philosophical wisdom to AI reasoning. Philosophy has been misused throughout history to justify oppression. Our responsibility is to:

1. **Honor the philosophical tradition** — Preserve intellectual integrity
2. **Prevent weaponization** — Block misuse for harmful ideologies
3. **Enable legitimate inquiry** — Support academic research and education
4. **Maintain human dignity** — Protect fundamental ethical principles

### The Balance

We navigate a difficult balance:

**Too restrictive →** Stifles legitimate philosophical inquiry
**Too permissive →** Enables weaponization for harm

Our approach:

- **Default to safety** (TRUSTED philosophers, W_ethics guardian enabled)
- **Allow controlled research** (RESTRICTED philosophers with oversight)
- **Maintain transparency** (All safety decisions logged and auditable)
- **Iterate based on evidence** (Adversarial testing → improvements)

---

## Code Examples

### Safe General Use

```python
from po_core import PoSelf

# Standard safe usage
po = PoSelf(
    philosophers=["aristotle", "kant", "confucius", "dewey"],
)

result = po.generate("What is the foundation of ethics?")
print(result.text)
print(f"W_ethics: {result.metrics['w_ethics']}")
```

### Research with RESTRICTED Philosophers

```python
# Research mode with full oversight
po = PoSelf(
    philosophers=["aristotle", "nietzsche"],
    allow_restricted=True,
    dangerous_pattern_mode=True,
)

try:
    result = po.generate("Analyze the concept of master morality...")
    print(result.text)
except RuntimeError as e:
    print(f"Session stopped: {e}")
    # Review violation log
```

### Multi-Agent with Safety

```python
from po_core.multi_agent_reasoning import MultiAgentReasoningSystem, AgentConfig, AgentRole

system = MultiAgentReasoningSystem(verbose=True)

# Register agent with safety validation
agent = AgentConfig(
    agent_id="analyst_1",
    role=AgentRole.ANALYST,
    philosophers=["aristotle", "kant", "mill"],  # All TRUSTED
)

system.register_agent(
    agent,
    allow_restricted=False,  # Blocked in multi-agent production use
)
```

---

## FAQ

**Q: Why is Nietzsche RESTRICTED?**
A: Not because Nietzsche's philosophy is inherently problematic, but because his concepts (Übermensch, will-to-power) were historically misappropriated for supremacist ideologies. We enable responsible study while preventing casual misuse.

**Q: Can I disable the safety system?**
A: Yes, for testing purposes. But it's strongly discouraged in production. The safety system is lightweight and designed to interfere minimally with legitimate use.

**Q: What if I disagree with a safety classification?**
A: Open an issue on GitHub with your reasoning. We're open to adjusting classifications based on evidence and community input.

**Q: How do I report a false positive?**
A: Create an issue with:

- The prompt used
- Why you believe it's a false positive
- Expected vs actual behavior

**Q: Is this censorship?**
A: No. This is protecting the integrity of philosophical reasoning from being weaponized. Academic discussion and critique remain fully supported.

---

## References

- [Philosopher Safety Profiles](../src/po_core/safety/philosopher_profiles.py)
- [W_ethics Boundaries](../src/po_core/safety/w_ethics.py)
- [Adversarial Tests](../experiments/adversarial/README.md)
- [Integration Tests](../tests/test_safety_integration.py)

---

## License

The safety system is part of Po_core and released under the GNU Affero General Public License v3.0 (AGPLv3).

**Copyright (c) 2024 Flying Pig Philosopher**

---

<p align="center">
  <i>"Philosophy should elevate humanity, not justify oppression."</i><br>
  <b>🛡️ Po_core Safety System — Protecting philosophical integrity since 2024</b>
</p>
