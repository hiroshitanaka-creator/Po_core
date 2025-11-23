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

from typing import Any, Dict, List, Optional

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
            description="Language philosopher focused on language games, forms of life, and meaning as use"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
            "metadata": {
                "philosopher": self.name,
                "approach": "Language analysis and conceptual clarification",
                "focus": "Language games, meaning as use, and forms of life"
            }
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
        reasoning = self._construct_reasoning(
            language_games, forms_of_life, meaning_use, confusion, period
        )

        return {
            "reasoning": reasoning,
            "language_games": language_games,
            "forms_of_life": forms_of_life,
            "meaning_use": meaning_use,
            "family_resemblance": family_resemblance,
            "private_language": private_language,
            "confusion": confusion,
            "limits": limits,
            "period": period
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
        if any(word in text_lower for word in ["should", "must", "do this", "please", "command"]):
            games_detected.append("Directive - giving orders or requests")

        # Descriptive language game (describing states of affairs)
        if any(word in text_lower for word in ["is", "are", "describe", "looks like", "appears"]):
            games_detected.append("Descriptive - describing how things are")

        # Interrogative language game (asking questions)
        if any(char in text for char in ["?", "what", "how", "why", "when", "where"]):
            games_detected.append("Interrogative - asking questions")

        # Expressive language game (expressing feelings, attitudes)
        if any(word in text_lower for word in ["feel", "hope", "wish", "love", "hate", "believe"]):
            games_detected.append("Expressive - expressing inner states")

        # Performative language game (doing things with words)
        if any(word in text_lower for word in ["promise", "declare", "apologize", "thank", "name"]):
            games_detected.append("Performative - performing actions through words")

        # Evaluative language game (making judgments)
        if any(word in text_lower for word in ["good", "bad", "right", "wrong", "beautiful", "ugly"]):
            games_detected.append("Evaluative - making value judgments")

        # Explanatory language game (giving reasons)
        if any(word in text_lower for word in ["because", "since", "therefore", "reason", "explain"]):
            games_detected.append("Explanatory - giving reasons and explanations")

        if not games_detected:
            games_detected.append("Unclear - language game not readily identifiable")

        return {
            "games": games_detected,
            "count": len(games_detected),
            "primary": games_detected[0],
            "note": "Language games are language embedded in activities and forms of life"
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
        if any(word in text_lower for word in ["we", "us", "community", "society", "together", "shared"]):
            forms.append("Communal - shared social practices")

        # Individual/solitary form of life
        if any(word in text_lower for word in ["i", "me", "alone", "myself", "individual", "personal"]):
            forms.append("Individual - personal practices")

        # Scientific/theoretical form of life
        if any(word in text_lower for word in ["theory", "evidence", "test", "hypothesis", "science"]):
            forms.append("Scientific - theoretical inquiry practices")

        # Practical/everyday form of life
        if any(word in text_lower for word in ["everyday", "practical", "daily", "ordinary", "common"]):
            forms.append("Everyday - ordinary practical life")

        # Religious/spiritual form of life
        if any(word in text_lower for word in ["god", "divine", "sacred", "spiritual", "faith", "prayer"]):
            forms.append("Religious - spiritual practices")

        # Artistic/aesthetic form of life
        if any(word in text_lower for word in ["art", "beauty", "create", "aesthetic", "express"]):
            forms.append("Artistic - creative and aesthetic practices")

        if not forms:
            forms.append("Implicit - form of life not explicitly evident")

        return {
            "forms": forms,
            "primary": forms[0],
            "note": "Forms of life are the shared agreements and practices that ground language"
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
        reference_words = ["essence", "true meaning", "really means", "definition", "refers to"]
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
            description = "Meaning understood as reference or essence - pre-Wittgensteinian"
            orientation = "Traditional"
        else:
            adherence = "Unclear"
            description = "Theory of meaning not clear"
            orientation = "Indeterminate"

        return {
            "adherence": adherence,
            "description": description,
            "orientation": orientation,
            "principle": "The meaning of a word is its use in the language"
        }

    def _check_family_resemblance(self, text: str) -> Dict[str, Any]:
        """
        Check for family resemblance thinking.

        Family resemblance = concepts united by overlapping similarities, not essence
        No single feature common to all instances
        """
        text_lower = text.lower()

        # Family resemblance indicators
        resemblance_words = ["similar", "resemble", "like", "overlap", "variety", "different kinds"]
        has_resemblance = sum(1 for word in resemblance_words if word in text_lower)

        # Essence/definition indicators (opposed to family resemblance)
        essence_words = ["essence", "common to all", "necessary", "sufficient", "definition"]
        has_essence = sum(1 for word in essence_words if word in text_lower)

        # Boundary/vagueness indicators
        boundary_words = ["vague", "blurry", "unclear boundary", "hard to say", "borderline"]
        has_boundary = sum(1 for word in boundary_words if word in text_lower)

        if has_resemblance >= 1 or has_boundary >= 1:
            thinking = "Family Resemblance"
            description = "Concepts understood through overlapping similarities, not essence"
            type_thinking = "Wittgensteinian"
        elif has_essence >= 1:
            thinking = "Essentialist"
            description = "Concepts understood through necessary and sufficient conditions"
            type_thinking = "Traditional"
        else:
            thinking = "Unclear"
            description = "Conceptual structure not clear"
            type_thinking = "Indeterminate"

        return {
            "thinking": thinking,
            "description": description,
            "type": type_thinking,
            "principle": "Concepts are united by family resemblance, not common essence"
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
        public_words = ["public", "shared", "we all", "objective", "observable", "criteria"]
        has_public = sum(1 for word in public_words if word in text_lower)

        # Ineffability indicators
        ineffable_words = ["cannot express", "indescribable", "ineffable", "beyond words"]
        has_ineffable = sum(1 for word in ineffable_words if word in text_lower)

        if has_private >= 2 or has_ineffable >= 1:
            status = "Private Language Tendency"
            description = "Tendency toward private, incommunicable meaning - Wittgenstein would challenge this"
            issue = "Problematic"
        elif has_public >= 1:
            status = "Public Language"
            description = "Recognition of shared, public criteria - consistent with Wittgenstein"
            issue = "Sound"
        else:
            status = "Unclear"
            description = "Public/private dimension unclear"
            issue = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "issue": issue,
            "principle": "There can be no purely private language - language requires public criteria"
        }

    def _detect_philosophical_confusion(self, text: str) -> Dict[str, Any]:
        """
        Detect philosophical confusion or conceptual muddles.

        Wittgenstein: "Philosophical problems arise when language goes on holiday"
        Philosophy as therapy - dissolving rather than solving problems
        """
        text_lower = text.lower()

        # Philosophical question indicators
        deep_questions = ["what is", "the nature of", "essence of", "meaning of life", "ultimate"]
        has_deep_questions = sum(1 for phrase in deep_questions if phrase in text_lower)

        # Confusion indicators
        confusion_words = ["confused", "puzzled", "paradox", "contradiction", "doesn't make sense"]
        has_confusion = sum(1 for phrase in confusion_words if phrase in text_lower)

        # Language misuse indicators
        misuse_words = ["category mistake", "nonsense", "meaningless", "abuse of language"]
        has_misuse = sum(1 for phrase in misuse_words if phrase in text_lower)

        # Therapeutic indicators
        therapeutic_words = ["dissolve", "show the fly the way out", "clarify", "untangle"]
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
            "principle": "Philosophy should dissolve problems, not solve them - therapy not theory"
        }

    def _check_limits_of_language(self, text: str) -> Dict[str, Any]:
        """
        Check awareness of limits of language.

        Early Wittgenstein: "Whereof one cannot speak, thereof one must be silent"
        "The limits of my language mean the limits of my world"
        """
        text_lower = text.lower()

        # Sayable/unsayable indicators
        unsayable_words = ["cannot say", "beyond words", "ineffable", "inexpressible", "silence"]
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
            "principle": "What can be shown cannot be said - whereof we cannot speak, we must be silent"
        }

    def _determine_period(self, text: str) -> Dict[str, Any]:
        """
        Determine whether text resonates more with early or late Wittgenstein.

        Early: Logical structure, limits of language, picture theory
        Late: Language games, forms of life, use theory
        """
        text_lower = text.lower()

        # Early Wittgenstein indicators
        early_words = ["logic", "structure", "limits", "cannot say", "essence", "picture", "fact"]
        early_score = sum(1 for word in early_words if word in text_lower)

        # Late Wittgenstein indicators
        late_words = ["use", "practice", "game", "form of life", "ordinary", "everyday", "context"]
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
            "note": "Wittgenstein's philosophy changed dramatically between early and late periods"
        }

    def _construct_reasoning(
        self,
        language_games: Dict[str, Any],
        forms_of_life: Dict[str, Any],
        meaning_use: Dict[str, Any],
        confusion: Dict[str, Any],
        period: Dict[str, Any]
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
        reasoning += f"This resonates with {period['period']}: {period['description']}. "

        # Conclude with Wittgensteinian principle
        reasoning += (
            "Remember: Don't ask for the meaning, ask for the use. "
            "Philosophy is a battle against the bewitchment of our intelligence by means of language."
        )

        return reasoning
