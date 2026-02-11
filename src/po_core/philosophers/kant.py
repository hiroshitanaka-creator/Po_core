"""
Kant - German Critical Philosopher

Immanuel Kant (1724-1804)
Focus: Critical Philosophy, Categorical Imperative, Transcendental Idealism, Autonomy

Key Concepts:
- Categorical Imperative: Universal moral law with three formulations
- Phenomena vs Noumena: Appearances vs things-in-themselves
- Transcendental Idealism: Space and time as forms of intuition
- Categories of Understanding: 12 a priori concepts organizing experience
- Synthetic a Priori: Knowledge that is both informative and necessary
- Autonomy: Self-legislation of the moral law
- Duty (Pflicht): Acting from duty vs acting in conformity with duty
- The Sublime: Mathematical and dynamical sublime
- Kingdom of Ends: Community of rational beings treating each as ends
- Good Will: The only unconditionally good thing
- Critique of Pure Reason: Limits of theoretical reason
- Practical Reason: Primacy of practical over theoretical reason
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Kant(Philosopher):
    """
    Kant's critical philosophy and moral theory.

    Analyzes prompts through the lens of the categorical imperative,
    transcendental idealism, autonomy, duty, and the limits of reason.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Immanuel Kant",
            description="Critical philosopher focused on universal moral law, autonomy, duty, and the limits of reason",
        )
        self.tradition = "German Idealism / Critical Philosophy"
        self.key_concepts = ['categorical imperative', 'duty', 'autonomy', 'a priori', 'transcendental idealism']

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Kant's critical philosophical perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Kant's philosophical analysis
        """
        # Perform comprehensive Kantian analysis
        analysis = self._analyze_kantian_framework(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Critical Philosophy / Deontological Ethics",
            "tension": tension,
            "categorical_imperative": analysis["categorical_imperative"],
            "phenomena_noumena": analysis["phenomena_noumena"],
            "transcendental_idealism": analysis["transcendental_idealism"],
            "categories_understanding": analysis["categories"],
            "synthetic_apriori": analysis["synthetic_apriori"],
            "autonomy": analysis["autonomy"],
            "duty": analysis["duty"],
            "sublime": analysis["sublime"],
            "kingdom_of_ends": analysis["kingdom_of_ends"],
            "good_will": analysis["good_will"],
            "theoretical_reason": analysis["theoretical_reason"],
            "practical_reason": analysis["practical_reason"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Critical philosophy and deontological moral theory",
                "focus": "Universal moral law, autonomy, duty, and the architectonic of reason",
            },
        }

    def _analyze_kantian_framework(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Kantian critical analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Kantian dimensions
        categorical_imperative = self._analyze_categorical_imperative(prompt)
        phenomena_noumena = self._analyze_phenomena_noumena(prompt)
        transcendental_idealism = self._analyze_transcendental_idealism(prompt)
        categories = self._analyze_categories_of_understanding(prompt)
        synthetic_apriori = self._analyze_synthetic_apriori(prompt)
        autonomy = self._assess_autonomy(prompt)
        duty = self._analyze_duty(prompt)
        sublime = self._analyze_sublime(prompt)
        kingdom_of_ends = self._assess_kingdom_of_ends(prompt)
        good_will = self._assess_good_will(prompt)
        theoretical_reason = self._analyze_theoretical_reason(prompt)
        practical_reason = self._analyze_practical_reason(prompt)

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            categorical_imperative,
            autonomy,
            duty,
            good_will,
            phenomena_noumena,
            theoretical_reason,
            practical_reason,
        )

        return {
            "reasoning": reasoning,
            "categorical_imperative": categorical_imperative,
            "phenomena_noumena": phenomena_noumena,
            "transcendental_idealism": transcendental_idealism,
            "categories": categories,
            "synthetic_apriori": synthetic_apriori,
            "autonomy": autonomy,
            "duty": duty,
            "sublime": sublime,
            "kingdom_of_ends": kingdom_of_ends,
            "good_will": good_will,
            "theoretical_reason": theoretical_reason,
            "practical_reason": practical_reason,
        }

    def _analyze_categorical_imperative(self, text: str) -> Dict[str, Any]:
        """
        Analyze adherence to the Categorical Imperative.

        Three formulations:
        1. Universal Law: Act only according to that maxim whereby you can will that it become a universal law
        2. Humanity: Treat humanity, whether in yourself or others, always as an end, never merely as a means
        3. Kingdom of Ends: Act as if you were legislating for a kingdom of ends
        """
        text_lower = text.lower()

        # Universal Law Formulation indicators
        universal_words = [
            "universal",
            "always",
            "everyone",
            "all people",
            "everywhere",
            "law",
        ]
        universal_count = sum(1 for word in universal_words if word in text_lower)

        # Universalizability test
        if any(
            phrase in text_lower
            for phrase in ["what if everyone", "if all", "everyone did this"]
        ):
            universalizable = True
            universal_test = "Explicitly considering universalizability"
        elif universal_count >= 2:
            universalizable = True
            universal_test = "Implicit universalizability"
        else:
            universalizable = False
            universal_test = "Not clearly universalizable"

        # Humanity Formulation indicators
        humanity_words = [
            "person",
            "human",
            "people",
            "dignity",
            "respect",
            "worth",
            "value",
        ]
        humanity_count = sum(1 for word in humanity_words if word in text_lower)

        # Means vs ends
        ends_words = ["end", "purpose", "goal", "for its own sake"]
        means_words = ["use", "tool", "means", "instrument", "exploit"]

        treats_as_end = sum(1 for phrase in ends_words if phrase in text_lower)
        treats_as_means = sum(1 for phrase in means_words if phrase in text_lower)

        if treats_as_end > treats_as_means and humanity_count >= 2:
            humanity_status = "Respects Humanity"
            humanity_desc = "Treating persons as ends in themselves"
        elif treats_as_means > treats_as_end:
            humanity_status = "Violates Humanity Formula"
            humanity_desc = "Treating persons merely as means"
        else:
            humanity_status = "Neutral"
            humanity_desc = "Humanity formulation not clearly addressed"

        # Kingdom of Ends indicators
        kingdom_words = [
            "community",
            "society",
            "shared",
            "mutual",
            "reciprocal",
            "legislation",
        ]
        kingdom_count = sum(1 for word in kingdom_words if word in text_lower)

        # Determine overall categorical imperative status
        if universalizable and humanity_status == "Respects Humanity":
            status = "Passes Categorical Imperative"
            description = (
                "Action appears to be a universal moral law respecting humanity"
            )
            moral_permissibility = "Morally Required"
        elif universalizable or humanity_status == "Respects Humanity":
            status = "Partially Aligned"
            description = "Some alignment with categorical imperative"
            moral_permissibility = "Possibly Permissible"
        elif humanity_status == "Violates Humanity Formula":
            status = "Violates Categorical Imperative"
            description = "Treats persons merely as means"
            moral_permissibility = "Morally Forbidden"
        else:
            status = "Indeterminate"
            description = "Insufficient information to apply categorical imperative"
            moral_permissibility = "Unclear"

        return {
            "status": status,
            "description": description,
            "moral_permissibility": moral_permissibility,
            "formulations": {
                "universal_law": {
                    "universalizable": universalizable,
                    "test": universal_test,
                    "score": universal_count,
                },
                "humanity": {
                    "status": humanity_status,
                    "description": humanity_desc,
                    "treats_as_end": treats_as_end,
                    "treats_as_means": treats_as_means,
                },
                "kingdom_of_ends": {
                    "score": kingdom_count,
                    "indication": (
                        "High"
                        if kingdom_count >= 3
                        else "Moderate"
                        if kingdom_count >= 1
                        else "Low"
                    ),
                },
            },
            "principle": "Act only according to that maxim whereby you can will that it become a universal law",
        }

    def _analyze_phenomena_noumena(self, text: str) -> Dict[str, Any]:
        """
        Analyze the distinction between phenomena (appearances) and noumena (things-in-themselves).

        Phenomena: Objects as they appear to us through the forms of sensibility
        Noumena: Things as they are in themselves, unknowable
        """
        text_lower = text.lower()

        # Phenomena indicators (appearances, experience, perception)
        phenomena_words = [
            "appear",
            "seem",
            "perceive",
            "experience",
            "observe",
            "sense",
        ]
        phenomena_count = sum(1 for word in phenomena_words if word in text_lower)

        # Noumena indicators (thing-in-itself, reality, beyond appearance)
        noumena_words = [
            "reality",
            "actual",
            "truly is",
            "in itself",
            "beyond",
            "real nature",
        ]
        noumena_count = sum(1 for phrase in noumena_words if phrase in text_lower)

        # Distinction awareness
        distinction_words = [
            "appear vs",
            "seems but is",
            "surface",
            "underlying reality",
        ]
        has_distinction = any(phrase in text_lower for phrase in distinction_words)

        # Limits of knowledge
        limits_words = [
            "cannot know",
            "unknowable",
            "limits",
            "beyond understanding",
            "inaccessible",
        ]
        recognizes_limits = any(phrase in text_lower for phrase in limits_words)

        if phenomena_count >= 2 and noumena_count >= 1:
            awareness = "Distinction Recognized"
            description = (
                "Aware of the difference between appearances and things-in-themselves"
            )
            stance = "Critical"
        elif phenomena_count >= 2:
            awareness = "Phenomenal Focus"
            description = "Focused on appearances and experience"
            stance = "Empirical"
        elif noumena_count >= 2:
            awareness = "Noumenal Speculation"
            description = (
                "Attempting to know things-in-themselves (transcendent metaphysics)"
            )
            stance = "Dogmatic"
        else:
            awareness = "Distinction Not Evident"
            description = "Phenomena/noumena distinction not addressed"
            stance = "Pre-critical"

        return {
            "awareness": awareness,
            "description": description,
            "stance": stance,
            "phenomena_emphasis": phenomena_count,
            "noumena_emphasis": noumena_count,
            "recognizes_limits": recognizes_limits,
            "principle": "We can know phenomena (appearances) but not noumena (things-in-themselves)",
        }

    def _analyze_transcendental_idealism(self, text: str) -> Dict[str, Any]:
        """
        Analyze transcendental idealism.

        Space and time are not properties of things-in-themselves but forms of our intuition.
        The categories of understanding structure all possible experience.
        """
        text_lower = text.lower()

        # Space and time as forms of intuition
        space_time_words = [
            "space",
            "time",
            "temporal",
            "spatial",
            "duration",
            "extension",
        ]
        space_time_count = sum(1 for word in space_time_words if word in text_lower)

        # Subjective contribution indicators
        subjective_words = [
            "perceive",
            "mind",
            "consciousness",
            "subject",
            "experience",
            "intuition",
        ]
        subjective_count = sum(1 for word in subjective_words if word in text_lower)

        # A priori indicators
        apriori_words = ["necessary", "prior to", "before", "precondition", "condition"]
        apriori_count = sum(1 for phrase in apriori_words if phrase in text_lower)

        # Structure/framework indicators
        structure_words = ["structure", "framework", "organize", "constitute", "form"]
        structure_count = sum(1 for word in structure_words if word in text_lower)

        if space_time_count >= 2 and subjective_count >= 2 and structure_count >= 1:
            position = "Transcendental Idealism"
            description = (
                "Recognition that space/time and categories structure experience"
            )
            status = "Critical philosophy"
        elif subjective_count >= 2 and structure_count >= 1:
            position = "Subjective Structuring"
            description = "Awareness of mind's contribution to experience"
            status = "Proto-critical"
        elif space_time_count >= 1:
            position = "Space-Time Awareness"
            description = "Mentions space/time but not as forms of intuition"
            status = "Pre-critical"
        else:
            position = "No Transcendental Analysis"
            description = "Transcendental conditions of experience not addressed"
            status = "Naive"

        return {
            "position": position,
            "description": description,
            "status": status,
            "space_time_score": space_time_count,
            "subjective_contribution": subjective_count,
            "apriori_recognition": apriori_count >= 2,
            "principle": "Space and time are pure forms of sensible intuition, not properties of things-in-themselves",
        }

    def _analyze_categories_of_understanding(self, text: str) -> Dict[str, Any]:
        """
        Analyze the 12 Categories of Understanding.

        Four groups of three:
        1. Quantity: Unity, Plurality, Totality
        2. Quality: Reality, Negation, Limitation
        3. Relation: Substance-Accident, Cause-Effect, Community
        4. Modality: Possibility, Existence, Necessity
        """
        text_lower = text.lower()

        categories_present = []

        # Quantity categories
        if any(word in text_lower for word in ["one", "unity", "single", "whole"]):
            categories_present.append("Unity")
        if any(
            word in text_lower for word in ["many", "multiple", "plural", "several"]
        ):
            categories_present.append("Plurality")
        if any(word in text_lower for word in ["all", "total", "totality", "complete"]):
            categories_present.append("Totality")

        # Quality categories
        if any(
            word in text_lower for word in ["real", "reality", "actual", "positive"]
        ):
            categories_present.append("Reality")
        if any(
            word in text_lower for word in ["not", "negation", "negative", "denial"]
        ):
            categories_present.append("Negation")
        if any(
            word in text_lower for word in ["limit", "limitation", "bounded", "finite"]
        ):
            categories_present.append("Limitation")

        # Relation categories
        if any(
            word in text_lower for word in ["substance", "thing", "object", "persist"]
        ):
            categories_present.append("Substance")
        if any(word in text_lower for word in ["cause", "effect", "because", "result"]):
            categories_present.append("Causality")
        if any(
            word in text_lower
            for word in ["interact", "mutual", "reciprocal", "community"]
        ):
            categories_present.append("Community")

        # Modality categories
        if any(word in text_lower for word in ["possible", "can", "might", "could"]):
            categories_present.append("Possibility")
        if any(word in text_lower for word in ["exist", "is", "actual", "being"]):
            categories_present.append("Existence")
        if any(
            word in text_lower for word in ["necessary", "must", "cannot be otherwise"]
        ):
            categories_present.append("Necessity")

        # Determine which groups are represented
        groups = {
            "Quantity": len(
                [
                    c
                    for c in categories_present
                    if c in ["Unity", "Plurality", "Totality"]
                ]
            ),
            "Quality": len(
                [
                    c
                    for c in categories_present
                    if c in ["Reality", "Negation", "Limitation"]
                ]
            ),
            "Relation": len(
                [
                    c
                    for c in categories_present
                    if c in ["Substance", "Causality", "Community"]
                ]
            ),
            "Modality": len(
                [
                    c
                    for c in categories_present
                    if c in ["Possibility", "Existence", "Necessity"]
                ]
            ),
        }

        dominant_group = max(groups, key=groups.get) if any(groups.values()) else "None"

        return {
            "categories_identified": categories_present,
            "count": len(categories_present),
            "groups": groups,
            "dominant_group": dominant_group,
            "principle": "The 12 categories are a priori concepts that structure all possible experience",
        }

    def _analyze_synthetic_apriori(self, text: str) -> Dict[str, Any]:
        """
        Analyze synthetic a priori judgments.

        Analytic: Predicate contained in subject (e.g., "All bachelors are unmarried")
        Synthetic: Predicate adds new information (e.g., "This table is heavy")
        A priori: Known independent of experience (e.g., "7+5=12")
        A posteriori: Known through experience (e.g., "The cat is on the mat")

        Synthetic a priori: Informative yet necessary (e.g., mathematical truths, causality)
        """
        text_lower = text.lower()

        # Necessity indicators (a priori)
        necessity_words = [
            "necessary",
            "must",
            "always",
            "cannot be otherwise",
            "necessarily",
        ]
        necessity_count = sum(1 for phrase in necessity_words if phrase in text_lower)

        # Informativeness indicators (synthetic)
        informative_words = ["new", "discover", "learn", "inform", "reveal"]
        informative_count = sum(1 for word in informative_words if word in text_lower)

        # Mathematics indicators (paradigm of synthetic a priori)
        math_words = ["mathematics", "geometry", "arithmetic", "calculate", "equation"]
        has_mathematics = any(word in text_lower for word in math_words)

        # Causality (synthetic a priori concept)
        causality_words = [
            "cause",
            "effect",
            "because",
            "therefore",
            "necessary connection",
        ]
        has_causality = any(phrase in text_lower for phrase in causality_words)

        # Experience independence
        apriori_words = [
            "prior to experience",
            "independent of experience",
            "before experience",
        ]
        apriori_explicit = any(phrase in text_lower for phrase in apriori_words)

        if (necessity_count >= 2 and informative_count >= 1) or has_mathematics:
            judgment_type = "Synthetic a Priori"
            description = (
                "Combines necessity with informativeness - extends knowledge a priori"
            )
            epistemic_status = "Foundational"
        elif necessity_count >= 2:
            judgment_type = "A Priori (possibly analytic)"
            description = "Necessary but may not extend knowledge"
            epistemic_status = "Formal"
        elif informative_count >= 2:
            judgment_type = "Synthetic a Posteriori"
            description = "Informative but derived from experience"
            epistemic_status = "Empirical"
        else:
            judgment_type = "Indeterminate"
            description = "Judgment type unclear"
            epistemic_status = "Unknown"

        return {
            "judgment_type": judgment_type,
            "description": description,
            "epistemic_status": epistemic_status,
            "necessity": necessity_count >= 2,
            "informative": informative_count >= 1,
            "has_mathematics": has_mathematics,
            "has_causality": has_causality,
            "principle": "Synthetic a priori judgments are possible and ground metaphysics and mathematics",
        }

    def _assess_autonomy(self, text: str) -> Dict[str, Any]:
        """
        Assess autonomy (self-legislation).

        Autonomy: The will gives itself the moral law
        Heteronomy: The will is determined by external factors (inclination, authority, consequences)
        """
        text_lower = text.lower()

        # Autonomy indicators
        autonomy_words = [
            "self",
            "own",
            "myself",
            "choose",
            "free",
            "autonomous",
            "self-determine",
        ]
        autonomy_count = sum(1 for word in autonomy_words if word in text_lower)

        # Rational self-legislation
        legislation_words = ["law", "principle", "reason", "rational", "legislate"]
        legislation_count = sum(1 for word in legislation_words if word in text_lower)

        # Heteronomy indicators
        heteronomy_words = [
            "want",
            "desire",
            "feel like",
            "commanded",
            "told",
            "authority says",
        ]
        heteronomy_count = sum(1 for phrase in heteronomy_words if phrase in text_lower)

        # Inclination vs duty
        inclination_words = ["want to", "desire to", "enjoy", "pleasant", "feel good"]
        duty_words = ["should", "ought", "must", "duty", "obligation", "required"]

        inclination_score = sum(
            1 for phrase in inclination_words if phrase in text_lower
        )
        duty_score = sum(1 for phrase in duty_words if phrase in text_lower)

        if (
            autonomy_count >= 2
            and legislation_count >= 1
            and duty_score > inclination_score
        ):
            status = "Autonomous"
            description = "Self-legislation through practical reason - moral autonomy"
            will_type = "Free Will"
        elif autonomy_count >= 2:
            status = "Tends toward Autonomy"
            description = "Some self-determination but not clearly moral autonomy"
            will_type = "Partially Free"
        elif heteronomy_count >= 2 or inclination_score > duty_score + 2:
            status = "Heteronomous"
            description = "Will determined by inclination or external authority"
            will_type = "Unfree Will"
        else:
            status = "Undetermined"
            description = "Autonomy/heteronomy status unclear"
            will_type = "Unclear"

        return {
            "status": status,
            "description": description,
            "will_type": will_type,
            "autonomy_score": autonomy_count,
            "heteronomy_score": heteronomy_count,
            "inclination_vs_duty": {
                "inclination": inclination_score,
                "duty": duty_score,
            },
            "principle": "Autonomy is the ground of human dignity - the will giving itself the moral law",
        }

    def _analyze_duty(self, text: str) -> Dict[str, Any]:
        """
        Analyze duty (Pflicht).

        Acting from duty: Motivated by respect for the moral law (moral worth)
        Acting in conformity with duty: External compliance, motivated by inclination (no moral worth)
        Contrary to duty: Violates the moral law
        """
        text_lower = text.lower()

        # Duty language
        duty_words = [
            "duty",
            "obligation",
            "ought",
            "should",
            "must",
            "required",
            "imperative",
        ]
        duty_count = sum(1 for phrase in duty_words if phrase in text_lower)

        # Motivation by respect for law
        respect_words = [
            "respect",
            "reverence",
            "moral law",
            "principle",
            "because it is right",
        ]
        respect_count = sum(1 for phrase in respect_words if phrase in text_lower)

        # Inclination language
        inclination_words = [
            "want",
            "desire",
            "like",
            "enjoy",
            "pleasant",
            "benefit",
            "advantage",
        ]
        inclination_count = sum(1 for word in inclination_words if word in text_lower)

        # Conflict indicators
        conflict_words = ["even though", "despite", "against my wishes", "reluctantly"]
        has_conflict = any(phrase in text_lower for phrase in conflict_words)

        if duty_count >= 2 and respect_count >= 1 and has_conflict:
            status = "Acting from Duty"
            description = "Motivated by respect for moral law, even against inclination"
            moral_worth = "Has Moral Worth"
        elif duty_count >= 2 and respect_count >= 1:
            status = "Acting from Duty"
            description = "Motivated by respect for the moral law"
            moral_worth = "Has Moral Worth"
        elif duty_count >= 1 and inclination_count >= 2:
            status = "Acting in Conformity with Duty"
            description = "External compliance but motivated by inclination"
            moral_worth = "No Moral Worth (though permissible)"
        elif duty_count >= 1:
            status = "Duty Acknowledged"
            description = "Duty recognized but motivation unclear"
            moral_worth = "Uncertain"
        else:
            status = "Duty Not Evident"
            description = "No clear duty considerations"
            moral_worth = "Not Applicable"

        return {
            "status": status,
            "description": description,
            "moral_worth": moral_worth,
            "duty_score": duty_count,
            "respect_for_law": respect_count >= 1,
            "inclination_present": inclination_count >= 1,
            "duty_inclination_conflict": has_conflict,
            "principle": "Only actions done from duty (not merely in conformity with duty) have moral worth",
        }

    def _analyze_sublime(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sublime (das Erhabene).

        Mathematical Sublime: Absolutely large (e.g., starry sky, ocean)
        Dynamical Sublime: Power that threatens (e.g., storm, volcano)

        The sublime reveals our supersensible faculty of reason, our moral vocation.
        """
        text_lower = text.lower()

        # Mathematical sublime indicators (vastness, infinity, magnitude)
        mathematical_words = [
            "vast",
            "infinite",
            "immense",
            "boundless",
            "enormous",
            "measureless",
        ]
        mathematical_count = sum(1 for word in mathematical_words if word in text_lower)

        # Dynamical sublime indicators (power, might, terror)
        dynamical_words = [
            "powerful",
            "mighty",
            "terrible",
            "overwhelming",
            "awesome",
            "fearsome",
        ]
        dynamical_count = sum(1 for word in dynamical_words if word in text_lower)

        # Sublime objects
        sublime_objects = [
            "mountain",
            "ocean",
            "sky",
            "storm",
            "volcano",
            "abyss",
            "universe",
        ]
        has_sublime_object = any(obj in text_lower for obj in sublime_objects)

        # Feeling of inadequacy followed by elevation
        inadequacy_words = ["small", "insignificant", "overwhelmed", "cannot grasp"]
        elevation_words = ["transcend", "rise above", "moral", "dignity", "reason"]

        has_inadequacy = any(phrase in text_lower for phrase in inadequacy_words)
        has_elevation = any(word in text_lower for word in elevation_words)

        if (mathematical_count >= 2 or dynamical_count >= 2) and has_sublime_object:
            if has_inadequacy and has_elevation:
                sublime_type = "Full Sublime Experience"
                description = (
                    "Inadequacy of imagination followed by elevation through reason"
                )
            elif mathematical_count > dynamical_count:
                sublime_type = "Mathematical Sublime"
                description = (
                    "Confronting the absolutely large - magnitude beyond comprehension"
                )
            else:
                sublime_type = "Dynamical Sublime"
                description = "Confronting overwhelming power while remaining safe"
        elif has_sublime_object:
            sublime_type = "Potential Sublime"
            description = "Object capable of eliciting the sublime"
        else:
            sublime_type = "No Sublime"
            description = "The sublime not evident"

        return {
            "sublime_type": sublime_type,
            "description": description,
            "mathematical_score": mathematical_count,
            "dynamical_score": dynamical_count,
            "has_sublime_object": has_sublime_object,
            "reveals_supersensible": has_elevation,
            "principle": "The sublime reveals our supersensible faculty and moral vocation beyond nature",
        }

    def _assess_kingdom_of_ends(self, text: str) -> Dict[str, Any]:
        """
        Assess the Kingdom of Ends (Reich der Zwecke).

        A systematic union of rational beings through common objective laws.
        Each member is both legislator and subject - all are ends in themselves.
        """
        text_lower = text.lower()

        # Community/kingdom indicators
        community_words = [
            "community",
            "society",
            "kingdom",
            "all",
            "everyone",
            "together",
        ]
        community_count = sum(1 for word in community_words if word in text_lower)

        # Rational beings
        rational_words = ["rational", "reason", "persons", "beings", "humanity"]
        rational_count = sum(1 for word in rational_words if word in text_lower)

        # Ends in themselves
        ends_words = [
            "end in itself",
            "inherent worth",
            "dignity",
            "sacred",
            "absolute value",
        ]
        ends_count = sum(1 for phrase in ends_words if phrase in text_lower)

        # Mutual legislation
        legislation_words = ["law", "legislate", "principle", "rule", "govern"]
        legislation_count = sum(1 for word in legislation_words if word in text_lower)

        # Reciprocity
        reciprocity_words = [
            "mutual",
            "reciprocal",
            "each other",
            "one another",
            "shared",
        ]
        reciprocity_count = sum(
            1 for phrase in reciprocity_words if phrase in text_lower
        )

        total_score = community_count + rational_count + ends_count + reciprocity_count

        if total_score >= 4 and legislation_count >= 1:
            status = "Kingdom of Ends"
            description = (
                "A systematic union of rational beings under common moral laws"
            )
            realization = "Moral Ideal"
        elif community_count >= 2 and ends_count >= 1:
            status = "Approaching Kingdom of Ends"
            description = "Recognition of community of rational beings as ends"
            realization = "Partial Recognition"
        elif community_count >= 1:
            status = "Community Recognized"
            description = "Some awareness of social bonds"
            realization = "Not Yet Moral Ideal"
        else:
            status = "No Kingdom of Ends"
            description = "Kingdom of Ends not addressed"
            realization = "Not Evident"

        return {
            "status": status,
            "description": description,
            "realization": realization,
            "community_score": community_count,
            "treats_as_ends": ends_count >= 1,
            "reciprocity": reciprocity_count >= 1,
            "principle": "Act as a member of a kingdom of ends - a systematic union of rational beings",
        }

    def _assess_good_will(self, text: str) -> Dict[str, Any]:
        """
        Assess the good will.

        The good will is the only thing good without qualification.
        Not good for what it accomplishes, but good in itself.
        """
        text_lower = text.lower()

        # Good will indicators
        will_words = ["will", "intention", "motive", "motivate"]
        will_count = sum(1 for word in will_words if word in text_lower)

        # Intrinsic goodness
        intrinsic_words = [
            "good in itself",
            "intrinsically",
            "inherently",
            "unconditionally",
        ]
        intrinsic_count = sum(1 for phrase in intrinsic_words if phrase in text_lower)

        # Duty/moral motivation
        moral_words = ["duty", "right", "ought", "moral", "principle"]
        moral_count = sum(1 for word in moral_words if word in text_lower)

        # Results/consequences (contrasted with good will)
        results_words = ["result", "outcome", "consequence", "success", "achieve"]
        results_count = sum(1 for word in results_words if word in text_lower)

        # Pure motivation (not mixed with inclination)
        pure_words = ["pure", "solely", "only", "merely because"]
        pure_count = sum(1 for phrase in pure_words if phrase in text_lower)

        if (
            will_count >= 1
            and moral_count >= 2
            and (intrinsic_count >= 1 or pure_count >= 1)
        ):
            status = "Good Will Present"
            description = "Will determined by duty and the moral law alone"
            value = "Unconditional Worth"
        elif will_count >= 1 and moral_count >= 1:
            status = "Moral Will"
            description = "Some moral motivation present"
            value = "Conditional Worth"
        elif results_count > moral_count and will_count >= 1:
            status = "Consequentialist Will"
            description = "Will focused on outcomes rather than moral law"
            value = "Instrumental Worth"
        else:
            status = "Will Not Evident"
            description = "Good will not clearly addressed"
            value = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "value": value,
            "motivated_by_duty": moral_count >= 2,
            "unconditional": intrinsic_count >= 1,
            "pure": pure_count >= 1,
            "principle": "A good will is the only thing good without qualification",
        }

    def _analyze_theoretical_reason(self, text: str) -> Dict[str, Any]:
        """
        Analyze theoretical reason (critique of pure reason).

        Theoretical reason is limited to phenomena (possible experience).
        Cannot know God, freedom, immortality - only think them.
        """
        text_lower = text.lower()

        # Knowledge claims
        knowledge_words = ["know", "knowledge", "certain", "prove", "demonstrate"]
        knowledge_count = sum(1 for word in knowledge_words if word in text_lower)

        # Experience/phenomena
        experience_words = ["experience", "perceive", "observe", "empirical"]
        experience_count = sum(1 for word in experience_words if word in text_lower)

        # Transcendent objects (beyond possible experience)
        transcendent_words = [
            "god",
            "soul",
            "immortal",
            "freedom",
            "infinity",
            "absolute",
        ]
        transcendent_count = sum(1 for word in transcendent_words if word in text_lower)

        # Limits of knowledge
        limits_words = [
            "cannot know",
            "unknowable",
            "beyond knowledge",
            "limits of reason",
        ]
        recognizes_limits = any(phrase in text_lower for phrase in limits_words)

        # Speculation vs critical stance
        speculation_words = [
            "speculate",
            "metaphysics",
            "transcendent",
            "beyond experience",
        ]
        has_speculation = any(phrase in text_lower for phrase in speculation_words)

        if knowledge_count >= 2 and recognizes_limits and transcendent_count >= 1:
            stance = "Critical"
            description = (
                "Recognizes limits of theoretical reason regarding transcendent objects"
            )
            status = "Post-Critique"
        elif knowledge_count >= 2 and experience_count >= 2:
            stance = "Empirical"
            description = "Knowledge claims limited to possible experience"
            status = "Scientific"
        elif transcendent_count >= 2 and not recognizes_limits:
            stance = "Dogmatic"
            description = (
                "Claims knowledge of transcendent objects - pre-critical metaphysics"
            )
            status = "Transcendent Illusion"
        else:
            stance = "Undetermined"
            description = "Theoretical reason stance unclear"
            status = "Not Addressed"

        return {
            "stance": stance,
            "description": description,
            "status": status,
            "knowledge_claims": knowledge_count,
            "recognizes_limits": recognizes_limits,
            "transcendent_objects": transcendent_count >= 1,
            "principle": "Theoretical reason is limited to phenomena - we cannot know things-in-themselves",
        }

    def _analyze_practical_reason(self, text: str) -> Dict[str, Any]:
        """
        Analyze practical reason (critique of practical reason).

        Practical reason determines the will through the moral law.
        Has primacy over theoretical reason - postulates freedom, God, immortality.
        """
        text_lower = text.lower()

        # Practical reason indicators
        practical_words = ["should", "ought", "must", "duty", "act", "do", "will"]
        practical_count = sum(1 for phrase in practical_words if phrase in text_lower)

        # Moral law
        moral_law_words = ["moral law", "categorical imperative", "principle", "maxim"]
        moral_law_count = sum(1 for phrase in moral_law_words if phrase in text_lower)

        # Freedom/autonomy
        freedom_words = ["free", "freedom", "autonomous", "self-legislate"]
        freedom_count = sum(1 for word in freedom_words if word in text_lower)

        # Postulates of practical reason
        postulates = {
            "freedom": any(
                word in text_lower for word in ["free", "freedom", "autonomous"]
            ),
            "god": "god" in text_lower or "divine" in text_lower,
            "immortality": any(
                word in text_lower for word in ["immortal", "eternal", "afterlife"]
            ),
        }
        postulates_count = sum(postulates.values())

        # Primacy over theoretical
        primacy_words = [
            "primacy",
            "practical over theoretical",
            "must believe",
            "faith",
        ]
        has_primacy = any(phrase in text_lower for phrase in primacy_words)

        if practical_count >= 3 and moral_law_count >= 1 and freedom_count >= 1:
            status = "Strong Practical Reason"
            description = "Practical reason determining the will through the moral law"
            orientation = "Deontological"
        elif practical_count >= 2:
            status = "Practical Orientation"
            description = "Some practical reasoning about action"
            orientation = "Action-focused"
        elif practical_count >= 1:
            status = "Weak Practical Reason"
            description = "Minimal practical considerations"
            orientation = "Limited"
        else:
            status = "No Practical Reason"
            description = "Practical reason not engaged"
            orientation = "Theoretical Only"

        return {
            "status": status,
            "description": description,
            "orientation": orientation,
            "practical_count": practical_count,
            "moral_law_present": moral_law_count >= 1,
            "freedom_recognized": postulates["freedom"],
            "postulates": postulates,
            "postulates_count": postulates_count,
            "principle": "Practical reason has primacy - determines the will through the moral law",
        }

    def _construct_reasoning(
        self,
        categorical_imperative: Dict[str, Any],
        autonomy: Dict[str, Any],
        duty: Dict[str, Any],
        good_will: Dict[str, Any],
        phenomena_noumena: Dict[str, Any],
        theoretical_reason: Dict[str, Any],
        practical_reason: Dict[str, Any],
    ) -> str:
        """Construct comprehensive Kantian philosophical reasoning."""
        reasoning = (
            f"From a Kantian critical perspective, this text must be examined through both "
            f"theoretical and practical reason. "
        )

        # Categorical imperative analysis
        reasoning += (
            f"Categorical imperative: {categorical_imperative['status']} - "
            f"{categorical_imperative['description']}. "
        )

        # Autonomy
        reasoning += f"Autonomy: {autonomy['status']} - {autonomy['description']}. "

        # Duty and moral worth
        if duty["status"] != "Duty Not Evident":
            reasoning += f"Duty: {duty['status']} with {duty['moral_worth']}. "

        # Good will
        if good_will["status"] != "Will Not Evident":
            reasoning += f"Good will: {good_will['description']}. "

        # Theoretical limits
        reasoning += (
            f"Theoretical reason: {theoretical_reason['stance']} - "
            f"{theoretical_reason['description']}. "
        )

        # Practical reason
        reasoning += (
            f"Practical reason: {practical_reason['status']} - "
            f"{practical_reason['description']}. "
        )

        # Phenomena/noumena
        reasoning += f"Phenomena/noumena: {phenomena_noumena['awareness']}. "

        # Concluding Kantian wisdom
        reasoning += (
            "Remember: Act only according to that maxim whereby you can will that it become a universal law. "
            "Treat humanity, whether in yourself or others, always as an end, never merely as a means. "
            "The moral law reveals our freedom and dignity as rational beings."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Kantian analysis.

        Tensions arise from:
        - Violation of categorical imperative
        - Heteronomy (lack of autonomy)
        - Acting from inclination rather than duty
        - Treating persons as mere means
        - Dogmatic metaphysics (exceeding limits of reason)
        - Consequentialism over deontology
        """
        tension_score = 0
        tension_elements = []

        # Check categorical imperative
        ci_status = analysis["categorical_imperative"]["status"]
        if ci_status == "Violates Categorical Imperative":
            tension_score += 3
            tension_elements.append("Violates the categorical imperative")
        elif ci_status == "Indeterminate":
            tension_score += 1
            tension_elements.append("Unclear moral status")

        # Check autonomy
        autonomy_status = analysis["autonomy"]["status"]
        if autonomy_status == "Heteronomous":
            tension_score += 2
            tension_elements.append("Heteronomous will - determined by inclination")
        elif autonomy_status == "Undetermined":
            tension_score += 1
            tension_elements.append("Autonomy unclear")

        # Check duty
        duty_moral_worth = analysis["duty"]["moral_worth"]
        if "No Moral Worth" in duty_moral_worth:
            tension_score += 1
            tension_elements.append("Acting in conformity with duty, not from duty")

        # Check humanity formula
        humanity_status = analysis["categorical_imperative"]["formulations"][
            "humanity"
        ]["status"]
        if humanity_status == "Violates Humanity Formula":
            tension_score += 2
            tension_elements.append("Treating persons merely as means")

        # Check theoretical reason
        theoretical_stance = analysis["theoretical_reason"]["stance"]
        if theoretical_stance == "Dogmatic":
            tension_score += 2
            tension_elements.append("Dogmatic metaphysics - exceeding limits of reason")

        # Check practical reason
        practical_status = analysis["practical_reason"]["status"]
        if practical_status == "No Practical Reason":
            tension_score += 1
            tension_elements.append("Lack of practical moral reasoning")

        # Determine tension level
        if tension_score >= 7:
            level = "Very High"
            description = "Severe moral violations - against the categorical imperative and human dignity"
        elif tension_score >= 5:
            level = "High"
            description = "Significant tensions in moral autonomy and duty"
        elif tension_score >= 3:
            level = "Moderate"
            description = "Some tensions between inclination and duty"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, generally aligned with moral law"
        else:
            level = "Very Low"
            description = "Well-aligned with Kantian moral principles"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
