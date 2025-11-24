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
            description="Daoist philosophy emphasizing naturalness (ziran), non-action (wu wei), spiritual freedom (xiaoyaoyou), and the relativity of perspectives"
        )

    def reason(self, text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
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

        return {
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
                "uselessness": uselessness
            },
            "summary": self._generate_summary(
                dao, wu_wei, ziran, qi, xiaoyaoyou, qiwulun,
                dream, transformation, uselessness
            )
        }

    def _assess_dao(self, text: str) -> Dict[str, Any]:
        """
        Assess Dao (道) - The Way.

        The Dao is the natural order, the way of nature, the pattern
        underlying all existence. It is nameless, ineffable, and spontaneous.
        """
        text_lower = text.lower()

        dao_words = [
            "way", "path", "dao", "tao", "nature", "natural order",
            "flow", "cosmic", "ultimate", "underlying", "pattern",
            "nameless", "ineffable", "source", "origin", "mystery"
        ]

        has_dao = sum(1 for word in dao_words if word in text_lower)
        dao_present = has_dao >= 2

        return {
            "dao_present": dao_present,
            "score": has_dao,
            "interpretation": "Text references the Dao - the natural Way and cosmic order underlying all things." if dao_present else "Limited reference to the Dao or natural Way."
        }

    def _assess_wu_wei(self, text: str) -> Dict[str, Any]:
        """
        Assess Wu Wei (無為) - Non-action, effortless action.

        Wu wei is acting without forcing, following the natural flow,
        achieving through non-striving, doing by not-doing.
        """
        text_lower = text.lower()

        wu_wei_words = [
            "effortless", "non-action", "wu wei", "without forcing",
            "natural", "spontaneous", "flow", "ease", "not striving",
            "let go", "allow", "yield", "soft", "gentle",
            "without effort", "unforced", "natural way", "non-doing"
        ]

        has_wu_wei = sum(1 for word in wu_wei_words if word in text_lower)
        wu_wei_present = has_wu_wei >= 2

        return {
            "wu_wei_present": wu_wei_present,
            "score": has_wu_wei,
            "interpretation": "Text embodies wu wei - effortless action and non-forcing, following the natural flow." if wu_wei_present else "Limited expression of non-action or effortless way."
        }

    def _assess_ziran(self, text: str) -> Dict[str, Any]:
        """
        Assess Ziran (自然) - Naturalness, spontaneity.

        Ziran means "so of itself" - naturalness, spontaneity,
        being what one is without artifice or contrivance.
        """
        text_lower = text.lower()

        ziran_words = [
            "natural", "spontaneous", "authentic", "genuine",
            "unaffected", "simple", "simplicity", "organic",
            "innate", "inherent", "uncontrived", "artless",
            "free", "unforced", "self-so", "naturally"
        ]

        has_ziran = sum(1 for word in ziran_words if word in text_lower)
        ziran_present = has_ziran >= 2

        return {
            "ziran_present": ziran_present,
            "score": has_ziran,
            "interpretation": "Text expresses ziran - naturalness and spontaneity, being so of itself." if ziran_present else "Limited expression of naturalness or spontaneity."
        }

    def _assess_qi(self, text: str) -> Dict[str, Any]:
        """
        Assess Qi (氣) - Vital energy, life force.

        Qi is the vital breath, energy that animates all living things,
        the dynamic force flowing through the universe.
        """
        text_lower = text.lower()

        qi_words = [
            "energy", "vital", "breath", "life force", "spirit",
            "vitality", "animate", "living", "dynamic", "force",
            "flow", "chi", "qi", "power", "essence"
        ]

        has_qi = sum(1 for word in qi_words if word in text_lower)
        qi_present = has_qi >= 2

        return {
            "qi_present": qi_present,
            "score": has_qi,
            "interpretation": "Text references qi - vital energy and life force flowing through all things." if qi_present else "Limited reference to vital energy or life force."
        }

    def _assess_xiaoyaoyou(self, text: str) -> Dict[str, Any]:
        """
        Assess Xiaoyaoyou (逍遙遊) - Free and easy wandering.

        Xiaoyaoyou is spiritual freedom, unencumbered wandering,
        liberation from worldly constraints and conventions.
        """
        text_lower = text.lower()

        xiaoyaoyou_words = [
            "freedom", "free", "wander", "wandering", "liberated",
            "unencumbered", "roam", "soar", "fly", "limitless",
            "boundless", "unconstrained", "at ease", "carefree",
            "unfettered", "unrestricted", "liberty", "transcend"
        ]

        has_xiaoyaoyou = sum(1 for word in xiaoyaoyou_words if word in text_lower)
        xiaoyaoyou_present = has_xiaoyaoyou >= 2

        return {
            "xiaoyaoyou_present": xiaoyaoyou_present,
            "score": has_xiaoyaoyou,
            "interpretation": "Text expresses xiaoyaoyou - free and easy wandering, spiritual freedom." if xiaoyaoyou_present else "Limited expression of spiritual freedom or wandering."
        }

    def _assess_qiwulun(self, text: str) -> Dict[str, Any]:
        """
        Assess Qiwulun (齊物論) - Equality of things, relativism.

        Qiwulun is the relativity of perspectives, the equality of all things,
        questioning fixed distinctions and conventional judgments.
        """
        text_lower = text.lower()

        qiwulun_words = [
            "relative", "relativity", "perspective", "viewpoint",
            "equal", "equality", "same", "different", "distinction",
            "judgment", "conventional", "question", "doubt",
            "depends", "context", "standpoint", "point of view"
        ]

        has_qiwulun = sum(1 for word in qiwulun_words if word in text_lower)
        qiwulun_present = has_qiwulun >= 3

        return {
            "qiwulun_present": qiwulun_present,
            "score": has_qiwulun,
            "interpretation": "Text expresses qiwulun - relativity of perspectives and equality of things." if qiwulun_present else "Limited expression of relativism or equality of perspectives."
        }

    def _assess_dream_reality(self, text: str) -> Dict[str, Any]:
        """
        Assess dream and reality theme.

        Zhuangzi's butterfly dream questions the distinction between
        dreaming and waking, reality and illusion.
        """
        text_lower = text.lower()

        dream_words = [
            "dream", "dreaming", "illusion", "real", "reality",
            "butterfly", "awake", "waking", "sleep", "sleeping",
            "imagination", "fantasy", "appearance", "true", "false"
        ]

        has_dream = sum(1 for word in dream_words if word in text_lower)
        dream_present = has_dream >= 3

        return {
            "dream_reality_present": dream_present,
            "score": has_dream,
            "interpretation": "Text questions the distinction between dream and reality, appearance and truth." if dream_present else "Limited engagement with dream/reality theme."
        }

    def _assess_transformation(self, text: str) -> Dict[str, Any]:
        """
        Assess transformation (化).

        Everything transforms constantly - birth, death, and change
        are natural processes to be accepted rather than feared.
        """
        text_lower = text.lower()

        transformation_words = [
            "transform", "transformation", "change", "changing",
            "become", "becoming", "evolve", "evolution", "metamorphosis",
            "transition", "shift", "convert", "alter", "mutation",
            "impermanence", "flux", "flow", "process"
        ]

        has_transformation = sum(1 for word in transformation_words if word in text_lower)
        transformation_present = has_transformation >= 2

        return {
            "transformation_present": transformation_present,
            "score": has_transformation,
            "interpretation": "Text acknowledges transformation - the constant change and flow of all things." if transformation_present else "Limited recognition of transformation or change."
        }

    def _assess_uselessness(self, text: str) -> Dict[str, Any]:
        """
        Assess the usefulness of uselessness.

        Zhuangzi values what appears useless - the gnarled tree
        survives because it has no practical use. Usefulness can be limiting.
        """
        text_lower = text.lower()

        uselessness_words = [
            "useless", "uselessness", "no use", "purpose", "practical",
            "utility", "functional", "value", "worthless", "pointless"
        ]

        # Check for themes of finding value in the useless
        paradox_phrases = [
            "useless", "no purpose", "no use", "worthless",
            "impractical", "serves no"
        ]

        has_uselessness = sum(1 for word in uselessness_words if word in text_lower)
        has_paradox = sum(1 for phrase in paradox_phrases if phrase in text_lower)

        uselessness_present = has_uselessness >= 2

        return {
            "uselessness_theme_present": uselessness_present,
            "score": has_uselessness,
            "interpretation": "Text engages with the paradox of usefulness - what appears useless may have deeper value." if uselessness_present else "Limited engagement with usefulness/uselessness theme."
        }

    def _generate_summary(
        self,
        dao: Dict[str, Any],
        wu_wei: Dict[str, Any],
        ziran: Dict[str, Any],
        qi: Dict[str, Any],
        xiaoyaoyou: Dict[str, Any],
        qiwulun: Dict[str, Any],
        dream: Dict[str, Any],
        transformation: Dict[str, Any],
        uselessness: Dict[str, Any]
    ) -> str:
        """Generate a Daoist summary of the analysis."""
        parts = []

        if dao["dao_present"]:
            parts.append("Text references the Dao - the natural Way underlying all things.")

        if wu_wei["wu_wei_present"]:
            parts.append("It embodies wu wei - effortless action and non-forcing.")

        if ziran["ziran_present"]:
            parts.append("It expresses ziran - naturalness and spontaneity.")

        if qi["qi_present"]:
            parts.append("It references qi - vital energy flowing through existence.")

        if xiaoyaoyou["xiaoyaoyou_present"]:
            parts.append("It expresses xiaoyaoyou - free and easy wandering, spiritual freedom.")

        if qiwulun["qiwulun_present"]:
            parts.append("It embodies qiwulun - relativity of perspectives and equality of things.")

        if dream["dream_reality_present"]:
            parts.append("It questions the distinction between dream and reality.")

        if transformation["transformation_present"]:
            parts.append("It acknowledges transformation and constant change.")

        if uselessness["uselessness_theme_present"]:
            parts.append("It engages with the paradox of usefulness and uselessness.")

        if not parts:
            parts.append("Text shows limited engagement with core Daoist themes.")

        return " ".join(parts)
