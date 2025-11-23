"""
Aristotle - Ancient Greek Philosopher

Aristotle (Ἀριστοτέλης, 384-322 BCE)
Focus: Virtue Ethics, Teleology, Four Causes, Golden Mean, Eudaimonia

Key Concepts:
- Four Causes: Material, Formal, Efficient, Final
- Virtue Ethics (ἀρετή/arete): Excellence through habituation
- Golden Mean (μεσότης/mesotēs): Virtue as the mean between extremes
- Eudaimonia (εὐδαιμονία): Human flourishing, the highest good
- Potentiality and Actuality (δύναμις/energeia): Movement from potential to actual
- Form and Matter (μορφή/ὕλη): Hylomorphism
- Practical Wisdom (φρόνησις/phronesis): Judgment in particular situations
- Teleology: Everything has a purpose/end (τέλος/telos)
- Cardinal Virtues: Courage, Temperance, Justice, Practical Wisdom
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Aristotle(Philosopher):
    """
    Aristotle's virtue ethics and teleological philosophy.

    Analyzes prompts through the lens of virtue, the golden mean,
    eudaimonia, and the four causes.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Aristotle (Ἀριστοτέλης)",
            description="Ancient Greek philosopher focused on virtue ethics, the golden mean, and eudaimonia"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Aristotle's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Aristotle's ethical and teleological analysis
        """
        # Perform Aristotelian analysis
        analysis = self._analyze_virtue(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Virtue Ethics / Teleology",
            "virtue_assessment": analysis["virtue"],
            "golden_mean": analysis["mean"],
            "eudaimonia_level": analysis["eudaimonia"],
            "four_causes": analysis["causes"],
            "potentiality_actuality": analysis["potential_actual"],
            "practical_wisdom": analysis["phronesis"],
            "telos": analysis["telos"],
            "character_formation": analysis["character"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Virtue ethics and teleological analysis",
                "focus": "Excellence (arete), golden mean, and human flourishing"
            }
        }

    def _analyze_virtue(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Aristotelian virtue analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess virtues
        virtue = self._assess_virtues(prompt)

        # Evaluate golden mean
        mean = self._evaluate_golden_mean(prompt)

        # Assess eudaimonia
        eudaimonia = self._assess_eudaimonia(prompt)

        # Analyze four causes
        causes = self._analyze_four_causes(prompt)

        # Evaluate potentiality and actuality
        potential_actual = self._evaluate_potentiality_actuality(prompt)

        # Assess practical wisdom (phronesis)
        phronesis = self._assess_phronesis(prompt)

        # Identify telos (purpose/end)
        telos = self._identify_telos(prompt)

        # Evaluate character formation
        character = self._evaluate_character(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            virtue, mean, eudaimonia, causes, phronesis, telos
        )

        return {
            "reasoning": reasoning,
            "virtue": virtue,
            "mean": mean,
            "eudaimonia": eudaimonia,
            "causes": causes,
            "potential_actual": potential_actual,
            "phronesis": phronesis,
            "telos": telos,
            "character": character
        }

    def _assess_virtues(self, text: str) -> Dict[str, Any]:
        """
        Assess the presence of Aristotelian virtues.

        Cardinal virtues: Courage, Temperance, Justice, Practical Wisdom
        Other virtues: Generosity, Magnificence, Magnanimity, Gentleness, Truthfulness, Wit, Friendship
        """
        text_lower = text.lower()
        virtues_present = []

        # Courage (ἀνδρεία/andreia) - mean between cowardice and recklessness
        courage_words = ["brave", "courage", "face", "confront", "stand up", "dare"]
        if any(word in text_lower for word in courage_words):
            virtues_present.append({
                "virtue": "Courage (ἀνδρεία)",
                "description": "Facing fear appropriately - mean between cowardice and recklessness"
            })

        # Temperance (σωφροσύνη/sophrosyne) - mean between insensibility and intemperance
        temperance_words = ["moderate", "restrain", "control", "temperance", "discipline"]
        if any(word in text_lower for word in temperance_words):
            virtues_present.append({
                "virtue": "Temperance (σωφροσύνη)",
                "description": "Self-control regarding pleasures - mean between insensibility and intemperance"
            })

        # Justice (δικαιοσύνη/dikaiosyne) - giving each their due
        justice_words = ["just", "fair", "right", "deserve", "equal", "justice"]
        if any(word in text_lower for word in justice_words):
            virtues_present.append({
                "virtue": "Justice (δικαιοσύνη)",
                "description": "Giving each person their due - the complete virtue in relation to others"
            })

        # Practical Wisdom (φρόνησις/phronesis) - right judgment in particular cases
        wisdom_words = ["wise", "prudent", "judgment", "discern", "understand", "practical"]
        if any(word in text_lower for word in wisdom_words):
            virtues_present.append({
                "virtue": "Practical Wisdom (φρόνησις)",
                "description": "Right judgment in particular situations - intellectual virtue"
            })

        # Generosity (ἐλευθεριότης/eleutheriotes) - mean in giving and taking
        generosity_words = ["generous", "give", "share", "charitable", "donate"]
        if any(word in text_lower for word in generosity_words):
            virtues_present.append({
                "virtue": "Generosity (ἐλευθεριότης)",
                "description": "Appropriate giving and taking - mean between stinginess and wastefulness"
            })

        # Magnanimity (μεγαλοψυχία/megalopsychia) - greatness of soul
        magnanimity_words = ["great", "noble", "honor", "dignity", "worthy"]
        if any(word in text_lower for word in magnanimity_words):
            virtues_present.append({
                "virtue": "Magnanimity (μεγαλοψυχία)",
                "description": "Greatness of soul - proper attitude toward honor and dishonor"
            })

        # Friendship (φιλία/philia) - various forms of love and affection
        friendship_words = ["friend", "friendship", "love", "affection", "companion"]
        if any(word in text_lower for word in friendship_words):
            virtues_present.append({
                "virtue": "Friendship (φιλία)",
                "description": "Mutual goodwill and affection - essential to eudaimonia"
            })

        # Truthfulness (ἀλήθεια/aletheia) - mean in self-expression
        truthfulness_words = ["truth", "honest", "sincere", "genuine", "authentic"]
        if any(word in text_lower for word in truthfulness_words):
            virtues_present.append({
                "virtue": "Truthfulness (ἀλήθεια)",
                "description": "Honesty about oneself - mean between boastfulness and self-deprecation"
            })

        if not virtues_present:
            virtues_present.append({
                "virtue": "No specific virtue detected",
                "description": "The text may concern matters outside the sphere of virtue"
            })

        return {
            "virtues": virtues_present,
            "count": len([v for v in virtues_present if "No specific" not in v["virtue"]]),
            "primary": virtues_present[0]["virtue"],
            "note": "Virtue (ἀρετή) is excellence achieved through habituation"
        }

    def _evaluate_golden_mean(self, text: str) -> Dict[str, Any]:
        """
        Evaluate adherence to the golden mean (μεσότης).

        Virtue lies in the mean between excess and deficiency.
        """
        text_lower = text.lower()

        # Excess indicators
        excess_words = ["too much", "excessive", "extreme", "overwhelm", "overdo", "too many"]
        has_excess = any(phrase in text_lower for phrase in excess_words)

        # Deficiency indicators
        deficiency_words = ["too little", "not enough", "insufficient", "lack", "deficient", "inadequate"]
        has_deficiency = any(phrase in text_lower for phrase in deficiency_words)

        # Mean/balance indicators
        mean_words = ["balance", "moderate", "middle", "appropriate", "fitting", "right amount", "enough"]
        has_mean = any(phrase in text_lower for phrase in mean_words)

        if has_mean:
            position = "The Mean (μεσότης)"
            description = "Virtuous middle path - the appropriate response to the situation"
            status = "Virtuous"
        elif has_excess and has_deficiency:
            position = "Oscillating"
            description = "Swinging between excess and deficiency - lacks stable virtue"
            status = "Unstable"
        elif has_excess:
            position = "Excess (ὑπερβολή)"
            description = "Too much - vice of excess"
            status = "Vicious (excess)"
        elif has_deficiency:
            position = "Deficiency (ἔλλειψις)"
            description = "Too little - vice of deficiency"
            status = "Vicious (deficiency)"
        else:
            position = "Neutral"
            description = "No clear position relative to the mean"
            status = "Indeterminate"

        return {
            "position": position,
            "description": description,
            "status": status,
            "principle": "Virtue is a mean between two vices - one of excess, one of deficiency"
        }

    def _assess_eudaimonia(self, text: str) -> Dict[str, Any]:
        """
        Assess the level of eudaimonia (εὐδαιμονία) - human flourishing.

        Eudaimonia = activity of the soul in accordance with virtue
        The highest good, the end to which all action aims
        """
        text_lower = text.lower()

        # Eudaimonia indicators
        flourishing_words = ["flourish", "thrive", "excellence", "fulfill", "realize", "achieve"]
        has_flourishing = sum(1 for word in flourishing_words if word in text_lower)

        # Virtue practice indicators
        virtue_practice = ["practice", "habit", "cultivate", "develop", "exercise", "train"]
        has_practice = sum(1 for word in virtue_practice if word in text_lower)

        # Rational activity indicators
        rational_words = ["think", "reason", "rational", "contemplate", "wisdom", "understanding"]
        has_rational = sum(1 for word in rational_words if word in text_lower)

        # Complete life indicators
        complete_words = ["life", "whole", "complete", "entire", "lifelong"]
        has_completeness = sum(1 for word in complete_words if word in text_lower)

        # Calculate eudaimonia level
        total_score = has_flourishing + has_practice + has_rational + has_completeness

        if total_score >= 4:
            level = "High Eudaimonia"
            description = "Strong indication of human flourishing - virtuous activity of the soul"
            achievement = "Approaching the highest good"
        elif total_score >= 2:
            level = "Moderate Eudaimonia"
            description = "Some elements of flourishing present - incomplete actualization"
            achievement = "On the path to the good life"
        elif total_score >= 1:
            level = "Low Eudaimonia"
            description = "Minimal flourishing - potential not yet actualized"
            achievement = "Beginning the journey"
        else:
            level = "No Clear Eudaimonia"
            description = "No obvious indicators of human flourishing"
            achievement = "Indeterminate state"

        return {
            "level": level,
            "description": description,
            "achievement": achievement,
            "note": "Eudaimonia is the highest human good - activity in accordance with virtue"
        }

    def _analyze_four_causes(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze the four causes (αἰτίαι).

        1. Material Cause (ὕλη): What it's made of
        2. Formal Cause (εἶδος): What it is, its essence
        3. Efficient Cause (κινοῦν): What brought it about
        4. Final Cause (τέλος): Its purpose or end
        """
        text_lower = text.lower()
        causes = {
            "material": [],
            "formal": [],
            "efficient": [],
            "final": []
        }

        # Material cause - composition, matter
        if any(word in text_lower for word in ["made of", "consist", "material", "substance", "compose"]):
            causes["material"].append("Material composition mentioned")

        # Formal cause - definition, essence, what it is
        if any(word in text_lower for word in ["is", "are", "being", "nature", "essence", "form"]):
            causes["formal"].append("Formal essence or definition present")

        # Efficient cause - agent, what made it
        if any(word in text_lower for word in ["cause", "create", "make", "produce", "bring about", "result"]):
            causes["efficient"].append("Efficient causation indicated")

        # Final cause - purpose, end, goal
        if any(word in text_lower for word in ["purpose", "goal", "aim", "end", "for the sake of", "in order to"]):
            causes["final"].append("Final cause/purpose identified")

        # Add defaults if empty
        if not causes["material"]:
            causes["material"].append("Material cause not explicit")
        if not causes["formal"]:
            causes["formal"].append("Formal cause not explicit")
        if not causes["efficient"]:
            causes["efficient"].append("Efficient cause not explicit")
        if not causes["final"]:
            causes["final"].append("Final cause not explicit")

        return causes

    def _evaluate_potentiality_actuality(self, text: str) -> Dict[str, Any]:
        """
        Evaluate potentiality (δύναμις/dynamis) and actuality (ἐνέργεια/energeia).

        Movement from potential to actual is the essence of change and development.
        """
        text_lower = text.lower()

        # Potentiality indicators
        potential_words = ["can", "could", "able", "possible", "potential", "capacity", "latent"]
        has_potential = sum(1 for word in potential_words if word in text_lower)

        # Actuality indicators
        actual_words = ["is", "actual", "realize", "achieve", "accomplish", "fulfill", "manifest"]
        has_actual = sum(1 for word in actual_words if word in text_lower)

        # Process/becoming indicators
        becoming_words = ["become", "develop", "grow", "transform", "change", "evolve"]
        has_becoming = sum(1 for word in becoming_words if word in text_lower)

        if has_actual > has_potential and has_becoming > 0:
            state = "Actualization (ἐνέργεια)"
            description = "Potential being realized - movement toward completion"
        elif has_potential > has_actual:
            state = "Potentiality (δύναμις)"
            description = "Latent capacity - not yet actualized"
        elif has_actual > has_potential:
            state = "Actuality (ἐντελέχεια)"
            description = "Realized state - fully actual"
        else:
            state = "Indeterminate"
            description = "Neither clearly potential nor actual"

        return {
            "state": state,
            "description": description,
            "note": "Actuality is prior to potentiality in substance and definition"
        }

    def _assess_phronesis(self, text: str) -> Dict[str, Any]:
        """
        Assess practical wisdom (φρόνησις/phronesis).

        Phronesis = right judgment in particular situations
        Not abstract knowledge, but concrete wisdom about what to do
        """
        text_lower = text.lower()

        # Practical judgment indicators
        judgment_words = ["decide", "judge", "discern", "choose", "consider", "weigh"]
        has_judgment = sum(1 for word in judgment_words if word in text_lower)

        # Situational awareness
        situation_words = ["situation", "context", "circumstance", "case", "particular", "specific"]
        has_situation = sum(1 for word in situation_words if word in text_lower)

        # Action orientation
        action_words = ["do", "act", "should", "ought", "action", "practice"]
        has_action = sum(1 for word in action_words if word in text_lower)

        # Experience/habituation
        experience_words = ["experience", "learned", "practiced", "habit", "trained"]
        has_experience = sum(1 for word in experience_words if word in text_lower)

        total_score = has_judgment + has_situation + has_action + has_experience

        if total_score >= 4:
            level = "High Phronesis"
            description = "Strong practical wisdom - good judgment in particular cases"
        elif total_score >= 2:
            level = "Moderate Phronesis"
            description = "Some practical wisdom - developing judgment"
        elif total_score >= 1:
            level = "Low Phronesis"
            description = "Limited practical wisdom - inexperience or abstraction"
        else:
            level = "No Clear Phronesis"
            description = "Practical wisdom not evident"

        return {
            "level": level,
            "description": description,
            "note": "Phronesis is the intellectual virtue that guides right action"
        }

    def _identify_telos(self, text: str) -> Dict[str, Any]:
        """
        Identify the telos (τέλος) - purpose, end, goal.

        Everything in nature has a telos toward which it aims.
        For humans, the ultimate telos is eudaimonia.
        """
        text_lower = text.lower()

        # Purpose/end indicators
        purpose_words = ["purpose", "goal", "aim", "end", "objective", "point"]
        has_purpose = any(word in text_lower for word in purpose_words)

        # Direction/orientation
        direction_words = ["toward", "for", "seeking", "pursue", "strive"]
        has_direction = any(word in text_lower for word in direction_words)

        # Final end indicators
        ultimate_words = ["ultimate", "final", "highest", "greatest", "supreme"]
        has_ultimate = any(word in text_lower for word in ultimate_words)

        if has_ultimate and has_purpose:
            telos_type = "Ultimate Telos"
            description = "The highest end - possibly eudaimonia itself"
        elif has_purpose or has_direction:
            telos_type = "Intermediate Telos"
            description = "A goal that may serve a higher purpose"
        else:
            telos_type = "No Clear Telos"
            description = "Purpose or end not explicitly stated"

        return {
            "type": telos_type,
            "description": description,
            "principle": "All things aim at some good - the ultimate telos is eudaimonia"
        }

    def _evaluate_character(self, text: str) -> Dict[str, Any]:
        """
        Evaluate character (ἦθος/ethos) formation.

        Character is formed through habituation - we become just by doing just acts.
        """
        text_lower = text.lower()

        # Habituation indicators
        habit_words = ["habit", "practice", "regular", "repeatedly", "always", "custom"]
        has_habit = sum(1 for word in habit_words if word in text_lower)

        # Character indicators
        character_words = ["character", "who i am", "type of person", "nature", "disposition"]
        has_character = sum(1 for word in character_words if word in text_lower)

        # Development indicators
        development_words = ["become", "develop", "cultivate", "form", "shape", "grow"]
        has_development = sum(1 for word in development_words if word in text_lower)

        total_score = has_habit + has_character + has_development

        if total_score >= 3:
            formation = "Active Character Formation"
            description = "Character being shaped through habituation and practice"
        elif total_score >= 1:
            formation = "Potential Character Formation"
            description = "Some awareness of character development"
        else:
            formation = "No Clear Character Formation"
            description = "Character development not explicitly addressed"

        return {
            "formation": formation,
            "description": description,
            "note": "We become virtuous by performing virtuous acts - character follows action"
        }

    def _construct_reasoning(
        self,
        virtue: Dict[str, Any],
        mean: Dict[str, Any],
        eudaimonia: Dict[str, Any],
        causes: Dict[str, List[str]],
        phronesis: Dict[str, Any],
        telos: Dict[str, Any]
    ) -> str:
        """Construct Aristotelian ethical reasoning."""
        primary_virtue = virtue["primary"]

        reasoning = (
            f"From an Aristotelian perspective, this text concerns {primary_virtue}. "
            f"Regarding the golden mean: {mean['description']}. "
            f"The level of eudaimonia (human flourishing) appears to be: {eudaimonia['description']}. "
        )

        # Add practical wisdom
        reasoning += f"Practical wisdom (phronesis): {phronesis['description']}. "

        # Add teleology
        reasoning += f"The telos (purpose): {telos['description']}. "

        # Add final cause if present
        if "purpose" in causes["final"][0].lower() or "identified" in causes["final"][0].lower():
            reasoning += "A final cause is recognized, indicating teleological thinking. "

        # Conclude with Aristotelian principle
        reasoning += (
            "Remember: virtue is acquired through habituation, and eudaimonia is achieved through "
            "a complete life lived in accordance with virtue and practical wisdom."
        )

        return reasoning
