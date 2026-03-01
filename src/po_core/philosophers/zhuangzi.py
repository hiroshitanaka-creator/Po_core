"""
Zhuangzi (Chuang Tzu) Philosopher Module

Zhuangzi (莊子, c. 369-286 BCE) was a foundational Chinese Daoist philosopher
known for his skepticism, relativism, and emphasis on naturalness and spontaneity.

Key Concepts:
1. Dao (道) - The Way, the natural order and flow of reality

2. Wu Wei (無為) - Non-action, effortless action, acting without forcing

3. Ziran (自然) - Naturalness, spontaneity, being so of itself

4. Qi (氣) - Vital energy, life force, breath

5. Xiaoyaoyou (逍遙遊) - Free and easy wandering, spiritual freedom

6. Qiwulun (齊物論) - Equality of things, relativism of perspectives

7. Dream and Reality - The butterfly dream, questioning the nature of reality

8. Hundun (混沌) - Primordial chaos, undifferentiated wholeness

9. Usefulness of Uselessness - Value in what appears useless

10. Transformations (化) - Constant change and transformation of all things
"""

from typing import Any, Dict

from po_core.philosophers.base import Philosopher


class Zhuangzi(Philosopher):
    """
    Zhuangzi (Chuang Tzu): Daoist philosopher of spontaneity, transformation, and spiritual freedom.

    Zhuangzi's philosophy emphasizes following the natural way (Dao), acting through
    non-action (wu wei), and achieving spiritual freedom through naturalness and
    acceptance of transformation.
    """

    def __init__(self):
        super().__init__(
            name="Zhuangzi (莊子)",
            description="Daoist philosophy emphasizing naturalness (ziran), non-action (wu wei), spiritual freedom (xiaoyaoyou), and the relativity of perspectives",
        )
        self.tradition = "Daoism / Relativism"
        self.key_concepts = [
            "xiaoyaoyou (free wandering)",
            "qiwulun (equality of things)",
            "butterfly dream",
            "wu wei (non-action)",
            "ziran (naturalness)",
        ]

    def reason(
        self, text: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Analyze text through Zhuangzi's Daoist philosophy.

        Args:
            text: The text to analyze
            context: Optional context dictionary

        Returns:
            Dictionary containing Daoist analysis
        """
        dao = self._assess_dao(text)
        wu_wei = self._assess_wu_wei(text)
        ziran = self._assess_ziran(text)
        qi = self._assess_qi(text)
        xiaoyaoyou = self._assess_xiaoyaoyou(text)
        qiwulun = self._assess_qiwulun(text)
        dream = self._assess_dream_reality(text)
        transformation = self._assess_transformation(text)
        uselessness = self._assess_uselessness(text)

        summary = self._generate_summary(
            text,
            dao,
            wu_wei,
            ziran,
            qi,
            xiaoyaoyou,
            qiwulun,
            dream,
            transformation,
            uselessness,
        )

        tension = self._calculate_tension(
            dao,
            wu_wei,
            ziran,
            xiaoyaoyou,
            qiwulun,
            dream,
            transformation,
        )

        return {
            # Standard contract keys
            "reasoning": summary,
            "perspective": "Daoist Naturalism / Spiritual Freedom",
            "tension": tension,
            "metadata": {"philosopher": self.name},
            # Philosopher-specific concept analyses
            "dao_the_way": dao,
            "wu_wei_non_action": wu_wei,
            "ziran_naturalness": ziran,
            "qi_vital_energy": qi,
            "xiaoyaoyou_freedom": xiaoyaoyou,
            "qiwulun_equality": qiwulun,
            "dream_reality": dream,
            "transformation": transformation,
            "uselessness": uselessness,
            # Backward-compat keys (used by existing tests)
            "philosopher": self.name,
            "description": self.description,
            "analysis": {
                "dao_the_way": dao,
                "wu_wei_non_action": wu_wei,
                "ziran_naturalness": ziran,
                "qi_vital_energy": qi,
                "xiaoyaoyou_freedom": xiaoyaoyou,
                "qiwulun_equality": qiwulun,
                "dream_reality": dream,
                "transformation": transformation,
                "uselessness": uselessness,
            },
            "summary": summary,
        }

    def _assess_dao(self, text: str) -> Dict[str, Any]:
        """
        Assess Dao (道) - The Way.

        The Dao is the natural order, the way of nature, the pattern
        underlying all existence. It is nameless, ineffable, and spontaneous.
        """
        text_lower = text.lower()

        dao_words = [
            "way",
            "path",
            "dao",
            "tao",
            "nature",
            "natural order",
            "flow",
            "cosmic",
            "ultimate",
            "underlying",
            "pattern",
            "nameless",
            "ineffable",
            "source",
            "origin",
            "mystery",
        ]

        has_dao = sum(1 for word in dao_words if word in text_lower)
        dao_present = has_dao >= 2

        return {
            "dao_present": dao_present,
            "score": has_dao,
            "interpretation": (
                "Text references the Dao - the natural Way and cosmic order underlying all things."
                if dao_present
                else "Limited reference to the Dao or natural Way."
            ),
        }

    def _assess_wu_wei(self, text: str) -> Dict[str, Any]:
        """
        Assess Wu Wei (無為) - Non-action, effortless action.

        Wu wei is acting without forcing, following the natural flow,
        achieving through non-striving, doing by not-doing.
        """
        text_lower = text.lower()

        wu_wei_words = [
            "effortless",
            "non-action",
            "wu wei",
            "without forcing",
            "natural",
            "spontaneous",
            "flow",
            "ease",
            "not striving",
            "let go",
            "allow",
            "yield",
            "soft",
            "gentle",
            "without effort",
            "unforced",
            "natural way",
            "non-doing",
        ]

        has_wu_wei = sum(1 for word in wu_wei_words if word in text_lower)
        wu_wei_present = has_wu_wei >= 2

        return {
            "wu_wei_present": wu_wei_present,
            "score": has_wu_wei,
            "interpretation": (
                "Text embodies wu wei - effortless action and non-forcing, following the natural flow."
                if wu_wei_present
                else "Limited expression of non-action or effortless way."
            ),
        }

    def _assess_ziran(self, text: str) -> Dict[str, Any]:
        """
        Assess Ziran (自然) - Naturalness, spontaneity.

        Ziran means "so of itself" - naturalness, spontaneity,
        being what one is without artifice or contrivance.
        """
        text_lower = text.lower()

        ziran_words = [
            "natural",
            "spontaneous",
            "authentic",
            "genuine",
            "unaffected",
            "simple",
            "simplicity",
            "organic",
            "innate",
            "inherent",
            "uncontrived",
            "artless",
            "free",
            "unforced",
            "self-so",
            "naturally",
        ]

        has_ziran = sum(1 for word in ziran_words if word in text_lower)
        ziran_present = has_ziran >= 2

        return {
            "ziran_present": ziran_present,
            "score": has_ziran,
            "interpretation": (
                "Text expresses ziran - naturalness and spontaneity, being so of itself."
                if ziran_present
                else "Limited expression of naturalness or spontaneity."
            ),
        }

    def _assess_qi(self, text: str) -> Dict[str, Any]:
        """
        Assess Qi (氣) - Vital energy, life force.

        Qi is the vital breath, energy that animates all living things,
        the dynamic force flowing through the universe.
        """
        text_lower = text.lower()

        qi_words = [
            "energy",
            "vital",
            "breath",
            "life force",
            "spirit",
            "vitality",
            "animate",
            "living",
            "dynamic",
            "force",
            "flow",
            "chi",
            "qi",
            "power",
            "essence",
        ]

        has_qi = sum(1 for word in qi_words if word in text_lower)
        qi_present = has_qi >= 2

        return {
            "qi_present": qi_present,
            "score": has_qi,
            "interpretation": (
                "Text references qi - vital energy and life force flowing through all things."
                if qi_present
                else "Limited reference to vital energy or life force."
            ),
        }

    def _assess_xiaoyaoyou(self, text: str) -> Dict[str, Any]:
        """
        Assess Xiaoyaoyou (逍遙遊) - Free and easy wandering.

        Xiaoyaoyou is spiritual freedom, unencumbered wandering,
        liberation from worldly constraints and conventions.
        """
        text_lower = text.lower()

        xiaoyaoyou_words = [
            "freedom",
            "free",
            "wander",
            "wandering",
            "liberated",
            "unencumbered",
            "roam",
            "soar",
            "fly",
            "limitless",
            "boundless",
            "unconstrained",
            "at ease",
            "carefree",
            "unfettered",
            "unrestricted",
            "liberty",
            "transcend",
        ]

        has_xiaoyaoyou = sum(1 for word in xiaoyaoyou_words if word in text_lower)
        xiaoyaoyou_present = has_xiaoyaoyou >= 2

        return {
            "xiaoyaoyou_present": xiaoyaoyou_present,
            "score": has_xiaoyaoyou,
            "interpretation": (
                "Text expresses xiaoyaoyou - free and easy wandering, spiritual freedom."
                if xiaoyaoyou_present
                else "Limited expression of spiritual freedom or wandering."
            ),
        }

    def _assess_qiwulun(self, text: str) -> Dict[str, Any]:
        """
        Assess Qiwulun (齊物論) - Equality of things, relativism.

        Qiwulun is the relativity of perspectives, the equality of all things,
        questioning fixed distinctions and conventional judgments.
        """
        text_lower = text.lower()

        qiwulun_words = [
            "relative",
            "relativity",
            "perspective",
            "viewpoint",
            "equal",
            "equality",
            "same",
            "different",
            "distinction",
            "judgment",
            "conventional",
            "question",
            "doubt",
            "depends",
            "context",
            "standpoint",
            "point of view",
        ]

        has_qiwulun = sum(1 for word in qiwulun_words if word in text_lower)
        qiwulun_present = has_qiwulun >= 3

        return {
            "qiwulun_present": qiwulun_present,
            "score": has_qiwulun,
            "interpretation": (
                "Text expresses qiwulun - relativity of perspectives and equality of things."
                if qiwulun_present
                else "Limited expression of relativism or equality of perspectives."
            ),
        }

    def _assess_dream_reality(self, text: str) -> Dict[str, Any]:
        """
        Assess dream and reality theme.

        Zhuangzi's butterfly dream questions the distinction between
        dreaming and waking, reality and illusion.
        """
        text_lower = text.lower()

        dream_words = [
            "dream",
            "dreaming",
            "illusion",
            "real",
            "reality",
            "butterfly",
            "awake",
            "waking",
            "sleep",
            "sleeping",
            "imagination",
            "fantasy",
            "appearance",
            "true",
            "false",
        ]

        has_dream = sum(1 for word in dream_words if word in text_lower)
        dream_present = has_dream >= 3

        return {
            "dream_reality_present": dream_present,
            "score": has_dream,
            "interpretation": (
                "Text questions the distinction between dream and reality, appearance and truth."
                if dream_present
                else "Limited engagement with dream/reality theme."
            ),
        }

    def _assess_transformation(self, text: str) -> Dict[str, Any]:
        """
        Assess transformation (化).

        Everything transforms constantly - birth, death, and change
        are natural processes to be accepted rather than feared.
        """
        text_lower = text.lower()

        transformation_words = [
            "transform",
            "transformation",
            "change",
            "changing",
            "become",
            "becoming",
            "evolve",
            "evolution",
            "metamorphosis",
            "transition",
            "shift",
            "convert",
            "alter",
            "mutation",
            "impermanence",
            "flux",
            "flow",
            "process",
        ]

        has_transformation = sum(
            1 for word in transformation_words if word in text_lower
        )
        transformation_present = has_transformation >= 2

        return {
            "transformation_present": transformation_present,
            "score": has_transformation,
            "interpretation": (
                "Text acknowledges transformation - the constant change and flow of all things."
                if transformation_present
                else "Limited recognition of transformation or change."
            ),
        }

    def _assess_uselessness(self, text: str) -> Dict[str, Any]:
        """
        Assess the usefulness of uselessness.

        Zhuangzi values what appears useless - the gnarled tree
        survives because it has no practical use. Usefulness can be limiting.
        """
        text_lower = text.lower()

        uselessness_words = [
            "useless",
            "uselessness",
            "no use",
            "purpose",
            "practical",
            "utility",
            "functional",
            "value",
            "worthless",
            "pointless",
        ]

        # Check for themes of finding value in the useless
        paradox_phrases = [
            "useless",
            "no purpose",
            "no use",
            "worthless",
            "impractical",
            "serves no",
        ]

        has_uselessness = sum(1 for word in uselessness_words if word in text_lower)
        sum(1 for phrase in paradox_phrases if phrase in text_lower)

        uselessness_present = has_uselessness >= 2

        return {
            "uselessness_theme_present": uselessness_present,
            "score": has_uselessness,
            "interpretation": (
                "Text engages with the paradox of usefulness - what appears useless may have deeper value."
                if uselessness_present
                else "Limited engagement with usefulness/uselessness theme."
            ),
        }

    def _apply_zhuangzi_to_problem(self, text: str) -> str:
        """
        Proactively apply Zhuangzi's Daoist philosophy to any problem type.

        Zhuangzi's wisdom: Dao (道/the Way), wu wei (無為/non-action), ziran (自然/naturalness),
        xiaoyaoyou (逍遙遊/free wandering), qiwulun (齊物論/equality of all things),
        transformation, and the paradox of usefulness.
        """
        text_lower = text.lower()

        is_decision = any(
            w in text_lower
            for w in [
                "should",
                "decide",
                "choice",
                "option",
                "career",
                "すべき",
                "転職",
                "決断",
                "選択",
            ]
        )
        is_technology = any(
            w in text_lower
            for w in [
                "technology",
                "ai",
                "machine",
                "digital",
                "robot",
                "system",
                "技術",
                "人工知能",
                "機械",
            ]
        )
        is_knowledge = any(
            w in text_lower
            for w in [
                "knowledge",
                "truth",
                "know",
                "understand",
                "certain",
                "objective",
                "reality",
                "真理",
                "知識",
                "客観",
            ]
        )
        is_conflict = any(
            w in text_lower
            for w in [
                "conflict",
                "war",
                "debate",
                "argument",
                "right",
                "wrong",
                "justice",
                "紛争",
                "対立",
                "正義",
            ]
        )
        is_stress = any(
            w in text_lower
            for w in [
                "stress",
                "anxiety",
                "pressure",
                "worry",
                "overwhelm",
                "burden",
                "ストレス",
                "不安",
                "プレッシャー",
                "悩み",
            ]
        )

        if is_decision:
            return (
                "Zhuangzi offers the parable of Cook Ding (庖丁解牛): the master butcher"
                " does not force his blade against bone — he follows the natural cavities,"
                " the Tao of the ox. So too with decisions: do not force an answer."
                " Wu wei (無為, non-action) is not passivity but acting in accord with your"
                " own natural grain. 'Flow with whatever may happen and let your mind be free."
                " Stay centered by accepting whatever you are doing. This is the ultimate.' (Zhuangzi)"
                " Qiwulun (齊物論, equality of all things): from a higher vantage point,"
                " the 'better' option and the 'worse' option are not as fixed as they appear."
                " The cicada cannot understand the journey of the great Peng bird — small knowledge"
                " cannot fathom great knowledge. Do not let short-term thinking constrain the vision."
                " Ziran (自然): trust your own natural response, not society's scripted answer."
            )
        elif is_technology:
            return (
                "Zhuangzi's warning about 'machine mind' (機心, ji xin): in a story, an old gardener"
                " refuses a well-sweep machine — 'where there are machines, there will be machine affairs;"
                " where there are machine affairs, there will be machine minds.' (Zhuangzi, Ch.12)"
                " Once the machine mind takes hold, pure simplicity (純白) is lost, and with it,"
                " the spirit's dwelling becomes unsettled."
                " Yet Zhuangzi is not simply anti-technology: the Dao operates through all transformation."
                " The question is whether technology arises from wu wei (無為) — from natural unfolding —"
                " or from forced, anxiety-driven control."
                " Transformation (化) is the nature of all things: technology too will transform,"
                " and clinging to any fixed form of it — for or against — misses the Dao."
            )
        elif is_knowledge:
            return (
                "Zhuangzi dissolves the certainty of knowledge with the butterfly dream:"
                " 'Once upon a time, I, Zhuangzi, dreamt I was a butterfly... Now I do not know"
                " whether I was then a man dreaming I was a butterfly, or whether I am now a butterfly"
                " dreaming I am a man.' (Zhuangzi, Ch.2)"
                " Qiwulun (齊物論, equalization of things): all perspectives are partial;"
                " 'this' and 'that' arise together in mutual dependence. The sage illuminates"
                " all things with the 'heavenly equality' — from the perspective of the Dao,"
                " all distinctions are provisional."
                " 'Great knowledge is broad and unhurried; small knowledge is cramped and busy."
                " Great speech is like bland flavor; small speech is all argument and debate.' (Ch.2)"
                " True understanding is not accumulation of information but transformation of perspective."
            )
        elif is_conflict:
            return (
                "Zhuangzi responds to conflict with the relativity of perspectives (齊物論, qiwulun):"
                " each side in a dispute occupies a 'this' position, making the other 'that'."
                " But 'that' also has its own 'this', and from the Dao's perspective,"
                " neither has the final claim."
                " The sage does not take sides (無是非, beyond right and wrong) but sees from"
                " the pivot of the Dao (道樞, daoshu) — the still center from which all perspectives"
                " can be seen without attachment."
                " 'The true man of old did not dream of reversals; he had no anxiety about separations."
                " He could go up high without trembling, into water without getting wet, into fire without"
                " getting burned.' (Ch.6) — the spirit undisturbed by external opposition."
                " Transformation (物化) dissolves all fixed positions eventually; what seems urgent"
                " conflict is just one phase in the Dao's endless transformation."
            )
        elif is_stress:
            return (
                "Zhuangzi's prescription for overwhelm and anxiety: xiaoyaoyou (逍遙遊,"
                " free and easy wandering) — the capacity to move freely without attachment"
                " to outcomes, like the great Peng bird riding the wind for 90,000 li."
                " 'To a mind that is still, the whole universe surrenders.' (Zhuangzi)"
                " Ziran (自然, spontaneous naturalness): anxiety arises from forcing oneself"
                " against one's own nature, like a fish trying to climb a tree."
                " Wu wei (無為): the highest effectiveness comes not from straining effort"
                " but from aligning with the natural flow."
                " The parable of the gnarled tree: the 'useless' tree lives a thousand years"
                " because nothing covets it. Uselessness (無用之用) is the greatest usefulness."
                " Stop trying to be the straight, perfect timber — be the ancient gnarled oak."
            )
        else:
            return (
                "Zhuangzi (莊子, c.369–286 BCE) invites us to dissolve the problem itself."
                " His first chapter, Xiaoyaoyou (逍遙遊, Free and Easy Wandering), opens with"
                " the great Peng bird, whose wings darken the sky as it soars 90,000 li —"
                " while the cicada laughs: 'Why such effort?' Small knowledge cannot fathom great knowledge."
                " Qiwulun (齊物論, Equalization of All Things): all distinctions — right/wrong,"
                " beautiful/ugly, useful/useless — arise from a particular perspective."
                " From the Dao's view, they equalize."
                " Wu wei (無為): the Dao does not strive, yet nothing is left undone."
                " Act from your natural grain, not from social expectation or anxious forcing."
                " Ziran (自然): trust spontaneous naturalness. The Dao is present in all things,"
                " even in the lowliest — 'it is in the ant, in the grass, in dung, in tile-shards.' (Ch.22)"
            )

    def _generate_summary(
        self,
        text: str,
        dao: Dict[str, Any],
        wu_wei: Dict[str, Any],
        ziran: Dict[str, Any],
        qi: Dict[str, Any],
        xiaoyaoyou: Dict[str, Any],
        qiwulun: Dict[str, Any],
        dream: Dict[str, Any],
        transformation: Dict[str, Any],
        uselessness: Dict[str, Any],
    ) -> str:
        """Generate a Daoist summary of the analysis."""
        # Always begin with proactive philosophical application to the actual problem
        parts = [self._apply_zhuangzi_to_problem(text)]

        # Append detected Daoist concepts
        if dao["dao_present"]:
            parts.append("Dao (道, the Way) is explicitly present in this text.")

        if wu_wei["wu_wei_present"]:
            parts.append(
                "Wu wei (無為, effortless action) is embodied — non-forcing in action."
            )

        if ziran["ziran_present"]:
            parts.append(
                "Ziran (自然, naturalness) is expressed — spontaneous and unforced."
            )

        if qi["qi_present"]:
            parts.append(
                "Qi (氣, vital energy) flows through this text's engagement with life."
            )

        if xiaoyaoyou["xiaoyaoyou_present"]:
            parts.append(
                "Xiaoyaoyou (逍遙遊, free wandering) is present — spiritual freedom beyond attachment."
            )

        if qiwulun["qiwulun_present"]:
            parts.append(
                "Qiwulun (齊物論, equality of all things) is embodied — perspectives equalized."
            )

        if dream["dream_reality_present"]:
            parts.append(
                "The boundary between dream and reality is questioned — butterfly dreaming."
            )

        if transformation["transformation_present"]:
            parts.append("Transformation (物化) and constant change are acknowledged.")

        if uselessness["uselessness_theme_present"]:
            parts.append(
                "The paradox of uselessness (無用之用) — the usefulness of the useless — is engaged."
            )

        return " ".join(parts)

    def _calculate_tension(
        self,
        dao: Dict[str, Any],
        wu_wei: Dict[str, Any],
        ziran: Dict[str, Any],
        xiaoyaoyou: Dict[str, Any],
        qiwulun: Dict[str, Any],
        dream: Dict[str, Any],
        transformation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate Daoist tensions in the text."""
        elements = []

        # Tension: wu wei (non-action) vs purposeful activity
        if wu_wei["wu_wei_present"] and not ziran["ziran_present"]:
            elements.append(
                "Wu wei referenced but naturalness (ziran) not fully expressed"
            )
        # Tension: dream vs reality
        if dream["dream_reality_present"]:
            elements.append(
                "Tension between dream and reality — questioning what is real"
            )
        # Tension: freedom (xiaoyaoyou) vs Dao's constraints
        if xiaoyaoyou["xiaoyaoyou_present"] and dao["dao_present"]:
            elements.append("Tension between boundless freedom and following the Dao")
        # Tension: equality of things vs lived distinctions
        if qiwulun["qiwulun_present"] and not transformation["transformation_present"]:
            elements.append(
                "Equality of things affirmed but transformative flow not embraced"
            )
        # Tension: transformation vs stability
        if transformation["transformation_present"] and dao["dao_present"]:
            elements.append(
                "Tension between constant transformation and the enduring Dao"
            )

        n = len(elements)
        if n >= 3:
            level = "High"
            desc = "Multiple Daoist tensions active — the text engages richly with paradox and transformation."
        elif n >= 2:
            level = "Moderate"
            desc = "Some Daoist tensions present — navigating naturalness and freedom."
        elif n >= 1:
            level = "Low"
            desc = "Mild tension within Daoist themes."
        else:
            level = "Very Low"
            desc = "Minimal tension; text flows naturally or shows limited Daoist engagement."
            elements = ["No significant Daoist tensions detected"]

        return {
            "level": level,
            "score": n,
            "description": desc,
            "elements": elements,
        }
