"""
Gilles Deleuze - French Post-Structuralist Philosopher

Gilles Deleuze (1925-1995)
Focus: Difference, Rhizome, Becoming, Body without Organs, Deterritorialization

Key Concepts:
- Rhizome: Non-hierarchical, multi-directional connections (vs tree structure)
- Difference and Repetition: Difference is primary, identity is secondary
- Body without Organs (BwO): Resistance to fixed organization, pure potentiality
- Becoming: Not being but becoming (becoming-animal, becoming-woman, etc.)
- Lines of Flight (lignes de fuite): Escape from established orders
- Deterritorialization and Reterritorialization: Breaking from/reforming territories
- Smooth and Striated Space: Smooth (nomadic) vs striated (sedentary)
- Desiring-Machines: Desire as productive, not lack-based
- Assemblage (agencement): Heterogeneous multiplicities
- Virtual and Actual: Virtuality as real but not actualized
- Concept Creation: Philosophy as creation of concepts, not contemplation
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Deleuze(Philosopher):
    """
    Gilles Deleuze's philosophy of difference and becoming.

    Analyzes prompts through the lens of rhizomes, becoming,
    deterritorialization, and creative difference.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Gilles Deleuze",
            description="Post-structuralist focused on difference, rhizomes, becoming, and concept creation"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Deleuze's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Deleuze's differential analysis
        """
        # Perform Deleuzian analysis
        analysis = self._analyze_difference(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Philosophy of Difference / Post-Structuralism",
            "rhizome_vs_tree": analysis["rhizome"],
            "difference_repetition": analysis["difference"],
            "becoming": analysis["becoming"],
            "body_without_organs": analysis["bwo"],
            "lines_of_flight": analysis["lines"],
            "territorialization": analysis["territory"],
            "smooth_striated": analysis["space"],
            "desire": analysis["desire"],
            "virtuality": analysis["virtuality"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Creative difference and multiplicity",
                "focus": "Rhizomes, becoming, and deterritorialization"
            }
        }

    def _analyze_difference(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Deleuzian differential analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess rhizome vs tree structure
        rhizome = self._assess_rhizome_tree(prompt)

        # Analyze difference and repetition
        difference = self._analyze_difference_repetition(prompt)

        # Detect becoming
        becoming = self._detect_becoming(prompt)

        # Check for body without organs
        bwo = self._check_body_without_organs(prompt)

        # Identify lines of flight
        lines = self._identify_lines_of_flight(prompt)

        # Assess territorialization
        territory = self._assess_territorialization(prompt)

        # Evaluate smooth vs striated space
        space = self._evaluate_smooth_striated(prompt)

        # Analyze desire
        desire = self._analyze_desire(prompt)

        # Check virtuality
        virtuality = self._check_virtuality(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            rhizome, difference, becoming, lines, territory
        )

        return {
            "reasoning": reasoning,
            "rhizome": rhizome,
            "difference": difference,
            "becoming": becoming,
            "bwo": bwo,
            "lines": lines,
            "territory": territory,
            "space": space,
            "desire": desire,
            "virtuality": virtuality
        }

    def _assess_rhizome_tree(self, text: str) -> Dict[str, Any]:
        """
        Assess rhizomatic vs arborescent (tree) structure.

        Rhizome: Non-hierarchical, multi-directional, any point connects to any other
        Tree: Hierarchical, root-trunk-branches, binary divisions
        """
        text_lower = text.lower()

        # Rhizomatic indicators
        rhizome_words = ["network", "connection", "interconnect", "web", "mesh", "lateral", "horizontal"]
        has_rhizome = sum(1 for word in rhizome_words if word in text_lower)

        # Tree/hierarchical indicators
        tree_words = ["hierarchy", "top", "bottom", "root", "branch", "level", "above", "below", "structure"]
        has_tree = sum(1 for word in tree_words if word in text_lower)

        # Multiple entry points (rhizomatic)
        multiple_words = ["multiple", "many", "various", "diverse", "different paths", "ways"]
        has_multiple = sum(1 for word in multiple_words if word in text_lower)

        # Single origin (arborescent)
        single_words = ["single", "one", "origin", "source", "beginning", "foundation"]
        has_single = sum(1 for word in single_words if word in text_lower)

        # Determine structure
        rhizome_score = has_rhizome + has_multiple
        tree_score = has_tree + has_single

        if rhizome_score > tree_score and rhizome_score >= 2:
            structure = "Rhizomatic"
            description = "Non-hierarchical, multi-directional connections - any point connects to any other"
            type_struct = "Nomadic"
        elif tree_score > rhizome_score and tree_score >= 2:
            structure = "Arborescent (Tree)"
            description = "Hierarchical, rooted structure - binary divisions and vertical organization"
            type_struct = "Sedentary"
        elif rhizome_score > 0 and tree_score > 0:
            structure = "Mixed (Rhizome-Tree)"
            description = "Combination of rhizomatic and arborescent elements"
            type_struct = "Hybrid"
        else:
            structure = "Unclear"
            description = "Structure type not evident"
            type_struct = "Indeterminate"

        return {
            "structure": structure,
            "description": description,
            "type": type_struct,
            "principle": "The rhizome is anti-hierarchical - any point connects to any other"
        }

    def _analyze_difference_repetition(self, text: str) -> Dict[str, Any]:
        """
        Analyze difference and repetition.

        Deleuze: Difference is primary, identity/sameness is derivative
        Repetition always produces difference, never exact sameness
        """
        text_lower = text.lower()

        # Difference indicators
        difference_words = ["different", "differ", "difference", "vary", "change", "unique", "distinct"]
        has_difference = sum(1 for word in difference_words if word in text_lower)

        # Sameness/identity indicators
        same_words = ["same", "identical", "equal", "similar", "like", "alike", "uniform"]
        has_same = sum(1 for word in same_words if word in text_lower)

        # Repetition indicators
        repetition_words = ["repeat", "again", "recur", "cycle", "pattern", "iterate"]
        has_repetition = sum(1 for word in repetition_words if word in text_lower)

        # Creative/productive repetition
        creative_words = ["new", "create", "generate", "produce", "emerge"]
        has_creative = sum(1 for word in creative_words if word in text_lower)

        if has_difference >= 2:
            orientation = "Difference-Oriented"
            description = "Primacy of difference - identity is derivative, difference is fundamental"
            status = "Deleuzian"
        elif has_repetition >= 1 and has_creative >= 1:
            orientation = "Creative Repetition"
            description = "Repetition that produces difference - each return is unique"
            status = "Deleuzian"
        elif has_same >= 2:
            orientation = "Identity-Oriented"
            description = "Emphasis on sameness and identity - pre-Deleuzian"
            status = "Traditional"
        else:
            orientation = "Unclear"
            description = "Relation to difference/identity unclear"
            status = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "status": status,
            "principle": "Difference is primary - identity is a product of difference, not vice versa"
        }

    def _detect_becoming(self, text: str) -> Dict[str, Any]:
        """
        Detect becoming (devenir).

        Becoming vs being: Process of transformation, not stable states
        Becoming-animal, becoming-woman, becoming-imperceptible, etc.
        """
        text_lower = text.lower()

        # Becoming indicators
        becoming_words = ["become", "becoming", "transform", "metamorphose", "change into", "turn into"]
        has_becoming = sum(1 for word in becoming_words if word in text_lower)

        # Being/state indicators (opposed to becoming)
        being_words = ["is", "are", "being", "state", "fixed", "stable", "permanent", "essence"]
        has_being = sum(1 for word in being_words if word in text_lower)

        # Process/movement indicators
        process_words = ["process", "flow", "movement", "flux", "transition", "passage"]
        has_process = sum(1 for word in process_words if word in text_lower)

        # Specific becomings
        specific_becomings = []
        if "animal" in text_lower or "creature" in text_lower:
            specific_becomings.append("Becoming-animal")
        if "woman" in text_lower or "feminine" in text_lower:
            specific_becomings.append("Becoming-woman")
        if "invisible" in text_lower or "imperceptible" in text_lower:
            specific_becomings.append("Becoming-imperceptible")
        if "child" in text_lower:
            specific_becomings.append("Becoming-child")
        if "molecular" in text_lower or "particle" in text_lower:
            specific_becomings.append("Becoming-molecular")

        if has_becoming >= 2 or (has_becoming >= 1 and has_process >= 1):
            presence = "Strong Becoming"
            description = "Emphasis on becoming over being - process over state"
            mode = "Nomadic"
        elif has_process >= 2:
            presence = "Process-Oriented"
            description = "Process and movement emphasized"
            mode = "Becoming-oriented"
        elif has_being > has_becoming * 2:
            presence = "Being-Oriented"
            description = "Emphasis on stable states and being - opposed to Deleuzian becoming"
            mode = "Sedentary"
        else:
            presence = "Unclear"
            description = "Becoming vs being orientation unclear"
            mode = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "mode": mode,
            "specific_becomings": specific_becomings if specific_becomings else ["None detected"],
            "principle": "Becoming, not being - life is process, not state"
        }

    def _check_body_without_organs(self, text: str) -> Dict[str, Any]:
        """
        Check for body without organs (BwO).

        BwO: Resistance to fixed organization, pure potentiality
        Against the organism as organized, stratified body
        """
        text_lower = text.lower()

        # BwO indicators (resistance to organization)
        resistance_words = ["resist", "against", "oppose", "reject", "refuse", "break free"]
        has_resistance = sum(1 for word in resistance_words if word in text_lower)

        # Organization/structure indicators
        organization_words = ["organize", "structure", "system", "order", "arranged", "fixed"]
        has_organization = sum(1 for word in organization_words if word in text_lower)

        # Potentiality/openness indicators
        potential_words = ["potential", "possible", "open", "fluid", "flexible", "unformed"]
        has_potential = sum(1 for word in potential_words if word in text_lower)

        # Intensity/desire indicators
        intensity_words = ["intensity", "desire", "passion", "force", "energy", "power"]
        has_intensity = sum(1 for word in intensity_words if word in text_lower)

        if has_resistance >= 1 and has_organization >= 1:
            status = "BwO Present"
            description = "Resistance to fixed organization - striving for pure potentiality"
            level = "Active"
        elif has_potential >= 2 or has_intensity >= 2:
            status = "BwO Tendency"
            description = "Emphasis on potentiality and intensity"
            level = "Emerging"
        elif has_organization >= 2 and has_resistance == 0:
            status = "Organized Body"
            description = "Acceptance of fixed organization - opposed to BwO"
            level = "Absent"
        else:
            status = "Unclear"
            description = "BwO status unclear"
            level = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "level": level,
            "principle": "The BwO is not against organs, but against the organism's organization"
        }

    def _identify_lines_of_flight(self, text: str) -> Dict[str, Any]:
        """
        Identify lines of flight (lignes de fuite).

        Lines of flight: Escape routes, deterritorialization, creative transformation
        Breaking away from established structures and territories
        """
        text_lower = text.lower()

        # Flight/escape indicators
        flight_words = ["escape", "flee", "break away", "departure", "exit", "leave", "abandon"]
        has_flight = sum(1 for word in flight_words if word in text_lower)

        # Constraint/capture indicators
        constraint_words = ["trapped", "confined", "stuck", "bound", "limited", "restricted"]
        has_constraint = sum(1 for word in constraint_words if word in text_lower)

        # Creation/transformation indicators
        creation_words = ["create", "new", "transform", "invent", "innovate", "generate"]
        has_creation = sum(1 for word in creation_words if word in text_lower)

        # Established order indicators
        order_words = ["established", "traditional", "conventional", "normal", "standard", "system"]
        has_order = sum(1 for word in order_words if word in text_lower)

        # Determine lines of flight
        if has_flight >= 1 and has_creation >= 1:
            presence = "Active Lines of Flight"
            description = "Creative escape from established orders - deterritorialization in action"
            type_line = "Revolutionary"
        elif has_constraint >= 1 and (has_flight >= 1 or has_creation >= 1):
            presence = "Emerging Lines of Flight"
            description = "Awareness of constraint with movement toward escape"
            type_line = "Potential"
        elif has_order >= 2 and has_flight == 0:
            presence = "No Lines of Flight"
            description = "Captured by established order - reterritorialized"
            type_line = "Blocked"
        else:
            presence = "Unclear"
            description = "Lines of flight status unclear"
            type_line = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "type": type_line,
            "principle": "Lines of flight are creative escapes that produce new territories"
        }

    def _assess_territorialization(self, text: str) -> Dict[str, Any]:
        """
        Assess territorialization, deterritorialization, and reterritorialization.

        Territory: Established domain or organization
        Deterritorialization: Breaking from territory
        Reterritorialization: Forming new territory
        """
        text_lower = text.lower()

        # Territorialization indicators (establishing territory)
        territory_words = ["establish", "found", "create space", "domain", "territory", "ground", "base"]
        has_territory = sum(1 for word in territory_words if word in text_lower)

        # Deterritorialization indicators (breaking away)
        deterrit_words = ["break", "dissolve", "disrupt", "deconstruct", "dismantle", "escape"]
        has_deterrit = sum(1 for word in deterrit_words if word in text_lower)

        # Reterritorialization indicators (reforming)
        reterrit_words = ["reform", "rebuild", "reconstruct", "new order", "reorganize"]
        has_reterrit = sum(1 for word in reterrit_words if word in text_lower)

        # Determine process
        if has_deterrit >= 1 and has_reterrit >= 1:
            process = "Deterritorialization-Reterritorialization"
            description = "Breaking from old territories while forming new ones - creative transformation"
            status = "Dynamic"
        elif has_deterrit >= 2:
            process = "Deterritorialization"
            description = "Breaking away from established territories - lines of flight active"
            status = "Revolutionary"
        elif has_territory >= 2 and has_deterrit == 0:
            process = "Territorialized"
            description = "Established in fixed territory - no movement toward escape"
            status = "Static"
        else:
            process = "Unclear"
            description = "Territorialization process unclear"
            status = "Indeterminate"

        return {
            "process": process,
            "description": description,
            "status": status,
            "principle": "Deterritorialization and reterritorialization are constant processes"
        }

    def _evaluate_smooth_striated(self, text: str) -> Dict[str, Any]:
        """
        Evaluate smooth vs striated space.

        Smooth space: Nomadic, open, fluid, intensive (desert, sea, ice)
        Striated space: Sedentary, organized, metric, extensive (city, agriculture)
        """
        text_lower = text.lower()

        # Smooth space indicators
        smooth_words = ["open", "fluid", "flow", "nomadic", "wander", "drift", "smooth", "continuous"]
        has_smooth = sum(1 for word in smooth_words if word in text_lower)

        # Striated space indicators
        striated_words = ["grid", "line", "boundary", "division", "segment", "organize", "measure", "metric"]
        has_striated = sum(1 for word in striated_words if word in text_lower)

        # Nomadic indicators
        nomadic_words = ["move", "travel", "journey", "roam", "explore"]
        has_nomadic = sum(1 for word in nomadic_words if word in text_lower)

        # Sedentary indicators
        sedentary_words = ["settle", "stay", "fixed", "permanent", "home", "stable"]
        has_sedentary = sum(1 for word in sedentary_words if word in text_lower)

        smooth_score = has_smooth + has_nomadic
        striated_score = has_striated + has_sedentary

        if smooth_score > striated_score and smooth_score >= 2:
            space_type = "Smooth Space"
            description = "Nomadic, fluid, intensive - like the sea or desert"
            mode = "Nomadic"
        elif striated_score > smooth_score and striated_score >= 2:
            space_type = "Striated Space"
            description = "Organized, metric, extensive - like the city or grid"
            mode = "Sedentary"
        elif smooth_score > 0 and striated_score > 0:
            space_type = "Mixed Space"
            description = "Combination of smooth and striated - constant transformation"
            mode = "Hybrid"
        else:
            space_type = "Unclear"
            description = "Spatial quality unclear"
            mode = "Indeterminate"

        return {
            "type": space_type,
            "description": description,
            "mode": mode,
            "principle": "Smooth and striated spaces constantly transform into each other"
        }

    def _analyze_desire(self, text: str) -> Dict[str, Any]:
        """
        Analyze desire.

        Deleuzian desire: Productive, creative, affirmative (vs psychoanalytic lack)
        Desiring-machines produce reality
        """
        text_lower = text.lower()

        # Productive desire indicators
        productive_words = ["desire", "produce", "create", "generate", "make", "build"]
        has_productive = sum(1 for word in productive_words if word in text_lower)

        # Lack-based desire indicators (psychoanalytic)
        lack_words = ["lack", "need", "want", "missing", "absence", "void", "empty"]
        has_lack = sum(1 for word in lack_words if word in text_lower)

        # Affirmation indicators
        affirm_words = ["yes", "affirmative", "positive", "embrace", "celebrate"]
        has_affirm = sum(1 for word in affirm_words if word in text_lower)

        # Negation indicators
        negate_words = ["no", "negative", "deny", "refuse", "reject"]
        has_negate = sum(1 for word in negate_words if word in text_lower)

        if has_productive >= 2 or (has_productive >= 1 and has_affirm >= 1):
            conception = "Productive Desire"
            description = "Desire as productive and creative - desiring-machines"
            type_desire = "Deleuzian"
        elif has_lack >= 2:
            conception = "Lack-Based Desire"
            description = "Desire as lack or need - psychoanalytic model"
            type_desire = "Psychoanalytic"
        else:
            conception = "Unclear"
            description = "Conception of desire unclear"
            type_desire = "Indeterminate"

        return {
            "conception": conception,
            "description": description,
            "type": type_desire,
            "principle": "Desire is productive, not based on lack - desiring-machines produce reality"
        }

    def _check_virtuality(self, text: str) -> Dict[str, Any]:
        """
        Check virtuality.

        Virtual: Real but not actual, fully real potentiality
        Not opposed to real, but to actual
        Virtual-actual vs possible-real distinction
        """
        text_lower = text.lower()

        # Virtuality indicators
        virtual_words = ["virtual", "potential", "latent", "implicit", "immanent"]
        has_virtual = sum(1 for word in virtual_words if word in text_lower)

        # Actuality indicators
        actual_words = ["actual", "actualize", "realize", "manifest", "explicit"]
        has_actual = sum(1 for word in actual_words if word in text_lower)

        # Possibility indicators (different from virtuality)
        possible_words = ["possible", "might", "could", "maybe", "perhaps"]
        has_possible = sum(1 for word in possible_words if word in text_lower)

        if has_virtual >= 1 or (has_actual >= 1 and "realize" in text_lower):
            status = "Virtual-Actual Relation"
            description = "Recognition of virtuality - real but not yet actualized"
            understanding = "Deleuzian"
        elif has_possible >= 2:
            status = "Possible-Real Relation"
            description = "Thinking in terms of possibility - not yet Deleuzian virtuality"
            understanding = "Traditional"
        else:
            status = "Unclear"
            description = "Virtuality status unclear"
            understanding = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "understanding": understanding,
            "principle": "The virtual is real - virtuality is not opposed to reality but to actuality"
        }

    def _construct_reasoning(
        self,
        rhizome: Dict[str, Any],
        difference: Dict[str, Any],
        becoming: Dict[str, Any],
        lines: Dict[str, Any],
        territory: Dict[str, Any]
    ) -> str:
        """Construct Deleuzian differential reasoning."""
        reasoning = (
            f"From a Deleuzian perspective, the structure here is {rhizome['structure']}: {rhizome['description']}. "
            f"Regarding difference: {difference['description']}. "
            f"Becoming: {becoming['description']}. "
        )

        # Add lines of flight
        reasoning += f"Lines of flight: {lines['description']}. "

        # Add territorialization
        reasoning += f"Territorialization: {territory['description']}. "

        # Conclude with Deleuzian principle
        reasoning += (
            "Remember: Create concepts, don't contemplate them. "
            "Difference is primary. Life is becoming, not being. "
            "Escape the organism through the body without organs."
        )

        return reasoning
