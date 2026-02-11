"""
Edmund Husserl - Founder of Phenomenology

Edmund Husserl (1859-1938)
Focus: Phenomenology, Consciousness, Intentionality, Transcendental Subjectivity

Key Concepts:
- Phenomenological Reduction (Epoché): Bracketing the natural attitude
- Intentionality: Consciousness is always consciousness-of-something
- Noesis and Noema: Acts of consciousness and their intentional objects
- Lifeworld (Lebenswelt): Pre-theoretical background of lived experience
- Transcendental Ego: The pure I as constituting subject
- Essence (Eidos): Eidetic intuition of essential structures
- Horizons: Inner and outer horizons of experiential givenness
- Time-Consciousness: Retention, primal impression, protention
- Intersubjectivity: Constitution of other subjects in experience
- Evidence (Evidenz): Self-givenness and fulfillment of intention
- Natural Attitude vs Phenomenological Attitude
- Constitution: How consciousness constitutes objects and meaning
- Categorial Intuition: Grasping formal and material essences
- Apodictic Evidence: Absolute certainty and self-evidence
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Husserl(Philosopher):
    """
    Edmund Husserl's transcendental phenomenology.

    Analyzes prompts through the lens of pure consciousness, intentionality,
    phenomenological reduction, eidetic structures, and transcendental constitution.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Edmund Husserl",
            description="Founder of phenomenology - focused on consciousness, intentionality, and transcendental constitution",
        )
        self.tradition = "Phenomenology"
        self.key_concepts = ['intentionality', 'epoché (bracketing)', 'lifeworld (Lebenswelt)', 'transcendental reduction', 'noema and noesis']

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Husserl's phenomenological perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Husserl's phenomenological analysis
        """
        # Perform comprehensive Husserlian phenomenological analysis
        analysis = self._analyze_consciousness(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Transcendental Phenomenology",
            "tension": tension,
            "key_concepts": analysis["concepts"],
            "questions": analysis["questions"],
            "epoche": analysis["epoche"],
            "intentionality": analysis["intentionality"],
            "noesis_noema": analysis["noesis_noema"],
            "lifeworld": analysis["lifeworld"],
            "transcendental_ego": analysis["transcendental_ego"],
            "essence": analysis["essence"],
            "horizons": analysis["horizons"],
            "time_consciousness": analysis["time_consciousness"],
            "intersubjectivity": analysis["intersubjectivity"],
            "evidence": analysis["evidence"],
            "natural_attitude": analysis["natural_attitude"],
            "constitution": analysis["constitution"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Transcendental phenomenology / Eidetic analysis",
                "focus": "Pure consciousness, intentionality, essences, and transcendental constitution",
            },
        }

    def _analyze_consciousness(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Husserlian phenomenological analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Husserlian dimensions
        epoche = self._assess_epoche(prompt)
        intentionality = self._analyze_intentionality(prompt)
        noesis_noema = self._analyze_noesis_noema(prompt)
        lifeworld = self._assess_lifeworld(prompt)
        transcendental_ego = self._assess_transcendental_ego(prompt)
        essence = self._analyze_essence(prompt)
        horizons = self._analyze_horizons(prompt)
        time_consciousness = self._analyze_time_consciousness(prompt)
        intersubjectivity = self._assess_intersubjectivity(prompt)
        evidence = self._assess_evidence(prompt)
        natural_attitude = self._assess_natural_attitude(prompt)
        constitution = self._analyze_constitution(prompt)

        # Identify key concepts and questions
        concepts = self._identify_concepts(prompt)
        questions = self._generate_questions(prompt, concepts)

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            epoche,
            intentionality,
            noesis_noema,
            lifeworld,
            transcendental_ego,
            essence,
            evidence,
            concepts,
        )

        return {
            "reasoning": reasoning,
            "concepts": concepts,
            "questions": questions,
            "epoche": epoche,
            "intentionality": intentionality,
            "noesis_noema": noesis_noema,
            "lifeworld": lifeworld,
            "transcendental_ego": transcendental_ego,
            "essence": essence,
            "horizons": horizons,
            "time_consciousness": time_consciousness,
            "intersubjectivity": intersubjectivity,
            "evidence": evidence,
            "natural_attitude": natural_attitude,
            "constitution": constitution,
        }

    def _assess_epoche(self, text: str) -> Dict[str, Any]:
        """
        Assess phenomenological reduction (epoché).

        Epoché: Bracketing or suspending the natural attitude
        Putting out of play all presuppositions about existence
        The phenomenological reduction to pure consciousness
        """
        text_lower = text.lower()

        # Epoché/bracketing indicators
        epoche_words = [
            "bracket",
            "suspend",
            "reduction",
            "epoché",
            "epoche",
            "put aside",
            "set aside",
            "parentheses",
            "phenomenological reduction",
        ]
        epoche_count = sum(1 for phrase in epoche_words if phrase in text_lower)

        # Presupposition/assumption indicators
        presupposition_words = [
            "presupposition",
            "assumption",
            "presume",
            "take for granted",
            "assume",
            "belief",
            "prejudice",
            "bias",
        ]
        presupposition_count = sum(
            1 for phrase in presupposition_words if phrase in text_lower
        )

        # Suspension/withholding indicators
        suspension_words = ["suspend", "withhold", "refrain", "abstain", "hold back"]
        suspension_count = sum(1 for word in suspension_words if word in text_lower)

        # Pure consciousness indicators
        pure_consciousness = [
            "pure consciousness",
            "transcendental consciousness",
            "consciousness itself",
            "pure experience",
        ]
        pure_count = sum(1 for phrase in pure_consciousness if phrase in text_lower)

        # Natural attitude indicators (opposite)
        natural_attitude = [
            "natural attitude",
            "take for real",
            "obvious existence",
            "just is",
            "of course exists",
        ]
        natural_count = sum(1 for phrase in natural_attitude if phrase in text_lower)

        if epoche_count >= 1 and suspension_count >= 1:
            status = "Phenomenological Reduction Performed"
            description = "Epoché enacted - bracketing presuppositions to access pure consciousness"
            stage = "Transcendental"
        elif epoche_count >= 1 or presupposition_count >= 2:
            status = "Awareness of Bracketing"
            description = "Recognition of the need to suspend assumptions"
            stage = "Preparatory"
        elif pure_count >= 1:
            status = "Pure Consciousness Sought"
            description = "Seeking pure consciousness without presuppositions"
            stage = "Reductive"
        elif natural_count >= 1:
            status = "Natural Attitude Dominant"
            description = "Remaining within the natural attitude - epoché not performed"
            stage = "Pre-phenomenological"
        else:
            status = "Epoché Status Unclear"
            description = "The phenomenological reduction is not explicitly addressed"
            stage = "Undetermined"

        return {
            "status": status,
            "description": description,
            "stage": stage,
            "epoche_score": epoche_count,
            "suspension_score": suspension_count,
            "presuppositions_noted": presupposition_count,
            "principle": "Epoché: Bracketing the natural attitude to access pure consciousness",
        }

    def _analyze_intentionality(self, text: str) -> Dict[str, Any]:
        """
        Analyze intentionality.

        Intentionality: Consciousness is always consciousness-of-something
        Every act of consciousness is directed toward an object
        The fundamental structure of consciousness
        """
        text_lower = text.lower()

        # Intentionality explicit
        intentionality_words = [
            "intentional",
            "intentionality",
            "directed toward",
            "consciousness of",
            "about something",
        ]
        intentionality_count = sum(
            1 for phrase in intentionality_words if phrase in text_lower
        )

        # Directedness indicators
        directedness_words = ["directed", "aimed at", "toward", "targets", "refers to"]
        directedness_count = sum(
            1 for phrase in directedness_words if phrase in text_lower
        )

        # Object-consciousness indicators
        object_consciousness = [
            "object of consciousness",
            "intended object",
            "what is meant",
            "what is intended",
        ]
        object_count = sum(1 for phrase in object_consciousness if phrase in text_lower)

        # Act-object structure
        act_object = [
            "act and object",
            "thinking about",
            "perceiving something",
            "remembering that",
            "imagining what",
        ]
        act_object_count = sum(1 for phrase in act_object if phrase in text_lower)

        # Reference/aboutness indicators
        reference_words = ["refers to", "about", "concerning", "regarding", "reference"]
        reference_count = sum(1 for word in reference_words if word in text_lower)

        if intentionality_count >= 1:
            status = "Intentionality Explicit"
            description = "Consciousness explicitly recognized as intentional - always of something"
            structure = "Husserlian"
        elif object_count >= 1 or act_object_count >= 1:
            status = "Act-Object Structure"
            description = "Consciousness structured as act directed toward object"
            structure = "Intentional"
        elif directedness_count >= 1 and reference_count >= 1:
            status = "Directedness Present"
            description = "Consciousness shows directedness and reference"
            structure = "Referential"
        elif reference_count >= 2:
            status = "Referential Character"
            description = "Aboutness and reference evident"
            structure = "Referential"
        else:
            status = "Intentionality Not Evident"
            description = "Intentional structure not clearly present"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "intentionality_score": intentionality_count,
            "directedness": directedness_count >= 1,
            "act_object_structure": act_object_count >= 1,
            "principle": "Intentionality: Consciousness is always consciousness-of-something",
        }

    def _analyze_noesis_noema(self, text: str) -> Dict[str, Any]:
        """
        Analyze noesis and noema.

        Noesis: The act of consciousness (perceiving, judging, imagining)
        Noema: The object as intended (the perceived, the judged, the imagined)
        Correlation between act and intended object
        """
        text_lower = text.lower()

        # Noesis indicators (act of consciousness)
        noesis_words = [
            "noesis",
            "act of",
            "perceiving",
            "judging",
            "thinking",
            "intending",
            "experiencing",
            "consciousness acts",
        ]
        noesis_count = sum(1 for phrase in noesis_words if phrase in text_lower)

        # Noema indicators (intended object)
        noema_words = [
            "noema",
            "intended object",
            "as intended",
            "as meant",
            "object-as-intended",
            "sense",
            "meaning",
        ]
        noema_count = sum(1 for phrase in noema_words if phrase in text_lower)

        # Correlation indicators
        correlation_words = ["correlation", "correlate", "corresponding", "parallel"]
        correlation_count = sum(1 for word in correlation_words if word in text_lower)

        # How/what structure (how given vs what given)
        how_what = [
            "how it appears",
            "what appears",
            "manner of givenness",
            "mode of presentation",
        ]
        how_what_count = sum(1 for phrase in how_what if phrase in text_lower)

        # Act-content distinction
        act_content = [
            "act and content",
            "act versus object",
            "subjective and objective",
        ]
        act_content_count = sum(1 for phrase in act_content if phrase in text_lower)

        if (noesis_count >= 1 and noema_count >= 1) or correlation_count >= 1:
            status = "Noesis-Noema Correlation"
            description = (
                "Full noetic-noematic structure - act correlated with intended object"
            )
            structure = "Correlated"
        elif noesis_count >= 1 and how_what_count >= 1:
            status = "Noetic Analysis"
            description = "Focus on acts of consciousness and modes of givenness"
            structure = "Noetic"
        elif noema_count >= 1 or how_what_count >= 1:
            status = "Noematic Analysis"
            description = "Focus on objects-as-intended and their sense"
            structure = "Noematic"
        elif act_content_count >= 1:
            status = "Act-Content Distinction"
            description = "Recognition of distinction between act and content"
            structure = "Preliminary"
        else:
            status = "No Noesis-Noema Structure"
            description = "Noetic-noematic structure not evident"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "noesis_score": noesis_count,
            "noema_score": noema_count,
            "correlation": correlation_count >= 1,
            "principle": "Noesis-Noema: Correlation of act and intended object",
        }

    def _assess_lifeworld(self, text: str) -> Dict[str, Any]:
        """
        Assess the lifeworld (Lebenswelt).

        Lifeworld: Pre-theoretical, pre-scientific world of lived experience
        The taken-for-granted background of all experience
        Foundation for all scientific and theoretical activity
        """
        text_lower = text.lower()

        # Lifeworld explicit
        lifeworld_words = ["lifeworld", "lebenswelt", "life-world", "lived world"]
        lifeworld_count = sum(1 for phrase in lifeworld_words if phrase in text_lower)

        # Pre-theoretical indicators
        pretheoretical_words = [
            "pre-theoretical",
            "pre-scientific",
            "before theory",
            "everyday",
            "ordinary experience",
            "lived experience",
        ]
        pretheoretical_count = sum(
            1 for phrase in pretheoretical_words if phrase in text_lower
        )

        # Background/ground indicators
        background_words = [
            "background",
            "ground",
            "horizon",
            "context",
            "taken for granted",
            "presupposed",
            "tacit",
        ]
        background_count = sum(1 for phrase in background_words if phrase in text_lower)

        # Everyday world indicators
        everyday_words = [
            "everyday",
            "ordinary",
            "common",
            "familiar",
            "daily life",
            "mundane",
            "quotidian",
        ]
        everyday_count = sum(1 for word in everyday_words if word in text_lower)

        # Scientific/theoretical (contrasted with lifeworld)
        scientific_words = ["scientific", "theoretical", "abstract", "formalized"]
        scientific_count = sum(1 for word in scientific_words if word in text_lower)

        if lifeworld_count >= 1:
            status = "Lifeworld Explicit"
            description = "The lifeworld explicitly recognized as ground of experience"
            character = "Phenomenological"
        elif pretheoretical_count >= 1 and background_count >= 1:
            status = "Pre-theoretical Ground"
            description = "Recognition of pre-theoretical background of experience"
            character = "Foundational"
        elif everyday_count >= 1 and scientific_count >= 1:
            status = "Everyday vs Scientific"
            description = (
                "Contrast between lived experience and theoretical abstraction"
            )
            character = "Contrasted"
        elif everyday_count >= 2:
            status = "Everyday Experience"
            description = "Focus on ordinary, everyday world"
            character = "Mundane"
        else:
            status = "Lifeworld Not Evident"
            description = "The lifeworld is not explicitly addressed"
            character = "None"

        return {
            "status": status,
            "description": description,
            "character": character,
            "lifeworld_score": lifeworld_count,
            "pretheoretical": pretheoretical_count >= 1,
            "background_noted": background_count >= 1,
            "principle": "Lifeworld: Pre-theoretical ground of all experience and science",
        }

    def _assess_transcendental_ego(self, text: str) -> Dict[str, Any]:
        """
        Assess the transcendental ego.

        Transcendental Ego: The pure I as constituting subject
        Not the empirical self but the pure pole of identity
        The subject for whom objects are constituted
        """
        text_lower = text.lower()

        # Transcendental ego explicit
        transcendental_ego = [
            "transcendental ego",
            "transcendental i",
            "pure i",
            "pure ego",
            "transcendental subject",
        ]
        transcendental_count = sum(
            1 for phrase in transcendental_ego if phrase in text_lower
        )

        # Constituting subject indicators
        constituting_words = [
            "constituting",
            "constitute",
            "constitution",
            "constitutive",
            "subject constitutes",
        ]
        constituting_count = sum(
            1 for phrase in constituting_words if phrase in text_lower
        )

        # Pure consciousness indicators
        pure_words = [
            "pure consciousness",
            "pure subjectivity",
            "transcendental consciousness",
        ]
        pure_count = sum(1 for phrase in pure_words if phrase in text_lower)

        # Pole of identity indicators
        pole_words = ["pole", "center", "unity", "identical i", "same i"]
        pole_count = sum(1 for phrase in pole_words if phrase in text_lower)

        # Empirical self (contrasted with transcendental ego)
        empirical_words = [
            "empirical self",
            "empirical i",
            "psychological ego",
            "person",
            "individual",
        ]
        empirical_count = sum(1 for phrase in empirical_words if phrase in text_lower)

        if transcendental_count >= 1:
            status = "Transcendental Ego Explicit"
            description = (
                "Pure transcendental I explicitly recognized as constituting subject"
            )
            level = "Transcendental"
        elif constituting_count >= 1 and pure_count >= 1:
            status = "Constituting Subjectivity"
            description = "Pure consciousness as constituting subject"
            level = "Transcendental-implicit"
        elif constituting_count >= 1:
            status = "Constitutive Activity"
            description = "Recognition of constitutive acts of consciousness"
            level = "Constitutive"
        elif empirical_count >= 1 and pure_count == 0:
            status = "Empirical Level"
            description = "Focus on empirical self - not transcendental reduction"
            level = "Empirical"
        else:
            status = "Transcendental Ego Not Evident"
            description = "The transcendental ego is not addressed"
            level = "None"

        return {
            "status": status,
            "description": description,
            "level": level,
            "transcendental_score": transcendental_count,
            "constituting": constituting_count >= 1,
            "pure_consciousness": pure_count >= 1,
            "principle": "Transcendental Ego: Pure I as pole of constituting acts",
        }

    def _analyze_essence(self, text: str) -> Dict[str, Any]:
        """
        Analyze essence (eidos) and eidetic intuition.

        Essence: Essential structures given in eidetic intuition
        Eidetic variation: Free variation in imagination to grasp essence
        Essential vs factual truth
        """
        text_lower = text.lower()

        # Essence/eidos explicit
        essence_words = [
            "essence",
            "eidos",
            "essential",
            "eidetic",
            "necessary",
            "invariant",
            "universal",
        ]
        essence_count = sum(1 for word in essence_words if word in text_lower)

        # Eidetic intuition/variation
        eidetic_words = [
            "eidetic intuition",
            "eidetic variation",
            "free variation",
            "imaginative variation",
            "essence intuition",
        ]
        eidetic_count = sum(1 for phrase in eidetic_words if phrase in text_lower)

        # Necessary/universal structure
        necessary_words = [
            "necessary",
            "must be",
            "cannot be otherwise",
            "universal",
            "always",
            "invariant",
        ]
        necessary_count = sum(1 for phrase in necessary_words if phrase in text_lower)

        # Essential vs factual
        essential_factual = [
            "essential versus factual",
            "essence and fact",
            "necessary and contingent",
            "eidetic and empirical",
        ]
        essential_factual_count = sum(
            1 for phrase in essential_factual if phrase in text_lower
        )

        # Contingent/factual (contrasted with essential)
        contingent_words = [
            "contingent",
            "factual",
            "accidental",
            "merely happens",
            "could be otherwise",
        ]
        contingent_count = sum(1 for phrase in contingent_words if phrase in text_lower)

        if eidetic_count >= 1:
            status = "Eidetic Intuition"
            description = "Eidetic variation to grasp essential structures"
            mode = "Eidetic"
        elif essence_count >= 2 and necessary_count >= 1:
            status = "Essential Analysis"
            description = "Focus on essential, necessary structures"
            mode = "Essential"
        elif essential_factual_count >= 1:
            status = "Essential-Factual Distinction"
            description = "Recognition of distinction between essence and fact"
            mode = "Discriminating"
        elif essence_count >= 1:
            status = "Essence Noted"
            description = "Essences mentioned but not fully analyzed"
            mode = "Preliminary"
        elif contingent_count >= 1 and essence_count == 0:
            status = "Factual Level"
            description = "Focus on facts - not essential analysis"
            mode = "Empirical"
        else:
            status = "No Eidetic Analysis"
            description = "Essential structures not addressed"
            mode = "None"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "essence_score": essence_count,
            "eidetic_intuition": eidetic_count >= 1,
            "necessary_structures": necessary_count >= 1,
            "principle": "Eidos: Essential structures grasped through eidetic intuition",
        }

    def _analyze_horizons(self, text: str) -> Dict[str, Any]:
        """
        Analyze horizons of experience.

        Horizons: Every experience has inner and outer horizons
        Inner horizon: Unseen sides and aspects of the object itself
        Outer horizon: Context and co-given world
        """
        text_lower = text.lower()

        # Horizon explicit
        horizon_words = ["horizon", "horizons", "horizonal"]
        horizon_count = sum(1 for word in horizon_words if word in text_lower)

        # Inner horizon indicators
        inner_horizon = [
            "inner horizon",
            "unseen sides",
            "back side",
            "hidden aspects",
            "more to see",
        ]
        inner_count = sum(1 for phrase in inner_horizon if phrase in text_lower)

        # Outer horizon indicators
        outer_horizon = [
            "outer horizon",
            "context",
            "surrounding world",
            "background",
            "field",
        ]
        outer_count = sum(1 for phrase in outer_horizon if phrase in text_lower)

        # Implicit/co-given indicators
        implicit_words = [
            "implicit",
            "co-given",
            "tacit",
            "presupposed",
            "background",
            "surrounding",
        ]
        implicit_count = sum(1 for word in implicit_words if word in text_lower)

        # Perspective/aspect indicators
        perspective_words = [
            "perspective",
            "aspect",
            "side",
            "profile",
            "view",
            "appearance",
        ]
        perspective_count = sum(1 for word in perspective_words if word in text_lower)

        if horizon_count >= 1 and (inner_count >= 1 or outer_count >= 1):
            status = "Horizonal Structure"
            description = "Explicit recognition of inner and outer horizons"
            structure = "Full"
        elif horizon_count >= 1:
            status = "Horizon Mentioned"
            description = "Horizonal character noted"
            structure = "General"
        elif perspective_count >= 1 and implicit_count >= 1:
            status = "Perspectival Givenness"
            description = "Objects given in perspectives with implicit horizons"
            structure = "Perspectival"
        elif implicit_count >= 2:
            status = "Implicit Co-givenness"
            description = "Recognition of implicit, co-given dimensions"
            structure = "Implicit"
        else:
            status = "No Horizonal Analysis"
            description = "Horizons not addressed"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "horizon_score": horizon_count,
            "inner_horizon": inner_count >= 1,
            "outer_horizon": outer_count >= 1,
            "principle": "Horizons: Every experience has inner and outer horizons",
        }

    def _analyze_time_consciousness(self, text: str) -> Dict[str, Any]:
        """
        Analyze time-consciousness.

        Time-Consciousness: Retention, primal impression, protention
        Retention: Just-past held in consciousness
        Primal impression: The now-point
        Protention: Anticipation of what's coming
        """
        text_lower = text.lower()

        # Time-consciousness explicit
        time_consciousness = [
            "time-consciousness",
            "internal time",
            "temporal consciousness",
        ]
        time_consciousness_count = sum(
            1 for phrase in time_consciousness if phrase in text_lower
        )

        # Retention indicators
        retention_words = [
            "retention",
            "just-past",
            "retained",
            "still present",
            "fading",
            "receding",
        ]
        retention_count = sum(1 for phrase in retention_words if phrase in text_lower)

        # Primal impression indicators
        primal_impression = [
            "primal impression",
            "now-point",
            "living present",
            "impression",
            "present moment",
        ]
        impression_count = sum(
            1 for phrase in primal_impression if phrase in text_lower
        )

        # Protention indicators
        protention_words = [
            "protention",
            "anticipate",
            "expect",
            "coming",
            "about to",
            "future horizon",
        ]
        protention_count = sum(1 for phrase in protention_words if phrase in text_lower)

        # Temporal flow indicators
        flow_words = [
            "flow",
            "stream",
            "temporal flux",
            "flowing",
            "succession",
            "temporal synthesis",
        ]
        flow_count = sum(1 for phrase in flow_words if phrase in text_lower)

        # Past-present-future structure
        if retention_count >= 1 and impression_count >= 1 and protention_count >= 1:
            status = "Full Temporal Structure"
            description = "Complete structure: retention-impression-protention"
            structure = "Tripartite"
        elif time_consciousness_count >= 1:
            status = "Time-Consciousness Explicit"
            description = "Internal time-consciousness explicitly addressed"
            structure = "Husserlian"
        elif flow_count >= 1 and (retention_count >= 1 or protention_count >= 1):
            status = "Temporal Synthesis"
            description = "Recognition of temporal flow and synthesis"
            structure = "Synthetic"
        elif impression_count >= 1 or retention_count >= 1:
            status = "Temporal Dimension"
            description = "Some temporal structure present"
            structure = "Partial"
        else:
            status = "No Time-Consciousness"
            description = "Time-consciousness not addressed"
            structure = "None"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "retention": retention_count >= 1,
            "primal_impression": impression_count >= 1,
            "protention": protention_count >= 1,
            "principle": "Time-consciousness: Retention-impression-protention structure",
        }

    def _assess_intersubjectivity(self, text: str) -> Dict[str, Any]:
        """
        Assess intersubjectivity.

        Intersubjectivity: Constitution of other subjects in experience
        Other egos given through empathy (Einfühlung)
        Constitution of objective world through intersubjective agreement
        """
        text_lower = text.lower()

        # Intersubjectivity explicit
        intersubjectivity_words = [
            "intersubjectivity",
            "intersubjective",
            "other subjects",
            "other egos",
        ]
        intersubjectivity_count = sum(
            1 for phrase in intersubjectivity_words if phrase in text_lower
        )

        # Empathy/Einfühlung indicators
        empathy_words = [
            "empathy",
            "einfühlung",
            "appresentation",
            "analogical apperception",
            "pairing",
        ]
        empathy_count = sum(1 for phrase in empathy_words if phrase in text_lower)

        # Other minds/subjects
        other_minds = [
            "other minds",
            "others",
            "other people",
            "other persons",
            "fellow subjects",
            "we",
            "community",
        ]
        other_count = sum(1 for phrase in other_minds if phrase in text_lower)

        # Objective world indicators
        objective_world = [
            "objective world",
            "shared world",
            "common world",
            "intersubjectively constituted",
        ]
        objective_count = sum(1 for phrase in objective_world if phrase in text_lower)

        # Solipsism (problem to be overcome)
        solipsism_words = ["solipsism", "only i", "alone", "isolated consciousness"]
        solipsism_count = sum(1 for phrase in solipsism_words if phrase in text_lower)

        if intersubjectivity_count >= 1 or empathy_count >= 1:
            status = "Intersubjectivity Explicit"
            description = "Intersubjective constitution through empathy and pairing"
            level = "Transcendental"
        elif objective_count >= 1 and other_count >= 1:
            status = "Intersubjective World"
            description = "Recognition of shared, objective world"
            level = "Constituted"
        elif other_count >= 1:
            status = "Others Present"
            description = "Other subjects acknowledged"
            level = "Mundane"
        elif solipsism_count >= 1:
            status = "Solipsism Problem"
            description = "Problem of solipsism raised"
            level = "Problematic"
        else:
            status = "No Intersubjectivity"
            description = "Intersubjectivity not addressed"
            level = "None"

        return {
            "status": status,
            "description": description,
            "level": level,
            "intersubjectivity_score": intersubjectivity_count,
            "empathy": empathy_count >= 1,
            "other_subjects": other_count >= 1,
            "principle": "Intersubjectivity: Other subjects constituted through empathy",
        }

    def _assess_evidence(self, text: str) -> Dict[str, Any]:
        """
        Assess evidence (Evidenz).

        Evidence: Self-givenness and fulfillment of intention
        Apodictic evidence: Absolute, indubitability
        Adequate evidence: Complete givenness
        """
        text_lower = text.lower()

        # Evidence explicit
        evidence_words = ["evidence", "evidenz", "self-evident", "self-givenness"]
        evidence_count = sum(1 for phrase in evidence_words if phrase in text_lower)

        # Self-givenness indicators
        selfgivenness = [
            "self-given",
            "given itself",
            "itself present",
            "bodily present",
            "in person",
        ]
        selfgivenness_count = sum(1 for phrase in selfgivenness if phrase in text_lower)

        # Fulfillment indicators
        fulfillment_words = [
            "fulfillment",
            "fulfilled",
            "fulfilling",
            "verification",
            "confirmed",
        ]
        fulfillment_count = sum(
            1 for phrase in fulfillment_words if phrase in text_lower
        )

        # Apodictic indicators
        apodictic_words = [
            "apodictic",
            "indubitable",
            "absolute certainty",
            "cannot doubt",
            "necessarily",
        ]
        apodictic_count = sum(1 for phrase in apodictic_words if phrase in text_lower)

        # Adequate/inadequate indicators
        adequate_words = ["adequate", "inadequate", "complete givenness", "incomplete"]
        adequate_count = sum(1 for word in adequate_words if word in text_lower)

        # Intuition indicators
        intuition_words = ["intuition", "intuit", "direct seeing", "immediate seeing"]
        intuition_count = sum(1 for phrase in intuition_words if phrase in text_lower)

        if apodictic_count >= 1:
            status = "Apodictic Evidence"
            description = "Absolute, indubitable self-evidence"
            level = "Apodictic"
        elif evidence_count >= 1 and selfgivenness_count >= 1:
            status = "Self-Givenness"
            description = "Objects given themselves in evidence"
            level = "Original"
        elif fulfillment_count >= 1:
            status = "Fulfillment"
            description = "Intentions fulfilled through givenness"
            level = "Fulfilling"
        elif intuition_count >= 1:
            status = "Intuitive Givenness"
            description = "Direct intuitive seeing"
            level = "Intuitive"
        else:
            status = "No Evidence Analysis"
            description = "Evidence not addressed"
            level = "None"

        return {
            "status": status,
            "description": description,
            "level": level,
            "evidence_score": evidence_count,
            "selfgivenness": selfgivenness_count >= 1,
            "apodictic": apodictic_count >= 1,
            "principle": "Evidence: Self-givenness and fulfillment of intention",
        }

    def _assess_natural_attitude(self, text: str) -> Dict[str, Any]:
        """
        Assess natural attitude vs phenomenological attitude.

        Natural attitude: Taking the world as simply existing
        Phenomenological attitude: Suspending existence claims, focusing on givenness
        """
        text_lower = text.lower()

        # Natural attitude explicit
        natural_attitude = [
            "natural attitude",
            "naturally",
            "take for granted",
            "simply exists",
            "just is there",
            "obvious",
        ]
        natural_count = sum(1 for phrase in natural_attitude if phrase in text_lower)

        # Phenomenological attitude explicit
        phenomenological_attitude = [
            "phenomenological attitude",
            "phenomenological standpoint",
            "transcendental standpoint",
            "after reduction",
        ]
        phenomenological_count = sum(
            1 for phrase in phenomenological_attitude if phrase in text_lower
        )

        # Existence belief indicators (natural attitude)
        existence_belief = [
            "really exists",
            "out there",
            "independent reality",
            "actual world",
            "objective reality",
        ]
        existence_count = sum(1 for phrase in existence_belief if phrase in text_lower)

        # Suspension/bracketing (phenomenological attitude)
        suspension = [
            "suspend",
            "bracket",
            "put aside",
            "neutralize",
            "set aside existence",
        ]
        suspension_count = sum(1 for phrase in suspension if phrase in text_lower)

        # How it appears (phenomenological focus)
        how_appears = [
            "how it appears",
            "as it appears",
            "mode of givenness",
            "manner of appearance",
        ]
        how_appears_count = sum(1 for phrase in how_appears if phrase in text_lower)

        if phenomenological_count >= 1 or suspension_count >= 1:
            attitude = "Phenomenological Attitude"
            description = (
                "Phenomenological standpoint - focus on givenness, not existence"
            )
            stance = "Phenomenological"
        elif how_appears_count >= 1:
            attitude = "Descriptive Focus"
            description = "Focus on how things appear - moving toward phenomenology"
            stance = "Descriptive"
        elif natural_count >= 1 or existence_count >= 1:
            attitude = "Natural Attitude"
            description = "Natural attitude - taking world as simply existing"
            stance = "Natural"
        else:
            attitude = "Attitude Unclear"
            description = (
                "Neither natural nor phenomenological attitude clearly present"
            )
            stance = "Undetermined"

        return {
            "attitude": attitude,
            "description": description,
            "stance": stance,
            "natural_score": natural_count,
            "phenomenological_score": phenomenological_count,
            "suspension": suspension_count >= 1,
            "principle": "Natural attitude takes world as existing; phenomenological attitude brackets this",
        }

    def _analyze_constitution(self, text: str) -> Dict[str, Any]:
        """
        Analyze constitution.

        Constitution: How consciousness constitutes objects and meaning
        Not creation but sense-giving and validity-constitution
        Active and passive synthesis
        """
        text_lower = text.lower()

        # Constitution explicit
        constitution_words = [
            "constitution",
            "constitute",
            "constituted",
            "constitutive",
            "sense-giving",
        ]
        constitution_count = sum(
            1 for phrase in constitution_words if phrase in text_lower
        )

        # Synthesis indicators
        synthesis_words = [
            "synthesis",
            "synthetic",
            "synthesize",
            "active synthesis",
            "passive synthesis",
        ]
        synthesis_count = sum(1 for phrase in synthesis_words if phrase in text_lower)

        # Meaning/sense-giving
        meaning_giving = [
            "meaning",
            "sense",
            "significance",
            "sense-giving",
            "bestow meaning",
        ]
        meaning_count = sum(1 for phrase in meaning_giving if phrase in text_lower)

        # Active vs passive
        active_passive = ["active", "passive", "receptivity", "spontaneity"]
        active_passive_count = sum(1 for word in active_passive if word in text_lower)

        # Association/genesis indicators
        genesis_words = [
            "association",
            "genesis",
            "genetic",
            "sedimentation",
            "habituality",
        ]
        genesis_count = sum(1 for word in genesis_words if word in text_lower)

        if constitution_count >= 2 or (
            constitution_count >= 1 and synthesis_count >= 1
        ):
            status = "Constitutive Analysis"
            description = "Explicit analysis of how consciousness constitutes objects"
            mode = "Transcendental"
        elif constitution_count >= 1:
            status = "Constitution Noted"
            description = "Constitution mentioned"
            mode = "General"
        elif synthesis_count >= 1 and meaning_count >= 1:
            status = "Synthetic Activity"
            description = "Recognition of synthetic meaning-giving"
            mode = "Synthetic"
        elif genesis_count >= 1:
            status = "Genetic Analysis"
            description = "Focus on genesis and sedimentation"
            mode = "Genetic"
        else:
            status = "No Constitutional Analysis"
            description = "Constitution not addressed"
            mode = "None"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "constitution_score": constitution_count,
            "synthesis": synthesis_count >= 1,
            "meaning_giving": meaning_count >= 1,
            "principle": "Constitution: Consciousness constitutes meaning and validity",
        }

    def _identify_concepts(self, text: str) -> List[str]:
        """Identify key Husserlian concepts in the text."""
        text_lower = text.lower()
        concepts = []

        concept_map = {
            "Intentionality": [
                "intentional",
                "consciousness of",
                "directed toward",
                "about",
            ],
            "Phenomenological Reduction": ["epoché", "bracket", "reduction", "suspend"],
            "Essence (Eidos)": ["essence", "essential", "eidetic", "necessary"],
            "Evidence": ["evidence", "self-given", "intuition", "evident"],
            "Constitution": ["constitute", "constituted", "constitutive"],
            "Lifeworld": ["lifeworld", "lived world", "everyday", "pre-theoretical"],
            "Time-Consciousness": ["time", "temporal", "retention", "protention"],
            "Horizons": ["horizon", "context", "background", "implicit"],
            "Noesis-Noema": ["noesis", "noema", "act", "object"],
            "Transcendental Ego": ["transcendental", "pure ego", "pure i"],
            "Intersubjectivity": ["intersubjective", "others", "empathy"],
            "Natural Attitude": ["natural attitude", "take for granted", "obvious"],
        }

        for concept, keywords in concept_map.items():
            if any(word in text_lower for word in keywords):
                concepts.append(concept)

        if not concepts:
            concepts.append("Intentionality")

        return concepts

    def _generate_questions(self, text: str, concepts: List[str]) -> List[str]:
        """Generate Husserlian phenomenological questions based on the analysis."""
        questions = []

        # Core phenomenological question
        questions.append("What is given in consciousness, and how is it given?")

        # Based on concepts
        if "Intentionality" in concepts:
            questions.append("What is consciousness directed toward here?")
        if "Phenomenological Reduction" in concepts:
            questions.append("What remains after bracketing all existence claims?")
        if "Essence (Eidos)" in concepts:
            questions.append("What are the essential, invariant structures?")
        if "Constitution" in concepts:
            questions.append(
                "How does consciousness constitute this object and its meaning?"
            )
        if "Evidence" in concepts:
            questions.append("Is this given in self-evidence or merely signified?")
        if "Lifeworld" in concepts:
            questions.append("What is the pre-theoretical lifeworld ground?")

        return questions[:5]  # Limit to 5 questions

    def _construct_reasoning(
        self,
        epoche: Dict[str, Any],
        intentionality: Dict[str, Any],
        noesis_noema: Dict[str, Any],
        lifeworld: Dict[str, Any],
        transcendental_ego: Dict[str, Any],
        essence: Dict[str, Any],
        evidence: Dict[str, Any],
        concepts: List[str],
    ) -> str:
        """Construct comprehensive Husserlian phenomenological reasoning."""
        reasoning = (
            f"From Husserl's transcendental phenomenological perspective, we must analyze "
            f"what is given in pure consciousness. "
            f"Epoché: {epoche['description']}. "
        )

        # Add intentionality
        reasoning += f"Intentionality: {intentionality['description']}. "

        # Add noesis-noema if present
        if noesis_noema["status"] != "No Noesis-Noema Structure":
            reasoning += f"Noetic-noematic structure: {noesis_noema['description']}. "

        # Add evidence
        reasoning += f"Evidence: {evidence['description']}. "

        # Add essence if present
        if essence["status"] != "No Eidetic Analysis":
            reasoning += f"Essential analysis: {essence['description']}. "

        # Add lifeworld if present
        if lifeworld["status"] != "Lifeworld Not Evident":
            reasoning += f"Lifeworld: {lifeworld['description']}. "

        # Add transcendental ego if present
        if transcendental_ego["status"] != "Transcendental Ego Not Evident":
            reasoning += (
                f"Transcendental subjectivity: {transcendental_ego['description']}. "
            )

        # Conclude with phenomenological principles
        reasoning += (
            "Through rigorous phenomenological analysis, we return 'to the things themselves' (zu den Sachen selbst). "
            "Consciousness is essentially intentional - always directed toward objects. "
            "By performing the epoché and examining pure consciousness, we uncover the essential structures "
            "and constitutive activities through which meaning and validity arise."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Husserlian analysis.

        Tensions arise from:
        - Remaining in natural attitude without epoché
        - Lack of essential analysis (stuck in factuality)
        - Missing intentional analysis
        - No recognition of constitutive activity
        - Absence of evidence/self-givenness
        """
        tension_score = 0
        tension_elements = []

        # Check epoché
        epoche = analysis["epoche"]
        if epoche["stage"] == "Pre-phenomenological":
            tension_score += 2
            tension_elements.append(
                "Remaining in natural attitude - epoché not performed"
            )
        elif epoche["stage"] == "Undetermined":
            tension_score += 1
            tension_elements.append("Unclear phenomenological stance")

        # Check intentionality
        intentionality = analysis["intentionality"]
        if intentionality["structure"] == "None":
            tension_score += 2
            tension_elements.append("Intentional structure not recognized")

        # Check essence
        essence = analysis["essence"]
        if essence["mode"] == "Empirical":
            tension_score += 1
            tension_elements.append("Stuck in factual realm - no essential analysis")
        elif essence["mode"] == "None":
            tension_score += 1
            tension_elements.append("Essential structures not addressed")

        # Check evidence
        evidence = analysis["evidence"]
        if evidence["level"] == "None":
            tension_score += 1
            tension_elements.append("No analysis of evidence and self-givenness")

        # Check constitution
        constitution = analysis["constitution"]
        if constitution["mode"] == "None":
            tension_score += 1
            tension_elements.append("Constitutive activity not recognized")

        # Check natural attitude
        natural_attitude = analysis["natural_attitude"]
        if natural_attitude["stance"] == "Natural":
            tension_score += 1
            tension_elements.append("Natural attitude not transcended")

        # Determine tension level
        if tension_score >= 6:
            level = "Very High"
            description = (
                "Deep pre-phenomenological stance - natural attitude dominates"
            )
        elif tension_score >= 4:
            level = "High"
            description = "Significant lack of phenomenological analysis"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some phenomenological insights but incomplete"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor gaps in phenomenological rigor"
        else:
            level = "Very Low"
            description = "Rigorous phenomenological analysis"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
