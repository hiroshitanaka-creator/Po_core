"""
Sartre - Existentialist Philosopher

Jean-Paul Sartre (1905-1980)
Focus: Existence precedes Essence, Freedom, Responsibility, Bad Faith

Key Concepts:
- Existence precedes essence: We create our own nature through choices
- Radical freedom: We are "condemned to be free"
- Responsibility: We are responsible for our choices and the world
- Bad faith (mauvaise foi): Self-deception to escape freedom
- For-itself vs In-itself: Conscious being vs thing-like being
- The gaze of the Other: How others' perception affects us
- Anguish (angoisse): The dizziness of freedom
- Engagement (engagement): Commitment and action
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Sartre(Philosopher):
    """
    Sartre's existentialist perspective.

    Analyzes prompts through the lens of freedom, responsibility,
    choice, and authentic existence vs bad faith.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Jean-Paul Sartre",
            description="Existentialist focused on freedom, responsibility, and 'existence precedes essence'"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Sartre's existentialist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Sartre's existentialist analysis
        """
        # Store context if provided
        if context:
            self._context.update(context)

        # Perform existentialist analysis
        analysis = self._analyze_existence(prompt)

        # Identify tensions and contradictions
        tension = self._identify_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Existentialist",
            "tension": tension,
            "freedom_assessment": analysis["freedom"],
            "responsibility_check": analysis["responsibility"],
            "bad_faith_indicators": analysis["bad_faith"],
            "mode_of_being": analysis["mode_of_being"],
            "engagement_level": analysis["engagement"],
            "anguish_present": analysis["anguish"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Existentialist analysis",
                "focus": "Freedom, choice, responsibility, and bad faith"
            }
        }

    def _analyze_existence(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Sartrean existentialist analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess freedom
        freedom = self._assess_freedom(prompt)

        # Check for responsibility
        responsibility = self._check_responsibility(prompt)

        # Detect bad faith
        bad_faith = self._detect_bad_faith(prompt)

        # Determine mode of being
        mode_of_being = self._determine_mode_of_being(prompt)

        # Assess engagement
        engagement = self._assess_engagement(prompt)

        # Check for anguish
        anguish = self._check_anguish(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            freedom, responsibility, bad_faith, mode_of_being, engagement, anguish
        )

        return {
            "reasoning": reasoning,
            "freedom": freedom,
            "responsibility": responsibility,
            "bad_faith": bad_faith,
            "mode_of_being": mode_of_being,
            "engagement": engagement,
            "anguish": anguish
        }

    def _assess_freedom(self, text: str) -> Dict[str, Any]:
        """Assess the presence and nature of freedom in the text."""
        text_lower = text.lower()

        # Freedom indicators
        freedom_words = ["choice", "choose", "decide", "freedom", "free", "can", "able", "will"]
        constraint_words = ["must", "have to", "forced", "cannot", "unable", "bound", "determined"]

        freedom_count = sum(1 for word in freedom_words if word in text_lower)
        constraint_count = sum(1 for word in constraint_words if word in text_lower)

        if freedom_count > constraint_count:
            status = "High freedom awareness - choice and possibility are recognized"
            level = "High"
        elif constraint_count > freedom_count:
            status = "Constrained - emphasis on limitation rather than freedom"
            level = "Low"
        else:
            status = "Neutral - freedom and constraint in tension"
            level = "Medium"

        # Check for radical freedom
        if "free" in text_lower and any(word in text_lower for word in ["absolutely", "totally", "completely"]):
            radical = True
            status += " (Radical freedom acknowledged)"
        else:
            radical = False

        return {
            "level": level,
            "status": status,
            "radical_freedom": radical,
            "sartrean_note": "We are condemned to be free - freedom is inescapable"
        }

    def _check_responsibility(self, text: str) -> Dict[str, Any]:
        """Check for awareness of responsibility."""
        text_lower = text.lower()

        # Responsibility indicators
        resp_words = ["responsible", "responsibility", "accountable", "duty", "obligation"]
        evasion_words = ["not my fault", "they made me", "had no choice", "couldn't help"]

        has_responsibility = any(word in text_lower for word in resp_words)
        has_evasion = any(phrase in text_lower for phrase in evasion_words)

        if has_responsibility and not has_evasion:
            status = "Responsibility acknowledged"
            level = "High"
        elif has_evasion or (not has_responsibility and "choice" not in text_lower):
            status = "Responsibility evaded or unacknowledged"
            level = "Low"
        else:
            status = "Implicit responsibility through choice"
            level = "Medium"

        return {
            "level": level,
            "status": status,
            "sartrean_note": "To choose is to take responsibility for the entire world"
        }

    def _detect_bad_faith(self, text: str) -> List[str]:
        """
        Detect indicators of bad faith (mauvaise foi).

        Bad faith = self-deception to escape freedom and responsibility.
        """
        text_lower = text.lower()
        indicators = []

        # Type 1: Claiming determinism
        if any(phrase in text_lower for phrase in ["i am just", "that's just how i am", "i was born", "it's my nature"]):
            indicators.append("Essence before existence - claiming fixed nature (bad faith)")

        # Type 2: Blaming others or circumstances
        if any(phrase in text_lower for phrase in ["they made me", "society", "everyone else", "the system"]):
            indicators.append("Blaming external forces - denying agency (bad faith)")

        # Type 3: Claiming no choice
        if any(phrase in text_lower for phrase in ["had no choice", "couldn't do anything", "impossible"]):
            indicators.append("Denying choice - fleeing from freedom (bad faith)")

        # Type 4: Conformity to roles
        if any(word in text_lower for word in ["supposed to", "should", "must", "expected"]):
            indicators.append("Role-playing - hiding behind social expectations (possible bad faith)")

        # Type 5: Passive voice / avoiding agency
        if any(phrase in text_lower for phrase in ["it happened", "things are", "that's life"]):
            indicators.append("Passive framing - obscuring personal agency (bad faith tendency)")

        if not indicators:
            indicators.append("No obvious bad faith detected - authentic engagement possible")

        return indicators

    def _determine_mode_of_being(self, text: str) -> str:
        """
        Determine the mode of being: For-itself (conscious) vs In-itself (thing-like).

        For-itself (pour-soi): Conscious being, aware, choosing
        In-itself (en-soi): Thing-like being, passive, determined
        """
        text_lower = text.lower()

        # For-itself indicators
        consciousness_words = ["think", "choose", "feel", "decide", "aware", "conscious", "i"]

        # In-itself indicators
        thing_words = ["is", "are", "fixed", "determined", "given", "fact"]

        for_itself_count = sum(1 for word in consciousness_words if word in text_lower)
        in_itself_count = sum(1 for word in thing_words if word in text_lower)

        if for_itself_count > in_itself_count:
            return "For-itself (pour-soi) - Conscious, choosing being"
        elif in_itself_count > for_itself_count:
            return "In-itself (en-soi) - Thing-like, determined being"
        else:
            return "Mixed - Tension between consciousness and facticity"

    def _assess_engagement(self, text: str) -> Dict[str, Any]:
        """
        Assess the level of engagement (commitment to action).

        Sartre emphasizes that existence requires engagement with the world.
        """
        text_lower = text.lower()

        # Engagement indicators
        action_words = ["do", "act", "make", "create", "change", "fight", "commit"]
        passivity_words = ["wait", "hope", "wish", "dream", "if only", "someday"]

        action_count = sum(1 for word in action_words if word in text_lower)
        passivity_count = sum(1 for word in passivity_words if word in text_lower)

        if action_count > passivity_count:
            level = "High - Active engagement"
            note = "Authentic engagement with the world through action"
        elif passivity_count > action_count:
            level = "Low - Passive or contemplative"
            note = "Lack of engagement - existence requires action"
        else:
            level = "Medium - Potential for engagement"
            note = "Poised between action and passivity"

        return {
            "level": level,
            "note": note,
            "sartrean_principle": "Existence is not given; it must be created through action"
        }

    def _check_anguish(self, text: str) -> Dict[str, Any]:
        """
        Check for the presence of anguish (angoisse).

        Anguish = the dizziness of freedom, awareness of responsibility.
        """
        text_lower = text.lower()

        # Anguish indicators
        anguish_words = ["anxiety", "anguish", "dread", "weight", "burden", "overwhelm"]
        freedom_words = ["choice", "decide", "responsibility", "free"]

        has_anguish = any(word in text_lower for word in anguish_words)
        has_freedom = any(word in text_lower for word in freedom_words)

        if has_anguish and has_freedom:
            present = True
            note = "Anguish present - authentic awareness of freedom's weight"
        elif has_anguish:
            present = True
            note = "Existential discomfort - possible anguish"
        else:
            present = False
            note = "No explicit anguish - may indicate bad faith or innocence"

        return {
            "present": present,
            "note": note,
            "sartrean_insight": "Anguish is the recognition of absolute freedom and responsibility"
        }

    def _identify_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify Sartrean tensions and contradictions.

        Args:
            analysis: The analysis results

        Returns:
            Dictionary containing tension level, description, and elements
        """
        tension_elements = []

        # Tension from bad faith
        bad_faith = analysis["bad_faith"]
        if len(bad_faith) > 0:
            for indicator in bad_faith:
                tension_elements.append(f"Bad faith present: {indicator}")

        # Tension from denied freedom
        freedom = analysis["freedom"]
        if "Denied" in freedom["level"]:
            tension_elements.append("Freedom denied - refusing to acknowledge radical freedom")
        elif "Limited" in freedom["level"]:
            tension_elements.append("Freedom limited - not fully recognizing absolute freedom")

        # Tension from avoided responsibility
        responsibility = analysis["responsibility"]
        if "Avoided" in responsibility["level"]:
            tension_elements.append("Responsibility avoided - refusing to acknowledge accountability for choices")
        elif "Limited" in responsibility["level"]:
            tension_elements.append("Limited responsibility - not fully accepting existential burden")

        # Tension from in-itself mode of being
        mode_of_being = analysis["mode_of_being"]
        if "In-itself" in mode_of_being:
            tension_elements.append("In-itself mode - reducing self to thing-like existence, denying consciousness")

        # Tension from lack of engagement
        engagement = analysis["engagement"]
        if "Disengaged" in engagement["level"] or "Low" in engagement["level"]:
            tension_elements.append("Lack of engagement - withdrawal from commitment and action")

        # Tension from lack of anguish
        anguish = analysis["anguish"]
        if not anguish["present"]:
            tension_elements.append("No anguish - may indicate bad faith or unawareness of freedom's weight")

        # Determine tension level
        tension_count = len(tension_elements)
        if tension_count == 0:
            level = "Very Low"
            description = "No significant tensions - authentic existence with acknowledged freedom and responsibility"
        elif tension_count == 1:
            level = "Low"
            description = "Minor tension detected in existential analysis"
        elif tension_count == 2:
            level = "Moderate"
            description = "Moderate tensions between authentic existence and bad faith"
        elif tension_count <= 4:
            level = "High"
            description = "Significant tensions - substantial flight from freedom and responsibility"
        else:
            level = "Very High"
            description = "Severe tensions - dominated by bad faith and denial of existential condition"

        return {
            "level": level,
            "description": description,
            "elements": tension_elements
        }

    def _construct_reasoning(
        self,
        freedom: Dict[str, Any],
        responsibility: Dict[str, Any],
        bad_faith: List[str],
        mode_of_being: str,
        engagement: Dict[str, Any],
        anguish: Dict[str, Any]
    ) -> str:
        """Construct Sartrean existentialist reasoning."""
        reasoning = (
            f"From a Sartrean existentialist perspective, this text reveals a {freedom['level'].lower()} "
            f"degree of freedom awareness. {freedom['status']}. "
            f"Regarding responsibility: {responsibility['status']}. "
            f"The mode of being appears as: {mode_of_being}. "
        )

        # Add bad faith analysis
        primary_bad_faith = bad_faith[0]
        if "No obvious bad faith" in primary_bad_faith:
            reasoning += "Authentic existence is possible here. "
        else:
            reasoning += f"However, signs of bad faith emerge: {primary_bad_faith}. "

        # Add engagement
        reasoning += f"Engagement level: {engagement['level']}. "

        # Add anguish
        if anguish['present']:
            reasoning += f"Anguish is present, indicating authentic confrontation with freedom. "
        else:
            reasoning += "The absence of anguish may suggest flight from freedom. "

        # Conclude with Sartrean principle
        reasoning += "Remember: existence precedes essence - we are nothing but what we make of ourselves."

        return reasoning
