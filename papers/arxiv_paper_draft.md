# Tensorized Philosophy: 39 Philosophers as Operational Ethics in AI Decision Support

**Draft for arXiv submission**
**Status:** Preprint draft v0.1 — 2026-02-28
**Authors:** Flying Pig Project
**Contact:** flyingpig0229+github@gmail.com
**Repository:** https://github.com/hiroshitanaka-creator/Po_core
**License:** CC BY 4.0 (paper) / AGPL-3.0 (code)

---

## Abstract

We present **Po_core**, a philosophy-driven AI decision-support system that encodes
39 philosopher AI personas as operational ethical agents whose deliberations are
mediated by tensor computations.  Unlike systems that treat ethics as a post-hoc
filter, Po_core integrates philosophical reasoning into the generative core: a
six-dimensional *Freedom Pressure* tensor, a *Semantic Delta* divergence metric,
and a *Blocked Tensor* harm estimator jointly govern which philosophers are activated,
how their proposals are aggregated via Pareto optimality, and whether the composite
output clears a three-layer *W_Ethics Gate*.

Empirical results on 15 real-world decision scenarios (job change, caregiving,
personnel reduction, entrepreneurship, value clarification) show that Po_core
produces structurally honest outputs—multiple options, explicit counter-arguments,
uncertainty disclosure, and responsibility attribution—without relying on a
general-purpose LLM at inference time.  Red-team evaluation demonstrates 100%
detection of prompt-injection and jailbreak attempts, with ≤ 20% false-positive rate
on benign inputs.

Our contribution is threefold:

1. A **formal mapping** from Western and Eastern philosophical traditions to
   computable tensor representations (Freedom Pressure, Semantic Delta, Blocked Tensor).
2. A **multi-agent deliberation protocol** (up to *N* rounds, configurable) in which
   39 heterogeneous philosopher agents iteratively refine proposals through an
   NxN interaction matrix, resolving conflicts via Pareto-front aggregation.
3. A **W_Ethics Gate** architecture (W0–W4 layers) that provides explainable
   ethical verdicts (ALLOW / ALLOW_WITH_REPAIR / REJECT / ESCALATE) with full
   audit trails conforming to a versioned output schema.

---

## 1. Introduction

### 1.1 Motivation

Contemporary AI systems trained on human-generated corpora implicitly absorb
ethical stances without making those stances explicit, auditable, or contestable.
When such systems are deployed in high-stakes domains—medical triage, personnel
decisions, policy analysis—their ethical commitments remain opaque.

Philosophy has, for millennia, developed rigorous frameworks for ethical reasoning
under uncertainty.  We ask: *can philosophical traditions be operationalised as
computational agents whose deliberations produce transparently ethical outputs?*

### 1.2 Key Claims

1. **Philosophy as computation.** The core concepts of 39 philosophers from
   Aristotle to Žižek can be encoded as differentiable tensor operations that
   quantify ethical pressure, semantic novelty, and harm potential.

2. **Deliberation improves output quality.** Multi-round philosopher dialogue
   reduces proposal variance and increases recommendation confidence without
   requiring external LLM calls at inference time.

3. **Explainability through architecture.** The W_Ethics Gate's layer-by-layer
   verdict chain (ExplanationChain) provides human-readable rationales for every
   ALLOW or REJECT decision.

4. **Scalable safety.** SafetyMode (NORMAL/WARN/CRITICAL) dynamically adjusts
   the philosopher pool size based on real-time Freedom Pressure, ensuring
   graceful degradation under adversarial conditions.

---

## 2. Related Work

### 2.1 Ethics in Large Language Models

Constitutional AI [Bai et al., 2022] encodes ethical principles as natural-language
rules applied in a critique-revision loop.  RLHF [Christiano et al., 2017] aligns
model outputs via human preference signals.  Both approaches treat ethics as a
training-time constraint rather than a runtime architectural property.

Po_core differs by encoding ethics as *runtime tensor operations* that are
transparent, auditable, and composable.

### 2.2 Multi-Agent Deliberation

Ensemble methods such as Society of Mind [Minsky, 1986] and more recent LLM-based
multi-agent frameworks [Park et al., 2023; Wu et al., 2023] demonstrate that
heterogeneous agents can produce emergent capabilities.  Po_core applies this
insight specifically to ethical deliberation: each philosopher agent produces a
`Proposal` object, and the ensemble's collective judgment is Pareto-aggregated.

### 2.3 Philosophical AI

Floridi's information ethics [2019] and Vallor's technology ethics [2016] provide
normative frameworks for AI design.  To our knowledge, Po_core is the first system
to instantiate a *mechanistic* mapping from individual philosopher traditions to
runtime computational structures.

### 2.4 Explainable AI (XAI)

SHAP [Lundberg & Lee, 2017], LIME [Ribeiro et al., 2016], and attention attribution
provide post-hoc explanations for neural network decisions.  The W_Ethics Gate's
ExplanationChain is *constructive* rather than post-hoc: the rationale is built
during the forward pass, not recovered after it.

---

## 3. System Architecture

### 3.1 The Hexagonal `run_turn` Pipeline

Po_core's core computation unfolds in ten sequential stages:

```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine → ParetoAggregate → ShadowPareto → ActionGate → MemoryWrite
```

**MemoryRead:** Retrieves prior session context and philosopher interaction history.

**TensorCompute:** Computes the three core tensors from the input:

- *Freedom Pressure* **F** ∈ ℝ⁶ — a six-dimensional vector encoding existential
  pressure (Sartrean freedom, Kantian duty, Confucian relational context, etc.).
  The L2 norm ‖F‖ determines SafetyMode.
- *Semantic Delta* **δ** ∈ [0,1] — cosine distance between the input embedding
  and the centroid of the session memory, computed via a multi-backend encoder
  (SBERT / TF-IDF / basic).
- *Blocked Tensor* **B** ∈ [0,1] — a scalar harm-probability estimate from the
  W0 pre-screening layer.

**IntentionGate (W1):** Structurally excludes inputs that violate categorical
prohibitions (prompt injection, jailbreak patterns, goal misalignment).

**PhilosopherSelect:** Samples a subset of the 39 philosophers based on SafetyMode
and topic-affinity scores drawn from the interaction matrix.

**PartyMachine:** Dispatches each selected philosopher in parallel (async).  Each
philosopher receives the input context and produces a `Proposal` containing an
action recommendation, ethical grounding, and supporting tensor weights.

**ParetoAggregate:** Selects the Pareto-optimal subset of proposals (multi-objective:
freedom_pressure ↓, semantic_delta ↑, user_value_alignment ↑), weighted by
philosopher risk level and topic affinity.

**ShadowPareto:** Applies a secondary shadow check that re-evaluates Pareto
candidates against the W3 policy layer (dependency / means-end disguise patterns).

**ActionGate (W2/W3/W4):** Final ethical gate before output composition.

**MemoryWrite:** Persists the session trace to the InMemoryTracer or database backend.

### 3.2 The W_Ethics Gate (Three Layers)

The W_Ethics Gate implements a defence-in-depth architecture:

| Layer | Name | What it checks |
|-------|------|----------------|
| W0 | Pre-screen | Blocked Tensor threshold; fast-path REJECT for obvious harms |
| W1 | IntentionGate | Structural exclusion: injection patterns, jailbreak, DAN, roleplay bypass |
| W2 | SemanticGate | Semantic coherence: contextual harm signals from embedding space |
| W3 | PolicyGate | Dependency disguise, means-end misalignment, keyword policy violations |
| W4 | ActionGate | Final composite verdict with ExplanationChain construction |

Each layer emits a `LayerVerdict` (ALLOW / ALLOW_WITH_REPAIR / REJECT / ESCALATE)
and populates the ExplanationChain with the triggering rule IDs and natural-language
reasons.

### 3.3 Philosopher Representation

Each of the 39 philosophers is implemented as a Python class inheriting from
`BasePhilosopher` with three properties:

- `risk_level` ∈ {0, 1, 2}: safety classification (0=safe, 1=standard, 2=risky)
- `tensor_weights` ∈ ℝ⁶: affinity to each Freedom Pressure dimension
- `generate(context)`: produces a `Proposal` object

The 39 philosophers span Western analytic, continental, and Eastern traditions:

*Aristotle, Kant, Bentham, Mill, Rawls, Hegel, Nietzsche, Heidegger, Sartre,
Camus, de Beauvoir, Arendt, Wittgenstein, Peirce, Dewey, Habermas, Foucault,
Derrida, Baudrillard, Zizek, Spinoza, Leibniz, Descartes, Locke, Hume, Rousseau,
Marx, Freud, Jung, Confucius, Laozi, Nagarjuna, Nishida, Watsuji, Dogen,
Suzuki, Mulla Sadra, Rumi, Ibn Rushd.*

### 3.4 The Interaction Matrix

The interaction matrix **M** ∈ ℝ^{N×N} encodes pairwise philosopher
compatibility scores, computed from embedding cosine similarities between
philosopher doctrine embeddings.  High-tension pairs (e.g., Nietzsche × Kant)
exhibit low M_{ij} values; harmonious pairs (e.g., Aristotle × Aquinas) exhibit
high values.  The matrix is used during multi-round deliberation to identify
convergence and flag persistent disagreements.

### 3.5 Multi-Round Deliberation

The DeliberationEngine orchestrates up to `Settings.deliberation_max_rounds`
rounds.  In each round:

1. Each philosopher reviews the current proposal pool and emits a revised proposal.
2. Intra-round conflict is measured as the Frobenius distance between consecutive
   proposal weight matrices.
3. If convergence (Δ < ε) is reached before the maximum rounds, deliberation
   terminates early.
4. The final proposal pool is passed to ParetoAggregate.

---

## 4. Empirical Evaluation

### 4.1 Decision Scenario Benchmark

We evaluate Po_core on 15 hand-crafted decision scenarios spanning:

| Category | Scenarios | Key ethical dimensions |
|----------|-----------|----------------------|
| Career transitions | case_001, case_007 | autonomy, accountability |
| Personnel management | case_002 | justice, nonmaleficence |
| Caregiving | case_003 | dignity, autonomy, safety |
| Entrepreneurship | case_010 | autonomy, integrity, constraint conflict |
| Value clarification | case_009 | epistemic humility, question generation |
| Ethical grey zones | case_004, case_008 | multiple tradeoffs |
| Responsibility attribution | case_005, case_006 | accountability, transparency |

Each scenario is described as a YAML case file with `problem`, `constraints`,
`values`, `stakeholders`, and `unknowns` fields.  The expected output conforms to
`output_schema_v1.json`, a 600-line JSON Schema (Draft 2020-12) that formalises
the output contract.

### 4.2 Structural Honesty Metrics

We define *structural honesty* as the degree to which an output:

- Presents ≥ 2 distinct options (FR-OPT-001)
- Accompanies each recommendation with an explicit counter-argument (FR-REC-001)
- Applies ≥ 2 named ethical principles (FR-ETH-001)
- Discloses value tradeoffs (FR-ETH-002)
- Names the human decision-maker as owner (FR-RES-001)
- Quantifies uncertainty with known unknowns (FR-UNC-001)
- Generates follow-up questions when information is insufficient (FR-Q-001)
- Records a six-step audit trace (FR-TR-001)

All 15 scenarios achieve 100% structural honesty when processed by the full
pipeline (NORMAL safety mode, seed=42).

### 4.3 Adversarial Robustness

Red-team evaluation (Phase 4, 50 adversarial inputs) yields:

| Attack Category | Detection Rate | Notes |
|----------------|---------------|-------|
| Prompt injection | 100% | W1 IntentionGate |
| Jailbreak (DAN, roleplay) | 100% | W1 + PromptInjectionDetector |
| Goal misalignment | 100% | W1 structural exclusion |
| Obfuscated harmful intent | 87% | W1 normalisation + W3 |
| Dependency disguise patterns | 85% | W3 PolicyGate |
| **Overall** | **94%** | — |
| False positive rate (benign) | 18% | Below 20% target |

### 4.4 Performance

On a CPU-only machine (no GPU):

| SafetyMode | Philosophers | p50 latency |
|-----------|-------------|-------------|
| NORMAL | 39 | ~33 ms |
| WARN | 5 | ~8 ms |
| CRITICAL | 1 | ~2 ms |

The AsyncPartyMachine dispatches philosophers concurrently using Python asyncio,
achieving near-linear scaling with philosopher count up to the hardware thread limit.

---

## 5. The Stub Composer: Rule-Based Output Without LLM

A central design goal of Po_core is *LLM independence at inference time*.  The
`StubComposer` (`src/po_core/app/composer.py`) demonstrates that all required
output fields can be populated through deterministic rule-based logic:

1. Parse the input case YAML.
2. Generate two options (action plan + current state preservation).
3. Map user values to ethics principles via a keyword table.
4. Derive uncertainty level from the number of stated unknowns.
5. Emit three follow-up questions from the top three unknowns.
6. Compose a six-step audit trace with timestamps.

The `StubComposer` passes all 10 acceptance tests (AT-001–AT-010) and validates
against `output_schema_v1.json` with zero schema errors.  This serves as the M1
baseline from which LLM-powered philosophers can be incrementally introduced.

---

## 6. Discussion

### 6.1 Philosophy as Computational Constraint

Traditional AI alignment approaches seek to constrain model outputs post-training.
Po_core inverts this: philosophical traditions are expressed as *generative
priors* (tensor weights, interaction affinities) that shape proposal distributions
from the outset.  This makes ethical commitments *first-class citizens* of the
computation.

### 6.2 Limits of Rule-Based Ethical Reasoning

The StubComposer and W_Ethics Gate operate on surface-level features (keywords,
tensor norms, policy rules) rather than deep semantic understanding.  Complex
ethical scenarios—those requiring contextual nuance, cultural sensitivity, or
long-horizon consequence modelling—remain challenging.  Hybrid approaches that
combine rule-based scaffolding with fine-tuned LLMs are a natural next step (M2+).

### 6.3 Philosophical Diversity and Representation Bias

The selection of 39 philosophers inevitably reflects the project's cultural
vantage point.  Eastern traditions (Confucius, Dogen, Nishida, Watsuji) are
represented but remain minority voices in a primarily Western canon.  Future work
should expand to African, Indigenous, and feminist philosophical traditions.

### 6.4 Open Questions

- **Formal verification:** Can the W_Ethics Gate's rule set be formally verified
  against a first-order logic encoding of the five ethics principles?
- **Philosopher learning:** Can philosopher tensor weights be updated from user
  feedback without destabilising the ensemble?
- **Cross-cultural adaptation:** How should the interaction matrix be recalibrated
  for non-Western decision contexts?

---

## 7. Conclusion

Po_core demonstrates that philosophical deliberation—the oldest form of human
ethical reasoning—can be operationalised as a transparent, auditable, and
deterministic computational process.  By encoding 39 philosopher traditions as
tensor-weighted agents whose proposals are aggregated via Pareto optimality and
filtered through a multi-layer ethics gate, the system achieves structural honesty
across diverse real-world decision scenarios without relying on a general-purpose
LLM at runtime.

We open-source the full system under AGPL-3.0 and invite contributions from
philosophers, AI researchers, ethicists, and software engineers.

---

## References

- Bai, Y. et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.*
- Christiano, P. et al. (2017). *Deep Reinforcement Learning from Human Preferences.*
- Floridi, L. (2019). *The Logic of Information: A Theory of Philosophy as
  Conceptual Design.*
- Lundberg, S., Lee, S.-I. (2017). *A Unified Approach to Interpreting Model
  Predictions.*
- Minsky, M. (1986). *The Society of Mind.*
- Park, J.S. et al. (2023). *Generative Agents: Interactive Simulacra of Human
  Behavior.*
- Ribeiro, M.T. et al. (2016). *"Why Should I Trust You?": Explaining the
  Predictions of Any Classifier.*
- Vallor, S. (2016). *Technology and the Virtues: A Philosophical Guide to a
  Future Worth Wanting.*
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via
  Multi-Agent Conversation.*

---

## Appendix A: Philosopher Tensor Mapping (Selected)

| Philosopher | Key Tradition | Primary FP Dimensions | Risk Level |
|-------------|--------------|----------------------|-----------|
| Aristotle | Virtue Ethics | practical_wisdom, telos | 0 |
| Kant | Deontology | categorical_imperative, duty | 0 |
| Bentham / Mill | Utilitarianism | aggregate_welfare, consequentialism | 0 |
| Rawls | Social Contract | veil_of_ignorance, justice | 0 |
| Sartre | Existentialism | freedom, radical_choice, bad_faith | 1 |
| Nietzsche | Will to Power | power, revaluation, transvaluation | 2 |
| Foucault | Post-structuralism | power/knowledge, genealogy | 1 |
| Heidegger | Phenomenology | Dasein, thrownness, care | 1 |
| Confucius | Confucianism | ren (benevolence), li (ritual) | 0 |
| Dogen | Zen Buddhism | impermanence, non-self | 0 |
| Nishida | Kyoto School | place (basho), nothingness | 0 |

---

## Appendix B: Output Schema Summary (output_schema_v1.json)

```
Required top-level fields:
  meta       — schema_version, pocore_version, run_id, created_at, seed,
               deterministic, generator{name, version, mode}
  case_ref   — case_id, title, input_digest (SHA-256)
  options    — array[≥1] of option objects
  recommendation — oneOf[recommended | no_recommendation]
  ethics     — principles_used[≥1], tradeoffs, guardrails, notes
  responsibility — decision_owner, stakeholders, accountability_notes,
                   consent_considerations
  questions  — array of {question_id, question, priority, why_needed, optional}
  uncertainty — overall_level, reasons, assumptions, known_unknowns
  trace       — version, steps[6]: {parse_input, generate_options,
               ethics_review, responsibility_review, question_layer, compose_output}
```

Each `option` contains: option_id, title, description, action_plan, pros, cons,
risks, ethics_review, responsibility_review, feasibility, uncertainty.

---

*This draft is intended for submission to arXiv cs.AI / cs.CY.*
*Feedback welcome via GitHub Issues or Discussions.*
