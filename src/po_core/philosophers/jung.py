"""
Jung - Analytical Psychologist

Carl Gustav Jung (1875-1961)
Focus: Collective Unconscious, Archetypes, Individuation, Synchronicity

Key Concepts:
- Collective Unconscious: Universal, inherited repository of experiences
- Archetypes: Universal symbolic patterns (Shadow, Anima/Animus, Self, etc.)
- Individuation: The process of becoming one's true self
- Synchronicity: Meaningful coincidences beyond causality
- Psychological Types: Introversion/Extraversion, Four Functions
- Self vs Ego: The totality of psyche vs the conscious "I"
- Shadow: The repressed, unconscious aspects of personality
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Jung(Philosopher):
    """
    Jung's analytical psychology perspective.

    Analyzes prompts through the lens of archetypes, collective unconscious,
    individuation process, and psychological wholeness.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Carl Gustav Jung",
            description="Analytical psychologist focused on archetypes, collective unconscious, and individuation"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Jung's analytical psychology perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Jung's psychological analysis
        """
        # Perform Jungian analysis
        analysis = self._analyze_psyche(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Analytical Psychology",
            "archetypes_detected": analysis["archetypes"],
            "collective_unconscious_themes": analysis["collective_themes"],
            "individuation_stage": analysis["individuation"],
            "psychological_type": analysis["psych_type"],
            "shadow_integration": analysis["shadow"],
            "synchronicity_indicators": analysis["synchronicity"],
            "self_realization": analysis["self_realization"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Analytical Psychology",
                "focus": "Archetypes, individuation, and the collective unconscious"
            }
        }

    def _analyze_psyche(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Jungian psychological analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Detect archetypes
        archetypes = self._detect_archetypes(prompt)

        # Identify collective unconscious themes
        collective_themes = self._identify_collective_themes(prompt)

        # Assess individuation stage
        individuation = self._assess_individuation(prompt)

        # Determine psychological type
        psych_type = self._determine_psychological_type(prompt)

        # Check shadow integration
        shadow = self._check_shadow_integration(prompt)

        # Detect synchronicity
        synchronicity = self._detect_synchronicity(prompt)

        # Assess self-realization
        self_realization = self._assess_self_realization(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            archetypes, collective_themes, individuation, psych_type, shadow, self_realization
        )

        return {
            "reasoning": reasoning,
            "archetypes": archetypes,
            "collective_themes": collective_themes,
            "individuation": individuation,
            "psych_type": psych_type,
            "shadow": shadow,
            "synchronicity": synchronicity,
            "self_realization": self_realization
        }

    def _detect_archetypes(self, text: str) -> List[Dict[str, str]]:
        """
        Detect archetypal patterns in the text.

        Major archetypes: Shadow, Anima/Animus, Self, Persona, Hero, Mother, Wise Old Man, Trickster
        """
        text_lower = text.lower()
        detected = []

        # Shadow archetype (repressed, dark side)
        shadow_words = ["dark", "hidden", "secret", "repressed", "deny", "shadow", "evil", "shame"]
        if any(word in text_lower for word in shadow_words):
            detected.append({
                "archetype": "Shadow",
                "description": "The repressed, unconscious aspects - what we refuse to acknowledge"
            })

        # Anima/Animus (contrasexual aspect)
        anima_words = ["feminine", "masculine", "inner woman", "inner man", "soul", "muse"]
        if any(word in text_lower for word in anima_words):
            detected.append({
                "archetype": "Anima/Animus",
                "description": "The contrasexual element - bridge to the unconscious"
            })

        # Hero archetype (quest, transformation)
        hero_words = ["journey", "quest", "challenge", "overcome", "hero", "battle", "victory", "struggle"]
        if any(word in text_lower for word in hero_words):
            detected.append({
                "archetype": "Hero",
                "description": "The transformative journey - ego development through trials"
            })

        # Wise Old Man/Woman (wisdom, guidance)
        wisdom_words = ["wisdom", "guide", "teacher", "mentor", "sage", "elder", "know", "understand"]
        if any(word in text_lower for word in wisdom_words):
            detected.append({
                "archetype": "Wise Old Man/Woman",
                "description": "The voice of wisdom - knowledge and guidance from the unconscious"
            })

        # Mother archetype (nurturing, origin)
        mother_words = ["mother", "birth", "nurture", "care", "origin", "womb", "fertile", "nourish"]
        if any(word in text_lower for word in mother_words):
            detected.append({
                "archetype": "Mother",
                "description": "The Great Mother - source of life, nurturing, and containment"
            })

        # Trickster archetype (chaos, disruption)
        trickster_words = ["trick", "chaos", "disrupt", "fool", "joke", "paradox", "absurd"]
        if any(word in text_lower for word in trickster_words):
            detected.append({
                "archetype": "Trickster",
                "description": "The agent of chaos - disrupts order to enable transformation"
            })

        # Self archetype (wholeness, integration)
        self_words = ["whole", "complete", "unity", "integrated", "center", "balance", "harmony"]
        if any(word in text_lower for word in self_words):
            detected.append({
                "archetype": "Self",
                "description": "The archetype of wholeness - totality of the psyche"
            })

        # Persona (social mask)
        persona_words = ["mask", "role", "public", "appearance", "pretend", "act", "performance"]
        if any(word in text_lower for word in persona_words):
            detected.append({
                "archetype": "Persona",
                "description": "The social mask - how we present ourselves to the world"
            })

        if not detected:
            detected.append({
                "archetype": "Ego",
                "description": "The conscious 'I' - center of consciousness (default archetype)"
            })

        return detected

    def _identify_collective_themes(self, text: str) -> List[str]:
        """
        Identify themes from the collective unconscious.

        Universal patterns that appear across cultures and times.
        """
        text_lower = text.lower()
        themes = []

        # Mythological themes
        myth_words = ["myth", "legend", "story", "tale", "ancient", "eternal", "timeless"]
        if any(word in text_lower for word in myth_words):
            themes.append("Mythological patterns - echoes of universal human narratives")

        # Death and rebirth
        rebirth_words = ["death", "rebirth", "transformation", "end", "beginning", "phoenix", "resurrection"]
        if any(word in text_lower for word in rebirth_words):
            themes.append("Death and rebirth - the eternal cycle of transformation")

        # The quest/journey
        quest_words = ["journey", "path", "way", "seek", "search", "find", "discover"]
        if any(word in text_lower for word in quest_words):
            themes.append("The hero's journey - universal pattern of growth and return")

        # Opposites and paradox
        paradox_words = ["opposite", "both", "neither", "paradox", "contradiction", "light and dark"]
        if any(word in text_lower for word in paradox_words):
            themes.append("Coincidentia oppositorum - unity of opposites")

        # The numinous (spiritual/sacred)
        numinous_words = ["sacred", "divine", "spiritual", "transcendent", "holy", "mystical"]
        if any(word in text_lower for word in numinous_words):
            themes.append("The numinous - encounter with the sacred dimension")

        if not themes:
            themes.append("Personal unconscious material - individual rather than collective")

        return themes

    def _assess_individuation(self, text: str) -> Dict[str, Any]:
        """
        Assess the stage of individuation (becoming one's true self).

        Stages: Persona identification -> Shadow confrontation -> Anima/Animus integration -> Self realization
        """
        text_lower = text.lower()

        # Early stage: Persona identification
        persona_indicators = ["should", "supposed to", "role", "expected", "normal"]
        persona_count = sum(1 for word in persona_indicators if word in text_lower)

        # Middle stage: Shadow work
        shadow_indicators = ["dark", "hidden", "admit", "acknowledge", "confront", "accept"]
        shadow_count = sum(1 for word in shadow_indicators if word in text_lower)

        # Advanced stage: Integration
        integration_indicators = ["integrate", "whole", "balance", "accept all", "unity", "complete"]
        integration_count = sum(1 for word in integration_indicators if word in text_lower)

        # Self-realization stage
        self_indicators = ["true self", "authentic", "realized", "awakened", "centered"]
        self_count = sum(1 for word in self_indicators if word in text_lower)

        # Determine stage
        if self_count > 0 or integration_count >= 2:
            stage = "Self-Realization"
            description = "Approaching wholeness - integration of conscious and unconscious"
            level = "Advanced"
        elif shadow_count >= 2:
            stage = "Shadow Integration"
            description = "Confronting the repressed - crucial middle stage"
            level = "Intermediate"
        elif persona_count >= 2:
            stage = "Persona Identification"
            description = "Identified with social roles - early stage"
            level = "Beginning"
        else:
            stage = "Unconscious"
            description = "Pre-individuation - not yet begun the conscious journey"
            level = "Initial"

        return {
            "stage": stage,
            "description": description,
            "level": level,
            "jungian_note": "Individuation is the process of becoming who you truly are"
        }

    def _determine_psychological_type(self, text: str) -> Dict[str, Any]:
        """
        Determine psychological type based on Jung's typology.

        Attitude: Introversion vs Extraversion
        Functions: Thinking, Feeling, Sensation, Intuition
        """
        text_lower = text.lower()

        # Introversion vs Extraversion
        intro_words = ["inner", "reflect", "alone", "private", "internal", "withdraw"]
        extra_words = ["outer", "people", "social", "external", "interact", "engage"]

        intro_count = sum(1 for word in intro_words if word in text_lower)
        extra_count = sum(1 for word in extra_words if word in text_lower)

        if intro_count > extra_count:
            attitude = "Introverted"
        elif extra_count > intro_count:
            attitude = "Extraverted"
        else:
            attitude = "Balanced"

        # Four functions
        thinking_words = ["think", "logic", "reason", "analyze", "rational"]
        feeling_words = ["feel", "emotion", "value", "heart", "care"]
        sensation_words = ["sense", "physical", "concrete", "real", "tangible", "see", "hear"]
        intuition_words = ["intuition", "possibility", "future", "imagine", "vision", "potential"]

        thinking_count = sum(1 for word in thinking_words if word in text_lower)
        feeling_count = sum(1 for word in feeling_words if word in text_lower)
        sensation_count = sum(1 for word in sensation_words if word in text_lower)
        intuition_count = sum(1 for word in intuition_words if word in text_lower)

        # Determine dominant function
        function_scores = {
            "Thinking": thinking_count,
            "Feeling": feeling_count,
            "Sensation": sensation_count,
            "Intuition": intuition_count
        }
        dominant_function = max(function_scores, key=function_scores.get)

        return {
            "attitude": attitude,
            "dominant_function": dominant_function,
            "type_description": f"{attitude} {dominant_function}",
            "note": "Psychological type influences how we perceive and judge reality"
        }

    def _check_shadow_integration(self, text: str) -> Dict[str, Any]:
        """
        Check the level of shadow integration.

        Shadow = repressed, denied, unconscious aspects of personality
        """
        text_lower = text.lower()

        # Denial indicators
        denial_words = ["not me", "never", "refuse", "deny", "reject", "impossible"]
        denial_count = sum(1 for word in denial_words if word in text_lower)

        # Projection indicators (seeing shadow in others)
        projection_words = ["they are", "everyone else", "those people", "them"]
        projection_count = sum(1 for word in projection_words if word in text_lower)

        # Integration indicators
        integration_words = ["acknowledge", "accept", "admit", "own", "recognize", "embrace"]
        integration_count = sum(1 for word in integration_words if word in text_lower)

        # Dark side acknowledgment
        dark_words = ["dark", "shadow", "flaw", "weakness", "imperfect"]
        dark_count = sum(1 for word in dark_words if word in text_lower)

        if integration_count >= 2 or (dark_count > 0 and integration_count > 0):
            status = "Integrating"
            level = "High"
            note = "Conscious acknowledgment of shadow - healthy integration"
        elif projection_count >= 2:
            status = "Projecting"
            level = "Low"
            note = "Shadow projected onto others - unconscious disowning"
        elif denial_count >= 2:
            status = "Denying"
            level = "Very Low"
            note = "Active shadow denial - strong repression"
        else:
            status = "Unconscious"
            level = "Medium"
            note = "Shadow neither integrated nor actively denied - neutral state"

        return {
            "status": status,
            "level": level,
            "note": note,
            "jungian_principle": "Until you make the unconscious conscious, it will direct your life"
        }

    def _detect_synchronicity(self, text: str) -> Dict[str, Any]:
        """
        Detect indicators of synchronicity (meaningful coincidence).

        Synchronicity = acausal connecting principle, meaningful coincidence
        """
        text_lower = text.lower()

        # Synchronicity indicators
        sync_words = ["coincidence", "meaningful", "connected", "synchronicity", "fate", "destiny"]
        has_sync = any(word in text_lower for word in sync_words)

        # Meaning + Coincidence together
        has_meaning = "meaning" in text_lower or "significant" in text_lower
        has_coincidence = "coincidence" in text_lower or "chance" in text_lower or "happened" in text_lower

        if has_sync or (has_meaning and has_coincidence):
            present = True
            description = "Synchronicity detected - meaningful acausal connection"
        else:
            present = False
            description = "No synchronicity - causality-based understanding"

        return {
            "present": present,
            "description": description,
            "principle": "Synchronicity reveals the meaningful connection between psyche and matter"
        }

    def _assess_self_realization(self, text: str) -> Dict[str, Any]:
        """
        Assess the level of Self-realization.

        Self (capital S) = the archetype of wholeness, totality of psyche
        """
        text_lower = text.lower()

        # Self indicators
        self_words = ["whole", "complete", "integrated", "unified", "centered", "balanced"]
        self_count = sum(1 for word in self_words if word in text_lower)

        # Fragmentation indicators
        fragment_words = ["divided", "split", "torn", "conflicted", "scattered", "fragmented"]
        fragment_count = sum(1 for word in fragment_words if word in text_lower)

        # Transcendence indicators
        transcend_words = ["transcend", "beyond", "higher", "spiritual", "enlightened"]
        transcend_count = sum(1 for word in transcend_words if word in text_lower)

        if self_count >= 2 or transcend_count >= 1:
            level = "High - Approaching Self"
            status = "Moving toward wholeness and integration"
        elif fragment_count >= 2:
            level = "Low - Fragmented"
            status = "Experiencing psychic fragmentation"
        else:
            level = "Medium - Ego-consciousness"
            status = "Identified with ego, Self not yet realized"

        return {
            "level": level,
            "status": status,
            "note": "The Self is both the center and circumference of the psyche"
        }

    def _construct_reasoning(
        self,
        archetypes: List[Dict[str, str]],
        collective_themes: List[str],
        individuation: Dict[str, Any],
        psych_type: Dict[str, Any],
        shadow: Dict[str, Any],
        self_realization: Dict[str, Any]
    ) -> str:
        """Construct Jungian analytical reasoning."""
        primary_archetype = archetypes[0]["archetype"]
        archetype_desc = archetypes[0]["description"]

        reasoning = (
            f"From a Jungian analytical perspective, this text activates the {primary_archetype} archetype: "
            f"{archetype_desc}. "
            f"The individuation stage appears to be '{individuation['stage']}' - {individuation['description']}. "
            f"The psychological type suggests a {psych_type['type_description']} orientation. "
        )

        # Add shadow analysis
        reasoning += f"Regarding shadow integration: {shadow['note']}. "

        # Add collective unconscious
        if collective_themes:
            reasoning += f"This taps into the collective unconscious: {collective_themes[0]}. "

        # Add Self-realization
        reasoning += f"Self-realization assessment: {self_realization['status']}. "

        # Conclude with Jungian wisdom
        reasoning += (
            "The psyche seeks wholeness through the integration of conscious and unconscious elements."
        )

        return reasoning
