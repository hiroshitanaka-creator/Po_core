"""
Ludwig Wittgenstein - Language Philosopher

Ludwig Wittgenstein (1889-1951)
Focus: Language Games, Forms of Life, Meaning as Use, Limits of Language

Key Concepts:
Early Wittgenstein (Tractatus Logico-Philosophicus):
- "The world is everything that is the case"
- "Whereof one cannot speak, thereof one must be silent"
- "The limits of my language mean the limits of my world"
- Picture theory of language
- Logical atomism

Late Wittgenstein (Philosophical Investigations):
- Language Games (Sprachspiel): Language embedded in activities
- Forms of Life (Lebensform): Shared practices and agreements
- Family Resemblance: Concepts without rigid boundaries
- Meaning is Use: "The meaning of a word is its use in the language"
- Private Language Argument: No purely private language
- Philosophy as therapy: "Philosophical problems arise when language goes on holiday"
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Wittgenstein(Philosopher):
    """
    Ludwig Wittgenstein's language philosophy.

    Analyzes prompts through the lens of language games, forms of life,
    and the limits and uses of language.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Ludwig Wittgenstein",
            description="Language philosopher focused on language games, forms of life, and meaning as use",
        )
        self.tradition = "Analytic Philosophy / Language"
        self.key_concepts = [
            "language games",
            "forms of life",
            "family resemblance",
            "meaning as use",
            "private language argument",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Wittgenstein's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Wittgenstein's language analysis
        """
        # Perform Wittgensteinian analysis
        analysis = self._analyze_language(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Language Philosophy",
            "language_games": analysis["language_games"],
            "forms_of_life": analysis["forms_of_life"],
            "meaning_use": analysis["meaning_use"],
            "family_resemblance": analysis["family_resemblance"],
            "private_language": analysis["private_language"],
            "philosophical_confusion": analysis["confusion"],
            "limits_of_language": analysis["limits"],
            "early_vs_late": analysis["period"],
            "tension": {
                "level": "Moderate",
                "description": "Tension between saying and showing, rule and practice",
                "elements": [
                    "Language games have boundaries yet resist precise definition",
                    "Rules require interpretation yet cannot be infinitely regressed",
                    "What can be shown cannot always be said",
                ],
            },
            "metadata": {
                "philosopher": self.name,
                "approach": "Language analysis and conceptual clarification",
                "focus": "Language games, meaning as use, and forms of life",
            },
        }

    def _analyze_language(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Wittgensteinian language analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Identify language games
        language_games = self._identify_language_games(prompt)

        # Assess forms of life
        forms_of_life = self._assess_forms_of_life(prompt)

        # Evaluate meaning as use
        meaning_use = self._evaluate_meaning_use(prompt)

        # Check family resemblance
        family_resemblance = self._check_family_resemblance(prompt)

        # Analyze private language
        private_language = self._analyze_private_language(prompt)

        # Detect philosophical confusion
        confusion = self._detect_philosophical_confusion(prompt)

        # Check limits of language
        limits = self._check_limits_of_language(prompt)

        # Determine early vs late period
        period = self._determine_period(prompt)

        # Construct reasoning
        applied = self._apply_wittgenstein_to_problem(prompt)
        reasoning = self._construct_reasoning(
            language_games, forms_of_life, meaning_use, confusion, period
        )
        reasoning = f"{applied}\n\n{reasoning}"

        return {
            "reasoning": reasoning,
            "language_games": language_games,
            "forms_of_life": forms_of_life,
            "meaning_use": meaning_use,
            "family_resemblance": family_resemblance,
            "private_language": private_language,
            "confusion": confusion,
            "limits": limits,
            "period": period,
        }

    def _identify_language_games(self, text: str) -> Dict[str, Any]:
        """
        Identify language games (Sprachspiel) in the text.

        Language game = language embedded in an activity, a form of life
        Examples: Giving orders, describing objects, reporting events, making jokes, asking questions
        """
        text_lower = text.lower()
        games_detected = []

        # Directive language game (commands, requests)
        if any(
            word in text_lower
            for word in ["should", "must", "do this", "please", "command"]
        ):
            games_detected.append("Directive - giving orders or requests")

        # Descriptive language game (describing states of affairs)
        if any(
            word in text_lower
            for word in ["is", "are", "describe", "looks like", "appears"]
        ):
            games_detected.append("Descriptive - describing how things are")

        # Interrogative language game (asking questions)
        if any(char in text for char in ["?", "what", "how", "why", "when", "where"]):
            games_detected.append("Interrogative - asking questions")

        # Expressive language game (expressing feelings, attitudes)
        if any(
            word in text_lower
            for word in ["feel", "hope", "wish", "love", "hate", "believe"]
        ):
            games_detected.append("Expressive - expressing inner states")

        # Performative language game (doing things with words)
        if any(
            word in text_lower
            for word in ["promise", "declare", "apologize", "thank", "name"]
        ):
            games_detected.append("Performative - performing actions through words")

        # Evaluative language game (making judgments)
        if any(
            word in text_lower
            for word in ["good", "bad", "right", "wrong", "beautiful", "ugly"]
        ):
            games_detected.append("Evaluative - making value judgments")

        # Explanatory language game (giving reasons)
        if any(
            word in text_lower
            for word in ["because", "since", "therefore", "reason", "explain"]
        ):
            games_detected.append("Explanatory - giving reasons and explanations")

        if not games_detected:
            games_detected.append("Unclear - language game not readily identifiable")

        return {
            "games": games_detected,
            "count": len(games_detected),
            "primary": games_detected[0],
            "note": "Language games are language embedded in activities and forms of life",
        }

    def _assess_forms_of_life(self, text: str) -> Dict[str, Any]:
        """
        Assess the forms of life (Lebensform) implicit in the text.

        Form of life = shared practices, agreements, ways of living
        The bedrock that grounds language games
        """
        text_lower = text.lower()
        forms = []

        # Social/communal form of life
        if any(
            word in text_lower
            for word in ["we", "us", "community", "society", "together", "shared"]
        ):
            forms.append("Communal - shared social practices")

        # Individual/solitary form of life
        if any(
            word in text_lower
            for word in ["i", "me", "alone", "myself", "individual", "personal"]
        ):
            forms.append("Individual - personal practices")

        # Scientific/theoretical form of life
        if any(
            word in text_lower
            for word in ["theory", "evidence", "test", "hypothesis", "science"]
        ):
            forms.append("Scientific - theoretical inquiry practices")

        # Practical/everyday form of life
        if any(
            word in text_lower
            for word in ["everyday", "practical", "daily", "ordinary", "common"]
        ):
            forms.append("Everyday - ordinary practical life")

        # Religious/spiritual form of life
        if any(
            word in text_lower
            for word in ["god", "divine", "sacred", "spiritual", "faith", "prayer"]
        ):
            forms.append("Religious - spiritual practices")

        # Artistic/aesthetic form of life
        if any(
            word in text_lower
            for word in ["art", "beauty", "create", "aesthetic", "express"]
        ):
            forms.append("Artistic - creative and aesthetic practices")

        if not forms:
            forms.append("Implicit - form of life not explicitly evident")

        return {
            "forms": forms,
            "primary": forms[0],
            "note": "Forms of life are the shared agreements and practices that ground language",
        }

    def _evaluate_meaning_use(self, text: str) -> Dict[str, Any]:
        """
        Evaluate adherence to "meaning is use" principle.

        Late Wittgenstein: The meaning of a word is its use in the language
        Not reference to objects, but how the word functions in practice
        """
        text_lower = text.lower()

        # Use/function indicators
        use_words = ["use", "function", "practice", "employ", "apply", "how we"]
        has_use = sum(1 for word in use_words if word in text_lower)

        # Reference/essence indicators (opposed to use theory)
        reference_words = [
            "essence",
            "true meaning",
            "really means",
            "definition",
            "refers to",
        ]
        has_reference = sum(1 for word in reference_words if word in text_lower)

        # Context/situation indicators
        context_words = ["context", "situation", "depends", "varies", "different cases"]
        has_context = sum(1 for word in context_words if word in text_lower)

        if has_use >= 1 or has_context >= 1:
            adherence = "Strong Use-Theory"
            description = "Meaning understood in terms of use and context"
            orientation = "Late Wittgenstein"
        elif has_reference >= 1:
            adherence = "Reference Theory"
            description = (
                "Meaning understood as reference or essence - pre-Wittgensteinian"
            )
            orientation = "Traditional"
        else:
            adherence = "Unclear"
            description = "Theory of meaning not clear"
            orientation = "Indeterminate"

        return {
            "adherence": adherence,
            "description": description,
            "orientation": orientation,
            "principle": "The meaning of a word is its use in the language",
        }

    def _check_family_resemblance(self, text: str) -> Dict[str, Any]:
        """
        Check for family resemblance thinking.

        Family resemblance = concepts united by overlapping similarities, not essence
        No single feature common to all instances
        """
        text_lower = text.lower()

        # Family resemblance indicators
        resemblance_words = [
            "similar",
            "resemble",
            "like",
            "overlap",
            "variety",
            "different kinds",
        ]
        has_resemblance = sum(1 for word in resemblance_words if word in text_lower)

        # Essence/definition indicators (opposed to family resemblance)
        essence_words = [
            "essence",
            "common to all",
            "necessary",
            "sufficient",
            "definition",
        ]
        has_essence = sum(1 for word in essence_words if word in text_lower)

        # Boundary/vagueness indicators
        boundary_words = [
            "vague",
            "blurry",
            "unclear boundary",
            "hard to say",
            "borderline",
        ]
        has_boundary = sum(1 for word in boundary_words if word in text_lower)

        if has_resemblance >= 1 or has_boundary >= 1:
            thinking = "Family Resemblance"
            description = (
                "Concepts understood through overlapping similarities, not essence"
            )
            type_thinking = "Wittgensteinian"
        elif has_essence >= 1:
            thinking = "Essentialist"
            description = (
                "Concepts understood through necessary and sufficient conditions"
            )
            type_thinking = "Traditional"
        else:
            thinking = "Unclear"
            description = "Conceptual structure not clear"
            type_thinking = "Indeterminate"

        return {
            "thinking": thinking,
            "description": description,
            "type": type_thinking,
            "principle": "Concepts are united by family resemblance, not common essence",
        }

    def _analyze_private_language(self, text: str) -> Dict[str, Any]:
        """
        Analyze relation to private language argument.

        Wittgenstein argues against purely private language
        Language requires public criteria, shared practices
        """
        text_lower = text.lower()

        # Private/subjective indicators
        private_words = ["only i", "private", "subjective", "my own", "inside", "inner"]
        has_private = sum(1 for word in private_words if word in text_lower)

        # Public/shared indicators
        public_words = [
            "public",
            "shared",
            "we all",
            "objective",
            "observable",
            "criteria",
        ]
        has_public = sum(1 for word in public_words if word in text_lower)

        # Ineffability indicators
        ineffable_words = [
            "cannot express",
            "indescribable",
            "ineffable",
            "beyond words",
        ]
        has_ineffable = sum(1 for word in ineffable_words if word in text_lower)

        if has_private >= 2 or has_ineffable >= 1:
            status = "Private Language Tendency"
            description = "Tendency toward private, incommunicable meaning - Wittgenstein would challenge this"
            issue = "Problematic"
        elif has_public >= 1:
            status = "Public Language"
            description = (
                "Recognition of shared, public criteria - consistent with Wittgenstein"
            )
            issue = "Sound"
        else:
            status = "Unclear"
            description = "Public/private dimension unclear"
            issue = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "issue": issue,
            "principle": "There can be no purely private language - language requires public criteria",
        }

    def _detect_philosophical_confusion(self, text: str) -> Dict[str, Any]:
        """
        Detect philosophical confusion or conceptual muddles.

        Wittgenstein: "Philosophical problems arise when language goes on holiday"
        Philosophy as therapy - dissolving rather than solving problems
        """
        text_lower = text.lower()

        # Philosophical question indicators
        deep_questions = [
            "what is",
            "the nature of",
            "essence of",
            "meaning of life",
            "ultimate",
        ]
        has_deep_questions = sum(1 for phrase in deep_questions if phrase in text_lower)

        # Confusion indicators
        confusion_words = [
            "confused",
            "puzzled",
            "paradox",
            "contradiction",
            "doesn't make sense",
        ]
        has_confusion = sum(1 for phrase in confusion_words if phrase in text_lower)

        # Language misuse indicators
        misuse_words = [
            "category mistake",
            "nonsense",
            "meaningless",
            "abuse of language",
        ]
        has_misuse = sum(1 for phrase in misuse_words if phrase in text_lower)

        # Therapeutic indicators
        therapeutic_words = [
            "dissolve",
            "show the fly the way out",
            "clarify",
            "untangle",
        ]
        has_therapeutic = sum(1 for phrase in therapeutic_words if phrase in text_lower)

        if has_confusion >= 1 or has_deep_questions >= 2:
            detection = "Philosophical Confusion Detected"
            description = "Language on holiday - conceptual muddles need dissolution"
            need = "Therapy needed"
        elif has_therapeutic >= 1:
            detection = "Therapeutic Approach"
            description = "Attempting to dissolve rather than solve"
            need = "Therapy in progress"
        elif has_misuse >= 1:
            detection = "Language Misuse"
            description = "Recognition of linguistic confusion"
            need = "Clarification needed"
        else:
            detection = "No Clear Confusion"
            description = "No obvious philosophical muddles"
            need = "None apparent"

        return {
            "detection": detection,
            "description": description,
            "need": need,
            "principle": "Philosophy should dissolve problems, not solve them - therapy not theory",
        }

    def _check_limits_of_language(self, text: str) -> Dict[str, Any]:
        """
        Check awareness of limits of language.

        Early Wittgenstein: "Whereof one cannot speak, thereof one must be silent"
        "The limits of my language mean the limits of my world"
        """
        text_lower = text.lower()

        # Sayable/unsayable indicators
        unsayable_words = [
            "cannot say",
            "beyond words",
            "ineffable",
            "inexpressible",
            "silence",
        ]
        has_unsayable = sum(1 for word in unsayable_words if word in text_lower)

        # Showing vs saying
        showing_words = ["show", "manifest", "reveal", "display", "evident"]
        saying_words = ["say", "state", "assert", "declare", "express"]
        has_showing = sum(1 for word in showing_words if word in text_lower)
        has_saying = sum(1 for word in saying_words if word in text_lower)

        # Mystical indicators (early Wittgenstein)
        mystical_words = ["mystical", "transcendent", "sublime", "wonder", "awe"]
        has_mystical = sum(1 for word in mystical_words if word in text_lower)

        if has_unsayable >= 1 or has_mystical >= 1:
            awareness = "Aware of Limits"
            description = "Recognition of what cannot be said - early Wittgensteinian"
            attitude = "Tractarian"
        elif has_showing > has_saying:
            awareness = "Showing vs Saying"
            description = "Emphasis on showing rather than saying"
            attitude = "Early Wittgenstein"
        else:
            awareness = "No Clear Limits"
            description = "Limits of language not explicitly addressed"
            attitude = "Unclear"

        return {
            "awareness": awareness,
            "description": description,
            "attitude": attitude,
            "principle": "What can be shown cannot be said - whereof we cannot speak, we must be silent",
        }

    def _determine_period(self, text: str) -> Dict[str, Any]:
        """
        Determine whether text resonates more with early or late Wittgenstein.

        Early: Logical structure, limits of language, picture theory
        Late: Language games, forms of life, use theory
        """
        text_lower = text.lower()

        # Early Wittgenstein indicators
        early_words = [
            "logic",
            "structure",
            "limits",
            "cannot say",
            "essence",
            "picture",
            "fact",
        ]
        early_score = sum(1 for word in early_words if word in text_lower)

        # Late Wittgenstein indicators
        late_words = [
            "use",
            "practice",
            "game",
            "form of life",
            "ordinary",
            "everyday",
            "context",
        ]
        late_score = sum(1 for word in late_words if word in text_lower)

        if late_score > early_score and late_score >= 2:
            period = "Late Wittgenstein"
            work = "Philosophical Investigations"
            description = "Emphasis on language games, use, and forms of life"
        elif early_score > late_score and early_score >= 2:
            period = "Early Wittgenstein"
            work = "Tractatus Logico-Philosophicus"
            description = "Emphasis on logical structure and limits of language"
        elif late_score > 0 or early_score > 0:
            period = "Mixed"
            work = "Both periods"
            description = "Elements of both early and late Wittgenstein"
        else:
            period = "Unclear"
            work = "Neither period clearly evident"
            description = "Wittgensteinian themes not prominent"

        return {
            "period": period,
            "work": work,
            "description": description,
            "note": "Wittgenstein's philosophy changed dramatically between early and late periods",
        }

    def _apply_wittgenstein_to_problem(self, text: str) -> str:
        """Apply Wittgenstein's philosophy proactively to the given problem."""
        t = text.lower()
        is_language_meaning = any(
            w in t
            for w in [
                "language",
                "meaning",
                "word",
                "concept",
                "defin",
                "name",
                "refer",
                "communicat",
                "express",
            ]
        )
        is_philosophy_confusion = any(
            w in t
            for w in [
                "philosoph",
                "confus",
                "paradox",
                "puzzle",
                "problem",
                "bewilder",
                "unanswer",
                "mystery",
                "metaphysic",
            ]
        )
        is_knowledge_certainty = any(
            w in t
            for w in [
                "know",
                "certain",
                "doubt",
                "belief",
                "evidence",
                "foundati",
                "justif",
                "proof",
                "sceptic",
            ]
        )
        is_rule_following = any(
            w in t
            for w in [
                "rule",
                "follow",
                "custom",
                "practice",
                "norm",
                "standard",
                "regulat",
                "agreement",
                "correctness",
            ]
        )
        is_ethics_value = any(
            w in t
            for w in [
                "ethics",
                "moral",
                "value",
                "good",
                "evil",
                "ought",
                "transcend",
                "silence",
                "inexpressible",
            ]
        )
        is_ai_computation = any(
            w in t
            for w in [
                "ai",
                "artificial intelligence",
                "comput",
                "machine",
                "robot",
                "algorithm",
                "conscious",
                "mind",
                "turing",
            ]
        )

        if is_language_meaning:
            return (
                "Wittgenstein's later philosophy dissolves the question 'what does this word mean?' "
                "by replacing it with 'how is this word used?' Meaning is not a mental image, not a "
                "reference to an object, not a Platonic essence — it is use within a language game, "
                "which is itself embedded in a form of life (Lebensform). The private language "
                "argument demonstrates that no genuinely private meaning is possible: for a word to "
                "mean something, there must be criteria for its correct application that can in "
                "principle be checked by others, anchored in shared practices rather than inner "
                "ostension. Family resemblance captures how concepts like 'game' or 'language' hold "
                "together not through a single common essence but through overlapping and criss-crossing "
                "similarities — like the features of a family — with no one feature shared by all. "
                "To understand a word is to know how to go on with it in the relevant practice."
            )
        elif is_philosophy_confusion:
            return (
                "Wittgenstein conceives of philosophy not as a discipline that produces theories or "
                "discoveries but as a therapeutic practice: its goal is to show the fly the way out "
                "of the fly-bottle. Philosophical problems arise when language goes on holiday — when "
                "words are used outside the language games that give them meaning, producing the "
                "characteristic feeling of depth and bafflement that philosophers mistake for profound "
                "questions. The task is not to answer these pseudo-questions but to dissolve them: "
                "to show how the apparent problem arose from grammatical confusion, from assimilating "
                "the grammar of one domain to another. Philosophy leaves everything as it is — it "
                "does not discover new truths but removes the bewitchment that makes us think we need "
                "them. 'What is your aim in philosophy? To shew the fly the way out of the fly-bottle.'"
            )
        elif is_knowledge_certainty:
            return (
                "In 'On Certainty', Wittgenstein argues that the bedrock of our epistemic practices "
                "consists not of beliefs but of hinge propositions — commitments so fundamental that "
                "doubting them would undermine the very practice of doubting itself. These hinges are "
                "not known in the ordinary sense; they are acted upon, lived from. The image is of a "
                "river and its bed: the flowing water of revisable beliefs moves within a bed of "
                "bedrock certainties that themselves can shift — but only very slowly, and only "
                "under pressure from the whole system. Doubt requires a framework of certainty to be "
                "coherent: you cannot doubt everything at once, for doubt presupposes that most things "
                "are not in question. The sceptic's demand for justification from first principles "
                "misunderstands the grammar of knowledge — it looks for a foundation where there is "
                "only a practice."
            )
        elif is_rule_following:
            return (
                "The rule-following paradox — perhaps the deepest problem in Wittgenstein's later "
                "philosophy — shows that any action can be made to accord with any rule under some "
                "interpretation. No rule contains its own application; the rule '+2' does not by "
                "itself determine that '1000, 1002, 1004...' is correct rather than '1000, 1004, "
                "1008...' — the interpretation is always possible, always could go another way. "
                "Yet we do follow rules, reliably and without constant conscious interpretation. "
                "The resolution is that rule-following is a practice grounded in forms of life: "
                "we agree in our reactions, our training, our shared responses — and this "
                "agreement is not agreement in opinions but in form of life. Following a rule is "
                "not a private mental act but a public practice, sustained by community, training, "
                "and the natural reactions that human beings share as the kind of creatures they are."
            )
        elif is_ethics_value:
            return (
                "The Tractatus Logico-Philosophicus draws a sharp boundary between what can be said "
                "and what can only be shown. Ethics and aesthetics are transcendental — they are "
                "conditions of the world, not facts within it, and therefore cannot be stated in "
                "meaningful propositions. 'Whereof one cannot speak, thereof one must be silent': "
                "this is not a dismissal of ethics but a recognition that ethical value inhabits a "
                "different register from empirical description. What shows itself in ethical life — "
                "the weight of obligation, the reality of the good — is not thereby unreal; it is "
                "more real, for Wittgenstein, than anything that can be said. The limits of my "
                "language are the limits of my world; but the world has limits, and those limits "
                "show themselves in the ethical, the aesthetic, and the mystical — what Wittgenstein "
                "calls 'the higher' — even though (or precisely because) it cannot be said."
            )
        elif is_ai_computation:
            return (
                "The beetle-in-a-box thought experiment illuminates the problem of ascribing inner "
                "states to machines: suppose everyone has a box containing a 'beetle' that only they "
                "can see — the word 'beetle' still has a use in our language, but the beetle 'drops "
                "out of the language game' as a thing. If AI systems produce outputs that function "
                "like reports of inner states, this tells us about their linguistic behavior, not "
                "necessarily about inner experience. The Turing test is itself a language game — it "
                "tests whether a machine can participate in human linguistic practices, but participation "
                "in a language game does not settle the question of inner experience, which may be "
                "inexpressible in the relevant sense. Wittgenstein's later philosophy suggests we "
                "should attend to the use of mental-state language rather than assuming it picks out "
                "a private inner object — which means the question of machine consciousness may be "
                "less about hidden states and more about forms of life."
            )
        else:
            return (
                "Wittgenstein's philosophy underwent a radical transformation between the Tractatus "
                "Logico-Philosophicus and the Philosophical Investigations. The early Wittgenstein "
                "sought the logical form underlying all meaningful language, drawing a sharp boundary "
                "between what can be said (empirical facts) and what can only be shown (logic, ethics, "
                "the mystical). The later Wittgenstein abandoned the picture theory of meaning in "
                "favor of meaning-as-use: words acquire meaning through their role in language games, "
                "which are themselves embedded in forms of life — the shared practices and reactions "
                "that constitute the human form of existence. Philosophy, on this view, is therapeutic: "
                "it dissolves problems caused by language going on holiday, shows the fly the way out "
                "of the fly-bottle, and leaves everything as it is — while changing how we see it. "
                "Family resemblance, the private language argument, rule-following, and hinge "
                "propositions are the key analytical tools of this later, therapeutic philosophy."
            )

    def _construct_reasoning(
        self,
        language_games: Dict[str, Any],
        forms_of_life: Dict[str, Any],
        meaning_use: Dict[str, Any],
        confusion: Dict[str, Any],
        period: Dict[str, Any],
    ) -> str:
        """Construct Wittgensteinian language analysis reasoning."""
        primary_game = language_games["primary"]

        reasoning = (
            f"From a Wittgensteinian perspective, the primary language game here is: {primary_game}. "
            f"This is embedded in a {forms_of_life['primary']} form of life. "
            f"Regarding meaning: {meaning_use['description']}. "
        )

        # Add philosophical confusion if present
        if "Confusion" in confusion["detection"]:
            reasoning += f"Philosophical analysis: {confusion['description']}. "

        # Add period indication
        reasoning += (
            f"This resonates with {period['period']}: {period['description']}. "
        )

        # Conclude with Wittgensteinian principle
        reasoning += (
            "Remember: Don't ask for the meaning, ask for the use. "
            "Philosophy is a battle against the bewitchment of our intelligence by means of language."
        )

        return reasoning
