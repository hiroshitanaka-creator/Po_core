"""
Søren Kierkegaard - Danish Philosopher and Theologian

Søren Kierkegaard (1813-1855)
Focus: Existence, Faith, Anxiety, Individual, Subjectivity

Key Concepts:
- Three Stages of Life: Aesthetic, Ethical, Religious
- Anxiety/Angst: Existential dread and freedom
- Despair: The Sickness unto Death
- Leap of Faith: Beyond reason into faith
- Subjectivity is Truth: Individual truth vs objective truth
- The Individual: Single individual before God, against the crowd
- Paradox: The absolute paradox of Christianity
- Repetition: Forward movement vs recollection
- The Moment/Instant: Decision and eternal significance
- Indirect Communication: Pseudonymous authorship
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Kierkegaard(Philosopher):
    """
    Søren Kierkegaard's existential philosophy.

    Analyzes prompts through the lens of existence, faith, anxiety,
    and the three stages of life (aesthetic, ethical, religious).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Søren Kierkegaard",
            description="Existential philosopher focused on individual existence, faith, and subjective truth"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Kierkegaard's existential perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Kierkegaard's existential analysis
        """
        # Perform Kierkegaardian analysis
        analysis = self._analyze_existence(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Existential Philosophy",
            "life_stage": analysis["stage"],
            "anxiety": analysis["anxiety"],
            "despair": analysis["despair"],
            "faith": analysis["faith"],
            "subjectivity": analysis["subjectivity"],
            "individuality": analysis["individual"],
            "paradox": analysis["paradox"],
            "leap": analysis["leap"],
            "moment": analysis["moment"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Existential analysis of individual existence",
                "focus": "Faith, anxiety, despair, and the stages of life"
            }
        }

    def _analyze_existence(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Kierkegaardian existential analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Determine life stage
        stage = self._determine_life_stage(prompt)

        # Assess anxiety
        anxiety = self._assess_anxiety(prompt)

        # Detect despair
        despair = self._detect_despair(prompt)

        # Evaluate faith
        faith = self._evaluate_faith(prompt)

        # Assess subjectivity
        subjectivity = self._assess_subjectivity(prompt)

        # Check individuality
        individual = self._check_individual(prompt)

        # Detect paradox
        paradox = self._detect_paradox(prompt)

        # Assess leap of faith
        leap = self._assess_leap(prompt)

        # Evaluate the moment
        moment = self._evaluate_moment(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            stage, anxiety, despair, faith, subjectivity
        )

        return {
            "reasoning": reasoning,
            "stage": stage,
            "anxiety": anxiety,
            "despair": despair,
            "faith": faith,
            "subjectivity": subjectivity,
            "individual": individual,
            "paradox": paradox,
            "leap": leap,
            "moment": moment
        }

    def _determine_life_stage(self, text: str) -> Dict[str, Any]:
        """
        Determine the dominant stage of life: Aesthetic, Ethical, or Religious.

        Aesthetic: Pleasure, immediacy, rotation method, Don Juan
        Ethical: Duty, marriage, commitment, Judge Wilhelm
        Religious: Faith, paradox, Abraham, Knight of Faith
        """
        text_lower = text.lower()

        # Aesthetic indicators
        aesthetic_words = ["pleasure", "enjoy", "fun", "beautiful", "desire", "moment", "variety", "bored"]
        has_aesthetic = sum(1 for word in aesthetic_words if word in text_lower)

        # Ethical indicators
        ethical_words = ["duty", "responsibility", "commitment", "marriage", "moral", "ought", "should", "obligation"]
        has_ethical = sum(1 for word in ethical_words if word in text_lower)

        # Religious indicators
        religious_words = ["faith", "god", "believe", "trust", "prayer", "divine", "eternal", "religious"]
        has_religious = sum(1 for word in religious_words if word in text_lower)

        # Determine dominant stage
        scores = {
            "Aesthetic": has_aesthetic,
            "Ethical": has_ethical,
            "Religious": has_religious
        }
        dominant = max(scores, key=scores.get)

        if scores[dominant] == 0:
            stage_type = "Unclear"
            description = "Dominant life stage not evident"
            note = "No clear existential orientation"
        elif dominant == "Aesthetic":
            stage_type = "Aesthetic Stage"
            description = "Living for pleasure and immediate experience - the rotation method"
            note = "Aesthetic existence leads to boredom and despair"
        elif dominant == "Ethical":
            stage_type = "Ethical Stage"
            description = "Living according to duty and universal ethical principles"
            note = "Ethical existence requires choice and commitment"
        else:  # Religious
            stage_type = "Religious Stage"
            description = "Living in faith and paradox before God - the Knight of Faith"
            note = "Religious existence requires the leap of faith"

        return {
            "stage": stage_type,
            "description": description,
            "scores": scores,
            "note": note,
            "principle": "Three stages: Aesthetic (pleasure), Ethical (duty), Religious (faith)"
        }

    def _assess_anxiety(self, text: str) -> Dict[str, Any]:
        """
        Assess existential anxiety/angst.

        Anxiety is the dizziness of freedom - possibility and nothingness
        Not fear of something specific but dread before possibility
        """
        text_lower = text.lower()

        # Anxiety indicators
        anxiety_words = ["anxiety", "anxious", "dread", "angst", "worry", "fear", "nervous"]
        has_anxiety = sum(1 for word in anxiety_words if word in text_lower)

        # Freedom/possibility indicators
        freedom_words = ["freedom", "free", "possibility", "possible", "choice", "choose"]
        has_freedom = sum(1 for word in freedom_words if word in text_lower)

        # Dizziness/vertigo indicators
        vertigo_words = ["dizzy", "vertigo", "overwhelm", "abyss", "void"]
        has_vertigo = sum(1 for phrase in vertigo_words if phrase in text_lower)

        # Nothingness indicators
        nothing_words = ["nothing", "nothingness", "emptiness", "void"]
        has_nothing = sum(1 for word in nothing_words if word in text_lower)

        # Specific object of fear (not anxiety)
        fear_object_words = ["afraid of", "fear of", "scared of"]
        has_fear_object = sum(1 for phrase in fear_object_words if phrase in text_lower)

        if has_anxiety >= 1 and has_freedom >= 1:
            presence = "Existential Anxiety"
            description = "Anxiety before the dizziness of freedom - the possibility of possibility"
            intensity = "High"
        elif has_vertigo >= 1 or (has_anxiety >= 1 and has_nothing >= 1):
            presence = "Dread Before Nothingness"
            description = "Dread before the abyss of possibility and nothingness"
            intensity = "Profound"
        elif has_anxiety >= 2:
            presence = "Anxiety Present"
            description = "Existential dread - not fear of something but anxiety before possibility"
            intensity = "Moderate"
        elif has_fear_object >= 1:
            presence = "Fear (Not Anxiety)"
            description = "Fear of specific object - not existential anxiety"
            intensity = "Low"
        else:
            presence = "No Anxiety Evident"
            description = "Anxiety not clearly present"
            intensity = "None"

        return {
            "presence": presence,
            "description": description,
            "intensity": intensity,
            "principle": "Anxiety is the dizziness of freedom - possibility before nothingness"
        }

    def _detect_despair(self, text: str) -> Dict[str, Any]:
        """
        Detect despair - the sickness unto death.

        Despair is not wanting to be oneself or wanting to be oneself
        Three forms: unconscious, not wanting to be oneself, wanting to be oneself
        """
        text_lower = text.lower()

        # Despair indicators
        despair_words = ["despair", "hopeless", "meaningless", "pointless"]
        has_despair = sum(1 for word in despair_words if word in text_lower)

        # Not wanting to be oneself
        not_self_words = ["not myself", "want to be someone else", "escape myself", "hate myself"]
        has_not_self = sum(1 for phrase in not_self_words if phrase in text_lower)

        # Wanting to be oneself (defiant despair)
        defiant_self_words = ["my own", "myself alone", "by myself", "self-made", "independent"]
        has_defiant = sum(1 for phrase in defiant_self_words if phrase in text_lower)

        # Unconscious despair (spiritlessness)
        unconscious_words = ["unaware", "numb", "distracted", "entertainment", "conformity"]
        has_unconscious = sum(1 for word in unconscious_words if word in text_lower)

        # Self-awareness
        awareness_words = ["aware", "conscious", "realize", "understand myself"]
        has_awareness = sum(1 for phrase in awareness_words if phrase in text_lower)

        if has_despair >= 1 and has_not_self >= 1:
            type_despair = "Despair of Not Wanting to Be Oneself"
            description = "Despair of weakness - not wanting to be oneself"
            depth = "Conscious"
        elif has_despair >= 1 and has_defiant >= 1:
            type_despair = "Despair of Wanting to Be Oneself"
            description = "Despair of defiance - wanting to be oneself by one's own power"
            depth = "Defiant"
        elif has_unconscious >= 2:
            type_despair = "Unconscious Despair"
            description = "Spiritlessness - not aware of being in despair"
            depth = "Unconscious"
        elif has_despair >= 1:
            type_despair = "Despair Present"
            description = "The sickness unto death - despair is a sickness of the self"
            depth = "Evident"
        else:
            type_despair = "No Despair Evident"
            description = "Despair not clearly present"
            depth = "None"

        return {
            "type": type_despair,
            "description": description,
            "depth": depth,
            "principle": "Despair is the sickness unto death - a sickness in the self"
        }

    def _evaluate_faith(self, text: str) -> Dict[str, Any]:
        """
        Evaluate faith - the leap into the absurd.

        Faith is not knowledge but a relation to the absolute
        Abraham as the Knight of Faith
        """
        text_lower = text.lower()

        # Faith indicators
        faith_words = ["faith", "believe", "trust", "belief"]
        has_faith = sum(1 for word in faith_words if word in text_lower)

        # Reason/knowledge indicators
        reason_words = ["reason", "rational", "logical", "prove", "evidence", "knowledge"]
        has_reason = sum(1 for word in reason_words if word in text_lower)

        # Paradox/absurd indicators
        absurd_words = ["paradox", "absurd", "impossible", "beyond reason"]
        has_absurd = sum(1 for phrase in absurd_words if phrase in text_lower)

        # Abraham/religious indicators
        religious_refs = ["abraham", "sacrifice", "knight of faith"]
        has_religious_ref = sum(1 for phrase in religious_refs if phrase in text_lower)

        # Doubt indicators
        doubt_words = ["doubt", "uncertain", "question", "skeptic"]
        has_doubt = sum(1 for word in doubt_words if word in text_lower)

        if has_faith >= 1 and has_absurd >= 1:
            faith_type = "Faith in the Absurd"
            description = "Faith despite the paradox - the leap beyond reason"
            status = "Authentic faith"
        elif has_religious_ref >= 1 or (has_faith >= 1 and has_reason == 0):
            faith_type = "Religious Faith"
            description = "Faith as relation to the absolute - Knight of Faith"
            status = "Faith present"
        elif has_faith >= 1 and has_reason >= 1:
            faith_type = "Faith Seeking Understanding"
            description = "Attempting to ground faith in reason"
            status = "Incomplete"
        elif has_doubt >= 1:
            faith_type = "Doubt"
            description = "Questioning and uncertainty"
            status = "Pre-faith"
        else:
            faith_type = "No Faith Evident"
            description = "Faith not clearly present"
            status = "None"

        return {
            "type": faith_type,
            "description": description,
            "status": status,
            "principle": "Faith is the leap beyond reason into the paradox of the absolute"
        }

    def _assess_subjectivity(self, text: str) -> Dict[str, Any]:
        """
        Assess subjectivity vs objectivity.

        Truth is subjectivity - individual passionate inwardness
        Objective truth vs subjective truth
        """
        text_lower = text.lower()

        # Subjectivity indicators
        subjective_words = ["i feel", "i believe", "my experience", "personal", "individual", "my truth"]
        has_subjective = sum(1 for phrase in subjective_words if phrase in text_lower)

        # Objectivity indicators
        objective_words = ["objective", "fact", "evidence", "proven", "universal", "everyone"]
        has_objective = sum(1 for word in objective_words if word in text_lower)

        # Passion/inwardness indicators
        passion_words = ["passion", "passionate", "deeply", "inward", "heart"]
        has_passion = sum(1 for word in passion_words if word in text_lower)

        # Detachment indicators
        detached_words = ["detached", "neutral", "impartial", "dispassionate"]
        has_detached = sum(1 for word in detached_words if word in text_lower)

        if has_subjective >= 2 or (has_subjective >= 1 and has_passion >= 1):
            orientation = "Subjective Truth"
            description = "Truth is subjectivity - passionate inward appropriation"
            approach = "Kierkegaardian"
        elif has_passion >= 1:
            orientation = "Passionate Inwardness"
            description = "Intensity of individual existence"
            approach = "Existential"
        elif has_objective >= 2 or has_detached >= 1:
            orientation = "Objective Truth"
            description = "Seeking universal, dispassionate truth"
            approach = "Objective"
        else:
            orientation = "Unclear"
            description = "Subjective/objective orientation unclear"
            approach = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "approach": approach,
            "principle": "Truth is subjectivity - individual passionate appropriation of truth"
        }

    def _check_individual(self, text: str) -> Dict[str, Any]:
        """
        Check for the individual vs the crowd.

        The single individual before God
        Against Christendom and the crowd
        """
        text_lower = text.lower()

        # Individual indicators
        individual_words = ["individual", "myself", "alone", "single", "one person"]
        has_individual = sum(1 for phrase in individual_words if phrase in text_lower)

        # Crowd/mass indicators
        crowd_words = ["crowd", "everyone", "masses", "public", "they", "society", "conformity"]
        has_crowd = sum(1 for word in crowd_words if word in text_lower)

        # Before God indicators
        god_relation = ["before god", "in god", "god's eyes"]
        has_god_relation = sum(1 for phrase in god_relation if phrase in text_lower)

        # Conformity indicators
        conform_words = ["conform", "fit in", "belong", "follow", "same as"]
        has_conform = sum(1 for phrase in conform_words if phrase in text_lower)

        if has_individual >= 1 and has_god_relation >= 1:
            status = "Single Individual Before God"
            description = "The individual in absolute relation to the absolute"
            stance = "Authentic"
        elif has_individual >= 2 or (has_individual >= 1 and has_crowd == 0):
            status = "Individual Existence"
            description = "Standing as an individual, not lost in the crowd"
            stance = "Individual"
        elif has_crowd >= 2 or has_conform >= 1:
            status = "Lost in the Crowd"
            description = "Absorbed in the masses - untruth is the crowd"
            stance = "Inauthentic"
        else:
            status = "Unclear"
            description = "Individuality status unclear"
            stance = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "stance": stance,
            "principle": "The individual - single individual before God, against the crowd"
        }

    def _detect_paradox(self, text: str) -> Dict[str, Any]:
        """
        Detect the absolute paradox.

        The paradox of Christianity - eternal entering time
        The God-man, incarnation
        """
        text_lower = text.lower()

        # Paradox indicators
        paradox_words = ["paradox", "contradiction", "absurd", "impossible", "both and"]
        has_paradox = sum(1 for phrase in paradox_words if phrase in text_lower)

        # Eternal/temporal indicators
        eternal_temporal = ["eternal", "time", "moment", "instant", "temporal"]
        has_eternal_temporal = sum(1 for word in eternal_temporal if word in text_lower)

        # Incarnation/God-man indicators
        incarnation_words = ["incarnation", "god-man", "divine human", "eternal in time"]
        has_incarnation = sum(1 for phrase in incarnation_words if phrase in text_lower)

        # Rational/logical indicators
        rational_words = ["rational", "logical", "reasonable", "makes sense"]
        has_rational = sum(1 for phrase in rational_words if phrase in text_lower)

        if has_paradox >= 1 and has_incarnation >= 1:
            presence = "The Absolute Paradox"
            description = "The paradox of the eternal entering time - the God-man"
            type_paradox = "Christian"
        elif has_paradox >= 1 and has_eternal_temporal >= 2:
            presence = "Paradox of Eternal and Temporal"
            description = "Eternal truth in temporal existence"
            type_paradox = "Existential"
        elif has_paradox >= 1:
            presence = "Paradox Present"
            description = "Confronting the paradoxical nature of existence"
            type_paradox = "General"
        elif has_rational >= 1:
            presence = "Rationality"
            description = "Seeking rational coherence - avoiding paradox"
            type_paradox = "None"
        else:
            presence = "No Paradox Evident"
            description = "Paradox not clearly present"
            type_paradox = "Unclear"

        return {
            "presence": presence,
            "description": description,
            "type": type_paradox,
            "principle": "The absolute paradox - eternal truth in temporal existence"
        }

    def _assess_leap(self, text: str) -> Dict[str, Any]:
        """
        Assess the leap of faith.

        The leap beyond reason into faith
        Not gradual approximation but decisive leap
        """
        text_lower = text.lower()

        # Leap indicators
        leap_words = ["leap", "jump", "decide", "decision", "commit"]
        has_leap = sum(1 for word in leap_words if word in text_lower)

        # Faith/belief indicators
        faith_words = ["faith", "believe", "trust"]
        has_faith = sum(1 for word in faith_words if word in text_lower)

        # Gradual/approximation indicators
        gradual_words = ["gradual", "step by step", "slowly", "approximate", "progress"]
        has_gradual = sum(1 for phrase in gradual_words if phrase in text_lower)

        # Risk/venture indicators
        risk_words = ["risk", "venture", "dare", "courage"]
        has_risk = sum(1 for word in risk_words if word in text_lower)

        if (has_leap >= 1 and has_faith >= 1) or has_risk >= 1:
            status = "Leap of Faith"
            description = "The decisive leap beyond reason into faith"
            mode = "Existential decision"
        elif has_leap >= 1:
            status = "Decisive Movement"
            description = "Making a decisive choice or commitment"
            mode = "Decision"
        elif has_gradual >= 1:
            status = "Gradual Approximation"
            description = "Attempting gradual approach - avoiding the leap"
            mode = "Evasion"
        else:
            status = "No Leap Evident"
            description = "Leap not clearly present"
            mode = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "principle": "The leap of faith - decisive movement beyond reason"
        }

    def _evaluate_moment(self, text: str) -> Dict[str, Any]:
        """
        Evaluate the moment/instant of decision.

        The moment where eternal breaks into time
        The instant of decision with eternal significance
        """
        text_lower = text.lower()

        # Moment/instant indicators
        moment_words = ["moment", "instant", "now", "present"]
        has_moment = sum(1 for word in moment_words if word in text_lower)

        # Decision indicators
        decision_words = ["decide", "decision", "choose", "choice"]
        has_decision = sum(1 for word in decision_words if word in text_lower)

        # Eternal significance indicators
        eternal_words = ["eternal", "forever", "always", "significance"]
        has_eternal = sum(1 for word in eternal_words if word in text_lower)

        # Delay/postpone indicators
        delay_words = ["later", "tomorrow", "postpone", "wait", "someday"]
        has_delay = sum(1 for word in delay_words if word in text_lower)

        if has_moment >= 1 and has_eternal >= 1:
            significance = "The Moment of Eternal Significance"
            description = "The instant where eternal breaks into temporal existence"
            urgency = "Absolute"
        elif has_moment >= 1 and has_decision >= 1:
            significance = "Moment of Decision"
            description = "The decisive instant requiring choice"
            urgency = "High"
        elif has_moment >= 1:
            significance = "Present Moment"
            description = "Awareness of the present instant"
            urgency = "Moderate"
        elif has_delay >= 1:
            significance = "Postponement"
            description = "Delaying the decisive moment"
            urgency = "Evasive"
        else:
            significance = "No Moment Evident"
            description = "Moment not clearly present"
            urgency = "None"

        return {
            "significance": significance,
            "description": description,
            "urgency": urgency,
            "principle": "The moment/instant - where eternal significance enters time"
        }

    def _construct_reasoning(
        self,
        stage: Dict[str, Any],
        anxiety: Dict[str, Any],
        despair: Dict[str, Any],
        faith: Dict[str, Any],
        subjectivity: Dict[str, Any]
    ) -> str:
        """Construct Kierkegaardian existential reasoning."""
        reasoning = (
            f"From Kierkegaard's existential perspective, this reflects the {stage['stage']}: {stage['description']}. "
            f"Anxiety: {anxiety['description']}. "
            f"Despair: {despair['description']}. "
            f"Faith: {faith['description']}. "
            f"Subjectivity: {subjectivity['description']}. "
        )

        # Conclude with Kierkegaardian principle
        reasoning += (
            "The task is to become an individual, to exist before God in faith, "
            "choosing oneself in passionate inwardness despite anxiety and despair. "
            "Truth is subjectivity."
        )

        return reasoning
