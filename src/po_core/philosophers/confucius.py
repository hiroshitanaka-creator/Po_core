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
            description="Confucian philosophy emphasizing ren (benevolence), li (ritual propriety), and the cultivation of virtue through learning and proper relationships",
        )
        self.tradition = "Confucianism"
        self.key_concepts = [
            "ren (benevolence)",
            "li (ritual propriety)",
            "junzi (exemplary person)",
            "xiao (filial piety)",
            "zhongyong (doctrine of the mean)",
        ]

    def reason(
        self, text: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
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

        summary = self._generate_summary(
            text, ren, li, yi, xiao, junzi, zhong_shu, de, tianming, learning
        )
        tension = self._calculate_tension(
            ren, li, yi, xiao, junzi, zhong_shu, de, tianming, learning
        )

        return {
            # Standard contract keys
            "reasoning": summary,
            "perspective": "Confucian Ethics / Virtue Cultivation",
            "tension": tension,
            "metadata": {"philosopher": self.name},
            # Philosopher-specific concept analyses
            "ren_benevolence": ren,
            "li_ritual_propriety": li,
            "yi_righteousness": yi,
            "xiao_filial_piety": xiao,
            "junzi_exemplary_person": junzi,
            "zhong_shu_loyalty_reciprocity": zhong_shu,
            "de_virtue": de,
            "tianming_mandate": tianming,
            "learning_cultivation": learning,
            # Backward-compat keys (used by existing tests)
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
                "learning_cultivation": learning,
            },
            "summary": summary,
        }

    def _assess_ren(self, text: str) -> Dict[str, Any]:
        """
        Assess Ren (仁) - Benevolence, humaneness.

        Ren is the supreme virtue in Confucianism - love, compassion,
        and care for others. It is the foundation of all virtues.
        """
        text_lower = text.lower()

        ren_words = [
            "benevolence",
            "benevolent",
            "compassion",
            "compassionate",
            "humanity",
            "humane",
            "kindness",
            "kind",
            "care",
            "caring",
            "love",
            "loving",
            "empathy",
            "empathetic",
            "goodness",
            "altruism",
            "generosity",
            "generous",
            "warmth",
            "tender",
        ]

        has_ren = sum(1 for word in ren_words if word in text_lower)
        ren_present = has_ren >= 2

        return {
            "ren_present": ren_present,
            "score": has_ren,
            "interpretation": (
                "Text embodies ren - benevolence and humaneness toward others, the supreme Confucian virtue."
                if ren_present
                else "Limited expression of ren or benevolence."
            ),
        }

    def _assess_li(self, text: str) -> Dict[str, Any]:
        """
        Assess Li (礼) - Ritual propriety, proper conduct.

        Li encompasses rituals, ceremonies, etiquette, and proper behavior
        according to social roles and relationships.
        """
        text_lower = text.lower()

        li_words = [
            "ritual",
            "ceremony",
            "propriety",
            "proper",
            "etiquette",
            "manners",
            "decorum",
            "protocol",
            "custom",
            "tradition",
            "formality",
            "respect",
            "respectful",
            "courtesy",
            "polite",
            "behavior",
            "conduct",
            "appropriate",
            "fitting",
            "reverence",
        ]

        has_li = sum(1 for word in li_words if word in text_lower)
        li_present = has_li >= 2

        return {
            "li_present": li_present,
            "score": has_li,
            "interpretation": (
                "Text emphasizes li - ritual propriety and proper conduct according to social roles."
                if li_present
                else "Limited emphasis on ritual propriety or proper conduct."
            ),
        }

    def _assess_yi(self, text: str) -> Dict[str, Any]:
        """
        Assess Yi (義) - Righteousness, moral disposition.

        Yi is the moral sense to do what is right, justice, and
        appropriateness in moral action.
        """
        text_lower = text.lower()

        yi_words = [
            "righteous",
            "righteousness",
            "justice",
            "just",
            "moral",
            "morality",
            "right",
            "ethical",
            "ethics",
            "principle",
            "principled",
            "integrity",
            "upright",
            "honorable",
            "duty",
            "obligation",
            "ought",
            "should",
            "correct",
            "proper",
        ]

        has_yi = sum(1 for word in yi_words if word in text_lower)
        yi_present = has_yi >= 2

        return {
            "yi_present": yi_present,
            "score": has_yi,
            "interpretation": (
                "Text demonstrates yi - righteousness and moral commitment to what is right."
                if yi_present
                else "Limited expression of righteousness or moral principle."
            ),
        }

    def _assess_xiao(self, text: str) -> Dict[str, Any]:
        """
        Assess Xiao (孝) - Filial piety.

        Xiao is respect, obedience, and care for parents and ancestors,
        fundamental to Confucian family and social order.
        """
        text_lower = text.lower()

        xiao_words = [
            "filial",
            "piety",
            "parent",
            "parents",
            "father",
            "mother",
            "family",
            "ancestor",
            "ancestors",
            "elder",
            "elders",
            "respect",
            "honor",
            "obedience",
            "duty",
            "devotion",
            "care",
            "serve",
            "revere",
            "reverence",
        ]

        has_xiao = sum(1 for word in xiao_words if word in text_lower)
        xiao_present = has_xiao >= 3

        return {
            "xiao_present": xiao_present,
            "score": has_xiao,
            "interpretation": (
                "Text expresses xiao - filial piety and respect for parents and ancestors."
                if xiao_present
                else "Limited emphasis on filial piety or family reverence."
            ),
        }

    def _assess_junzi(self, text: str) -> Dict[str, Any]:
        """
        Assess Junzi (君子) - The exemplary person, the gentleman.

        The junzi is the Confucian ideal of a morally cultivated person
        who embodies virtue, learning, and proper conduct.
        """
        text_lower = text.lower()

        junzi_words = [
            "exemplary",
            "gentleman",
            "noble",
            "superior",
            "virtuous",
            "cultivated",
            "refined",
            "cultivate",
            "self-improvement",
            "worthy",
            "excellence",
            "character",
            "moral",
            "integrity",
            "wisdom",
            "wise",
            "sage",
            "model",
            "ideal",
            "leader",
        ]

        has_junzi = sum(1 for word in junzi_words if word in text_lower)
        junzi_present = has_junzi >= 2

        return {
            "junzi_present": junzi_present,
            "score": has_junzi,
            "interpretation": (
                "Text reflects the ideal of junzi - the exemplary person of virtue and cultivation."
                if junzi_present
                else "Limited reference to the exemplary person or moral ideal."
            ),
        }

    def _assess_zhong_shu(self, text: str) -> Dict[str, Any]:
        """
        Assess Zhong (忠) and Shu (恕) - Loyalty and Reciprocity.

        Zhong is loyalty and conscientiousness. Shu is reciprocity and empathy -
        the negative golden rule: "Do not impose on others what you do not wish for yourself."
        """
        text_lower = text.lower()

        zhong_words = [
            "loyal",
            "loyalty",
            "faithful",
            "faithfulness",
            "devotion",
            "dedicated",
            "dedication",
            "commitment",
            "committed",
            "conscientious",
        ]

        shu_words = [
            "reciprocity",
            "empathy",
            "golden rule",
            "treat others",
            "consideration",
            "understanding",
            "mutual",
            "respect",
            "others",
            "sympathy",
            "compassion",
            "fellow",
        ]

        has_zhong = sum(1 for word in zhong_words if word in text_lower)
        has_shu = sum(1 for word in shu_words if word in text_lower)

        return {
            "zhong_loyalty_present": has_zhong >= 1,
            "shu_reciprocity_present": has_shu >= 2,
            "zhong_score": has_zhong,
            "shu_score": has_shu,
            "interpretation": self._interpret_zhong_shu(has_zhong, has_shu),
        }

    def _interpret_zhong_shu(self, zhong: int, shu: int) -> str:
        """Interpret zhong and shu."""
        if zhong >= 1 and shu >= 2:
            return "Text embodies both zhong (loyalty) and shu (reciprocity) - commitment and empathetic consideration."
        elif zhong >= 1:
            return "Text emphasizes zhong - loyalty and conscientious commitment."
        elif shu >= 2:
            return (
                "Text emphasizes shu - reciprocity and empathetic treatment of others."
            )
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
            "virtue",
            "virtuous",
            "character",
            "integrity",
            "moral",
            "goodness",
            "excellence",
            "quality",
            "upright",
            "honorable",
            "worthy",
            "meritorious",
            "exemplary",
            "noble",
            "ethical",
        ]

        has_de = sum(1 for word in de_words if word in text_lower)
        de_present = has_de >= 2

        return {
            "de_present": de_present,
            "score": has_de,
            "interpretation": (
                "Text emphasizes de - virtue and moral character that leads through example."
                if de_present
                else "Limited emphasis on virtue or moral character."
            ),
        }

    def _assess_tianming(self, text: str) -> Dict[str, Any]:
        """
        Assess Tianming (天命) - Mandate of Heaven.

        The cosmic moral order and the idea that legitimate authority
        comes from alignment with Heaven's will and moral virtue.
        """
        text_lower = text.lower()

        tianming_words = [
            "heaven",
            "heavenly",
            "cosmic",
            "mandate",
            "destiny",
            "fate",
            "divine",
            "sacred",
            "order",
            "moral order",
            "will of heaven",
            "legitimacy",
            "authority",
            "decree",
        ]

        has_tianming = sum(1 for word in tianming_words if word in text_lower)
        tianming_present = has_tianming >= 2

        return {
            "tianming_present": tianming_present,
            "score": has_tianming,
            "interpretation": (
                "Text references tianming - the Mandate of Heaven and cosmic moral order."
                if tianming_present
                else "Limited reference to Heaven's mandate or cosmic order."
            ),
        }

    def _assess_learning(self, text: str) -> Dict[str, Any]:
        """
        Assess learning and self-cultivation (學).

        Confucianism emphasizes continuous learning, study of classics,
        and self-cultivation through education and practice.
        """
        text_lower = text.lower()

        learning_words = [
            "learn",
            "learning",
            "study",
            "education",
            "educate",
            "teach",
            "teaching",
            "knowledge",
            "cultivate",
            "cultivation",
            "practice",
            "self-improvement",
            "develop",
            "development",
            "refine",
            "refinement",
            "grow",
            "growth",
            "wisdom",
            "scholar",
        ]

        has_learning = sum(1 for word in learning_words if word in text_lower)
        learning_present = has_learning >= 2

        return {
            "learning_present": learning_present,
            "score": has_learning,
            "interpretation": (
                "Text emphasizes learning and self-cultivation through study and practice."
                if learning_present
                else "Limited emphasis on learning or self-cultivation."
            ),
        }

    def _apply_confucian_to_problem(self, text: str) -> str:
        """
        Proactively apply Confucian philosophy to any problem type.

        Confucius's ethics center on ren (仁/benevolence), li (禮/ritual propriety),
        yi (義/righteousness), junzi (君子/exemplary person), and continuous self-cultivation.
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
        is_leadership = any(
            w in text_lower
            for w in [
                "leader",
                "manage",
                "govern",
                "organization",
                "team",
                "authority",
                "power",
                "政治",
                "リーダー",
                "組織",
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
            ]
        )
        is_conflict = any(
            w in text_lower
            for w in [
                "conflict",
                "dispute",
                "war",
                "violence",
                "disagree",
                "opposition",
                "紛争",
                "対立",
                "争い",
            ]
        )
        is_relationship = any(
            w in text_lower
            for w in [
                "relationship",
                "family",
                "friend",
                "trust",
                "love",
                "parent",
                "child",
                "関係",
                "家族",
                "友情",
                "信頼",
            ]
        )

        if is_decision:
            return (
                "Confucius teaches: 'The exemplary person (君子, junzi) acts from righteousness (義, yi),"
                " not from profit (利, li).' Before asking 'which option is better?', ask:"
                " 'Which path allows me to cultivate ren (仁, benevolence) and maintain integrity?'"
                " The rectification of names (正名, zhengming) demands clarity about what this decision"
                " truly is — its real moral weight, not just its practical consequences."
                " 'When you know a thing, hold that you know it; when you do not know a thing,"
                " allow that you do not know it — this is knowledge.' (Analects 2.17)"
                " Self-cultivation (修身) is the foundation: a decision made from cultivated character"
                " will be sound; one made from fear or desire alone will not."
            )
        elif is_leadership:
            return (
                "Confucius on governance and leadership: 'If you lead with virtue (德, de),"
                " the people will gather around you like stars around the North Star.' (Analects 2.1)"
                " The exemplary person (君子, junzi) leads not through coercion but through moral example."
                " Zhengming (正名, rectification of names): leaders must ensure words correspond to reality —"
                " if names are not correct, speech will not accord with truth, and affairs cannot be accomplished."
                " Ren (仁, benevolence) in leadership means: 'Do not impose on others what you yourself"
                " do not want.' (Analects 12.2 — the Golden Rule of Confucian ethics)"
                " True authority comes from earned moral credibility (信, xin), not from position alone."
            )
        elif is_technology:
            return (
                "Confucius would examine technology through the lens of ren (仁) and li (禮):"
                " Does this technology help humans cultivate virtue and right relationships,"
                " or does it erode them?"
                " The five constants (五常: ren仁, yi義, li禮, zhi智, xin信) provide the ethical framework:"
                " a technology must serve benevolence, righteousness, proper conduct, wisdom, and trustworthiness."
                " The rectification of names (正名, zhengming) demands we be precise: is this tool"
                " genuinely 'intelligent', genuinely 'helpful', genuinely 'safe'?"
                " Confucius valued learning (學) and reflection (思) in equal measure:"
                " 'Learning without thought is labor lost; thought without learning is perilous.' (Analects 2.15)"
                " Technology embodies learning without wisdom unless human reflection guides its use."
            )
        elif is_conflict:
            return (
                "Confucius addresses conflict through zhong-shu (忠恕 — loyalty and reciprocity):"
                " 'Do not impose on others what you yourself do not want.' (Analects 12.2)"
                " Before engaging conflict, the junzi (君子) practices self-examination (内省):"
                " 'I daily examine myself on three points: whether I am faithful in doing business"
                " for others, sincere with friends, and have mastered what I have been taught.' (Analects 1.4)"
                " Li (禮, ritual propriety) provides the framework for transforming conflict into dialogue:"
                " proper forms of address, proper procedure, proper humility."
                " Yi (義, righteousness) demands we ask not 'who wins?' but 'what is just?'"
                " Harmony (和, he) is the highest achievement of ritual propriety — not uniformity, but"
                " the harmony that emerges from properly ordered relationships."
            )
        elif is_relationship:
            return (
                "Confucius places human relationships at the center of all ethics through the Five Relationships"
                " (五倫: ruler-minister, parent-child, husband-wife, elder-younger, friend-friend)."
                " Each relationship carries mutual obligations grounded in ren (仁, benevolence)."
                " Xiao (孝, filial piety) — reverence for parents and ancestors — is the root of ren:"
                " 'Filial piety and fraternal submission! Are they not the root of all benevolent actions?' (Analects 1.2)"
                " Zhong-shu (忠恕): be loyal and faithful in your obligations; extend to others"
                " the same consideration you desire for yourself."
                " The junzi (君子) cultivates relationships through continuous self-improvement,"
                " not through demanding change from others first."
                " 'Expect much of yourself, little of others — resentment is kept far away.' (Analects 15.15)"
            )
        else:
            return (
                "Confucius (孔子, 551–479 BCE) teaches that all wisdom begins with ren (仁, benevolence)"
                " — the capacity for human-heartedness, for genuine care and relationship."
                " 'Is he not a man of complete virtue, who feels no discomposure though men may take no note of him?' (Analects 1.1)"
                " The exemplary person (君子, junzi) is not defined by birth or status, but by ceaseless"
                " self-cultivation (修身) through learning, reflection, and virtuous action."
                " Li (禮, ritual propriety) gives form to ren: the right action at the right time,"
                " in the right relationship, with the right intention."
                " Yi (義, righteousness) demands we act from principle, not from calculation of gain."
                " 'At fifteen, I had my mind bent on learning. At thirty, I stood firm."
                " At forty, I had no doubts... At seventy, I could follow what my heart desired"
                " without transgressing what was right.' (Analects 2.4) — the life of cultivation."
            )

    def _generate_summary(
        self,
        text: str,
        ren: Dict[str, Any],
        li: Dict[str, Any],
        yi: Dict[str, Any],
        xiao: Dict[str, Any],
        junzi: Dict[str, Any],
        zhong_shu: Dict[str, Any],
        de: Dict[str, Any],
        tianming: Dict[str, Any],
        learning: Dict[str, Any],
    ) -> str:
        """Generate a Confucian summary of the analysis."""
        # Always begin with proactive philosophical application to the actual problem
        parts = [self._apply_confucian_to_problem(text)]

        # Append detected Confucian concepts as deeper analysis
        if ren["ren_present"]:
            parts.append(
                "Ren (仁, benevolence) is manifest: the supreme Confucian virtue is present."
            )

        if li["li_present"]:
            parts.append(
                "Li (禮, ritual propriety) is evident — proper conduct and form."
            )

        if yi["yi_present"]:
            parts.append(
                "Yi (義, righteousness) is demonstrated — moral principle over expedience."
            )

        if xiao["xiao_present"]:
            parts.append(
                "Xiao (孝, filial piety) is expressed — reverence for family and origins."
            )

        if junzi["junzi_present"]:
            parts.append("The junzi (君子, exemplary person) ideal is reflected.")

        if zhong_shu["zhong_loyalty_present"] or zhong_shu["shu_reciprocity_present"]:
            parts.append(zhong_shu["interpretation"])

        if de["de_present"]:
            parts.append("De (德, virtue/moral power) is emphasized.")

        if tianming["tianming_present"]:
            parts.append(
                "Tianming (天命, Mandate of Heaven) and cosmic moral order are invoked."
            )

        if learning["learning_present"]:
            parts.append(
                "The value of xue (學, learning) and self-cultivation is affirmed."
            )

        return " ".join(parts)

    def _calculate_tension(
        self,
        ren: Dict[str, Any],
        li: Dict[str, Any],
        yi: Dict[str, Any],
        xiao: Dict[str, Any],
        junzi: Dict[str, Any],
        zhong_shu: Dict[str, Any],
        de: Dict[str, Any],
        tianming: Dict[str, Any],
        learning: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate Confucian tensions in the text."""
        elements = []

        # Count present core virtues
        core_virtues = [
            ren["ren_present"],
            li["li_present"],
            yi["yi_present"],
            xiao["xiao_present"],
            de["de_present"],
        ]
        n_virtues = sum(1 for v in core_virtues if v)

        # Deficiency tensions — absence of virtues is itself a tension
        if not ren["ren_present"]:
            elements.append(
                "Deficiency in ren (benevolence) — lack of compassion and humaneness"
            )
        if not li["li_present"]:
            elements.append(
                "Deficiency in li (ritual propriety) — lack of proper conduct"
            )
        if not yi["yi_present"]:
            elements.append("Deficiency in yi (righteousness) — weak moral disposition")

        # Conflict tensions — when present virtues create ethical dilemmas
        if yi["yi_present"] and xiao["xiao_present"]:
            elements.append(
                "Tension between righteousness (yi) and filial obligation (xiao)"
            )
        if junzi["junzi_present"] and not de["de_present"]:
            elements.append(
                "Aspiration to junzi ideal without clear virtue (de) foundation"
            )
        if zhong_shu["zhong_loyalty_present"] and zhong_shu["shu_reciprocity_present"]:
            elements.append(
                "Tension between loyalty (zhong) and empathetic reciprocity (shu)"
            )

        # When many virtues present harmoniously, the ideal is achieved — low tension
        if n_virtues >= 4:
            elements = []

        n = len(elements)
        if n >= 3:
            level = "High"
            desc = "Multiple Confucian tensions active — competing virtues and obligations create rich ethical complexity."
        elif n >= 2:
            level = "Moderate"
            desc = "Some tensions from virtue deficiency or competing obligations."
        elif n >= 1:
            level = "Low"
            desc = "Mild tension within Confucian ethical framework."
        else:
            level = "Very Low"
            desc = "Minimal tension; virtues align in harmonious moral order."
            elements = ["No significant Confucian tensions detected"]

        return {
            "level": level,
            "score": n,
            "description": desc,
            "elements": elements,
        }
