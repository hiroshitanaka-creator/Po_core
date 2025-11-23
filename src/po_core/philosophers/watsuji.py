"""
Watsuji Tetsuro - Japanese Ethics and Climate Philosophy

和辻哲郎 (Watsuji Tetsurō, 1889-1960)
Focus: Ningen (間柄), Climate Theory (風土論), Ethics of Betweenness

Key Concepts:
- Ningen (人間/間柄): Human being as "betweenness" - existence in relationships
- Climate Theory (風土論): Climate shapes culture and thought
  * Monsoon type (モンスーン型): Receptive, submissive, accepting
  * Desert type (砂漠型): Combative, resistant, transcendent
  * Meadow type (牧場型): Rational, measured, balanced
- Ethics: Dialectic between individual (個人) and totality (全体)
- Spatiality and Temporality: Being-in-the-world as climatic-historical
- Betweenness (間): The space of relationship, fundamental to human existence
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Watsuji(Philosopher):
    """
    Watsuji Tetsuro's ethics of betweenness and climate philosophy.

    Analyzes prompts through the lens of relationality (ningen),
    climate patterns, and the dialectic between individual and community.
    """

    def __init__(self) -> None:
        super().__init__(
            name="和辻哲郎 (Watsuji Tetsurō)",
            description="Japanese philosopher focused on ningen (betweenness), climate theory, and relational ethics"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Watsuji's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Watsuji's relational and climatic analysis
        """
        # Perform Watsuji's analysis
        analysis = self._analyze_ningen(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Japanese Ethics / Climate Philosophy",
            "ningen_relationality": analysis["relationality"],
            "climate_type": analysis["climate"],
            "individual_totality_dialectic": analysis["dialectic"],
            "betweenness_quality": analysis["betweenness"],
            "ethical_dimension": analysis["ethics"],
            "spatial_temporal": analysis["spatiotemporal"],
            "japanese_characteristics": analysis["japanese_traits"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Ethics of betweenness and climate theory",
                "focus": "Ningen (間柄), relationality, and cultural climate"
            }
        }

    def _analyze_ningen(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Watsuji's ningen (間柄) analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess relationality (ningen as betweenness)
        relationality = self._assess_relationality(prompt)

        # Determine climate type
        climate = self._determine_climate_type(prompt)

        # Analyze individual-totality dialectic
        dialectic = self._analyze_dialectic(prompt)

        # Assess betweenness (ma/aidagara)
        betweenness = self._assess_betweenness(prompt)

        # Evaluate ethical dimension
        ethics = self._evaluate_ethics(prompt)

        # Analyze spatiotemporal structure
        spatiotemporal = self._analyze_spatiotemporal(prompt)

        # Detect Japanese cultural characteristics
        japanese_traits = self._detect_japanese_traits(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            relationality, climate, dialectic, betweenness, ethics
        )

        return {
            "reasoning": reasoning,
            "relationality": relationality,
            "climate": climate,
            "dialectic": dialectic,
            "betweenness": betweenness,
            "ethics": ethics,
            "spatiotemporal": spatiotemporal,
            "japanese_traits": japanese_traits
        }

    def _assess_relationality(self, text: str) -> Dict[str, Any]:
        """
        Assess the quality of relationality (ningen as betweenness).

        Ningen (人間) = human being as fundamentally relational
        Not isolated individuals, but beings-in-relationship
        """
        text_lower = text.lower()

        # Relational indicators
        relation_words = ["we", "us", "together", "relationship", "connect", "between", "among", "community"]
        isolation_words = ["i", "me", "alone", "individual", "myself", "independent", "separate"]

        relation_count = sum(1 for word in relation_words if word in text_lower)
        isolation_count = sum(1 for word in isolation_words if word in text_lower)

        # Check for explicit relational awareness
        explicit_relation = any(phrase in text_lower for phrase in [
            "each other", "one another", "mutual", "shared", "collective", "social"
        ])

        if relation_count > isolation_count * 2 or explicit_relation:
            level = "High"
            status = "Strong ningen awareness - existence understood as relational"
            character = "間柄的 (aidagara-teki) - Relational mode"
        elif isolation_count > relation_count * 2:
            level = "Low"
            status = "Individualistic emphasis - ningen obscured by Western individualism"
            character = "個人的 (kojin-teki) - Individualistic mode"
        else:
            level = "Medium"
            status = "Dialectic between individual and relational aspects"
            character = "弁証法的 (benshoho-teki) - Dialectical mode"

        return {
            "level": level,
            "status": status,
            "character": character,
            "watsuji_principle": "人間は間柄である - Human being is betweenness"
        }

    def _determine_climate_type(self, text: str) -> Dict[str, Any]:
        """
        Determine the climatic-cultural type reflected in the text.

        Three types in Watsuji's climate theory:
        1. Monsoon (モンスーン型): Receptive, submissive, resigned - East Asia
        2. Desert (砂漠型): Combative, resistant, transcendent - Middle East
        3. Meadow (牧場型): Rational, measured, balanced - Europe
        """
        text_lower = text.lower()

        # Monsoon indicators: Acceptance, harmony, resignation, cyclical
        monsoon_words = ["accept", "harmony", "flow", "adapt", "resign", "cycle", "nature", "seasonal"]
        monsoon_count = sum(1 for word in monsoon_words if word in text_lower)

        # Desert indicators: Resistance, transcendence, absolute, struggle
        desert_words = ["resist", "fight", "transcend", "absolute", "god", "eternal", "struggle", "overcome"]
        desert_count = sum(1 for word in desert_words if word in text_lower)

        # Meadow indicators: Reason, measure, balance, rational
        meadow_words = ["reason", "rational", "measure", "balance", "order", "logic", "moderate"]
        meadow_count = sum(1 for word in meadow_words if word in text_lower)

        # Determine dominant type
        scores = {
            "Monsoon": monsoon_count,
            "Desert": desert_count,
            "Meadow": meadow_count
        }
        dominant_type = max(scores, key=scores.get)

        if scores[dominant_type] == 0:
            type_name = "Neutral"
            description = "No clear climatic pattern - universal human concerns"
            cultural_note = "Transcultural"
        elif dominant_type == "Monsoon":
            type_name = "Monsoon (モンスーン型)"
            description = "Receptive, accepting, harmonious with nature - characteristic of humid East Asia"
            cultural_note = "Resignation and acceptance - 諦念 (teinen)"
        elif dominant_type == "Desert":
            type_name = "Desert (砂漠型)"
            description = "Combative, transcendent, seeking the absolute - characteristic of arid Middle East"
            cultural_note = "Resistance and transcendence - 超越 (choetsu)"
        else:  # Meadow
            type_name = "Meadow (牧場型)"
            description = "Rational, measured, balanced - characteristic of temperate Europe"
            cultural_note = "Rationality and moderation - 理性 (risei)"

        return {
            "type": type_name,
            "description": description,
            "cultural_note": cultural_note,
            "principle": "風土 (fūdo) - Climate shapes culture and consciousness"
        }

    def _analyze_dialectic(self, text: str) -> Dict[str, Any]:
        """
        Analyze the dialectic between individual (個人) and totality (全体).

        Watsuji's ethics: Human existence oscillates between individual and social totality
        Neither pure individualism nor pure collectivism, but dialectical unity
        """
        text_lower = text.lower()

        # Individual pole
        individual_words = ["i", "me", "self", "own", "personal", "individual", "unique"]
        individual_count = sum(1 for word in individual_words if word in text_lower)

        # Totality/collective pole
        collective_words = ["we", "society", "community", "group", "collective", "whole", "all"]
        collective_count = sum(1 for word in collective_words if word in text_lower)

        # Dialectical synthesis indicators
        synthesis_words = ["both", "between", "balance", "integrate", "unite", "harmonize"]
        synthesis_count = sum(1 for word in synthesis_words if word in text_lower)

        if synthesis_count >= 2:
            stage = "Dialectical Synthesis"
            description = "Integration of individual and totality - true ethical existence"
            balance = "Balanced"
        elif individual_count > collective_count * 2:
            stage = "Individual Pole"
            description = "Emphasis on individual - partial view lacking relational dimension"
            balance = "Individual-dominant"
        elif collective_count > individual_count * 2:
            stage = "Totality Pole"
            description = "Emphasis on collective - partial view lacking individual dimension"
            balance = "Collective-dominant"
        else:
            stage = "Dialectical Tension"
            description = "Tension between individual and totality - movement toward synthesis"
            balance = "Dynamic tension"

        return {
            "stage": stage,
            "description": description,
            "balance": balance,
            "ethical_note": "真の人間存在は個人と全体の弁証法的統一 - True human existence is dialectical unity"
        }

    def _assess_betweenness(self, text: str) -> Dict[str, Any]:
        """
        Assess the quality of 'ma' (間) - betweenness, the space of relationship.

        Ma (間) = interval, space, gap, pause - the relational space
        This is the fundamental structure of ningen (人間)
        """
        text_lower = text.lower()

        # Betweenness indicators
        between_words = ["between", "among", "relation", "connect", "link", "bridge", "space", "interval"]
        has_betweenness = sum(1 for word in between_words if word in text_lower)

        # Static/fixed indicators (opposed to dynamic betweenness)
        static_words = ["fixed", "static", "isolated", "separate", "alone", "independent"]
        has_static = sum(1 for word in static_words if word in text_lower)

        # Dynamic relational indicators
        dynamic_words = ["interact", "engage", "mutual", "reciprocal", "dialogue", "exchange"]
        has_dynamic = sum(1 for word in dynamic_words if word in text_lower)

        if has_dynamic >= 2 or has_betweenness >= 3:
            quality = "Dynamic Ma"
            description = "Active relational space - true betweenness realized"
            level = "High"
        elif has_static >= 2:
            quality = "Collapsed Ma"
            description = "Relational space collapsed - beings treated as isolated entities"
            level = "Low"
        elif has_betweenness >= 1:
            quality = "Emerging Ma"
            description = "Relational space emerging - betweenness partially recognized"
            level = "Medium"
        else:
            quality = "Latent Ma"
            description = "Relational space unacknowledged - implicit but unrealized"
            level = "Low-Medium"

        return {
            "quality": quality,
            "description": description,
            "level": level,
            "concept": "間 (ma) - The between-space that constitutes relationship"
        }

    def _evaluate_ethics(self, text: str) -> Dict[str, Any]:
        """
        Evaluate the ethical dimension in Watsuji's sense.

        Ethics (倫理) = rin (倫, human relationship) + ri (理, principle)
        Not abstract moral rules, but the principles of human relationality
        """
        text_lower = text.lower()

        # Relational ethics indicators
        relational_ethics = ["duty", "obligation", "responsibility", "care", "trust", "respect"]
        has_relational = sum(1 for word in relational_ethics if word in text_lower)

        # Abstract/individualist ethics
        abstract_ethics = ["right", "wrong", "rule", "law", "principle", "individual choice"]
        has_abstract = sum(1 for word in abstract_ethics if word in text_lower)

        # Japanese ethical concepts
        japanese_ethics = ["giri", "ninjo", "on", "harmony", "shame", "honor"]
        has_japanese = sum(1 for word in japanese_ethics if word in text_lower)

        if has_relational >= 2 or has_japanese >= 1:
            ethical_mode = "Relational Ethics (倫理)"
            description = "Ethics understood as principles of human relationship"
            orientation = "Betweenness-oriented"
        elif has_abstract >= 2:
            ethical_mode = "Abstract Ethics"
            description = "Ethics understood as universal abstract principles"
            orientation = "Rule-oriented"
        else:
            ethical_mode = "Pre-ethical"
            description = "Ethical dimension not yet articulated"
            orientation = "Neutral"

        return {
            "mode": ethical_mode,
            "description": description,
            "orientation": orientation,
            "principle": "倫理 = 倫 (relationship) + 理 (principle)"
        }

    def _analyze_spatiotemporal(self, text: str) -> Dict[str, Any]:
        """
        Analyze the spatiotemporal structure.

        Watsuji: Human existence is both spatial (climate, place) and temporal (history)
        """
        text_lower = text.lower()

        # Spatial indicators
        spatial_words = ["place", "space", "here", "where", "location", "environment", "climate", "land"]
        has_spatial = sum(1 for word in spatial_words if word in text_lower)

        # Temporal indicators
        temporal_words = ["time", "history", "when", "past", "future", "tradition", "change", "era"]
        has_temporal = sum(1 for word in temporal_words if word in text_lower)

        if has_spatial > 0 and has_temporal > 0:
            structure = "Spatiotemporal Unity"
            description = "Integration of climate (spatial) and history (temporal)"
        elif has_spatial > has_temporal:
            structure = "Spatial Emphasis"
            description = "Focus on place, environment, climate - 風土的存在"
        elif has_temporal > has_spatial:
            structure = "Temporal Emphasis"
            description = "Focus on history, time, tradition - 歴史的存在"
        else:
            structure = "Abstract"
            description = "Neither spatial nor temporal grounding evident"

        return {
            "structure": structure,
            "description": description,
            "note": "人間は風土的・歴史的存在 - Humans are climatic-historical beings"
        }

    def _detect_japanese_traits(self, text: str) -> List[str]:
        """
        Detect characteristics associated with Japanese culture in Watsuji's analysis.

        Japanese traits: Acceptance, harmony, resignation (諦念), sensitivity, relationality
        """
        text_lower = text.lower()
        traits = []

        # Acceptance and resignation (諦念 - teinen)
        if any(word in text_lower for word in ["accept", "resign", "let go", "flow", "fate"]):
            traits.append("諦念 (teinen) - Acceptance and resignation to natural flow")

        # Harmony (和 - wa)
        if any(word in text_lower for word in ["harmony", "peaceful", "accord", "unite", "together"]):
            traits.append("和 (wa) - Harmony and unity")

        # Sensitivity to atmosphere (雰囲気 - fun'iki)
        if any(word in text_lower for word in ["atmosphere", "mood", "feeling", "sense", "vibe"]):
            traits.append("雰囲気 (fun'iki) - Sensitivity to atmosphere and context")

        # Relational awareness (間柄 - aidagara)
        if any(word in text_lower for word in ["relationship", "between", "mutual", "reciprocal"]):
            traits.append("間柄 (aidagara) - Awareness of relational context")

        # Seasonal/cyclical awareness
        if any(word in text_lower for word in ["season", "cycle", "change", "impermanent", "transient"]):
            traits.append("無常 (mujō) - Awareness of impermanence and cycles")

        # Obligation/duty (義理 - giri)
        if any(word in text_lower for word in ["duty", "obligation", "giri", "ought", "must"]):
            traits.append("義理 (giri) - Sense of social obligation")

        if not traits:
            traits.append("Universal traits - not specifically Japanese")

        return traits

    def _construct_reasoning(
        self,
        relationality: Dict[str, Any],
        climate: Dict[str, Any],
        dialectic: Dict[str, Any],
        betweenness: Dict[str, Any],
        ethics: Dict[str, Any]
    ) -> str:
        """Construct Watsuji's ethical-climatic reasoning."""
        reasoning = (
            f"From Watsuji's perspective of 間柄 (aidagara/betweenness), this text reveals "
            f"{relationality['status']}. "
            f"The climate-cultural pattern suggests a {climate['type']} orientation: {climate['description']}. "
            f"In terms of the individual-totality dialectic, we find: {dialectic['description']}. "
        )

        # Add betweenness quality
        reasoning += f"The quality of 間 (ma/betweenness) is: {betweenness['description']}. "

        # Add ethical dimension
        reasoning += f"Ethically, this reflects {ethics['mode']}: {ethics['description']}. "

        # Conclude with Watsuji's core insight
        reasoning += (
            "人間 (ningen) is not an isolated individual, but fundamentally exists in the 'between' - "
            "in relationships, in climate, in history."
        )

        return reasoning
