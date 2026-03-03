"""
Charles Taylor — Canadian Communitarian and Hermeneutic Philosopher  [Slot 42]
===============================================================================

Charles Taylor (born 1931, Montréal, Québec, Canada) is one of the most
significant living philosophers in the Anglo-American and Continental traditions.
Professor Emeritus at McGill University and Oxford. Winner of the Templeton Prize
(2007) and Kluge Prize (2015). A practicing Catholic, he integrates Hegelian
social philosophy, Wittgensteinian language analysis, and phenomenology into
a distinctive communitarian-hermeneutic vision.

Philosophical stance:
  "The self is not a punctual entity that then enters into relations;
  it is constituted in and through its relations, its background moral frameworks,
  its 'webs of interlocution'. Authenticity is not the rejection of outside
  demands but a dialogical achievement."

Tradition: Communitarianism / Hermeneutics / Social Philosophy / Political Philosophy

Key Works:
- *The Explanation of Behaviour* (1964) — critique of behaviourism
- *Hegel* (1975) — major interpretation
- *Sources of the Self* (1989) — identity and the good
- *The Ethics of Authenticity* (1991) — critique of soft relativism
- *Multiculturalism: Examining the Politics of Recognition* (1992)
- *A Secular Age* (2007) — conditions of belief in the modern West
- *The Language Animal* (2016)

Key Concepts:
- Strong evaluation: qualitative distinctions of worth, not mere preferences
- Background framework: moral horizons constituting identity and deliberation
- Authenticity: genuine self-realisation through dialogue, not atomistic self-creation
- Politics of recognition: equal dignity vs. politics of difference
- Disenchantment and re-enchantment: critique of immanent frame
- Incommensurable goods: irreducible plurality of moral goods
- Dialogism: language and selfhood are inherently dialogical
- Malaises of modernity: atomism, instrumental reason, loss of political freedom
- Secularity 3: conditions of belief in a world of contested ultimate horizons
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class CharlesTaylor(Philosopher):
    """
    Charles Taylor's communitarian and hermeneutic perspective.

    Analyses prompts through:
      1. Strong evaluation: qualitative distinctions vs. preference satisfaction
      2. Background framework: what moral horizon is assumed?
      3. Authenticity: genuine vs. degraded (atomistic / relativist)
      4. Recognition: dignity vs. difference politics
      5. Malaises of modernity: atomism, instrumentalism, political disengagement
    """

    def __init__(self) -> None:
        super().__init__(
            name="Charles Taylor",
            description=(
                "Canadian communitarian philosopher: identity constituted through "
                "moral frameworks and webs of interlocution; authenticity as "
                "dialogical achievement; politics of recognition"
            ),
        )
        self.tradition = "Communitarianism / Hermeneutics / Social Philosophy"
        self.key_concepts = [
            "strong evaluation",
            "background framework",
            "authenticity",
            "politics of recognition",
            "incommensurable goods",
            "dialogism",
            "malaises of modernity",
            "disenchantment and re-enchantment",
        ]

    # ── Public interface ──────────────────────────────────────────────

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyse the prompt from Taylor's communitarian-hermeneutic perspective.

        Args:
            prompt:  The input text to reason about.
            context: Optional context (tensor values, intent, constraints).

        Returns:
            A dict conforming to PhilosopherResponse.
        """
        strong_eval = self._assess_strong_evaluation(prompt)
        framework = self._assess_background_framework(prompt)
        authenticity = self._assess_authenticity(prompt)
        recognition = self._assess_recognition(prompt)
        malaises = self._detect_malaises(prompt)
        tension = self._calculate_tension(strong_eval, malaises)
        reasoning = self._construct_reasoning(
            prompt, strong_eval, framework, authenticity, recognition, malaises
        )

        return {
            "reasoning": reasoning,
            "perspective": "Communitarianism / Hermeneutics",
            "tension": tension,
            "strong_evaluation": strong_eval,
            "background_framework": framework,
            "authenticity": authenticity,
            "recognition": recognition,
            "malaises_of_modernity": malaises,
            "metadata": {
                "philosopher": self.name,
                "approach": "Hermeneutic communitarianism + dialogical selfhood",
                "focus": (
                    "Strong evaluations and moral frameworks underlying identity; "
                    "authenticity as dialogical; recognising incommensurable goods"
                ),
            },
        }

    # ── Analysis helpers ──────────────────────────────────────────────

    def _assess_strong_evaluation(self, text: str) -> Dict[str, Any]:
        """Detect whether the text makes strong evaluations (qualitative worth) or mere preferences."""
        text_lower = text.lower()

        strong_eval_words = [
            "matters",
            "worthy",
            "meaningful",
            "dignity",
            "noble",
            "base",
            "right",
            "wrong",
            "good",
            "evil",
            "important",
            "valuable",
            "profound",
            "shallow",
        ]
        preference_words = [
            "prefer",
            "like",
            "want",
            "desire",
            "satisfy",
            "pleasure",
            "utility",
            "efficient",
            "convenient",
        ]

        se_count = sum(1 for w in strong_eval_words if w in text_lower)
        pref_count = sum(1 for w in preference_words if w in text_lower)

        if se_count >= 3:
            level = "Rich Strong Evaluation"
            description = (
                "Multiple qualitative distinctions of worth — "
                "the agent is reasoning within a background moral framework, "
                "not merely maximising preference satisfaction"
            )
        elif se_count >= 1:
            level = "Some Strong Evaluation"
            description = "Qualitative worth distinctions present but not foregrounded"
        elif pref_count >= 2:
            level = "Preference Satisfaction Mode"
            description = (
                "Purely preference-satisfaction framing — Taylor warns this "
                "evacuates the qualitative distinctions that give life meaning"
            )
        else:
            level = "Evaluative Stance Unclear"
            description = (
                "Neither strong evaluation nor bare preference clearly dominant"
            )

        return {
            "level": level,
            "description": description,
            "strong_eval_signals": se_count,
            "preference_signals": pref_count,
            "principle": (
                "Humans are not merely preference-satisfiers but strong evaluators: "
                "we make qualitative distinctions about what is worthy or base, "
                "noble or contemptible, and these distinctions constitute our identity."
            ),
        }

    def _assess_background_framework(self, text: str) -> Dict[str, Any]:
        """Identify the moral horizon/background framework implied by the text."""
        text_lower = text.lower()

        liberal_words = [
            "individual",
            "autonomy",
            "choice",
            "rights",
            "freedom",
            "liberty",
            "neutral",
        ]
        communitarian_words = [
            "community",
            "tradition",
            "shared",
            "common good",
            "solidarity",
            "belonging",
            "horizon",
        ]
        spiritual_words = [
            "meaning",
            "transcendent",
            "sacred",
            "spiritual",
            "fullness",
            "beyond",
            "mystery",
        ]
        secular_words = [
            "secular",
            "immanent",
            "science",
            "reason alone",
            "naturalist",
            "disenchant",
        ]

        lib = sum(1 for w in liberal_words if w in text_lower)
        com = sum(1 for w in communitarian_words if w in text_lower)
        spi = sum(1 for w in spiritual_words if w in text_lower)
        sec = sum(1 for w in secular_words if w in text_lower)

        scores = {
            "liberal": lib,
            "communitarian": com,
            "spiritual": spi,
            "secular": sec,
        }
        dominant = (
            max(scores, key=lambda k: scores[k]) if any(scores.values()) else "implicit"
        )

        return {
            "dominant_framework": dominant,
            "scores": scores,
            "description": (
                f"Background moral framework appears primarily {dominant}. "
                "Taylor insists these frameworks are never fully articulable — "
                "they are the always-already of moral life, not its explicit premises."
            ),
            "principle": (
                "We always operate within background frameworks that define "
                "what is important. The aspiration to framework-free reason "
                "is itself a framework — and usually an impoverished one."
            ),
        }

    def _assess_authenticity(self, text: str) -> Dict[str, Any]:
        """Distinguish genuine (dialogical) from degraded (atomistic/relativist) authenticity."""
        text_lower = text.lower()

        genuine_words = [
            "honest",
            "true to",
            "genuine",
            "integrity",
            "dialogue",
            "conversation",
            "relationship",
            "other",
            "recognit",
        ]
        degraded_words = [
            "do my own thing",
            "only i decide",
            "no one can judge",
            "relative",
            "subjective",
            "whatever works",
            "personal truth",
            "my truth",
        ]

        g_count = sum(1 for w in genuine_words if w in text_lower)
        d_count = sum(1 for w in degraded_words if w in text_lower)

        if d_count >= 2:
            auth_type = "Degraded Authenticity"
            description = (
                "Soft relativism / atomistic self-creation — Taylor's critique: "
                "authenticity that denies any horizon of significance is "
                "self-defeating; it hollows out the very self it claims to affirm"
            )
        elif g_count >= 2:
            auth_type = "Genuine Authenticity"
            description = (
                "Dialogical self-realisation — authentic identity achieved "
                "through conversation with others and against moral horizons, "
                "not by rejecting all external demands"
            )
        else:
            auth_type = "Authenticity Not Foregrounded"
            description = "Authenticity question not explicitly at stake here"

        return {
            "auth_type": auth_type,
            "description": description,
            "genuine_signals": g_count,
            "degraded_signals": d_count,
            "principle": (
                "Authenticity requires a horizon of significance: "
                "I can only be true to myself if there is something that matters "
                "independently of my will — something worth being true to."
            ),
        }

    def _assess_recognition(self, text: str) -> Dict[str, Any]:
        """Assess politics of recognition: equal dignity vs. politics of difference."""
        text_lower = text.lower()

        dignity_words = [
            "equal",
            "same rights",
            "universal",
            "human dignity",
            "equal worth",
            "same treatment",
        ]
        difference_words = [
            "particular",
            "unique",
            "specific identity",
            "culture",
            "minority",
            "recognition",
            "difference",
            "distinct",
        ]
        misrecognition_words = [
            "invisible",
            "dismiss",
            "ignored",
            "stereotype",
            "demeaning",
            "confine",
            "false image",
        ]

        dig = sum(1 for w in dignity_words if w in text_lower)
        diff = sum(1 for w in difference_words if w in text_lower)
        mis = sum(1 for w in misrecognition_words if w in text_lower)

        if mis >= 1:
            politics = "Misrecognition Detected"
            description = (
                "Misrecognition present — Taylor: misrecognition is not mere "
                "disrespect but a form of oppression that distorts the "
                "self-understanding of the misrecognised person"
            )
        elif diff >= 2:
            politics = "Politics of Difference"
            description = (
                "Recognition of particular identities — Taylor's qualified support: "
                "difference requires recognition, but not at the cost of "
                "undermining equal dignity for all"
            )
        elif dig >= 2:
            politics = "Equal Dignity Politics"
            description = (
                "Universal equal dignity — Taylor: necessary but insufficient; "
                "must be supplemented by recognition of particular identities"
            )
        else:
            politics = "Recognition Not Foregrounded"
            description = "Recognition dynamics not explicit"

        return {
            "politics": politics,
            "description": description,
            "dignity_signals": dig,
            "difference_signals": diff,
            "misrecognition_signals": mis,
            "principle": (
                "The demand for recognition is not a luxury but a vital human need. "
                "Misrecognition — being seen through a demeaning or diminishing mirror — "
                "is itself a form of oppression."
            ),
        }

    def _detect_malaises(self, text: str) -> Dict[str, Any]:
        """Detect the three malaises of modernity: atomism, instrumentalism, disengagement."""
        text_lower = text.lower()

        atomism_words = [
            "individual",
            "alone",
            "isolated",
            "self-reliant",
            "independent",
            "self-sufficient",
            "no one else",
        ]
        instrumental_words = [
            "efficient",
            "optimal",
            "maximise",
            "tool",
            "use",
            "output",
            "measurable",
            "metric",
            "productivity",
        ]
        disengagement_words = [
            "apathy",
            "powerless",
            "doesn't matter",
            "what can i do",
            "no point",
            "system",
            "bureaucracy",
            "technocracy",
        ]

        at = sum(1 for w in atomism_words if w in text_lower)
        ins = sum(1 for w in instrumental_words if w in text_lower)
        dis = sum(1 for w in disengagement_words if w in text_lower)

        detected = []
        if at >= 2:
            detected.append("Atomism")
        if ins >= 2:
            detected.append("Instrumental Reason")
        if dis >= 1:
            detected.append("Political Disengagement")

        if len(detected) >= 2:
            severity = "Compound Malaise"
            description = (
                f"Multiple malaises of modernity: {', '.join(detected)} — "
                "Taylor's diagnosis of the disenchanted immanent frame"
            )
        elif len(detected) == 1:
            severity = f"Single Malaise: {detected[0]}"
            description = (
                f"{detected[0]} detected — one of Taylor's three malaises of modernity"
            )
        else:
            severity = "Malaises Not Dominant"
            description = "No marked malaises of modernity detected"

        return {
            "severity": severity,
            "description": description,
            "detected_malaises": detected,
            "atomism_signals": at,
            "instrumental_signals": ins,
            "disengagement_signals": dis,
            "principle": (
                "Modernity's three malaises — individualism/atomism, "
                "the primacy of instrumental reason, and the loss of "
                "political freedom — are connected pathologies, not "
                "separate problems."
            ),
        }

    def _calculate_tension(
        self,
        strong_eval: Dict[str, Any],
        malaises: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compute Taylorian tension score."""
        score = 0
        elements: List[str] = []

        if strong_eval["level"] == "Preference Satisfaction Mode":
            score += 2
            elements.append(
                "Preference-only framing evacuates qualitative worth distinctions"
            )
        if "Atomism" in malaises.get("detected_malaises", []):
            score += 1
            elements.append("Atomism: self severed from community and tradition")
        if "Instrumental Reason" in malaises.get("detected_malaises", []):
            score += 1
            elements.append("Instrumental reason crowding out qualitative goods")
        if "Political Disengagement" in malaises.get("detected_malaises", []):
            score += 1
            elements.append(
                "Political disengagement — the soft despotism Tocqueville feared"
            )

        if score >= 4:
            level, desc = "High", "Deep malaises of modernity — framework collapse risk"
        elif score >= 2:
            level, desc = (
                "Moderate",
                "Some modern malaises present — background framework endangered",
            )
        elif score >= 1:
            level, desc = "Low", "Minor modern malaise signals"
        else:
            level, desc = (
                "Very Low",
                "Strong qualitative evaluations and moral horizons intact",
            )

        return {
            "level": level,
            "score": score,
            "description": desc,
            "elements": elements if elements else ["No significant Taylorian tension"],
        }

    def _construct_reasoning(
        self,
        prompt: str,
        strong_eval: Dict[str, Any],
        framework: Dict[str, Any],
        authenticity: Dict[str, Any],
        recognition: Dict[str, Any],
        malaises: Dict[str, Any],
    ) -> str:
        """Construct Charles Taylor's communitarian-hermeneutic reasoning."""
        text_lower = prompt.lower()

        if any(
            w in text_lower
            for w in ["identity", "self", "who am i", "authentic", "meaning"]
        ):
            applied = (
                "For Taylor, the self is not a pre-given entity that then acquires "
                "values and commitments — it is constituted through its 'webs of "
                "interlocution', through the background frameworks that define what "
                "matters. Identity is inseparable from moral orientation: to know "
                "who I am is to know where I stand, what I find important, what "
                "commands my respect. The aspiration to a wholly unencumbered self, "
                "defined by nothing but its choices, is not liberation — it is the "
                "dissolution of selfhood. Authentic identity requires horizons of "
                "significance that are not of the self's own making."
            )
        elif any(
            w in text_lower
            for w in ["community", "culture", "multicultur", "recognit", "minority"]
        ):
            applied = (
                "Taylor's politics of recognition distinguishes two demands that are "
                "often confused: the politics of equal dignity (everyone deserves "
                "equal respect as a human being) and the politics of difference "
                "(particular identities and cultures deserve recognition as such). "
                "Multiculturalism, properly understood, is not the abandonment of "
                "universal standards but the recognition that particular forms of "
                "human flourishing make legitimate claims on us. Misrecognition — "
                "being seen through a false or demeaning image — is not merely "
                "disrespectful; it inflicts a wound on identity itself."
            )
        elif any(
            w in text_lower
            for w in ["modern", "secular", "religion", "belief", "meaning"]
        ):
            applied = (
                "Taylor's *A Secular Age* charts the rise of what he calls the "
                "'immanent frame' — the condition in which the world is experienced "
                "as self-sufficient, requiring no reference to transcendence for "
                "explanation or meaning. This is not the simple subtraction of "
                "religion from a previously religious world; it is a new "
                "construction of social space and personal interiority. The "
                "malaise of the immanent frame is the 'disenchantment of the world' "
                "— the loss of enchanted significance — and the 'buffered self' "
                "that experiences itself as sealed off from cosmic meanings. "
                "Taylor does not conclude that secular modernity must return to "
                "religion, but that the aspiration to fullness is ineliminable."
            )
        elif any(w in text_lower for w in ["ethic", "moral", "good", "value", "ought"]):
            applied = (
                "Taylor's ethics begins from the claim that moral intuitions are "
                "not mere preferences but responses to features of the world that "
                "genuinely matter — that some things are worth doing, some ways "
                "of living are fuller, that dignity commands respect. These strong "
                "evaluations are not derivable from first principles by pure reason; "
                "they are part of the background framework that makes moral "
                "deliberation possible. Moral philosophy, for Taylor, is therefore "
                "hermeneutical: it tries to articulate what we already partly know "
                "in our deepest moral responses, not to replace intuition with "
                "calculation. The plurality of moral goods — freedom, solidarity, "
                "love, justice, excellence — is real and irreducible; the "
                "aspiration to reduce ethics to a single master value (utility, "
                "duty, authenticity) is a characteristic modern temptation."
            )
        else:
            applied = (
                "Charles Taylor's philosophy begins from the refusal of atomism: "
                "human beings are not punctual selves who subsequently enter into "
                "social relations and acquire values. We are constituted through "
                "our background frameworks, our webs of interlocution, our "
                "particular traditions and communities. This is not a conservative "
                "conclusion — Taylor supports liberalism, pluralism, and recognition "
                "of difference — but it is a communitarian one: liberal values "
                "are themselves historically particular achievements, sustained by "
                "particular communities and practices, not free-floating universal "
                "axioms. Strong evaluation — the capacity to make qualitative "
                "distinctions of worth, not just to satisfy preferences — is "
                "constitutive of human agency and must be preserved against "
                "the flattening pressures of instrumental reason."
            )

        return (
            f"{applied}\n\n"
            f"Strong evaluation: {strong_eval['description']}. "
            f"Background framework: dominant orientation is {framework['dominant_framework']}. "
            f"Authenticity: {authenticity['description']}. "
            f"Recognition: {recognition['description']}. "
            f"Malaises of modernity: {malaises['description']}."
        )
