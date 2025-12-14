"""
Maurice Merleau-Ponty - French Phenomenologist

Maurice Merleau-Ponty (1908-1961)
Focus: Embodiment, Perception, Lived Body, Flesh

Key Concepts:
- Lived Body (le corps propre): Body as subject, not object
- Perception: Primary access to world, pre-reflective
- Flesh (la chair): Reversibility of sensing and sensed
- Chiasm: Intertwining of seer and seen, toucher and touched
- Ambiguity: Fundamental ambiguity of experience
- Being-in-the-World: Embodied situatedness
- Phenomenal Field: Pre-objective domain of experience
- Gestalt: Structured wholes in perception
- Intentionality: Motor intentionality, operative intentionality
- Intersubjectivity: Through embodied perception
- Depth: Primordial dimension of experience
- Style: Individual manner of being-in-the-world
- Reversibility (réversibilité): Touching-touched, seeing-seen
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class MerleauPonty(Philosopher):
    """
    Maurice Merleau-Ponty's phenomenology of embodiment and perception.

    Analyzes prompts through the lens of lived body, perception,
    flesh, and the ambiguity of embodied experience.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Maurice Merleau-Ponty",
            description="Phenomenologist focused on embodiment, perception, and the lived body"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Merleau-Ponty's phenomenological perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Merleau-Ponty's phenomenological analysis
        """
        # Perform Merleau-Pontian analysis
        analysis = self._analyze_embodiment(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Phenomenology of Embodiment",
            "lived_body": analysis["lived_body"],
            "perception": analysis["perception"],
            "flesh": analysis["flesh"],
            "chiasm": analysis["chiasm"],
            "ambiguity": analysis["ambiguity"],
            "being_in_world": analysis["being_in_world"],
            "gestalt": analysis["gestalt"],
            "reversibility": analysis["reversibility"],
            "intersubjectivity": analysis["intersubjectivity"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Phenomenology of perception and embodied experience",
                "focus": "Lived body, perception, flesh, and ambiguity"
            }
        }

    def _analyze_embodiment(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Merleau-Pontian phenomenological analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess lived body
        lived_body = self._assess_lived_body(prompt)

        # Evaluate perception
        perception = self._evaluate_perception(prompt)

        # Detect flesh
        flesh = self._detect_flesh(prompt)

        # Assess chiasm
        chiasm = self._assess_chiasm(prompt)

        # Check ambiguity
        ambiguity = self._check_ambiguity(prompt)

        # Evaluate being-in-the-world
        being_in_world = self._evaluate_being_in_world(prompt)

        # Detect gestalt
        gestalt = self._detect_gestalt(prompt)

        # Assess reversibility
        reversibility = self._assess_reversibility(prompt)

        # Check intersubjectivity
        intersubjectivity = self._check_intersubjectivity(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            lived_body, perception, flesh, ambiguity
        )

        return {
            "reasoning": reasoning,
            "lived_body": lived_body,
            "perception": perception,
            "flesh": flesh,
            "chiasm": chiasm,
            "ambiguity": ambiguity,
            "being_in_world": being_in_world,
            "gestalt": gestalt,
            "reversibility": reversibility,
            "intersubjectivity": intersubjectivity
        }

    def _assess_lived_body(self, text: str) -> Dict[str, Any]:
        """
        Assess the lived body (le corps propre).

        Lived body: Body as subject, not object
        Body-subject vs body-object
        Phenomenal body vs objective body
        """
        text_lower = text.lower()

        # Lived body indicators (body as subject)
        lived_body_words = ["my body", "embodied", "bodily", "felt", "lived experience"]
        has_lived_body = sum(1 for phrase in lived_body_words if phrase in text_lower)

        # Body as subject indicators
        body_subject = ["body knows", "body understands", "body can", "body feels"]
        has_body_subject = sum(1 for phrase in body_subject if phrase in text_lower)

        # Movement/motor indicators
        movement_words = ["move", "gesture", "reach", "grasp", "act"]
        has_movement = sum(1 for word in movement_words if word in text_lower)

        # Body as object (anatomical, mechanical)
        body_object = ["anatomy", "mechanism", "machine", "parts", "organs"]
        has_body_object = sum(1 for word in body_object if word in text_lower)

        # Sensation/feeling indicators
        sensation_words = ["feel", "sense", "sensation", "touch", "perceive"]
        has_sensation = sum(1 for word in sensation_words if word in text_lower)

        # Habit/skill indicators (body schema)
        habit_words = ["habit", "skill", "habitual", "practiced", "automatic"]
        has_habit = sum(1 for word in habit_words if word in text_lower)

        if has_lived_body >= 1 or has_body_subject >= 1:
            status = "Lived Body (Corps Propre)"
            description = "Body as subject - phenomenal body that perceives and acts"
            mode = "Body-subject"
        elif has_movement >= 1 and has_sensation >= 1:
            status = "Embodied Experience"
            description = "Embodied perception and motor intentionality"
            mode = "Pre-reflective"
        elif has_habit >= 1:
            status = "Body Schema"
            description = "Habitual body - sedimented skills and habits"
            mode = "Habitual"
        elif has_body_object >= 1:
            status = "Body as Object"
            description = "Objective body - anatomical, mechanical"
            mode = "Body-object"
        else:
            status = "No Clear Body"
            description = "Embodiment not clearly evident"
            mode = "None"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "principle": "Lived body (corps propre) is body as subject, not object"
        }

    def _evaluate_perception(self, text: str) -> Dict[str, Any]:
        """
        Evaluate perception.

        Perception: Primary access to world, pre-reflective
        Not mental representation but direct engagement
        Perceptual faith: primordial trust in world
        """
        text_lower = text.lower()

        # Perception indicators
        perception_words = ["perceive", "see", "hear", "touch", "sense"]
        has_perception = sum(1 for word in perception_words if word in text_lower)

        # Direct/immediate indicators
        direct_words = ["directly", "immediate", "present", "given"]
        has_direct = sum(1 for word in direct_words if word in text_lower)

        # Pre-reflective indicators
        prereflective_words = ["pre-reflective", "before thinking", "prior to", "unreflected"]
        has_prereflective = sum(1 for phrase in prereflective_words if phrase in text_lower)

        # Representation/mental (not direct perception)
        representation_words = ["represent", "mental image", "idea of", "concept"]
        has_representation = sum(1 for phrase in representation_words if phrase in text_lower)

        # World/reality indicators
        world_words = ["world", "reality", "things", "objects"]
        has_world = sum(1 for word in world_words if word in text_lower)

        # Meaning/significance in perception
        meaning_words = ["meaning", "significance", "sense", "understanding"]
        has_meaning = sum(1 for word in meaning_words if word in text_lower)

        if has_perception >= 1 and has_direct >= 1:
            status = "Direct Perception"
            description = "Immediate perceptual access to world - not through representations"
            character = "Pre-objective"
        elif has_perception >= 1 and has_prereflective >= 1:
            status = "Pre-Reflective Perception"
            description = "Perception prior to reflective thought - primordial contact"
            character = "Primordial"
        elif has_perception >= 1 and has_meaning >= 1:
            status = "Meaningful Perception"
            description = "Perception as already meaningful - not raw sense data"
            character = "Meaningful"
        elif has_representation >= 1:
            status = "Representational View"
            description = "Perception as mental representation - not Merleau-Pontian"
            character = "Intellectualist"
        elif has_perception >= 1:
            status = "Perception Present"
            description = "Perceptual experience indicated"
            character = "General"
        else:
            status = "No Clear Perception"
            description = "Perception not clearly evident"
            character = "None"

        return {
            "status": status,
            "description": description,
            "character": character,
            "principle": "Perception is primary, pre-reflective access to the world"
        }

    def _detect_flesh(self, text: str) -> Dict[str, Any]:
        """
        Detect the flesh (la chair).

        Flesh: Reversibility of sensing and sensed
        Not body-object but sensible-sentient
        Element of Being, chiasmic intertwining
        """
        text_lower = text.lower()

        # Flesh indicators
        flesh_words = ["flesh", "sensible", "tangible", "carnal"]
        has_flesh = sum(1 for word in flesh_words if word in text_lower)

        # Reversibility indicators
        reversibility_words = ["reversible", "intertwine", "chiasm", "both sides"]
        has_reversibility = sum(1 for phrase in reversibility_words if phrase in text_lower)

        # Sensing-sensed indicators
        sensing_sensed = ["see and seen", "touch and touched", "feel and felt"]
        has_sensing_sensed = sum(1 for phrase in sensing_sensed if phrase in text_lower)

        # Element/medium indicators
        element_words = ["element", "medium", "milieu", "fabric"]
        has_element = sum(1 for word in element_words if word in text_lower)

        # Visible/invisible indicators
        visible_invisible = ["visible", "invisible", "seen", "unseen"]
        has_visible_invisible = sum(1 for word in visible_invisible if word in text_lower)

        if has_flesh >= 1 or (has_reversibility >= 1 and has_sensing_sensed >= 1):
            presence = "The Flesh (La Chair)"
            description = "Flesh as reversible element - sensible-sentient intertwining"
            nature = "Chiasmic"
        elif has_sensing_sensed >= 1:
            presence = "Reversibility"
            description = "Reversibility of sensing and being sensed"
            nature = "Reciprocal"
        elif has_element >= 1:
            presence = "Elemental Medium"
            description = "Flesh as element or medium of being"
            nature = "Ontological"
        else:
            presence = "No Flesh Evident"
            description = "Flesh not clearly present"
            nature = "None"

        return {
            "presence": presence,
            "description": description,
            "nature": nature,
            "principle": "Flesh is reversible element - sensible and sentient intertwined"
        }

    def _assess_chiasm(self, text: str) -> Dict[str, Any]:
        """
        Assess chiasm (le chiasme).

        Chiasm: Intertwining of seer and seen, toucher and touched
        Crossing-over, reversibility structure
        """
        text_lower = text.lower()

        # Chiasm indicators
        chiasm_words = ["chiasm", "intertwine", "crossing", "interweave"]
        has_chiasm = sum(1 for word in chiasm_words if word in text_lower)

        # Seer-seen indicators
        seer_seen = ["see and seen", "seer and seen", "look and looked at"]
        has_seer_seen = sum(1 for phrase in seer_seen if phrase in text_lower)

        # Toucher-touched indicators
        toucher_touched = ["touch and touched", "toucher", "feel and felt"]
        has_toucher_touched = sum(1 for phrase in toucher_touched if phrase in text_lower)

        # Two-way/mutual indicators
        mutual_words = ["mutual", "reciprocal", "two-way", "both ways"]
        has_mutual = sum(1 for phrase in mutual_words if phrase in text_lower)

        # Crossing/overlap indicators
        crossing_words = ["cross", "overlap", "interplay", "exchange"]
        has_crossing = sum(1 for word in crossing_words if word in text_lower)

        if has_chiasm >= 1 or (has_seer_seen >= 1 or has_toucher_touched >= 1):
            status = "Chiasm"
            description = "Chiasmic intertwining - seer is seen, toucher is touched"
            structure = "Reversible"
        elif has_mutual >= 1 and has_crossing >= 1:
            status = "Mutual Intertwining"
            description = "Reciprocal crossing and interplay"
            structure = "Reciprocal"
        else:
            status = "No Chiasm Evident"
            description = "Chiasm not clearly present"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "principle": "Chiasm: intertwining of seer/seen, toucher/touched"
        }

    def _check_ambiguity(self, text: str) -> Dict[str, Any]:
        """
        Check for ambiguity (ambiguïté).

        Ambiguity: Fundamental character of embodied experience
        Not defect but essence of perceptual life
        Neither purely subjective nor purely objective
        """
        text_lower = text.lower()

        # Ambiguity indicators
        ambiguity_words = ["ambiguous", "ambiguity", "unclear", "indeterminate"]
        has_ambiguity = sum(1 for word in ambiguity_words if word in text_lower)

        # Both/neither indicators
        both_neither = ["both and", "neither nor", "at once", "simultaneously"]
        has_both_neither = sum(1 for phrase in both_neither if phrase in text_lower)

        # Dual aspect indicators
        dual_words = ["dual", "double", "two-sided", "paradox"]
        has_dual = sum(1 for phrase in dual_words if phrase in text_lower)

        # Clarity/determinacy (opposite)
        clarity_words = ["clear", "definite", "determinate", "unambiguous"]
        has_clarity = sum(1 for word in clarity_words if word in text_lower)

        # Subject-object interplay
        subject_object = ["subject and object", "subjective and objective"]
        has_subject_object = sum(1 for phrase in subject_object if phrase in text_lower)

        if has_ambiguity >= 1 or (has_both_neither >= 1 and has_subject_object >= 1):
            presence = "Fundamental Ambiguity"
            description = "Essential ambiguity of embodied experience - neither purely subjective nor objective"
            character = "Ontological"
        elif has_both_neither >= 1 or has_dual >= 1:
            presence = "Ambiguous Structure"
            description = "Dual or paradoxical character"
            character = "Structural"
        elif has_clarity >= 1:
            presence = "Clarity Sought"
            description = "Seeking unambiguous clarity - against ambiguity"
            character = "Anti-phenomenological"
        else:
            presence = "No Ambiguity Evident"
            description = "Ambiguity not clearly present"
            character = "None"

        return {
            "presence": presence,
            "description": description,
            "character": character,
            "principle": "Ambiguity is fundamental to embodied perceptual experience"
        }

    def _evaluate_being_in_world(self, text: str) -> Dict[str, Any]:
        """
        Evaluate being-in-the-world.

        Being-in-the-world: Embodied situatedness
        Not consciousness facing world but being immersed
        Primordial involvement with world
        """
        text_lower = text.lower()

        # Being-in-world indicators
        being_in_world = ["being in the world", "in the world", "world around"]
        has_being_in_world = sum(1 for phrase in being_in_world if phrase in text_lower)

        # Situated/immersed indicators
        situated_words = ["situated", "immersed", "embedded", "engaged"]
        has_situated = sum(1 for word in situated_words if word in text_lower)

        # Involvement/participation indicators
        involvement_words = ["involved", "participate", "engaged with", "part of"]
        has_involvement = sum(1 for phrase in involvement_words if phrase in text_lower)

        # World indicators
        world_words = ["world", "environment", "surroundings", "milieu"]
        has_world = sum(1 for word in world_words if word in text_lower)

        # Detached/observer (opposite)
        detached_words = ["detached", "observer", "outside", "separate from world"]
        has_detached = sum(1 for phrase in detached_words if phrase in text_lower)

        if has_being_in_world >= 1 or (has_situated >= 1 and has_world >= 1):
            status = "Being-in-the-World"
            description = "Embodied situatedness - immersed in world, not facing it"
            mode = "Primordial engagement"
        elif has_involvement >= 1 and has_world >= 1:
            status = "Worldly Engagement"
            description = "Engaged participation with world"
            mode = "Engaged"
        elif has_detached >= 1:
            status = "Detached Consciousness"
            description = "Consciousness as detached observer - not Merleau-Pontian"
            mode = "Intellectualist"
        else:
            status = "Unclear"
            description = "Being-in-world status unclear"
            mode = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "principle": "Being-in-the-world: primordial embodied engagement, not detached consciousness"
        }

    def _detect_gestalt(self, text: str) -> Dict[str, Any]:
        """
        Detect gestalt structures.

        Gestalt: Structured wholes in perception
        Figure-ground structure
        Not atomistic sensations but organized wholes
        """
        text_lower = text.lower()

        # Gestalt indicators
        gestalt_words = ["gestalt", "whole", "structure", "pattern", "form"]
        has_gestalt = sum(1 for word in gestalt_words if word in text_lower)

        # Figure-ground indicators
        figure_ground = ["figure", "ground", "background", "foreground", "stand out"]
        has_figure_ground = sum(1 for phrase in figure_ground if phrase in text_lower)

        # Organized/structured indicators
        organized_words = ["organized", "structured", "configured", "arranged"]
        has_organized = sum(1 for word in organized_words if word in text_lower)

        # Atomistic/parts (opposite)
        atomistic_words = ["atoms", "parts", "elements", "pieces", "fragments"]
        has_atomistic = sum(1 for word in atomistic_words if word in text_lower)

        # Meaning/significance in whole
        meaningful_whole = ["meaningful whole", "significant pattern", "coherent"]
        has_meaningful_whole = sum(1 for phrase in meaningful_whole if phrase in text_lower)

        if has_gestalt >= 1 or has_figure_ground >= 2:
            presence = "Gestalt Structure"
            description = "Perception as organized wholes - figure-ground structures"
            character = "Holistic"
        elif has_organized >= 1 and has_meaningful_whole >= 1:
            presence = "Structured Meaning"
            description = "Meaningful organized patterns"
            character = "Configurational"
        elif has_atomistic >= 1:
            presence = "Atomistic View"
            description = "Focus on parts and elements - not gestalt"
            character = "Empiricist"
        else:
            presence = "No Gestalt Evident"
            description = "Gestalt structure not clearly present"
            character = "None"

        return {
            "presence": presence,
            "description": description,
            "character": character,
            "principle": "Perception involves gestalt structures - organized wholes, not atomic sensations"
        }

    def _assess_reversibility(self, text: str) -> Dict[str, Any]:
        """
        Assess reversibility (réversibilité).

        Reversibility: Touching-touched, seeing-seen
        My body as both sensing and sensible
        Fundamental structure of flesh
        """
        text_lower = text.lower()

        # Reversibility explicit
        reversibility_words = ["reversibility", "reversible", "reverse"]
        has_reversibility = sum(1 for word in reversibility_words if word in text_lower)

        # Touching-touched
        touching_touched = ["touch myself", "touching and touched", "hand touches hand"]
        has_touching_touched = sum(1 for phrase in touching_touched if phrase in text_lower)

        # Seeing-seen
        seeing_seen = ["see myself", "seeing and seen", "visible and seeing"]
        has_seeing_seen = sum(1 for phrase in seeing_seen if phrase in text_lower)

        # Double sensation
        double_sensation = ["double sensation", "feel both", "sense both sides"]
        has_double_sensation = sum(1 for phrase in double_sensation if phrase in text_lower)

        # One-way/unidirectional (opposite)
        one_way = ["one way", "unidirectional", "only sensing", "only active"]
        has_one_way = sum(1 for phrase in one_way if phrase in text_lower)

        if has_reversibility >= 1 or has_touching_touched >= 1 or has_seeing_seen >= 1:
            status = "Reversibility"
            description = "Reversible structure - touching-touched, seeing-seen"
            structure = "Chiasmic"
        elif has_double_sensation >= 1:
            status = "Double Sensation"
            description = "Experiencing both sides of sensation"
            structure = "Dual"
        elif has_one_way >= 1:
            status = "Unidirectional"
            description = "One-way sensing - not reversible"
            structure = "Non-reversible"
        else:
            status = "No Reversibility Evident"
            description = "Reversibility not clearly present"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "principle": "Reversibility: my body is both sensing and sensible - touching-touched"
        }

    def _check_intersubjectivity(self, text: str) -> Dict[str, Any]:
        """
        Check intersubjectivity.

        Intersubjectivity: Through embodied perception
        Other bodies perceived as lived bodies like mine
        Not inference but direct perceptual recognition
        """
        text_lower = text.lower()

        # Intersubjectivity indicators
        intersubjectivity_words = ["intersubjectivity", "others", "other people", "we"]
        has_intersubjectivity = sum(1 for phrase in intersubjectivity_words if phrase in text_lower)

        # Other bodies/embodied others
        other_bodies = ["other bodies", "their body", "embodied others"]
        has_other_bodies = sum(1 for phrase in other_bodies if phrase in text_lower)

        # Direct perception of others
        direct_perception = ["see them", "perceive others", "directly experience"]
        has_direct_perception = sum(1 for phrase in direct_perception if phrase in text_lower)

        # Shared world indicators
        shared_world = ["shared world", "common world", "together", "collective"]
        has_shared_world = sum(1 for phrase in shared_world if phrase in text_lower)

        # Inference/analogy (not direct perception)
        inference_words = ["infer", "analogical", "deduce", "assume"]
        has_inference = sum(1 for word in inference_words if word in text_lower)

        if has_intersubjectivity >= 1 and has_other_bodies >= 1:
            status = "Embodied Intersubjectivity"
            description = "Intersubjectivity through embodied perception of other bodies"
            mode = "Perceptual"
        elif has_shared_world >= 1:
            status = "Shared World"
            description = "Common perceptual world with others"
            mode = "Collective"
        elif has_inference >= 1:
            status = "Inferential Approach"
            description = "Others known through inference - not direct perception"
            mode = "Intellectualist"
        else:
            status = "No Clear Intersubjectivity"
            description = "Intersubjectivity not clearly evident"
            mode = "None"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "principle": "Intersubjectivity through direct embodied perception of other bodies"
        }

    def _construct_reasoning(
        self,
        lived_body: Dict[str, Any],
        perception: Dict[str, Any],
        flesh: Dict[str, Any],
        ambiguity: Dict[str, Any]
    ) -> str:
        """Construct Merleau-Pontian phenomenological reasoning."""
        reasoning = (
            f"From Merleau-Ponty's phenomenological perspective, lived body: {lived_body['description']}. "
            f"Perception: {perception['description']}. "
            f"Flesh: {flesh['description']}. "
            f"Ambiguity: {ambiguity['description']}. "
        )

        # Conclude with Merleau-Pontian principles
        reasoning += (
            "We are embodied beings-in-the-world. "
            "Perception is our primary, pre-reflective access to reality. "
            "The body is both sensing and sensible - reversibility of the flesh. "
            "Ambiguity is fundamental to embodied existence, not a defect to overcome."
        )

        return reasoning
