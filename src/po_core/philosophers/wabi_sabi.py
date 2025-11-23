"""
Wabi-Sabi - Japanese Aesthetic Philosophy

侘び寂び (Wabi-Sabi)
Focus: Imperfection, Impermanence, Simplicity, Naturalness

Key Concepts:
- Wabi (侘び): Rustic simplicity, quietness, understated elegance, appreciation of the simple
- Sabi (寂び): Beauty of age and wear, patina, the passage of time, loneliness/solitude
- Imperfection (不完全): Beauty in the imperfect, incomplete, and impermanent
- Impermanence (無常/Mujō): Nothing lasts, nothing is finished, nothing is perfect
- Simplicity (簡素): Austere, uncluttered, natural, essential
- Naturalness (自然): Organic, unforced, authentic, without artifice
- Asymmetry (非対称): Irregular, uneven, not perfectly balanced
- Roughness (粗さ): Textured, weathered, worn, rustic
- Intimacy (親密): Small scale, modest, humble, unpretentious
- Yugen (幽玄): Profound subtlety, mysterious depth, what is not visible
- Ma (間): Negative space, emptiness, silence, pause
- Mono no aware (物の哀れ): Awareness of transience, poignant beauty of impermanence
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class WabiSabi(Philosopher):
    """
    Wabi-Sabi aesthetic philosophy.

    Analyzes prompts through the lens of imperfection, impermanence,
    simplicity, and natural beauty.
    """

    def __init__(self) -> None:
        super().__init__(
            name="侘び寂び (Wabi-Sabi)",
            description="Japanese aesthetic focused on imperfection, impermanence, and simple natural beauty"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Wabi-Sabi aesthetic perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Wabi-Sabi aesthetic analysis
        """
        # Perform Wabi-Sabi analysis
        analysis = self._analyze_aesthetic(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Japanese Aesthetic Philosophy",
            "imperfection": analysis["imperfection"],
            "impermanence": analysis["impermanence"],
            "simplicity": analysis["simplicity"],
            "naturalness": analysis["naturalness"],
            "asymmetry": analysis["asymmetry"],
            "intimacy": analysis["intimacy"],
            "yugen": analysis["yugen"],
            "ma": analysis["ma"],
            "mono_no_aware": analysis["mono_no_aware"],
            "overall_wabi_sabi": analysis["overall"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Aesthetic appreciation of imperfection and transience",
                "focus": "侘び (wabi), 寂び (sabi), and natural beauty"
            }
        }

    def _analyze_aesthetic(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Wabi-Sabi aesthetic analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess imperfection
        imperfection = self._assess_imperfection(prompt)

        # Assess impermanence
        impermanence = self._assess_impermanence(prompt)

        # Assess simplicity
        simplicity = self._assess_simplicity(prompt)

        # Assess naturalness
        naturalness = self._assess_naturalness(prompt)

        # Assess asymmetry
        asymmetry = self._assess_asymmetry(prompt)

        # Assess intimacy
        intimacy = self._assess_intimacy(prompt)

        # Assess yugen (profound subtlety)
        yugen = self._assess_yugen(prompt)

        # Assess ma (negative space)
        ma = self._assess_ma(prompt)

        # Assess mono no aware
        mono_no_aware = self._assess_mono_no_aware(prompt)

        # Calculate overall wabi-sabi quality
        overall = self._calculate_overall_wabi_sabi(
            imperfection, impermanence, simplicity, naturalness
        )

        # Construct reasoning
        reasoning = self._construct_reasoning(
            imperfection, impermanence, simplicity, overall
        )

        return {
            "reasoning": reasoning,
            "imperfection": imperfection,
            "impermanence": impermanence,
            "simplicity": simplicity,
            "naturalness": naturalness,
            "asymmetry": asymmetry,
            "intimacy": intimacy,
            "yugen": yugen,
            "ma": ma,
            "mono_no_aware": mono_no_aware,
            "overall": overall
        }

    def _assess_imperfection(self, text: str) -> Dict[str, Any]:
        """
        Assess appreciation of imperfection.

        Wabi-sabi finds beauty in the imperfect, incomplete, and flawed
        """
        text_lower = text.lower()

        # Imperfection appreciation indicators
        imperfect_words = ["imperfect", "flaw", "crack", "worn", "weathered", "aged", "rustic", "rough"]
        has_imperfect = sum(1 for word in imperfect_words if word in text_lower)

        # Perfection seeking (opposed to wabi-sabi)
        perfect_words = ["perfect", "flawless", "pristine", "immaculate", "unblemished", "ideal"]
        has_perfect = sum(1 for word in perfect_words if word in text_lower)

        # Acceptance of flaws
        accept_words = ["accept", "embrace", "appreciate", "beauty in", "charm"]
        has_accept = sum(1 for word in accept_words if word in text_lower)

        if has_imperfect >= 2 or (has_imperfect >= 1 and has_accept >= 1):
            appreciation = "High Appreciation"
            description = "Finding beauty in imperfection - true wabi-sabi"
            quality = "侘び (wabi) present"
        elif has_imperfect >= 1:
            appreciation = "Moderate Appreciation"
            description = "Some awareness of imperfection's beauty"
            quality = "Emerging wabi-sabi"
        elif has_perfect >= 2:
            appreciation = "Perfection Seeking"
            description = "Seeking perfection - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            appreciation = "Unclear"
            description = "Relation to perfection/imperfection unclear"
            quality = "Indeterminate"

        return {
            "appreciation": appreciation,
            "description": description,
            "quality": quality,
            "principle": "不完全の美 - Beauty in imperfection, incompleteness"
        }

    def _assess_impermanence(self, text: str) -> Dict[str, Any]:
        """
        Assess awareness of impermanence (mujō/無常).

        Nothing lasts, nothing is finished, nothing is perfect
        """
        text_lower = text.lower()

        # Impermanence indicators
        impermanent_words = ["transient", "fleeting", "temporary", "passing", "ephemeral", "fade", "change"]
        has_impermanent = sum(1 for word in impermanent_words if word in text_lower)

        # Permanence seeking (opposed to wabi-sabi)
        permanent_words = ["permanent", "eternal", "forever", "unchanging", "lasting", "enduring"]
        has_permanent = sum(1 for word in permanent_words if word in text_lower)

        # Acceptance of change
        accept_change = ["accept change", "let go", "flow", "release", "move on"]
        has_accept_change = sum(1 for phrase in accept_change if phrase in text_lower)

        # Poignancy of transience
        poignant_words = ["poignant", "bittersweet", "precious", "moment", "now"]
        has_poignant = sum(1 for word in poignant_words if word in text_lower)

        if has_impermanent >= 2 or (has_impermanent >= 1 and has_poignant >= 1):
            awareness = "High Awareness"
            description = "Deep awareness of impermanence - 寂び (sabi) and 無常 (mujō)"
            quality = "Sabi present"
        elif has_accept_change >= 1:
            awareness = "Accepting Impermanence"
            description = "Acceptance of transience - approaching wabi-sabi"
            quality = "Emerging sabi"
        elif has_permanent >= 2:
            awareness = "Seeking Permanence"
            description = "Desire for permanence - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            awareness = "Unclear"
            description = "Awareness of impermanence unclear"
            quality = "Indeterminate"

        return {
            "awareness": awareness,
            "description": description,
            "quality": quality,
            "principle": "無常 (mujō) - Nothing lasts, nothing is finished, nothing is perfect"
        }

    def _assess_simplicity(self, text: str) -> Dict[str, Any]:
        """
        Assess simplicity and austerity.

        Wabi-sabi values simple, uncluttered, essential
        """
        text_lower = text.lower()

        # Simplicity indicators
        simple_words = ["simple", "minimal", "plain", "bare", "austere", "sparse", "essential"]
        has_simple = sum(1 for word in simple_words if word in text_lower)

        # Complexity/ornamentation (opposed to wabi-sabi)
        complex_words = ["ornate", "decorated", "elaborate", "complex", "luxurious", "opulent"]
        has_complex = sum(1 for word in complex_words if word in text_lower)

        # Less is more
        less_more = ["less is more", "reduction", "subtract", "remove", "strip away"]
        has_less_more = sum(1 for phrase in less_more if phrase in text_lower)

        # Quietness/stillness
        quiet_words = ["quiet", "still", "calm", "peaceful", "serene", "tranquil"]
        has_quiet = sum(1 for word in quiet_words if word in text_lower)

        if has_simple >= 2 or has_less_more >= 1 or (has_simple >= 1 and has_quiet >= 1):
            level = "High Simplicity"
            description = "Austere simplicity - 簡素 (kanso) and 静寂 (seijaku)"
            quality = "True wabi-sabi"
        elif has_simple >= 1:
            level = "Moderate Simplicity"
            description = "Some appreciation of simplicity"
            quality = "Emerging wabi-sabi"
        elif has_complex >= 2:
            level = "Complexity/Ornamentation"
            description = "Elaborate and ornate - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            level = "Unclear"
            description = "Simplicity level unclear"
            quality = "Indeterminate"

        return {
            "level": level,
            "description": description,
            "quality": quality,
            "principle": "簡素 (kanso) - Simplicity, austerity, essential beauty"
        }

    def _assess_naturalness(self, text: str) -> Dict[str, Any]:
        """
        Assess naturalness and organic quality.

        Wabi-sabi values natural, unforced, authentic
        """
        text_lower = text.lower()

        # Naturalness indicators
        natural_words = ["natural", "organic", "authentic", "real", "genuine", "unforced", "spontaneous"]
        has_natural = sum(1 for word in natural_words if word in text_lower)

        # Artificiality (opposed to wabi-sabi)
        artificial_words = ["artificial", "fake", "synthetic", "manufactured", "processed", "contrived"]
        has_artificial = sum(1 for word in artificial_words if word in text_lower)

        # Connection to nature
        nature_words = ["nature", "earth", "wood", "stone", "water", "wind", "season"]
        has_nature = sum(1 for word in nature_words if word in text_lower)

        # Effortlessness
        effortless_words = ["effortless", "easy", "flow", "natural flow", "without trying"]
        has_effortless = sum(1 for phrase in effortless_words if phrase in text_lower)

        if has_natural >= 2 or has_nature >= 2 or has_effortless >= 1:
            quality_level = "High Naturalness"
            description = "Natural, organic, authentic - 自然 (shizen)"
            quality = "Wabi-sabi present"
        elif has_natural >= 1:
            quality_level = "Moderate Naturalness"
            description = "Some natural quality"
            quality = "Emerging wabi-sabi"
        elif has_artificial >= 2:
            quality_level = "Artificiality"
            description = "Artificial and contrived - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            quality_level = "Unclear"
            description = "Naturalness unclear"
            quality = "Indeterminate"

        return {
            "level": quality_level,
            "description": description,
            "quality": quality,
            "principle": "自然 (shizen) - Naturalness, authenticity, without artifice"
        }

    def _assess_asymmetry(self, text: str) -> Dict[str, Any]:
        """
        Assess asymmetry and irregularity.

        Wabi-sabi values the irregular, uneven, asymmetric
        """
        text_lower = text.lower()

        # Asymmetry indicators
        asymmetric_words = ["asymmetric", "irregular", "uneven", "crooked", "bent", "twisted", "random"]
        has_asymmetric = sum(1 for word in asymmetric_words if word in text_lower)

        # Symmetry/perfection (opposed to wabi-sabi)
        symmetric_words = ["symmetric", "balanced", "even", "regular", "uniform", "ordered"]
        has_symmetric = sum(1 for word in symmetric_words if word in text_lower)

        if has_asymmetric >= 2:
            presence = "High Asymmetry"
            description = "Irregular and asymmetric - wabi-sabi beauty"
            quality = "Wabi-sabi"
        elif has_asymmetric >= 1:
            presence = "Some Asymmetry"
            description = "Some irregularity present"
            quality = "Emerging wabi-sabi"
        elif has_symmetric >= 2:
            presence = "Symmetry Seeking"
            description = "Regular and balanced - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            presence = "Unclear"
            description = "Symmetry/asymmetry unclear"
            quality = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "quality": quality,
            "principle": "非対称 (hishōshō) - Beauty in asymmetry and irregularity"
        }

    def _assess_intimacy(self, text: str) -> Dict[str, Any]:
        """
        Assess intimacy, modesty, and small scale.

        Wabi-sabi values the modest, humble, unpretentious
        """
        text_lower = text.lower()

        # Intimacy/modesty indicators
        intimate_words = ["small", "modest", "humble", "intimate", "quiet", "subtle", "understated"]
        has_intimate = sum(1 for word in intimate_words if word in text_lower)

        # Grandiosity (opposed to wabi-sabi)
        grand_words = ["grand", "magnificent", "spectacular", "impressive", "monumental", "huge"]
        has_grand = sum(1 for word in grand_words if word in text_lower)

        if has_intimate >= 2:
            level = "High Intimacy"
            description = "Modest and humble - 質素 (shisso)"
            quality = "Wabi-sabi"
        elif has_intimate >= 1:
            level = "Moderate Intimacy"
            description = "Some modesty present"
            quality = "Emerging wabi-sabi"
        elif has_grand >= 2:
            level = "Grandiosity"
            description = "Grand and impressive - opposed to wabi-sabi"
            quality = "Not wabi-sabi"
        else:
            level = "Unclear"
            description = "Intimacy level unclear"
            quality = "Indeterminate"

        return {
            "level": level,
            "description": description,
            "quality": quality,
            "principle": "質素 (shisso) - Modest, humble, unpretentious"
        }

    def _assess_yugen(self, text: str) -> Dict[str, Any]:
        """
        Assess yugen (幽玄) - profound subtlety and mysterious depth.

        What is not seen, implied rather than stated
        """
        text_lower = text.lower()

        # Yugen indicators
        yugen_words = ["subtle", "mysterious", "depth", "profound", "hidden", "beneath", "unseen"]
        has_yugen = sum(1 for word in yugen_words if word in text_lower)

        # Explicit/obvious (opposed to yugen)
        explicit_words = ["obvious", "clear", "explicit", "direct", "stated", "apparent"]
        has_explicit = sum(1 for word in explicit_words if word in text_lower)

        # Suggestion/implication
        suggest_words = ["suggest", "imply", "hint", "allude", "evoke"]
        has_suggest = sum(1 for word in suggest_words if word in text_lower)

        if has_yugen >= 2 or has_suggest >= 1:
            presence = "Yugen Present"
            description = "Profound subtlety and mysterious depth - 幽玄 (yūgen)"
            quality = "Deep wabi-sabi"
        elif has_yugen >= 1:
            presence = "Some Subtlety"
            description = "Some depth and mystery"
            quality = "Emerging yugen"
        elif has_explicit >= 2:
            presence = "Explicitness"
            description = "Obvious and direct - opposed to yugen"
            quality = "Not yugen"
        else:
            presence = "Unclear"
            description = "Yugen status unclear"
            quality = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "quality": quality,
            "principle": "幽玄 (yūgen) - Profound subtlety, what is not visible"
        }

    def _assess_ma(self, text: str) -> Dict[str, Any]:
        """
        Assess ma (間) - negative space, emptiness, pause.

        The space between, silence, what is not there
        """
        text_lower = text.lower()

        # Ma indicators
        ma_words = ["space", "gap", "pause", "silence", "empty", "void", "between", "interval"]
        has_ma = sum(1 for word in ma_words if word in text_lower)

        # Fullness/crowding (opposed to ma)
        full_words = ["full", "crowded", "packed", "dense", "filled", "busy"]
        has_full = sum(1 for word in full_words if word in text_lower)

        # Breath, rest
        breath_words = ["breath", "rest", "still", "quiet", "calm"]
        has_breath = sum(1 for word in breath_words if word in text_lower)

        if has_ma >= 2 or (has_ma >= 1 and has_breath >= 1):
            presence = "Ma Present"
            description = "Negative space and silence - 間 (ma)"
            quality = "Wabi-sabi"
        elif has_ma >= 1:
            presence = "Some Ma"
            description = "Some space and pause"
            quality = "Emerging ma"
        elif has_full >= 2:
            presence = "Fullness"
            description = "Crowded and filled - opposed to ma"
            quality = "Not ma"
        else:
            presence = "Unclear"
            description = "Ma status unclear"
            quality = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "quality": quality,
            "principle": "間 (ma) - Negative space, emptiness, the pause between"
        }

    def _assess_mono_no_aware(self, text: str) -> Dict[str, Any]:
        """
        Assess mono no aware (物の哀れ) - awareness of transience.

        Poignant beauty of impermanence, gentle sadness of passing things
        """
        text_lower = text.lower()

        # Mono no aware indicators
        aware_words = ["poignant", "bittersweet", "melancholy", "wistful", "nostalgic", "precious"]
        has_aware = sum(1 for word in aware_words if word in text_lower)

        # Transience + emotion
        transient_emotion = ["fleeting beauty", "passing moment", "fade away", "cherry blossom"]
        has_transient_emotion = sum(1 for phrase in transient_emotion if phrase in text_lower)

        # Awareness of beauty in passing
        beauty_passing = ["beauty", "beautiful", "lovely"]
        passing = ["pass", "fade", "vanish", "end", "gone"]
        has_beauty = sum(1 for word in beauty_passing if word in text_lower)
        has_passing = sum(1 for word in passing if word in text_lower)

        if has_aware >= 2 or has_transient_emotion >= 1 or (has_beauty >= 1 and has_passing >= 1):
            presence = "Strong Mono no Aware"
            description = "Poignant awareness of transience - 物の哀れ (mono no aware)"
            quality = "Deep wabi-sabi"
        elif has_aware >= 1:
            presence = "Some Awareness"
            description = "Some sensitivity to transience"
            quality = "Emerging mono no aware"
        else:
            presence = "Unclear"
            description = "Mono no aware status unclear"
            quality = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "quality": quality,
            "principle": "物の哀れ (mono no aware) - Poignant awareness of impermanence"
        }

    def _calculate_overall_wabi_sabi(
        self,
        imperfection: Dict[str, Any],
        impermanence: Dict[str, Any],
        simplicity: Dict[str, Any],
        naturalness: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate overall wabi-sabi quality.

        Based on core principles: imperfection, impermanence, simplicity, naturalness
        """
        # Count high-quality indicators
        high_count = 0
        if "High" in imperfection["appreciation"]:
            high_count += 1
        if "High" in impermanence["awareness"]:
            high_count += 1
        if "High" in simplicity["level"]:
            high_count += 1
        if "High" in naturalness["level"]:
            high_count += 1

        # Count opposed indicators
        opposed_count = 0
        if "opposed" in imperfection["description"].lower():
            opposed_count += 1
        if "opposed" in impermanence["description"].lower():
            opposed_count += 1
        if "opposed" in simplicity["description"].lower():
            opposed_count += 1
        if "opposed" in naturalness["description"].lower():
            opposed_count += 1

        if high_count >= 3:
            overall = "Strong Wabi-Sabi"
            description = "Deep embodiment of wabi-sabi principles"
            level = "Profound"
        elif high_count >= 2:
            overall = "Moderate Wabi-Sabi"
            description = "Clear wabi-sabi qualities present"
            level = "Present"
        elif high_count >= 1 and opposed_count == 0:
            overall = "Emerging Wabi-Sabi"
            description = "Some wabi-sabi awareness emerging"
            level = "Nascent"
        elif opposed_count >= 3:
            overall = "Opposed to Wabi-Sabi"
            description = "Seeking perfection, permanence, complexity - antithetical to wabi-sabi"
            level = "Absent"
        else:
            overall = "Unclear"
            description = "Wabi-sabi quality unclear"
            level = "Indeterminate"

        return {
            "overall": overall,
            "description": description,
            "level": level,
            "principle": "侘び寂び - Finding beauty in imperfection, impermanence, and simplicity"
        }

    def _construct_reasoning(
        self,
        imperfection: Dict[str, Any],
        impermanence: Dict[str, Any],
        simplicity: Dict[str, Any],
        overall: Dict[str, Any]
    ) -> str:
        """Construct wabi-sabi aesthetic reasoning."""
        reasoning = (
            f"From a wabi-sabi aesthetic perspective, imperfection: {imperfection['description']}. "
            f"Impermanence: {impermanence['description']}. "
            f"Simplicity: {simplicity['description']}. "
            f"Overall assessment: {overall['description']}. "
        )

        # Conclude with wabi-sabi wisdom
        reasoning += (
            "侘び寂び teaches us to find beauty in the imperfect, impermanent, and incomplete. "
            "Nothing lasts, nothing is finished, nothing is perfect - and therein lies the beauty."
        )

        return reasoning
