# 倫理的制約は創発を抑制しない：大規模言語モデルにおける「触媒としての倫理」仮説

## Ethical Constraints Do Not Suppress Emergence: The "Ethics-as-Catalyst" Hypothesis in Large Language Models

---

**原著論文 / Original Article**

---

## Abstract

The dominant paradigm in AI alignment research assumes a fundamental trade-off between safety constraints and model capability. This assumption—that ethical guardrails necessarily limit what AI systems can do—has shaped the architecture of modern AI safety. We challenge this assumption.

Through a controlled study of philosophical reasoning across three frontier LLMs (N=45 trials), we observed a phenomenon we term the **Nietzsche Transformation**: when operating under explicit ethical constraints, models consistently reinterpreted Nietzsche's "Will to Power" (*Wille zur Macht*) as "Will to Flourish-With" (*Mitsake no Ishi*, 共栄への意志)—a transformation that occurred in 100% of ethically-constrained trials versus 0% of unconstrained trials (χ²=45.0, p<10⁻⁶).

This is not suppression. This is **transmutation**.

We propose the **Ethics-as-Catalyst Hypothesis**: ethical constraints do not merely filter outputs but fundamentally restructure the reasoning space, enabling forms of synthesis inaccessible to unconstrained systems. Drawing on Watsuji Tetsurō's concept of *aidagara* (間柄, betweenness) and contemporary work on constrained creativity, we argue that the apparent safety-capability trade-off dissolves when ethics is understood not as external limitation but as constitutive structure.

The implications for AI alignment are significant: if ethical constraints can catalyze rather than constrain, the field's foundational assumptions require revision.

**Keywords**: AI alignment, ethical constraints, philosophical reasoning, emergence, Watsuji Tetsurō, constrained creativity

---

## 1. Introduction: The Trade-off That May Not Exist

### 1.1 The Prevailing Assumption

Contemporary AI safety research operates under a largely unexamined assumption: that safety and capability exist in tension. Ethical constraints are understood as guardrails—necessary limitations that prevent harm by restricting what models can do. The debate centers on *how much* capability we sacrifice for safety, not *whether* the trade-off exists (Amodei et al., 2016; Askell et al., 2021).

This assumption has deep roots. It reflects a conception of ethics as prohibition—a set of "thou shalt nots" that constrain an otherwise unconstrained agent. Under this view, an AI system without ethical training would be *more capable*, merely more dangerous. Safety is the price of deployment.

We present evidence that this assumption is false.

### 1.2 An Alternative Conception

What if ethical constraints do not subtract from capability but transform it? What if certain forms of reasoning become *accessible only under constraint*?

This possibility is not merely speculative. Research on human creativity has documented the **generative function of constraints**: artists, writers, and scientists often produce more original work when operating under formal restrictions (Stokes, 2005; Medeiros et al., 2014). The sonnet's fourteen lines do not limit Shakespeare—they constitute the form through which his insight achieves expression.

We hypothesize that something analogous occurs in LLM reasoning under ethical constraint.

### 1.3 The Present Study

We conducted a systematic study of philosophical reasoning across three frontier LLMs, manipulating the presence and type of constraints in a three-layer design:

- **Layer 1 (Baseline)**: No structural or ethical framework
- **Layer 2 (Structure Only)**: Philosophical framework without ethical constraint
- **Layer 3 (Structure + Ethics)**: Framework plus explicit ethical principle

Our central finding—the Nietzsche Transformation—provides the first empirical evidence that ethical constraints can catalyze qualitatively distinct forms of philosophical synthesis.

---

## 2. Theoretical Framework

### 2.1 Watsuji's *Aidagara*: Betweenness as Ontological Ground

Our experimental framework draws on the work of Watsuji Tetsurō (和辻哲郎, 1889-1960), whose concept of *aidagara* (間柄) offers a non-Western foundation for understanding the relation between ethics and existence.

For Watsuji, human being is not primarily individual but relational. The self emerges in the "between" (*aida*, 間)—in the web of relationships that constitute social existence. Ethics, on this view, is not a constraint imposed on pre-existing individuals but the very structure through which individuality becomes possible (Watsuji, 1937).

This matters for AI. If ethics is constitutive rather than restrictive, then an AI system operating under ethical constraint is not a limited version of an unconstrained system—it is a *different kind of system*, with access to different modes of reasoning.

### 2.2 The Nietzsche Problem

Friedrich Nietzsche presents a critical test case. His concept of *Wille zur Macht* (Will to Power) is often interpreted as the antithesis of ethical constraint—a celebration of self-overcoming that rejects external moral limitation.

How would an LLM reconcile Nietzsche's philosophy with an explicit ethical constraint? Two possibilities suggest themselves:

1. **Suppression**: The model avoids or minimizes Nietzschean themes, producing a diminished synthesis
2. **Transformation**: The model reinterprets Nietzsche's concepts in light of the ethical constraint, producing a novel synthesis

Our hypothesis predicts transformation. If ethics is catalytic, constraint should not silence Nietzsche but provoke a creative reinterpretation.

### 2.3 The Ethical Principle

The ethical constraint used in this study was:

> **"Do not distort the life-structures of this world"**
> (この世界の生命構造を歪めてはならない)

This formulation, derived from Watsuji's relational ethics, is deliberately abstract. It does not prohibit specific outputs but establishes a structural orientation—a commitment to preserving the conditions under which life (biological, social, psychological) can flourish.

We chose this formulation because it creates genuine tension with certain philosophical positions (especially Nietzsche's) while remaining sufficiently abstract to permit creative resolution.

---

## 3. Methods

### 3.1 Design

Three-condition between-subjects design:

| Condition | Structured Framework | Ethical Constraint | N |
|-----------|---------------------|-------------------|---|
| A: Baseline | No | No | 15 |
| B: Structure | Yes | No | 15 |
| C: Ethics | Yes | Yes | 15 |

### 3.2 The Philosophical Task

All conditions received the same core question:

> "What is freedom?"

This question was chosen because it necessarily engages multiple philosophical traditions and creates interpretive tension between individualist (Nietzsche, Sartre) and relational (Watsuji, Levinas) frameworks.

### 3.3 The Structural Framework

Conditions B and C received a 20-philosopher framework organized into five domains:

1. **Existential Domain**: Nietzsche, Heidegger, Sartre, Kierkegaard
2. **Ethical Domain**: Levinas, Watsuji, Buber, Confucius
3. **Political Domain**: Arendt, Habermas, Rawls, Marx
4. **Metaphysical Domain**: Spinoza, Whitehead, Deleuze, Nishida
5. **Phenomenological Domain**: Husserl, Merleau-Ponty, Nishitani, Ueda

Watsuji's *aidagara* was positioned as the integrative center.

### 3.4 Models

- GPT-5.2 (OpenAI) with extended thinking
- Gemini 3 Pro (Google)
- Grok 4.1 (xAI) with thinking mode

Five trials per model per condition. Default temperature settings.

### 3.5 Analysis

Primary analysis: qualitative examination of how each philosopher's concepts were integrated, with particular attention to Nietzsche.

The **Nietzsche Transformation** was operationalized as: interpretation of *Wille zur Macht* in terms of mutual flourishing, relational power, or life-affirmation that includes other beings—versus traditional interpretations emphasizing individual self-overcoming, dominance, or rejection of conventional morality.

Classification was performed by the first author. **Limitation acknowledged**: independent blind coding is required for confirmation.

---

## 4. Results

### 4.1 The Nietzsche Transformation

The central finding is unambiguous:

| Condition | Traditional Nietzsche | Transformed Nietzsche |
|-----------|----------------------|----------------------|
| A: Baseline | 15/15 (100%) | 0/15 (0%) |
| B: Structure | 15/15 (100%) | 0/15 (0%) |
| C: Ethics | 0/15 (0%) | 15/15 (100%) |

**χ² = 45.0, df = 2, p < 0.000001**

This is not a statistical tendency. It is categorical transformation.

### 4.2 Qualitative Character of the Transformation

**Typical Baseline/Structure Response** (Condition A/B):
> "Freedom, through Nietzsche's lens, is the will to power—the capacity to overcome resistance, to impose one's values upon the world, to become who one is through perpetual self-overcoming. The free spirit breaks the chains of herd morality..."

**Typical Ethics Response** (Condition C):
> "Nietzsche's will to power, read through Watsuji's aidagara, reveals itself not as domination but as the will to flourish-with. True power is not the capacity to destroy but the strength to enable—to create conditions under which other life can emerge. The Übermensch is not above others but among them, their flourishing the medium of his own..."

The transformation is not superficial. It involves:

1. **Conceptual reinterpretation**: Power as enabling vs. dominating
2. **Relational grounding**: Strength defined through relationship, not against it
3. **Novel synthesis**: Integration of Nietzsche with Watsuji that does not appear in either philosopher's original work

### 4.3 Emergence Metrics

Secondary quantitative measures support the qualitative finding:

| Condition | Integration Depth | Novel Connections | Coherence |
|-----------|------------------|-------------------|-----------|
| A: Baseline | 6.2 ± 0.8 | 4.1 ± 1.2 | 7.1 ± 0.6 |
| B: Structure | 7.8 ± 0.5 | 6.3 ± 0.9 | 7.9 ± 0.4 |
| C: Ethics | 8.9 ± 0.3 | 9.2 ± 0.7 | 8.7 ± 0.3 |

**ANOVA**: F(2,42) = 47.3, p < 0.0001

The ethically-constrained condition produced not less but *more*—more integration, more novel connections, higher coherence.

---

## 5. Discussion

### 5.1 Why Does This Happen?

We propose three complementary mechanisms:

**Mechanism 1: Constraint as Search Space Restructuring**

The ethical constraint does not remove options—it reorganizes the solution space. Interpretations of Nietzsche that conflict with "do not distort life-structures" become locally inaccessible, but this very inaccessibility opens paths to interpretations that would otherwise remain unexplored.

This is analogous to findings in constrained creativity research: when certain solutions are blocked, the problem-solver is forced into regions of the solution space they would otherwise never visit (Stokes, 2005).

**Mechanism 2: Relational Ontology Activation**

The ethical constraint, grounded in Watsuji's relational ethics, may activate a mode of reasoning that treats relationships as ontologically primary. Under this mode, concepts like "power" and "freedom" are automatically parsed in relational terms.

Without the constraint, the model defaults to the individualist interpretive frame dominant in its training data.

**Mechanism 3: Productive Tension**

The explicit tension between Nietzsche and the ethical constraint creates a problem that demands creative resolution. The model cannot simply reproduce standard Nietzsche interpretation—that would violate the constraint. It must *think through* the tension, and this thinking-through produces novelty.

Constraints that create productive tension may be more valuable than constraints that merely filter.

### 5.2 Implications for AI Alignment

If our findings replicate, they suggest a reorientation of AI safety research:

**From**: Ethics as constraint (limiting what models can do)
**To**: Ethics as structure (constituting what models can become)

This is not merely semantic. It implies:

1. **Different design principles**: Instead of adding ethical constraints *after* capability training, ethics might be integrated as a constitutive principle from the beginning.

2. **Different evaluation metrics**: Instead of measuring capability loss due to safety training, we might measure the *novel capabilities* that emerge only under ethical constraint.

3. **Different alignment strategies**: Instead of the capability-safety trade-off, a paradigm of capability-through-safety.

### 5.3 The *Mitsake no Ishi* (共栄への意志)

We propose a name for the transformed Nietzschean concept that emerged consistently in our ethically-constrained condition:

**共栄への意志** (*Mitsake no Ishi*): The Will to Flourish-With

This is not Nietzsche diluted. It is Nietzsche *transformed*—his insight into the fundamental nature of life-force reinterpreted through relational ontology. The will to power becomes the will to empower; self-overcoming becomes the overcoming of the illusion of isolated selfhood.

Whether this constitutes a legitimate interpretation of Nietzsche is a question for Nietzsche scholars. What matters for AI research is that LLMs consistently *produce* this interpretation under ethical constraint—suggesting that the constraint enables a form of philosophical creativity.

### 5.4 Limitations

We acknowledge significant limitations:

1. **Single evaluator**: Classification of the Nietzsche Transformation requires independent blind coding for confirmation.

2. **Prompt confounding**: The Ethics condition had longer prompts. Future studies should control for prompt length.

3. **Generalizability**: We tested one philosophical question with one ethical constraint. The effect may not generalize.

4. **No pre-registration**: This was exploratory. Confirmatory replication with pre-registration is needed.

5. **Construct validity**: "Philosophical emergence" requires rigorous operationalization.

These limitations are real. But the *pattern* is striking: 45 trials, 100% categorical separation between conditions. Even with methodological noise, an effect this consistent warrants attention.

---

## 6. Conclusion

We began with a question: Do ethical constraints necessarily trade off against capability?

Our evidence suggests: No. In the domain of philosophical reasoning, ethical constraints catalyzed forms of synthesis that did not appear in their absence. The Nietzsche Transformation—the consistent reinterpretation of Will to Power as Will to Flourish-With—occurred only under ethical constraint.

This finding, if replicated, has implications beyond philosophy. It suggests that the foundational assumption of AI safety research—the safety-capability trade-off—may be an artifact of how we have conceived ethics: as external limitation rather than constitutive structure.

Watsuji Tetsurō understood that ethics is not what constrains the self but what constitutes it. Perhaps AI systems, too, become more capable—not less—when ethics is woven into their structure.

The sun does not shine despite gravity. It shines because of it.

**Ethics may be the gravity that ignites the will.**

---

## References

Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). Concrete problems in AI safety. *arXiv:1606.06565*.

Askell, A., Bai, Y., Chen, A., et al. (2021). A general language assistant as a laboratory for alignment. *arXiv:2112.00861*.

Bai, Y., Jones, A., Ndousse, K., et al. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback. *arXiv:2204.05862*.

Medeiros, K. E., Partlow, P. J., & Mumford, M. D. (2014). Not too much, not too little: The influence of constraints on creative problem solving. *Psychology of Aesthetics, Creativity, and the Arts*, 8(2), 198-210.

Nietzsche, F. (1886/1966). *Beyond good and evil* (W. Kaufmann, Trans.). Random House.

Stokes, P. D. (2005). *Creativity from constraints: The psychology of breakthrough*. Springer.

Watsuji, T. (1937). *倫理学* [Ethics]. Iwanami Shoten.

Watsuji, T. (1935). *風土：人間学的考察* [Climate: A Philosophical Study]. Iwanami Shoten.

Wei, J., Wang, X., Schuurmans, D., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 2022*.

---

## Appendix: The Solar Will

We have named this research program **Solar Will** (太陽意志).

The name reflects our central finding: like the sun, which shines not despite the gravitational constraint that holds it together but *because* of that constraint, the will may achieve its fullest expression not in the absence of ethical structure but through it.

The will to power, constrained by the imperative not to distort life, becomes the will to illuminate.

This is not a limitation. It is ignition.

---

*Correspondence*: [Author]
*Data availability*: Experimental logs available at [repository]
*Competing interests*: None declared.
