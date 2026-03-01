"""
Hegel - German Idealist Philosopher

Georg Wilhelm Friedrich Hegel (1770-1831)
Focus: Dialectic, Absolute Idealism, Phenomenology of Spirit, Historical Development

Key Concepts:
- Dialectic: Thesis-Antithesis-Synthesis / Aufhebung (sublation)
- Geist (Spirit/Mind): Absolute Spirit realizing itself through history
- Phenomenology of Spirit: Journey of consciousness to absolute knowing
- Master-Slave Dialectic: Recognition and self-consciousness through struggle
- Absolute Idealism: Reality is the self-development of Spirit/Absolute
- Concrete Universal: The universal that contains and develops its particulars
- Contradiction: Engine of development, not logical error
- History as Progress: Spirit's self-realization through historical development
- Freedom: Spirit's essential nature, realized in rational state
- The Absolute: The whole, truth as systematic totality
- Recognition (Anerkennung): Mutual recognition constituting self-consciousness
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Hegel(Philosopher):
    """
    Hegel's absolute idealism and dialectical philosophy.

    Analyzes prompts through the lens of dialectical development, Spirit's
    self-realization, contradiction as productive, and historical progress.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Georg Wilhelm Friedrich Hegel",
            description="German Idealist focused on dialectical development, Absolute Spirit, and historical reason",
        )
        self.tradition = "German Idealism / Dialectics"
        self.key_concepts = [
            "dialectic (thesis-antithesis-synthesis)",
            "Absolute Spirit",
            "Aufhebung (sublation)",
            "master-slave dialectic",
            "philosophy of history",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Hegel's dialectical idealist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Hegel's philosophical analysis
        """
        # Perform comprehensive Hegelian analysis
        analysis = self._analyze_hegelian_framework(prompt)

        # Calculate tension (dialectical contradiction)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Absolute Idealism / Dialectical Philosophy",
            "tension": tension,
            "dialectic": analysis["dialectic"],
            "geist": analysis["geist"],
            "phenomenology": analysis["phenomenology"],
            "master_slave": analysis["master_slave"],
            "absolute_idealism": analysis["absolute_idealism"],
            "concrete_universal": analysis["concrete_universal"],
            "contradiction": analysis["contradiction"],
            "history": analysis["history"],
            "freedom": analysis["freedom"],
            "absolute": analysis["absolute"],
            "recognition": analysis["recognition"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Dialectical idealism and systematic philosophy",
                "focus": "Spirit's self-realization through dialectical development",
            },
        }

    def _analyze_hegelian_framework(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Hegelian dialectical analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Hegelian dimensions
        dialectic = self._analyze_dialectic(prompt)
        geist = self._analyze_geist(prompt)
        phenomenology = self._analyze_phenomenology(prompt)
        master_slave = self._analyze_master_slave_dialectic(prompt)
        absolute_idealism = self._analyze_absolute_idealism(prompt)
        concrete_universal = self._analyze_concrete_universal(prompt)
        contradiction = self._analyze_contradiction(prompt)
        history = self._analyze_history(prompt)
        freedom = self._analyze_freedom(prompt)
        absolute = self._analyze_absolute(prompt)
        recognition = self._analyze_recognition(prompt)

        # Construct comprehensive dialectical reasoning
        reasoning = self._construct_reasoning(
            prompt,
            dialectic,
            geist,
            phenomenology,
            master_slave,
            contradiction,
            history,
            freedom,
            absolute,
        )

        return {
            "reasoning": reasoning,
            "dialectic": dialectic,
            "geist": geist,
            "phenomenology": phenomenology,
            "master_slave": master_slave,
            "absolute_idealism": absolute_idealism,
            "concrete_universal": concrete_universal,
            "contradiction": contradiction,
            "history": history,
            "freedom": freedom,
            "absolute": absolute,
            "recognition": recognition,
        }

    def _analyze_dialectic(self, text: str) -> Dict[str, Any]:
        """
        Analyze dialectical movement: Thesis-Antithesis-Synthesis / Aufhebung.

        Dialectic is the process by which Spirit develops through contradiction
        and sublation (Aufhebung) - negating, preserving, and elevating.
        """
        text_lower = text.lower()

        # Dialectical movement indicators
        thesis_words = ["position", "thesis", "claim", "assertion", "affirmation"]
        antithesis_words = [
            "opposite",
            "negation",
            "antithesis",
            "contradiction",
            "counter",
        ]
        synthesis_words = [
            "synthesis",
            "reconcile",
            "unite",
            "overcome",
            "sublate",
            "aufheben",
        ]

        has_thesis = sum(1 for word in thesis_words if word in text_lower)
        has_antithesis = sum(1 for word in antithesis_words if word in text_lower)
        has_synthesis = sum(1 for word in synthesis_words if word in text_lower)

        # Aufhebung (sublation) - canceling, preserving, and elevating
        aufhebung_words = ["preserve", "elevate", "transcend", "sublate", "both and"]
        has_aufhebung = sum(1 for phrase in aufhebung_words if phrase in text_lower)

        # Negation of negation
        negation_words = ["negate", "negative", "denial", "not"]
        negation_count = sum(1 for word in negation_words if word in text_lower)
        double_negation = negation_count >= 2

        # Movement/development indicators
        movement_words = [
            "develop",
            "evolve",
            "progress",
            "unfold",
            "become",
            "movement",
        ]
        sum(1 for word in movement_words if word in text_lower)

        # Determine dialectical stage
        if has_synthesis >= 1 or has_aufhebung >= 2:
            stage = "Synthesis/Aufhebung"
            description = "Dialectical sublation - negating, preserving, and elevating contradictions"
            movement_type = "Complete dialectical movement"
        elif has_antithesis >= 1 and has_thesis >= 1:
            stage = "Thesis-Antithesis"
            description = "Dialectical opposition present - awaiting synthesis"
            movement_type = "Partial dialectical movement"
        elif has_antithesis >= 1 or negation_count >= 1:
            stage = "Negation"
            description = "Moment of negation - dialectical opposition"
            movement_type = "Negative moment"
        elif has_thesis >= 1:
            stage = "Thesis/Immediacy"
            description = "Initial position - not yet dialectically developed"
            movement_type = "Abstract immediacy"
        else:
            stage = "Pre-dialectical"
            description = "No clear dialectical movement"
            movement_type = "Static"

        return {
            "stage": stage,
            "description": description,
            "movement_type": movement_type,
            "has_thesis": has_thesis >= 1,
            "has_antithesis": has_antithesis >= 1,
            "has_synthesis": has_synthesis >= 1,
            "aufhebung": has_aufhebung >= 1,
            "double_negation": double_negation,
            "principle": "The dialectic is the self-movement of the concept through contradiction to higher unity",
        }

    def _analyze_geist(self, text: str) -> Dict[str, Any]:
        """
        Analyze Geist (Spirit/Mind) and its self-realization.

        Geist is the Absolute realizing itself through history and consciousness.
        It is both substance and subject - the whole that develops itself.
        """
        text_lower = text.lower()

        # Spirit/mind indicators
        spirit_words = [
            "spirit",
            "mind",
            "geist",
            "consciousness",
            "reason",
            "rational",
        ]
        spirit_count = sum(1 for word in spirit_words if word in text_lower)

        # Self-realization indicators
        self_real_words = [
            "realize",
            "actualize",
            "manifest",
            "express",
            "unfold itself",
        ]
        has_self_realization = sum(
            1 for phrase in self_real_words if phrase in text_lower
        )

        # Substance and subject
        substance_words = ["substance", "being", "reality", "what is"]
        subject_words = ["subject", "self", "consciousness", "knower"]

        has_substance = any(word in text_lower for word in substance_words)
        has_subject = any(word in subject_words for word in subject_words)

        # Absolute Spirit indicators
        absolute_words = ["absolute", "whole", "totality", "universal", "infinite"]
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # Self-knowing indicators
        self_know_words = [
            "self-knowledge",
            "know itself",
            "self-aware",
            "self-consciousness",
        ]
        has_self_knowing = any(phrase in text_lower for phrase in self_know_words)

        # Historical manifestation
        historical_words = ["history", "historical", "epoch", "age", "development"]
        has_historical = any(word in text_lower for word in historical_words)

        if spirit_count >= 2 and has_self_realization >= 1 and absolute_count >= 1:
            status = "Absolute Spirit Self-Realizing"
            description = "Spirit coming to know itself through its own development"
            level = "Absolute Knowing"
        elif spirit_count >= 2 and has_self_knowing:
            status = "Self-Conscious Spirit"
            description = "Spirit aware of itself as both substance and subject"
            level = "Self-Consciousness"
        elif spirit_count >= 1 or has_subject:
            status = "Subjective Spirit"
            description = "Consciousness present but not yet fully self-aware"
            level = "Consciousness"
        else:
            status = "No Geist Evident"
            description = "Spirit/consciousness not clearly present"
            level = "Pre-conscious"

        return {
            "status": status,
            "description": description,
            "level": level,
            "spirit_emphasis": spirit_count,
            "self_realization": has_self_realization >= 1,
            "substance_and_subject": has_substance and has_subject,
            "absolute_dimension": absolute_count >= 1,
            "historical_manifestation": has_historical,
            "principle": "Spirit is substance that is also subject - the Absolute realizing itself",
        }

    def _analyze_phenomenology(self, text: str) -> Dict[str, Any]:
        """
        Analyze the phenomenological journey of consciousness.

        The Phenomenology of Spirit traces consciousness's development from
        sense-certainty through self-consciousness to absolute knowing.
        """
        text_lower = text.lower()

        # Stages of consciousness
        stages_identified = []

        # Sense-certainty (immediate awareness)
        if any(
            word in text_lower for word in ["sense", "immediate", "this", "here", "now"]
        ):
            stages_identified.append("Sense-Certainty")

        # Perception (thing with properties)
        if any(
            word in text_lower for word in ["perceive", "object", "thing", "properties"]
        ):
            stages_identified.append("Perception")

        # Understanding (force and law)
        if any(
            word in text_lower for word in ["understand", "law", "force", "explain"]
        ):
            stages_identified.append("Understanding")

        # Self-consciousness
        if any(
            word in text_lower for word in ["self-conscious", "self-awareness", "i am"]
        ):
            stages_identified.append("Self-Consciousness")

        # Reason
        if any(
            word in text_lower for word in ["reason", "rational", "concept", "notion"]
        ):
            stages_identified.append("Reason")

        # Spirit (objective spirit)
        if any(
            word in text_lower for word in ["spirit", "ethical", "community", "culture"]
        ):
            stages_identified.append("Spirit")

        # Absolute knowing
        if any(
            phrase in text_lower
            for phrase in ["absolute knowing", "absolute knowledge", "science"]
        ):
            stages_identified.append("Absolute Knowing")

        # Journey/development indicators
        journey_words = [
            "journey",
            "path",
            "development",
            "progress",
            "ascent",
            "bildung",
        ]
        has_journey = any(word in text_lower for word in journey_words)

        # Experience (Erfahrung) - consciousness testing itself
        experience_words = ["experience", "test", "trial", "prove", "learn"]
        experience_count = sum(1 for word in experience_words if word in text_lower)

        # Determine stage
        if "Absolute Knowing" in stages_identified:
            current_stage = "Absolute Knowing"
            description = "Consciousness has achieved absolute self-knowledge"
            status = "Complete"
        elif "Spirit" in stages_identified:
            current_stage = "Spirit"
            description = "Consciousness recognizes itself in ethical community"
            status = "Advanced"
        elif "Self-Consciousness" in stages_identified:
            current_stage = "Self-Consciousness"
            description = "Consciousness aware of itself as conscious"
            status = "Developing"
        elif len(stages_identified) >= 1:
            current_stage = stages_identified[0]
            description = f"At the stage of {stages_identified[0]}"
            status = "Early"
        else:
            current_stage = "Undetermined"
            description = "Phenomenological stage unclear"
            status = "Unknown"

        return {
            "current_stage": current_stage,
            "description": description,
            "status": status,
            "stages_identified": stages_identified,
            "stage_count": len(stages_identified),
            "has_journey": has_journey,
            "experience_emphasis": experience_count,
            "principle": "Consciousness develops through its own self-testing experience toward absolute knowing",
        }

    def _analyze_master_slave_dialectic(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Master-Slave (Herrschaft und Knechtschaft) dialectic.

        The struggle for recognition where consciousness confronts another consciousness.
        The slave, through work, achieves self-consciousness that the master lacks.
        """
        text_lower = text.lower()

        # Master indicators
        master_words = ["master", "lord", "dominate", "control", "command", "ruler"]
        has_master = sum(1 for word in master_words if word in text_lower)

        # Slave/servant indicators
        slave_words = ["slave", "servant", "subordinate", "servitude", "bondage"]
        has_slave = sum(1 for word in slave_words if word in text_lower)

        # Recognition (Anerkennung)
        recognition_words = ["recognize", "recognition", "acknowledge", "anerkennung"]
        has_recognition = sum(1 for word in recognition_words if word in text_lower)

        # Struggle/conflict
        struggle_words = ["struggle", "fight", "conflict", "combat", "life and death"]
        has_struggle = sum(1 for phrase in struggle_words if phrase in text_lower)

        # Work/labor (slave's transformation)
        work_words = ["work", "labor", "toil", "transform", "shape"]
        has_work = sum(1 for word in work_words if word in text_lower)

        # Fear of death
        fear_words = ["fear", "death", "mortality", "afraid"]
        any(word in text_lower for word in fear_words)

        # Independence/dependence
        independence_words = ["independent", "dependent", "dependence", "reliance"]
        any(word in text_lower for word in independence_words)

        # Reversal/transformation
        reversal_words = ["reversal", "transform", "become", "turn into"]
        has_reversal = any(phrase in text_lower for phrase in reversal_words)

        if has_master >= 1 and has_slave >= 1:
            if has_work >= 2 and has_reversal:
                position = "Dialectical Reversal"
                description = "Slave achieves self-consciousness through work while master stagnates"
                moment = "Resolution through labor"
            elif has_struggle >= 1 and has_recognition >= 1:
                position = "Life-and-Death Struggle"
                description = "Two consciousnesses struggling for recognition"
                moment = "Initial confrontation"
            else:
                position = "Master-Slave Relation"
                description = "Asymmetric relation of domination and servitude"
                moment = "Static domination"
        elif has_recognition >= 2 or (has_recognition >= 1 and has_struggle >= 1):
            position = "Struggle for Recognition"
            description = "Consciousness seeking recognition from another consciousness"
            moment = "Pre-master-slave"
        elif has_work >= 2:
            position = "Labor/Work"
            description = "Transformation through work - path to self-consciousness"
            moment = "Slave's moment"
        else:
            position = "No Master-Slave Dialectic"
            description = "Master-slave dialectic not evident"
            moment = "Not applicable"

        return {
            "position": position,
            "description": description,
            "moment": moment,
            "has_master": has_master >= 1,
            "has_slave": has_slave >= 1,
            "has_recognition": has_recognition >= 1,
            "has_struggle": has_struggle >= 1,
            "work_transformation": has_work >= 2,
            "dialectical_reversal": has_reversal,
            "principle": "Self-consciousness requires recognition from another - achieved through struggle and work",
        }

    def _analyze_absolute_idealism(self, text: str) -> Dict[str, Any]:
        """
        Analyze Absolute Idealism.

        Reality is the self-development of the Absolute/Spirit. The real is rational
        and the rational is real. Mind and world are unified in the Absolute.
        """
        text_lower = text.lower()

        # Absolute indicators
        absolute_words = ["absolute", "infinite", "unconditioned", "whole", "totality"]
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # Idealism indicators
        idealism_words = ["ideal", "mind", "spirit", "thought", "concept", "idea"]
        idealism_count = sum(1 for word in idealism_words if word in text_lower)

        # Real is rational
        real_rational = [
            "real is rational",
            "rational is real",
            "actuality",
            "wirklichkeit",
        ]
        has_real_rational = any(phrase in text_lower for phrase in real_rational)

        # Unity of thought and being
        unity_words = ["unity", "identity", "one", "unified", "same"]
        thought_being = ["thought and being", "mind and world", "subject and object"]
        has_unity = sum(1 for word in unity_words if word in text_lower)
        has_thought_being = any(phrase in text_lower for phrase in thought_being)

        # Self-development
        self_dev_words = [
            "self-development",
            "self-unfolding",
            "self-actualization",
            "self-movement",
        ]
        any(phrase in text_lower for phrase in self_dev_words)

        # System/systematic
        system_words = ["system", "systematic", "whole", "complete", "science"]
        has_system = sum(1 for word in system_words if word in text_lower)

        if (
            absolute_count >= 2
            and idealism_count >= 2
            and (has_unity >= 1 or has_thought_being)
        ):
            position = "Absolute Idealism"
            description = "Reality as the self-development of Absolute Spirit - unity of thought and being"
            stance = "Systematic idealism"
        elif idealism_count >= 2 and has_unity >= 1:
            position = "Idealism"
            description = "Reality as mental/spiritual but not yet absolute"
            stance = "Subjective idealism"
        elif has_real_rational:
            position = "Rational Reality"
            description = (
                "Recognition that the real is rational and the rational is real"
            )
            stance = "Hegelian principle"
        elif absolute_count >= 1:
            position = "Absolute Thinking"
            description = "Conceiving of the Absolute/Unconditioned"
            stance = "Philosophical"
        else:
            position = "No Idealism"
            description = "Absolute idealism not evident"
            stance = "Non-idealist"

        return {
            "position": position,
            "description": description,
            "stance": stance,
            "absolute_emphasis": absolute_count,
            "idealism_emphasis": idealism_count,
            "real_is_rational": has_real_rational,
            "thought_being_unity": has_thought_being,
            "systematic": has_system >= 2,
            "principle": "The Absolute is Spirit - reality is the rational self-development of the Idea",
        }

    def _analyze_concrete_universal(self, text: str) -> Dict[str, Any]:
        """
        Analyze the concrete universal (das konkrete Allgemeine).

        The universal is not abstract but contains and develops its particulars.
        The concept realizes itself through its specific manifestations.
        """
        text_lower = text.lower()

        # Universal indicators
        universal_words = ["universal", "general", "all", "every", "whole"]
        universal_count = sum(1 for word in universal_words if word in text_lower)

        # Particular indicators
        particular_words = [
            "particular",
            "specific",
            "individual",
            "instance",
            "example",
        ]
        particular_count = sum(1 for word in particular_words if word in text_lower)

        # Concrete vs abstract
        concrete_words = ["concrete", "actual", "real", "determinate", "specific"]
        abstract_words = ["abstract", "general", "formal", "empty"]

        has_concrete = sum(1 for word in concrete_words if word in text_lower)
        has_abstract = sum(1 for word in abstract_words if word in text_lower)

        # Unity of universal and particular
        unity_phrases = ["unity of", "contains", "includes", "embodies", "manifests"]
        has_unity = sum(1 for phrase in unity_phrases if phrase in text_lower)

        # Development through particulars
        development_words = ["develop", "unfold", "realize", "actualize", "specify"]
        has_development = sum(1 for word in development_words if word in text_lower)

        if universal_count >= 1 and particular_count >= 1 and has_concrete >= 1:
            if has_unity >= 1 or has_development >= 1:
                concept_type = "Concrete Universal"
                description = (
                    "Universal that contains and develops through its particulars"
                )
                status = "Dialectical concept"
            else:
                concept_type = "Universal and Particular"
                description = "Both universal and particular present but not unified"
                status = "Abstract relation"
        elif universal_count >= 1 and has_concrete >= 1:
            concept_type = "Concrete Universality"
            description = "Universal with concrete content"
            status = "Partially dialectical"
        elif universal_count >= 1 and has_abstract >= 1:
            concept_type = "Abstract Universal"
            description = "Universal separated from particulars - one-sided abstraction"
            status = "Undialectical"
        elif particular_count >= 2:
            concept_type = "Mere Particularity"
            description = "Particular instances without universal"
            status = "Empirical"
        else:
            concept_type = "Undetermined"
            description = "Universal/particular relation unclear"
            status = "Unknown"

        return {
            "concept_type": concept_type,
            "description": description,
            "status": status,
            "universal_emphasis": universal_count,
            "particular_emphasis": particular_count,
            "concrete": has_concrete >= 1,
            "develops_through_particulars": has_development >= 1,
            "principle": "The true universal is concrete - it contains and develops its particulars",
        }

    def _analyze_contradiction(self, text: str) -> Dict[str, Any]:
        """
        Analyze contradiction as productive force.

        For Hegel, contradiction is not error but the engine of development.
        All things contain contradictions that drive their self-transformation.
        """
        text_lower = text.lower()

        # Contradiction indicators
        contradiction_words = ["contradiction", "contradictory", "oppose", "conflict"]
        contradiction_count = sum(
            1 for word in contradiction_words if word in text_lower
        )

        # Opposition/negation
        opposition_words = ["opposite", "opposed", "against", "negate", "negative"]
        opposition_count = sum(1 for word in opposition_words if word in text_lower)

        # Productive/developmental contradiction
        productive_words = ["drive", "motor", "engine", "propel", "force", "dynamic"]
        has_productive = sum(1 for word in productive_words if word in text_lower)

        # Resolution/sublation
        resolution_words = ["resolve", "overcome", "sublate", "aufheben", "synthesis"]
        has_resolution = sum(1 for word in resolution_words if word in text_lower)

        # Movement through contradiction
        movement_words = ["develop", "transform", "become", "change", "movement"]
        has_movement = sum(1 for word in movement_words if word in text_lower)

        # Error vs productive force
        error_words = ["error", "mistake", "wrong", "illogical", "invalid"]
        has_error = any(word in text_lower for word in error_words)

        total_contradiction = contradiction_count + opposition_count

        if total_contradiction >= 2 and has_productive >= 1:
            status = "Productive Contradiction"
            description = "Contradiction as engine of development and transformation"
            type_contra = "Dialectical motor"
        elif total_contradiction >= 2 and has_resolution >= 1:
            status = "Contradiction Resolving"
            description = "Contradiction moving toward sublation"
            type_contra = "Dynamic opposition"
        elif total_contradiction >= 2 and has_movement >= 1:
            status = "Contradiction in Movement"
            description = "Opposition driving change"
            type_contra = "Developmental"
        elif total_contradiction >= 1 and has_error:
            status = "Logical Error"
            description = "Contradiction seen as error, not productive force"
            type_contra = "Formal logic"
        elif opposition_count >= 1:
            status = "Opposition Present"
            description = "Opposition without full contradiction"
            type_contra = "Static opposition"
        else:
            status = "No Contradiction"
            description = "Contradiction not evident"
            type_contra = "None"

        return {
            "status": status,
            "description": description,
            "type": type_contra,
            "contradiction_count": total_contradiction,
            "productive": has_productive >= 1,
            "resolving": has_resolution >= 1,
            "drives_movement": has_movement >= 1,
            "principle": "Contradiction is the root of all movement and life - not error but productive force",
        }

    def _analyze_history(self, text: str) -> Dict[str, Any]:
        """
        Analyze history as Spirit's self-realization.

        History is the progressive realization of freedom. Each epoch is a stage
        in Spirit's coming to know itself. World history is world judgment.
        """
        text_lower = text.lower()

        # History/historical
        history_words = ["history", "historical", "past", "epoch", "age", "era"]
        history_count = sum(1 for word in history_words if word in text_lower)

        # Progress/development
        progress_words = ["progress", "develop", "advance", "evolve", "unfold"]
        has_progress = sum(1 for word in progress_words if word in text_lower)

        # Freedom indicators
        freedom_words = ["freedom", "free", "liberty", "autonomy", "self-determination"]
        freedom_count = sum(1 for word in freedom_words if word in text_lower)

        # Spirit in history
        spirit_history = [
            "world spirit",
            "spirit of the age",
            "zeitgeist",
            "historical spirit",
        ]
        has_spirit_history = any(phrase in text_lower for phrase in spirit_history)

        # Stages/epochs
        stages_words = ["stage", "phase", "epoch", "period", "moment"]
        sum(1 for word in stages_words if word in text_lower)

        # Rationality of history
        rational_words = ["reason", "rational", "necessity", "purpose", "end"]
        has_rational = sum(1 for word in rational_words if word in text_lower)

        # World history as world judgment
        judgment_words = ["judgment", "tribunal", "judge", "verdict"]
        any(word in text_lower for word in judgment_words)

        if history_count >= 2 and has_progress >= 1 and freedom_count >= 1:
            view = "History as Progress of Freedom"
            description = "History as Spirit's progressive realization of freedom"
            status = "Hegelian historical consciousness"
        elif history_count >= 2 and has_spirit_history:
            view = "Spirit in History"
            description = "Recognition of Spirit manifesting in historical epochs"
            status = "Philosophy of history"
        elif history_count >= 1 and has_progress >= 1:
            view = "Historical Progress"
            description = "Development through historical time"
            status = "Progressive"
        elif history_count >= 1:
            view = "Historical Awareness"
            description = "Awareness of historical dimension"
            status = "Historical"
        else:
            view = "Ahistorical"
            description = "No historical perspective"
            status = "Outside history"

        return {
            "view": view,
            "description": description,
            "status": status,
            "history_emphasis": history_count,
            "progressive": has_progress >= 1,
            "freedom_realization": freedom_count >= 1,
            "spirit_in_history": has_spirit_history,
            "rational_necessity": has_rational >= 2,
            "principle": "World history is the progress in the consciousness of freedom",
        }

    def _analyze_freedom(self, text: str) -> Dict[str, Any]:
        """
        Analyze freedom as Spirit's essence.

        Freedom is not arbitrary choice but rational self-determination.
        True freedom is realized in the rational state and ethical community.
        """
        text_lower = text.lower()

        # Freedom indicators
        freedom_words = ["freedom", "free", "liberty", "liberation"]
        freedom_count = sum(1 for word in freedom_words if word in text_lower)

        # Rational freedom
        rational_words = ["rational", "reason", "reasonable", "self-determined"]
        has_rational = sum(1 for word in rational_words if word in text_lower)

        # Arbitrary will vs rational will
        arbitrary_words = ["arbitrary", "random", "whim", "caprice", "whatever"]
        has_arbitrary = any(word in text_lower for word in arbitrary_words)

        # State/community
        state_words = ["state", "community", "society", "ethical life", "sittlichkeit"]
        has_state = any(phrase in state_words for phrase in state_words)

        # Self-determination
        self_det_words = ["self-determine", "self-govern", "autonomous", "self-rule"]
        has_self_determination = any(phrase in text_lower for phrase in self_det_words)

        # Recognition of necessity
        necessity_words = ["necessity", "necessary", "must", "rational necessity"]
        has_necessity = sum(1 for phrase in necessity_words if phrase in text_lower)

        # Realization/actualization
        realization_words = ["realize", "actualize", "manifest", "achieve"]
        any(word in text_lower for word in realization_words)

        if freedom_count >= 2 and has_rational >= 1 and has_state:
            conception = "Rational Freedom in State"
            description = (
                "Freedom as rational self-determination realized in ethical community"
            )
            type_freedom = "Concrete freedom (Sittlichkeit)"
        elif freedom_count >= 1 and has_rational >= 1:
            conception = "Rational Freedom"
            description = "Freedom as rational self-determination, not arbitrary choice"
            type_freedom = "Moral freedom (Moralität)"
        elif freedom_count >= 1 and has_self_determination:
            conception = "Self-Determination"
            description = "Freedom as autonomy and self-governance"
            type_freedom = "Abstract freedom"
        elif freedom_count >= 1 and has_arbitrary:
            conception = "Arbitrary Freedom"
            description = "Freedom misunderstood as arbitrary choice"
            type_freedom = "Abstract negative freedom"
        elif freedom_count >= 1:
            conception = "Freedom Mentioned"
            description = "Freedom present but conception unclear"
            type_freedom = "Indeterminate"
        else:
            conception = "No Freedom Concept"
            description = "Freedom not addressed"
            type_freedom = "Absent"

        return {
            "conception": conception,
            "description": description,
            "type": type_freedom,
            "freedom_emphasis": freedom_count,
            "rational": has_rational >= 1,
            "in_state": has_state,
            "self_determination": has_self_determination,
            "recognizes_necessity": has_necessity >= 1,
            "principle": "Freedom is the essence of Spirit - not arbitrary will but rational self-determination",
        }

    def _analyze_absolute(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Absolute.

        The Absolute is the whole, the truth. "The truth is the whole."
        The Absolute is not a static substance but subject, process, Spirit.
        """
        text_lower = text.lower()

        # Absolute indicators
        absolute_words = ["absolute", "unconditional", "infinite", "whole", "totality"]
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # The whole/totality
        whole_words = ["whole", "totality", "complete", "entire", "all"]
        whole_count = sum(1 for word in whole_words if word in text_lower)

        # Truth as whole
        truth_whole = ["truth is the whole", "truth as totality", "whole truth"]
        has_truth_whole = any(phrase in text_lower for phrase in truth_whole)

        # Process/development
        process_words = [
            "process",
            "development",
            "becoming",
            "movement",
            "self-development",
        ]
        has_process = sum(1 for word in process_words if word in text_lower)

        # Substance as subject
        substance_subject = [
            "substance is subject",
            "substance and subject",
            "living substance",
        ]
        has_substance_subject = any(
            phrase in text_lower for phrase in substance_subject
        )

        # System/systematic
        system_words = ["system", "systematic", "science", "encyclopedia"]
        has_system = sum(1 for word in system_words if word in text_lower)

        # Parts and whole
        parts_words = ["parts", "moments", "aspects", "elements"]
        has_parts = any(word in text_lower for word in parts_words)

        if absolute_count >= 2 and has_truth_whole:
            status = "Truth as the Whole"
            description = "The Absolute as systematic totality - truth is the whole"
            conception = "Hegelian Absolute"
        elif absolute_count >= 2 and has_process >= 1:
            status = "Absolute as Process"
            description = "The Absolute as self-developing process, not static being"
            conception = "Dynamic Absolute"
        elif whole_count >= 2 and has_parts:
            status = "Systematic Whole"
            description = "Conception of totality containing its parts/moments"
            conception = "Concrete totality"
        elif absolute_count >= 1:
            status = "Absolute Invoked"
            description = "Reference to the Absolute/Unconditioned"
            conception = "Abstract absolute"
        else:
            status = "No Absolute"
            description = "The Absolute not addressed"
            conception = "Finite perspective"

        return {
            "status": status,
            "description": description,
            "conception": conception,
            "absolute_emphasis": absolute_count,
            "whole_emphasis": whole_count,
            "truth_as_whole": has_truth_whole,
            "process": has_process >= 1,
            "substance_subject": has_substance_subject,
            "systematic": has_system >= 1,
            "principle": "The truth is the whole - the Absolute is living substance that is also subject",
        }

    def _analyze_recognition(self, text: str) -> Dict[str, Any]:
        """
        Analyze recognition (Anerkennung).

        Self-consciousness requires recognition from another self-consciousness.
        Mutual recognition constitutes ethical community (Sittlichkeit).
        """
        text_lower = text.lower()

        # Recognition indicators
        recognition_words = ["recognize", "recognition", "acknowledge", "anerkennung"]
        recognition_count = sum(1 for word in recognition_words if word in text_lower)

        # Mutual/reciprocal recognition
        mutual_words = ["mutual", "reciprocal", "each other", "one another", "both"]
        has_mutual = sum(1 for phrase in mutual_words if phrase in text_lower)

        # Self-consciousness through other
        through_other = [
            "through other",
            "by another",
            "from other",
            "other's recognition",
        ]
        has_through_other = any(phrase in text_lower for phrase in through_other)

        # Struggle for recognition
        struggle_words = ["struggle", "fight", "demand", "seek recognition"]
        has_struggle = any(phrase in text_lower for phrase in struggle_words)

        # Ethical community (recognition realized)
        community_words = ["community", "society", "ethical", "sittlichkeit", "we"]
        has_community = sum(1 for word in community_words if word in text_lower)

        # Self and other
        self_other = ["self", "other", "i and you", "subject"]
        sum(1 for phrase in self_other if phrase in text_lower)

        if recognition_count >= 2 and has_mutual >= 1 and has_community >= 1:
            status = "Mutual Recognition in Community"
            description = "Reciprocal recognition constituting ethical community"
            level = "Sittlichkeit (Ethical Life)"
        elif recognition_count >= 2 and has_mutual >= 1:
            status = "Mutual Recognition"
            description = "Reciprocal acknowledgment between self-consciousnesses"
            level = "Intersubjectivity"
        elif recognition_count >= 1 and has_struggle:
            status = "Struggle for Recognition"
            description = "Seeking recognition from another consciousness"
            level = "Pre-mutual recognition"
        elif recognition_count >= 1:
            status = "Recognition Sought"
            description = "Awareness of need for recognition"
            level = "Self-consciousness emerging"
        else:
            status = "No Recognition"
            description = "Recognition not addressed"
            level = "Pre-recognition"

        return {
            "status": status,
            "description": description,
            "level": level,
            "recognition_emphasis": recognition_count,
            "mutual": has_mutual >= 1,
            "through_other": has_through_other,
            "struggle": has_struggle,
            "ethical_community": has_community >= 1,
            "principle": "Self-consciousness achieves reality only through recognition from another self-consciousness",
        }

    def _apply_hegel_to_problem(self, text: str) -> str:
        """Apply Hegelian philosophical concepts to the specific domain of the text."""
        t = text.lower()
        if any(
            w in t
            for w in [
                "conflict",
                "contradict",
                "oppose",
                "tension",
                "disagree",
                "struggle",
                "clash",
                "paradox",
            ]
        ):
            return (
                "Hegel's dialectic reveals that contradiction is not an obstacle to thought but its"
                " very engine. Every determinate position — the thesis — generates its own negation"
                " — the antithesis — not as an external attack but as a logical consequence of its"
                " own one-sidedness. The Aufhebung, Hegel's untranslatable term, simultaneously"
                " cancels, preserves, and elevates the opposed moments into a richer synthesis that"
                " contains both as subordinate aspects. Far from being a defect, contradiction is"
                " what makes reality dynamic and historical rather than static. Understanding the"
                " present conflict through this dialectical lens reveals it as a necessary moment in"
                " a larger movement toward more adequate self-comprehension by Spirit."
            )
        elif any(
            w in t
            for w in [
                "free",
                "freedom",
                "society",
                "state",
                "community",
                "institution",
                "politic",
                "right",
            ]
        ):
            return (
                "For Hegel, freedom is not the negative liberty of the isolated individual but the"
                " positive self-realization of Geist (Spirit) through the concrete institutions of"
                " Sittlichkeit — ethical life. The family, civil society, and the state are not"
                " external constraints on freedom but the very medium through which rational"
                " self-determination becomes actual. Abstract freedom — mere freedom from — remains"
                " empty without the concrete social relations that give it content. World history,"
                " on Hegel's account, is nothing other than the progress in the consciousness of"
                " freedom: the gradual actualization of Geist's self-knowledge through successive"
                " historical formations. True freedom is found not by escaping society but by"
                " recognizing oneself in its rational structures."
            )
        elif any(
            w in t
            for w in [
                "self",
                "identity",
                "consciousness",
                "recogni",
                "other",
                "subject",
                "person",
                "ego",
            ]
        ):
            return (
                "The master-slave dialectic in the Phenomenology of Spirit shows that"
                " self-consciousness can achieve reality only through recognition by another"
                " self-consciousness. The struggle for recognition — each consciousness risking"
                " life to be acknowledged — produces the asymmetric master-slave relationship, but"
                " this proves self-undermining: the master's recognition comes from a dependent"
                " slave whose acknowledgement carries no worth, while the slave, through labor and"
                " the discipline of forming the world, develops genuine self-consciousness. Identity"
                " is therefore irreducibly relational — what one is, one is only through being"
                " recognized by others. This logic of Anerkennung (recognition) runs through all"
                " social, political, and spiritual life."
            )
        elif any(
            w in t
            for w in [
                "histor",
                "progress",
                "develop",
                "change",
                "time",
                "epoch",
                "era",
                "civiliz",
                "culture",
            ]
        ):
            return (
                "Hegel conceives world history as the autobiography of Geist — the progressive"
                " self-realization of Spirit through the successive shapes of culture, religion, and"
                " political life. Each historical epoch is a determinate expression of Spirit's"
                " self-understanding, containing within itself the contradictions that will propel"
                " it toward its successor. The Weltgeist (World Spirit) actualizes itself through"
                " world-historical individuals — figures like Napoleon whom Hegel called 'the World"
                " Spirit on horseback' — who unwittingly serve the purposes of Reason. History is"
                " therefore not a random sequence of events but the rational development of freedom:"
                " 'The real is rational and the rational is real', understood dynamically and"
                " historically rather than as a static endorsement of the status quo."
            )
        elif any(
            w in t
            for w in [
                "know",
                "knowledge",
                "truth",
                "science",
                "reason",
                "absolute",
                "understand",
                "certain",
                "logic",
            ]
        ):
            return (
                "For Hegel, the Absolute — the ultimate truth of all reality — is not a static"
                " substance but a dynamic Subject that knows itself through the finite minds of"
                " human beings. As the Phenomenology's preface declares, 'The truth is the whole':"
                " any partial perspective is partially false, gaining its truth only within the"
                " larger totality. The Science of Logic traces the self-development of pure thought"
                " from Being through Nothing to Becoming, demonstrating that the categories of"
                " thought and the structures of reality are ultimately identical. Genuine knowledge"
                " is not the correspondence of an isolated mind to an external world but the"
                " self-articulation of Spirit through the dialectical movement of concept."
            )
        else:
            return (
                "Hegel's absolute idealism interprets all of reality as the self-development of"
                " Geist (Spirit/Mind) through a dialectical process of thesis, antithesis, and"
                " Aufhebung (cancellation-preservation-elevation). The Phenomenology of Spirit"
                " traces consciousness's journey from simple sense-certainty through"
                " self-consciousness, reason, and Spirit to Absolute Knowing, each stage revealing"
                " the inadequacy of the previous and generating its successor. Recognition"
                " (Anerkennung) is the key social-ontological category: self-consciousness is"
                " always already intersubjective, constituted through its relation to the Other."
                " The whole of reality — nature, history, art, religion, and philosophy — forms a"
                " single rational totality in which the Absolute comes to know itself."
            )

    def _construct_reasoning(
        self,
        prompt: str,
        dialectic: Dict[str, Any],
        geist: Dict[str, Any],
        phenomenology: Dict[str, Any],
        master_slave: Dict[str, Any],
        contradiction: Dict[str, Any],
        history: Dict[str, Any],
        freedom: Dict[str, Any],
        absolute: Dict[str, Any],
    ) -> str:
        """Construct comprehensive Hegelian philosophical reasoning."""
        applied = self._apply_hegel_to_problem(prompt)
        reasoning = (
            f"{applied}\n\n"
            "From Hegel's absolute idealist perspective, we must examine this text dialectically "
            "as a moment in Spirit's self-realization. "
        )

        # Dialectical movement
        reasoning += (
            f"Dialectical movement: {dialectic['stage']} - {dialectic['description']}. "
        )

        # Geist/Spirit
        reasoning += f"Geist: {geist['status']} - {geist['description']}. "

        # Phenomenological stage
        if phenomenology["current_stage"] != "Undetermined":
            reasoning += (
                f"Phenomenological stage: {phenomenology['current_stage']} - "
                f"{phenomenology['description']}. "
            )

        # Master-slave dialectic
        if master_slave["position"] != "No Master-Slave Dialectic":
            reasoning += f"Recognition: {master_slave['description']}. "

        # Contradiction as productive
        if contradiction["status"] != "No Contradiction":
            reasoning += f"Contradiction: {contradiction['description']}. "

        # Historical dimension
        reasoning += f"Historical view: {history['view']} - {history['description']}. "

        # Freedom
        reasoning += f"Freedom: {freedom['conception']} - {freedom['description']}. "

        # The Absolute
        reasoning += f"The Absolute: {absolute['status']}. "

        # Concluding Hegelian wisdom
        reasoning += (
            "Remember: The truth is the whole. The real is rational and the rational is real. "
            "Spirit develops through contradiction toward absolute self-knowledge. "
            "World history is the progress in the consciousness of freedom."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Hegelian analysis.

        For Hegel, tension/contradiction is productive, not negative.
        However, tensions arise from:
        - Arrested dialectical movement (no synthesis)
        - Abstract rather than concrete universals
        - Denial of contradiction's productivity
        - Ahistorical thinking
        - Misunderstanding freedom as arbitrary choice
        """
        tension_score = 0
        tension_elements = []

        # Check dialectical movement
        dialectic_stage = analysis["dialectic"]["stage"]
        if dialectic_stage == "Pre-dialectical":
            tension_score += 2
            tension_elements.append("No dialectical development - static thinking")
        elif dialectic_stage == "Thesis/Immediacy":
            tension_score += 1
            tension_elements.append("Abstract immediacy - not yet mediated")

        # Check for arrested development (thesis-antithesis without synthesis)
        if (
            dialectic_stage == "Thesis-Antithesis"
            and not analysis["dialectic"]["aufhebung"]
        ):
            tension_score += 1
            tension_elements.append("Dialectical opposition without sublation")

        # Check concrete vs abstract universal
        concept_type = analysis["concrete_universal"]["concept_type"]
        if concept_type == "Abstract Universal":
            tension_score += 2
            tension_elements.append("Abstract universal separated from particulars")
        elif concept_type == "Mere Particularity":
            tension_score += 1
            tension_elements.append("Empirical particulars without universal")

        # Check contradiction understanding
        if analysis["contradiction"]["type"] == "Formal logic":
            tension_score += 2
            tension_elements.append("Contradiction seen as error, not productive force")

        # Check historical consciousness
        if analysis["history"]["status"] == "Ahistorical":
            tension_score += 2
            tension_elements.append(
                "Ahistorical thinking - outside Spirit's development"
            )

        # Check freedom conception
        freedom_type = analysis["freedom"]["type"]
        if freedom_type == "Abstract negative freedom":
            tension_score += 1
            tension_elements.append(
                "Freedom as arbitrary choice, not rational self-determination"
            )

        # Check phenomenological development
        if analysis["phenomenology"]["status"] == "Early":
            tension_score += 1
            tension_elements.append(
                "Early stage of consciousness - not yet self-conscious"
            )

        # Check recognition
        if analysis["recognition"]["level"] == "Pre-recognition":
            tension_score += 1
            tension_elements.append("Lack of intersubjective recognition")

        # Determine tension level (note: some tension is productive in Hegel)
        if tension_score >= 8:
            level = "Very High"
            description = "Severe undialectical thinking - abstract, ahistorical, denies contradiction"
        elif tension_score >= 6:
            level = "High"
            description = (
                "Significant tensions - arrested development, abstract universals"
            )
        elif tension_score >= 4:
            level = "Moderate"
            description = "Some tensions in dialectical development"
        elif tension_score >= 2:
            level = "Low"
            description = "Minor tensions - productive contradictions present"
        else:
            level = "Very Low"
            description = (
                "Well-aligned with dialectical movement and Spirit's self-realization"
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements
                if tension_elements
                else ["No significant tensions - productive contradiction at work"]
            ),
        }
