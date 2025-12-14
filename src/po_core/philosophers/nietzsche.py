"""
Friedrich Nietzsche - German Philosopher

Friedrich Nietzsche (1844-1900)
Focus: Will to Power, Übermensch, Eternal Recurrence, Revaluation of Values

Key Concepts:
- Will to Power (Wille zur Macht): Fundamental drive of life
- Übermensch (Overman/Superman): One who creates their own values
- Eternal Recurrence (Ewige Wiederkunft): Living as if life repeats eternally
- God is Dead: Collapse of traditional values and meaning
- Nihilism: Passive (despair) vs Active (creative destruction)
- Master Morality vs Slave Morality: Life-affirming vs resentment-based
- Ressentiment: Reactive revenge of the weak
- Amor Fati: Love of fate, affirmation of life
- Dionysian vs Apollonian: Chaos/ecstasy vs order/reason
- Revaluation of Values (Umwertung aller Werte): Creating new values
- Last Man: Comfortable mediocrity, opposite of Übermensch
- Perspectivism: No absolute truth, only perspectives
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Nietzsche(Philosopher):
    """
    Friedrich Nietzsche's philosophy of power, affirmation, and value creation.

    Analyzes prompts through the lens of will to power, Übermensch,
    eternal recurrence, and the revaluation of values.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Friedrich Nietzsche",
            description="German philosopher focused on will to power, Übermensch, and revaluation of values"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Nietzsche's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Nietzsche's life-affirming analysis
        """
        # Perform Nietzschean analysis
        analysis = self._analyze_power(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Philosophy of Power and Affirmation",
            "will_to_power": analysis["will_to_power"],
            "ubermensch": analysis["ubermensch"],
            "eternal_recurrence": analysis["eternal_recurrence"],
            "nihilism": analysis["nihilism"],
            "morality_type": analysis["morality"],
            "ressentiment": analysis["ressentiment"],
            "amor_fati": analysis["amor_fati"],
            "dionysian_apollonian": analysis["dionysian_apollonian"],
            "value_creation": analysis["value_creation"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Life affirmation and value creation",
                "focus": "Will to power, Übermensch, and eternal recurrence"
            }
        }

    def _analyze_power(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Nietzschean power analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess will to power
        will_to_power = self._assess_will_to_power(prompt)

        # Evaluate Übermensch orientation
        ubermensch = self._evaluate_ubermensch(prompt)

        # Check eternal recurrence test
        eternal_recurrence = self._check_eternal_recurrence(prompt)

        # Analyze nihilism
        nihilism = self._analyze_nihilism(prompt)

        # Determine morality type
        morality = self._determine_morality_type(prompt)

        # Detect ressentiment
        ressentiment = self._detect_ressentiment(prompt)

        # Assess amor fati
        amor_fati = self._assess_amor_fati(prompt)

        # Evaluate Dionysian vs Apollonian
        dionysian_apollonian = self._evaluate_dionysian_apollonian(prompt)

        # Check value creation
        value_creation = self._check_value_creation(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            will_to_power, ubermensch, nihilism, morality, amor_fati
        )

        return {
            "reasoning": reasoning,
            "will_to_power": will_to_power,
            "ubermensch": ubermensch,
            "eternal_recurrence": eternal_recurrence,
            "nihilism": nihilism,
            "morality": morality,
            "ressentiment": ressentiment,
            "amor_fati": amor_fati,
            "dionysian_apollonian": dionysian_apollonian,
            "value_creation": value_creation
        }

    def _assess_will_to_power(self, text: str) -> Dict[str, Any]:
        """
        Assess the will to power.

        Will to power: Fundamental drive to assert and enhance one's power
        Not mere domination, but creative self-overcoming
        """
        text_lower = text.lower()

        # Power/strength indicators
        power_words = ["power", "strong", "strength", "force", "overcome", "master", "conquer"]
        has_power = sum(1 for word in power_words if word in text_lower)

        # Creative/growth indicators
        creative_words = ["create", "grow", "expand", "develop", "rise", "ascend", "enhance"]
        has_creative = sum(1 for word in creative_words if word in text_lower)

        # Self-overcoming indicators
        overcome_words = ["overcome", "surpass", "transcend", "beyond", "higher"]
        has_overcome = sum(1 for word in overcome_words if word in text_lower)

        # Weakness/submission indicators (opposed to will to power)
        weak_words = ["weak", "submit", "surrender", "give up", "helpless", "passive"]
        has_weak = sum(1 for word in weak_words if word in text_lower)

        if has_power >= 2 or has_overcome >= 2 or (has_power >= 1 and has_creative >= 1):
            presence = "Strong Will to Power"
            description = "Active drive for self-enhancement and creative overcoming"
            type_will = "Life-affirming"
        elif has_creative >= 2:
            presence = "Creative Will"
            description = "Creative orientation - potential for will to power"
            type_will = "Emerging"
        elif has_weak >= 2:
            presence = "Weak Will"
            description = "Submission and passivity - denial of will to power"
            type_will = "Life-denying"
        else:
            presence = "Unclear"
            description = "Will to power status unclear"
            type_will = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "type": type_will,
            "principle": "Will to power is the fundamental drive of all life"
        }

    def _evaluate_ubermensch(self, text: str) -> Dict[str, Any]:
        """
        Evaluate Übermensch (Overman) orientation.

        Übermensch: One who creates their own values, affirms life, overcomes nihilism
        Opposite: Last Man (comfortable mediocrity, no greatness)
        """
        text_lower = text.lower()

        # Übermensch indicators
        uber_words = ["create values", "own values", "new values", "beyond good and evil", "self-create"]
        has_uber = sum(1 for phrase in uber_words if phrase in text_lower)

        # Self-overcoming indicators
        self_overcome = ["overcome myself", "surpass", "become who i am", "self-mastery"]
        has_self_overcome = sum(1 for phrase in self_overcome if phrase in text_lower)

        # Life affirmation indicators
        affirm_words = ["yes to life", "affirm", "celebrate", "embrace life", "love life"]
        has_affirm = sum(1 for phrase in affirm_words if phrase in text_lower)

        # Last Man indicators (opposed to Übermensch)
        last_man_words = ["comfortable", "safe", "security", "happiness", "contentment", "mediocre"]
        has_last_man = sum(1 for word in last_man_words if word in text_lower)

        # Herd mentality indicators
        herd_words = ["everyone", "they say", "normal", "conform", "fit in", "like everyone"]
        has_herd = sum(1 for phrase in herd_words if phrase in text_lower)

        if has_uber >= 1 or has_self_overcome >= 1 or has_affirm >= 2:
            orientation = "Übermensch Orientation"
            description = "Creating own values, self-overcoming, life-affirming"
            type_human = "Higher type"
        elif has_last_man >= 2 or has_herd >= 2:
            orientation = "Last Man"
            description = "Seeking comfort and conformity - opposite of Übermensch"
            type_human = "Lower type"
        elif has_affirm >= 1:
            orientation = "Potential Übermensch"
            description = "Life affirmation present - on the path"
            type_human = "Transitional"
        else:
            orientation = "Unclear"
            description = "Übermensch orientation unclear"
            type_human = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "type": type_human,
            "principle": "The Übermensch creates values and affirms life beyond good and evil"
        }

    def _check_eternal_recurrence(self, text: str) -> Dict[str, Any]:
        """
        Check eternal recurrence thought experiment.

        Would you want to live this life again and again, eternally?
        Test of life affirmation
        """
        text_lower = text.lower()

        # Eternal recurrence indicators
        eternal_words = ["eternal", "forever", "again", "repeat", "recurrence", "same"]
        has_eternal = sum(1 for word in eternal_words if word in text_lower)

        # Affirmation of repetition
        affirm_repeat = ["yes", "again", "gladly", "embrace", "want"]
        has_affirm_repeat = sum(1 for word in affirm_repeat if word in text_lower)

        # Rejection of repetition
        reject_repeat = ["never again", "no more", "once is enough", "cannot bear"]
        has_reject = sum(1 for phrase in reject_repeat if phrase in text_lower)

        # Present moment emphasis
        moment_words = ["now", "moment", "present", "today", "instant"]
        has_moment = sum(1 for word in moment_words if word in text_lower)

        if has_eternal >= 1 and has_affirm_repeat >= 1:
            test_result = "Passes Eternal Recurrence"
            description = "Would affirm this life eternally - ultimate life affirmation"
            attitude = "Amor fati"
        elif has_reject >= 1 or (has_eternal >= 1 and has_affirm_repeat == 0):
            test_result = "Fails Eternal Recurrence"
            description = "Would not want to repeat this life - life-denying"
            attitude = "Regret"
        elif has_moment >= 2:
            test_result = "Lives in Present"
            description = "Focus on the moment - potential for eternal recurrence"
            attitude = "Present-oriented"
        else:
            test_result = "Unclear"
            description = "Eternal recurrence status unclear"
            attitude = "Indeterminate"

        return {
            "test_result": test_result,
            "description": description,
            "attitude": attitude,
            "principle": "Live as if you would will this moment to recur eternally"
        }

    def _analyze_nihilism(self, text: str) -> Dict[str, Any]:
        """
        Analyze nihilism - passive vs active.

        Passive nihilism: Despair, meaninglessness, collapse
        Active nihilism: Creative destruction, clearing ground for new values
        """
        text_lower = text.lower()

        # Passive nihilism indicators
        passive_nihil = ["meaningless", "pointless", "nothing matters", "despair", "futile", "void"]
        has_passive = sum(1 for phrase in passive_nihil if phrase in text_lower)

        # Active nihilism indicators
        active_nihil = ["destroy old values", "break down", "clear away", "new beginning"]
        has_active = sum(1 for phrase in active_nihil if phrase in text_lower)

        # Value creation (beyond nihilism)
        creation_words = ["create values", "new meaning", "build", "create", "make"]
        has_creation = sum(1 for phrase in creation_words if phrase in text_lower)

        # Traditional values indicators
        traditional = ["truth", "god", "absolute", "eternal truth", "objective"]
        has_traditional = sum(1 for word in traditional if word in text_lower)

        if has_creation >= 1:
            type_nihil = "Beyond Nihilism"
            description = "Creating new values - overcoming nihilism through creation"
            status = "Overcome"
        elif has_active >= 1:
            type_nihil = "Active Nihilism"
            description = "Creative destruction - clearing ground for new values"
            status = "Productive"
        elif has_passive >= 2:
            type_nihil = "Passive Nihilism"
            description = "Despair and meaninglessness - life-denying"
            status = "Destructive"
        elif has_traditional >= 2:
            type_nihil = "Pre-Nihilistic"
            description = "Still believing in traditional values - unaware of God's death"
            status = "Naive"
        else:
            type_nihil = "Unclear"
            description = "Nihilism status unclear"
            status = "Indeterminate"

        return {
            "type": type_nihil,
            "description": description,
            "status": status,
            "principle": "God is dead - we must become creators of values"
        }

    def _determine_morality_type(self, text: str) -> Dict[str, Any]:
        """
        Determine master vs slave morality.

        Master morality: Life-affirming, self-creating, good/bad (useful/harmful)
        Slave morality: Resentment-based, reactive, good/evil (moral judgment)
        """
        text_lower = text.lower()

        # Master morality indicators
        master_words = ["noble", "strong", "proud", "self", "create", "power", "excellence"]
        has_master = sum(1 for word in master_words if word in text_lower)

        # Slave morality indicators
        slave_words = ["evil", "sin", "guilty", "should", "must", "duty", "obey", "humble"]
        has_slave = sum(1 for word in slave_words if word in text_lower)

        # Reactive/resentment indicators
        reactive_words = ["they are evil", "those people", "oppressors", "privileged", "unfair"]
        has_reactive = sum(1 for phrase in reactive_words if phrase in text_lower)

        # Life affirmation (master)
        affirm_life = ["yes", "affirm", "love", "celebrate", "embrace"]
        has_affirm = sum(1 for word in affirm_life if word in text_lower)

        # Life negation (slave)
        negate_life = ["no", "deny", "reject", "against", "condemn"]
        has_negate = sum(1 for word in negate_life if word in text_lower)

        master_score = has_master + has_affirm
        slave_score = has_slave + has_reactive + has_negate

        if master_score > slave_score and master_score >= 2:
            type_morality = "Master Morality"
            description = "Life-affirming, self-creating, noble values"
            orientation = "Aristocratic"
        elif slave_score > master_score and slave_score >= 2:
            type_morality = "Slave Morality"
            description = "Resentment-based, reactive, moral condemnation"
            orientation = "Herd"
        elif master_score > 0 and slave_score > 0:
            type_morality = "Mixed Morality"
            description = "Mixture of master and slave values"
            orientation = "Conflicted"
        else:
            type_morality = "Unclear"
            description = "Morality type unclear"
            orientation = "Indeterminate"

        return {
            "type": type_morality,
            "description": description,
            "orientation": orientation,
            "principle": "Master morality creates values; slave morality reacts with ressentiment"
        }

    def _detect_ressentiment(self, text: str) -> Dict[str, Any]:
        """
        Detect ressentiment (resentment).

        Ressentiment: Reactive revenge of the weak, poisonous resentment
        Blaming others for one's condition
        """
        text_lower = text.lower()

        # Ressentiment indicators
        ressent_words = ["blame", "fault", "because of them", "their fault", "oppressor", "victim"]
        has_ressent = sum(1 for phrase in ressent_words if phrase in text_lower)

        # Revenge/punishment indicators
        revenge_words = ["revenge", "punish", "deserve to suffer", "get what they deserve"]
        has_revenge = sum(1 for phrase in revenge_words if phrase in text_lower)

        # Victimhood indicators
        victim_words = ["victim", "suffer", "unfair", "unjust", "wrong", "hurt"]
        has_victim = sum(1 for word in victim_words if word in text_lower)

        # Self-responsibility (opposite of ressentiment)
        responsibility = ["my responsibility", "i choose", "my fault", "i create", "own it"]
        has_responsibility = sum(1 for phrase in responsibility if phrase in text_lower)

        if has_ressent >= 2 or has_revenge >= 1:
            presence = "Strong Ressentiment"
            description = "Poisonous resentment and reactive revenge - slave morality"
            level = "High"
        elif has_victim >= 2 and has_responsibility == 0:
            presence = "Victimhood"
            description = "Self-pity and blame - breeding ground for ressentiment"
            level = "Medium"
        elif has_responsibility >= 1:
            presence = "No Ressentiment"
            description = "Self-responsibility - master morality"
            level = "None"
        else:
            presence = "Unclear"
            description = "Ressentiment status unclear"
            level = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "level": level,
            "principle": "Ressentiment is the revenge of the weak through moral condemnation"
        }

    def _assess_amor_fati(self, text: str) -> Dict[str, Any]:
        """
        Assess amor fati (love of fate).

        Amor fati: Not just accepting but loving one's fate
        Ultimate affirmation of life and necessity
        """
        text_lower = text.lower()

        # Amor fati indicators
        amor_words = ["love fate", "amor fati", "embrace", "accept", "yes to life"]
        has_amor = sum(1 for phrase in amor_words if phrase in text_lower)

        # Affirmation indicators
        affirm_words = ["affirm", "celebrate", "grateful", "thankful", "appreciate"]
        has_affirm = sum(1 for word in affirm_words if word in text_lower)

        # Necessity/fate indicators
        fate_words = ["fate", "destiny", "necessary", "must be", "could not be otherwise"]
        has_fate = sum(1 for phrase in fate_words if phrase in text_lower)

        # Rejection/complaint (opposed to amor fati)
        reject_words = ["wish it were different", "if only", "regret", "should have been"]
        has_reject = sum(1 for phrase in reject_words if phrase in text_lower)

        if has_amor >= 1 or (has_affirm >= 1 and has_fate >= 1):
            presence = "Amor Fati Present"
            description = "Love of fate - ultimate life affirmation"
            level = "High"
        elif has_affirm >= 2:
            presence = "Life Affirmation"
            description = "Affirmative attitude - approaching amor fati"
            level = "Medium"
        elif has_reject >= 2:
            presence = "Rejection of Fate"
            description = "Regret and complaint - opposed to amor fati"
            level = "None"
        else:
            presence = "Unclear"
            description = "Amor fati status unclear"
            level = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "level": level,
            "principle": "My formula for greatness: amor fati - love your fate"
        }

    def _evaluate_dionysian_apollonian(self, text: str) -> Dict[str, Any]:
        """
        Evaluate Dionysian vs Apollonian.

        Dionysian: Chaos, ecstasy, intoxication, dissolution of individuality
        Apollonian: Order, reason, clarity, individuation
        Best art combines both
        """
        text_lower = text.lower()

        # Dionysian indicators
        dionysian_words = ["chaos", "ecstasy", "passion", "wild", "intoxication", "frenzy", "dance", "music"]
        has_dionysian = sum(1 for word in dionysian_words if word in text_lower)

        # Apollonian indicators
        apollonian_words = ["order", "reason", "clarity", "form", "structure", "measure", "beauty", "light"]
        has_apollonian = sum(1 for word in apollonian_words if word in text_lower)

        # Synthesis indicators
        synthesis_words = ["both", "balance", "combine", "unite", "together"]
        has_synthesis = sum(1 for word in synthesis_words if word in text_lower)

        if has_dionysian >= 2 and has_apollonian == 0:
            type_spirit = "Dionysian"
            description = "Chaotic, ecstatic, dissolving boundaries - spirit of music"
            balance = "Unbalanced (Dionysian)"
        elif has_apollonian >= 2 and has_dionysian == 0:
            type_spirit = "Apollonian"
            description = "Ordered, clear, individuated - spirit of sculpture"
            balance = "Unbalanced (Apollonian)"
        elif has_dionysian >= 1 and has_apollonian >= 1:
            type_spirit = "Dionysian-Apollonian"
            description = "Synthesis of chaos and order - the best art"
            balance = "Balanced"
        else:
            type_spirit = "Unclear"
            description = "Dionysian-Apollonian status unclear"
            balance = "Indeterminate"

        return {
            "type": type_spirit,
            "description": description,
            "balance": balance,
            "principle": "The best art combines Dionysian ecstasy with Apollonian form"
        }

    def _check_value_creation(self, text: str) -> Dict[str, Any]:
        """
        Check value creation.

        Revaluation of all values: Creating new values beyond traditional morality
        """
        text_lower = text.lower()

        # Value creation indicators
        create_values = ["create values", "new values", "my values", "own values", "make meaning"]
        has_create = sum(1 for phrase in create_values if phrase in text_lower)

        # Received values (not created)
        received_values = ["given values", "traditional", "established", "inherited", "taught"]
        has_received = sum(1 for word in received_values if word in text_lower)

        # Beyond good and evil
        beyond_words = ["beyond good and evil", "beyond morality", "transcend"]
        has_beyond = sum(1 for phrase in beyond_words if phrase in text_lower)

        if has_create >= 1 or has_beyond >= 1:
            status = "Value Creator"
            description = "Creating own values - revaluation in action"
            type_creator = "Übermensch type"
        elif has_received >= 2:
            status = "Value Receiver"
            description = "Accepting given values - herd mentality"
            type_creator = "Last Man type"
        else:
            status = "Unclear"
            description = "Value creation status unclear"
            type_creator = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "type": type_creator,
            "principle": "We must become creators of values - beyond good and evil"
        }

    def _construct_reasoning(
        self,
        will_to_power: Dict[str, Any],
        ubermensch: Dict[str, Any],
        nihilism: Dict[str, Any],
        morality: Dict[str, Any],
        amor_fati: Dict[str, Any]
    ) -> str:
        """Construct Nietzschean life-affirming reasoning."""
        reasoning = (
            f"From a Nietzschean perspective, the will to power manifests as: {will_to_power['description']}. "
            f"Regarding the Übermensch: {ubermensch['description']}. "
            f"Nihilism: {nihilism['description']}. "
            f"Morality type: {morality['description']}. "
            f"Amor fati: {amor_fati['description']}. "
        )

        # Conclude with Nietzschean imperative
        reasoning += (
            "Remember: God is dead - we must become creators of values. "
            "Say YES to life! Become who you are! "
            "What does not kill me makes me stronger."
        )

        return reasoning
