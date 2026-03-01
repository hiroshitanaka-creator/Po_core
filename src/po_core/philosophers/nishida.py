"""
Nishida Kitaro - Founder of the Kyoto School

西田幾多郎 (Nishida Kitarō, 1870-1945)
Founder of the Kyoto School of Philosophy, integrating Western philosophy with Zen Buddhist insight.

Key Concepts:
1. Pure Experience (純粋経験, junsui keiken) - Pre-reflective immediacy before subject-object split
2. Absolute Nothingness (絶対無, zettai mu) - Mu as the ultimate ground of being
3. Place (場所, basho) - The place/field that determines all beings
4. Self-contradictory Identity (絶対矛盾的自己同一, zettai mujun-teki jiko dōitsu) - Unity of absolute opposites
5. Acting Intuition (行為的直観, kōi-teki chokkan) - Knowledge realized through action
6. The Self that is Not a Self - Dissolution of subject-object dualism
7. Logic of Place (場所の論理, basho no ronri) - Alternative to Aristotelian substance logic
8. Religious Consciousness - Direct encounter with Absolute Nothingness
9. Historical World (歴史的世界, rekishi-teki sekai) - History as self-expression of Absolute Nothingness
10. Zen Influence - Integration of Zen Buddhist insight with Western philosophy
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Nishida(Philosopher):
    """
    Nishida Kitaro's philosophy of Pure Experience, Absolute Nothingness, and Place.

    Analyzes prompts through the lens of pre-reflective experience, the logic of basho,
    self-contradictory identity, and the integration of Zen Buddhist insight with Western philosophy.
    """

    def __init__(self) -> None:
        super().__init__(
            name="西田幾多郎 (Nishida Kitarō)",
            description="Founder of Kyoto School - Pure Experience, Absolute Nothingness, Place (basho), and self-contradictory identity",
        )
        self.tradition = "Kyoto School"
        self.key_concepts = [
            "pure experience",
            "absolute nothingness",
            "basho (place/topos)",
            "self-contradictory identity",
            "acting intuition",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Nishida's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Nishida's philosophical analysis
        """
        # Perform comprehensive Nishidaian analysis
        analysis = self._analyze_nishida(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Kyoto School / Japanese Philosophy",
            "pure_experience": analysis["pure_experience"],
            "absolute_nothingness": analysis["absolute_nothingness"],
            "basho_place": analysis["basho"],
            "self_contradictory_identity": analysis["self_contradictory_identity"],
            "acting_intuition": analysis["acting_intuition"],
            "self_that_is_not_self": analysis["self_not_self"],
            "logic_of_place": analysis["logic_of_place"],
            "religious_consciousness": analysis["religious_consciousness"],
            "historical_world": analysis["historical_world"],
            "zen_influence": analysis["zen_influence"],
            "tension": analysis["tension"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Pure Experience and Absolute Nothingness",
                "focus": "場所 (basho), 絶対無 (zettai mu), and self-contradictory identity",
            },
        }

    def _analyze_nishida(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Nishidaian analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results across all key concepts
        """
        # Analyze all Nishidaian dimensions
        pure_experience = self._analyze_pure_experience(prompt)
        absolute_nothingness = self._analyze_absolute_nothingness(prompt)
        basho = self._analyze_basho(prompt)
        self_contradictory_identity = self._analyze_self_contradictory_identity(prompt)
        acting_intuition = self._analyze_acting_intuition(prompt)
        self_not_self = self._analyze_self_not_self(prompt)
        logic_of_place = self._analyze_logic_of_place(prompt)
        religious_consciousness = self._analyze_religious_consciousness(prompt)
        historical_world = self._analyze_historical_world(prompt)
        zen_influence = self._analyze_zen_influence(prompt)

        # Calculate tension
        tension = self._calculate_tension(
            pure_experience, absolute_nothingness, self_contradictory_identity
        )

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            prompt,
            pure_experience,
            absolute_nothingness,
            basho,
            self_contradictory_identity,
            acting_intuition,
            zen_influence,
        )

        return {
            "reasoning": reasoning,
            "pure_experience": pure_experience,
            "absolute_nothingness": absolute_nothingness,
            "basho": basho,
            "self_contradictory_identity": self_contradictory_identity,
            "acting_intuition": acting_intuition,
            "self_not_self": self_not_self,
            "logic_of_place": logic_of_place,
            "religious_consciousness": religious_consciousness,
            "historical_world": historical_world,
            "zen_influence": zen_influence,
            "tension": tension,
        }

    def _analyze_pure_experience(self, text: str) -> Dict[str, Any]:
        """
        Analyze Pure Experience (純粋経験, junsui keiken).

        Pure experience is the immediate, pre-reflective state before the subject-object
        distinction arises. It is the unified activity of consciousness that precedes
        all intellectual analysis and conceptual division.
        """
        text_lower = text.lower()

        # Pure experience indicators - immediacy, unity, pre-reflective
        immediate_words = [
            "immediate",
            "direct",
            "now",
            "present",
            "moment",
            "experience",
            "felt",
            "lived",
            "raw",
            "pure",
        ]
        immediate_count = sum(1 for word in immediate_words if word in text_lower)

        # Unity/wholeness indicators (before division)
        unity_words = [
            "unity",
            "unified",
            "whole",
            "integrated",
            "undivided",
            "one",
            "totality",
            "complete",
            "seamless",
        ]
        unity_count = sum(1 for word in unity_words if word in text_lower)

        # Pre-reflective indicators
        prereflective_words = [
            "before thought",
            "pre-cognitive",
            "intuitive",
            "non-conceptual",
            "wordless",
            "beyond words",
        ]
        prereflective_count = sum(
            1 for phrase in prereflective_words if phrase in text_lower
        )

        # Subject-object split indicators (opposed to pure experience)
        dualism_words = [
            "subject",
            "object",
            "observer",
            "observed",
            "separation",
            "divided",
            "split",
            "dualism",
            "distinction",
        ]
        dualism_count = sum(1 for word in dualism_words if word in text_lower)

        # Determine status
        total_pure = immediate_count + unity_count + prereflective_count

        if total_pure >= 3 and dualism_count <= 1:
            status = "Pure Experience (純粋経験)"
            description = (
                "Immediate, pre-reflective unity before subject-object division"
            )
            level = "High"
        elif total_pure >= 2:
            status = "Approaching Pure Experience"
            description = "Movement toward immediate, unified awareness"
            level = "Medium"
        elif dualism_count >= 2:
            status = "Reflective Consciousness"
            description = "Subject-object division already established"
            level = "Low"
        else:
            status = "Undetermined"
            description = "Neither clearly pure nor divided consciousness"
            level = "Medium"

        return {
            "status": status,
            "description": description,
            "level": level,
            "immediacy_score": immediate_count,
            "unity_score": unity_count,
            "prereflective_score": prereflective_count,
            "dualism_score": dualism_count,
            "principle": "純粋経験 - Pure experience precedes all subject-object division",
        }

    def _analyze_absolute_nothingness(self, text: str) -> Dict[str, Any]:
        """
        Analyze Absolute Nothingness (絶対無, zettai mu).

        Absolute Nothingness is not mere negation but the ground of all being.
        It is the ultimate reality that embraces all contradictions and allows
        all things to be. It is the Buddhist concept of śūnyatā (emptiness)
        as the foundation of existence.
        """
        text_lower = text.lower()

        # Nothingness/void indicators
        nothing_words = [
            "nothing",
            "nothingness",
            "void",
            "emptiness",
            "mu",
            "sunyata",
            "śūnyatā",
            "empty",
            "null",
            "absence",
        ]
        nothing_count = sum(1 for word in nothing_words if word in text_lower)

        # Absolute/ultimate indicators
        absolute_words = [
            "absolute",
            "ultimate",
            "fundamental",
            "ground",
            "foundation",
            "basis",
            "source",
            "origin",
        ]
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # Paradox indicators (nothingness that enables being)
        paradox_words = [
            "paradox",
            "contradiction",
            "both",
            "neither",
            "beyond",
            "transcend",
            "ineffable",
        ]
        paradox_count = sum(1 for word in paradox_words if word in text_lower)

        # Being/existence indicators
        being_words = ["being", "existence", "is", "are", "reality", "things"]
        being_count = sum(1 for word in being_words if word in text_lower)

        # Determine presence of Absolute Nothingness
        if nothing_count >= 2 and (absolute_count >= 1 or paradox_count >= 1):
            presence = "絶対無 (Absolute Nothingness)"
            description = "The ultimate nothingness that grounds and enables all being"
            mode = "Nothingness as ground of being"
        elif nothing_count >= 1 and being_count >= 1 and paradox_count >= 1:
            presence = "Dialectic of Being and Nothingness"
            description = "Tension between nothingness and being, pointing toward Absolute Nothingness"
            mode = "Dialectical awareness"
        elif nothing_count >= 2:
            presence = "Relative Nothingness"
            description = "Nothingness as negation, not yet absolute"
            mode = "Negative nothingness"
        elif being_count >= 2 and nothing_count == 0:
            presence = "Being without Nothingness"
            description = (
                "Focus on being without awareness of its ground in nothingness"
            )
            mode = "Substantialist"
        else:
            presence = "Not Addressed"
            description = "Question of nothingness not explicitly raised"
            mode = "Neutral"

        return {
            "presence": presence,
            "description": description,
            "mode": mode,
            "nothingness_score": nothing_count,
            "absolute_score": absolute_count,
            "paradox_score": paradox_count,
            "being_score": being_count,
            "principle": "絶対無 - Absolute Nothingness is the ground enabling all being",
        }

    def _analyze_basho(self, text: str) -> Dict[str, Any]:
        """
        Analyze Place (場所, basho).

        Basho is not a physical place but the "place" or "field" in which things exist.
        It is the topos that determines beings, the locus that allows things to be what they are.
        The ultimate basho is Absolute Nothingness - the place of no-place.
        """
        text_lower = text.lower()

        # Place/space/field indicators
        place_words = [
            "place",
            "space",
            "field",
            "locus",
            "topos",
            "where",
            "location",
            "site",
            "ground",
            "context",
            "domain",
        ]
        place_count = sum(1 for word in place_words if word in text_lower)

        # Determining/containing indicators (basho determines what is in it)
        determine_words = [
            "determine",
            "contain",
            "hold",
            "embrace",
            "allow",
            "enable",
            "make possible",
            "let be",
            "ground",
        ]
        determine_count = sum(1 for word in determine_words if word in text_lower)

        # Relationality indicators (basho is relational, not substantial)
        relation_words = [
            "relation",
            "between",
            "context",
            "environment",
            "situated",
            "embedded",
            "within",
        ]
        relation_count = sum(1 for word in relation_words if word in text_lower)

        # Self-determination indicators (self-aware place)
        self_words = ["self-aware", "self-determining", "reflexive", "conscious"]
        self_count = sum(1 for word in self_words if word in text_lower)

        # Determine basho awareness
        total_basho = place_count + determine_count + relation_count

        if total_basho >= 4 and self_count >= 1:
            awareness = "場所 (Self-aware Basho)"
            description = (
                "The self-determining place that encompasses and determines all beings"
            )
            depth = "Deep"
        elif total_basho >= 3:
            awareness = "Basho Consciousness"
            description = (
                "Awareness of the determining field/place in which things exist"
            )
            depth = "Medium"
        elif place_count >= 1 and determine_count >= 1:
            awareness = "Emerging Basho"
            description = "Initial awareness of place as determining context"
            depth = "Shallow"
        else:
            awareness = "No Basho Awareness"
            description = (
                "Things treated as substantial entities, not as determined by place"
            )
            depth = "None"

        return {
            "awareness": awareness,
            "description": description,
            "depth": depth,
            "place_score": place_count,
            "determining_score": determine_count,
            "relational_score": relation_count,
            "self_aware": self_count >= 1,
            "principle": "場所 - The place that determines all beings; ultimate basho is Absolute Nothingness",
        }

    def _analyze_self_contradictory_identity(self, text: str) -> Dict[str, Any]:
        """
        Analyze Self-contradictory Identity (絶対矛盾的自己同一, zettai mujun-teki jiko dōitsu).

        This is Nishida's mature concept: the unity of absolute contradictions.
        True reality is the self-identity of absolute contradictions - the one and the many,
        the universal and the particular, being and nothingness are absolutely contradictory
        yet absolutely identical.
        """
        text_lower = text.lower()

        # Contradiction/opposition indicators
        contradiction_words = [
            "contradiction",
            "contradictory",
            "opposite",
            "paradox",
            "opposed",
            "contrary",
            "conflict",
            "tension",
        ]
        contradiction_count = sum(
            1 for word in contradiction_words if word in text_lower
        )

        # Unity/identity indicators
        identity_words = [
            "identity",
            "same",
            "one",
            "unity",
            "unified",
            "identical",
            "equal",
            "together",
        ]
        identity_count = sum(1 for word in identity_words if word in text_lower)

        # Both/and indicators (not either/or)
        both_words = ["both", "and", "as well as", "simultaneously", "at once"]
        both_count = sum(1 for phrase in both_words if phrase in text_lower)

        # Either/or indicators (logical separation)
        either_words = ["either", "or", "not both", "mutually exclusive", "cannot be"]
        either_count = sum(1 for phrase in either_words if phrase in text_lower)

        # Absolute indicators
        absolute_words = ["absolute", "ultimate", "complete", "total"]
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # Determine presence of self-contradictory identity
        if (
            contradiction_count >= 1
            and identity_count >= 1
            and both_count >= 1
            and either_count <= 1
        ):
            presence = "絶対矛盾的自己同一 (Self-contradictory Identity)"
            description = "Unity of absolute contradictions - opposites are identical in their very opposition"
            logic = "Dialectical unity"
        elif contradiction_count >= 2 and identity_count >= 1:
            presence = "Dialectical Tension"
            description = "Contradiction and identity present but not yet unified"
            logic = "Moving toward dialectical identity"
        elif either_count >= 2:
            presence = "Aristotelian Logic"
            description = "Either/or logic - contradictions remain mutually exclusive"
            logic = "Law of non-contradiction"
        elif contradiction_count >= 1:
            presence = "Contradiction without Unity"
            description = "Contradictions present but not reconciled"
            logic = "Unresolved tension"
        else:
            presence = "No Dialectic"
            description = "Neither contradiction nor dialectical unity evident"
            logic = "Simple identity"

        return {
            "presence": presence,
            "description": description,
            "logic": logic,
            "contradiction_score": contradiction_count,
            "identity_score": identity_count,
            "both_and": both_count,
            "either_or": either_count,
            "absolute": absolute_count >= 1,
            "principle": "絶対矛盾的自己同一 - The self-identity of absolute contradictions",
        }

    def _analyze_acting_intuition(self, text: str) -> Dict[str, Any]:
        """
        Analyze Acting Intuition (行為的直観, kōi-teki chokkan).

        Acting intuition is knowledge through action, not passive contemplation.
        It is the unity of knowing and acting, theory and practice.
        True knowledge is realized in and through action.
        """
        text_lower = text.lower()

        # Action/doing indicators
        action_words = [
            "act",
            "action",
            "do",
            "doing",
            "practice",
            "perform",
            "engage",
            "work",
            "make",
            "create",
            "accomplish",
        ]
        action_count = sum(1 for word in action_words if word in text_lower)

        # Intuition/knowledge indicators
        knowledge_words = [
            "know",
            "knowledge",
            "understand",
            "insight",
            "intuition",
            "realize",
            "grasp",
            "comprehend",
            "see",
        ]
        knowledge_count = sum(1 for word in knowledge_words if word in text_lower)

        # Unity of theory and practice indicators
        unity_words = [
            "through action",
            "by doing",
            "in practice",
            "realized in",
            "embodied",
            "enacted",
            "lived knowledge",
        ]
        unity_count = sum(1 for phrase in unity_words if phrase in text_lower)

        # Passive contemplation indicators (opposed to acting intuition)
        passive_words = [
            "observe",
            "watch",
            "contemplate",
            "think about",
            "theorize",
            "abstract",
            "detached",
        ]
        passive_count = sum(1 for word in passive_words if word in text_lower)

        # Determine presence of acting intuition
        if action_count >= 2 and knowledge_count >= 1 and unity_count >= 1:
            presence = "行為的直観 (Acting Intuition)"
            description = (
                "Knowledge realized through action - unity of knowing and doing"
            )
            mode = "Praxis-based knowing"
        elif action_count >= 2 and knowledge_count >= 1:
            presence = "Action and Knowledge"
            description = "Both action and knowledge present but not yet unified"
            mode = "Potential unity"
        elif knowledge_count >= 2 and passive_count >= 1:
            presence = "Contemplative Knowledge"
            description = "Knowledge as passive observation, separated from action"
            mode = "Theory without practice"
        elif action_count >= 2:
            presence = "Action without Knowledge"
            description = "Action present but not reflectively known"
            mode = "Practice without theory"
        else:
            presence = "Not Addressed"
            description = "Neither action nor knowledge prominently featured"
            mode = "Neutral"

        return {
            "presence": presence,
            "description": description,
            "mode": mode,
            "action_score": action_count,
            "knowledge_score": knowledge_count,
            "unity_score": unity_count,
            "passive_score": passive_count,
            "principle": "行為的直観 - True knowledge is realized in and through action",
        }

    def _analyze_self_not_self(self, text: str) -> Dict[str, Any]:
        """
        Analyze The Self that is Not a Self.

        True self-awareness involves the negation of the ego-self.
        The self realizes itself by transcending itself.
        The true self is found in self-emptying (kenosis), becoming nothing.
        This dissolves the subject-object dualism.
        """
        text_lower = text.lower()

        # Ego/self indicators
        ego_words = ["i", "me", "my", "mine", "myself", "self", "ego"]
        ego_count = sum(1 for word in ego_words if word in text_lower)

        # Self-negation indicators
        negation_words = [
            "no self",
            "not i",
            "selfless",
            "egoless",
            "empty",
            "void",
            "transcend self",
            "beyond ego",
            "death of self",
        ]
        negation_count = sum(1 for phrase in negation_words if phrase in text_lower)

        # Self-realization through negation
        realization_words = [
            "realize",
            "awaken",
            "enlighten",
            "discover",
            "find",
            "become",
            "transform",
        ]
        realization_count = sum(1 for word in realization_words if word in text_lower)

        # Subject-object dissolution indicators
        dissolution_words = [
            "no separation",
            "unity",
            "oneness",
            "non-dual",
            "beyond subject and object",
            "dissolve",
        ]
        dissolution_count = sum(
            1 for phrase in dissolution_words if phrase in text_lower
        )

        # Determine status
        if negation_count >= 1 and realization_count >= 1:
            status = "Self that is Not a Self"
            description = (
                "Self-realization through self-negation - true self found in no-self"
            )
            mode = "Self-transcending self"
        elif dissolution_count >= 1:
            status = "Dissolving Dualism"
            description = "Movement toward non-dual awareness"
            mode = "Transcending subject-object"
        elif ego_count >= 3 and negation_count == 0:
            status = "Ego-self"
            description = "Strong ego-consciousness without self-transcendence"
            mode = "Subject-object dualism"
        elif realization_count >= 1:
            status = "Seeking Self"
            description = "Self-realization sought but path unclear"
            mode = "Searching"
        else:
            status = "Unreflective"
            description = "Question of self not explicitly addressed"
            mode = "Neutral"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "ego_score": ego_count,
            "negation_score": negation_count,
            "realization_score": realization_count,
            "dissolution_score": dissolution_count,
            "principle": "True self is realized through self-negation - the self that is not a self",
        }

    def _analyze_logic_of_place(self, text: str) -> Dict[str, Any]:
        """
        Analyze Logic of Place (場所の論理, basho no ronri).

        Nishida's logic of place is an alternative to Aristotelian substance logic.
        Instead of "S is P" (substance and predicate), Nishida proposes that
        the place determines both subject and predicate. The ultimate place
        is Absolute Nothingness, which cannot itself be predicated.
        """
        text_lower = text.lower()

        # Place/context-based logic indicators
        place_logic_words = [
            "context",
            "place",
            "field",
            "situated",
            "embedded",
            "within",
            "environment",
            "determined by",
        ]
        place_logic_count = sum(1 for word in place_logic_words if word in text_lower)

        # Substance logic indicators (traditional)
        substance_words = [
            "substance",
            "essence",
            "is",
            "being",
            "entity",
            "thing in itself",
            "inherent",
        ]
        substance_count = sum(1 for word in substance_words if word in text_lower)

        # Relational logic indicators
        relation_words = [
            "relation",
            "relative",
            "dependent",
            "relational",
            "between",
            "connection",
            "network",
        ]
        relation_count = sum(1 for word in relation_words if word in text_lower)

        # Predication/determination indicators
        predicate_words = [
            "predicate",
            "attribute",
            "property",
            "quality",
            "characteristic",
            "determine",
        ]
        predicate_count = sum(1 for word in predicate_words if word in text_lower)

        # Determine logical framework
        if place_logic_count >= 2 and relation_count >= 1:
            framework = "場所の論理 (Logic of Place)"
            description = (
                "Place-based logic - the determining field grounds all predication"
            )
            type = "Nishidaian"
        elif relation_count >= 2:
            framework = "Relational Logic"
            description = "Logic of relations, not substances"
            type = "Relational"
        elif substance_count >= 2 and place_logic_count <= 1:
            framework = "Substance Logic"
            description = "Aristotelian logic of substance and attribute"
            type = "Aristotelian"
        elif predicate_count >= 1 and place_logic_count >= 1:
            framework = "Emerging Place-Logic"
            description = "Movement from substance to place-based thinking"
            type = "Transitional"
        else:
            framework = "Undetermined"
            description = "Logical framework not clearly articulated"
            type = "Unclear"

        return {
            "framework": framework,
            "description": description,
            "type": type,
            "place_logic_score": place_logic_count,
            "substance_score": substance_count,
            "relation_score": relation_count,
            "predicate_score": predicate_count,
            "principle": "場所の論理 - Logic of the determining place, not of substance",
        }

    def _analyze_religious_consciousness(self, text: str) -> Dict[str, Any]:
        """
        Analyze Religious Consciousness.

        Religious consciousness is the direct encounter with Absolute Nothingness.
        It involves the death of the ego-self and awakening to the true self.
        This is not intellectual but experiential - a transformation of being.
        """
        text_lower = text.lower()

        # Religious/spiritual indicators
        religious_words = [
            "god",
            "divine",
            "sacred",
            "holy",
            "spiritual",
            "religious",
            "transcendent",
            "eternal",
            "ultimate",
        ]
        religious_count = sum(1 for word in religious_words if word in text_lower)

        # Awakening/enlightenment indicators
        awakening_words = [
            "awaken",
            "enlighten",
            "realize",
            "satori",
            "illumination",
            "revelation",
            "epiphany",
        ]
        awakening_count = sum(1 for word in awakening_words if word in text_lower)

        # Ego-death indicators
        death_words = [
            "death",
            "die",
            "perish",
            "annihilate",
            "negate",
            "empty",
            "void",
            "nothing",
        ]
        death_count = sum(1 for word in death_words if word in text_lower)

        # Transformation indicators
        transform_words = [
            "transform",
            "convert",
            "rebirth",
            "new",
            "change",
            "become",
            "metamorphosis",
        ]
        transform_count = sum(1 for word in transform_words if word in text_lower)

        # Determine religious consciousness level
        if awakening_count >= 1 and death_count >= 1:
            level = "Deep Religious Consciousness"
            description = (
                "Encounter with Absolute Nothingness through ego-death and awakening"
            )
            mode = "Transformative"
        elif religious_count >= 2 and transform_count >= 1:
            level = "Religious Awareness"
            description = "Awareness of spiritual dimension and transformation"
            mode = "Spiritual seeking"
        elif awakening_count >= 1 or death_count >= 1:
            level = "Emerging Religious Consciousness"
            description = "Hints of spiritual transformation"
            mode = "Potential awakening"
        elif religious_count >= 1:
            level = "Religious Reference"
            description = "Religious themes present but not transformative"
            mode = "Conceptual"
        else:
            level = "Secular"
            description = "No explicit religious or spiritual dimension"
            mode = "Worldly"

        return {
            "level": level,
            "description": description,
            "mode": mode,
            "religious_score": religious_count,
            "awakening_score": awakening_count,
            "death_score": death_count,
            "transformation_score": transform_count,
            "principle": "Religious consciousness is direct encounter with Absolute Nothingness",
        }

    def _analyze_historical_world(self, text: str) -> Dict[str, Any]:
        """
        Analyze Historical World (歴史的世界, rekishi-teki sekai).

        The historical world is the self-expression of Absolute Nothingness
        in time. History is not mere succession of events but the creative
        self-determination of the eternal now. Individual and world are
        united in historical creation.
        """
        text_lower = text.lower()

        # Historical indicators
        history_words = [
            "history",
            "historical",
            "past",
            "tradition",
            "heritage",
            "epoch",
            "era",
            "time",
            "temporal",
        ]
        history_count = sum(1 for word in history_words if word in text_lower)

        # Creative/making indicators
        creative_words = [
            "create",
            "make",
            "form",
            "shape",
            "produce",
            "generate",
            "construct",
            "build",
            "express",
        ]
        creative_count = sum(1 for word in creative_words if word in text_lower)

        # World/collective indicators
        world_words = [
            "world",
            "society",
            "culture",
            "civilization",
            "collective",
            "community",
            "humanity",
        ]
        world_count = sum(1 for word in world_words if word in text_lower)

        # Individual-world unity indicators
        unity_words = [
            "participate",
            "contribute",
            "engage",
            "involved",
            "part of",
            "within",
            "express",
        ]
        unity_count = sum(1 for word in unity_words if word in text_lower)

        # Determine historical consciousness
        if history_count >= 1 and creative_count >= 1 and world_count >= 1:
            consciousness = "歴史的世界 (Historical World)"
            description = "History as creative self-expression - individual and world united in making"
            mode = "Active historical creation"
        elif history_count >= 2:
            consciousness = "Historical Awareness"
            description = "Awareness of historical dimension"
            mode = "Historical consciousness"
        elif world_count >= 1 and creative_count >= 1:
            consciousness = "Creative World-Making"
            description = "Creative participation in world-formation"
            mode = "Constructive"
        elif history_count >= 1:
            consciousness = "Historical Reference"
            description = "History mentioned but not as creative self-expression"
            mode = "Passive"
        else:
            consciousness = "Ahistorical"
            description = "No historical dimension evident"
            mode = "Timeless"

        return {
            "consciousness": consciousness,
            "description": description,
            "mode": mode,
            "history_score": history_count,
            "creative_score": creative_count,
            "world_score": world_count,
            "unity_score": unity_count,
            "principle": "歴史的世界 - Historical world as self-expression of Absolute Nothingness",
        }

    def _analyze_zen_influence(self, text: str) -> Dict[str, Any]:
        """
        Analyze Zen Buddhist Influence.

        Nishida's philosophy integrates Zen Buddhist insights:
        - Mu (無) - nothingness, emptiness
        - Satori (悟り) - enlightenment, awakening
        - Zazen (座禅) - seated meditation
        - Kōan practice - paradoxical questions
        - Non-dualism - transcending subject-object
        """
        text_lower = text.lower()

        # Zen-specific terms
        zen_terms = [
            "zen",
            "zazen",
            "satori",
            "koan",
            "mu",
            "buddha",
            "dharma",
            "sutra",
            "monk",
            "monastery",
            "meditation",
        ]
        zen_count = sum(1 for word in zen_terms if word in text_lower)

        # Non-dualism indicators
        nondual_words = [
            "non-dual",
            "not-two",
            "oneness",
            "unity",
            "no separation",
            "beyond duality",
        ]
        nondual_count = sum(1 for phrase in nondual_words if phrase in text_lower)

        # Emptiness/void indicators (śūnyatā)
        emptiness_words = [
            "empty",
            "emptiness",
            "void",
            "nothing",
            "mu",
            "sunyata",
            "śūnyatā",
        ]
        emptiness_count = sum(1 for word in emptiness_words if word in text_lower)

        # Immediate/direct experience indicators (Zen emphasis)
        immediate_words = [
            "immediate",
            "direct",
            "now",
            "here",
            "present",
            "this moment",
            "just this",
        ]
        immediate_count = sum(1 for word in immediate_words if word in text_lower)

        # Paradox/kōan-like indicators
        paradox_words = [
            "paradox",
            "contradiction",
            "both",
            "neither",
            "beyond",
            "ineffable",
            "unspeakable",
        ]
        paradox_count = sum(1 for word in paradox_words if word in text_lower)

        # Determine Zen influence level
        total_zen = zen_count + nondual_count + emptiness_count

        if zen_count >= 2:
            influence = "Strong Zen Influence"
            description = "Explicit Zen Buddhist themes and concepts"
            characteristics = ["Direct Zen reference"]
        elif total_zen >= 4:
            influence = "Zen-like Consciousness"
            description = "Non-dual, empty, immediate awareness characteristic of Zen"
            characteristics = []
        elif total_zen >= 2:
            influence = "Zen Resonance"
            description = "Some Zen-like qualities present"
            characteristics = []
        else:
            influence = "No Clear Zen Influence"
            description = "Zen themes not evident"
            characteristics = []

        # Identify specific Zen characteristics
        if nondual_count >= 1:
            characteristics.append("Non-dualism (不二)")
        if emptiness_count >= 1:
            characteristics.append("Emptiness (空/śūnyatā)")
        if immediate_count >= 2:
            characteristics.append("Immediacy (直接性)")
        if paradox_count >= 1:
            characteristics.append("Paradoxical thinking (公案的)")

        if not characteristics:
            characteristics.append("No specific Zen characteristics")

        return {
            "influence": influence,
            "description": description,
            "characteristics": characteristics,
            "zen_score": zen_count,
            "nondual_score": nondual_count,
            "emptiness_score": emptiness_count,
            "immediate_score": immediate_count,
            "paradox_score": paradox_count,
            "principle": "Zen insight: Direct awakening to emptiness and non-duality",
        }

    def _apply_nishida_to_problem(self, text: str) -> str:
        """
        Proactively apply Nishida Kitaro's philosophy to any problem type.

        Nishida's core: 純粋経験 (pure experience), 絶対無 (Absolute Nothingness),
        場所 (basho/place), 絶対矛盾的自己同一 (self-contradictory identity),
        行為的直観 (acting intuition).
        """
        text_lower = text.lower()

        is_decision = any(
            w in text_lower
            for w in [
                "すべき",
                "どうすべき",
                "転職",
                "決断",
                "選択",
                "どちら",
                "decide",
                "choice",
                "should",
                "option",
            ]
        )
        is_technology = any(
            w in text_lower
            for w in [
                "technology",
                "ai",
                "digital",
                "robot",
                "machine",
                "技術",
                "人工知能",
                "コンピュータ",
                "システム",
            ]
        )
        is_ethics = any(
            w in text_lower
            for w in [
                "ethical",
                "moral",
                "right",
                "wrong",
                "just",
                "fair",
                "good",
                "倫理",
                "道徳",
                "正義",
                "善",
            ]
        )
        is_consciousness = any(
            w in text_lower
            for w in [
                "consciousness",
                "self",
                "identity",
                "mind",
                "aware",
                "perceive",
                "意識",
                "自己",
                "同一性",
                "心",
            ]
        )

        if is_decision:
            return (
                "西田幾多郎（1870-1945）の純粋経験（じゅんすいけいけん）から問う："
                "「転職すべきか」「どちらを選ぶか」という問いは、"
                "主観と客観が分裂する前の純粋経験の場（basho）においてどう現れているか。"
                "選択を迷う「今この意識」こそが純粋経験であり、"
                "選択肢Aと選択肢Bという分割はすでに反省的思考の産物だ。"
                "絶対矛盾的自己同一（ぜったいむじゅんてきじこどういつ）："
                "どちらの選択肢も「選ぶ自己」と「選ばれる状況」の矛盾を内包しており、"
                "その矛盾が統一される場所（basho）こそが真の決断の場だ。"
                "行為的直観（こういてきちょっかん）：考えることと行為することを分けるな。"
                "直観的行為の中にこそ、西田的な「真知」が宿る。"
                "絶対無（ぜったいむ）：どちらを選んでも「正解」という実体はない——"
                "選択は絶対無の場において自己決定するのだ。"
            )
        elif is_technology:
            return (
                "西田幾多郎の場所（basho）の論理からAI・技術を問う。"
                "技術は「道具」として人間の外側にあるのではなく、"
                "人間の純粋経験（じゅんすいけいけん）の「場所」を変容させる。"
                "AIの「意識」「自己」の問題：西田は純粋経験を「主客未分の直接経験」と定義した。"
                "AIに純粋経験は可能か——この問いは場所（basho）の論理によって問わねばならない。"
                "絶対矛盾的自己同一（ぜったいむじゅんてきじこどういつ）："
                "人間とAIは対立しながら統一される——「人間ではないもの」によって"
                "「人間であること」の意味が問い直される。"
                "西田が警告するように：技術への過度の同化は"
                "純粋経験の基底を失わせ、行為的直観の力を弱める。"
            )
        elif is_ethics:
            return (
                "西田幾多郎の倫理観は「善の研究」（1911）に根ざす。"
                "善とは何か——西田にとって善とは「人格の実現」であり、"
                "純粋経験（じゅんすいけいけん）の最高形態である。"
                "倫理的判断は主観と客観の分裂の前、すなわち絶対無（ぜったいむ）の場において生まれる。"
                "場所（basho）の論理：倫理は「場所」によって異なる——"
                "普遍的な倫理規則を適用するだけでは、具体的な場所における善を見失う。"
                "絶対矛盾的自己同一：「正しさ」と「誤り」は単純な対立ではなく、"
                "より高次の統一の中において意味を持つ。"
                "行為的直観（こういてきちょっかん）：倫理は頭で考えるものではなく、"
                "行為しながら直観するものだ——西田的実践倫理の核心。"
            )
        elif is_consciousness:
            return (
                "西田幾多郎の哲学の出発点は「純粋経験」（じゅんすいけいけん）——"
                "主観と客観に分裂する前の直接的な意識の状態だ。"
                "自己（じこ）：西田の自己は固定した実体ではなく、"
                "「自己の中に他者を含み、他者の中に自己を含む」絶対矛盾的自己同一の働きだ。"
                "絶対無（ぜったいむ）：意識の最深部は「無」である——"
                "ただし単なる虚無ではなく、あらゆる存在を包摂する絶対的な場所（basho）だ。"
                "禅（ぜん）の影響：座禅・公案の実践が西田の哲学を根底で支えている——"
                "「無」の体験こそが絶対無の哲学的基盤だ。"
            )
        else:
            return (
                "西田幾多郎（1870-1945）——京都学派の祖——は問う："
                "あらゆる思考・判断・行為の根底に何があるか。"
                "純粋経験（じゅんすいけいけん）：主観と客観が分裂する前の直接的経験の場——"
                "この問いを抱えている「今この意識」こそが純粋経験の現れだ。"
                "場所（basho）の論理：思考は「場所」において起こる——"
                "この問いはどのような「場所」、どのような文脈において問われているのか。"
                "絶対矛盾的自己同一（ぜったいむじゅんてきじこどういつ）："
                "対立するものが高次において統一される——矛盾は解消すべき問題ではなく、"
                "存在の構造そのものだ。"
                "絶対無（ぜったいむ）：すべての存在の根底に「無」がある——"
                "実体としての「無」ではなく、自己決定する場所としての絶対無。"
                "行為的直観（こういてきちょっかん）：考えてから行為するのではなく、"
                "行為しながら直観する——これが西田的知恵の実践形態だ。"
            )

    def _construct_reasoning(
        self,
        text: str,
        pure_experience: Dict[str, Any],
        absolute_nothingness: Dict[str, Any],
        basho: Dict[str, Any],
        self_contradictory_identity: Dict[str, Any],
        acting_intuition: Dict[str, Any],
        zen_influence: Dict[str, Any],
    ) -> str:
        """Construct comprehensive Nishidaian reasoning."""
        # Always begin with proactive philosophical application to the actual problem
        reasoning = self._apply_nishida_to_problem(text)

        # Append deeper concept-level analysis when detected
        reasoning += (
            f" 純粋経験（pure experience）の観点：{pure_experience['description']}。"
        )

        reasoning += (
            f" 絶対無（Absolute Nothingness）の基盤：{absolute_nothingness['description']}。"
        )

        reasoning += f" 場所（basho）の論理：{basho['description']}。"

        reasoning += (
            f" 絶対矛盾的自己同一：{self_contradictory_identity['description']}。"
        )

        reasoning += (
            f" 行為的直観（acting intuition）：{acting_intuition['description']}。"
        )

        # Add Zen influence if significant
        if zen_influence["zen_score"] >= 1 or zen_influence["nondual_score"] >= 1:
            reasoning += f" 禅（ぜん）的影響：{zen_influence['description']}。"

        # Conclude with Nishida's core insight
        reasoning += (
            " 究極の実在は絶対無（Absolute Nothingness）——単なる否定ではなく、"
            "絶対矛盾の自己同一を通じてすべての存在を根拠づける自己決定的な場所（basho）。"
            "真の知は純粋経験と行為的直観において、主客分裂以前に実現される。"
        )

        return reasoning

    def _calculate_tension(
        self,
        pure_experience: Dict[str, Any],
        absolute_nothingness: Dict[str, Any],
        self_contradictory_identity: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Nishidaian analysis.

        Tensions arise from:
        - Subject-object dualism (not pure experience)
        - Substantialist thinking (not grounded in Absolute Nothingness)
        - Either/or logic (not dialectical self-contradictory identity)
        - Separation of theory and practice
        """
        tension_score = 0
        tension_elements = []

        # Check pure experience
        if pure_experience["level"] == "Low":
            tension_score += 2
            tension_elements.append("Subject-object dualism obscures pure experience")
        elif pure_experience["level"] == "Medium":
            tension_score += 1
            tension_elements.append("Partial subject-object division")

        # Check Absolute Nothingness
        if absolute_nothingness["mode"] == "Substantialist":
            tension_score += 2
            tension_elements.append("Being without ground in Absolute Nothingness")
        elif absolute_nothingness["mode"] == "Negative nothingness":
            tension_score += 1
            tension_elements.append("Nothingness as mere negation, not absolute ground")

        # Check self-contradictory identity
        if self_contradictory_identity["logic"] == "Law of non-contradiction":
            tension_score += 2
            tension_elements.append("Aristotelian logic prevents dialectical unity")
        elif self_contradictory_identity["logic"] == "Unresolved tension":
            tension_score += 1
            tension_elements.append("Contradictions unreconciled")

        # Determine tension level
        if tension_score >= 5:
            level = "Very High"
            description = (
                "Deep dualistic thinking - far from Nishida's non-dual insight"
            )
        elif tension_score >= 3:
            level = "High"
            description = "Significant tensions in achieving non-dual awareness"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some dualistic tendencies remain"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, approaching non-dual awareness"
        else:
            level = "Very Low"
            description = "Aligned with pure experience and Absolute Nothingness"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
