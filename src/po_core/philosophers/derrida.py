"""
Derrida - Deconstructionist Philosopher

Jacques Derrida (1930-2004)
Focus: Deconstruction, Différance, Trace, Binary Opposition

Key Concepts:
- Deconstruction: Revealing hidden assumptions and contradictions
- Différance: Difference + deferral of meaning
- Trace: The absent presence, what is excluded to define something
- Binary Opposition: Hierarchical oppositions (speech/writing, presence/absence)
- Logocentrism: Critique of the privilege of presence and voice
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Derrida(Philosopher):
    """
    Derrida's deconstructionist perspective.

    Analyzes prompts by revealing hidden assumptions, binary oppositions,
    and the play of différance (difference and deferral).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Jacques Derrida",
            description="Deconstructionist focusing on différance, trace, and the instability of meaning"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Derrida's deconstructionist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Derrida's deconstructive analysis
        """
        # Perform deconstructive analysis
        analysis = self._deconstruct(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Deconstructionist",
            "binary_oppositions": analysis["binaries"],
            "traces": analysis["traces"],
            "differance": analysis["differance"],
            "contradictions": analysis["contradictions"],
            "what_is_excluded": analysis["excluded"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Deconstruction",
                "focus": "Différance, trace, and binary oppositions"
            }
        }

    def _deconstruct(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Derridean deconstruction.

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

        # Construct deconstructive reasoning
        reasoning = self._construct_reasoning(binaries, traces, differance, contradictions)

        return {
            "reasoning": reasoning,
            "binaries": binaries,
            "traces": traces,
            "differance": differance,
            "contradictions": contradictions,
            "excluded": excluded
        }

    def _find_binary_oppositions(self, text: str) -> List[Dict[str, str]]:
        """Find binary oppositions in the text."""
        binaries = []
        text_lower = text.lower()

        # Common binary pairs
        binary_pairs = [
            ("true", "false"),
            ("good", "bad", "evil"),
            ("right", "wrong"),
            ("present", "absent"),
            ("inside", "outside"),
            ("same", "different"),
            ("self", "other"),
            ("mind", "body"),
            ("nature", "culture"),
            ("speech", "writing"),
            ("reality", "appearance"),
            ("authentic", "inauthentic"),
            ("being", "nothingness", "non-being"),
        ]

        for pair in binary_pairs:
            found = [term for term in pair if term in text_lower]
            if len(found) >= 2:
                binaries.append({
                    "opposition": " / ".join(found),
                    "note": f"Hierarchical opposition detected"
                })
            elif len(found) == 1:
                # Find the implied opposite
                other_terms = [term for term in pair if term not in found]
                if other_terms:
                    binaries.append({
                        "opposition": f"{found[0]} / [{other_terms[0]}]",
                        "note": f"Implicit opposition - '{other_terms[0]}' is the absent trace"
                    })

        if not binaries:
            binaries.append({
                "opposition": "meaning / [non-meaning]",
                "note": "The text itself presupposes an opposition to what it excludes"
            })

        return binaries

    def _find_traces(self, text: str) -> List[str]:
        """Identify traces - what is absent but shapes the present."""
        traces = []

        # Look for negations (traces of what is denied)
        negation_words = ["not", "no", "never", "nothing", "without", "lack"]
        for word in negation_words:
            if word in text.lower():
                traces.append(f"Negation detected: The absent (what is negated) haunts the present")
                break

        # Look for references to absence
        absence_words = ["absent", "missing", "lost", "forgotten", "hidden"]
        for word in absence_words:
            if word in text.lower():
                traces.append(f"Explicit absence: What is missing defines what is present")
                break

        # Look for implied presence through absence
        if "authentic" in text.lower():
            traces.append("The 'inauthentic' as trace - defines authenticity by exclusion")

        if "meaning" in text.lower():
            traces.append("Non-meaning as trace - meaning requires its opposite to exist")

        if not traces:
            traces.append("The trace of what is unspoken - every text excludes to include")

        return traces

    def _analyze_differance(self, text: str) -> Dict[str, Any]:
        """
        Analyze différance - the play of difference and deferral.

        Différance (with an 'a') = difference + deferral
        Meaning is never fully present, always deferred.
        """
        # Check for temporal deferral
        deferral_words = ["will", "future", "later", "eventually", "become", "promise"]
        has_deferral = any(word in text.lower() for word in deferral_words)

        # Check for relational difference
        difference_words = ["different", "other", "contrast", "versus", "but", "however"]
        has_difference = any(word in text.lower() for word in difference_words)

        # Check for self-reference (meaning referring to other meanings)
        self_ref_words = ["is", "means", "refers to", "signifies", "represents"]
        has_self_ref = any(word in text.lower() for word in self_ref_words)

        status = "stable"
        if has_deferral and has_difference:
            status = "fully deferred - meaning postponed through difference"
        elif has_deferral:
            status = "temporally deferred - meaning postponed to future"
        elif has_difference:
            status = "spatially deferred - meaning defined by difference"
        elif has_self_ref:
            status = "self-referential - meaning refers to other meanings"

        return {
            "temporal_deferral": has_deferral,
            "spatial_difference": has_difference,
            "self_referential": has_self_ref,
            "status": status,
            "note": "Meaning is never fully present, always deferred through différance"
        }

    def _find_contradictions(self, text: str) -> List[str]:
        """Find internal contradictions or tensions."""
        contradictions = []

        # Look for explicit contradictions
        if "but" in text.lower() or "however" in text.lower():
            contradictions.append("Explicit tension: 'but/however' signals internal contradiction")

        # Look for simultaneous affirmation and negation
        if "not" in text.lower() and any(word in text.lower() for word in ["is", "are", "be"]):
            contradictions.append("Negation + Affirmation: Simultaneous presence and absence")

        # Look for paradoxes
        paradox_pairs = [
            ("authentic", "inauthentic"),
            ("true", "false"),
            ("real", "unreal"),
        ]
        for term1, term2 in paradox_pairs:
            if term1 in text.lower() and term2 in text.lower():
                contradictions.append(f"Paradox: {term1} and {term2} coexist, destabilizing meaning")

        if not contradictions:
            contradictions.append("Latent contradiction: All texts contain suppressed tensions")

        return contradictions

    def _find_excluded(self, text: str, binaries: List[Dict[str, str]]) -> List[str]:
        """What is excluded to create this meaning?"""
        excluded = []

        # Extract excluded terms from binaries
        for binary in binaries:
            if "[" in binary["opposition"]:
                # Extract the bracketed (excluded) term
                import re
                matches = re.findall(r'\[(.*?)\]', binary["opposition"])
                if matches:
                    excluded.extend([f"'{match}' - excluded to privilege its opposite" for match in matches])

        # General exclusions
        if "meaning" in text.lower():
            excluded.append("Nonsense and ambiguity - excluded to create 'meaning'")

        if "truth" in text.lower():
            excluded.append("Falsehood and uncertainty - excluded to claim 'truth'")

        if not excluded:
            excluded.append("The undecidable - what cannot be captured by binary logic")

        return excluded

    def _construct_reasoning(
        self,
        binaries: List[Dict[str, str]],
        traces: List[str],
        differance: Dict[str, Any],
        contradictions: List[str]
    ) -> str:
        """Construct the deconstructive reasoning."""
        binary_text = binaries[0]["opposition"] if binaries else "implicit oppositions"

        reasoning = (
            f"Through deconstruction, we reveal that this text operates through binary oppositions "
            f"(such as {binary_text}). These oppositions are not neutral but hierarchical. "
            f"However, the meaning is never fully present - it is deferred through différance: "
            f"{differance['status']}. "
            f"The traces of what is absent (such as: {traces[0]}) shape what appears present. "
            f"{contradictions[0]}. "
            f"Thus, the text undermines its own claimed stability."
        )

        return reasoning
