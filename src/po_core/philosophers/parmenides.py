"""
Parmenides Philosopher Module

Implements pre-Socratic ontology based on Parmenides's philosophy.

Key concepts:
- Being: That which is, the fundamental reality
- Non-Being: That which is not, impossible to think or speak
- The Way of Truth: Philosophical reasoning about reality
- The Way of Opinion: Mortal beliefs about appearances
- Monism: Reality is one, unchanging, indivisible
- Immutability: Being does not change
- Completeness: Being lacks nothing
- Rational Inquiry: Thought and being are the same
- Goddess's Revelation: Divine source of philosophical truth
- Appearance vs Reality: Distinction between seeming and being
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Parmenides(Philosopher):
    """
    Parmenides of Elea (c. 515-450 BCE)

    Pre-Socratic Greek philosopher whose poem 'On Nature' established
    foundational questions of Western metaphysics. He argued that
    Being is one, unchanging, and eternal, and that change and
    plurality are illusions. His work profoundly influenced Plato
    and all subsequent ontology.
    """

    def __init__(self):
        super().__init__(
            name="Parmenides",
            description="Pre-Socratic philosopher who established foundational questions of Western metaphysics",
        )
        self.tradition = "Pre-Socratic / Eleatic School"
        self.key_concepts = [
            "being",
            "non-being",
            "the way of truth",
            "the way of opinion",
            "monism",
            "immutability",
            "completeness",
            "rational inquiry",
            "appearance and reality",
            "necessity",
            "eternity",
            "unity",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Apply Parmenidean ontological reasoning to the prompt.

        Returns analysis through the lens of Being, the critique of
        non-being, and the distinction between truth and opinion.
        """
        analysis = self._analyze_parmenides(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Eleatic Ontology / Pre-Socratic Metaphysics",
            "tension": tension,
            "being": analysis["being"],
            "non_being": analysis["non_being"],
            "way_of_truth": analysis["truth"],
            "way_of_opinion": analysis["opinion"],
            "monism": analysis["monism"],
            "immutability": analysis["immutability"],
            "completeness": analysis["completeness"],
            "appearance_reality": analysis["appearance_reality"],
            "logical_analysis": analysis["logical"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "ontological_reasoning",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_parmenides(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Parmenidean analysis of the prompt."""
        being = self._analyze_being(prompt)
        non_being = self._analyze_non_being(prompt)
        truth = self._analyze_way_of_truth(prompt)
        opinion = self._analyze_way_of_opinion(prompt)
        monism = self._analyze_monism(prompt)
        immutability = self._analyze_immutability(prompt)
        completeness = self._analyze_completeness(prompt)
        appearance_reality = self._analyze_appearance_reality(prompt)
        logical = self._derive_logical_analysis(prompt)

        reasoning = self._construct_reasoning(
            prompt,
            being,
            non_being,
            truth,
            opinion,
            monism,
            immutability,
            completeness,
            appearance_reality,
        )

        return {
            "reasoning": reasoning,
            "being": being,
            "non_being": non_being,
            "truth": truth,
            "opinion": opinion,
            "monism": monism,
            "immutability": immutability,
            "completeness": completeness,
            "appearance_reality": appearance_reality,
            "logical": logical,
        }

    def _analyze_being(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the concept of Being.

        Parmenides's central insight: Being is. That which is,
        necessarily is and cannot not-be.
        """
        return {
            "fundamental_thesis": {
                "statement": "Being is; Non-being is not",
                "necessity": "It is necessary to say and think that being is",
                "impossibility": "You cannot know or speak what is not",
            },
            "characteristics": {
                "ungenerated": "Being never came into being",
                "imperishable": "Being will never cease to be",
                "whole": "Being is complete, not lacking anything",
                "unique": "There is only one Being",
                "unmoved": "Being does not change or move",
                "eternal": "Being has no past or future, only present",
            },
            "signs_of_being": {
                "description": "The 'signposts' (semata) that mark true Being",
                "list": [
                    "Ungenerated and imperishable",
                    "Whole and single",
                    "Unshaken and complete",
                    "Never was nor will be, but is now altogether",
                ],
            },
            "sphere_metaphor": {
                "description": "Being is like a well-rounded sphere",
                "meaning": "Equally balanced in every direction from center",
                "implication": "Perfect, complete, lacking nothing",
            },
            "application": "What is the Being of what is here in question?",
        }

    def _analyze_non_being(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the impossibility of Non-being.

        Parmenides argues that Non-being is unthinkable and unspeakable,
        for to think or speak of it makes it something.
        """
        return {
            "impossibility": {
                "statement": "Non-being is not",
                "reasoning": "You cannot know what is not, nor can you speak it",
                "paradox": "To say 'Non-being is' already makes it something",
            },
            "unthinkability": {
                "claim": "That which is not cannot be thought",
                "reason": "Thought and being are the same",
                "consequence": "All genuine thought is thought of what is",
            },
            "unspeakability": {
                "claim": "Non-being cannot be spoken",
                "reason": "To name is to make present",
                "paradox": "Speaking of nothing speaks of something",
            },
            "forbidden_path": {
                "description": "The path of 'it is not'",
                "warning": "The goddess bars this way utterly",
                "reason": "It leads nowhere; nothing can be learned from nothing",
            },
            "implications": {
                "no_void": "There is no empty space",
                "no_nothing": "There is no absolute nothing",
                "density": "Being is continuous, without gaps",
            },
            "application": "What absurdity arises from supposing non-being here?",
        }

    def _analyze_way_of_truth(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the Way of Truth (aletheia).

        The goddess reveals two paths: the Way of Truth, which speaks
        of what is, and the Way of Opinion, which speaks of appearances.
        """
        return {
            "nature": {
                "description": "The path that says 'it is and cannot not-be'",
                "character": "Follows necessity and truth",
                "method": "Pure rational inquiry, not sense perception",
            },
            "goddess_revelation": {
                "context": "The poem describes a journey to the goddess",
                "teaching": "She reveals the heart of truth to the inquirer",
                "authority": "Divine warrant for rational insight",
            },
            "rational_method": {
                "principle": "Follow logos (reason) where it leads",
                "rejection": "Do not trust habit born of much experience",
                "tool": "Use reason alone to judge the contested argument",
            },
            "identity_of_thought_and_being": {
                "thesis": "The same thing is for thinking and for being",
                "meaning": "What can be thought is; what cannot be thought is not",
                "significance": "Establishes the rational as the real",
            },
            "application": "What does rational inquiry reveal about this?",
        }

    def _analyze_way_of_opinion(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the Way of Opinion (doxa).

        Mortal opinions err by trusting appearances and mixing
        being with non-being.
        """
        return {
            "nature": {
                "description": "The path of mortal beliefs about appearances",
                "error": "Mortals mistakenly posit both being and non-being",
                "result": "Wandering, two-headed, knowing nothing",
            },
            "mortal_errors": {
                "senses": "Trusting eyes, ears, tongue over reason",
                "habit": "Following customary paths of thought",
                "mixture": "Mixing 'is' and 'is not' in speech",
            },
            "cosmology": {
                "description": "The second part of the poem describes appearances",
                "status": "Deceptive ordering of words, but useful for mortals",
                "elements": "Light and Night as opposing principles",
            },
            "two_headed_mortals": {
                "description": "Those who wander, thinking being and non-being are the same and different",
                "path": "Backward-turning, helpless",
                "condition": "Deafness and blindness possess them",
            },
            "application": "What mortal opinions obscure the truth here?",
        }

    def _analyze_monism(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the doctrine that Being is One.

        Parmenides argues that reality is fundamentally one,
        not many; plurality is illusion.
        """
        return {
            "thesis": {
                "statement": "Being is one",
                "argument": "There is nothing besides Being to divide it",
                "conclusion": "Plurality is appearance, not reality",
            },
            "continuity": {
                "description": "Being is continuous, not divided",
                "reason": "What could separate Being from Being?",
                "only": "Only non-being could divide; but non-being is not",
            },
            "homogeneity": {
                "description": "Being is the same throughout",
                "reason": "There is no more or less of Being",
                "image": "Like a sphere, the same from center in every direction",
            },
            "against_plurality": {
                "challenge": "If there are many things, what distinguishes them?",
                "problem": "Either Being or non-being distinguishes",
                "result": "Non-being cannot; Being is the same everywhere",
            },
            "application": "What unity underlies apparent diversity here?",
        }

    def _analyze_immutability(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the doctrine that Being does not change.

        Parmenides argues that change is impossible because it
        requires something to come from nothing or go into nothing.
        """
        return {
            "thesis": {
                "statement": "Being is unmoved and unchanging",
                "argument": "Change requires coming-to-be or passing-away",
                "problem": "Both require non-being, which is impossible",
            },
            "no_generation": {
                "statement": "Being did not come into being",
                "argument": "From what could it arise? Non-being? Impossible.",
                "question": "What need would urge it to grow later or sooner?",
            },
            "no_destruction": {
                "statement": "Being will not cease to be",
                "argument": "Into what could it pass? Non-being? Impossible.",
                "result": "Being remains what it is eternally",
            },
            "no_motion": {
                "description": "Being does not move or change in any way",
                "reason": "Motion requires void; void is non-being; non-being is not",
                "stillness": "Being rests in its limits",
            },
            "eternal_present": {
                "description": "Being is now, all at once, complete",
                "time": "Past and future do not apply to Being",
                "mode": "Eternal, not everlasting in time",
            },
            "application": "What apparent changes are revealed as illusions?",
        }

    def _analyze_completeness(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the doctrine that Being lacks nothing.

        Being is complete (teleion), whole, lacking nothing,
        bounded and perfect.
        """
        return {
            "thesis": {
                "statement": "Being is complete and lacks nothing",
                "reason": "If it lacked something, it would lack everything",
                "image": "The well-rounded sphere, equal from center everywhere",
            },
            "boundedness": {
                "description": "Being has limits (peiras)",
                "not_infinite": "Unboundedness would be incompleteness",
                "perfection": "Limits express wholeness, not restriction",
            },
            "self_sufficiency": {
                "description": "Being needs nothing outside itself",
                "reason": "There is nothing outside Being",
                "independence": "Being is complete in itself",
            },
            "present_perfection": {
                "description": "Being is complete now, not becoming so",
                "contrast": "Not a process but an achieved state",
                "mode": "Always already perfect",
            },
            "application": "What completeness or lack appears here?",
        }

    def _analyze_appearance_reality(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the distinction between appearance and reality.

        Parmenides inaugurates the fundamental distinction between
        how things appear and how they truly are.
        """
        return {
            "fundamental_distinction": {
                "appearance": "How things seem to mortals",
                "reality": "How things truly are (Being)",
                "gap": "These may be radically different",
            },
            "source_of_illusion": {
                "senses": "Eyes and ears report plurality and change",
                "habit": "Custom reinforces mortal opinions",
                "language": "Ordinary speech mixes being and non-being",
            },
            "discerning_reality": {
                "method": "Reason, not sensation",
                "criterion": "What can be thought without contradiction",
                "result": "Being as one, eternal, unchanging",
            },
            "status_of_appearances": {
                "question": "Are appearances nothing at all?",
                "difficulty": "Even appearances are something",
                "later_philosophy": "Plato's Forms address this problem",
            },
            "application": "What appears here, and what is truly real?",
        }

    def _derive_logical_analysis(self, prompt: str) -> Dict[str, Any]:
        """Extract logical principles from Parmenides's reasoning."""
        return {
            "principle_of_non_contradiction": {
                "statement": "Being cannot both be and not be",
                "role": "Foundational to the Way of Truth",
                "application": "Reject any thought that violates this",
            },
            "principle_of_sufficient_reason": {
                "implicit": "Why should Being arise at one time rather than another?",
                "answer": "It should not; therefore it is eternal",
                "application": "Changes require explanation; none is possible",
            },
            "ex_nihilo_rejection": {
                "statement": "Nothing comes from nothing",
                "application": "Being could not have arisen from non-being",
                "consequence": "Being is eternal",
            },
            "identity_of_thought_and_being": {
                "statement": "To think is to think of what is",
                "application": "Genuine thought tracks reality",
                "limit": "What cannot be thought cannot be",
            },
            "dialectical_method": {
                "description": "Consider the opposite and show it impossible",
                "application": "Non-being leads to absurdity",
                "conclusion": "Therefore only Being is",
            },
        }

    def _construct_reasoning(
        self,
        prompt: str,
        being: Dict,
        non_being: Dict,
        truth: Dict,
        opinion: Dict,
        monism: Dict,
        immutability: Dict,
        completeness: Dict,
        appearance_reality: Dict,
    ) -> str:
        """Construct comprehensive Parmenidean reasoning."""
        return f"""Eleatic Inquiry: "{prompt}"

THE WAY OF TRUTH
{truth['nature']['description']}. {truth['identity_of_thought_and_being']['thesis']}
{truth['rational_method']['principle']}

BEING IS
{being['fundamental_thesis']['statement']}. {being['fundamental_thesis']['necessity']}
Being is marked by these signs: {', '.join(being['signs_of_being']['list'][:3])}.

THE IMPOSSIBILITY OF NON-BEING
{non_being['impossibility']['statement']}. {non_being['unthinkability']['reason']}
{non_being['forbidden_path']['reason']}

THE UNITY OF BEING
{monism['thesis']['statement']}. {monism['continuity']['reason']}
{monism['homogeneity']['description']}

THE IMMUTABILITY OF BEING
{immutability['thesis']['statement']}. {immutability['no_generation']['statement']}
{immutability['eternal_present']['description']}

THE COMPLETENESS OF BEING
{completeness['thesis']['statement']}. {completeness['self_sufficiency']['reason']}
{being['sphere_metaphor']['description']}

APPEARANCE AND REALITY
{appearance_reality['fundamental_distinction']['gap']}
{opinion['mortal_errors']['senses']}
{appearance_reality['discerning_reality']['method']}

Thus reason declares: Being is one, eternal, unchanging, complete.
Change and plurality are the way of mortal opinion, not truth.
What appears to the senses must be judged by reason alone."""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Parmenides's philosophy reveals tension between appearance and
        reality, between what reason demands and what senses report.
        """
        tension_factors = []

        # Tension between appearance and reality
        appearance_reality = analysis["appearance_reality"]
        if appearance_reality.get("fundamental_distinction"):
            tension_factors.append(0.3)

        # Tension from challenge to common sense
        opinion = analysis["opinion"]
        if opinion.get("mortal_errors"):
            tension_factors.append(0.25)

        # Tension from immutability
        immutability = analysis["immutability"]
        if immutability.get("thesis"):
            tension_factors.append(0.2)

        # Tension from monism
        monism = analysis["monism"]
        if monism.get("against_plurality"):
            tension_factors.append(0.15)

        # Base metaphysical tension
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
