"""
Nagarjuna - Madhyamaka Buddhist Philosopher

Nagarjuna (c. 150-250 CE)
Focus: Emptiness (Sunyata), Middle Way, Two Truths, Dependent Origination

Key Concepts:
- Sunyata (Emptiness): All phenomena are empty of inherent existence (svabhava)
- Two Truths: Conventional truth (samvrti) and ultimate truth (paramartha)
- Pratityasamutpada: Dependent origination - everything arises in dependence
- Catuskoti (Tetralemma): Four-cornered negation logic
- Svabhava: Critique of inherent existence or self-nature
- Nirvana-Samsara identity: Ultimately non-different
- Madhyamaka: The Middle Way between eternalism and nihilism
- Prasangika: Reductio ad absurdum argumentation
- Conventional language: Use while recognizing its limits
- Upaya (Skillful means): Teaching adapted to capacity
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Nagarjuna(Philosopher):
    """
    Nagarjuna's Madhyamaka (Middle Way) perspective.

    Analyzes prompts through the lens of emptiness (sunyata),
    dependent origination, two truths, and the tetralemma.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Nagarjuna",
            description="Madhyamaka philosopher focused on emptiness (sunyata), dependent origination, and the Middle Way",
        )
        self.tradition = "Madhyamaka Buddhism"
        self.key_concepts = ['sunyata (emptiness)', 'pratityasamutpada (dependent origination)', 'two truths doctrine', 'middle way', 'catuskoti (tetralemma)']

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze from Nagarjuna's Madhyamaka perspective."""
        analysis = self._analyze_madhyamaka(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Madhyamaka / Middle Way Buddhism",
            "tension": tension,
            "sunyata": analysis["sunyata"],
            "two_truths": analysis["two_truths"],
            "dependent_origination": analysis["dependent_origination"],
            "tetralemma": analysis["tetralemma"],
            "svabhava_critique": analysis["svabhava"],
            "nirvana_samsara": analysis["nirvana_samsara"],
            "middle_way": analysis["middle_way"],
            "skillful_means": analysis["skillful_means"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Madhyamaka dialectics",
                "focus": "Emptiness, dependent origination, two truths",
            },
        }

    def _analyze_madhyamaka(self, prompt: str) -> Dict[str, Any]:
        """Perform comprehensive Madhyamaka analysis."""
        sunyata = self._analyze_sunyata(prompt)
        two_truths = self._analyze_two_truths(prompt)
        dependent_origination = self._analyze_dependent_origination(prompt)
        tetralemma = self._analyze_tetralemma(prompt)
        svabhava = self._analyze_svabhava(prompt)
        nirvana_samsara = self._analyze_nirvana_samsara(prompt)
        middle_way = self._analyze_middle_way(prompt)
        skillful_means = self._analyze_skillful_means(prompt)

        reasoning = self._construct_reasoning(
            sunyata, two_truths, dependent_origination, tetralemma, svabhava, middle_way
        )

        return {
            "reasoning": reasoning,
            "sunyata": sunyata,
            "two_truths": two_truths,
            "dependent_origination": dependent_origination,
            "tetralemma": tetralemma,
            "svabhava": svabhava,
            "nirvana_samsara": nirvana_samsara,
            "middle_way": middle_way,
            "skillful_means": skillful_means,
        }

    def _analyze_sunyata(self, text: str) -> Dict[str, Any]:
        """Analyze emptiness (sunyata) - all phenomena lack inherent existence."""
        text_lower = text.lower()

        emptiness_words = ["empty", "emptiness", "void", "nothing", "lack", "without"]
        emptiness_count = sum(1 for word in emptiness_words if word in text_lower)

        essence_words = [
            "essence",
            "inherent",
            "intrinsic",
            "nature",
            "self-nature",
            "own-being",
        ]
        essence_count = sum(1 for word in essence_words if word in text_lower)

        if emptiness_count >= 2:
            status = "Sunyata Recognized"
            description = (
                "Emptiness is acknowledged - phenomena lack inherent existence"
            )
        elif essence_count >= 2:
            status = "Reification Present"
            description = (
                "Clinging to essence/inherent existence - needs deconstruction"
            )
        elif emptiness_count >= 1:
            status = "Traces of Emptiness"
            description = "Some awareness of emptiness"
        else:
            status = "Emptiness Not Explicit"
            description = "The empty nature of phenomena not addressed"

        return {
            "status": status,
            "description": description,
            "emptiness_score": emptiness_count,
            "reification_score": essence_count,
            "principle": "Sunyata: All phenomena are empty of inherent existence (svabhava-sunya)",
        }

    def _analyze_two_truths(self, text: str) -> Dict[str, Any]:
        """Analyze the two truths doctrine."""
        text_lower = text.lower()

        conventional_words = [
            "conventional",
            "relative",
            "everyday",
            "practical",
            "ordinary",
            "common",
        ]
        conventional_count = sum(1 for word in conventional_words if word in text_lower)

        ultimate_words = [
            "ultimate",
            "absolute",
            "final",
            "true nature",
            "reality itself",
        ]
        ultimate_count = sum(1 for phrase in ultimate_words if phrase in text_lower)

        if conventional_count >= 1 and ultimate_count >= 1:
            status = "Two Truths Distinction"
            description = "Both conventional and ultimate levels recognized"
            level = "Integrated"
        elif ultimate_count >= 2:
            status = "Ultimate Emphasis"
            description = "Focus on ultimate truth - risk of nihilism"
            level = "Ultimate"
        elif conventional_count >= 2:
            status = "Conventional Emphasis"
            description = "Operating at conventional level"
            level = "Conventional"
        else:
            status = "Levels Not Distinguished"
            description = "Two truths distinction not explicit"
            level = "Undifferentiated"

        return {
            "status": status,
            "description": description,
            "level": level,
            "conventional_score": conventional_count,
            "ultimate_score": ultimate_count,
            "principle": "Two truths: conventional (samvrti-satya) and ultimate (paramartha-satya)",
        }

    def _analyze_dependent_origination(self, text: str) -> Dict[str, Any]:
        """Analyze pratityasamutpada - dependent origination."""
        text_lower = text.lower()

        dependence_words = [
            "depend",
            "dependent",
            "arise",
            "originate",
            "cause",
            "condition",
            "because",
            "due to",
            "from",
            "leads to",
            "result",
        ]
        dependence_count = sum(1 for word in dependence_words if word in text_lower)

        independence_words = [
            "independent",
            "standalone",
            "self-sufficient",
            "uncaused",
            "absolute",
        ]
        independence_count = sum(1 for word in independence_words if word in text_lower)

        if dependence_count >= 3:
            status = "Dependent Origination Recognized"
            description = "Things arise in dependence on conditions - pratityasamutpada"
        elif dependence_count >= 1:
            status = "Some Awareness of Dependence"
            description = "Causal relations acknowledged"
        elif independence_count >= 1:
            status = "Independence Assumed"
            description = (
                "Independent existence assumed - contrary to dependent origination"
            )
        else:
            status = "Origination Not Addressed"
            description = "Dependent arising not explicitly thematized"

        return {
            "status": status,
            "description": description,
            "dependence_score": dependence_count,
            "independence_score": independence_count,
            "principle": "Pratityasamutpada: Whatever arises, arises in dependence on conditions",
        }

    def _analyze_tetralemma(self, text: str) -> Dict[str, Any]:
        """Analyze catuskoti (tetralemma) - four-cornered negation."""
        text_lower = text.lower()

        negation_words = ["not", "neither", "nor", "none", "no"]
        negation_count = sum(1 for word in negation_words if word in text_lower)

        both_neither = ["both", "neither", "and yet", "at the same time"]
        both_neither_count = sum(1 for phrase in both_neither if phrase in text_lower)

        affirmation_words = ["is", "exists", "true", "real", "definitely"]
        affirmation_count = sum(1 for word in affirmation_words if word in text_lower)

        if negation_count >= 3 and both_neither_count >= 1:
            status = "Tetralemma Applied"
            description = "Four-cornered negation in use - neither X nor non-X nor both nor neither"
        elif negation_count >= 2:
            status = "Multiple Negations"
            description = "Negation in use but not full tetralemma"
        elif affirmation_count > negation_count:
            status = "Affirmative Logic"
            description = "Affirmative assertions dominate - tetralemma not applied"
        else:
            status = "Catuskoti Not Evident"
            description = "Four-cornered negation not applied"

        return {
            "status": status,
            "description": description,
            "negation_score": negation_count,
            "both_neither_score": both_neither_count,
            "principle": "Catuskoti: Not X, not non-X, not both, not neither - exhaustive negation",
        }

    def _analyze_svabhava(self, text: str) -> Dict[str, Any]:
        """Analyze svabhava (self-nature/inherent existence) - and its critique."""
        text_lower = text.lower()

        svabhava_words = [
            "essence",
            "nature",
            "inherent",
            "intrinsic",
            "self-nature",
            "truly",
            "really is",
            "in itself",
        ]
        svabhava_count = sum(1 for phrase in svabhava_words if phrase in text_lower)

        anti_svabhava = [
            "empty",
            "no essence",
            "without nature",
            "merely",
            "only appears",
        ]
        anti_svabhava_count = sum(1 for phrase in anti_svabhava if phrase in text_lower)

        if anti_svabhava_count >= 1:
            status = "Svabhava Deconstructed"
            description = "Inherent existence is negated - phenomena are svabhava-sunya"
        elif svabhava_count >= 2:
            status = "Svabhava Assumed"
            description = "Inherent existence is assumed - needs Madhyamaka critique"
        elif svabhava_count >= 1:
            status = "Some Essentialism"
            description = "Traces of essentialist thinking"
        else:
            status = "Svabhava Not Addressed"
            description = "Question of inherent existence not raised"

        return {
            "status": status,
            "description": description,
            "svabhava_score": svabhava_count,
            "anti_svabhava_score": anti_svabhava_count,
            "principle": "Svabhava-sunya: All phenomena are empty of inherent existence",
        }

    def _analyze_nirvana_samsara(self, text: str) -> Dict[str, Any]:
        """Analyze the identity of nirvana and samsara."""
        text_lower = text.lower()

        liberation_words = [
            "liberation",
            "freedom",
            "nirvana",
            "enlightenment",
            "awakening",
            "peace",
        ]
        liberation_count = sum(1 for word in liberation_words if word in text_lower)

        bondage_words = [
            "suffering",
            "bondage",
            "samsara",
            "cycle",
            "attachment",
            "craving",
        ]
        bondage_count = sum(1 for word in bondage_words if word in text_lower)

        identity_words = [
            "same",
            "identical",
            "no difference",
            "not separate",
            "non-dual",
        ]
        identity_count = sum(1 for phrase in identity_words if phrase in text_lower)

        if liberation_count >= 1 and bondage_count >= 1 and identity_count >= 1:
            status = "Identity Recognized"
            description = "Nirvana and samsara are not ultimately different"
        elif liberation_count >= 1 and bondage_count >= 1:
            status = "Both Present"
            description = "Both liberation and bondage mentioned but not identified"
        elif liberation_count >= 1:
            status = "Liberation Sought"
            description = "Liberation as goal - may assume duality with samsara"
        elif bondage_count >= 1:
            status = "Bondage Emphasized"
            description = "Focus on suffering - liberation may seem distant"
        else:
            status = "Neither Prominent"
            description = "Nirvana-samsara dynamic not thematized"

        return {
            "status": status,
            "description": description,
            "liberation_score": liberation_count,
            "bondage_score": bondage_count,
            "identity_awareness": identity_count >= 1,
            "principle": "Samsara is nirvana - there is no difference between them (MMK XXV.19)",
        }

    def _analyze_middle_way(self, text: str) -> Dict[str, Any]:
        """Analyze adherence to the Middle Way."""
        text_lower = text.lower()

        eternalism_words = [
            "eternal",
            "permanent",
            "forever",
            "unchanging",
            "absolute existence",
        ]
        eternalism_count = sum(1 for phrase in eternalism_words if phrase in text_lower)

        nihilism_words = [
            "nothing exists",
            "meaningless",
            "nihil",
            "nonexistent",
            "does not exist",
        ]
        nihilism_count = sum(1 for phrase in nihilism_words if phrase in text_lower)

        middle_words = ["middle", "balance", "neither extreme", "between", "moderate"]
        middle_count = sum(1 for phrase in middle_words if phrase in text_lower)

        if middle_count >= 1:
            status = "Middle Way"
            description = "Avoiding extremes of eternalism and nihilism"
            position = "Madhyamaka"
        elif eternalism_count > nihilism_count:
            status = "Eternalism Tendency"
            description = "Tendency toward eternalism - reifying existence"
            position = "Sasvatavada"
        elif nihilism_count > eternalism_count:
            status = "Nihilism Tendency"
            description = "Tendency toward nihilism - denying conventional existence"
            position = "Ucchedavada"
        elif eternalism_count >= 1 and nihilism_count >= 1:
            status = "Both Extremes Present"
            description = "Both eternalist and nihilist tendencies - need Middle Way"
            position = "Confused"
        else:
            status = "Extremes Not Evident"
            description = "Neither extreme explicitly present"
            position = "Undetermined"

        return {
            "status": status,
            "description": description,
            "position": position,
            "eternalism_score": eternalism_count,
            "nihilism_score": nihilism_count,
            "middle_way_score": middle_count,
            "principle": "Madhyamaka: The Middle Way between eternalism (sasvatavada) and nihilism (ucchedavada)",
        }

    def _analyze_skillful_means(self, text: str) -> Dict[str, Any]:
        """Analyze upaya (skillful means) - teaching adapted to capacity."""
        text_lower = text.lower()

        adaptation_words = [
            "adapt",
            "suitable",
            "appropriate",
            "according to",
            "level",
            "capacity",
        ]
        adaptation_count = sum(1 for word in adaptation_words if word in text_lower)

        teaching_words = ["teach", "explain", "show", "guide", "point", "indicate"]
        teaching_count = sum(1 for word in teaching_words if word in text_lower)

        if adaptation_count >= 1 and teaching_count >= 1:
            status = "Upaya Present"
            description = "Teaching adapted to capacity - skillful means in use"
        elif adaptation_count >= 1:
            status = "Adaptation Awareness"
            description = "Awareness of need for adaptation"
        elif teaching_count >= 1:
            status = "Teaching Present"
            description = "Teaching occurs but adaptation unclear"
        else:
            status = "Upaya Not Evident"
            description = "Skillful means not explicitly addressed"

        return {
            "status": status,
            "description": description,
            "adaptation_score": adaptation_count,
            "teaching_score": teaching_count,
            "principle": "Upaya: Teachings are expedient means adapted to the hearer's capacity",
        }

    def _construct_reasoning(
        self,
        sunyata: Dict[str, Any],
        two_truths: Dict[str, Any],
        dependent_origination: Dict[str, Any],
        tetralemma: Dict[str, Any],
        svabhava: Dict[str, Any],
        middle_way: Dict[str, Any],
    ) -> str:
        """Construct Madhyamaka reasoning."""
        reasoning = (
            f"From Nagarjuna's Madhyamaka perspective, this text is analyzed through the lens of emptiness. "
            f"Sunyata: {sunyata['description']}. "
            f"Two Truths: {two_truths['description']}. "
        )

        reasoning += f"Dependent Origination: {dependent_origination['description']}. "
        reasoning += f"Svabhava: {svabhava['description']}. "
        reasoning += f"Middle Way: {middle_way['description']}. "

        if tetralemma["status"] == "Tetralemma Applied":
            reasoning += "The tetralemma deconstructs all fixed positions. "

        reasoning += (
            "Remember: 'Whatever is dependently originated is declared to be emptiness. "
            "That, being a dependent designation, is itself the Middle Way.' (MMK XXIV.18)"
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate philosophical tension."""
        tension_score = 0
        tension_elements = []

        if analysis["sunyata"]["reification_score"] >= 2:
            tension_score += 2
            tension_elements.append("Reification of inherent existence")

        if analysis["svabhava"]["svabhava_score"] >= 2:
            tension_score += 2
            tension_elements.append("Svabhava assumed - needs deconstruction")

        if analysis["middle_way"]["position"] == "Sasvatavada":
            tension_score += 2
            tension_elements.append("Eternalism tendency")
        elif analysis["middle_way"]["position"] == "Ucchedavada":
            tension_score += 2
            tension_elements.append("Nihilism tendency")

        if analysis["dependent_origination"]["independence_score"] >= 1:
            tension_score += 1
            tension_elements.append("Independence assumed")

        if tension_score >= 5:
            level = "Very High"
            description = (
                "Strong reification and extremism - needs Madhyamaka deconstruction"
            )
        elif tension_score >= 3:
            level = "High"
            description = "Significant clinging to inherent existence"
        elif tension_score >= 1:
            level = "Moderate"
            description = "Some attachment to views"
        else:
            level = "Low"
            description = "Aligned with emptiness and Middle Way"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
