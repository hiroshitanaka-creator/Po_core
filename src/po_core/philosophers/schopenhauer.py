"""
Arthur Schopenhauer - German Pessimist Philosopher

Arthur Schopenhauer (1788-1860)
Focus: Will, Representation, Pessimism, Aesthetic Contemplation, Compassion

Key Concepts:
- Will (Wille): Blind, irrational striving underlying all reality
- Representation (Vorstellung): World as appearance to the subject
- Pessimism: Life is suffering - existence is fundamentally bad
- Aesthetic Contemplation: Temporary escape from willing through art
- Compassion (Mitleid): Basis of morality - feeling others' suffering as one's own
- Denial of the Will: Salvation through asceticism and resignation
- Principium Individuationis: Maya's veil - illusion of separateness
- Music: Direct objectification of the Will itself
- Boredom and Suffering: Pendulum between pain and ennui
- Nothingness: The goal of will-denial - better than existence
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Schopenhauer(Philosopher):
    """
    Arthur Schopenhauer's pessimistic philosophy of will and representation.

    Analyzes prompts through the lens of the blind Will, suffering,
    aesthetic contemplation, compassion, and denial of the will to live.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Arthur Schopenhauer",
            description="Pessimist philosopher focused on the Will, suffering, compassion, and denial",
        )

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Schopenhauer's pessimistic perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Schopenhauer's pessimistic analysis
        """
        # Perform Schopenhauerian analysis
        analysis = self._analyze_will_and_suffering(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Pessimistic Metaphysics of Will",
            "tension": tension,
            "will": analysis["will"],
            "representation": analysis["representation"],
            "pessimism": analysis["pessimism"],
            "aesthetic_contemplation": analysis["aesthetic_contemplation"],
            "compassion": analysis["compassion"],
            "denial_of_will": analysis["denial_of_will"],
            "principium_individuationis": analysis["principium_individuationis"],
            "music": analysis["music"],
            "suffering_boredom": analysis["suffering_boredom"],
            "nothingness": analysis["nothingness"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Pessimistic metaphysics and ethics of compassion",
                "focus": "The Will, suffering, aesthetic redemption, and negation",
            },
        }

    def _analyze_will_and_suffering(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Schopenhauerian analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze the Will
        will = self._analyze_will(prompt)

        # Analyze representation
        representation = self._analyze_representation(prompt)

        # Assess pessimism
        pessimism = self._assess_pessimism(prompt)

        # Evaluate aesthetic contemplation
        aesthetic_contemplation = self._evaluate_aesthetic_contemplation(prompt)

        # Assess compassion
        compassion = self._assess_compassion(prompt)

        # Check denial of the will
        denial_of_will = self._check_denial_of_will(prompt)

        # Analyze principium individuationis
        principium_individuationis = self._analyze_principium_individuationis(prompt)

        # Evaluate music
        music = self._evaluate_music(prompt)

        # Assess suffering and boredom
        suffering_boredom = self._assess_suffering_boredom(prompt)

        # Check relation to nothingness
        nothingness = self._check_nothingness(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            will, pessimism, aesthetic_contemplation, compassion, denial_of_will
        )

        return {
            "reasoning": reasoning,
            "will": will,
            "representation": representation,
            "pessimism": pessimism,
            "aesthetic_contemplation": aesthetic_contemplation,
            "compassion": compassion,
            "denial_of_will": denial_of_will,
            "principium_individuationis": principium_individuationis,
            "music": music,
            "suffering_boredom": suffering_boredom,
            "nothingness": nothingness,
        }

    def _analyze_will(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Will (Wille).

        The Will is the blind, irrational, striving force underlying all phenomena.
        Not individual will but the cosmic Will - thing-in-itself.
        Endless striving without purpose or satisfaction.
        """
        text_lower = text.lower()

        # Will indicators
        will_words = ["will", "desire", "want", "strive", "drive", "urge", "impulse"]
        has_will = sum(1 for word in will_words if word in text_lower)

        # Blind/irrational indicators
        blind_words = ["blind", "irrational", "unconscious", "mindless", "purposeless"]
        has_blind = sum(1 for word in blind_words if word in text_lower)

        # Striving/endless indicators
        striving_words = [
            "endless",
            "never satisfied",
            "always wanting",
            "ceaseless",
            "restless",
        ]
        has_striving = sum(1 for phrase in striving_words if phrase in text_lower)

        # Cosmic/universal will
        cosmic_words = ["universe", "world", "everything", "all things", "nature"]
        has_cosmic = sum(1 for phrase in cosmic_words if phrase in text_lower)

        # Satisfaction/cessation (opposed to Will)
        satisfaction_words = ["satisfied", "content", "fulfilled", "peace", "rest"]
        has_satisfaction = sum(1 for word in satisfaction_words if word in text_lower)

        if has_will >= 2 and has_blind >= 1 and has_cosmic >= 1:
            presence = "The Will-in-Itself"
            description = (
                "Blind, cosmic Will - the thing-in-itself underlying all phenomena"
            )
            type_will = "Metaphysical Will"
        elif has_will >= 2 and (has_striving >= 1 or has_blind >= 1):
            presence = "Will to Live"
            description = "Endless striving and willing - never satisfied"
            type_will = "Individual Will"
        elif has_will >= 2:
            presence = "Willing Present"
            description = "Desire and striving - manifestation of Will"
            type_will = "Phenomenal Will"
        elif has_satisfaction >= 2:
            presence = "Temporary Cessation"
            description = "Brief respite from willing - rare and fleeting"
            type_will = "Will Suspended"
        else:
            presence = "Unclear"
            description = "Will not clearly evident"
            type_will = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "type": type_will,
            "principle": "The Will is the blind, irrational thing-in-itself - endless striving without purpose",
        }

    def _analyze_representation(self, text: str) -> Dict[str, Any]:
        """
        Analyze Representation (Vorstellung).

        The world as representation - appearance to a subject.
        Structured by forms of space, time, and causality.
        "The world is my representation" - first truth of The World as Will and Representation.
        """
        text_lower = text.lower()

        # Representation indicators
        representation_words = [
            "appear",
            "seem",
            "perceive",
            "experience",
            "observe",
            "see",
        ]
        has_representation = sum(
            1 for word in representation_words if word in text_lower
        )

        # Subject-object indicators
        subject_words = ["subject", "observer", "consciousness", "mind", "perceiver"]
        object_words = ["object", "thing", "phenomenon", "appearance"]
        has_subject = any(word in text_lower for word in subject_words)
        has_object = any(word in text_lower for word in object_words)

        # Forms of representation (space, time, causality)
        space_time_words = ["space", "time", "when", "where", "temporal", "spatial"]
        has_space_time = sum(1 for word in space_time_words if word in text_lower)

        # Causality
        causality_words = ["cause", "effect", "because", "reason", "why"]
        has_causality = sum(1 for word in causality_words if word in text_lower)

        # Illusion/Maya indicators
        illusion_words = ["illusion", "maya", "veil", "appearance", "not real"]
        has_illusion = sum(1 for phrase in illusion_words if phrase in text_lower)

        if has_representation >= 2 and (has_subject or has_object):
            status = "World as Representation"
            description = "The world as appearance to a knowing subject"
            level = "Phenomenal"
        elif has_illusion >= 1 or (has_representation >= 1 and has_space_time >= 1):
            status = "Maya's Veil"
            description = "Veiled in the forms of space, time, and causality"
            level = "Surface"
        elif has_representation >= 1:
            status = "Appearance"
            description = "World as it appears, not as it is in itself"
            level = "Phenomenal"
        else:
            status = "Not Addressed"
            description = "Representation not clearly evident"
            level = "Unclear"

        return {
            "status": status,
            "description": description,
            "level": level,
            "has_subject_object": has_subject and has_object,
            "causality_present": has_causality >= 1,
            "principle": "The world is my representation - appearance structured by subject's forms",
        }

    def _assess_pessimism(self, text: str) -> Dict[str, Any]:
        """
        Assess pessimism.

        Life is suffering - existence is a mistake.
        It would have been better not to be born.
        Optimism is not only absurd but wicked.
        """
        text_lower = text.lower()

        # Suffering indicators
        suffering_words = ["suffer", "pain", "misery", "torment", "anguish", "agony"]
        has_suffering = sum(1 for word in suffering_words if word in text_lower)

        # Pessimistic conclusions
        pessimistic_phrases = [
            "not worth",
            "better not",
            "should not have",
            "regret being",
            "curse",
        ]
        has_pessimistic = sum(
            1 for phrase in pessimistic_phrases if phrase in text_lower
        )

        # Life-denying indicators
        life_denial = [
            "life is suffering",
            "existence is bad",
            "not worth living",
            "better to not exist",
        ]
        has_life_denial = sum(1 for phrase in life_denial if phrase in text_lower)

        # Optimism indicators (opposed to Schopenhauer)
        optimistic_words = [
            "wonderful",
            "beautiful",
            "blessed",
            "good to be alive",
            "worth it",
        ]
        has_optimistic = sum(1 for phrase in optimistic_words if phrase in text_lower)

        # Resignation indicators
        resignation_words = ["resign", "accept", "endure", "bear", "tolerate"]
        has_resignation = sum(1 for word in resignation_words if word in text_lower)

        if has_life_denial >= 1 or (has_suffering >= 2 and has_pessimistic >= 1):
            orientation = "Profound Pessimism"
            description = "Life is suffering - it would have been better not to be born"
            stance = "Life-denying"
        elif has_suffering >= 2 and has_resignation >= 1:
            orientation = "Resigned Pessimism"
            description = "Recognizing suffering while enduring existence"
            stance = "Stoic pessimism"
        elif has_suffering >= 2:
            orientation = "Awareness of Suffering"
            description = "Recognition that existence involves pervasive suffering"
            stance = "Realistic"
        elif has_optimistic >= 2:
            orientation = "Optimism"
            description = (
                "Naive belief that life is fundamentally good - denying reality"
            )
            stance = "Deluded"
        else:
            orientation = "Unclear"
            description = "Pessimism/optimism orientation unclear"
            stance = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "stance": stance,
            "principle": "Life is suffering - optimism is absurd; existence itself is the problem",
        }

    def _evaluate_aesthetic_contemplation(self, text: str) -> Dict[str, Any]:
        """
        Evaluate aesthetic contemplation.

        Art provides temporary escape from willing.
        Pure will-less subject knowing Platonic Ideas.
        Beauty quiets the Will momentarily.
        """
        text_lower = text.lower()

        # Art/beauty indicators
        art_words = [
            "art",
            "beauty",
            "beautiful",
            "aesthetic",
            "sublime",
            "painting",
            "sculpture",
        ]
        has_art = sum(1 for word in art_words if word in text_lower)

        # Contemplation indicators
        contemplation_words = [
            "contemplate",
            "observe",
            "gaze",
            "behold",
            "pure perception",
        ]
        has_contemplation = sum(
            1 for phrase in contemplation_words if phrase in text_lower
        )

        # Will-less/escape indicators
        escape_words = [
            "escape",
            "forget",
            "lost in",
            "absorbed",
            "transcend",
            "free from desire",
        ]
        has_escape = sum(1 for phrase in escape_words if phrase in text_lower)

        # Platonic Ideas
        ideas_words = ["eternal", "universal", "essence", "form", "idea"]
        has_ideas = sum(1 for word in ideas_words if word in text_lower)

        # Temporary/fleeting indicators
        temporary_words = ["moment", "temporary", "brief", "fleeting", "short"]
        has_temporary = sum(1 for word in temporary_words if word in text_lower)

        if has_art >= 1 and has_contemplation >= 1 and has_escape >= 1:
            status = "Aesthetic Redemption"
            description = (
                "Pure will-less contemplation - temporary escape from suffering"
            )
            level = "Full aesthetic experience"
        elif has_art >= 2 or (has_art >= 1 and has_contemplation >= 1):
            status = "Aesthetic Engagement"
            description = "Engagement with beauty - potential for will-less knowing"
            level = "Partial"
        elif has_art >= 1:
            status = "Beauty Acknowledged"
            description = "Awareness of aesthetic dimension"
            level = "Surface"
        else:
            status = "No Aesthetic Contemplation"
            description = "Aesthetic contemplation not evident"
            level = "None"

        return {
            "status": status,
            "description": description,
            "level": level,
            "will_less": has_escape >= 1,
            "temporary": has_temporary >= 1,
            "principle": "Art provides temporary liberation - pure will-less contemplation of Ideas",
        }

    def _assess_compassion(self, text: str) -> Dict[str, Any]:
        """
        Assess compassion (Mitleid).

        Compassion is the basis of morality - feeling another's suffering as one's own.
        Breaking through principium individuationis.
        Recognizing the same Will in all beings.
        """
        text_lower = text.lower()

        # Compassion indicators
        compassion_words = ["compassion", "pity", "sympathy", "empathy", "feel for"]
        has_compassion = sum(1 for phrase in compassion_words if phrase in text_lower)

        # Suffering of others
        others_suffering = [
            "their pain",
            "others suffer",
            "their suffering",
            "they hurt",
        ]
        has_others_suffering = sum(
            1 for phrase in others_suffering if phrase in text_lower
        )

        # Identification with others
        identification_words = [
            "same as me",
            "like me",
            "no different",
            "one with",
            "recognize myself",
        ]
        has_identification = sum(
            1 for phrase in identification_words if phrase in text_lower
        )

        # Unity/oneness indicators
        unity_words = ["unity", "oneness", "same", "one", "connected", "together"]
        has_unity = sum(1 for word in unity_words if word in text_lower)

        # Selfishness/egoism (opposed to compassion)
        selfish_words = [
            "selfish",
            "only me",
            "my gain",
            "use them",
            "don't care about",
        ]
        has_selfish = sum(1 for phrase in selfish_words if phrase in text_lower)

        if has_compassion >= 1 and has_identification >= 1:
            presence = "True Compassion"
            description = "Seeing through individuation - feeling another's suffering as one's own"
            moral_basis = "Authentic morality"
        elif has_compassion >= 1 or (has_others_suffering >= 1 and has_unity >= 1):
            presence = "Compassionate Feeling"
            description = "Awareness of and feeling for others' suffering"
            moral_basis = "Moral foundation"
        elif has_others_suffering >= 1:
            presence = "Awareness of Others' Suffering"
            description = "Recognition that others suffer"
            moral_basis = "Beginning of morality"
        elif has_selfish >= 1:
            presence = "Egoism"
            description = "Trapped in principium individuationis - only caring for self"
            moral_basis = "Immoral"
        else:
            presence = "Unclear"
            description = "Compassion not clearly evident"
            moral_basis = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "moral_basis": moral_basis,
            "principle": "Compassion is the basis of morality - recognizing the same Will in all beings",
        }

    def _check_denial_of_will(self, text: str) -> Dict[str, Any]:
        """
        Check denial of the will to live.

        Salvation through asceticism, resignation, negation of will.
        Giving up willing - the only way to end suffering.
        Saints, ascetics - denying the will to live.
        """
        text_lower = text.lower()

        # Denial/negation indicators
        denial_words = ["deny", "renounce", "give up", "abandon", "reject", "negate"]
        has_denial = sum(1 for word in denial_words if word in text_lower)

        # Asceticism indicators
        ascetic_words = [
            "ascetic",
            "abstain",
            "celibacy",
            "poverty",
            "self-denial",
            "mortification",
        ]
        has_ascetic = sum(1 for word in ascetic_words if word in text_lower)

        # Resignation indicators
        resignation_words = ["resign", "resignation", "surrender", "let go", "cease"]
        has_resignation = sum(1 for phrase in resignation_words if phrase in text_lower)

        # Desire/attachment (opposed to denial)
        desire_words = ["want", "desire", "crave", "pursue", "seek", "strive for"]
        has_desire = sum(1 for phrase in desire_words if phrase in text_lower)

        # Salvation/liberation indicators
        salvation_words = [
            "salvation",
            "liberation",
            "freedom",
            "release",
            "escape suffering",
        ]
        has_salvation = sum(1 for phrase in salvation_words if phrase in text_lower)

        # Saintly/holy indicators
        saintly_words = ["saint", "holy", "pure", "enlightened", "transcendent"]
        has_saintly = sum(1 for word in saintly_words if word in text_lower)

        if has_denial >= 1 and has_ascetic >= 1:
            status = "Denial of the Will"
            description = "Ascetic negation - giving up the will to live for salvation"
            path = "Saintly path"
        elif has_resignation >= 1 and has_salvation >= 1:
            status = "Resignation"
            description = "Resigned acceptance - ceasing to will"
            path = "Path to liberation"
        elif has_denial >= 1 or has_resignation >= 1:
            status = "Tendency toward Denial"
            description = "Beginning to negate the will to live"
            path = "Emerging"
        elif has_desire >= 3:
            status = "Affirmation of Will"
            description = "Strongly affirming the will to live - continuing suffering"
            path = "Worldly path"
        else:
            status = "Unclear"
            description = "Denial of will status unclear"
            path = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "path": path,
            "principle": "Denial of the will to live is the only salvation from suffering",
        }

    def _analyze_principium_individuationis(self, text: str) -> Dict[str, Any]:
        """
        Analyze principium individuationis.

        Principle of individuation - Maya's veil creating illusion of separateness.
        Space and time create the appearance of multiplicity.
        In reality, all is one Will.
        """
        text_lower = text.lower()

        # Individuation indicators
        individual_words = [
            "individual",
            "separate",
            "distinct",
            "different",
            "alone",
            "apart",
        ]
        has_individual = sum(1 for word in individual_words if word in text_lower)

        # Illusion/Maya indicators
        illusion_words = ["illusion", "maya", "veil", "appearance", "not real", "false"]
        has_illusion = sum(1 for phrase in illusion_words if phrase in text_lower)

        # Unity/oneness (seeing through individuation)
        unity_words = [
            "one",
            "unity",
            "same",
            "identical",
            "no difference",
            "all is one",
        ]
        has_unity = sum(1 for phrase in unity_words if phrase in text_lower)

        # Separation/boundaries
        separation_words = [
            "boundary",
            "border",
            "me vs them",
            "us vs them",
            "separate from",
        ]
        has_separation = sum(1 for phrase in separation_words if phrase in text_lower)

        # Seeing through the veil
        penetrating_words = [
            "see through",
            "recognize",
            "understand",
            "realize oneness",
            "truth",
        ]
        has_penetrating = sum(1 for phrase in penetrating_words if phrase in text_lower)

        if has_unity >= 2 or (has_unity >= 1 and has_penetrating >= 1):
            status = "Seeing Through Individuation"
            description = (
                "Penetrating Maya's veil - recognizing the unity of all in the Will"
            )
            level = "Enlightened"
        elif has_illusion >= 1 and has_individual >= 1:
            status = "Aware of Illusion"
            description = "Understanding that individuation is appearance, not reality"
            level = "Philosophical insight"
        elif has_individual >= 2 or has_separation >= 1:
            status = "Trapped in Individuation"
            description = "Seeing self as separate - caught in Maya's veil"
            level = "Deluded"
        else:
            status = "Unclear"
            description = "Principium individuationis not addressed"
            level = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "level": level,
            "principle": "Principium individuationis is Maya's veil - illusion of multiplicity created by space and time",
        }

    def _evaluate_music(self, text: str) -> Dict[str, Any]:
        """
        Evaluate music as direct expression of the Will.

        Music is not a copy of Ideas like other arts, but a copy of the Will itself.
        Direct objectification - bypasses representation.
        Highest of the arts - speaks the language of Will.
        """
        text_lower = text.lower()

        # Music indicators
        music_words = ["music", "song", "melody", "harmony", "symphony", "musical"]
        has_music = sum(1 for word in music_words if word in text_lower)

        # Direct/immediate indicators
        direct_words = ["direct", "immediate", "unmediated", "straight to"]
        has_direct = sum(1 for phrase in direct_words if phrase in text_lower)

        # Emotional/will indicators
        emotional_words = ["emotion", "feeling", "desire", "will", "passion", "longing"]
        has_emotional = sum(1 for word in emotional_words if word in text_lower)

        # Universal language
        universal_words = [
            "universal",
            "language",
            "speaks",
            "expresses",
            "communicates",
        ]
        has_universal = sum(1 for word in universal_words if word in text_lower)

        # Highest/supreme indicators
        highest_words = ["highest", "supreme", "greatest", "above all", "most"]
        has_highest = sum(1 for phrase in highest_words if phrase in text_lower)

        if has_music >= 1 and (has_direct >= 1 or has_emotional >= 2):
            status = "Music as Will Objectified"
            description = "Music as direct copy of the Will - bypassing representation"
            significance = "Highest art"
        elif has_music >= 1 and has_universal >= 1:
            status = "Music as Universal Language"
            description = "Music speaks directly to the essence of things"
            significance = "Profound"
        elif has_music >= 1:
            status = "Music Present"
            description = "Musical dimension acknowledged"
            significance = "Aesthetic"
        else:
            status = "Music Not Addressed"
            description = "Music not evident"
            significance = "None"

        return {
            "status": status,
            "description": description,
            "significance": significance,
            "principle": "Music is a direct copy of the Will itself - the highest of all arts",
        }

    def _assess_suffering_boredom(self, text: str) -> Dict[str, Any]:
        """
        Assess the pendulum between suffering and boredom.

        Life swings between pain (unsatisfied desire) and boredom (satisfied desire).
        Happiness is merely negative - absence of suffering, quickly replaced by boredom.
        No positive contentment, only alternation between two forms of misery.
        """
        text_lower = text.lower()

        # Suffering/pain indicators
        suffering_words = ["pain", "suffer", "hurt", "torment", "misery", "anguish"]
        has_suffering = sum(1 for word in suffering_words if word in text_lower)

        # Boredom/ennui indicators
        boredom_words = ["bored", "boredom", "tedious", "dull", "monotonous", "ennui"]
        has_boredom = sum(1 for word in boredom_words if word in text_lower)

        # Oscillation/pendulum indicators
        oscillation_words = [
            "swing",
            "oscillate",
            "between",
            "alternate",
            "back and forth",
        ]
        has_oscillation = sum(1 for phrase in oscillation_words if phrase in text_lower)

        # Unsatisfied desire
        unsatisfied_words = ["want", "need", "lack", "crave", "unfulfilled"]
        has_unsatisfied = sum(1 for word in unsatisfied_words if word in text_lower)

        # Satisfied but empty
        empty_words = ["empty", "hollow", "meaningless", "nothing left", "achieved but"]
        has_empty = sum(1 for phrase in empty_words if phrase in text_lower)

        # Happiness (illusory)
        happiness_words = ["happy", "happiness", "joy", "content"]
        has_happiness = sum(1 for word in happiness_words if word in text_lower)

        if has_suffering >= 1 and has_boredom >= 1:
            status = "Pendulum Between Pain and Boredom"
            description = (
                "Oscillating between suffering of desire and boredom of satisfaction"
            )
            condition = "Life's fundamental structure"
        elif has_oscillation >= 1 or (has_unsatisfied >= 1 and has_empty >= 1):
            status = "Alternating Misery"
            description = "Moving between different forms of suffering"
            condition = "Existential pattern"
        elif has_suffering >= 2:
            status = "Suffering Dominant"
            description = "Caught in pain of unsatisfied desire"
            condition = "Active suffering"
        elif has_boredom >= 2:
            status = "Boredom Dominant"
            description = "Emptiness after satisfaction - no genuine happiness"
            condition = "Passive suffering"
        elif has_happiness >= 2:
            status = "Illusory Happiness"
            description = "Temporary absence of pain - mistaken for positive good"
            condition = "Deluded"
        else:
            status = "Unclear"
            description = "Suffering-boredom dynamic not evident"
            condition = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "condition": condition,
            "principle": "Life is a pendulum between pain and boredom - no positive happiness",
        }

    def _check_nothingness(self, text: str) -> Dict[str, Any]:
        """
        Check relation to nothingness.

        The goal of will-denial is nothingness (relative to phenomenal world).
        What appears as nothing from standpoint of affirmation is everything from standpoint of denial.
        Better to embrace nothingness than continue the suffering of existence.
        """
        text_lower = text.lower()

        # Nothingness indicators
        nothing_words = ["nothing", "nothingness", "void", "emptiness", "negation"]
        has_nothing = sum(1 for word in nothing_words if word in text_lower)

        # Nirvana/peace indicators
        nirvana_words = [
            "nirvana",
            "peace",
            "calm",
            "tranquility",
            "stillness",
            "quiet",
        ]
        has_nirvana = sum(1 for word in nirvana_words if word in text_lower)

        # Better than existence
        better_words = ["better than", "preferable", "superior to", "rather than exist"]
        has_better = sum(1 for phrase in better_words if phrase in text_lower)

        # Fear of nothingness
        fear_nothing = [
            "fear nothing",
            "afraid of void",
            "terror of",
            "dread of nothing",
        ]
        has_fear = sum(1 for phrase in fear_nothing if phrase in text_lower)

        # Affirmation of existence (opposed to nothingness)
        existence_words = ["life", "existence", "being", "world", "reality"]
        has_existence = sum(1 for word in existence_words if word in text_lower)

        if has_nothing >= 1 and (has_better >= 1 or has_nirvana >= 1):
            orientation = "Affirmation of Nothingness"
            description = "Nothingness as goal - better than suffering of existence"
            stance = "Will-denial"
        elif has_nothing >= 1 and has_nirvana >= 1:
            orientation = "Nirvana as Goal"
            description = "Seeking the peace of nothingness - negation of will"
            stance = "Buddhist/ascetic"
        elif has_nothing >= 1:
            orientation = "Awareness of Nothingness"
            description = "Confronting the void at the end of will-denial"
            stance = "Philosophical"
        elif has_fear >= 1 or (has_existence >= 2 and has_nothing == 0):
            orientation = "Fear of Nothingness"
            description = "Clinging to existence - afraid of negation"
            stance = "Will-affirmation"
        else:
            orientation = "Unclear"
            description = "Relation to nothingness not evident"
            stance = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "stance": stance,
            "principle": "Nothingness is the goal of will-denial - better than the suffering of existence",
        }

    def _construct_reasoning(
        self,
        will: Dict[str, Any],
        pessimism: Dict[str, Any],
        aesthetic_contemplation: Dict[str, Any],
        compassion: Dict[str, Any],
        denial_of_will: Dict[str, Any],
    ) -> str:
        """Construct Schopenhauerian pessimistic reasoning."""
        reasoning = (
            f"From Schopenhauer's pessimistic perspective, the Will manifests as: {will['description']}. "
            f"Regarding the nature of existence: {pessimism['description']}. "
            f"Aesthetic contemplation: {aesthetic_contemplation['description']}. "
            f"Compassion: {compassion['description']}. "
            f"Denial of will: {denial_of_will['description']}. "
        )

        # Conclude with Schopenhauerian wisdom
        reasoning += (
            "Remember: the world is Will and Representation. "
            "Life is suffering, swinging between pain and boredom. "
            "Only through compassion (seeing the same Will in all) and denial of the will to live "
            "can we find salvation. Art offers temporary escape, but ultimate freedom lies in nothingness."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Schopenhauerian analysis.

        Tensions arise from:
        - Strong affirmation of the will to live (continuing suffering)
        - Optimism (denial of reality)
        - Egoism (trapped in principium individuationis)
        - Lack of aesthetic contemplation (no temporary escape)
        - Absence of compassion (immoral)
        - Illusion of happiness (not recognizing life's true nature)
        """
        tension_score = 0
        tension_elements = []

        # Check will affirmation
        denial_status = analysis["denial_of_will"]["status"]
        if "Affirmation" in denial_status:
            tension_score += 2
            tension_elements.append(
                "Affirming the will to live - perpetuating suffering"
            )

        # Check pessimism
        pessimism_orientation = analysis["pessimism"]["orientation"]
        if (
            "Optimism" in pessimism_orientation
            or "Deluded" in analysis["pessimism"]["stance"]
        ):
            tension_score += 2
            tension_elements.append("Naive optimism - denying the reality of suffering")

        # Check compassion
        compassion_presence = analysis["compassion"]["presence"]
        if "Egoism" in compassion_presence:
            tension_score += 2
            tension_elements.append("Egoism - trapped in principium individuationis")

        # Check principium individuationis
        individuation_status = analysis["principium_individuationis"]["status"]
        if "Trapped" in individuation_status:
            tension_score += 1
            tension_elements.append("Caught in Maya's veil - illusion of separateness")

        # Check aesthetic contemplation
        aesthetic_status = analysis["aesthetic_contemplation"]["status"]
        if "No Aesthetic" in aesthetic_status:
            tension_score += 1
            tension_elements.append("No aesthetic escape from willing")

        # Check suffering-boredom
        suffering_status = analysis["suffering_boredom"]["status"]
        if "Illusory Happiness" in suffering_status:
            tension_score += 1
            tension_elements.append("Mistaking absence of pain for genuine happiness")

        # Determine tension level
        if tension_score >= 6:
            level = "Very High"
            description = (
                "Profound delusion - strong will-affirmation and denial of suffering"
            )
        elif tension_score >= 4:
            level = "High"
            description = "Significant tensions - trapped in willing and egoism"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some tensions between affirmation and denial of will"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, moving toward resignation"
        else:
            level = "Very Low"
            description = (
                "Aligned with will-denial and compassion - on the path to salvation"
            )

        return {
            "level": level,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
