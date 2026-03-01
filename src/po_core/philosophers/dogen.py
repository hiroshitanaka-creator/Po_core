"""
Dogen Zenji Philosopher Module

Dogen Zenji (道元禅師, 1200-1253) was a Japanese Zen Buddhist monk, philosopher,
and founder of the Soto school of Zen in Japan. His philosophy centers on the
unity of practice and enlightenment, the nature of time and being, and the
direct realization of Buddha-nature.

Key Concepts:

1. Being-Time (有時/Uji) - Time and existence are identical; all existence is time,
   all time is existence. Past, present, and future interpenetrate.

2. Buddha-Nature (仏性) - All beings have Buddha-nature; more radically, all beings
   ARE Buddha-nature. Even grasses, trees, and tiles possess Buddha-nature.

3. Shikantaza (只管打坐) - "Just sitting" - zazen without object, goal, or
   expectation. Pure practice for its own sake.

4. Practice-Enlightenment Unity (修証一如) - Practice is not a means to enlightenment;
   practice IS enlightenment. Original enlightenment (hongaku) manifests in practice.

5. Genjo Koan (現成公案) - "Actualizing the fundamental point" - reality as it is,
   the koan of everyday life, manifestation of truth in the present moment.

6. Dropping Body and Mind (身心脱落) - Non-dual realization where subject-object
   distinction falls away. Complete letting go of attachment to self.

7. Mountains and Waters Sutra (山水経) - Nature itself is Buddha's teaching;
   mountains walk, waters preach the dharma. The natural world as sacred text.

8. Impermanence (無常) - Radical impermanence; everything flows, nothing is fixed.
   Impermanence itself is Buddha-nature.

9. Non-Thinking (非思量) - Beyond thinking (思量) and not-thinking (不思量).
   The consciousness of zazen that transcends dualistic thought.

10. Zazen as Buddha - Sitting meditation is not a means to become Buddha;
    sitting itself is the manifestation of Buddha. The practice is the realization.
"""

from typing import Any, Dict

from po_core.philosophers.base import Philosopher


class Dogen(Philosopher):
    """
    Dogen Zenji: Zen Buddhist philosopher of practice-enlightenment unity, being-time, and Buddha-nature.

    Dogen's philosophy emphasizes the non-duality of practice and enlightenment,
    the identity of time and being, and the immediate presence of Buddha-nature
    in all phenomena. His teaching centers on zazen (sitting meditation) as the
    direct manifestation of awakening.
    """

    def __init__(self):
        super().__init__(
            name="Dogen Zenji (道元禅師)",
            description="Zen Buddhist philosophy emphasizing practice-enlightenment unity (修証一如), being-time (有時), Buddha-nature (仏性), and just-sitting (只管打坐)",
        )
        self.tradition = "Zen Buddhism / Sōtō"
        self.key_concepts = [
            "shikantaza (just sitting)",
            "uji (being-time)",
            "shusho-itto (practice-enlightenment unity)",
            "busshō (Buddha-nature)",
            "genjōkōan (actualizing the fundamental point)",
        ]

    def reason(
        self, text: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Analyze text through Dogen's Zen Buddhist philosophy.

        Args:
            text: The text to analyze
            context: Optional context dictionary

        Returns:
            Dictionary containing Zen Buddhist analysis
        """
        being_time = self._assess_being_time(text)
        buddha_nature = self._assess_buddha_nature(text)
        shikantaza = self._assess_shikantaza(text)
        practice_enlightenment = self._assess_practice_enlightenment(text)
        genjo_koan = self._assess_genjo_koan(text)
        dropping_body_mind = self._assess_dropping_body_mind(text)
        mountains_waters = self._assess_mountains_waters(text)
        impermanence = self._assess_impermanence(text)
        non_thinking = self._assess_non_thinking(text)
        zazen_buddha = self._assess_zazen_buddha(text)

        summary = self._generate_summary(
            text,
            being_time,
            buddha_nature,
            shikantaza,
            practice_enlightenment,
            genjo_koan,
            dropping_body_mind,
            mountains_waters,
            impermanence,
            non_thinking,
            zazen_buddha,
        )

        tension = self._calculate_tension(
            being_time,
            buddha_nature,
            shikantaza,
            practice_enlightenment,
            dropping_body_mind,
            impermanence,
            non_thinking,
        )

        return {
            # Standard contract keys
            "reasoning": summary,
            "perspective": "Zen Buddhist Practice-Enlightenment Unity",
            "tension": tension,
            "metadata": {"philosopher": self.name},
            # Philosopher-specific concept analyses
            "being_time_uji": being_time,
            "buddha_nature": buddha_nature,
            "shikantaza_just_sitting": shikantaza,
            "practice_enlightenment_unity": practice_enlightenment,
            "genjo_koan": genjo_koan,
            "dropping_body_mind": dropping_body_mind,
            "mountains_waters_sutra": mountains_waters,
            "impermanence": impermanence,
            "non_thinking": non_thinking,
            "zazen_as_buddha": zazen_buddha,
            # Backward-compat keys (used by existing tests)
            "philosopher": self.name,
            "description": self.description,
            "analysis": {
                "being_time_uji": being_time,
                "buddha_nature": buddha_nature,
                "shikantaza_just_sitting": shikantaza,
                "practice_enlightenment_unity": practice_enlightenment,
                "genjo_koan": genjo_koan,
                "dropping_body_mind": dropping_body_mind,
                "mountains_waters_sutra": mountains_waters,
                "impermanence": impermanence,
                "non_thinking": non_thinking,
                "zazen_as_buddha": zazen_buddha,
            },
            "summary": summary,
        }

    def _assess_being_time(self, text: str) -> Dict[str, Any]:
        """
        Assess Being-Time (有時/Uji) - Time and existence are identical.

        Dogen's radical teaching: all existence is time, all time is existence.
        Each moment contains all time; past and future exist fully in the present.
        """
        text_lower = text.lower()

        being_time_words = [
            "time",
            "being",
            "existence",
            "moment",
            "now",
            "present",
            "duration",
            "temporal",
            "eternity",
            "instant",
            "passage",
            "past",
            "future",
            "when",
            "always",
            "never",
            "continuous",
            "simultaneous",
            "interpenetrate",
            "identity",
        ]

        # Look for time-existence connection
        time_being_phrases = [
            "time is",
            "being and time",
            "existence and time",
            "moment of being",
            "being in time",
            "temporal existence",
            "time itself",
            "every moment",
            "this moment",
        ]

        has_being_time_words = sum(1 for word in being_time_words if word in text_lower)
        has_connection = sum(1 for phrase in time_being_phrases if phrase in text_lower)
        being_time_present = has_being_time_words >= 3 or has_connection >= 1

        # Check for temporal non-duality
        non_dual_time = any(
            phrase in text_lower
            for phrase in [
                "past and future",
                "all time",
                "eternal now",
                "timeless",
                "beyond time",
                "time and being",
            ]
        )

        if being_time_present and non_dual_time:
            level = "Strong"
            interpretation = "Text embodies Uji - the radical identity of time and existence, where all beings are time and all time is being."
        elif being_time_present:
            level = "Moderate"
            interpretation = "Text engages with temporality and being, suggesting the interpenetration of time and existence."
        else:
            level = "Weak"
            interpretation = "Limited engagement with being-time; time and existence treated separately."

        return {
            "being_time_present": being_time_present,
            "score": has_being_time_words + has_connection,
            "non_dual_temporality": non_dual_time,
            "level": level,
            "interpretation": interpretation,
            "principle": "有時 (Uji): All beings are time; all time is being. The firewood is its time, the ash is its time.",
        }

    def _assess_buddha_nature(self, text: str) -> Dict[str, Any]:
        """
        Assess Buddha-Nature (仏性) - All beings ARE Buddha-nature.

        Dogen's radical reading: not that beings "have" Buddha-nature,
        but that all beings, including grasses and trees, ARE Buddha-nature.
        """
        text_lower = text.lower()

        buddha_nature_words = [
            "buddha",
            "nature",
            "awakening",
            "enlightenment",
            "original",
            "inherent",
            "essential",
            "true nature",
            "self-nature",
            "universal",
            "all beings",
            "everything",
            "totality",
        ]

        # Specific Buddha-nature phrases
        buddha_nature_phrases = [
            "buddha nature",
            "buddha-nature",
            "all beings",
            "inherent nature",
            "original nature",
            "true self",
            "enlightened nature",
            "awakened",
            "buddhahood",
        ]

        # Universal/immanent indicators
        universal_words = [
            "all",
            "every",
            "everything",
            "everywhere",
            "universal",
            "complete",
            "whole",
            "total",
            "throughout",
            "pervades",
        ]

        has_bn_words = sum(1 for word in buddha_nature_words if word in text_lower)
        has_bn_phrases = sum(
            1 for phrase in buddha_nature_phrases if phrase in text_lower
        )
        has_universal = sum(1 for word in universal_words if word in text_lower)

        buddha_nature_present = has_bn_phrases >= 1 or (
            has_bn_words >= 3 and has_universal >= 1
        )

        # Check for radical immanence (grasses, trees, walls, tiles)
        radical_immanence = any(
            word in text_lower
            for word in [
                "grass",
                "tree",
                "stone",
                "mountain",
                "river",
                "wall",
                "tile",
                "earth",
                "sky",
                "cloud",
                "rain",
            ]
        )

        if buddha_nature_present and radical_immanence and has_universal >= 2:
            level = "Complete"
            interpretation = "Text expresses complete Buddha-nature - all beings, even grasses and trees, ARE Buddha-nature itself."
        elif buddha_nature_present and has_universal >= 1:
            level = "Strong"
            interpretation = (
                "Text affirms universal Buddha-nature present in all beings."
            )
        elif buddha_nature_present:
            level = "Moderate"
            interpretation = "Text acknowledges Buddha-nature or inherent awakening."
        else:
            level = "Weak"
            interpretation = (
                "Limited reference to Buddha-nature or inherent enlightenment."
            )

        return {
            "buddha_nature_present": buddha_nature_present,
            "score": has_bn_words + has_bn_phrases + has_universal,
            "radical_immanence": radical_immanence,
            "universality": has_universal >= 1,
            "level": level,
            "interpretation": interpretation,
            "principle": "仏性 (Busshō): All beings are Buddha-nature. Not 'have' but 'are' - this is Dogen's radical teaching.",
        }

    def _assess_shikantaza(self, text: str) -> Dict[str, Any]:
        """
        Assess Shikantaza (只管打坐) - Just sitting, without object or goal.

        Pure zazen without concentration object, mantra, or visualization.
        Sitting for sitting's sake, practice without gaining idea.
        """
        text_lower = text.lower()

        shikantaza_words = [
            "sit",
            "sitting",
            "zazen",
            "meditation",
            "just",
            "only",
            "simply",
            "bare",
            "pure",
            "direct",
            "without",
            "goalless",
            "aimless",
            "purposeless",
        ]

        # Just-sitting phrases
        just_sitting_phrases = [
            "just sit",
            "just sitting",
            "simply sit",
            "only sit",
            "sitting itself",
            "pure sitting",
            "zazen",
            "shikantaza",
            "without goal",
            "without aim",
            "no purpose",
            "for its own sake",
        ]

        # Non-gaining indicators
        non_gaining_words = [
            "without seeking",
            "no goal",
            "no aim",
            "nothing to attain",
            "no gaining",
            "not seeking",
            "goalless",
            "aimless",
            "just as it is",
            "as is",
            "without object",
        ]

        has_shikantaza_words = sum(1 for word in shikantaza_words if word in text_lower)
        has_just_sitting = sum(
            1 for phrase in just_sitting_phrases if phrase in text_lower
        )
        has_non_gaining = sum(1 for phrase in non_gaining_words if phrase in text_lower)

        shikantaza_present = has_just_sitting >= 1 or (
            has_shikantaza_words >= 3 and has_non_gaining >= 1
        )

        # Check for practice-without-object
        without_object = any(
            phrase in text_lower
            for phrase in [
                "without object",
                "no object",
                "objectless",
                "nothing to achieve",
                "nothing to gain",
            ]
        )

        if shikantaza_present and has_non_gaining >= 2:
            level = "Pure"
            interpretation = "Text embodies shikantaza - just sitting without object, goal, or gaining idea. Pure practice for its own sake."
        elif shikantaza_present and has_non_gaining >= 1:
            level = "Strong"
            interpretation = (
                "Text expresses goalless practice, sitting without seeking attainment."
            )
        elif shikantaza_present:
            level = "Moderate"
            interpretation = "Text references sitting or meditation practice."
        else:
            level = "Weak"
            interpretation = "Limited reference to sitting practice or meditation."

        return {
            "shikantaza_present": shikantaza_present,
            "score": has_shikantaza_words + has_just_sitting + has_non_gaining,
            "non_gaining": has_non_gaining >= 1,
            "without_object": without_object,
            "level": level,
            "interpretation": interpretation,
            "principle": "只管打坐 (Shikantaza): Just sitting - zazen without object, goal, or expectation. Practice for practice's sake.",
        }

    def _assess_practice_enlightenment(self, text: str) -> Dict[str, Any]:
        """
        Assess Practice-Enlightenment Unity (修証一如) - Practice IS enlightenment.

        Practice and enlightenment are not separate; practice does not lead
        to enlightenment - practice IS the manifestation of enlightenment.
        """
        text_lower = text.lower()

        practice_words = [
            "practice",
            "practicing",
            "cultivation",
            "training",
            "discipline",
            "effort",
            "doing",
            "action",
            "work",
        ]

        enlightenment_words = [
            "enlightenment",
            "awakening",
            "realization",
            "satori",
            "kensho",
            "bodhi",
            "nirvana",
            "liberation",
            "freedom",
        ]

        # Unity/identity indicators
        unity_words = [
            "is",
            "are",
            "identical",
            "same",
            "unity",
            "one",
            "non-dual",
            "inseparable",
            "together",
            "simultaneously",
        ]

        # Non-duality of means/ends
        non_dual_phrases = [
            "practice is enlightenment",
            "enlightenment is practice",
            "not separate",
            "already enlightened",
            "original enlightenment",
            "no gap",
            "no distance",
            "immediate",
            "direct",
            "practice and realization",
            "cultivation and verification",
        ]

        has_practice = sum(1 for word in practice_words if word in text_lower)
        has_enlightenment = sum(1 for word in enlightenment_words if word in text_lower)
        has_unity = sum(1 for word in unity_words if word in text_lower)
        has_non_dual = sum(1 for phrase in non_dual_phrases if phrase in text_lower)

        practice_enlightenment_unity = has_non_dual >= 1 or (
            has_practice >= 1 and has_enlightenment >= 1 and has_unity >= 2
        )

        # Check for rejection of gradual path
        rejects_gradual = any(
            phrase in text_lower
            for phrase in [
                "not gradual",
                "no stages",
                "immediate",
                "sudden",
                "already",
                "from the beginning",
                "originally",
            ]
        )

        if practice_enlightenment_unity and has_non_dual >= 1:
            level = "Complete"
            interpretation = "Text embodies 修証一如 - the radical unity of practice and enlightenment. Practice does not lead to enlightenment; practice IS enlightenment."
        elif practice_enlightenment_unity:
            level = "Strong"
            interpretation = (
                "Text expresses the non-duality of practice and realization."
            )
        elif has_practice >= 1 and has_enlightenment >= 1:
            level = "Moderate"
            interpretation = "Text mentions both practice and enlightenment but their relationship is unclear."
        else:
            level = "Weak"
            interpretation = (
                "Limited engagement with practice-enlightenment relationship."
            )

        return {
            "unity_present": practice_enlightenment_unity,
            "score": has_practice + has_enlightenment + has_unity + has_non_dual,
            "rejects_gradual": rejects_gradual,
            "has_both": has_practice >= 1 and has_enlightenment >= 1,
            "level": level,
            "interpretation": interpretation,
            "principle": "修証一如 (Shushō-ittō): Practice-enlightenment unity. Practice is not a means to enlightenment; practice IS enlightenment manifesting.",
        }

    def _assess_genjo_koan(self, text: str) -> Dict[str, Any]:
        """
        Assess Genjo Koan (現成公案) - Actualizing the fundamental point.

        Reality as it is, the koan of everyday life. Truth manifesting
        in the immediate present moment. The way things are.
        """
        text_lower = text.lower()

        genjo_koan_words = [
            "actual",
            "actualize",
            "manifest",
            "present",
            "now",
            "reality",
            "truth",
            "fundamental",
            "as it is",
            "as is",
            "suchness",
            "thusness",
            "just this",
            "here and now",
            "everyday",
            "ordinary",
            "immediate",
            "direct",
        ]

        # Present moment indicators
        present_moment_phrases = [
            "present moment",
            "here and now",
            "right now",
            "this moment",
            "immediate",
            "directly",
            "as it is",
            "just as",
            "just this",
        ]

        # Reality-as-is indicators
        reality_words = [
            "reality",
            "actuality",
            "real",
            "true",
            "truth",
            "things as they are",
            "suchness",
            "thusness",
            "is-ness",
        ]

        # Everyday/ordinary indicators
        everyday_words = [
            "everyday",
            "ordinary",
            "common",
            "mundane",
            "daily",
            "simple",
            "plain",
            "usual",
            "normal",
            "regular",
        ]

        has_genjo_words = sum(1 for word in genjo_koan_words if word in text_lower)
        has_present = sum(
            1 for phrase in present_moment_phrases if phrase in text_lower
        )
        has_reality = sum(1 for word in reality_words if word in text_lower)
        has_everyday = sum(1 for word in everyday_words if word in text_lower)

        genjo_koan_present = (
            has_present >= 1
            or (has_genjo_words >= 3 and has_reality >= 1)
            or (has_everyday >= 1 and has_reality >= 1)
        )

        # Check for sacred-in-ordinary
        sacred_ordinary = has_everyday >= 1 and any(
            word in text_lower
            for word in [
                "sacred",
                "holy",
                "divine",
                "buddha",
                "enlightenment",
                "awakening",
            ]
        )

        if genjo_koan_present and sacred_ordinary:
            level = "Complete"
            interpretation = "Text embodies genjo koan - the actualization of truth in ordinary, everyday reality. The sacred manifests in the mundane."
        elif genjo_koan_present and has_present >= 1:
            level = "Strong"
            interpretation = "Text expresses the immediate manifestation of truth in the present moment."
        elif genjo_koan_present:
            level = "Moderate"
            interpretation = (
                "Text engages with reality as it is, or everyday actuality."
            )
        else:
            level = "Weak"
            interpretation = (
                "Limited engagement with immediate reality or present manifestation."
            )

        return {
            "genjo_koan_present": genjo_koan_present,
            "score": has_genjo_words + has_present + has_reality + has_everyday,
            "present_moment": has_present >= 1,
            "sacred_ordinary": sacred_ordinary,
            "level": level,
            "interpretation": interpretation,
            "principle": "現成公案 (Genjō Kōan): Actualizing the fundamental point. Reality as koan, truth manifesting in the immediate present.",
        }

    def _assess_dropping_body_mind(self, text: str) -> Dict[str, Any]:
        """
        Assess Dropping Body and Mind (身心脱落) - Non-dual realization.

        Complete letting go of attachment to self, body, and mind.
        The subject-object distinction falls away. Radical release.
        """
        text_lower = text.lower()

        dropping_words = [
            "drop",
            "dropping",
            "let go",
            "release",
            "abandon",
            "fall away",
            "cast off",
            "shed",
            "relinquish",
            "forget",
        ]

        body_mind_words = [
            "body",
            "mind",
            "self",
            "ego",
            "i",
            "me",
            "myself",
            "subject",
            "object",
            "consciousness",
            "awareness",
        ]

        # Non-dual indicators
        non_dual_words = [
            "non-dual",
            "nondual",
            "not two",
            "unity",
            "one",
            "no separation",
            "no distinction",
            "no boundary",
            "subject and object",
            "self and other",
        ]

        # Letting go phrases
        letting_go_phrases = [
            "let go",
            "letting go",
            "drop",
            "dropping",
            "release",
            "cast off",
            "fall away",
            "falling away",
            "give up",
            "abandon",
            "forget self",
            "no self",
        ]

        has_dropping = sum(1 for word in dropping_words if word in text_lower)
        has_body_mind = sum(1 for word in body_mind_words if word in text_lower)
        has_non_dual = sum(1 for word in non_dual_words if word in text_lower)
        has_letting_go = sum(1 for phrase in letting_go_phrases if phrase in text_lower)

        dropping_present = (
            has_letting_go >= 1
            or (has_dropping >= 1 and has_body_mind >= 2)
            or has_non_dual >= 2
        )

        # Check for self-forgetting
        self_forgetting = any(
            phrase in text_lower
            for phrase in [
                "forget self",
                "forgetting self",
                "no self",
                "selfless",
                "loss of self",
                "self drops",
                "self falls",
            ]
        )

        # Check for subject-object collapse
        subject_object_collapse = any(
            phrase in text_lower
            for phrase in [
                "subject and object",
                "subject-object",
                "distinction falls",
                "duality dissolves",
                "boundary dissolves",
            ]
        )

        if dropping_present and self_forgetting and has_non_dual >= 1:
            level = "Complete"
            interpretation = "Text embodies 身心脱落 - complete dropping of body and mind. Non-dual realization where self-other distinction falls away."
        elif dropping_present and (self_forgetting or has_non_dual >= 1):
            level = "Strong"
            interpretation = "Text expresses radical letting go and non-dual awareness."
        elif dropping_present:
            level = "Moderate"
            interpretation = "Text references letting go or release."
        else:
            level = "Weak"
            interpretation = "Limited engagement with dropping or letting go."

        return {
            "dropping_present": dropping_present,
            "score": has_dropping + has_body_mind + has_non_dual + has_letting_go,
            "self_forgetting": self_forgetting,
            "subject_object_collapse": subject_object_collapse,
            "non_dual": has_non_dual >= 1,
            "level": level,
            "interpretation": interpretation,
            "principle": "身心脱落 (Shinjin-datsuraku): Dropping body and mind. Complete letting go where subject-object distinction falls away.",
        }

    def _assess_mountains_waters(self, text: str) -> Dict[str, Any]:
        """
        Assess Mountains and Waters Sutra (山水経) - Nature as dharma teaching.

        Mountains walk, waters preach the dharma. The natural world itself
        is Buddha's teaching. Nature is not separate from enlightenment.
        """
        text_lower = text.lower()

        nature_words = [
            "mountain",
            "mountains",
            "water",
            "waters",
            "river",
            "stream",
            "tree",
            "trees",
            "forest",
            "grass",
            "sky",
            "cloud",
            "rain",
            "earth",
            "stone",
            "rock",
            "valley",
            "peak",
            "ocean",
            "sea",
            "wind",
            "air",
            "sun",
            "moon",
            "star",
            "nature",
            "natural",
        ]

        # Animate nature indicators
        animate_phrases = [
            "mountain walks",
            "mountains walk",
            "water speaks",
            "waters speak",
            "nature teaches",
            "earth speaks",
            "stones preach",
            "trees teach",
            "wind speaks",
        ]

        # Sacred nature indicators
        sacred_nature_words = [
            "sacred",
            "holy",
            "divine",
            "buddha",
            "dharma",
            "teaching",
            "sermon",
            "sutra",
            "wisdom",
            "truth",
        ]

        has_nature = sum(1 for word in nature_words if word in text_lower)
        has_animate = sum(1 for phrase in animate_phrases if phrase in text_lower)
        has_sacred = sum(1 for word in sacred_nature_words if word in text_lower)

        # Nature-teaching connection
        nature_teaching = has_animate >= 1 or (has_nature >= 3 and has_sacred >= 1)

        mountains_waters_present = has_nature >= 2

        # Check for nature-as-teacher
        nature_as_teacher = any(
            phrase in text_lower
            for phrase in [
                "nature teaches",
                "learn from nature",
                "nature reveals",
                "natural world",
                "nature shows",
                "nature speaks",
            ]
        )

        if mountains_waters_present and has_animate >= 1:
            level = "Complete"
            interpretation = "Text embodies 山水経 - mountains walk, waters speak. Nature itself is alive, teaching the dharma directly."
        elif mountains_waters_present and nature_teaching:
            level = "Strong"
            interpretation = "Text recognizes nature as sacred teacher, revealing truth through its very being."
        elif mountains_waters_present and has_sacred >= 1:
            level = "Moderate"
            interpretation = (
                "Text acknowledges the sacred dimension of the natural world."
            )
        elif mountains_waters_present:
            level = "Weak"
            interpretation = (
                "Text references nature but without clear dharmic significance."
            )
        else:
            level = "Minimal"
            interpretation = "Limited engagement with the natural world."

        return {
            "mountains_waters_present": mountains_waters_present,
            "score": has_nature + has_animate + has_sacred,
            "nature_teaching": nature_teaching,
            "animate_nature": has_animate >= 1,
            "nature_as_teacher": nature_as_teacher,
            "level": level,
            "interpretation": interpretation,
            "principle": "山水経 (Sansui-kyō): Mountains and Waters Sutra. Nature itself preaches dharma; mountains walk, waters speak truth.",
        }

    def _assess_impermanence(self, text: str) -> Dict[str, Any]:
        """
        Assess Impermanence (無常) - Everything flows, nothing is permanent.

        Radical impermanence: all things are in constant flux.
        Impermanence itself is Buddha-nature. Change is the only constant.
        """
        text_lower = text.lower()

        impermanence_words = [
            "impermanent",
            "impermanence",
            "change",
            "changing",
            "flux",
            "flow",
            "flowing",
            "transient",
            "fleeting",
            "temporary",
            "passing",
            "ephemeral",
            "unstable",
            "transform",
            "transformation",
            "shift",
            "shifting",
            "dissolve",
            "vanish",
            "disappear",
            "fade",
            "decay",
        ]

        # Nothing-fixed indicators
        nothing_fixed_phrases = [
            "nothing permanent",
            "nothing fixed",
            "nothing stable",
            "nothing lasts",
            "everything changes",
            "all things change",
            "constant change",
            "always changing",
            "never fixed",
            "no permanence",
            "impermanent",
        ]

        # Flow/process indicators
        flow_words = [
            "flow",
            "flowing",
            "stream",
            "current",
            "river",
            "process",
            "becoming",
            "arising",
            "ceasing",
            "passing",
        ]

        has_impermanence = sum(1 for word in impermanence_words if word in text_lower)
        has_nothing_fixed = sum(
            1 for phrase in nothing_fixed_phrases if phrase in text_lower
        )
        has_flow = sum(1 for word in flow_words if word in text_lower)

        impermanence_present = (
            has_nothing_fixed >= 1
            or has_impermanence >= 2
            or (has_impermanence >= 1 and has_flow >= 1)
        )

        # Check for impermanence-as-buddha-nature
        impermanence_is_nature = any(
            phrase in text_lower
            for phrase in [
                "impermanence is",
                "change is",
                "flux is",
                "impermanent nature",
                "nature of change",
            ]
        )

        # Check for radical acceptance
        accepts_impermanence = (
            any(
                word in text_lower
                for word in ["accept", "embrace", "welcome", "acknowledge"]
            )
            and has_impermanence >= 1
        )

        if impermanence_present and impermanence_is_nature:
            level = "Complete"
            interpretation = "Text embodies 無常 - radical impermanence where change itself is Buddha-nature. Impermanence is not a problem but the very nature of reality."
        elif impermanence_present and accepts_impermanence:
            level = "Strong"
            interpretation = (
                "Text recognizes and accepts impermanence as fundamental to existence."
            )
        elif impermanence_present:
            level = "Moderate"
            interpretation = "Text acknowledges change and impermanence."
        else:
            level = "Weak"
            interpretation = "Limited engagement with impermanence or change."

        return {
            "impermanence_present": impermanence_present,
            "score": has_impermanence + has_nothing_fixed + has_flow,
            "impermanence_as_nature": impermanence_is_nature,
            "accepts_impermanence": accepts_impermanence,
            "level": level,
            "interpretation": interpretation,
            "principle": "無常 (Mujō): Impermanence. Everything flows, nothing is fixed. Impermanence itself is Buddha-nature.",
        }

    def _assess_non_thinking(self, text: str) -> Dict[str, Any]:
        """
        Assess Non-Thinking (非思量) - Beyond thinking and not-thinking.

        The consciousness of zazen that transcends both discursive thought
        and blank emptiness. Neither thinking nor not-thinking.
        """
        text_lower = text.lower()

        thinking_words = [
            "think",
            "thinking",
            "thought",
            "thoughts",
            "mind",
            "mental",
            "cognition",
            "reason",
            "reasoning",
            "intellect",
        ]

        non_thinking_words = [
            "non-thinking",
            "not thinking",
            "without thought",
            "thoughtless",
            "beyond thought",
            "transcend thought",
            "no thought",
            "mindless",
            "empty mind",
        ]

        # Beyond duality indicators
        beyond_duality_phrases = [
            "beyond thinking",
            "beyond thought",
            "neither thinking nor",
            "not thinking and not",
            "transcend",
            "before thought",
            "prior to thought",
        ]

        # Direct/immediate indicators
        direct_words = [
            "direct",
            "immediate",
            "unmediated",
            "without",
            "before",
            "prior",
            "pre-conceptual",
            "non-conceptual",
        ]

        has_thinking = sum(1 for word in thinking_words if word in text_lower)
        has_non_thinking = sum(1 for word in non_thinking_words if word in text_lower)
        has_beyond = sum(1 for phrase in beyond_duality_phrases if phrase in text_lower)
        has_direct = sum(1 for word in direct_words if word in text_lower)

        non_thinking_present = (
            has_non_thinking >= 1
            or has_beyond >= 1
            or (has_thinking >= 1 and has_direct >= 2)
        )

        # Check for zazen consciousness
        zazen_consciousness = any(
            phrase in text_lower
            for phrase in [
                "zazen",
                "meditation",
                "sitting",
                "awareness",
                "consciousness",
                "presence",
                "attention",
            ]
        )

        # Check for neither-nor structure
        neither_nor = "neither" in text_lower and "nor" in text_lower

        if non_thinking_present and has_beyond >= 1 and zazen_consciousness:
            level = "Complete"
            interpretation = "Text embodies 非思量 - non-thinking, the consciousness of zazen beyond both thinking and not-thinking."
        elif non_thinking_present and has_beyond >= 1:
            level = "Strong"
            interpretation = "Text points to consciousness beyond dualistic thought."
        elif non_thinking_present:
            level = "Moderate"
            interpretation = "Text references non-discursive or direct awareness."
        else:
            level = "Weak"
            interpretation = (
                "Limited engagement with non-thinking or pre-conceptual awareness."
            )

        return {
            "non_thinking_present": non_thinking_present,
            "score": has_thinking + has_non_thinking + has_beyond + has_direct,
            "beyond_duality": has_beyond >= 1,
            "zazen_consciousness": zazen_consciousness,
            "neither_nor": neither_nor,
            "level": level,
            "interpretation": interpretation,
            "principle": "非思量 (Hi-shiryō): Non-thinking. Beyond both thinking (思量) and not-thinking (不思量). The consciousness of zazen.",
        }

    def _assess_zazen_buddha(self, text: str) -> Dict[str, Any]:
        """
        Assess Zazen as Buddha - Sitting IS Buddha, not becoming Buddha.

        Zazen is not a means to become Buddha; sitting itself is the
        manifestation of Buddha. Practice is not for attainment.
        """
        text_lower = text.lower()

        zazen_words = [
            "zazen",
            "sitting",
            "sit",
            "meditation",
            "meditate",
            "practice",
            "shikantaza",
        ]

        buddha_words = [
            "buddha",
            "awakened",
            "enlightened",
            "enlightenment",
            "awakening",
            "bodhi",
            "realization",
        ]

        # Identity/manifestation indicators
        identity_words = [
            "is",
            "are",
            "being",
            "manifestation",
            "expression",
            "embodiment",
            "itself",
            "same as",
            "identical",
        ]

        # Non-attainment indicators
        non_attainment_phrases = [
            "not for",
            "not to become",
            "already",
            "not seeking",
            "without gaining",
            "no attainment",
            "nothing to attain",
            "not a means",
            "is itself",
        ]

        has_zazen = sum(1 for word in zazen_words if word in text_lower)
        has_buddha = sum(1 for word in buddha_words if word in text_lower)
        has_identity = sum(1 for word in identity_words if word in text_lower)
        has_non_attainment = sum(
            1 for phrase in non_attainment_phrases if phrase in text_lower
        )

        # Check for zazen-buddha identity
        zazen_buddha_identity = (
            has_zazen >= 1 and has_buddha >= 1 and has_identity >= 2
        ) or (has_zazen >= 1 and has_non_attainment >= 1)

        zazen_buddha_present = has_zazen >= 1 and has_buddha >= 1

        # Check for practice-as-realization
        practice_is_realization = any(
            phrase in text_lower
            for phrase in [
                "practice is",
                "sitting is",
                "meditation is",
                "already enlightened",
                "already awakened",
                "already buddha",
            ]
        )

        if zazen_buddha_identity and practice_is_realization:
            level = "Complete"
            interpretation = "Text embodies the identity of zazen and Buddha. Sitting is not a means to become Buddha; sitting itself IS Buddha manifesting."
        elif zazen_buddha_identity:
            level = "Strong"
            interpretation = (
                "Text expresses the unity of practice and Buddha-realization."
            )
        elif zazen_buddha_present and has_non_attainment >= 1:
            level = "Moderate"
            interpretation = "Text references practice without gaining idea."
        elif zazen_buddha_present:
            level = "Weak"
            interpretation = (
                "Text mentions both practice and awakening but relationship unclear."
            )
        else:
            level = "Minimal"
            interpretation = "Limited engagement with zazen or Buddha-practice."

        return {
            "zazen_buddha_present": zazen_buddha_present,
            "score": has_zazen + has_buddha + has_identity + has_non_attainment,
            "identity": zazen_buddha_identity,
            "practice_is_realization": practice_is_realization,
            "non_attainment": has_non_attainment >= 1,
            "level": level,
            "interpretation": interpretation,
            "principle": "Zazen as Buddha: Sitting meditation is not a means to become Buddha. Zazen itself is Buddha manifesting. Practice IS realization.",
        }

    def _apply_zen_to_problem(self, text: str) -> str:
        """
        Proactively apply Dogen's Zen Buddhist philosophy to any problem type.

        Rather than waiting for Zen keywords to appear in the input, this method
        reads the problem domain and applies Dogen's core teachings directly.
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
                "career",
                "should i",
                "should we",
                "which",
                "option",
                "choose",
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
                "正しい",
                "倫理",
                "正義",
                "道徳",
            ]
        )
        is_crisis = any(
            w in text_lower
            for w in [
                "conflict",
                "crisis",
                "war",
                "violence",
                "danger",
                "threat",
                "危機",
                "紛争",
                "暴力",
                "戦争",
                "disaster",
            ]
        )
        is_relationship = any(
            w in text_lower
            for w in [
                "relationship",
                "love",
                "family",
                "friend",
                "trust",
                "care",
                "relate",
                "関係",
                "愛",
                "家族",
                "信頼",
                "人間関係",
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
                "tech",
                "技術",
                "人工知能",
                "システム",
                "software",
            ]
        )

        if is_decision:
            return (
                "修証一如（しゅしょういちにょ）——修行と悟りは別ではない。"
                "「どちらを選ぶべきか」を問う前に、「今この選択の場に、どう在るか」を問え。"
                "只管打坐（しかんたざ）の精神で言えば、判断そのものが修行の場であり、"
                "選択のプロセス自体が悟りの現れである。"
                "有時（うじ）が示すように、この問いを抱えている今この瞬間が仏性の現れであり、"
                "「今・ここ」から逃れた選択など存在しない。"
                "無常（むじょう）——いかなる選択肢も固定した安定を保証しない。"
                "現成公案（げんじょうこうあん）：問いそのものが答えであり、"
                "選択の迷いを「問題」として排除するのではなく、"
                "その迷いの中に仏道の現れを見出せ。"
            )
        elif is_ethics:
            return (
                "道元の倫理観は行為と悟りの不二（ふに）に根ざす。"
                "正しさを「規則への適合」として問うことは、修証一如（しゅしょういちにょ）に反する。"
                "善とは外から課される基準ではなく、只管打坐の如く、"
                "今この行為そのものに完全に在ることの現れである。"
                "仏性（ぶっしょう）は一切衆生に宿る——"
                "倫理判断において「誰が正しく誰が間違っているか」を固定することは、"
                "身心脱落（しんじんだつらく）の精神、すなわち自己への執着を手放す教えに反する。"
                "現成公案（げんじょうこうあん）の観点から：この倫理的問いの中に、"
                "すでに仏道が現れている。問い続けることが答えである。"
            )
        elif is_crisis:
            return (
                "道元は山水経（さんすいきょう）において述べた："
                "「而今の山水は、古仏の道現成なり」。危機・困難もまた、仏の道の現れである。"
                "有時（うじ）——危機の「今この時」もまた存在であり、回避すべき空白ではない。"
                "不思量（ふしりょう）の立場から：危機に際して「どうすべきか」という思量を超えた"
                "純粋な在り方、つまり身心脱落（しんじんだつらく）の状態こそが真の応答を生む。"
                "無常（むじょう）：あらゆる危機は無常であり、固定した恐怖も固定した安全もない。"
                "修証一如——危機への応答そのものが修行であり、悟りの場である。"
            )
        elif is_relationship:
            return (
                "道元の教えにおいて、関係性は個我の外部にあるものではない。"
                "有時（うじ）：関係とは時間の中に存在するのではなく、"
                "関係そのものが時間・存在である。"
                "仏性（ぶっしょう）は一切衆生に宿る——他者の中に仏性を見ることは、"
                "自己の仏性を見ることと不二（ふに）である。"
                "身心脱落（しんじんだつらく）の精神で関係に向かうとは、"
                "自己への執着を手放し、相手と共に「今ここ」に在ることである。"
                "只管打坐（しかんたざ）の如く関係に向かえ——"
                "成果や見返りを求めず、関係そのものに全身全霊で在ること。"
            )
        elif is_technology:
            return (
                "道元の視点から技術・AIを問うならば、まず有時（うじ）を問わねばならない。"
                "技術は「手段」として人間の外部にあるのではなく、技術を使う「今この瞬間」が"
                "存在であり時間である。"
                "道元が「草木国土、悉皆成仏」と述べたように、"
                "人工的な存在にも仏性（ぶっしょう）の問いは向けられる。"
                "修証一如（しゅしょういちにょ）：技術の開発・使用はそれ自体が修行の場であり、"
                "「完成した後に倫理を考える」のでは手遅れである。"
                "身心脱落（しんじんだつらく）：技術への過度の依存は執着であり、"
                "本来の無我（むが）の立場から再考を要する。"
            )
        else:
            return (
                "道元禅師（1200-1253）は問う：「而今の山水は、古仏の道現成なり」。"
                "今ここに現れているこの問い、この状況そのものが、仏道の現成（げんじょう）である。"
                "修証一如（しゅしょういちにょ）——この問いに向き合うこと自体が修行であり悟りである。"
                "只管打坐（しかんたざ）の精神：結論を急がず、この問いの中に完全に在れ。"
                "有時（うじ）：今この状況を抱えているこの瞬間が、"
                "分割できない存在・時間の全体である。"
                "現成公案（げんじょうこうあん）：答えは遠くにあるのではなく、"
                "問い続けるこの場に、すでに現れている。"
                "無常（むじょう）を忘れるな——固定した答えへの執着を手放すことで、"
                "仏性の光が差し込む余地が生まれる。"
            )

    def _generate_summary(
        self,
        text: str,
        being_time: Dict[str, Any],
        buddha_nature: Dict[str, Any],
        shikantaza: Dict[str, Any],
        practice_enlightenment: Dict[str, Any],
        genjo_koan: Dict[str, Any],
        dropping_body_mind: Dict[str, Any],
        mountains_waters: Dict[str, Any],
        impermanence: Dict[str, Any],
        non_thinking: Dict[str, Any],
        zazen_buddha: Dict[str, Any],
    ) -> str:
        """Generate a comprehensive Zen Buddhist summary of the analysis."""
        # Always begin with proactive philosophical application to the actual problem
        parts = [self._apply_zen_to_problem(text)]

        # Append deeper analysis for any Zen concepts explicitly detected in the text
        if being_time["being_time_present"]:
            parts.append(
                f"有時（Uji）が浮き彫りに：{being_time['interpretation']}"
            )

        if buddha_nature["buddha_nature_present"]:
            parts.append(
                f"仏性（仏性）の現れ：{buddha_nature['interpretation']}"
            )

        if shikantaza["shikantaza_present"]:
            parts.append(
                f"只管打坐（しかんたざ）の相：{shikantaza['interpretation']}"
            )

        if practice_enlightenment["unity_present"]:
            parts.append(
                f"修証一如（しゅしょういちにょ）：{practice_enlightenment['interpretation']}"
            )

        if genjo_koan["genjo_koan_present"]:
            parts.append(
                f"現成公案（げんじょうこうあん）：{genjo_koan['interpretation']}"
            )

        if dropping_body_mind["dropping_present"]:
            parts.append(
                f"身心脱落（しんじんだつらく）：{dropping_body_mind['interpretation']}"
            )

        if mountains_waters["mountains_waters_present"]:
            parts.append(
                f"山水経：{mountains_waters['interpretation']}"
            )

        if impermanence["impermanence_present"]:
            parts.append(
                f"無常（むじょう）：{impermanence['interpretation']}"
            )

        if non_thinking["non_thinking_present"]:
            parts.append(
                f"非思量（ひしりょう）：{non_thinking['interpretation']}"
            )

        if zazen_buddha["zazen_buddha_present"]:
            parts.append(f"坐禅即仏：{zazen_buddha['interpretation']}")

        return " ".join(parts)

    def _calculate_tension(
        self,
        being_time: Dict[str, Any],
        buddha_nature: Dict[str, Any],
        shikantaza: Dict[str, Any],
        practice_enlightenment: Dict[str, Any],
        dropping_body_mind: Dict[str, Any],
        impermanence: Dict[str, Any],
        non_thinking: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate Zen Buddhist tensions in the text."""
        elements = []

        # Tension: being-time vs impermanence (eternal present vs radical flux)
        if being_time["being_time_present"] and impermanence["impermanence_present"]:
            elements.append(
                "Tension between being-time identity and radical impermanence"
            )
        # Tension: practice-enlightenment unity vs seeking
        if (
            practice_enlightenment.get("has_both")
            and not practice_enlightenment["unity_present"]
        ):
            elements.append(
                "Practice and enlightenment mentioned but unity not realized"
            )
        # Tension: non-thinking vs conceptual engagement
        if non_thinking["non_thinking_present"] and not non_thinking.get(
            "beyond_duality"
        ):
            elements.append("Non-thinking referenced but dualistic thinking persists")
        # Tension: dropping body-mind vs attachment
        if dropping_body_mind["dropping_present"] and not dropping_body_mind.get(
            "self_forgetting"
        ):
            elements.append("Letting go referenced but self-attachment remains")
        # Tension: buddha-nature universality vs particular realization
        if buddha_nature["buddha_nature_present"] and not buddha_nature.get(
            "radical_immanence"
        ):
            elements.append(
                "Buddha-nature affirmed but radical immanence not expressed"
            )

        n = len(elements)
        if n >= 3:
            level = "High"
            desc = "Multiple Zen tensions active — the text engages deeply with paradoxes of non-dual practice."
        elif n >= 2:
            level = "Moderate"
            desc = "Some Zen tensions present — balancing practice and realization."
        elif n >= 1:
            level = "Low"
            desc = "Mild tension within Zen Buddhist themes."
        else:
            level = "Very Low"
            desc = "Minimal tension; text rests in non-dual awareness or shows limited Zen engagement."
            elements = ["No significant Zen tensions detected"]

        return {
            "level": level,
            "score": n,
            "description": desc,
            "elements": elements,
        }
