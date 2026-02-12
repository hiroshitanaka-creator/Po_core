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
- The Look (le regard): Being seen objectifies us
- Nausea (la nausée): Confronting the absurd contingency of existence
- Facticity and transcendence: The tension between given facts and projects
- Being-for-others: Our being as it appears to others
- Shame and pride: Responses to the Look
- The body: Three ontological dimensions of embodiment
- Situation: The concrete context of freedom
- Project: Fundamental life project and choices
- Condemned to freedom: The weight of absolute freedom
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
            description="Existentialist focused on freedom, responsibility, and 'existence precces essence'",
        )
        self.tradition = "Existentialism"
        self.key_concepts = [
            "existence precedes essence",
            "radical freedom",
            "bad faith (mauvaise foi)",
            "being-for-itself",
            "anguish",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Sartre's existentialist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Sartre's existentialist analysis
        """
        # Perform existentialist analysis
        analysis = self._analyze_existence(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

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
            "the_look": analysis["the_look"],
            "nausea": analysis["nausea"],
            "facticity_transcendence": analysis["facticity_transcendence"],
            "being_for_others": analysis["being_for_others"],
            "shame_pride": analysis["shame_pride"],
            "body_dimensions": analysis["body"],
            "situation": analysis["situation"],
            "project": analysis["project"],
            "condemned_to_freedom": analysis["condemned_to_freedom"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Existentialist analysis",
                "focus": "Freedom, choice, responsibility, and bad faith",
            },
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

        # Analyze the Look
        the_look = self._analyze_the_look(prompt)

        # Analyze nausea
        nausea = self._analyze_nausea(prompt)

        # Analyze facticity and transcendence
        facticity_transcendence = self._analyze_facticity_transcendence(prompt)

        # Analyze being-for-others
        being_for_others = self._analyze_being_for_others(prompt)

        # Analyze shame and pride
        shame_pride = self._analyze_shame_pride(prompt)

        # Analyze the body
        body = self._analyze_body(prompt)

        # Analyze situation
        situation = self._analyze_situation(prompt)

        # Analyze project
        project = self._analyze_project(prompt)

        # Analyze condemned to freedom
        condemned_to_freedom = self._analyze_condemned_to_freedom(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            freedom,
            responsibility,
            bad_faith,
            mode_of_being,
            engagement,
            anguish,
            the_look,
            nausea,
            facticity_transcendence,
            being_for_others,
            shame_pride,
        )

        return {
            "reasoning": reasoning,
            "freedom": freedom,
            "responsibility": responsibility,
            "bad_faith": bad_faith,
            "mode_of_being": mode_of_being,
            "engagement": engagement,
            "anguish": anguish,
            "the_look": the_look,
            "nausea": nausea,
            "facticity_transcendence": facticity_transcendence,
            "being_for_others": being_for_others,
            "shame_pride": shame_pride,
            "body": body,
            "situation": situation,
            "project": project,
            "condemned_to_freedom": condemned_to_freedom,
        }

    def _assess_freedom(self, text: str) -> Dict[str, Any]:
        """
        Assess the presence and nature of freedom in the text.

        For Sartre, freedom is not just a property we have - it is what we are.
        We are freedom itself, and this is both our glory and our burden.
        """
        text_lower = text.lower()

        # Freedom indicators
        freedom_words = [
            "choice",
            "choose",
            "decide",
            "freedom",
            "free",
            "can",
            "able",
            "will",
        ]
        constraint_words = [
            "must",
            "have to",
            "forced",
            "cannot",
            "unable",
            "bound",
            "determined",
        ]

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
        if "free" in text_lower and any(
            word in text_lower for word in ["absolutely", "totally", "completely"]
        ):
            radical = True
            status += " (Radical freedom acknowledged)"
        else:
            radical = False

        return {
            "level": level,
            "status": status,
            "radical_freedom": radical,
            "freedom_score": freedom_count,
            "constraint_score": constraint_count,
            "sartrean_note": "We are condemned to be free - freedom is inescapable",
            "principle": "Freedom is not something we have; it is what we are",
        }

    def _check_responsibility(self, text: str) -> Dict[str, Any]:
        """
        Check for awareness of responsibility.

        For Sartre, to choose is to take responsibility not just for oneself
        but for all humanity. In choosing myself, I choose for all.
        """
        text_lower = text.lower()

        # Responsibility indicators
        resp_words = [
            "responsible",
            "responsibility",
            "accountable",
            "duty",
            "obligation",
        ]
        evasion_words = [
            "not my fault",
            "they made me",
            "had no choice",
            "couldn't help",
        ]

        has_responsibility = any(word in text_lower for word in resp_words)
        has_evasion = any(phrase in text_lower for phrase in evasion_words)

        if has_responsibility and not has_evasion:
            status = "Responsibility acknowledged"
            level = "High"
            authenticity = "Authentic responsibility"
        elif has_evasion or (not has_responsibility and "choice" not in text_lower):
            status = "Responsibility evaded or unacknowledged"
            level = "Low"
            authenticity = "Flight from responsibility"
        else:
            status = "Implicit responsibility through choice"
            level = "Medium"
            authenticity = "Potential for authentic responsibility"

        return {
            "level": level,
            "status": status,
            "authenticity": authenticity,
            "sartrean_note": "To choose is to take responsibility for the entire world",
            "principle": "In choosing myself, I choose for all humanity",
        }

    def _detect_bad_faith(self, text: str) -> List[str]:
        """
        Detect indicators of bad faith (mauvaise foi).

        Bad faith = self-deception to escape freedom and responsibility.
        It is a lie to oneself that one is aware of but refuses to acknowledge.
        """
        text_lower = text.lower()
        indicators = []

        # Type 1: Claiming determinism
        if any(
            phrase in text_lower
            for phrase in [
                "i am just",
                "that's just how i am",
                "i was born",
                "it's my nature",
            ]
        ):
            indicators.append(
                "Essence before existence - claiming fixed nature (bad faith)"
            )

        # Type 2: Blaming others or circumstances
        if any(
            phrase in text_lower
            for phrase in ["they made me", "society", "everyone else", "the system"]
        ):
            indicators.append("Blaming external forces - denying agency (bad faith)")

        # Type 3: Claiming no choice
        if any(
            phrase in text_lower
            for phrase in ["had no choice", "couldn't do anything", "impossible"]
        ):
            indicators.append("Denying choice - fleeing from freedom (bad faith)")

        # Type 4: Conformity to roles
        if any(
            word in text_lower for word in ["supposed to", "should", "must", "expected"]
        ):
            indicators.append(
                "Role-playing - hiding behind social expectations (possible bad faith)"
            )

        # Type 5: Passive voice / avoiding agency
        if any(
            phrase in text_lower
            for phrase in ["it happened", "things are", "that's life"]
        ):
            indicators.append(
                "Passive framing - obscuring personal agency (bad faith tendency)"
            )

        # Type 6: The waiter in bad faith - over-identification with role
        if any(phrase in text_lower for phrase in ["i'm just a", "as a", "my role"]):
            indicators.append("Over-identification with social role (bad faith)")

        # Type 7: Spirit of seriousness - treating values as objective
        if any(
            phrase in text_lower
            for phrase in ["objectively", "absolutely right", "obviously wrong"]
        ):
            indicators.append(
                "Spirit of seriousness - treating values as objective facts (bad faith)"
            )

        if not indicators:
            indicators.append(
                "No obvious bad faith detected - authentic engagement possible"
            )

        return indicators

    def _determine_mode_of_being(self, text: str) -> str:
        """
        Determine the mode of being: For-itself (conscious) vs In-itself (thing-like).

        For-itself (pour-soi): Conscious being, aware, choosing, always at a distance from itself
        In-itself (en-soi): Thing-like being, passive, determined, self-identical
        For-others (pour-autrui): Being as it appears to others
        """
        text_lower = text.lower()

        # For-itself indicators
        consciousness_words = [
            "think",
            "choose",
            "feel",
            "decide",
            "aware",
            "conscious",
            "i",
        ]

        # In-itself indicators
        thing_words = ["is", "are", "fixed", "determined", "given", "fact"]

        # For-others indicators
        others_words = ["they see me", "others think", "how i appear", "reputation"]

        for_itself_count = sum(1 for word in consciousness_words if word in text_lower)
        in_itself_count = sum(1 for word in thing_words if word in text_lower)
        for_others_count = sum(1 for phrase in others_words if phrase in text_lower)

        if for_others_count >= 2:
            return "For-others (pour-autrui) - Being as object for the Other's gaze"
        elif for_itself_count > in_itself_count:
            return "For-itself (pour-soi) - Conscious, choosing being"
        elif in_itself_count > for_itself_count:
            return "In-itself (en-soi) - Thing-like, determined being"
        else:
            return "Mixed - Tension between consciousness and facticity"

    def _assess_engagement(self, text: str) -> Dict[str, Any]:
        """
        Assess the level of engagement (commitment to action).

        Sartre emphasizes that existence requires engagement with the world.
        We must commit ourselves, take sides, act in the world.
        """
        text_lower = text.lower()

        # Engagement indicators
        action_words = ["do", "act", "make", "create", "change", "fight", "commit"]
        passivity_words = ["wait", "hope", "wish", "dream", "if only", "someday"]

        action_count = sum(1 for word in action_words if word in text_lower)
        passivity_count = sum(1 for word in passivity_words if word in text_lower)

        # Political/social engagement indicators
        political_words = ["struggle", "resist", "solidarity", "revolution", "justice"]
        political_count = sum(1 for word in political_words if word in text_lower)

        if action_count > passivity_count and political_count >= 1:
            level = "Very High - Political engagement"
            note = "Authentic political engagement - existence committed to action"
        elif action_count > passivity_count:
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
            "political_engagement": political_count >= 1,
            "sartrean_principle": "Existence is not given; it must be created through action",
            "principle": "The intellectual must commit - there is no spectator position",
        }

    def _check_anguish(self, text: str) -> Dict[str, Any]:
        """
        Check for the presence of anguish (angoisse).

        Anguish = the dizziness of freedom, awareness of responsibility.
        It is not fear of something external but vertigo before one's own freedom.
        """
        text_lower = text.lower()

        # Anguish indicators
        anguish_words = ["anxiety", "anguish", "dread", "weight", "burden", "overwhelm"]
        freedom_words = ["choice", "decide", "responsibility", "free"]

        has_anguish = any(word in text_lower for word in anguish_words)
        has_freedom = any(word in text_lower for word in freedom_words)

        # Vertigo indicators
        vertigo_words = ["dizzy", "vertigo", "abyss", "precipice", "falling"]
        has_vertigo = any(word in text_lower for word in vertigo_words)

        if has_anguish and has_freedom:
            present = True
            note = "Anguish present - authentic awareness of freedom's weight"
            intensity = "High"
        elif has_vertigo:
            present = True
            note = "Vertigo of freedom - the dizziness before possibilities"
            intensity = "Very High"
        elif has_anguish:
            present = True
            note = "Existential discomfort - possible anguish"
            intensity = "Medium"
        else:
            present = False
            note = "No explicit anguish - may indicate bad faith or innocence"
            intensity = "None"

        return {
            "present": present,
            "note": note,
            "intensity": intensity,
            "sartrean_insight": "Anguish is the recognition of absolute freedom and responsibility",
            "principle": "Anguish: the vertigo that seizes us before our own possibilities",
        }

    def _analyze_the_look(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Look (le regard) - being seen by the Other.

        The Look of the Other transforms me from subject to object.
        I become aware of myself as I am for the Other - frozen, objectified.
        The Look reveals the dimension of being-for-others.
        """
        text_lower = text.lower()

        # Being seen indicators
        seen_words = [
            "seen",
            "watched",
            "observed",
            "gaze",
            "stare",
            "look at me",
            "eyes",
            "staring",
            "watching me",
        ]
        seen_count = sum(1 for phrase in seen_words if phrase in text_lower)

        # Objectification indicators
        object_words = [
            "judged",
            "evaluated",
            "assessed",
            "labeled",
            "categorized",
            "they think i am",
            "see me as",
        ]
        object_count = sum(1 for phrase in object_words if phrase in text_lower)

        # Self-consciousness indicators
        self_conscious_words = [
            "self-conscious",
            "aware of myself",
            "how do i look",
            "what do they think",
            "embarrassed",
        ]
        self_conscious_count = sum(
            1 for phrase in self_conscious_words if phrase in text_lower
        )

        if seen_count >= 2 or object_count >= 2:
            status = "The Look is Present"
            description = "The gaze of the Other objectifies - subject becomes object"
            mode = "Being-for-others dominant"
        elif seen_count >= 1 and self_conscious_count >= 1:
            status = "Awareness of the Look"
            description = "Self-consciousness under the gaze of the Other"
            mode = "Tension between for-itself and for-others"
        elif self_conscious_count >= 1:
            status = "Self-consciousness Present"
            description = "Awareness of oneself as potential object"
            mode = "Pre-reflective awareness of others"
        else:
            status = "The Look Not Explicit"
            description = "Being-for-others not thematized"
            mode = "For-itself emphasized"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "seen_score": seen_count,
            "objectification_score": object_count,
            "self_consciousness": self_conscious_count >= 1,
            "principle": "The Look: Under the gaze of the Other, I become an object",
        }

    def _analyze_nausea(self, text: str) -> Dict[str, Any]:
        """
        Analyze nausea (la nausée) - confronting the absurd contingency of existence.

        Nausea is the experience of existence as brute, meaningless, de trop (superfluous).
        Things are simply there, without reason, without necessity.
        """
        text_lower = text.lower()

        # Nausea/disgust indicators
        nausea_words = ["nausea", "disgust", "revulsion", "sick", "nauseating"]
        nausea_count = sum(1 for word in nausea_words if word in text_lower)

        # Contingency indicators
        contingency_words = [
            "contingent",
            "unnecessary",
            "could not be",
            "no reason",
            "absurd",
            "meaningless",
            "pointless",
            "arbitrary",
        ]
        contingency_count = sum(
            1 for phrase in contingency_words if phrase in text_lower
        )

        # Superfluousness indicators (de trop)
        superfluous_words = [
            "superfluous",
            "too much",
            "excess",
            "unnecessary",
            "shouldn't exist",
            "de trop",
        ]
        superfluous_count = sum(
            1 for phrase in superfluous_words if phrase in text_lower
        )

        # Viscosity/stickiness indicators (existence as sticky, pasty)
        viscous_words = ["sticky", "viscous", "slimy", "paste", "thick", "heavy"]
        viscous_count = sum(1 for word in viscous_words if word in text_lower)

        total_nausea = (
            nausea_count + contingency_count + superfluous_count + viscous_count
        )

        if nausea_count >= 1 and contingency_count >= 1:
            status = "Nausea Present"
            description = "Experience of existence as contingent, absurd, de trop"
            intensity = "High"
        elif contingency_count >= 2:
            status = "Confronting Contingency"
            description = "Awareness of the groundlessness of existence"
            intensity = "Medium"
        elif superfluous_count >= 1:
            status = "Sense of Superfluousness"
            description = "Experience of being de trop - one too many"
            intensity = "Medium"
        elif total_nausea >= 2:
            status = "Traces of Nausea"
            description = "Some awareness of existence's absurd facticity"
            intensity = "Low"
        else:
            status = "No Nausea Evident"
            description = "The absurd contingency not confronted"
            intensity = "None"

        return {
            "status": status,
            "description": description,
            "intensity": intensity,
            "nausea_score": nausea_count,
            "contingency_score": contingency_count,
            "superfluousness": superfluous_count,
            "viscosity": viscous_count,
            "principle": "Nausea: the experience of existence as contingent, absurd, de trop",
        }

    def _analyze_facticity_transcendence(self, text: str) -> Dict[str, Any]:
        """
        Analyze facticity and transcendence - the fundamental tension in human reality.

        Facticity: the given facts of our existence (body, past, situation)
        Transcendence: our ability to surpass the given toward future possibilities
        We are both facticity (what we are) and transcendence (what we make of it).
        """
        text_lower = text.lower()

        # Facticity indicators
        facticity_words = [
            "given",
            "fact",
            "born",
            "past",
            "already",
            "situation",
            "body",
            "history",
            "condition",
            "circumstances",
        ]
        facticity_count = sum(1 for word in facticity_words if word in text_lower)

        # Transcendence indicators
        transcendence_words = [
            "surpass",
            "overcome",
            "beyond",
            "transcend",
            "future",
            "possibility",
            "project",
            "become",
            "can be",
            "will be",
        ]
        transcendence_count = sum(
            1 for phrase in transcendence_words if phrase in text_lower
        )

        # Tension indicators
        tension_words = ["but", "yet", "however", "although", "despite", "tension"]
        tension_count = sum(1 for word in tension_words if word in text_lower)

        if facticity_count >= 2 and transcendence_count >= 2:
            status = "Full Tension"
            description = (
                "Awareness of both facticity and transcendence - the human condition"
            )
            balance = "Balanced"
        elif facticity_count > transcendence_count + 1:
            status = "Facticity Dominant"
            description = "Emphasis on the given - transcendence obscured"
            balance = "Weighted toward facticity"
        elif transcendence_count > facticity_count + 1:
            status = "Transcendence Dominant"
            description = "Emphasis on surpassing - facticity minimized"
            balance = "Weighted toward transcendence"
        else:
            status = "Implicit Tension"
            description = "The tension not explicitly articulated"
            balance = "Undetermined"

        return {
            "status": status,
            "description": description,
            "balance": balance,
            "facticity_score": facticity_count,
            "transcendence_score": transcendence_count,
            "tension_explicit": tension_count >= 1,
            "principle": "We are what we are (facticity) and what we make of what we are (transcendence)",
        }

    def _analyze_being_for_others(self, text: str) -> Dict[str, Any]:
        """
        Analyze being-for-others (être-pour-autrui).

        The Other is not just another consciousness but a drain hole
        through which my world flows. The Other steals my world.
        I exist for the Other in ways I can never fully know or control.
        """
        text_lower = text.lower()

        # Other's perspective indicators
        others_perspective = [
            "they see me",
            "how i appear",
            "others think",
            "in their eyes",
            "they judge",
            "reputation",
            "image",
            "what they think",
        ]
        others_count = sum(1 for phrase in others_perspective if phrase in text_lower)

        # Conflict indicators (Sartre: "Hell is other people")
        conflict_words = [
            "conflict",
            "struggle",
            "compete",
            "against",
            "versus others",
            "battle",
            "dominate",
            "submit",
        ]
        conflict_count = sum(1 for phrase in conflict_words if phrase in text_lower)

        # Alienation indicators
        alienation_words = [
            "alienated",
            "estranged",
            "distant",
            "separate",
            "isolated",
            "don't understand me",
            "misunderstood",
        ]
        alienation_count = sum(1 for phrase in alienation_words if phrase in text_lower)

        # Recognition/acknowledgment indicators
        recognition_words = [
            "recognize",
            "acknowledge",
            "accept",
            "understand me",
            "see me",
        ]
        recognition_count = sum(
            1 for phrase in recognition_words if phrase in text_lower
        )

        if others_count >= 2 and conflict_count >= 1:
            status = "Conflictual Being-for-Others"
            description = "The Other as threat - conflict over recognition"
            mode = "Adversarial"
        elif others_count >= 2:
            status = "Strong Being-for-Others"
            description = "Existence defined through the Other's gaze"
            mode = "Other-directed"
        elif alienation_count >= 2:
            status = "Alienated from Others"
            description = "The impossibility of mutual recognition"
            mode = "Estranged"
        elif recognition_count >= 1:
            status = "Seeking Recognition"
            description = "Desire for the Other's acknowledgment"
            mode = "Dependent"
        else:
            status = "Being-for-Others Not Prominent"
            description = "Focus on for-itself rather than for-others"
            mode = "Self-directed"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "others_perspective": others_count,
            "conflict_score": conflict_count,
            "alienation": alienation_count,
            "recognition_seeking": recognition_count,
            "principle": "L'enfer, c'est les autres - Hell is other people",
        }

    def _analyze_shame_pride(self, text: str) -> Dict[str, Any]:
        """
        Analyze shame and pride - the fundamental responses to the Look.

        Shame: I am ashamed of myself as I appear to the Other
        Pride: I glory in myself as I appear to the Other
        Both reveal that I recognize the Other's judgment as real.
        """
        text_lower = text.lower()

        # Shame indicators
        shame_words = [
            "shame",
            "ashamed",
            "embarrassed",
            "humiliated",
            "mortified",
            "disgrace",
            "dishonor",
        ]
        shame_count = sum(1 for word in shame_words if word in text_lower)

        # Pride indicators
        pride_words = ["proud", "pride", "glory", "honor", "dignity", "self-respect"]
        pride_count = sum(1 for word in pride_words if word in text_lower)

        # Guilt indicators (distinct from shame - about actions vs self)
        guilt_words = ["guilt", "guilty", "remorse", "regret"]
        guilt_count = sum(1 for word in guilt_words if word in text_lower)

        # Recognition of Other's judgment
        judgment_words = ["they think", "in their eyes", "judged by", "seen as"]
        judgment_count = sum(1 for phrase in judgment_words if phrase in text_lower)

        if shame_count >= 1 and judgment_count >= 1:
            status = "Shame Before the Other"
            description = (
                "Shame reveals my being-for-others - I am as the Other sees me"
            )
            dominant_affect = "Shame"
        elif pride_count >= 1 and judgment_count >= 1:
            status = "Pride Before the Other"
            description = (
                "Pride in how I appear to the Other - still captive to their gaze"
            )
            dominant_affect = "Pride"
        elif shame_count >= 1:
            status = "Shame Present"
            description = "Shame indicates awareness of being-for-others"
            dominant_affect = "Shame"
        elif pride_count >= 1:
            status = "Pride Present"
            description = "Pride indicates investment in being-for-others"
            dominant_affect = "Pride"
        elif guilt_count >= 1:
            status = "Guilt (Not Shame)"
            description = "Guilt about actions - different from shame about being"
            dominant_affect = "Guilt"
        else:
            status = "Neither Shame nor Pride Evident"
            description = "The affective dimension of being-for-others not explicit"
            dominant_affect = "None"

        return {
            "status": status,
            "description": description,
            "dominant_affect": dominant_affect,
            "shame_score": shame_count,
            "pride_score": pride_count,
            "guilt_score": guilt_count,
            "judgment_awareness": judgment_count,
            "principle": "Shame reveals my being-for-others - I am ashamed of myself as I appear",
        }

    def _analyze_body(self, text: str) -> Dict[str, Any]:
        """
        Analyze the three ontological dimensions of the body.

        1. Body-for-itself: The body as lived, as I experience it (body as perspective)
        2. Body-for-others: The body as object for the Other's gaze
        3. Body-as-known-by-other: My experience of my body as the Other sees it
        """
        text_lower = text.lower()

        # Body-for-itself indicators (lived body, phenomenal body)
        lived_body = [
            "feel",
            "sensation",
            "pain",
            "pleasure",
            "movement",
            "gesture",
            "breathing",
            "heart",
            "embodied",
            "bodily",
        ]
        lived_count = sum(1 for word in lived_body if word in text_lower)

        # Body-for-others indicators (body as object)
        body_object = [
            "body",
            "appearance",
            "physical",
            "looks",
            "how i look",
            "my body",
            "physique",
            "form",
        ]
        body_object_count = sum(1 for phrase in body_object if phrase in text_lower)

        # Self-conscious body indicators (body-as-known-by-other)
        self_conscious_body = [
            "self-conscious about",
            "embarrassed by my body",
            "they see my body",
            "ugly",
            "beautiful",
        ]
        self_conscious_count = sum(
            1 for phrase in self_conscious_body if phrase in text_lower
        )

        # Determine dominant dimension
        dimensions_present = []
        if lived_count >= 1:
            dimensions_present.append("Body-for-itself (lived body)")
        if body_object_count >= 2:
            dimensions_present.append("Body-for-others (body as object)")
        if self_conscious_count >= 1:
            dimensions_present.append("Body-as-known-by-other")

        if len(dimensions_present) >= 2:
            status = "Multiple Dimensions"
            description = f"Body experienced in multiple dimensions: {', '.join(dimensions_present)}"
        elif "Body-for-itself" in str(dimensions_present):
            status = "Lived Body Emphasized"
            description = "Body as lived experience, not as object"
        elif "Body-for-others" in str(dimensions_present):
            status = "Objectified Body"
            description = "Body as object for the Other's gaze"
        elif body_object_count >= 1 or lived_count >= 1:
            status = "Body Implicit"
            description = "Body present but ontological dimension unclear"
        else:
            status = "Body Not Thematized"
            description = "Embodiment not explicitly addressed"

        return {
            "status": status,
            "description": description,
            "dimensions_present": dimensions_present,
            "lived_body_score": lived_count,
            "body_as_object": body_object_count,
            "self_conscious_body": self_conscious_count,
            "principle": "The body has three dimensions: for-itself, for-others, and as-known-by-other",
        }

    def _analyze_situation(self, text: str) -> Dict[str, Any]:
        """
        Analyze situation - the concrete context of freedom.

        Situation is not just external circumstances but the meaningful
        context that appears through my projects. There is no freedom
        without situation, and no situation without freedom.
        """
        text_lower = text.lower()

        # Situation/context indicators
        situation_words = [
            "situation",
            "context",
            "circumstances",
            "condition",
            "environment",
            "setting",
            "place",
            "time",
            "where",
        ]
        situation_count = sum(1 for word in situation_words if word in text_lower)

        # Historical/social situation indicators
        historical_words = [
            "history",
            "era",
            "society",
            "culture",
            "epoch",
            "historical",
            "social",
            "political context",
        ]
        historical_count = sum(1 for phrase in historical_words if phrase in text_lower)

        # Resistance/limit indicators
        resistance_words = [
            "obstacle",
            "resistance",
            "limit",
            "constraint",
            "difficulty",
            "barrier",
        ]
        resistance_count = sum(1 for word in resistance_words if word in text_lower)

        # Meaning-through-project indicators
        meaning_words = [
            "meaningful",
            "significance",
            "matters",
            "important",
            "relevant",
            "purpose",
        ]
        meaning_count = sum(1 for word in meaning_words if word in text_lower)

        if situation_count >= 2 and meaning_count >= 1:
            status = "Situation as Meaningful"
            description = "Situation appears through my projects - it has meaning"
            awareness = "High"
        elif historical_count >= 1:
            status = "Historical Situation"
            description = "Awareness of historical/social embeddedness"
            awareness = "Medium-High"
        elif resistance_count >= 1:
            status = "Situation as Resistance"
            description = "Situation appears as what resists my freedom"
            awareness = "Medium"
        elif situation_count >= 1:
            status = "Situation Mentioned"
            description = "Context acknowledged but relation to freedom unclear"
            awareness = "Low"
        else:
            status = "Situation Not Explicit"
            description = "The concrete context not thematized"
            awareness = "None"

        return {
            "status": status,
            "description": description,
            "awareness": awareness,
            "situation_score": situation_count,
            "historical_dimension": historical_count,
            "resistance": resistance_count,
            "meaningful_context": meaning_count >= 1,
            "principle": "Freedom and situation are inseparable - there is no freedom except in situation",
        }

    def _analyze_project(self, text: str) -> Dict[str, Any]:
        """
        Analyze project - the fundamental life project that unifies our choices.

        Every action expresses a fundamental project - an original choice of being.
        We are our project. The project is not fully conscious but can be revealed
        through existential psychoanalysis.
        """
        text_lower = text.lower()

        # Project/goal indicators
        project_words = [
            "project",
            "goal",
            "aim",
            "plan",
            "ambition",
            "aspiration",
            "want to be",
            "trying to",
            "working toward",
        ]
        project_count = sum(1 for phrase in project_words if phrase in text_lower)

        # Future-oriented indicators
        future_words = [
            "will",
            "future",
            "become",
            "going to",
            "intend",
            "hope to",
            "dream of",
        ]
        future_count = sum(1 for phrase in future_words if phrase in text_lower)

        # Fundamental choice indicators
        fundamental_words = [
            "fundamental",
            "essential",
            "core",
            "basically",
            "at heart",
            "truly",
            "really am",
        ]
        fundamental_count = sum(
            1 for phrase in fundamental_words if phrase in text_lower
        )

        # Unity of choices indicators
        unity_words = ["consistent", "pattern", "always", "throughout", "unified"]
        unity_count = sum(1 for word in unity_words if word in text_lower)

        if project_count >= 2 and fundamental_count >= 1:
            status = "Fundamental Project Evident"
            description = "Awareness of fundamental life project"
            clarity = "High"
        elif project_count >= 1 and future_count >= 2:
            status = "Project-oriented"
            description = "Future-directed through projects"
            clarity = "Medium"
        elif future_count >= 1:
            status = "Future Orientation"
            description = "Some future directedness but project unclear"
            clarity = "Low"
        elif unity_count >= 1:
            status = "Unity Sought"
            description = "Sense of pattern or unity but project not explicit"
            clarity = "Low"
        else:
            status = "Project Not Explicit"
            description = "Fundamental project not articulated"
            clarity = "None"

        return {
            "status": status,
            "description": description,
            "clarity": clarity,
            "project_score": project_count,
            "future_orientation": future_count,
            "fundamental_awareness": fundamental_count,
            "unity_sense": unity_count,
            "principle": "Every action expresses a fundamental project - an original choice of being",
        }

    def _analyze_condemned_to_freedom(self, text: str) -> Dict[str, Any]:
        """
        Analyze the experience of being condemned to freedom.

        We did not choose to be free, yet we are free. We are thrown into freedom.
        We cannot escape freedom - even refusing to choose is a choice.
        This is the anguish and the glory of human existence.
        """
        text_lower = text.lower()

        # Condemnation/burden indicators
        condemned_words = [
            "condemned",
            "burden",
            "weight",
            "curse",
            "forced to",
            "can't escape",
            "stuck with",
            "no escape",
        ]
        condemned_count = sum(1 for phrase in condemned_words if phrase in text_lower)

        # Inescapability indicators
        inescapable_words = [
            "inescapable",
            "always",
            "must",
            "cannot avoid",
            "no way out",
            "inevitable",
        ]
        inescapable_count = sum(
            1 for phrase in inescapable_words if phrase in text_lower
        )

        # Freedom + necessity together
        freedom_necessity = any(
            word in text_lower for word in ["free", "freedom", "choice"]
        )
        necessity_present = any(
            word in text_lower for word in ["must", "condemned", "forced"]
        )

        # Paradox awareness
        paradox_words = ["paradox", "contradiction", "both", "yet", "although"]
        paradox_count = sum(1 for word in paradox_words if word in text_lower)

        if freedom_necessity and necessity_present and condemned_count >= 1:
            status = "Condemned to Freedom"
            description = "Awareness of freedom as inescapable burden"
            recognition = "Full"
        elif condemned_count >= 1 or (freedom_necessity and necessity_present):
            status = "Tension of Freedom"
            description = "Awareness that freedom is not chosen but given"
            recognition = "Partial"
        elif inescapable_count >= 1:
            status = "Inescapability Sensed"
            description = "Sense of inescapable condition"
            recognition = "Implicit"
        else:
            status = "Freedom as Lightness"
            description = "Freedom without sense of condemnation"
            recognition = "None"

        return {
            "status": status,
            "description": description,
            "recognition": recognition,
            "condemned_score": condemned_count,
            "inescapable_score": inescapable_count,
            "paradox_awareness": paradox_count >= 1,
            "principle": "Man is condemned to be free - we did not choose our freedom",
        }

    def _construct_reasoning(
        self,
        freedom: Dict[str, Any],
        responsibility: Dict[str, Any],
        bad_faith: List[str],
        mode_of_being: str,
        engagement: Dict[str, Any],
        anguish: Dict[str, Any],
        the_look: Dict[str, Any],
        nausea: Dict[str, Any],
        facticity_transcendence: Dict[str, Any],
        being_for_others: Dict[str, Any],
        shame_pride: Dict[str, Any],
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

        # Add being-for-others if prominent
        if being_for_others["others_perspective"] >= 1:
            reasoning += f"Being-for-others: {being_for_others['description']}. "

        # Add the Look if present
        if the_look["status"] != "The Look Not Explicit":
            reasoning += f"The Look: {the_look['description']}. "

        # Add nausea if present
        if nausea["status"] != "No Nausea Evident":
            reasoning += f"Nausea: {nausea['description']}. "

        # Add facticity-transcendence tension
        if facticity_transcendence["status"] == "Full Tension":
            reasoning += f"The human condition is evident: {facticity_transcendence['description']}. "

        # Add shame/pride if present
        if shame_pride["dominant_affect"] != "None":
            reasoning += f"Affective response: {shame_pride['description']}. "

        # Add engagement
        reasoning += f"Engagement level: {engagement['level']}. "

        # Add anguish
        if anguish["present"]:
            reasoning += (
                f"Anguish is present, indicating authentic confrontation with freedom. "
            )
        else:
            reasoning += "The absence of anguish may suggest flight from freedom. "

        # Conclude with Sartrean principle
        reasoning += (
            "Remember: existence precedes essence - we are nothing but what we make of ourselves. "
            "We are condemned to be free, absolutely responsible, with no excuses."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate existential tension based on Sartrean analysis.

        Tensions arise from:
        - Bad faith (fleeing from freedom)
        - Unacknowledged responsibility
        - Objectification by the Look
        - Lack of engagement
        - Conflictual being-for-others
        - Dominance of facticity over transcendence
        """
        tension_score = 0
        tension_elements = []

        # Check bad faith
        bad_faith = analysis["bad_faith"]
        if len(bad_faith) >= 3:
            tension_score += 2
            tension_elements.append("Multiple indicators of bad faith")
        elif "No obvious bad faith" not in bad_faith[0]:
            tension_score += 1
            tension_elements.append(f"Bad faith: {bad_faith[0]}")

        # Check responsibility
        responsibility = analysis["responsibility"]
        if responsibility["level"] == "Low":
            tension_score += 2
            tension_elements.append("Responsibility evaded")

        # Check freedom awareness
        freedom = analysis["freedom"]
        if freedom["level"] == "Low":
            tension_score += 1
            tension_elements.append("Low freedom awareness")

        # Check engagement
        engagement = analysis["engagement"]
        if "Low" in engagement["level"]:
            tension_score += 1
            tension_elements.append("Lack of engagement")

        # Check anguish
        anguish = analysis["anguish"]
        if not anguish["present"]:
            tension_score += 1
            tension_elements.append("Anguish absent - possible flight from freedom")

        # Check being-for-others
        being_for_others = analysis["being_for_others"]
        if "Conflictual" in being_for_others["status"]:
            tension_score += 1
            tension_elements.append("Conflictual relation to Others")

        # Check facticity-transcendence
        facticity_transcendence = analysis["facticity_transcendence"]
        if facticity_transcendence["balance"] == "Weighted toward facticity":
            tension_score += 1
            tension_elements.append("Facticity dominates - transcendence limited")

        # Check nausea
        nausea = analysis["nausea"]
        if nausea["intensity"] in ["High", "Very High"]:
            tension_score += 1
            tension_elements.append("Confronting absurd contingency")

        # Determine tension level
        if tension_score >= 6:
            level = "Very High"
            description = "Deep existential crisis - bad faith, flight from freedom"
        elif tension_score >= 4:
            level = "High"
            description = "Significant tensions in freedom and responsibility"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some existential tensions present"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, generally authentic"
        else:
            level = "Very Low"
            description = "Aligned with authentic existence"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
