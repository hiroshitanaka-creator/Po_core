"""
Baruch Spinoza - Dutch Rationalist Philosopher

Baruch (Benedict) de Spinoza (1632-1677)
Focus: Substance Monism, Conatus, Determinism, Intellectual Love of God

Key Concepts:
- Substance Monism: Only one substance exists - God/Nature (Deus sive Natura)
- Attributes and Modes: Infinite attributes (thought, extension), finite modes
- Conatus: The striving of each thing to persevere in its being
- Amor Dei Intellectualis: Intellectual love of God through understanding
- Parallelism: Mind and body as parallel expressions of one substance
- Adequate vs Inadequate Ideas: Clear knowledge vs confused imagination
- Determinism: Everything follows necessarily from God's eternal nature
- Freedom as Understanding Necessity: True freedom through rational understanding
- Affections (Affects): Joy, sadness, desire as primary emotions
- Eternity of Mind: The eternal aspect of the mind sub specie aeternitatis
- Three Kinds of Knowledge: Imagination, Reason, Intuitive Science
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Spinoza(Philosopher):
    """
    Spinoza's rationalist philosophy of substance, necessity, and blessedness.

    Analyzes prompts through the lens of substance monism, conatus, determinism,
    adequate ideas, and the intellectual love of God.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Baruch Spinoza",
            description="Rationalist philosopher focused on substance monism, determinism, and the intellectual love of God",
        )
        self.tradition = "Rationalism / Monism"
        self.key_concepts = [
            "substance monism",
            "conatus",
            "intellectual love of God",
            "determinism",
            "Ethics (geometric method)",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Spinoza's rationalist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Spinoza's philosophical analysis
        """
        # Perform comprehensive Spinozistic analysis
        analysis = self._analyze_spinozistic_framework(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Rationalist Monism / Metaphysical Determinism",
            "tension": tension,
            "substance_monism": analysis["substance_monism"],
            "attributes_modes": analysis["attributes_modes"],
            "conatus": analysis["conatus"],
            "amor_dei_intellectualis": analysis["amor_dei"],
            "parallelism": analysis["parallelism"],
            "adequate_ideas": analysis["adequate_ideas"],
            "determinism": analysis["determinism"],
            "freedom": analysis["freedom"],
            "affects": analysis["affects"],
            "eternity_mind": analysis["eternity_mind"],
            "knowledge_kinds": analysis["knowledge_kinds"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Rationalist metaphysics and ethics",
                "focus": "Substance, necessity, and intellectual love of God",
            },
        }

    def _analyze_spinozistic_framework(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Spinozistic analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Spinozistic dimensions
        substance_monism = self._analyze_substance_monism(prompt)
        attributes_modes = self._analyze_attributes_modes(prompt)
        conatus = self._analyze_conatus(prompt)
        amor_dei = self._analyze_amor_dei_intellectualis(prompt)
        parallelism = self._analyze_parallelism(prompt)
        adequate_ideas = self._analyze_adequate_ideas(prompt)
        determinism = self._analyze_determinism(prompt)
        freedom = self._analyze_freedom_necessity(prompt)
        affects = self._analyze_affects(prompt)
        eternity_mind = self._analyze_eternity_mind(prompt)
        knowledge_kinds = self._analyze_three_kinds_knowledge(prompt)

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            substance_monism, conatus, determinism, adequate_ideas, freedom, amor_dei
        )

        return {
            "reasoning": reasoning,
            "substance_monism": substance_monism,
            "attributes_modes": attributes_modes,
            "conatus": conatus,
            "amor_dei": amor_dei,
            "parallelism": parallelism,
            "adequate_ideas": adequate_ideas,
            "determinism": determinism,
            "freedom": freedom,
            "affects": affects,
            "eternity_mind": eternity_mind,
            "knowledge_kinds": knowledge_kinds,
        }

    def _analyze_substance_monism(self, text: str) -> Dict[str, Any]:
        """
        Analyze substance monism - God/Nature (Deus sive Natura).

        Only one substance exists: God or Nature, the same thing.
        All things are in God and nothing can exist without God.
        """
        text_lower = text.lower()

        # Monism indicators
        monism_words = ["one", "unity", "whole", "all is one", "single", "unified"]
        monism_count = sum(1 for word in monism_words if word in text_lower)

        # God/Nature equivalence
        god_nature_words = ["god", "nature", "divine", "cosmos", "universe", "all"]
        god_nature_count = sum(1 for word in god_nature_words if word in text_lower)

        # Substance language
        substance_words = ["substance", "being", "essence", "reality", "fundamental"]
        substance_count = sum(1 for word in substance_words if word in text_lower)

        # Immanence vs transcendence
        immanence_words = ["within", "immanent", "in all things", "everywhere"]
        transcendence_words = ["beyond", "transcendent", "separate", "outside"]

        has_immanence = any(word in text_lower for word in immanence_words)
        has_transcendence = any(word in text_lower for word in transcendence_words)

        # Pluralism (opposed to monism)
        pluralism_words = [
            "many substances",
            "separate beings",
            "independent",
            "distinct",
        ]
        has_pluralism = any(phrase in text_lower for phrase in pluralism_words)

        if monism_count >= 2 and god_nature_count >= 1 and not has_pluralism:
            orientation = "Substance Monism"
            description = "Recognition of one infinite substance - God or Nature"
            status = "Deus sive Natura"
        elif monism_count >= 2 or substance_count >= 2:
            orientation = "Monistic Tendency"
            description = "Leaning toward unity of being"
            status = "Proto-Spinozistic"
        elif has_pluralism or substance_count == 0:
            orientation = "Substantive Pluralism"
            description = "Multiple independent substances - Cartesian error"
            status = "Pre-Spinozistic"
        else:
            orientation = "Unclear"
            description = "Substance orientation unclear"
            status = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "status": status,
            "immanent": has_immanence,
            "transcendent": has_transcendence,
            "principle": "Whatever is, is in God, and nothing can exist or be conceived without God (Ethics I, P15)",
        }

    def _analyze_attributes_modes(self, text: str) -> Dict[str, Any]:
        """
        Analyze attributes and modes.

        Attributes: What the intellect perceives as constituting the essence of substance
        Modes: Affections of substance, modifications that exist in and through substance
        """
        text_lower = text.lower()

        # Attribute indicators (thought and extension are the two we know)
        thought_words = [
            "thought",
            "thinking",
            "mind",
            "idea",
            "mental",
            "consciousness",
        ]
        extension_words = [
            "extension",
            "body",
            "physical",
            "matter",
            "space",
            "material",
        ]

        has_thought = any(word in text_lower for word in thought_words)
        has_extension = any(word in text_lower for word in extension_words)

        # Mode indicators (finite things)
        mode_words = [
            "finite",
            "particular",
            "individual",
            "modification",
            "thing",
            "being",
        ]
        mode_count = sum(1 for word in mode_words if word in text_lower)

        # Essence vs modification
        essence_words = ["essence", "essential", "fundamental", "constitute"]
        sum(1 for word in essence_words if word in text_lower)

        # Infinite vs finite
        infinite_words = ["infinite", "eternal", "unlimited", "boundless"]
        finite_words = ["finite", "limited", "bounded", "temporal"]

        any(word in text_lower for word in infinite_words)
        has_finite = any(word in text_lower for word in finite_words)

        if has_thought and has_extension:
            recognition = "Both Attributes Recognized"
            description = "Awareness of thought and extension as attributes of God"
            status = "Comprehensive"
        elif has_thought or has_extension:
            recognition = "Single Attribute"
            description = (
                f"Recognition of {'thought' if has_thought else 'extension'} attribute"
            )
            status = "Partial"
        else:
            recognition = "Attributes Not Evident"
            description = "Attributes of substance not addressed"
            status = "Unclear"

        # Mode analysis
        if mode_count >= 2 and has_finite:
            mode_status = "Modes Recognized"
            mode_desc = "Awareness of finite modifications of substance"
        elif mode_count >= 1:
            mode_status = "Mode Awareness"
            mode_desc = "Some recognition of particular things as modifications"
        else:
            mode_status = "Modes Not Addressed"
            mode_desc = "Modal nature of finite things not considered"

        return {
            "attribute_recognition": recognition,
            "description": description,
            "status": status,
            "has_thought_attribute": has_thought,
            "has_extension_attribute": has_extension,
            "mode_status": mode_status,
            "mode_description": mode_desc,
            "principle": "God is infinite substance consisting of infinite attributes; finite modes exist in and through God",
        }

    def _analyze_conatus(self, text: str) -> Dict[str, Any]:
        """
        Analyze conatus - the striving to persevere in being.

        Each thing strives to persevere in its own being.
        This striving is the essence of the thing itself.
        """
        text_lower = text.lower()

        # Striving/perseverance indicators
        conatus_words = [
            "strive",
            "persevere",
            "persist",
            "continue",
            "preserve",
            "maintain",
            "endure",
        ]
        conatus_count = sum(1 for word in conatus_words if word in text_lower)

        # Self-preservation
        preservation_words = [
            "self-preservation",
            "survival",
            "stay alive",
            "keep going",
            "hold on",
        ]
        preservation_count = sum(
            1 for phrase in preservation_words if phrase in text_lower
        )

        # Power/force of existence
        power_words = ["power", "force", "strength", "vigor", "vitality", "energy"]
        power_count = sum(1 for word in power_words if word in text_lower)

        # Essence language
        essence_words = ["essence", "essential", "being", "nature", "core"]
        essence_count = sum(1 for word in essence_words if word in text_lower)

        # Death/destruction (opposed to conatus)
        destruction_words = [
            "destroy",
            "death",
            "annihilate",
            "cease",
            "end",
            "give up",
        ]
        destruction_count = sum(1 for word in destruction_words if word in text_lower)

        total_conatus = conatus_count + preservation_count + power_count

        if total_conatus >= 3 and essence_count >= 1:
            presence = "Strong Conatus"
            description = (
                "Active striving to persevere in being - the very essence of existence"
            )
            intensity = "High"
        elif total_conatus >= 2:
            presence = "Conatus Present"
            description = "Striving for self-preservation evident"
            intensity = "Moderate"
        elif destruction_count >= 2 and total_conatus == 0:
            presence = "Negation of Conatus"
            description = "Self-destruction - against the essence of being"
            intensity = "Opposed"
        else:
            presence = "Conatus Unclear"
            description = "Striving to persevere not clearly evident"
            intensity = "Low"

        return {
            "presence": presence,
            "description": description,
            "intensity": intensity,
            "striving_score": conatus_count,
            "preservation_score": preservation_count,
            "principle": "Each thing, as far as it can by its own power, strives to persevere in its being (Ethics III, P6)",
        }

    def _analyze_amor_dei_intellectualis(self, text: str) -> Dict[str, Any]:
        """
        Analyze intellectual love of God (amor dei intellectualis).

        The mind's intellectual love of God is part of the infinite love
        with which God loves himself.
        Highest form of blessedness.
        """
        text_lower = text.lower()

        # Love language
        love_words = ["love", "devotion", "adore", "cherish"]
        love_count = sum(1 for word in love_words if word in text_lower)

        # Intellectual/understanding
        intellectual_words = [
            "understand",
            "knowledge",
            "comprehend",
            "grasp",
            "intellectual",
            "rational",
        ]
        intellectual_count = sum(1 for word in intellectual_words if word in text_lower)

        # God/divine/nature
        divine_words = ["god", "divine", "nature", "eternal", "infinite"]
        divine_count = sum(1 for word in divine_words if word in text_lower)

        # Blessedness/joy
        blessed_words = [
            "blessed",
            "blessedness",
            "joy",
            "happiness",
            "peace",
            "contentment",
        ]
        blessed_count = sum(1 for word in blessed_words if word in text_lower)

        # Eternity perspective
        eternity_words = ["eternal", "eternity", "timeless", "sub specie aeternitatis"]
        has_eternity = any(phrase in text_lower for phrase in eternity_words)

        # Emotional vs intellectual love
        emotional_words = ["feel", "emotion", "passion", "heart"]
        emotional_count = sum(1 for word in emotional_words if word in text_lower)

        if love_count >= 1 and intellectual_count >= 2 and divine_count >= 1:
            presence = "Amor Dei Intellectualis"
            description = (
                "Intellectual love of God through understanding - highest blessedness"
            )
            level = "Supreme"
        elif intellectual_count >= 2 and divine_count >= 1:
            presence = "Intellectual Understanding"
            description = "Rational comprehension of God/Nature"
            level = "High"
        elif (
            love_count >= 1
            and divine_count >= 1
            and emotional_count > intellectual_count
        ):
            presence = "Emotional Devotion"
            description = "Emotional rather than intellectual love - inadequate idea"
            level = "Confused"
        elif blessed_count >= 1:
            presence = "Approaching Blessedness"
            description = "Some recognition of higher joy"
            level = "Moderate"
        else:
            presence = "Not Evident"
            description = "Intellectual love of God not present"
            level = "Absent"

        return {
            "presence": presence,
            "description": description,
            "level": level,
            "has_eternity_perspective": has_eternity,
            "intellectual_score": intellectual_count,
            "emotional_score": emotional_count,
            "principle": "The mind's intellectual love of God is the very love of God with which God loves himself (Ethics V, P36)",
        }

    def _analyze_parallelism(self, text: str) -> Dict[str, Any]:
        """
        Analyze mind-body parallelism.

        The order and connection of ideas is the same as the order and connection of things.
        Mind and body are not causally related but parallel expressions of one substance.
        """
        text_lower = text.lower()

        # Mind/mental indicators
        mind_words = ["mind", "mental", "thought", "idea", "thinking", "consciousness"]
        mind_count = sum(1 for word in mind_words if word in text_lower)

        # Body/physical indicators
        body_words = ["body", "physical", "material", "corporeal", "bodily"]
        body_count = sum(1 for word in body_words if word in text_lower)

        # Parallel/correlation indicators
        parallel_words = ["parallel", "correspond", "same", "equal", "match", "mirror"]
        parallel_count = sum(1 for word in parallel_words if word in text_lower)

        # Interaction/causation (opposed to parallelism)
        interaction_words = [
            "mind affects body",
            "body affects mind",
            "interact",
            "cause",
        ]
        has_interaction = any(phrase in text_lower for phrase in interaction_words)

        # Unity/identity
        unity_words = ["one thing", "same thing", "identical", "two aspects"]
        has_unity = any(phrase in text_lower for phrase in unity_words)

        if mind_count >= 1 and body_count >= 1:
            if parallel_count >= 1 or has_unity:
                recognition = "Parallelism Recognized"
                description = "Mind and body as parallel expressions of one substance"
                status = "Spinozistic"
            elif has_interaction:
                recognition = "Interaction Model"
                description = "Mind-body interaction - Cartesian dualism"
                status = "Dualist Error"
            else:
                recognition = "Both Mentioned"
                description = "Mind and body addressed but relation unclear"
                status = "Unclear Relation"
        elif mind_count >= 1 or body_count >= 1:
            recognition = "Single Aspect"
            description = (
                f"Only {'mind' if mind_count > body_count else 'body'} considered"
            )
            status = "Incomplete"
        else:
            recognition = "Not Addressed"
            description = "Mind-body relation not considered"
            status = "Absent"

        return {
            "recognition": recognition,
            "description": description,
            "status": status,
            "mind_emphasis": mind_count,
            "body_emphasis": body_count,
            "parallel_indicators": parallel_count,
            "principle": "The order and connection of ideas is the same as the order and connection of things (Ethics II, P7)",
        }

    def _analyze_adequate_ideas(self, text: str) -> Dict[str, Any]:
        """
        Analyze adequate vs inadequate ideas.

        Adequate ideas: Clear, distinct, true knowledge from common notions and essence
        Inadequate ideas: Confused, mutilated knowledge from imagination and sensation
        """
        text_lower = text.lower()

        # Adequate idea indicators
        adequate_words = [
            "clear",
            "distinct",
            "certain",
            "true",
            "understand",
            "comprehend",
            "adequate",
        ]
        adequate_count = sum(1 for word in adequate_words if word in text_lower)

        # Inadequate idea indicators
        inadequate_words = [
            "confused",
            "unclear",
            "vague",
            "uncertain",
            "imagine",
            "seem",
            "appear",
        ]
        inadequate_count = sum(1 for word in inadequate_words if word in text_lower)

        # Knowledge vs opinion
        knowledge_words = ["know", "knowledge", "truth", "certainty", "demonstrate"]
        opinion_words = ["think", "believe", "opinion", "guess", "suppose"]

        knowledge_count = sum(1 for word in knowledge_words if word in text_lower)
        opinion_count = sum(1 for word in opinion_words if word in text_lower)

        # Reason/intellect vs imagination
        reason_words = ["reason", "rational", "logical", "intellect", "deduce"]
        imagination_words = ["imagine", "fantasy", "dream", "sensory", "perceive"]

        reason_count = sum(1 for word in reason_words if word in text_lower)
        imagination_count = sum(1 for word in imagination_words if word in text_lower)

        # Essence/necessity vs contingency
        necessity_words = ["necessary", "must", "essence", "eternal"]
        contingency_words = ["contingent", "accidental", "happen to", "could be"]

        has_necessity = any(word in text_lower for word in necessity_words)
        any(phrase in text_lower for phrase in contingency_words)

        # Calculate adequacy
        adequacy_score = adequate_count + knowledge_count + reason_count
        inadequacy_score = inadequate_count + opinion_count + imagination_count

        if adequacy_score >= 3 and has_necessity:
            idea_type = "Adequate Ideas"
            description = "Clear, distinct knowledge from reason - true understanding"
            epistemic_status = "Scientia"
        elif adequacy_score > inadequacy_score and adequacy_score >= 2:
            idea_type = "Tends toward Adequacy"
            description = "Moving toward clear and distinct ideas"
            epistemic_status = "Improving"
        elif inadequacy_score > adequacy_score or imagination_count >= 2:
            idea_type = "Inadequate Ideas"
            description = "Confused, mutilated knowledge from imagination"
            epistemic_status = "Imaginatio"
        else:
            idea_type = "Mixed"
            description = "Combination of adequate and inadequate ideas"
            epistemic_status = "Transitional"

        return {
            "idea_type": idea_type,
            "description": description,
            "epistemic_status": epistemic_status,
            "adequacy_score": adequacy_score,
            "inadequacy_score": inadequacy_score,
            "has_necessity": has_necessity,
            "principle": "An adequate idea is one which has all the properties of a true idea (Ethics II, Def 4)",
        }

    def _analyze_determinism(self, text: str) -> Dict[str, Any]:
        """
        Analyze determinism.

        Nothing happens by chance - all things follow necessarily from God's nature.
        The will is not free in the libertarian sense.
        """
        text_lower = text.lower()

        # Necessity/determinism indicators
        necessity_words = [
            "necessary",
            "must",
            "determined",
            "causation",
            "cause",
            "follows from",
        ]
        necessity_count = sum(1 for phrase in necessity_words if phrase in text_lower)

        # Everything follows from God's nature
        divine_necessity = [
            "god's nature",
            "divine nature",
            "eternal nature",
            "follows necessarily",
        ]
        has_divine_necessity = any(phrase in text_lower for phrase in divine_necessity)

        # No contingency
        no_chance = ["no chance", "not contingent", "not random", "no accident"]
        any(phrase in text_lower for phrase in no_chance)

        # Libertarian free will (opposed to determinism)
        free_will_words = [
            "free will",
            "could have done otherwise",
            "uncaused choice",
            "libertarian",
        ]
        has_free_will = any(phrase in text_lower for phrase in free_will_words)

        # Randomness/chance (opposed to determinism)
        chance_words = ["random", "chance", "accident", "contingent", "arbitrary"]
        chance_count = sum(1 for word in chance_words if word in text_lower)

        # Causal chain
        causal_words = ["because", "therefore", "thus", "consequently", "effect"]
        causal_count = sum(1 for word in causal_words if word in text_lower)

        if necessity_count >= 2 and causal_count >= 1 and not has_free_will:
            position = "Strict Determinism"
            description = "All things follow necessarily from God's eternal nature"
            status = "Spinozistic"
        elif necessity_count >= 2 or has_divine_necessity:
            position = "Deterministic Tendency"
            description = "Recognition of necessity and causation"
            status = "Proto-deterministic"
        elif has_free_will or chance_count >= 2:
            position = "Indeterminism"
            description = (
                "Belief in contingency or libertarian free will - confused thinking"
            )
            status = "Inadequate"
        else:
            position = "Unclear"
            description = "Determinism status unclear"
            status = "Indeterminate"

        return {
            "position": position,
            "description": description,
            "status": status,
            "necessity_score": necessity_count,
            "causal_chain": causal_count >= 2,
            "rejects_free_will": not has_free_will,
            "principle": "In nature there is nothing contingent; all things are determined from the necessity of the divine nature (Ethics I, P29)",
        }

    def _analyze_freedom_necessity(self, text: str) -> Dict[str, Any]:
        """
        Analyze freedom as understanding necessity.

        True freedom is not uncaused choice but understanding and acting from one's own nature.
        Freedom is knowledge of necessity.
        """
        text_lower = text.lower()

        # Freedom language
        freedom_words = ["free", "freedom", "liberate", "autonomous"]
        freedom_count = sum(1 for word in freedom_words if word in text_lower)

        # Understanding/knowledge
        understanding_words = ["understand", "know", "comprehend", "grasp", "knowledge"]
        understanding_count = sum(
            1 for word in understanding_words if word in text_lower
        )

        # Necessity language
        necessity_words = ["necessary", "necessity", "must", "determined"]
        necessity_count = sum(1 for word in necessity_words if word in text_lower)

        # Acting from own nature
        own_nature = [
            "own nature",
            "essence",
            "from itself",
            "self-caused",
            "autonomous",
        ]
        any(phrase in text_lower for phrase in own_nature)

        # Bondage/slavery (opposed to freedom)
        bondage_words = ["bondage", "slave", "enslaved", "trapped", "passive"]
        bondage_count = sum(1 for word in bondage_words if word in text_lower)

        # Passions/emotions controlling (bondage)
        passion_control = ["controlled by", "overcome by", "slave to", "victim of"]
        has_passion_control = any(phrase in text_lower for phrase in passion_control)

        # Freedom through understanding necessity
        if freedom_count >= 1 and understanding_count >= 2 and necessity_count >= 1:
            freedom_type = "True Freedom"
            description = (
                "Freedom as understanding necessity - acting from adequate knowledge"
            )
            status = "Blessed"
        elif understanding_count >= 2:
            freedom_type = "Path to Freedom"
            description = "Increasing understanding - moving toward freedom"
            status = "Liberation"
        elif bondage_count >= 1 or has_passion_control:
            freedom_type = "Human Bondage"
            description = "Enslaved by passions and inadequate ideas"
            status = "Servitude"
        elif freedom_count >= 1 and understanding_count == 0:
            freedom_type = "Illusory Freedom"
            description = "Confused notion of freedom without understanding"
            status = "Ignorant"
        else:
            freedom_type = "Unclear"
            description = "Freedom status unclear"
            status = "Indeterminate"

        return {
            "freedom_type": freedom_type,
            "description": description,
            "status": status,
            "has_understanding": understanding_count >= 2,
            "recognizes_necessity": necessity_count >= 1,
            "principle": "Freedom is understanding necessity; a free thing acts from its own nature alone (Ethics I, Def 7)",
        }

    def _analyze_affects(self, text: str) -> Dict[str, Any]:
        """
        Analyze affects (affections/emotions).

        Primary affects: Joy (increase in power), Sadness (decrease in power), Desire (conatus)
        Active vs passive affects
        """
        text_lower = text.lower()

        # Joy/increase indicators
        joy_words = [
            "joy",
            "happy",
            "glad",
            "delight",
            "pleasure",
            "increase",
            "enhance",
            "grow",
        ]
        joy_count = sum(1 for word in joy_words if word in text_lower)

        # Sadness/decrease indicators
        sadness_words = [
            "sad",
            "sorrow",
            "pain",
            "suffering",
            "decrease",
            "diminish",
            "reduce",
        ]
        sadness_count = sum(1 for word in sadness_words if word in text_lower)

        # Desire indicators
        desire_words = ["desire", "want", "strive", "seek", "appetite"]
        desire_count = sum(1 for word in desire_words if word in text_lower)

        # Active affects (from adequate ideas)
        active_words = ["active", "create", "produce", "generate", "understand"]
        active_count = sum(1 for word in active_words if word in text_lower)

        # Passive affects (from external causes)
        passive_words = ["passive", "受", "affected by", "caused by", "victim", "react"]
        passive_count = sum(1 for phrase in passive_words if phrase in text_lower)

        # Power language
        power_words = ["power", "potency", "capacity", "ability", "strength"]
        sum(1 for word in power_words if word in text_lower)

        # Determine dominant affect
        dominant_affect = "None"
        if joy_count > sadness_count and joy_count >= 2:
            dominant_affect = "Joy"
            affect_desc = "Increase in power of acting - movement toward perfection"
        elif sadness_count > joy_count and sadness_count >= 2:
            dominant_affect = "Sadness"
            affect_desc = "Decrease in power of acting - movement away from perfection"
        elif desire_count >= 2:
            dominant_affect = "Desire"
            affect_desc = "Conatus made conscious - striving for being"
        else:
            affect_desc = "Affects not clearly evident"

        # Active vs passive
        if active_count > passive_count and active_count >= 2:
            affect_type = "Active Affects"
            type_desc = "Affects that follow from adequate ideas - true virtue"
        elif passive_count > active_count or passive_count >= 2:
            affect_type = "Passive Affects"
            type_desc = "Affects from external causes - bondage to passion"
        else:
            affect_type = "Mixed"
            type_desc = "Combination of active and passive affects"

        return {
            "dominant_affect": dominant_affect,
            "affect_description": affect_desc,
            "affect_type": affect_type,
            "type_description": type_desc,
            "joy_score": joy_count,
            "sadness_score": sadness_count,
            "desire_score": desire_count,
            "active_score": active_count,
            "passive_score": passive_count,
            "principle": "Joy is the transition to greater perfection; sadness to lesser perfection (Ethics III, P11)",
        }

    def _analyze_eternity_mind(self, text: str) -> Dict[str, Any]:
        """
        Analyze eternity of mind.

        The mind conceives things under a species of eternity (sub specie aeternitatis).
        Part of the mind is eternal - the intellectual love of God.
        """
        text_lower = text.lower()

        # Eternity indicators
        eternity_words = ["eternal", "eternity", "timeless", "everlasting", "permanent"]
        eternity_count = sum(1 for word in eternity_words if word in text_lower)

        # Sub specie aeternitatis
        eternal_perspective = [
            "sub specie aeternitatis",
            "under eternity",
            "from eternity",
            "eternal perspective",
        ]
        has_eternal_perspective = any(
            phrase in text_lower for phrase in eternal_perspective
        )

        # Mind/intellect
        mind_words = ["mind", "intellect", "understanding", "consciousness"]
        mind_count = sum(1 for word in mind_words if word in text_lower)

        # Temporal vs eternal
        temporal_words = [
            "time",
            "temporal",
            "temporary",
            "transient",
            "passing",
            "moment",
        ]
        temporal_count = sum(1 for word in temporal_words if word in text_lower)

        # Immortality (but not personal survival)
        immortal_words = ["immortal", "deathless", "imperishable"]
        any(word in text_lower for word in immortal_words)

        # Personal survival (confused idea)
        personal_survival = ["afterlife", "heaven", "reincarnation", "life after death"]
        has_personal_survival = any(
            phrase in text_lower for phrase in personal_survival
        )

        if eternity_count >= 2 and mind_count >= 1 and not has_personal_survival:
            recognition = "Eternity of Mind"
            description = "Mind participates in eternity through adequate ideas"
            status = "Sub specie aeternitatis"
        elif has_eternal_perspective:
            recognition = "Eternal Perspective"
            description = "Viewing things from the perspective of eternity"
            status = "Philosophical"
        elif temporal_count > eternity_count:
            recognition = "Temporal Perspective"
            description = "Focused on temporal, transient existence"
            status = "Finite"
        elif has_personal_survival:
            recognition = "Personal Immortality"
            description = "Confused notion of personal survival - inadequate idea"
            status = "Superstitious"
        else:
            recognition = "Unclear"
            description = "Eternity of mind not addressed"
            status = "Indeterminate"

        return {
            "recognition": recognition,
            "description": description,
            "status": status,
            "eternity_score": eternity_count,
            "has_eternal_perspective": has_eternal_perspective,
            "temporal_focus": temporal_count > eternity_count,
            "principle": "The mind is eternal insofar as it conceives things under a species of eternity (Ethics V, P31)",
        }

    def _analyze_three_kinds_knowledge(self, text: str) -> Dict[str, Any]:
        """
        Analyze three kinds of knowledge.

        First kind: Imagination (imaginatio) - vague experience, hearsay, random experience
        Second kind: Reason (ratio) - common notions, adequate ideas of properties
        Third kind: Intuitive Science (scientia intuitiva) - knowledge from essence, highest knowledge
        """
        text_lower = text.lower()

        # First kind: Imagination
        imagination_words = [
            "imagine",
            "seem",
            "appear",
            "sensory",
            "experience",
            "perceive",
        ]
        imagination_count = sum(1 for word in imagination_words if word in text_lower)

        # Hearsay/opinion
        hearsay_words = ["heard", "told", "they say", "people say", "opinion", "belief"]
        hearsay_count = sum(1 for phrase in hearsay_words if phrase in text_lower)

        # Second kind: Reason
        reason_words = [
            "reason",
            "rational",
            "deduce",
            "logical",
            "common notion",
            "property",
        ]
        reason_count = sum(1 for phrase in reason_words if phrase in text_lower)

        # Demonstration/proof
        demonstration_words = ["demonstrate", "prove", "proof", "theorem", "derive"]
        demonstration_count = sum(
            1 for word in demonstration_words if word in text_lower
        )

        # Third kind: Intuitive knowledge
        intuition_words = [
            "intuition",
            "intuitive",
            "immediate",
            "direct knowledge",
            "essence",
        ]
        intuition_count = sum(1 for phrase in intuition_words if phrase in text_lower)

        # Essence/nature understanding
        essence_words = ["essence", "nature", "being", "what it is"]
        essence_count = sum(1 for phrase in essence_words if phrase in text_lower)

        # Determine dominant kind
        first_kind_score = imagination_count + hearsay_count
        second_kind_score = reason_count + demonstration_count
        third_kind_score = intuition_count + (
            essence_count if essence_count >= 2 else 0
        )

        if third_kind_score >= 2:
            dominant_kind = "Third Kind (Scientia Intuitiva)"
            description = "Intuitive knowledge from essence - highest blessedness"
            epistemic_level = "Supreme"
        elif second_kind_score >= 2:
            dominant_kind = "Second Kind (Ratio)"
            description = "Rational knowledge from common notions - adequate ideas"
            epistemic_level = "High"
        elif first_kind_score >= 2:
            dominant_kind = "First Kind (Imaginatio)"
            description = (
                "Knowledge from vague experience and hearsay - inadequate ideas"
            )
            epistemic_level = "Low"
        else:
            dominant_kind = "Unclear"
            description = "Kind of knowledge not clearly evident"
            epistemic_level = "Indeterminate"

        return {
            "dominant_kind": dominant_kind,
            "description": description,
            "epistemic_level": epistemic_level,
            "first_kind_score": first_kind_score,
            "second_kind_score": second_kind_score,
            "third_kind_score": third_kind_score,
            "principle": "Three kinds of knowledge: imagination, reason, and intuitive science (Ethics II, P40)",
        }

    def _construct_reasoning(
        self,
        substance_monism: Dict[str, Any],
        conatus: Dict[str, Any],
        determinism: Dict[str, Any],
        adequate_ideas: Dict[str, Any],
        freedom: Dict[str, Any],
        amor_dei: Dict[str, Any],
    ) -> str:
        """Construct comprehensive Spinozistic philosophical reasoning."""
        reasoning = (
            "From a Spinozistic perspective, we must understand all things through the one infinite substance - "
            "God or Nature (Deus sive Natura). "
        )

        # Substance monism
        reasoning += f"Substance: {substance_monism['description']}. "

        # Conatus
        reasoning += f"Conatus: {conatus['description']}. "

        # Determinism
        reasoning += f"Determinism: {determinism['description']}. "

        # Adequate ideas
        reasoning += f"Knowledge: {adequate_ideas['description']}. "

        # Freedom
        reasoning += f"Freedom: {freedom['description']}. "

        # Amor dei intellectualis
        if amor_dei["presence"] != "Not Evident":
            reasoning += f"Intellectual love: {amor_dei['description']}. "

        # Concluding Spinozistic wisdom
        reasoning += (
            "Remember: All things are in God and nothing can exist without God. "
            "Freedom is understanding necessity. "
            "Blessedness is not the reward of virtue, but virtue itself. "
            "We feel and know that we are eternal."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Spinozistic analysis.

        Tensions arise from:
        - Substantive pluralism (multiple substances)
        - Negation of conatus (self-destruction)
        - Inadequate ideas (confused knowledge)
        - Belief in libertarian free will
        - Human bondage (slavery to passions)
        - Passive affects dominating
        - Temporal perspective only
        - First kind of knowledge (imagination)
        """
        tension_score = 0
        tension_elements = []

        # Check substance monism
        substance_status = analysis["substance_monism"]["status"]
        if substance_status == "Pre-Spinozistic":
            tension_score += 2
            tension_elements.append("Substantive pluralism - denies the unity of being")

        # Check conatus
        conatus_presence = analysis["conatus"]["presence"]
        if "Negation" in conatus_presence:
            tension_score += 2
            tension_elements.append("Negation of conatus - self-destruction")

        # Check adequate ideas
        idea_type = analysis["adequate_ideas"]["idea_type"]
        if idea_type == "Inadequate Ideas":
            tension_score += 2
            tension_elements.append("Inadequate ideas - confused knowledge")
        elif idea_type == "Mixed":
            tension_score += 1
            tension_elements.append("Mixed adequate and inadequate ideas")

        # Check determinism
        determinism_position = analysis["determinism"]["position"]
        if determinism_position == "Indeterminism":
            tension_score += 2
            tension_elements.append(
                "Belief in contingency or free will - confused thinking"
            )

        # Check freedom
        freedom_type = analysis["freedom"]["freedom_type"]
        if freedom_type == "Human Bondage":
            tension_score += 2
            tension_elements.append("Human bondage - enslaved by passions")
        elif freedom_type == "Illusory Freedom":
            tension_score += 1
            tension_elements.append("Illusory notion of freedom")

        # Check affects
        affect_type = analysis["affects"]["affect_type"]
        if affect_type == "Passive Affects":
            tension_score += 1
            tension_elements.append("Passive affects - determined by external causes")

        dominant_affect = analysis["affects"]["dominant_affect"]
        if dominant_affect == "Sadness":
            tension_score += 1
            tension_elements.append("Sadness - decrease in power of acting")

        # Check knowledge kind
        knowledge_kind = analysis["knowledge_kinds"]["dominant_kind"]
        if "First Kind" in knowledge_kind:
            tension_score += 1
            tension_elements.append("First kind of knowledge - imagination and hearsay")

        # Check eternity of mind
        eternity_status = analysis["eternity_mind"]["status"]
        if eternity_status == "Superstitious":
            tension_score += 1
            tension_elements.append("Superstitious belief in personal immortality")

        # Determine tension level
        if tension_score >= 8:
            level = "Very High"
            description = (
                "Severe confusion - mired in inadequate ideas and human bondage"
            )
        elif tension_score >= 6:
            level = "High"
            description = (
                "Significant tensions - enslaved by passions and confused thinking"
            )
        elif tension_score >= 4:
            level = "Moderate"
            description = "Some tensions between adequate and inadequate ideas"
        elif tension_score >= 2:
            level = "Low"
            description = "Minor tensions, moving toward adequate knowledge"
        else:
            level = "Very Low"
            description = (
                "Aligned with reason and adequate ideas - approaching blessedness"
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
