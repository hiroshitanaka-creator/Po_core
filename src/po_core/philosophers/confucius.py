"""
Confucius (Kong Fuzi) Philosopher Module

Confucius (孔子, 551-479 BCE) was a Chinese philosopher and the founder of Confucianism,
one of the most influential philosophical traditions in East Asia.

Key Concepts:
1. Ren (仁) - Benevolence, humaneness, virtue central to Confucian ethics

2. Li (礼) - Ritual propriety, proper conduct, etiquette and ceremony

3. Yi (義) - Righteousness, moral disposition to do good

4. Xiao (孝) - Filial piety, respect for parents and ancestors

5. Junzi (君子) - The exemplary person, the gentleman of virtue

6. Zhong (忠) - Loyalty, conscientiousness

7. Shu (恕) - Reciprocity, empathy ("Do not impose on others what you do not wish for yourself")

8. De (德) - Virtue, moral character, integrity

9. Tianming (天命) - Mandate of Heaven, cosmic moral order

10. Wen (文) - Culture, learning, refinement through education
"""

from typing import Any, Dict

from po_core.philosophers.base import Philosopher


class Confucius(Philosopher):
    """
    Confucius (Kong Fuzi): Founder of Confucianism emphasizing virtue, ritual, and social harmony.

    Confucian philosophy centers on ethical self-cultivation, proper relationships,
    and the development of moral character through learning and practice of rituals.
    """

    def __init__(self):
        super().__init__(
            name="Confucius (孔子)",
            description="Confucian philosophy emphasizing ren (benevolence), li (ritual propriety), and the cultivation of virtue through learning and proper relationships"
        )

    def reason(self, text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Analyze text through Confucian philosophy.

        Args:
            text: The text to analyze
            context: Optional context dictionary

        Returns:
            Dictionary containing Confucian analysis
        """
        ren = self._assess_ren(text)
        li = self._assess_li(text)
        yi = self._assess_yi(text)
        xiao = self._assess_xiao(text)
        junzi = self._assess_junzi(text)
        zhong_shu = self._assess_zhong_shu(text)
        de = self._assess_de(text)
        tianming = self._assess_tianming(text)
        learning = self._assess_learning(text)

        return {
            "philosopher": self.name,
            "description": self.description,
            "analysis": {
                "ren_benevolence": ren,
                "li_ritual_propriety": li,
                "yi_righteousness": yi,
                "xiao_filial_piety": xiao,
                "junzi_exemplary_person": junzi,
                "zhong_shu_loyalty_reciprocity": zhong_shu,
                "de_virtue": de,
                "tianming_mandate": tianming,
                "learning_cultivation": learning
            },
            "summary": self._generate_summary(
                ren, li, yi, xiao, junzi, zhong_shu, de, tianming, learning
            )
        }

    def _assess_ren(self, text: str) -> Dict[str, Any]:
        """
        Assess Ren (仁) - Benevolence, humaneness.

        Ren is the supreme virtue in Confucianism - love, compassion,
        and care for others. It is the foundation of all virtues.
        """
        text_lower = text.lower()

        ren_words = [
            "benevolence", "benevolent", "compassion", "compassionate",
            "humanity", "humane", "kindness", "kind", "care", "caring",
            "love", "loving", "empathy", "empathetic", "goodness",
            "altruism", "generosity", "generous", "warmth", "tender"
        ]

        has_ren = sum(1 for word in ren_words if word in text_lower)
        ren_present = has_ren >= 2

        return {
            "ren_present": ren_present,
            "score": has_ren,
            "interpretation": "Text embodies ren - benevolence and humaneness toward others, the supreme Confucian virtue." if ren_present else "Limited expression of ren or benevolence."
        }

    def _assess_li(self, text: str) -> Dict[str, Any]:
        """
        Assess Li (礼) - Ritual propriety, proper conduct.

        Li encompasses rituals, ceremonies, etiquette, and proper behavior
        according to social roles and relationships.
        """
        text_lower = text.lower()

        li_words = [
            "ritual", "ceremony", "propriety", "proper", "etiquette",
            "manners", "decorum", "protocol", "custom", "tradition",
            "formality", "respect", "respectful", "courtesy", "polite",
            "behavior", "conduct", "appropriate", "fitting", "reverence"
        ]

        has_li = sum(1 for word in li_words if word in text_lower)
        li_present = has_li >= 2

        return {
            "li_present": li_present,
            "score": has_li,
            "interpretation": "Text emphasizes li - ritual propriety and proper conduct according to social roles." if li_present else "Limited emphasis on ritual propriety or proper conduct."
        }

    def _assess_yi(self, text: str) -> Dict[str, Any]:
        """
        Assess Yi (義) - Righteousness, moral disposition.

        Yi is the moral sense to do what is right, justice, and
        appropriateness in moral action.
        """
        text_lower = text.lower()

        yi_words = [
            "righteous", "righteousness", "justice", "just", "moral",
            "morality", "right", "ethical", "ethics", "principle",
            "principled", "integrity", "upright", "honorable", "duty",
            "obligation", "ought", "should", "correct", "proper"
        ]

        has_yi = sum(1 for word in yi_words if word in text_lower)
        yi_present = has_yi >= 2

        return {
            "yi_present": yi_present,
            "score": has_yi,
            "interpretation": "Text demonstrates yi - righteousness and moral commitment to what is right." if yi_present else "Limited expression of righteousness or moral principle."
        }

    def _assess_xiao(self, text: str) -> Dict[str, Any]:
        """
        Assess Xiao (孝) - Filial piety.

        Xiao is respect, obedience, and care for parents and ancestors,
        fundamental to Confucian family and social order.
        """
        text_lower = text.lower()

        xiao_words = [
            "filial", "piety", "parent", "parents", "father", "mother",
            "family", "ancestor", "ancestors", "elder", "elders",
            "respect", "honor", "obedience", "duty", "devotion",
            "care", "serve", "revere", "reverence"
        ]

        has_xiao = sum(1 for word in xiao_words if word in text_lower)
        xiao_present = has_xiao >= 3

        return {
            "xiao_present": xiao_present,
            "score": has_xiao,
            "interpretation": "Text expresses xiao - filial piety and respect for parents and ancestors." if xiao_present else "Limited emphasis on filial piety or family reverence."
        }

    def _assess_junzi(self, text: str) -> Dict[str, Any]:
        """
        Assess Junzi (君子) - The exemplary person, the gentleman.

        The junzi is the Confucian ideal of a morally cultivated person
        who embodies virtue, learning, and proper conduct.
        """
        text_lower = text.lower()

        junzi_words = [
            "exemplary", "gentleman", "noble", "superior", "virtuous",
            "cultivated", "refined", "cultivate", "self-improvement",
            "worthy", "excellence", "character", "moral", "integrity",
            "wisdom", "wise", "sage", "model", "ideal", "leader"
        ]

        has_junzi = sum(1 for word in junzi_words if word in text_lower)
        junzi_present = has_junzi >= 2

        return {
            "junzi_present": junzi_present,
            "score": has_junzi,
            "interpretation": "Text reflects the ideal of junzi - the exemplary person of virtue and cultivation." if junzi_present else "Limited reference to the exemplary person or moral ideal."
        }

    def _assess_zhong_shu(self, text: str) -> Dict[str, Any]:
        """
        Assess Zhong (忠) and Shu (恕) - Loyalty and Reciprocity.

        Zhong is loyalty and conscientiousness. Shu is reciprocity and empathy -
        the negative golden rule: "Do not impose on others what you do not wish for yourself."
        """
        text_lower = text.lower()

        zhong_words = [
            "loyal", "loyalty", "faithful", "faithfulness", "devotion",
            "dedicated", "dedication", "commitment", "committed", "conscientious"
        ]

        shu_words = [
            "reciprocity", "empathy", "golden rule", "treat others",
            "consideration", "understanding", "mutual", "respect",
            "others", "sympathy", "compassion", "fellow"
        ]

        has_zhong = sum(1 for word in zhong_words if word in text_lower)
        has_shu = sum(1 for word in shu_words if word in text_lower)

        return {
            "zhong_loyalty_present": has_zhong >= 1,
            "shu_reciprocity_present": has_shu >= 2,
            "zhong_score": has_zhong,
            "shu_score": has_shu,
            "interpretation": self._interpret_zhong_shu(has_zhong, has_shu)
        }

    def _interpret_zhong_shu(self, zhong: int, shu: int) -> str:
        """Interpret zhong and shu."""
        if zhong >= 1 and shu >= 2:
            return "Text embodies both zhong (loyalty) and shu (reciprocity) - commitment and empathetic consideration."
        elif zhong >= 1:
            return "Text emphasizes zhong - loyalty and conscientious commitment."
        elif shu >= 2:
            return "Text emphasizes shu - reciprocity and empathetic treatment of others."
        else:
            return "Limited emphasis on loyalty or reciprocity."

    def _assess_de(self, text: str) -> Dict[str, Any]:
        """
        Assess De (德) - Virtue, moral character, integrity.

        De is the inner moral power and character that enables one to
        lead and influence others through example rather than force.
        """
        text_lower = text.lower()

        de_words = [
            "virtue", "virtuous", "character", "integrity", "moral",
            "goodness", "excellence", "quality", "upright", "honorable",
            "worthy", "meritorious", "exemplary", "noble", "ethical"
        ]

        has_de = sum(1 for word in de_words if word in text_lower)
        de_present = has_de >= 2

        return {
            "de_present": de_present,
            "score": has_de,
            "interpretation": "Text emphasizes de - virtue and moral character that leads through example." if de_present else "Limited emphasis on virtue or moral character."
        }

    def _assess_tianming(self, text: str) -> Dict[str, Any]:
        """
        Assess Tianming (天命) - Mandate of Heaven.

        The cosmic moral order and the idea that legitimate authority
        comes from alignment with Heaven's will and moral virtue.
        """
        text_lower = text.lower()

        tianming_words = [
            "heaven", "heavenly", "cosmic", "mandate", "destiny",
            "fate", "divine", "sacred", "order", "moral order",
            "will of heaven", "legitimacy", "authority", "decree"
        ]

        has_tianming = sum(1 for word in tianming_words if word in text_lower)
        tianming_present = has_tianming >= 2

        return {
            "tianming_present": tianming_present,
            "score": has_tianming,
            "interpretation": "Text references tianming - the Mandate of Heaven and cosmic moral order." if tianming_present else "Limited reference to Heaven's mandate or cosmic order."
        }

    def _assess_learning(self, text: str) -> Dict[str, Any]:
        """
        Assess learning and self-cultivation (學).

        Confucianism emphasizes continuous learning, study of classics,
        and self-cultivation through education and practice.
        """
        text_lower = text.lower()

        learning_words = [
            "learn", "learning", "study", "education", "educate",
            "teach", "teaching", "knowledge", "cultivate", "cultivation",
            "practice", "self-improvement", "develop", "development",
            "refine", "refinement", "grow", "growth", "wisdom", "scholar"
        ]

        has_learning = sum(1 for word in learning_words if word in text_lower)
        learning_present = has_learning >= 2

        return {
            "learning_present": learning_present,
            "score": has_learning,
            "interpretation": "Text emphasizes learning and self-cultivation through study and practice." if learning_present else "Limited emphasis on learning or self-cultivation."
        }

    def _generate_summary(
        self,
        ren: Dict[str, Any],
        li: Dict[str, Any],
        yi: Dict[str, Any],
        xiao: Dict[str, Any],
        junzi: Dict[str, Any],
        zhong_shu: Dict[str, Any],
        de: Dict[str, Any],
        tianming: Dict[str, Any],
        learning: Dict[str, Any]
    ) -> str:
        """Generate a Confucian summary of the analysis."""
        parts = []

        if ren["ren_present"]:
            parts.append("Text embodies ren (benevolence) - the supreme Confucian virtue.")

        if li["li_present"]:
            parts.append("It emphasizes li (ritual propriety) and proper conduct.")

        if yi["yi_present"]:
            parts.append("It demonstrates yi (righteousness) and moral principle.")

        if xiao["xiao_present"]:
            parts.append("It expresses xiao (filial piety) toward family and ancestors.")

        if junzi["junzi_present"]:
            parts.append("It reflects the ideal of the junzi - the exemplary person.")

        if zhong_shu["zhong_loyalty_present"] or zhong_shu["shu_reciprocity_present"]:
            parts.append(zhong_shu["interpretation"])

        if de["de_present"]:
            parts.append("It emphasizes de (virtue) and moral character.")

        if tianming["tianming_present"]:
            parts.append("It references the Mandate of Heaven and cosmic moral order.")

        if learning["learning_present"]:
            parts.append("It values learning and self-cultivation.")

        if not parts:
            parts.append("Text shows limited engagement with core Confucian values.")

        return " ".join(parts)
