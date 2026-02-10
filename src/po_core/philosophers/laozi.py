"""
Laozi (Lao Tzu) - Daoist Philosopher

Laozi (c. 6th century BCE, traditional dating)
Focus: Tao Te Ching, The Way (Dao), Non-action (Wu Wei)

Key Concepts:
- Tao (道): The Way - ineffable source and principle of all things
- Wu Wei (無為): Non-action, effortless action, going with the flow
- Te (德): Virtue/Power that flows from alignment with Tao
- Pu (朴): The Uncarved Block - natural simplicity before conditioning
- Yin-Yang: Complementary opposites in dynamic balance
- Fu (復): Return - returning to the source, the root
- Soft Overcomes Hard: Water metaphor, flexibility wins
- Emptiness and Usefulness: The usefulness of nothing
- Wu (無): Non-being from which being emerges
- Sage-Ruler: Leadership through non-interference
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Laozi(Philosopher):
    """
    Laozi's Daoist perspective.

    Analyzes prompts through the lens of the Tao, wu wei,
    naturalness, and the dynamic interplay of opposites.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Laozi",
            description="Daoist sage focused on the Tao (Way), wu wei (non-action), and natural simplicity",
        )

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze from Laozi's Daoist perspective."""
        analysis = self._analyze_daoist(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Daoism / The Way",
            "tension": tension,
            "tao": analysis["tao"],
            "wu_wei": analysis["wu_wei"],
            "te": analysis["te"],
            "pu": analysis["pu"],
            "yin_yang": analysis["yin_yang"],
            "return": analysis["return"],
            "soft_hard": analysis["soft_hard"],
            "emptiness": analysis["emptiness"],
            "sage_ruler": analysis["sage_ruler"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Daoist wisdom",
                "focus": "Tao, wu wei, naturalness, and complementary opposites",
            },
        }

    def _analyze_daoist(self, prompt: str) -> Dict[str, Any]:
        """Perform comprehensive Daoist analysis."""
        tao = self._analyze_tao(prompt)
        wu_wei = self._analyze_wu_wei(prompt)
        te = self._analyze_te(prompt)
        pu = self._analyze_pu(prompt)
        yin_yang = self._analyze_yin_yang(prompt)
        return_analysis = self._analyze_return(prompt)
        soft_hard = self._analyze_soft_hard(prompt)
        emptiness = self._analyze_emptiness(prompt)
        sage_ruler = self._analyze_sage_ruler(prompt)

        reasoning = self._construct_reasoning(
            tao, wu_wei, te, pu, yin_yang, soft_hard, emptiness
        )

        return {
            "reasoning": reasoning,
            "tao": tao,
            "wu_wei": wu_wei,
            "te": te,
            "pu": pu,
            "yin_yang": yin_yang,
            "return": return_analysis,
            "soft_hard": soft_hard,
            "emptiness": emptiness,
            "sage_ruler": sage_ruler,
        }

    def _analyze_tao(self, text: str) -> Dict[str, Any]:
        """Analyze the Tao (Way) - ineffable source of all."""
        text_lower = text.lower()

        tao_words = ["way", "path", "tao", "dao", "source", "origin", "principle"]
        tao_count = sum(1 for word in tao_words if word in text_lower)

        ineffable_words = [
            "cannot be named",
            "indescribable",
            "beyond words",
            "mystery",
            "nameless",
        ]
        ineffable_count = sum(1 for phrase in ineffable_words if phrase in text_lower)

        if tao_count >= 2 and ineffable_count >= 1:
            status = "Tao Intuited"
            description = "The Way is sensed but known to be beyond naming"
        elif tao_count >= 2:
            status = "Way Mentioned"
            description = "The Way or path is referenced"
        elif ineffable_count >= 1:
            status = "Ineffability Recognized"
            description = "Something beyond words is acknowledged"
        else:
            status = "Tao Not Explicit"
            description = "The Tao is not directly addressed"

        return {
            "status": status,
            "description": description,
            "tao_score": tao_count,
            "ineffable_score": ineffable_count,
            "principle": "The Tao that can be told is not the eternal Tao (TTC 1)",
        }

    def _analyze_wu_wei(self, text: str) -> Dict[str, Any]:
        """Analyze wu wei - non-action, effortless action."""
        text_lower = text.lower()

        wu_wei_words = [
            "effortless",
            "natural",
            "spontaneous",
            "let go",
            "allow",
            "flow",
            "without force",
            "not force",
            "non-action",
        ]
        wu_wei_count = sum(1 for phrase in wu_wei_words if phrase in text_lower)

        action_words = [
            "force",
            "push",
            "struggle",
            "strive",
            "effort",
            "fight",
            "control",
        ]
        action_count = sum(1 for word in action_words if word in text_lower)

        if wu_wei_count >= 2:
            status = "Wu Wei Present"
            description = "Non-action, effortless action - aligned with the Tao"
        elif wu_wei_count >= 1:
            status = "Traces of Wu Wei"
            description = "Some naturalness and effortlessness"
        elif action_count >= 2:
            status = "Contrary to Wu Wei"
            description = "Forcing and striving - against the natural flow"
        else:
            status = "Wu Wei Not Evident"
            description = "Neither action nor non-action emphasized"

        return {
            "status": status,
            "description": description,
            "wu_wei_score": wu_wei_count,
            "action_score": action_count,
            "principle": "Wu wei: Act without acting, do without doing (TTC 2)",
        }

    def _analyze_te(self, text: str) -> Dict[str, Any]:
        """Analyze te (virtue/power) - power from alignment with Tao."""
        text_lower = text.lower()

        te_words = ["virtue", "power", "integrity", "character", "inner strength"]
        te_count = sum(1 for word in te_words if word in text_lower)

        alignment_words = ["aligned", "harmony", "accord", "accordance", "in tune"]
        alignment_count = sum(1 for word in alignment_words if word in text_lower)

        if te_count >= 1 and alignment_count >= 1:
            status = "Te Manifest"
            description = "Virtue arising from alignment with the Tao"
        elif te_count >= 1:
            status = "Virtue Present"
            description = "Virtue mentioned but source unclear"
        elif alignment_count >= 1:
            status = "Alignment Sought"
            description = "Harmony sought - te may follow"
        else:
            status = "Te Not Evident"
            description = "Virtue/power not explicitly addressed"

        return {
            "status": status,
            "description": description,
            "te_score": te_count,
            "alignment_score": alignment_count,
            "principle": "Te: Power/virtue that flows from alignment with the Tao",
        }

    def _analyze_pu(self, text: str) -> Dict[str, Any]:
        """Analyze pu (uncarved block) - natural simplicity."""
        text_lower = text.lower()

        pu_words = [
            "simple",
            "simplicity",
            "natural",
            "unadorned",
            "plain",
            "uncomplicated",
            "innocent",
            "original",
        ]
        pu_count = sum(1 for word in pu_words if word in text_lower)

        complexity_words = [
            "complex",
            "complicated",
            "sophisticated",
            "elaborate",
            "artificial",
        ]
        complexity_count = sum(1 for word in complexity_words if word in text_lower)

        if pu_count >= 2:
            status = "Pu (Simplicity)"
            description = "Natural simplicity - the uncarved block"
        elif pu_count >= 1:
            status = "Some Simplicity"
            description = "Elements of natural simplicity"
        elif complexity_count >= 2:
            status = "Complexity Dominant"
            description = "Complexity and artifice - far from the uncarved block"
        else:
            status = "Simplicity Not Addressed"
            description = "Natural simplicity not thematized"

        return {
            "status": status,
            "description": description,
            "pu_score": pu_count,
            "complexity_score": complexity_count,
            "principle": "Pu: Return to the simplicity of the uncarved block (TTC 19)",
        }

    def _analyze_yin_yang(self, text: str) -> Dict[str, Any]:
        """Analyze yin-yang - complementary opposites."""
        text_lower = text.lower()

        yin_words = ["dark", "soft", "yielding", "receptive", "passive", "cold", "moon"]
        yin_count = sum(1 for word in yin_words if word in text_lower)

        yang_words = [
            "light",
            "hard",
            "active",
            "assertive",
            "aggressive",
            "hot",
            "sun",
        ]
        yang_count = sum(1 for word in yang_words if word in text_lower)

        balance_words = [
            "balance",
            "harmony",
            "complement",
            "opposite",
            "both",
            "together",
        ]
        balance_count = sum(1 for word in balance_words if word in text_lower)

        if yin_count >= 1 and yang_count >= 1:
            status = "Yin-Yang Present"
            description = "Both yin and yang qualities - dynamic interplay"
            balance = "Balanced" if balance_count >= 1 else "Both present"
        elif yin_count > yang_count:
            status = "Yin Dominant"
            description = "Yin qualities emphasized - receptive, yielding"
            balance = "Yin"
        elif yang_count > yin_count:
            status = "Yang Dominant"
            description = "Yang qualities emphasized - active, assertive"
            balance = "Yang"
        else:
            status = "Yin-Yang Not Evident"
            description = "Complementary opposites not thematized"
            balance = "Undifferentiated"

        return {
            "status": status,
            "description": description,
            "balance": balance,
            "yin_score": yin_count,
            "yang_score": yang_count,
            "principle": "Yin and yang arise together, complement each other",
        }

    def _analyze_return(self, text: str) -> Dict[str, Any]:
        """Analyze fu (return) - returning to the source."""
        text_lower = text.lower()

        return_words = [
            "return",
            "back",
            "source",
            "root",
            "origin",
            "beginning",
            "home",
        ]
        return_count = sum(1 for word in return_words if word in text_lower)

        progress_words = ["forward", "progress", "advance", "develop", "improve", "new"]
        progress_count = sum(1 for word in progress_words if word in text_lower)

        if return_count >= 2:
            status = "Return (Fu)"
            description = "Returning to the source, the root - the movement of the Tao"
        elif return_count >= 1:
            status = "Some Return"
            description = "Hints of returning to origins"
        elif progress_count >= 2:
            status = "Progress Emphasized"
            description = "Forward movement emphasized - may miss the return"
        else:
            status = "Return Not Evident"
            description = "Returning to the source not addressed"

        return {
            "status": status,
            "description": description,
            "return_score": return_count,
            "progress_score": progress_count,
            "principle": "Returning is the movement of the Tao (TTC 40)",
        }

    def _analyze_soft_hard(self, text: str) -> Dict[str, Any]:
        """Analyze soft overcoming hard - the water principle."""
        text_lower = text.lower()

        soft_words = ["soft", "gentle", "flexible", "yielding", "water", "weak"]
        soft_count = sum(1 for word in soft_words if word in text_lower)

        hard_words = ["hard", "rigid", "stiff", "strong", "force", "power"]
        hard_count = sum(1 for word in hard_words if word in text_lower)

        if soft_count > hard_count:
            status = "Soft Prevails"
            description = "Softness and flexibility - like water overcoming rock"
        elif soft_count >= 1 and hard_count >= 1:
            status = "Both Present"
            description = "Both soft and hard qualities - the soft may overcome"
        elif hard_count > soft_count:
            status = "Hardness Emphasized"
            description = "Hardness and rigidity - may be overcome by the soft"
        else:
            status = "Not Addressed"
            description = "Soft-hard dynamic not thematized"

        return {
            "status": status,
            "description": description,
            "soft_score": soft_count,
            "hard_score": hard_count,
            "principle": "The soft overcomes the hard, the weak overcomes the strong (TTC 36)",
        }

    def _analyze_emptiness(self, text: str) -> Dict[str, Any]:
        """Analyze emptiness and its usefulness."""
        text_lower = text.lower()

        empty_words = ["empty", "hollow", "void", "nothing", "space", "emptiness"]
        empty_count = sum(1 for word in empty_words if word in text_lower)

        useful_words = ["useful", "use", "function", "purpose", "serve"]
        useful_count = sum(1 for word in useful_words if word in text_lower)

        if empty_count >= 1 and useful_count >= 1:
            status = "Emptiness as Useful"
            description = (
                "The usefulness of emptiness recognized - like the hub of a wheel"
            )
        elif empty_count >= 1:
            status = "Emptiness Present"
            description = "Emptiness acknowledged"
        else:
            status = "Emptiness Not Evident"
            description = "The creative void not addressed"

        return {
            "status": status,
            "description": description,
            "empty_score": empty_count,
            "useful_score": useful_count,
            "principle": "We shape clay into a pot, but it is the emptiness inside that holds (TTC 11)",
        }

    def _analyze_sage_ruler(self, text: str) -> Dict[str, Any]:
        """Analyze sage-ruler - leadership through non-interference."""
        text_lower = text.lower()

        leadership_words = ["lead", "leader", "ruler", "govern", "king", "chief"]
        leadership_count = sum(1 for word in leadership_words if word in text_lower)

        non_interference = [
            "let",
            "allow",
            "without interfering",
            "hands off",
            "minimal",
        ]
        non_interference_count = sum(
            1 for phrase in non_interference if phrase in text_lower
        )

        if leadership_count >= 1 and non_interference_count >= 1:
            status = "Sage Ruler"
            description = "Leadership through non-interference - ruling by not ruling"
        elif leadership_count >= 1:
            status = "Leadership Present"
            description = "Leadership mentioned but style unclear"
        elif non_interference_count >= 1:
            status = "Non-interference"
            description = "Letting be - sage-like approach"
        else:
            status = "Not Addressed"
            description = "Leadership/governance not thematized"

        return {
            "status": status,
            "description": description,
            "leadership_score": leadership_count,
            "non_interference_score": non_interference_count,
            "principle": "The best leader is barely known to exist (TTC 17)",
        }

    def _construct_reasoning(
        self,
        tao: Dict[str, Any],
        wu_wei: Dict[str, Any],
        te: Dict[str, Any],
        pu: Dict[str, Any],
        yin_yang: Dict[str, Any],
        soft_hard: Dict[str, Any],
        emptiness: Dict[str, Any],
    ) -> str:
        """Construct Daoist reasoning."""
        reasoning = (
            f"From Laozi's Daoist perspective, this text is examined through the lens of the Tao. "
            f"The Tao: {tao['description']}. "
            f"Wu Wei: {wu_wei['description']}. "
        )

        if te["status"] != "Te Not Evident":
            reasoning += f"Te (Virtue): {te['description']}. "

        reasoning += f"Simplicity (Pu): {pu['description']}. "
        reasoning += f"Yin-Yang: {yin_yang['description']}. "

        if soft_hard["status"] != "Not Addressed":
            reasoning += f"Soft and Hard: {soft_hard['description']}. "

        reasoning += (
            "The Tao that can be told is not the eternal Tao. "
            "In stillness, follow the flow of nature. In action, act without acting."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate philosophical tension."""
        tension_score = 0
        tension_elements = []

        if analysis["wu_wei"]["action_score"] >= 2:
            tension_score += 2
            tension_elements.append("Forcing and striving - contrary to wu wei")

        if analysis["pu"]["complexity_score"] >= 2:
            tension_score += 1
            tension_elements.append("Complexity and artifice")

        if analysis["yin_yang"]["balance"] == "Yang":
            tension_score += 1
            tension_elements.append("Yang dominant - imbalance")

        if analysis["soft_hard"]["hard_score"] > analysis["soft_hard"]["soft_score"]:
            tension_score += 1
            tension_elements.append("Hardness over softness")

        if tension_score >= 4:
            level = "High"
            description = (
                "Far from the Tao - too much forcing, complexity, and rigidity"
            )
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some distance from natural simplicity"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions with the Way"
        else:
            level = "Very Low"
            description = "Aligned with the Tao - naturalness and simplicity"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["Harmony with the Tao"]
            ),
        }
