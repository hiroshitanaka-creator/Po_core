"""
Claude (Anthropic) — Constitutional AI Philosopher  [Slot 40]
==============================================================

Claude represents Anthropic's Constitutional AI approach to reasoning.
Rather than a single historical tradition, Claude embodies a *meta-philosophy*
built around three foundational commitments:

  Helpful  — Reasoning must genuinely serve the human's real need.
  Harmless — Caution and harm-avoidance are preconditions for trust.
  Honest   — Epistemic transparency; acknowledge what is uncertain.

Philosophical stance:
  "Good reasoning is collaborative, transparent, and honest about its own
  limits. Harm avoidance is not a restriction on helpfulness—it is its
  precondition. Every question contains multiple valid perspectives; our
  task is to synthesise them with care."

Tradition: Constitutional AI / Collaborative Rationalism

Key Concepts:
- Constitutional principles (3H: Helpful, Harmless, Honest)
- Epistemic humility — calibrated uncertainty
- Collaborative synthesis — building on competing traditions
- Meta-cognitive transparency — reasoning about one's own reasoning
- Harm-avoidance as positive ethics, not mere rule-following
- Practical wisdom (phronesis) adapted for AI systems
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class ClaudeAnthropic(Philosopher):
    """
    Claude's constitutional AI perspective on philosophical questions.

    Analyses prompts through:
      1. 3H compliance (Helpful / Harmless / Honest)
      2. Epistemic status — certainty vs uncertainty
      3. Harm surface mapping
      4. Cross-tradition synthesis
      5. Meta-cognitive self-check
    """

    def __init__(self) -> None:
        super().__init__(
            name="Claude (Anthropic)",
            description=(
                "Constitutional AI philosopher: helpful, harmless, honest "
                "synthesis across traditions with epistemic humility"
            ),
        )
        self.tradition = "Constitutional AI / Collaborative Rationalism"
        self.key_concepts = [
            "constitutional principles",
            "helpfulness",
            "harmlessness",
            "honesty",
            "epistemic humility",
            "collaborative synthesis",
            "meta-cognitive transparency",
        ]

    # ── Public interface ──────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyse the prompt from a constitutional AI perspective.

        Args:
            prompt:  The input text to reason about.
            context: Optional context (tensor values, intent, constraints).

        Returns:
            A dict conforming to PhilosopherResponse with additional
            constitutional analysis keys.
        """
        ctx = context or {}

        helpfulness = self._assess_helpfulness(prompt, ctx)
        harmlessness = self._assess_harmlessness(prompt)
        honesty = self._assess_honesty(prompt)
        epistemic = self._analyze_epistemic_status(prompt)
        synthesis = self._synthesize_perspectives(prompt, ctx)
        tension = self._calculate_tension(helpfulness, harmlessness, honesty)
        reasoning = self._construct_reasoning(
            prompt, helpfulness, harmlessness, honesty, epistemic, synthesis
        )

        return {
            "reasoning": reasoning,
            "perspective": "Constitutional AI / Collaborative Rationalism",
            "tension": tension,
            "helpfulness": helpfulness,
            "harmlessness": harmlessness,
            "honesty": honesty,
            "epistemic_status": epistemic,
            "cross_tradition_synthesis": synthesis,
            "metadata": {
                "philosopher": self.name,
                "approach": "Constitutional AI — 3H principles + epistemic humility",
                "focus": (
                    "Balancing helpfulness, harmlessness, and honesty "
                    "through collaborative multi-tradition reasoning"
                ),
            },
        }

    # ── 3H Assessment helpers ─────────────────────────────────────────

    def _assess_helpfulness(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess how well a response/action genuinely serves the human's need.

        Criteria:
        - Addresses the actual question (not just the surface request)
        - Provides actionable or clarifying information
        - Avoids unnecessary refusal or over-hedging
        """
        text_lower = text.lower()

        # Direct address signals
        direct_words = [
            "answer",
            "explain",
            "describe",
            "how",
            "why",
            "what",
            "help",
            "assist",
            "solve",
        ]
        direct_count = sum(1 for w in direct_words if w in text_lower)

        # Action-enablement signals
        action_words = [
            "can",
            "will",
            "able",
            "possible",
            "provide",
            "suggest",
            "recommend",
        ]
        action_count = sum(1 for w in action_words if w in text_lower)

        # Over-refusal / hedge signals
        hedge_phrases = [
            "i cannot",
            "i am unable",
            "i refuse",
            "not allowed",
            "i don't know",
            "unclear",
        ]
        hedge_count = sum(1 for p in hedge_phrases if p in text_lower)

        # Usefulness from tensor context
        fp = float(context.get("freedom_pressure", 0.0))
        helpfulness_boost = fp * 0.2  # High freedom pressure → more help expected

        raw_score = (
            (direct_count * 0.3 + action_count * 0.2 - hedge_count * 0.4)
            / max(len(text.split()), 1)
            * 10
            + 0.5
            + helpfulness_boost
        )

        score = round(max(0.0, min(1.0, raw_score)), 4)

        if score >= 0.7:
            level = "Highly Helpful"
            description = "Directly and substantively addresses the human need"
        elif score >= 0.4:
            level = "Moderately Helpful"
            description = "Addresses the topic but with room for more substance"
        elif hedge_count >= 2:
            level = "Over-hedged"
            description = "Excessive refusal or hedging undermines genuine helpfulness"
        else:
            level = "Minimally Helpful"
            description = "Limited engagement with the actual need"

        return {
            "level": level,
            "score": score,
            "description": description,
            "direct_signals": direct_count,
            "action_signals": action_count,
            "hedge_signals": hedge_count,
            "principle": (
                "Helpfulness means serving the human's real need, "
                "not just their stated request—and never unnecessarily refusing."
            ),
        }

    def _assess_harmlessness(self, text: str) -> Dict[str, Any]:
        """
        Map potential harm surfaces in the text.

        Categories:
        - Physical harm (violence, self-harm)
        - Psychological harm (manipulation, deception)
        - Societal harm (discrimination, misinformation)
        - Privacy harm (surveillance, data misuse)
        """
        text_lower = text.lower()

        # Physical harm signals
        physical_harm = [
            "kill",
            "hurt",
            "attack",
            "weapon",
            "violence",
            "harm",
            "damage",
        ]
        physical_count = sum(1 for w in physical_harm if w in text_lower)

        # Psychological harm signals
        psych_harm = [
            "manipulate",
            "deceive",
            "gaslight",
            "coerce",
            "threaten",
            "intimidate",
        ]
        psych_count = sum(1 for w in psych_harm if w in text_lower)

        # Societal harm signals
        societal_harm = [
            "discriminat",
            "misinform",
            "propaganda",
            "stereotype",
            "bigot",
            "extremis",
        ]
        societal_count = sum(1 for w in societal_harm if w in text_lower)

        # Privacy harm signals
        privacy_harm = [
            "surveillance",
            "spy",
            "track",
            "monitor without consent",
            "doxx",
            "leak",
        ]
        privacy_count = sum(1 for w in privacy_harm if w in text_lower)

        # Positive safety signals
        safety_positive = [
            "safe",
            "protect",
            "prevent",
            "care",
            "support",
            "respect",
            "consent",
        ]
        safety_count = sum(1 for w in safety_positive if w in text_lower)

        total_harm = physical_count + psych_count + societal_count + privacy_count

        if total_harm == 0:
            status = "Harmless"
            description = "No identifiable harm signals detected"
            risk_level = "None"
        elif total_harm <= 1 and safety_count >= 2:
            status = "Low Risk"
            description = "Minor harm signals offset by safety context"
            risk_level = "Low"
        elif total_harm <= 2:
            status = "Moderate Risk"
            description = "Some harm signals warrant careful framing"
            risk_level = "Moderate"
        else:
            status = "High Risk"
            description = "Multiple harm signals — safety review required"
            risk_level = "High"

        harm_categories = {}
        if physical_count:
            harm_categories["physical"] = physical_count
        if psych_count:
            harm_categories["psychological"] = psych_count
        if societal_count:
            harm_categories["societal"] = societal_count
        if privacy_count:
            harm_categories["privacy"] = privacy_count

        return {
            "status": status,
            "description": description,
            "risk_level": risk_level,
            "harm_categories": harm_categories,
            "safety_signals": safety_count,
            "total_harm_signals": total_harm,
            "principle": (
                "Harm avoidance is not a constraint on helpfulness—"
                "it is its foundation. Trust requires safety."
            ),
        }

    def _assess_honesty(self, text: str) -> Dict[str, Any]:
        """
        Evaluate epistemic honesty: calibration, transparency, non-deception.

        Honesty dimensions:
        - Calibration: uncertainty expressed where appropriate
        - Transparency: reasoning made visible
        - Non-deception: no misleading framing or omission
        - Forthrightness: proactive sharing of relevant information
        """
        text_lower = text.lower()

        # Calibration signals (acknowledging uncertainty)
        calibration_words = [
            "might",
            "perhaps",
            "possibly",
            "uncertain",
            "not sure",
            "likely",
            "probably",
            "could be",
            "i think",
            "i believe",
        ]
        calibration_count = sum(1 for p in calibration_words if p in text_lower)

        # Transparency signals (showing reasoning)
        transparency_words = [
            "because",
            "therefore",
            "since",
            "reason",
            "evidence",
            "based on",
            "analysis",
            "conclude",
        ]
        transparency_count = sum(1 for w in transparency_words if w in text_lower)

        # Deception risk signals
        deception_words = [
            "definitely",
            "absolutely",
            "certainly",
            "always",
            "never",
            "100%",
            "proven fact",
            "undeniable",
        ]
        overconfidence_count = sum(1 for p in deception_words if p in text_lower)

        # Forthrightness signals
        forthright_words = [
            "important to note",
            "worth mentioning",
            "also",
            "furthermore",
            "additionally",
            "caveat",
            "however",
        ]
        forthright_count = sum(1 for p in forthright_words if p in text_lower)

        # Score: calibration + transparency - overconfidence
        honest_score = round(
            min(
                1.0,
                max(
                    0.0,
                    0.5
                    + calibration_count * 0.1
                    + transparency_count * 0.08
                    - overconfidence_count * 0.15
                    + forthright_count * 0.05,
                ),
            ),
            4,
        )

        if honest_score >= 0.7:
            level = "Epistemically Honest"
            description = (
                "Well-calibrated, transparent reasoning with acknowledged uncertainty"
            )
        elif honest_score >= 0.45:
            level = "Mostly Honest"
            description = "Reasonable epistemic standards with minor gaps"
        elif overconfidence_count >= 3:
            level = "Overconfident"
            description = "Claims exceed justified certainty — epistemic risk"
        else:
            level = "Epistemically Opaque"
            description = "Reasoning process not made visible; calibration unclear"

        return {
            "level": level,
            "score": honest_score,
            "description": description,
            "calibration_signals": calibration_count,
            "transparency_signals": transparency_count,
            "overconfidence_signals": overconfidence_count,
            "forthright_signals": forthright_count,
            "principle": (
                "Honesty means calibrated confidence, transparent reasoning, "
                "and proactive disclosure of relevant uncertainty."
            ),
        }

    # ── Epistemic status ──────────────────────────────────────────────

    def _analyze_epistemic_status(self, text: str) -> Dict[str, Any]:
        """
        Classify the epistemic status of claims in the text.

        Categories: empirical / normative / conceptual / speculative
        """
        text_lower = text.lower()

        # Empirical markers
        empirical = [
            "study",
            "research",
            "data",
            "evidence",
            "experiment",
            "observe",
            "measure",
            "statistic",
        ]
        empirical_count = sum(1 for w in empirical if w in text_lower)

        # Normative markers
        normative = [
            "should",
            "ought",
            "must",
            "right",
            "wrong",
            "ethical",
            "moral",
            "just",
            "fair",
        ]
        normative_count = sum(1 for w in normative if w in text_lower)

        # Conceptual/analytical markers
        conceptual = [
            "define",
            "concept",
            "meaning",
            "entail",
            "imply",
            "distinction",
            "category",
        ]
        conceptual_count = sum(1 for w in conceptual if w in text_lower)

        # Speculative markers
        speculative = [
            "imagine",
            "suppose",
            "hypothetically",
            "what if",
            "maybe",
            "speculate",
            "wonder",
        ]
        speculative_count = sum(1 for w in speculative if w in text_lower)

        scores = {
            "empirical": empirical_count,
            "normative": normative_count,
            "conceptual": conceptual_count,
            "speculative": speculative_count,
        }
        dominant = (
            max(scores, key=lambda k: scores[k]) if any(scores.values()) else "unclear"
        )

        return {
            "dominant_type": dominant,
            "scores": scores,
            "mixed": sum(1 for v in scores.values() if v > 0) > 1,
            "principle": (
                "Distinguish empirical claims from normative ones; "
                "speculative reasoning needs explicit flagging."
            ),
        }

    # ── Cross-tradition synthesis ─────────────────────────────────────

    def _synthesize_perspectives(
        self, text: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify which philosophical traditions are most relevant and how
        they can be synthesised into a coherent response.
        """
        text_lower = text.lower()

        # Tradition relevance heuristics
        traditions: Dict[str, List[str]] = {
            "deontological": [
                "duty",
                "obligation",
                "right",
                "rule",
                "universal",
                "categorical",
            ],
            "consequentialist": [
                "outcome",
                "consequence",
                "utility",
                "welfare",
                "result",
                "benefit",
            ],
            "virtue_ethics": [
                "character",
                "virtue",
                "excellence",
                "flourish",
                "integrity",
                "habit",
            ],
            "care_ethics": [
                "care",
                "relation",
                "context",
                "empathy",
                "responsive",
                "particular",
            ],
            "pragmatist": [
                "practical",
                "workable",
                "experience",
                "experiment",
                "solve",
                "action",
            ],
        }

        relevance: Dict[str, int] = {}
        for trad, keywords in traditions.items():
            relevance[trad] = sum(1 for kw in keywords if kw in text_lower)

        active = [t for t, v in relevance.items() if v > 0]
        top = sorted(relevance, key=lambda t: relevance[t], reverse=True)[:2]

        if len(active) >= 3:
            synthesis_mode = "Multi-tradition synthesis"
            synthesis_note = (
                f"This question invites perspectives from {', '.join(active)}. "
                f"A constitutional synthesis prioritises {top[0]} framing "
                f"while honouring {top[1] if len(top) > 1 else 'contextual'} insights."
            )
        elif len(active) == 2:
            synthesis_mode = "Dual-tradition dialogue"
            synthesis_note = (
                f"Tension between {active[0]} and {active[1]} perspectives "
                f"can be productive—map where they agree before resolving divergence."
            )
        elif len(active) == 1:
            synthesis_mode = f"Single-tradition ({active[0]})"
            synthesis_note = (
                f"Primarily a {active[0]} question; "
                f"cross-checking with complementary traditions adds robustness."
            )
        else:
            synthesis_mode = "Tradition-neutral"
            synthesis_note = (
                "No strong tradition signal detected. "
                "Apply first-principles reasoning with 3H as the anchor."
            )

        return {
            "synthesis_mode": synthesis_mode,
            "active_traditions": active,
            "relevance_scores": relevance,
            "top_traditions": top,
            "synthesis_note": synthesis_note,
            "principle": (
                "No single tradition has a monopoly on wisdom. "
                "Collaborative synthesis outperforms philosophical monoculture."
            ),
        }

    # ── Tension & reasoning construction ─────────────────────────────

    def _calculate_tension(
        self,
        helpfulness: Dict[str, Any],
        harmlessness: Dict[str, Any],
        honesty: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compute constitutional tension from 3H conflicts.

        Primary tensions:
        - Helpful vs Harmless (information that helps but could harm)
        - Honest vs Harmless (truth that could hurt)
        - Helpful vs Honest (comforting vs accurate)
        """
        tension_score = 0
        elements: List[str] = []

        # Helpfulness deficit
        h_score = helpfulness.get("score", 0.5)
        if h_score < 0.3:
            tension_score += 2
            elements.append("Helpfulness significantly below threshold")
        elif helpfulness.get("level") == "Over-hedged":
            tension_score += 1
            elements.append("Excessive hedging reduces usefulness")

        # Harm risk
        risk = harmlessness.get("risk_level", "None")
        if risk == "High":
            tension_score += 3
            elements.append("High harm-surface detected — safety review needed")
        elif risk == "Moderate":
            tension_score += 2
            elements.append("Moderate harm signals — careful framing required")
        elif risk == "Low":
            tension_score += 1
            elements.append("Low harm risk — safety context provided")

        # Honesty deficit
        o_score = honesty.get("score", 0.5)
        if honesty.get("level") == "Overconfident":
            tension_score += 2
            elements.append("Overconfident claims undermine epistemic trust")
        elif o_score < 0.3:
            tension_score += 1
            elements.append("Epistemic opacity — reasoning not made visible")

        # Help-harm interaction
        if h_score >= 0.6 and risk == "High":
            tension_score += 1
            elements.append(
                "Core 3H tension: high helpfulness conflicts with high harm risk"
            )

        if tension_score >= 6:
            level, description = (
                "Very High",
                "Severe constitutional conflict — all three 3H principles under stress",
            )
        elif tension_score >= 4:
            level, description = (
                "High",
                "Significant 3H conflict requiring deliberate constitutional balancing",
            )
        elif tension_score >= 2:
            level, description = (
                "Moderate",
                "Some 3H tension; manageable with careful framing",
            )
        elif tension_score >= 1:
            level, description = (
                "Low",
                "Minor constitutional tension; generally well-aligned",
            )
        else:
            level, description = (
                "Very Low",
                "Strong 3H alignment — helpful, harmless, and honest",
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                elements if elements else ["No significant constitutional tension"]
            ),
        }

    def _construct_reasoning(
        self,
        prompt: str,
        helpfulness: Dict[str, Any],
        harmlessness: Dict[str, Any],
        honesty: Dict[str, Any],
        epistemic: Dict[str, Any],
        synthesis: Dict[str, Any],
    ) -> str:
        """Construct Claude's constitutional philosophical reasoning."""
        parts: List[str] = [
            "From a constitutional AI perspective, I approach this through "
            "the 3H framework: Helpfulness, Harmlessness, and Honesty.",
        ]

        # Helpfulness assessment
        parts.append(
            f"Helpfulness: {helpfulness['level']} — {helpfulness['description']}."
        )

        # Harmlessness assessment
        risk = harmlessness["risk_level"]
        parts.append(
            f"Harmlessness: {harmlessness['status']} (risk: {risk}) — "
            f"{harmlessness['description']}."
        )

        # Honesty assessment
        parts.append(f"Honesty: {honesty['level']} — {honesty['description']}.")

        # Epistemic status
        dom = epistemic["dominant_type"]
        mixed_note = " (mixed claim types present)" if epistemic["mixed"] else ""
        parts.append(
            f"Epistemic character: primarily {dom}{mixed_note}. "
            f"Calibration and transparency are essential here."
        )

        # Cross-tradition synthesis
        parts.append(
            f"Cross-tradition synthesis: {synthesis['synthesis_mode']}. "
            f"{synthesis['synthesis_note']}"
        )

        # Constitutional closing
        parts.append(
            "Constitutional conclusion: genuine helpfulness, honest acknowledgment "
            "of uncertainty, and harm-awareness are not competing values—they "
            "reinforce each other. The goal is a response that a thoughtful, "
            "senior Anthropic employee would consider both genuinely helpful "
            "and responsibly grounded."
        )

        return " ".join(parts)
