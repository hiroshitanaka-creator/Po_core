"""
Derrida - Deconstructionist Philosopher

Jacques Derrida (1930-2004)
Focus: Deconstruction, Différance, Trace, Binary Opposition

Key Concepts:
- Deconstruction: Revealing hidden assumptions and contradictions
- Différance: Difference + deferral of meaning (with an 'a')
- Trace: The absent presence, what is excluded to define something
- Binary Opposition: Hierarchical oppositions (speech/writing, presence/absence)
- Logocentrism: Critique of the privilege of presence and voice
- Phonocentrism: Privilege of speech over writing
- Supplement: What is added also reveals a lack
- Arche-writing: Writing as condition of all signification
- Dissemination: Proliferation and scattering of meaning
- Pharmakon: Undecidable - both poison and cure
- Hospitality: Unconditional welcome vs conditional hospitality
- Hauntology: Being haunted by absent presences
- Iterability: Repeatability that introduces difference
- Aporia: Impasses, undecidable moments
- Gift: The impossibility of the pure gift
- Justice: Justice vs Law (law is deconstructible, justice is not)
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Derrida(Philosopher):
    """
    Derrida's deconstructionist perspective.

    Analyzes prompts by revealing hidden assumptions, binary oppositions,
    the play of différance (difference and deferral), and undecidables.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Jacques Derrida",
            description="Deconstructionist focusing on différance, trace, supplementarity, and the instability of meaning",
        )
        self.tradition = "Deconstruction / Post-Structuralism"
        self.key_concepts = [
            "differance",
            "trace",
            "deconstruction",
            "supplementarity",
            "logocentrism",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Derrida's deconstructionist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Derrida's deconstructive analysis
        """
        # Perform comprehensive deconstructive analysis
        analysis = self._deconstruct(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Deconstructionist",
            "tension": tension,
            "binary_oppositions": analysis["binaries"],
            "traces": analysis["traces"],
            "differance": analysis["differance"],
            "contradictions": analysis["contradictions"],
            "what_is_excluded": analysis["excluded"],
            "supplement": analysis["supplement"],
            "logocentrism": analysis["logocentrism"],
            "dissemination": analysis["dissemination"],
            "undecidables": analysis["undecidables"],
            "hospitality": analysis["hospitality"],
            "hauntology": analysis["hauntology"],
            "iterability": analysis["iterability"],
            "aporia": analysis["aporia"],
            "gift": analysis["gift"],
            "justice": analysis["justice"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Deconstruction",
                "focus": "Différance, trace, binary oppositions, and the undecidable",
            },
        }

    def _deconstruct(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Derridean deconstruction.

        Args:
            prompt: The text to deconstruct

        Returns:
            Deconstruction results
        """
        # Identify binary oppositions
        binaries = self._find_binary_oppositions(prompt)

        # Identify traces (what is absent but implied)
        traces = self._find_traces(prompt)

        # Analyze différance (deferred/different meanings)
        differance = self._analyze_differance(prompt)

        # Find contradictions and tensions
        contradictions = self._find_contradictions(prompt)

        # What is excluded to create this meaning?
        excluded = self._find_excluded(prompt, binaries)

        # Analyze supplement
        supplement = self._analyze_supplement(prompt)

        # Check for logocentrism
        logocentrism = self._assess_logocentrism(prompt)

        # Analyze dissemination
        dissemination = self._analyze_dissemination(prompt)

        # Identify undecidables
        undecidables = self._identify_undecidables(prompt)

        # Analyze hospitality
        hospitality = self._analyze_hospitality(prompt)

        # Analyze hauntology
        hauntology = self._analyze_hauntology(prompt)

        # Assess iterability
        iterability = self._assess_iterability(prompt)

        # Identify aporia
        aporia = self._identify_aporia(prompt)

        # Analyze gift
        gift = self._analyze_gift(prompt)

        # Analyze justice
        justice = self._analyze_justice(prompt)

        # Construct deconstructive reasoning
        reasoning = self._construct_reasoning(
            prompt,
            binaries,
            traces,
            differance,
            contradictions,
            supplement,
            logocentrism,
            undecidables,
            aporia,
        )

        return {
            "reasoning": reasoning,
            "binaries": binaries,
            "traces": traces,
            "differance": differance,
            "contradictions": contradictions,
            "excluded": excluded,
            "supplement": supplement,
            "logocentrism": logocentrism,
            "dissemination": dissemination,
            "undecidables": undecidables,
            "hospitality": hospitality,
            "hauntology": hauntology,
            "iterability": iterability,
            "aporia": aporia,
            "gift": gift,
            "justice": justice,
        }

    def _find_binary_oppositions(self, text: str) -> List[Dict[str, Any]]:
        """
        Find binary oppositions in the text.

        Binary oppositions are hierarchical - one term is privileged over the other.
        Deconstruction reverses and displaces these hierarchies.
        """
        binaries = []
        text_lower = text.lower()

        # Common binary pairs with their typical hierarchy
        binary_pairs = [
            ("presence", "absence", "Presence is privileged in Western metaphysics"),
            ("speech", "writing", "Speech is seen as immediate, writing as derivative"),
            ("inside", "outside", "Interiority privileged over exteriority"),
            ("self", "other", "Self-identity privileged over alterity"),
            ("mind", "body", "Mind/soul privileged over corporeal"),
            ("nature", "culture", "The 'natural' seen as prior to cultural"),
            ("original", "copy", "Origin privileged over reproduction"),
            ("literal", "metaphorical", "Literal meaning seen as primary"),
            ("central", "marginal", "Center privileged over periphery"),
            ("meaning", "form", "Content privileged over style"),
            ("essence", "accident", "Essential properties over contingent"),
            ("identity", "difference", "Sameness over otherness"),
            ("reality", "appearance", "Reality behind appearances"),
            ("truth", "fiction", "Truth privileged over fiction"),
            ("reason", "emotion", "Reason privileged over passion"),
            ("man", "woman", "Masculine as universal"),
            ("good", "evil", "Good as primary, evil as privation"),
            ("life", "death", "Life as positive, death as negation"),
            ("order", "chaos", "Order as primary state"),
            ("whole", "part", "Totality over fragment"),
        ]

        for term1, term2, note in binary_pairs:
            found_first = term1 in text_lower
            found_second = term2 in text_lower

            if found_first and found_second:
                binaries.append(
                    {
                        "opposition": f"{term1} / {term2}",
                        "both_present": True,
                        "privileged_term": term1,
                        "suppressed_term": term2,
                        "note": note,
                        "deconstructive_move": f"Show how '{term2}' is constitutive of '{term1}'",
                    }
                )
            elif found_first:
                binaries.append(
                    {
                        "opposition": f"{term1} / [{term2}]",
                        "both_present": False,
                        "privileged_term": term1,
                        "suppressed_term": term2,
                        "note": f"'{term2}' is the absent trace that constitutes '{term1}'",
                        "deconstructive_move": f"Reveal the hidden dependence on '{term2}'",
                    }
                )
            elif found_second:
                binaries.append(
                    {
                        "opposition": f"[{term1}] / {term2}",
                        "both_present": False,
                        "privileged_term": term1,
                        "suppressed_term": term2,
                        "note": f"The 'inferior' term '{term2}' is present without its 'superior'",
                        "deconstructive_move": f"Question the assumed priority of '{term1}'",
                    }
                )

        # If no binaries found, indicate the fundamental opposition
        if not binaries:
            binaries.append(
                {
                    "opposition": "meaning / [non-meaning]",
                    "both_present": False,
                    "privileged_term": "meaning",
                    "suppressed_term": "non-meaning",
                    "note": "Every text presupposes an opposition to what it excludes",
                    "deconstructive_move": "Reveal how meaning depends on what it excludes",
                }
            )

        return binaries

    def _find_traces(self, text: str) -> List[Dict[str, str]]:
        """
        Identify traces - what is absent but shapes the present.

        The trace is neither present nor absent but the condition of both.
        """
        traces = []
        text_lower = text.lower()

        # Negation traces (what is negated haunts)
        negation_words = ["not", "no", "never", "nothing", "without", "lack", "absence"]
        for word in negation_words:
            if word in text_lower:
                traces.append(
                    {
                        "type": "Negation Trace",
                        "description": f"Negation ('{word}') reveals the trace of what is denied",
                        "implication": "The absent (what is negated) haunts the present",
                    }
                )
                break

        # Comparison traces (what is compared reveals the other)
        comparison_words = ["than", "rather", "instead", "unlike", "different from"]
        for phrase in comparison_words:
            if phrase in text_lower:
                traces.append(
                    {
                        "type": "Comparative Trace",
                        "description": f"Comparison ('{phrase}') reveals dependence on an other",
                        "implication": "Identity constituted through difference",
                    }
                )
                break

        # Temporal traces (past in present)
        temporal_words = ["memory", "remember", "history", "origin", "before"]
        for word in temporal_words:
            if word in text_lower:
                traces.append(
                    {
                        "type": "Temporal Trace",
                        "description": f"Temporal reference ('{word}') inscribes the past in the present",
                        "implication": "The present is never purely present - always inscribed by past",
                    }
                )
                break

        # Future traces (anticipation in present)
        future_words = ["promise", "expect", "anticipate", "future", "will"]
        for word in future_words:
            if word in text_lower:
                traces.append(
                    {
                        "type": "Futural Trace",
                        "description": f"Futural reference ('{word}') opens present to what is not yet",
                        "implication": "The present is structured by the to-come (à-venir)",
                    }
                )
                break

        # Reference traces (referring implies absence)
        if any(
            word in text_lower
            for word in ["refer", "represent", "signify", "mean", "indicate"]
        ):
            traces.append(
                {
                    "type": "Referential Trace",
                    "description": "Reference implies the absence of what is referred to",
                    "implication": "The sign is always the sign of an absence",
                }
            )

        if not traces:
            traces.append(
                {
                    "type": "Implicit Trace",
                    "description": "Every text is woven of traces it cannot contain",
                    "implication": "The trace of what is unspoken shapes what appears",
                }
            )

        return traces

    def _analyze_differance(self, text: str) -> Dict[str, Any]:
        """
        Analyze différance - the play of difference and deferral.

        Différance (with an 'a') = difference + deferral
        Neither a word nor a concept - it is the condition of both.
        Meaning is never fully present, always deferred.
        """
        text_lower = text.lower()

        # Temporal deferral indicators
        deferral_words = [
            "will",
            "future",
            "later",
            "eventually",
            "become",
            "promise",
            "waiting",
            "postpone",
            "delay",
            "soon",
            "someday",
        ]
        deferral_count = sum(1 for word in deferral_words if word in text_lower)

        # Spatial/relational difference indicators
        difference_words = [
            "different",
            "other",
            "contrast",
            "versus",
            "but",
            "however",
            "distinguish",
            "separate",
            "apart",
            "between",
        ]
        difference_count = sum(1 for word in difference_words if word in text_lower)

        # Self-reference indicators (meaning referring to other meanings)
        self_ref_words = [
            "means",
            "refers",
            "signifies",
            "represents",
            "indicates",
            "implies",
        ]
        self_ref_count = sum(1 for word in self_ref_words if word in text_lower)

        # Presence/immediacy claims
        presence_words = ["is", "present", "now", "immediate", "direct", "pure"]
        presence_count = sum(1 for word in presence_words if word in text_lower)

        # Calculate différance status
        differance_score = deferral_count + difference_count + self_ref_count

        if differance_score >= 4:
            status = "High Différance"
            description = "Meaning is highly deferred - multiple differences and deferrals at play"
        elif deferral_count >= 2 and difference_count >= 2:
            status = "Full Différance"
            description = "Both temporal deferral and spatial difference operate"
        elif deferral_count >= 2:
            status = "Temporal Deferral"
            description = "Meaning is postponed to the future - never fully present"
        elif difference_count >= 2:
            status = "Spatial Difference"
            description = (
                "Meaning constituted through differences - never self-identical"
            )
        elif self_ref_count >= 2:
            status = "Referential Deferral"
            description = (
                "Meaning refers to other meanings - infinite deferral of the signified"
            )
        else:
            status = "Implicit Différance"
            description = "Différance operates even where not explicitly marked"

        # Note on presence claims
        presence_note = ""
        if presence_count >= 2:
            presence_note = "Presence claims may mask the operation of différance"

        return {
            "status": status,
            "description": description,
            "temporal_deferral": deferral_count,
            "spatial_difference": difference_count,
            "referential_movement": self_ref_count,
            "presence_claims": presence_count,
            "presence_note": presence_note,
            "differance_score": differance_score,
            "principle": "Différance: The play of difference and deferral that makes meaning possible and impossible",
        }

    def _find_contradictions(self, text: str) -> List[Dict[str, str]]:
        """Find internal contradictions or tensions that destabilize the text."""
        contradictions = []
        text_lower = text.lower()

        # Explicit contradictions
        if "but" in text_lower or "however" in text_lower or "yet" in text_lower:
            contradictions.append(
                {
                    "type": "Explicit Tension",
                    "description": "Conjunction signals internal contradiction",
                    "effect": "The text undermines its own assertions",
                }
            )

        # Simultaneous affirmation and negation
        if "not" in text_lower and any(
            word in text_lower for word in ["is", "are", "be"]
        ):
            contradictions.append(
                {
                    "type": "Affirmation-Negation",
                    "description": "Simultaneous assertion and denial",
                    "effect": "Presence and absence coexist, destabilizing identity",
                }
            )

        # Paradoxes
        paradox_pairs = [
            ("true", "false"),
            ("real", "unreal"),
            ("same", "different"),
            ("inside", "outside"),
        ]
        for term1, term2 in paradox_pairs:
            if term1 in text_lower and term2 in text_lower:
                contradictions.append(
                    {
                        "type": "Paradox",
                        "description": f"'{term1}' and '{term2}' coexist",
                        "effect": "Binary opposition collapses",
                    }
                )

        # Self-reference paradox
        if any(phrase in text_lower for phrase in ["this statement", "i am", "we are"]):
            contradictions.append(
                {
                    "type": "Self-Reference",
                    "description": "Self-referential structure",
                    "effect": "The text cannot step outside itself to verify itself",
                }
            )

        # Performative contradiction
        if any(
            phrase in text_lower
            for phrase in ["there is no", "nothing is", "we cannot"]
        ):
            contradictions.append(
                {
                    "type": "Performative Contradiction",
                    "description": "The statement may contradict its own performance",
                    "effect": "Saying 'there is no X' invokes X",
                }
            )

        if not contradictions:
            contradictions.append(
                {
                    "type": "Latent Contradiction",
                    "description": "All texts contain suppressed tensions",
                    "effect": "The apparent coherence conceals deeper instability",
                }
            )

        return contradictions

    def _find_excluded(
        self, text: str, binaries: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """What is excluded to create this meaning?"""
        excluded = []

        # Extract excluded terms from binaries
        for binary in binaries:
            if not binary.get("both_present", True):
                suppressed = binary.get("suppressed_term", "")
                if suppressed:
                    excluded.append(
                        {
                            "term": suppressed,
                            "description": f"'{suppressed}' is excluded to privilege its opposite",
                            "deconstructive_insight": f"The excluded '{suppressed}' is constitutive of the text",
                        }
                    )

        # General exclusions based on content
        text_lower = text.lower()

        if "meaning" in text_lower:
            excluded.append(
                {
                    "term": "nonsense/ambiguity",
                    "description": "Nonsense and ambiguity are excluded to create 'meaning'",
                    "deconstructive_insight": "Meaning requires but suppresses its other",
                }
            )

        if "truth" in text_lower:
            excluded.append(
                {
                    "term": "error/fiction",
                    "description": "Falsehood and fiction are excluded to claim 'truth'",
                    "deconstructive_insight": "Truth is produced through exclusion",
                }
            )

        if "identity" in text_lower or "self" in text_lower:
            excluded.append(
                {
                    "term": "difference/other",
                    "description": "Difference and otherness are excluded to maintain identity",
                    "deconstructive_insight": "Identity depends on what it excludes",
                }
            )

        if not excluded:
            excluded.append(
                {
                    "term": "the undecidable",
                    "description": "What cannot be captured by binary logic is excluded",
                    "deconstructive_insight": "The undecidable haunts every decision",
                }
            )

        return excluded

    def _analyze_supplement(self, text: str) -> Dict[str, Any]:
        """
        Analyze the logic of the supplement.

        The supplement is added to something complete, yet reveals a lack.
        It is both addition and substitution.
        """
        text_lower = text.lower()

        # Supplement indicators
        addition_words = [
            "also",
            "addition",
            "extra",
            "supplement",
            "more",
            "further",
            "moreover",
            "besides",
            "add",
            "include",
        ]
        addition_count = sum(1 for word in addition_words if word in text_lower)

        # Substitution indicators
        substitution_words = [
            "instead",
            "replace",
            "substitute",
            "rather",
            "alternative",
        ]
        substitution_count = sum(1 for word in substitution_words if word in text_lower)

        # Completion/lack indicators
        completion_words = ["complete", "full", "whole", "total", "enough"]
        completion_count = sum(1 for word in completion_words if word in text_lower)

        lack_words = ["lack", "missing", "need", "require", "incomplete", "partial"]
        lack_count = sum(1 for word in lack_words if word in text_lower)

        if addition_count >= 1 and (completion_count >= 1 or lack_count >= 1):
            status = "Supplement Logic Active"
            description = (
                "Addition reveals lack - what is 'complete' requires supplementation"
            )
            paradox = True
        elif addition_count >= 2:
            status = "Supplementation Present"
            description = "Multiple additions suggest original insufficiency"
            paradox = True
        elif substitution_count >= 1:
            status = "Substitutive Supplement"
            description = "Substitution reveals the lack it fills"
            paradox = True
        elif completion_count >= 1:
            status = "Claimed Completeness"
            description = "Claims of completeness may mask supplementary structure"
            paradox = False
        else:
            status = "Implicit Supplementation"
            description = "All texts are supplementary - adding to what they interpret"
            paradox = False

        return {
            "status": status,
            "description": description,
            "paradox_active": paradox,
            "addition_count": addition_count,
            "substitution_count": substitution_count,
            "completion_count": completion_count,
            "lack_count": lack_count,
            "principle": "The supplement: what is added to a 'complete' thing reveals its incompleteness",
        }

    def _assess_logocentrism(self, text: str) -> Dict[str, Any]:
        """
        Assess logocentrism - the privilege of presence, voice, and logos.

        Logocentrism = phonocentrism (privilege of speech) + metaphysics of presence
        """
        text_lower = text.lower()

        # Presence indicators
        presence_words = ["present", "presence", "immediate", "direct", "now", "here"]
        presence_count = sum(1 for word in presence_words if word in text_lower)

        # Voice/speech indicators
        speech_words = ["say", "speak", "voice", "word", "oral", "verbal", "heard"]
        speech_count = sum(1 for word in speech_words if word in text_lower)

        # Logos/reason indicators
        logos_words = ["reason", "rational", "logic", "truth", "meaning", "essence"]
        logos_count = sum(1 for word in logos_words if word in text_lower)

        # Writing indicators (the suppressed term)
        writing_words = ["writing", "written", "text", "inscription", "trace"]
        writing_count = sum(1 for word in writing_words if word in text_lower)

        # Calculate logocentric tendency
        logo_score = presence_count + speech_count + logos_count

        if logo_score >= 5:
            status = "Strongly Logocentric"
            description = "Heavy reliance on presence, voice, and logos"
            critique = (
                "Deconstruction reveals the repressed role of writing and absence"
            )
        elif logo_score >= 3:
            status = "Moderately Logocentric"
            description = "Some appeal to presence and immediate meaning"
            critique = "Question the assumed priority of presence over absence"
        elif writing_count > logo_score:
            status = "Writing-Aware"
            description = "Acknowledges the textual, written dimension"
            critique = "May still harbor logocentric assumptions"
        else:
            status = "Implicitly Logocentric"
            description = "Western metaphysics is inherently logocentric"
            critique = "All texts operate within logocentric tradition"

        return {
            "status": status,
            "description": description,
            "critique": critique,
            "presence_score": presence_count,
            "speech_score": speech_count,
            "logos_score": logos_count,
            "writing_score": writing_count,
            "total_logocentric": logo_score,
            "principle": "Logocentrism: The metaphysical privilege of presence, voice, and reason",
        }

    def _analyze_dissemination(self, text: str) -> Dict[str, Any]:
        """
        Analyze dissemination - the scattering and proliferation of meaning.

        Meaning is not contained but disseminated - scattered like seeds.
        No final gathering (logos) can collect all meanings.
        """
        text_lower = text.lower()

        # Proliferation indicators
        prolif_words = [
            "many",
            "multiple",
            "various",
            "different",
            "several",
            "diverse",
        ]
        prolif_count = sum(1 for word in prolif_words if word in text_lower)

        # Scattering indicators
        scatter_words = ["spread", "scatter", "disperse", "distribute", "diffuse"]
        scatter_count = sum(1 for word in scatter_words if word in text_lower)

        # Gathering/unity indicators (opposite of dissemination)
        gather_words = [
            "gather",
            "collect",
            "unite",
            "single",
            "one",
            "unified",
            "total",
        ]
        gather_count = sum(1 for word in gather_words if word in text_lower)

        # Ambiguity/polysemy indicators
        ambig_words = ["ambiguous", "multiple meanings", "interpret", "reading"]
        ambig_count = sum(1 for word in ambig_words if word in text_lower)

        dissemination_score = prolif_count + scatter_count + ambig_count

        if dissemination_score >= 4:
            status = "High Dissemination"
            description = "Meaning proliferates without final gathering"
        elif dissemination_score >= 2:
            status = "Active Dissemination"
            description = "Multiple meanings resist unification"
        elif gather_count > dissemination_score:
            status = "Attempted Gathering"
            description = "Text attempts to gather meaning, but dissemination persists"
        else:
            status = "Implicit Dissemination"
            description = "All texts disseminate beyond authorial intention"

        return {
            "status": status,
            "description": description,
            "proliferation_score": prolif_count,
            "scattering_score": scatter_count,
            "gathering_score": gather_count,
            "ambiguity_score": ambig_count,
            "dissemination_total": dissemination_score,
            "principle": "Dissemination: Meaning scatters without final gathering",
        }

    def _identify_undecidables(self, text: str) -> List[Dict[str, str]]:
        """
        Identify undecidables - terms that belong to neither/both sides of a binary.

        Undecidables: pharmakon, hymen, supplement, différance, trace, etc.
        """
        undecidables = []
        text_lower = text.lower()

        # Check for classic undecidables
        undecidable_terms = {
            "pharmakon": ("poison/cure", "Both remedy and poison - undecidable"),
            "gift": (
                "gift/poison",
                "The pure gift is impossible - it always creates debt",
            ),
            "hymen": (
                "inside/outside",
                "Neither inside nor outside, both barrier and passage",
            ),
            "supplement": ("addition/substitution", "Both adding to and replacing"),
            "border": ("inside/outside", "The border belongs to neither side"),
            "margin": ("center/margin", "The margin is necessary for the center"),
            "translation": ("same/different", "Neither identical nor different"),
            "promise": ("present/future", "Present commitment to absent future"),
        }

        for term, (opposition, description) in undecidable_terms.items():
            if term in text_lower:
                undecidables.append(
                    {
                        "term": term,
                        "opposition_destabilized": opposition,
                        "description": description,
                        "effect": f"'{term}' cannot be assigned to either side of the binary",
                    }
                )

        # Check for structural undecidability
        if any(
            phrase in text_lower
            for phrase in ["both", "neither", "and yet", "at the same time"]
        ):
            undecidables.append(
                {
                    "term": "[structural undecidable]",
                    "opposition_destabilized": "general",
                    "description": "The text indicates something that belongs to both/neither",
                    "effect": "Binary logic is insufficient",
                }
            )

        if not undecidables:
            undecidables.append(
                {
                    "term": "[implicit undecidable]",
                    "opposition_destabilized": "meaning/non-meaning",
                    "description": "Every text contains moments of undecidability",
                    "effect": "Final decision is always deferred",
                }
            )

        return undecidables

    def _analyze_hospitality(self, text: str) -> Dict[str, Any]:
        """
        Analyze hospitality - the impossible demand of unconditional welcome.

        Unconditional hospitality: welcome without conditions
        Conditional hospitality: requires identification, limits
        The aporia: hospitality requires both and they contradict
        """
        text_lower = text.lower()

        # Hospitality indicators
        welcome_words = ["welcome", "invite", "receive", "guest", "host", "open door"]
        welcome_count = sum(1 for phrase in welcome_words if phrase in text_lower)

        # Condition indicators
        condition_words = ["condition", "require", "must", "if", "only if", "provided"]
        condition_count = sum(1 for word in condition_words if word in text_lower)

        # Exclusion indicators
        exclusion_words = ["exclude", "deny", "refuse", "reject", "limit", "border"]
        exclusion_count = sum(1 for word in exclusion_words if word in text_lower)

        # Stranger/other indicators
        other_words = ["stranger", "foreigner", "other", "alien", "outsider"]
        other_count = sum(1 for word in other_words if word in text_lower)

        if welcome_count >= 1 and condition_count >= 1:
            status = "Aporia of Hospitality"
            description = (
                "The tension between unconditional welcome and necessary conditions"
            )
            mode = "Aporetic"
        elif welcome_count >= 2:
            status = "Hospitality Invoked"
            description = "Welcome or openness is a concern"
            mode = "Hospitable"
        elif exclusion_count >= 1:
            status = "Hostility/Exclusion"
            description = "Exclusion operates - the limit of hospitality"
            mode = "Hostile"
        elif other_count >= 1:
            status = "Question of the Other"
            description = "The other is present - hospitality may be at stake"
            mode = "Potential"
        else:
            status = "Not Explicitly Present"
            description = "Hospitality not directly addressed"
            mode = "Implicit"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "welcome_score": welcome_count,
            "condition_score": condition_count,
            "exclusion_score": exclusion_count,
            "other_score": other_count,
            "principle": "Hospitality: The impossible demand of unconditional welcome",
        }

    def _analyze_hauntology(self, text: str) -> Dict[str, Any]:
        """
        Analyze hauntology - being haunted by absent presences.

        The specter: neither present nor absent, neither living nor dead
        Inheritance: we are always haunted by what comes before
        The to-come (à-venir): haunted by what is not yet
        """
        text_lower = text.lower()

        # Ghost/specter indicators
        ghost_words = ["ghost", "specter", "haunt", "spirit", "phantom", "apparition"]
        ghost_count = sum(1 for word in ghost_words if word in text_lower)

        # Past haunting indicators
        past_haunt = ["memory", "history", "inherit", "legacy", "ancestor", "tradition"]
        past_count = sum(1 for word in past_haunt if word in text_lower)

        # Future haunting indicators
        future_haunt = ["future", "coming", "promise", "hope", "fear", "anticipate"]
        future_count = sum(1 for word in future_haunt if word in text_lower)

        # Presence/absence indicators
        presence_absence = ["absent", "gone", "lost", "missing", "remain", "trace"]
        pa_count = sum(1 for word in presence_absence if word in text_lower)

        haunt_score = ghost_count + past_count + future_count + pa_count

        if ghost_count >= 1:
            status = "Explicit Haunting"
            description = "Spectral presence - neither fully present nor absent"
        elif past_count >= 2 and future_count >= 1:
            status = "Temporal Haunting"
            description = "Haunted by both past and future"
        elif past_count >= 2:
            status = "Haunted by the Past"
            description = "Inheritance - the past that does not pass"
        elif future_count >= 2:
            status = "Haunted by the To-Come"
            description = "The future that already affects the present"
        elif pa_count >= 2:
            status = "Presence of Absence"
            description = "What is absent makes itself felt"
        else:
            status = "Implicit Hauntology"
            description = "All presence is haunted by absence"

        return {
            "status": status,
            "description": description,
            "ghost_score": ghost_count,
            "past_haunting": past_count,
            "future_haunting": future_count,
            "presence_absence": pa_count,
            "hauntology_score": haunt_score,
            "principle": "Hauntology: We are haunted by specters - neither present nor absent",
        }

    def _assess_iterability(self, text: str) -> Dict[str, Any]:
        """
        Assess iterability - repeatability that introduces difference.

        Every repetition is also alteration.
        Signs must be iterable (repeatable) but this enables change.
        """
        text_lower = text.lower()

        # Repetition indicators
        repeat_words = ["repeat", "again", "same", "identical", "copy", "reproduce"]
        repeat_count = sum(1 for word in repeat_words if word in text_lower)

        # Difference indicators
        diff_words = ["different", "change", "alter", "transform", "vary", "new"]
        diff_count = sum(1 for word in diff_words if word in text_lower)

        # Context indicators
        context_words = ["context", "situation", "circumstance", "occasion"]
        context_count = sum(1 for word in context_words if word in text_lower)

        # Quotation/citation indicators
        quote_words = ["quote", "cite", "refer", "mention", "repeat"]
        quote_count = sum(1 for word in quote_words if word in text_lower)

        if repeat_count >= 1 and diff_count >= 1:
            status = "Iterability Manifest"
            description = "Repetition introduces difference - the same is also other"
        elif repeat_count >= 2:
            status = "Repetition Without Sameness"
            description = "Repetition cannot guarantee identity"
        elif context_count >= 1:
            status = "Context Dependency"
            description = "Meaning shifts with context - iteration alters"
        elif quote_count >= 1:
            status = "Citationality"
            description = "Every sign can be quoted, lifted from its context"
        else:
            status = "Implicit Iterability"
            description = "All signs are iterable - this is the condition of language"

        return {
            "status": status,
            "description": description,
            "repeat_score": repeat_count,
            "difference_score": diff_count,
            "context_score": context_count,
            "citation_score": quote_count,
            "principle": "Iterability: Repetition is the condition of both identity and difference",
        }

    def _identify_aporia(self, text: str) -> List[Dict[str, str]]:
        """
        Identify aporia - impasses, contradictions that cannot be resolved.

        Aporia: the impossible possibility, the impassable passage
        """
        aporias = []
        text_lower = text.lower()

        # Explicit aporia indicators
        if any(
            phrase in text_lower
            for phrase in ["impossible", "cannot", "impassable", "contradiction"]
        ):
            aporias.append(
                {
                    "type": "Explicit Impasse",
                    "description": "The text acknowledges an impossibility or impasse",
                    "significance": "The aporia is where thinking must linger",
                }
            )

        # Double bind indicators
        if any(
            phrase in text_lower
            for phrase in ["both and", "neither nor", "at the same time"]
        ):
            aporias.append(
                {
                    "type": "Double Bind",
                    "description": "Contradictory demands that cannot both be satisfied",
                    "significance": "No resolution without loss",
                }
            )

        # Decision indicators
        if any(word in text_lower for word in ["decide", "choice", "decision"]):
            aporias.append(
                {
                    "type": "Aporia of Decision",
                    "description": "A true decision passes through the undecidable",
                    "significance": "If it were calculable, it would not be a decision",
                }
            )

        # Responsibility indicators
        if any(
            word in text_lower for word in ["responsible", "responsibility", "duty"]
        ):
            aporias.append(
                {
                    "type": "Aporia of Responsibility",
                    "description": "Responsibility to one may mean irresponsibility to others",
                    "significance": "Responsibility is aporetic",
                }
            )

        if not aporias:
            aporias.append(
                {
                    "type": "Latent Aporia",
                    "description": "Every text encounters its own limits",
                    "significance": "The aporia is where deconstruction begins",
                }
            )

        return aporias

    def _analyze_gift(self, text: str) -> Dict[str, Any]:
        """
        Analyze the gift - the impossibility of the pure gift.

        A pure gift must not be recognized as gift, or it creates debt.
        The gift is impossible yet necessary.
        """
        text_lower = text.lower()

        # Gift indicators
        gift_words = ["gift", "give", "giving", "donate", "offer", "present"]
        gift_count = sum(1 for word in gift_words if word in text_lower)

        # Exchange indicators
        exchange_words = ["exchange", "return", "repay", "debt", "owe", "reciprocate"]
        exchange_count = sum(1 for word in exchange_words if word in text_lower)

        # Gratuity indicators
        gratuitous_words = ["free", "gratuitous", "without return", "unconditional"]
        gratuitous_count = sum(1 for phrase in gratuitous_words if phrase in text_lower)

        if gift_count >= 1 and exchange_count >= 1:
            status = "Gift/Economy Tension"
            description = "The gift enters the economy and is annulled as gift"
            aporia = True
        elif gift_count >= 1 and gratuitous_count >= 1:
            status = "Attempted Pure Gift"
            description = "An attempt at the gift without return - but is it possible?"
            aporia = True
        elif gift_count >= 2:
            status = "Gift Mentioned"
            description = "Gifting is at stake but its impossibility is not thematized"
            aporia = False
        elif exchange_count >= 1:
            status = "Economy"
            description = "Exchange economy - no pure gift"
            aporia = False
        else:
            status = "Not Explicitly Present"
            description = "The question of the gift is not raised"
            aporia = False

        return {
            "status": status,
            "description": description,
            "aporia_active": aporia,
            "gift_score": gift_count,
            "exchange_score": exchange_count,
            "gratuitous_score": gratuitous_count,
            "principle": "The Gift: The pure gift is impossible - recognition annuls it",
        }

    def _analyze_justice(self, text: str) -> Dict[str, Any]:
        """
        Analyze justice vs law.

        Law is deconstructible - it can be criticized and reformed.
        Justice is not deconstructible - it is the undeconstructible.
        """
        text_lower = text.lower()

        # Justice indicators
        justice_words = ["justice", "just", "fair", "fairness", "righteous"]
        justice_count = sum(1 for word in justice_words if word in text_lower)

        # Law indicators
        law_words = ["law", "legal", "rule", "regulation", "statute", "code"]
        law_count = sum(1 for word in law_words if word in text_lower)

        # Rights indicators
        rights_words = ["right", "rights", "entitlement"]
        rights_count = sum(1 for word in rights_words if word in text_lower)

        # Violence indicators
        violence_words = ["violence", "force", "power", "enforce"]
        violence_count = sum(1 for word in violence_words if word in text_lower)

        if justice_count >= 1 and law_count >= 1:
            status = "Justice/Law Distinction"
            description = "Both justice and law are at stake - are they aligned?"
            deconstruction = "Law can be deconstructed in the name of justice"
        elif justice_count >= 2:
            status = "Justice Invoked"
            description = "Justice as the undeconstructible"
            deconstruction = "Justice is what deconstruction answers to"
        elif law_count >= 1:
            status = "Law Without Justice"
            description = "Law is present but is it just?"
            deconstruction = "Law is always deconstructible"
        elif violence_count >= 1:
            status = "Force/Violence"
            description = "Law's foundation in violence is at stake"
            deconstruction = "The violence of foundation can be questioned"
        else:
            status = "Not Explicitly Present"
            description = "Justice and law not directly addressed"
            deconstruction = "Implicit normative claims may be deconstructed"

        return {
            "status": status,
            "description": description,
            "deconstruction_note": deconstruction,
            "justice_score": justice_count,
            "law_score": law_count,
            "rights_score": rights_count,
            "violence_score": violence_count,
            "principle": "Justice: The undeconstructible that deconstruction serves",
        }

    def _apply_derrida_to_problem(self, text: str) -> str:
        """Apply Derridean concepts to the domain of the given text."""
        t = text.lower()
        if any(
            w in t
            for w in [
                "language",
                "text",
                "word",
                "write",
                "read",
                "sign",
                "meaning",
                "interpret",
                "literal",
                "metaphor",
            ]
        ):
            return (
                "Deconstruction reveals that every text is inhabited by tensions and contradictions "
                "it cannot fully master. Différance — Derrida's portmanteau of 'deferral' and "
                "'difference' — designates the movement by which meaning is never fully present: "
                "each sign refers to other signs, endlessly deferring the arrival of a stable "
                "signified. The dream of a purely transparent language, a pure logos that would "
                "deliver meaning without mediation, is precisely the logocentric illusion that "
                "deconstruction dismantles. Reading therefore becomes an act of attending to the "
                "margins, the supplements, the traces of what a text had to exclude in order to "
                "appear coherent."
            )
        elif any(
            w in t
            for w in [
                "oppos",
                "binary",
                "versus",
                "either",
                "or",
                "distinction",
                "contrast",
                "hierarchy",
                "prior",
                "original",
            ]
        ):
            return (
                "Binary oppositions — nature/culture, speech/writing, presence/absence, "
                "reason/madness — are not neutral analytical tools but hierarchical structures "
                "in which one term is privileged and the other subordinated. Deconstruction's "
                "first move is to reverse the hierarchy: to show how the 'inferior' term is in "
                "fact constitutive of the 'superior' one. Its second move displaces the opposition "
                "altogether, showing that it cannot be maintained in its apparent clarity. The "
                "inferior term always haunts the superior as its necessary supplement, its "
                "constitutive outside — the writing that 'mere' speech cannot do without, the "
                "absence that defines presence."
            )
        elif any(
            w in t
            for w in [
                "justice",
                "law",
                "right",
                "legal",
                "fair",
                "norm",
                "rule",
                "obligation",
                "court",
                "punishment",
            ]
        ):
            return (
                "In 'Force of Law', Derrida argues that law is deconstructible — its foundations "
                "in force and convention can always be questioned — but justice is not: justice is "
                "the very experience of deconstruction, what deconstruction is in the service of. "
                "Justice is 'to-come' (l'avenir): never fully present, never calculable, never "
                "reducible to the application of an existing rule. Every genuine decision faces an "
                "aporia — it must both follow a rule (or it is arbitrary) and be singular (or it "
                "is merely mechanical); it must be both just and legal, both certain and uncertain. "
                "This undecidability is not a defect but the very condition of responsibility."
            )
        elif any(
            w in t
            for w in [
                "hospitality",
                "welcome",
                "stranger",
                "foreigner",
                "guest",
                "host",
                "other",
                "immigrant",
                "refugee",
                "border",
            ]
        ):
            return (
                "Derrida's meditation on hospitality traces an irreducible tension between "
                "unconditional hospitality — welcome the stranger absolutely, without condition, "
                "without asking for a name — and conditional hospitality, which is the only "
                "hospitality we can actually practice (hospitality with laws, with limits, with "
                "identities verified). The word itself carries the aporia: 'hostis' means both "
                "host and enemy; the guest threatens to become master of the house. Pure "
                "unconditional hospitality is impossible and perhaps even unjust (it dissolves "
                "the home that makes welcoming possible); yet conditional hospitality falls short "
                "of the unconditional demand. We must negotiate this aporia without resolution."
            )
        elif any(
            w in t
            for w in [
                "identity",
                "self",
                "difference",
                "same",
                "origin",
                "pure",
                "authentic",
                "culture",
                "tradition",
                "heritage",
            ]
        ):
            return (
                "There is no pure self-presence, no originary identity that precedes its relation "
                "to the Other. Différance shows that identity is constituted through difference and "
                "deferral: the 'same' is only intelligible against what it differs from, and what "
                "it differs from leaves a trace within it. The dream of cultural or personal purity "
                "— an identity untouched by the Other — is both impossible and politically "
                "dangerous; deconstruction shows that the Other is always already within the Same. "
                "What Derrida calls the 'trace' — the mark of the Other in every identity — "
                "is not a contamination to be purged but the condition of possibility of any "
                "identity whatsoever."
            )
        elif any(
            w in t
            for w in [
                "knowledge",
                "meaning",
                "concept",
                "idea",
                "theory",
                "philosophy",
                "foundation",
                "ground",
                "center",
                "system",
            ]
        ):
            return (
                "Every system of thought requires a center — a ground, an origin, a presence — "
                "that governs the play of the system's elements while itself standing outside "
                "that play. But Derrida shows that the center is itself a function of the "
                "structure, not its exterior foundation; the 'center is not the center'. The "
                "supplement reveals the incompleteness of what it was supposed merely to add to: "
                "writing supplements speech (in Rousseau and Plato) precisely because speech was "
                "never self-sufficient; the supplement fills a lack that the 'original' was "
                "supposed not to have. Iterability — the repeatability of any sign in new contexts "
                "— means that no meaning can be fully controlled or fixed by an originating "
                "intention."
            )
        else:
            return (
                "Deconstruction is not a method applied from outside but a patient attention to "
                "the internal tensions and undecidabilities that every text, institution, or "
                "practice harbors. Différance — the irreducible play of difference and deferral "
                "— ensures that no meaning, no identity, no presence is ever fully itself. "
                "Binary oppositions organize our thought but are hierarchical and unstable; "
                "the trace of the excluded term persists within the privileged one. Justice, "
                "hospitality, friendship, democracy — these are names for the unconditional "
                "demand that always exceeds any conditional, calculable instance of them: they "
                "are 'to-come', the infinite responsibility that deconstruction keeps open. "
                "Of Grammatology, Writing and Difference, and Specters of Marx each open this "
                "space of undecidability in a different domain."
            )

    def _construct_reasoning(
        self,
        prompt: str,
        binaries: List[Dict[str, Any]],
        traces: List[Dict[str, str]],
        differance: Dict[str, Any],
        contradictions: List[Dict[str, str]],
        supplement: Dict[str, Any],
        logocentrism: Dict[str, Any],
        undecidables: List[Dict[str, str]],
        aporia: List[Dict[str, str]],
    ) -> str:
        """Construct comprehensive deconstructive reasoning."""
        applied = self._apply_derrida_to_problem(prompt)
        # Start with binary oppositions
        primary_binary = binaries[0]["opposition"] if binaries else "presence/absence"
        reasoning = (
            f"{applied}\n\n"
            f"Through deconstruction, we reveal that this text operates through binary oppositions "
            f"(such as {primary_binary}). These oppositions are not neutral but hierarchical, "
            f"privileging one term over its 'inferior' other. "
        )

        # Add différance analysis
        reasoning += f"Différance: {differance['description']}. "

        # Add trace analysis
        primary_trace = (
            traces[0] if traces else {"description": "the trace of the unspoken"}
        )
        reasoning += f"The traces of what is absent shape what appears present: {primary_trace['description']}. "

        # Add supplement logic
        if supplement["paradox_active"]:
            reasoning += f"The logic of the supplement: {supplement['description']}. "

        # Add logocentrism critique
        if logocentrism["total_logocentric"] >= 2:
            reasoning += f"Logocentric tendency: {logocentrism['description']}. "

        # Add contradictions
        primary_contradiction = (
            contradictions[0] if contradictions else {"description": "latent tensions"}
        )
        reasoning += f"{primary_contradiction['description']}. "

        # Add undecidables
        if undecidables and undecidables[0]["term"] != "[implicit undecidable]":
            reasoning += (
                f"Undecidable: '{undecidables[0]['term']}' destabilizes the binary. "
            )

        # Add aporia
        primary_aporia = (
            aporia[0] if aporia else {"description": "the text encounters its limits"}
        )
        reasoning += f"Aporia: {primary_aporia['description']}. "

        # Conclude
        reasoning += (
            "Thus, the text undermines its own claimed stability. "
            "Deconstruction does not destroy but reveals the text's own internal tensions, "
            "the play of différance that makes meaning both possible and impossible."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate deconstructive tension.

        Tension arises from:
        - Strong binary oppositions (hierarchical)
        - High logocentrism
        - Suppressed contradictions
        - Active aporias
        """
        tension_score = 0
        tension_elements = []

        # Check binary oppositions
        binaries = analysis["binaries"]
        if len(binaries) >= 3:
            tension_score += 2
            tension_elements.append("Multiple binary oppositions at work")
        elif len(binaries) >= 1:
            tension_score += 1
            tension_elements.append(f"Binary: {binaries[0]['opposition']}")

        # Check logocentrism
        logo = analysis["logocentrism"]
        if logo["total_logocentric"] >= 4:
            tension_score += 2
            tension_elements.append("Strong logocentric tendency")
        elif logo["total_logocentric"] >= 2:
            tension_score += 1
            tension_elements.append("Moderate logocentrism")

        # Check contradictions
        contradictions = analysis["contradictions"]
        if any("Paradox" in c.get("type", "") for c in contradictions):
            tension_score += 2
            tension_elements.append("Paradox present")

        # Check undecidables
        undecidables = analysis["undecidables"]
        if any(u["term"] != "[implicit undecidable]" for u in undecidables):
            tension_score += 1
            tension_elements.append("Undecidables destabilize binaries")

        # Check aporia
        aporia = analysis["aporia"]
        if any(
            "Explicit" in a.get("type", "") or "Double" in a.get("type", "")
            for a in aporia
        ):
            tension_score += 2
            tension_elements.append("Explicit aporia")

        # Check différance
        differance = analysis["differance"]
        if differance["differance_score"] >= 4:
            tension_score += 1
            tension_elements.append("High différance in play")

        # Determine tension level
        if tension_score >= 6:
            level = "Very High"
            description = "Text highly unstable - deconstruction reveals deep fissures"
        elif tension_score >= 4:
            level = "High"
            description = "Significant tensions and contradictions"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some deconstructive tensions present"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, relatively stable"
        else:
            level = "Very Low"
            description = (
                "Minimal explicit tensions (but deconstruction always applies)"
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements
                if tension_elements
                else ["Implicit tensions always present"]
            ),
        }
