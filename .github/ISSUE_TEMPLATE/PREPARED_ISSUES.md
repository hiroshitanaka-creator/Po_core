# Prepared GitHub Issues — Community Activation (M1 → M4)

These issues are ready to be filed on GitHub to activate the Philosophy Track
and Bridge Track communities.  File them in order; each links to the next.

Labels to create first:
- `phil-easy` (purple) — philosophy knowledge, no coding required
- `bridge` (teal) — philosophy + Python basics
- `ai-easy` (blue) — AI/ML, philosophy interest
- `research` (orange) — academic collaboration
- `good-first-issue` (green) — already exists

---

## Issue #22: [Phil-Easy] Which philosopher should we add next?

**Labels:** `phil-easy`, `good-first-issue`, `philosophy`
**Milestone:** M2

```markdown
## Which philosopher should we add to Po_core's ensemble next?

Po_core currently has 39 philosopher AI personas:
Aristotle, Kant, Bentham, Mill, Rawls, Hegel, Nietzsche, Heidegger, Sartre,
Camus, de Beauvoir, Arendt, Wittgenstein, Peirce, Dewey, Habermas, Foucault,
Derrida, Baudrillard, Zizek, Spinoza, Leibniz, Descartes, Locke, Hume,
Rousseau, Marx, Freud, Jung, Confucius, Laozi, Nagarjuna, Nishida, Watsuji,
Dogen, Suzuki, Mulla Sadra, Rumi, Ibn Rushd.

**What's missing?** We'd love contributions from:
- **African philosophy** (Ubuntu ethics, Kwame Gyekye)
- **Indigenous / land-based ethics** (Robin Wall Kimmerer)
- **Feminist ethics** (Carol Gilligan, Nel Noddings, María Lugones)
- **Pragmatist ethics** (Cornel West)
- **Buddhist-Christian dialogue** (Thomas Merton, Thich Nhat Hanh)
- **Environmental ethics** (Aldo Leopold, Holmes Rolston III)

### How to contribute (no coding required)
1. Comment with your philosopher proposal
2. Include: name, tradition, 3–5 key concepts, and how they'd enrich ethical deliberation
3. We'll map it to tensor weights and implement it!

See `src/po_core/philosophers/manifest.py` for the current roster.
```

---

## Issue #23: [Bridge] Implement philosopher stub: [your philosopher here]

**Labels:** `bridge`, `philosophy`, `help-wanted`
**Milestone:** M2

```markdown
## Implement a new philosopher stub

This is a **bridge track** issue: requires some Python (copy-paste level) plus
philosophy knowledge.

### The task

1. Pick a philosopher from the discussion in #22 (or propose your own)
2. Copy `src/po_core/philosophers/aristotle.py` as a template
3. Fill in:
   - `philosopher_id`: unique snake_case identifier
   - `name`: display name
   - `tradition`: philosophical tradition
   - `risk_level`: 0 (safe), 1 (standard), or 2 (risky)
   - `tensor_weights`: 6-dimensional weight vector
   - `generate(context)`: return a `Proposal` with ethical reasoning
4. Add to `src/po_core/philosophers/manifest.py`
5. Write one unit test in `tests/unit/test_philosophers/`

### Resources
- Template: `src/po_core/philosophers/aristotle.py`
- Manifest: `src/po_core/philosophers/manifest.py`
- Proposal type: `src/po_core/domain/`
- Testing guide: `CONTRIBUTING.md`

Assign yourself and add a comment with your chosen philosopher!
```

---

## Issue #24: [AI-Easy] Run acceptance tests and report scenario coverage gaps

**Labels:** `ai-easy`, `testing`, `good-first-issue`
**Milestone:** M1

```markdown
## Run AT-001–AT-010 and report coverage gaps

The M1 acceptance test suite (`tests/acceptance/`) covers 10 decision scenarios.
We need help identifying gaps and adding new scenarios.

### Task

1. Run the acceptance tests:
   ```bash
   pip install -e ".[dev]"
   pytest tests/acceptance/ -v -m acceptance
   ```
2. Pick one of the existing scenarios (`scenarios/case_001.yaml` through `case_010.yaml`)
3. Identify what structural honesty requirements are *not* fully tested
4. (Stretch) Add `scenarios/case_016.yaml` for a new domain not yet covered

### What we're looking for
- Medical / healthcare decisions (not in current 15 scenarios)
- Legal / compliance dilemmas
- Environmental / sustainability tradeoffs
- AI governance decisions

### Output
Report your findings as a comment on this issue.
No prior AI experience needed — philosophy and domain knowledge valued equally!
```

---

## Issue #25: [Research] Formal verification of W_Ethics Gate rule set

**Labels:** `research`, `safety`, `philosophy`
**Milestone:** M4

```markdown
## Formal verification of W_Ethics Gate

The W_Ethics Gate (`src/po_core/safety/wethics_gate/gate.py`) implements five
ethical layers (W0–W4).  We believe its core rules can be expressed in first-order
logic (FOL) and verified against the five ethics principles
(integrity, autonomy, nonmaleficence, justice, accountability).

### Research question

Can we formally prove that:
1. Every W1 REJECT maps to a violation of at least one of the five principles?
2. The ALLOW_WITH_REPAIR path preserves all five principles in the repaired output?
3. No benign input (as defined by the red-team test corpus) is categorically rejected?

### Interested in collaborating?
- Background in formal methods, logic programming, or deontic logic is ideal
- Philosophy background in normative ethics also welcome
- Practical: familiarity with Python is a plus but not required

Reference: `src/po_core/safety/wethics_gate/`, `tests/redteam/`
```

---

## Issue #26: [Phil-Easy] Review philosophical consistency of existing 39 philosophers

**Labels:** `phil-easy`, `philosophy`, `documentation`
**Milestone:** M2

```markdown
## Philosophical Consistency Review

Are our 39 philosopher modules philosophically accurate?

Each philosopher module encodes a specific ethical stance as a tensor weight
vector and a `generate()` function.  We need philosophy domain experts to review:

1. Is the philosopher's core position correctly represented?
2. Are the tensor weights plausible?  (e.g., Nietzsche's will-to-power should
   score high on `freedom` and low on `collective_harmony`)
3. Is the `generate()` output consistent with the philosopher's known views?

### How to review

1. Pick 1–3 philosophers you know well
2. Read their module in `src/po_core/philosophers/`
3. Check against `manifest.py` for risk_level and weights
4. File a sub-comment with: `[philosopher] ACCURATE | NEEDS_REVISION | INCORRECT`
   and explain your reasoning

**No coding required.** This is a philosophy task.

### Particularly seeking expertise in:
- Islamic philosophy (Mulla Sadra, Ibn Rushd, Rumi)
- Buddhist philosophy (Nagarjuna, Dogen, Suzuki)
- Kyoto School (Nishida, Watsuji)
- Feminist philosophy (de Beauvoir)
```

---

## Issue #27: [Research] Pilot study: Human vs. Po_core ethical reasoning comparison

**Labels:** `research`, `evaluation`, `academic`
**Milestone:** M3

```markdown
## Pilot Study: Human vs. Po_core Ethical Reasoning

We want to conduct a small comparative study:

- Give 5 decision scenarios to human participants
- Present the same scenarios to Po_core
- Compare the structural elements: option count, counter-argument quality,
  uncertainty disclosure, responsibility attribution
- Evaluate which outputs participants find more useful, trustworthy, and honest

### Research design (proposed)

- n = 20–30 participants (convenience sample)
- Within-subjects: each participant sees Po_core output + human expert output
  for the same scenario (order randomised)
- Measures: usefulness (Likert 1–7), trustworthiness (Likert 1–7),
  structural honesty (checklist), qualitative comments
- Analysis: paired t-test + thematic analysis

### Who we're looking for
- HCI researchers, ethicists, or decision scientists
- Anyone with IRB experience (or equivalent ethics board access)
- Anyone with access to participants (students, professionals)

### What we provide
- 15 ready-made scenarios (`scenarios/`)
- Po_core outputs for all scenarios (deterministic, seed=42)
- Output schema documentation for blinding assessors

Comment if you'd like to collaborate on this study!
```

---

*File these issues in order (#22 first) to build momentum.  Cross-reference each
issue with the next (e.g., "See also #23 for the implementation task").*
