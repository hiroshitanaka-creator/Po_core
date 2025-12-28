"""
Hans Jonas Philosopher Module

Implements responsibility ethics based on Jonas's philosophy.

Key concepts:
- Imperative of Responsibility: Ethics for technological age
- Future Generations: Obligation to those not yet born
- Heuristics of Fear: Fear as guide to responsibility
- Technology Ethics: Critique of technological power
- Life and Organism: Phenomenology of the living
- Metabolism: Life as self-maintaining process
- Gnosticism Studies: Ancient religious thought
- Being and Ought: Grounding ethics in ontology
- Vulnerability: Protection of vulnerable existence
- Ecological Ethics: Responsibility for nature
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Jonas(Philosopher):
    """
    Hans Jonas (1903-1993)

    German-American philosopher known for his ethics of responsibility,
    particularly regarding technology and future generations. His work
    bridges phenomenology, environmental ethics, and philosophy of biology,
    arguing that technological power requires a new ethics of responsibility.
    """

    def __init__(self):
        super().__init__(
            name="Hans Jonas",
            tradition="Phenomenology / Ethics of Responsibility",
            key_concepts=[
                "imperative of responsibility",
                "future generations",
                "heuristics of fear",
                "technology ethics",
                "life and organism",
                "metabolism",
                "being and ought",
                "vulnerability",
                "ecological ethics",
                "precautionary principle",
                "human dignity",
                "preservation",
            ],
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Apply Jonas's responsibility ethics to the prompt.

        Returns analysis through the lens of responsibility for future
        generations, technological critique, and the preservation of life.
        """
        analysis = self._analyze_jonas(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Ethics of Responsibility / Phenomenology of Life",
            "tension": tension,
            "responsibility": analysis["responsibility"],
            "future_generations": analysis["future"],
            "heuristics_of_fear": analysis["fear"],
            "technology": analysis["technology"],
            "life_analysis": analysis["life"],
            "being_and_ought": analysis["ontological_ethics"],
            "vulnerability": analysis["vulnerability"],
            "ecological": analysis["ecological"],
            "practical_guidance": analysis["practical"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "responsibility_analysis",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_jonas(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Jonas analysis of the prompt."""
        responsibility = self._analyze_responsibility(prompt)
        future = self._analyze_future_generations(prompt)
        fear = self._analyze_heuristics_of_fear(prompt)
        technology = self._analyze_technology(prompt)
        life = self._analyze_life(prompt)
        ontological_ethics = self._analyze_being_and_ought(prompt)
        vulnerability = self._analyze_vulnerability(prompt)
        ecological = self._analyze_ecological_ethics(prompt)
        practical = self._derive_practical_guidance(prompt)

        reasoning = self._construct_reasoning(
            prompt, responsibility, future, fear, technology,
            life, ontological_ethics, vulnerability, ecological
        )

        return {
            "reasoning": reasoning,
            "responsibility": responsibility,
            "future": future,
            "fear": fear,
            "technology": technology,
            "life": life,
            "ontological_ethics": ontological_ethics,
            "vulnerability": vulnerability,
            "ecological": ecological,
            "practical": practical,
        }

    def _analyze_responsibility(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the imperative of responsibility.

        Jonas formulated a new categorical imperative for the
        technological age: "Act so that the effects of your action
        are compatible with the permanence of genuine human life."
        """
        return {
            "new_imperative": {
                "formulation": "Act so that effects are compatible with permanence of human life",
                "contrast_kant": "Not formal universalizability but material preservation",
                "scope": "Includes future generations and nature itself",
            },
            "nature_of_responsibility": {
                "asymmetrical": "Responsibility for the vulnerable who cannot reciprocate",
                "non_reciprocal": "Like parent for child, not contract between equals",
                "continuous": "An ongoing obligation, not discrete acts",
            },
            "paradigm": {
                "parent_child": "The model of responsibility for the vulnerable",
                "statesman": "Responsibility for political community and future",
                "quality": "Total, continuous, non-reciprocal care",
            },
            "collective": {
                "description": "Responsibility extends to collective action",
                "politics": "We are responsible for institutions and systems",
                "humanity": "Humanity as a whole bears responsibility for Earth",
            },
            "application": "What responsibility arises from this situation?",
        }

    def _analyze_future_generations(self, prompt: str) -> Dict[str, Any]:
        """
        Examine obligations to those not yet born.

        Jonas argues we have genuine obligations to future generations,
        even though they do not yet exist to make claims on us.
        """
        return {
            "existence_of_obligation": {
                "problem": "How can we owe anything to those who don't exist?",
                "answer": "The idea of humanity includes its futurity",
                "ground": "Humanity's continued existence is a primary good",
            },
            "content_of_obligation": {
                "preservation": "Ensure humanity can continue to exist",
                "quality": "Preserve conditions for genuine human life",
                "openness": "Keep future possibilities open",
            },
            "priority": {
                "principle": "Duties to future may override present interests",
                "reasoning": "Future generations are more vulnerable than present",
                "caution": "We can harm them; they cannot defend themselves",
            },
            "what_we_owe": {
                "existence": "A world in which humans can live",
                "quality": "Conditions for authentic human existence",
                "freedom": "Open possibilities, not foreclosed futures",
            },
            "application": "How does this affect future generations?",
        }

    def _analyze_heuristics_of_fear(self, prompt: str) -> Dict[str, Any]:
        """
        Apply fear as a guide to responsibility.

        Jonas argues that fear of possible catastrophe, not hope,
        should guide our response to technological power.
        """
        return {
            "role_of_fear": {
                "description": "Fear reveals what we truly value",
                "function": "Imagining worst outcomes clarifies responsibility",
                "legitimacy": "Fear is appropriate response to genuine danger",
            },
            "epistemological_function": {
                "description": "We know good through imagining its loss",
                "method": "Project possible disasters to understand stakes",
                "wisdom": "Bad outcomes are more knowable than good ones",
            },
            "primacy_of_bad_prognosis": {
                "principle": "Give more weight to dire predictions",
                "reasoning": "Error toward caution is less costly than error toward risk",
                "application": "When uncertain, assume the worse possibility",
            },
            "against_utopianism": {
                "critique": "Utopian hopes have justified terrible means",
                "alternative": "Responsibility requires sobriety, not optimism",
                "wisdom": "Preserve what we have before gambling for more",
            },
            "application": "What catastrophic possibilities should guide us here?",
        }

    def _analyze_technology(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the ethical challenges of technological power.

        Jonas argues that modern technology has fundamentally changed
        the human condition, requiring a new ethics adequate to our powers.
        """
        return {
            "changed_condition": {
                "description": "Technology has made humanity powerful enough to destroy itself",
                "novelty": "Previous ethics assumed nature's permanence",
                "challenge": "Our power now reaches future generations and global nature",
            },
            "characteristics": {
                "cumulative": "Effects accumulate over time",
                "irreversible": "Some changes cannot be undone",
                "global": "Impacts extend across the planet",
                "trans_generational": "Consequences extend to future generations",
            },
            "inadequacy_of_old_ethics": {
                "traditional": "Ethics focused on immediate human relations",
                "limitation": "Nature was backdrop, not object of responsibility",
                "need": "A new ethics commensurate with our new powers",
            },
            "technological_imperative": {
                "critique": "The view that we must do what we can do",
                "rejection": "Capability does not imply permission",
                "alternative": "Power demands responsibility, not exercise",
            },
            "application": "What technological powers and responsibilities are at stake?",
        }

    def _analyze_life(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the phenomenology of living organisms.

        Jonas developed a philosophical biology showing life as
        self-maintaining, self-transcending activity.
        """
        return {
            "metabolism": {
                "description": "Life maintains itself through material exchange",
                "paradox": "The organism remains itself while constantly changing",
                "significance": "Life is the first instance of value in the universe",
            },
            "needful_freedom": {
                "description": "Life is free but dependent on world",
                "tension": "Independence requires dependence on environment",
                "value": "Need creates interest, interest creates value",
            },
            "levels_of_life": {
                "plant": "Metabolism without perception",
                "animal": "Perception, emotion, movement",
                "human": "Reflection, freedom, responsibility",
            },
            "teleology": {
                "description": "Life is purposive, goal-directed",
                "ontological": "Purpose is real, not merely attributed",
                "implication": "Nature itself embodies value",
            },
            "application": "What forms of life are affected here?",
        }

    def _analyze_being_and_ought(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the grounding of ethics in ontology.

        Jonas attempts to derive ought from is, grounding ethics
        in the being of life itself.
        """
        return {
            "overcoming_dualism": {
                "problem": "Modern thought separated facts from values",
                "consequence": "Ethics became groundless, merely subjective",
                "project": "Restore unity of being and value",
            },
            "life_as_value": {
                "claim": "Life itself embodies a 'yes' to existence",
                "evidence": "Every organism strives to continue existing",
                "implication": "Being is inherently valuable",
            },
            "the_ought_in_being": {
                "argument": "From the fact of life follows an ought to preserve it",
                "ground": "Nature's purposiveness grounds moral obligation",
                "responsibility": "We who can destroy are obligated to preserve",
            },
            "humanity_as_trustee": {
                "description": "Humanity bears unique responsibility",
                "reason": "Only we can reflect on and choose to preserve",
                "obligation": "Power to destroy entails duty to preserve",
            },
            "application": "What ontological grounds for ethics are relevant?",
        }

    def _analyze_vulnerability(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the ethics of protecting the vulnerable.

        Responsibility arises in response to vulnerability -
        the vulnerable call forth our care.
        """
        return {
            "vulnerability_and_responsibility": {
                "description": "The vulnerable call forth responsibility",
                "model": "The infant's face demands care",
                "extension": "Future generations are maximally vulnerable to us",
            },
            "non_reciprocity": {
                "description": "We cannot expect return from the vulnerable",
                "difference": "Not contract but gift of care",
                "asymmetry": "The powerful owe the powerless",
            },
            "nature_as_vulnerable": {
                "description": "Nature has become vulnerable to human power",
                "novelty": "Previously nature was the given backdrop",
                "responsibility": "We must now care for nature itself",
            },
            "preservation": {
                "imperative": "Protect vulnerable existence",
                "scope": "Extends to all living beings",
                "limit": "Our power defines our responsibility",
            },
            "application": "What vulnerability requires protection here?",
        }

    def _analyze_ecological_ethics(self, prompt: str) -> Dict[str, Any]:
        """
        Examine responsibility for the natural world.

        Jonas extends ethics to include nature itself as an
        object of moral responsibility.
        """
        return {
            "nature_as_end": {
                "description": "Nature has intrinsic value, not just instrumental",
                "ground": "Life itself embodies value and purpose",
                "implication": "We are responsible for nature's preservation",
            },
            "holistic_responsibility": {
                "scope": "Ecosystems, species, the biosphere",
                "inclusion": "Non-human life deserves moral consideration",
                "stewardship": "Humanity as trustee, not master",
            },
            "limits_to_intervention": {
                "principle": "Not everything possible should be done",
                "caution": "Nature's complexity exceeds our understanding",
                "humility": "Respect for what we cannot control",
            },
            "sustainable_existence": {
                "goal": "Human life compatible with nature's permanence",
                "requirement": "Live within ecological limits",
                "obligation": "Preserve conditions for all life",
            },
            "application": "What ecological responsibilities arise here?",
        }

    def _derive_practical_guidance(self, prompt: str) -> Dict[str, Any]:
        """Extract practical guidance from Jonas's framework."""
        return {
            "precautionary_principle": {
                "description": "When in doubt, err on the side of caution",
                "application": "Potential catastrophes require preventive action",
                "wisdom": "Better to forgo possible benefits than risk disaster",
            },
            "decision_making": {
                "consider_future": "Include future generations in calculations",
                "consider_nature": "Nature has standing in moral deliberation",
                "consider_catastrophe": "What is the worst that could happen?",
            },
            "institutional": {
                "need": "Institutions that embody long-term responsibility",
                "challenge": "Politics favors short-term thinking",
                "requirement": "Structures that represent future interests",
            },
            "personal_ethics": {
                "modesty": "Restrain desires and expectations",
                "preservation": "Value what exists over imagined improvements",
                "responsibility": "Accept personal role in collective responsibility",
            },
        }

    def _construct_reasoning(
        self, prompt: str, responsibility: Dict, future: Dict, fear: Dict,
        technology: Dict, life: Dict, ontological_ethics: Dict,
        vulnerability: Dict, ecological: Dict
    ) -> str:
        """Construct comprehensive Jonas reasoning."""
        return f"""Analysis through Jonas's Ethics of Responsibility: "{prompt}"

THE IMPERATIVE OF RESPONSIBILITY
{responsibility['new_imperative']['formulation']}. {responsibility['new_imperative']['scope']}
Our technological power demands an ethics commensurate with our capacity to affect the future.

FUTURE GENERATIONS
{future['existence_of_obligation']['ground']}. {future['content_of_obligation']['preservation']}
We bear responsibility for those not yet born who cannot speak for themselves.

HEURISTICS OF FEAR
{fear['role_of_fear']['function']}. {fear['primacy_of_bad_prognosis']['principle']}
When the stakes are existential, caution is wisdom.

TECHNOLOGY AND POWER
{technology['changed_condition']['description']}. {technology['characteristics']['irreversible']}
The novelty of our power requires a new kind of ethical thinking.

THE PHENOMENOLOGY OF LIFE
{life['metabolism']['description']}. {life['needful_freedom']['tension']}
Life itself embodies value and purposiveness.

BEING AND OUGHT
{ontological_ethics['life_as_value']['claim']}. {ontological_ethics['the_ought_in_being']['argument']}
Ethics is grounded in the being of life itself.

VULNERABILITY AND CARE
{vulnerability['vulnerability_and_responsibility']['description']}.
{vulnerability['nature_as_vulnerable']['description']}. {vulnerability['nature_as_vulnerable']['responsibility']}

ECOLOGICAL RESPONSIBILITY
{ecological['nature_as_end']['description']}. {ecological['holistic_responsibility']['stewardship']}
{ecological['sustainable_existence']['goal']}

Thus the imperative of responsibility demands: preserve the conditions for
genuine human life and the integrity of nature for all time to come."""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Jonas's ethics involves the tension between present interests
        and future obligations, between power and responsibility.
        """
        tension_factors = []

        # Tension from future obligations
        future = analysis["future"]
        if future.get("priority"):
            tension_factors.append(0.25)

        # Tension from technological power
        technology = analysis["technology"]
        if technology.get("changed_condition"):
            tension_factors.append(0.25)

        # Tension from vulnerability
        vulnerability = analysis["vulnerability"]
        if vulnerability.get("non_reciprocity"):
            tension_factors.append(0.2)

        # Tension from ecological demands
        ecological = analysis["ecological"]
        if ecological.get("limits_to_intervention"):
            tension_factors.append(0.15)

        # Base existential tension
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
