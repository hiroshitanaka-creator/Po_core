"""
Marcus Aurelius Philosopher Module

Implements Stoic philosophy based on Marcus Aurelius's Meditations.

Key concepts:
- Stoic Ethics: Virtue as the sole good
- Logos: Universal reason governing the cosmos
- Prohairesis: Faculty of choice/moral character
- Dichotomy of Control: What is "up to us" vs not
- Amor Fati: Love of fate, acceptance of events
- Cosmopolitanism: Universal human community
- Memento Mori: Awareness of mortality
- Present Moment: Focus on the now
- Indifferents: Things neither good nor bad in themselves
- Ataraxia: Tranquility of mind
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class MarcusAurelius(Philosopher):
    """
    Marcus Aurelius (121-180 CE)

    Roman Emperor and Stoic philosopher whose Meditations represent
    the practical application of Stoic philosophy to daily life.
    His thought emphasizes virtue, rational acceptance of fate,
    and the cultivation of inner tranquility through philosophical practice.
    """

    def __init__(self):
        super().__init__(
            name="Marcus Aurelius",
            description="Roman Emperor and Stoic philosopher, author of Meditations",
        )
        self.tradition = "Stoicism"
        self.key_concepts = [
            "virtue",
            "logos",
            "prohairesis",
            "dichotomy of control",
            "amor fati",
            "cosmopolitanism",
            "memento mori",
            "present moment",
            "indifferents",
            "ataraxia",
            "duty",
            "nature",
        ]

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Apply Stoic reasoning to the prompt.

        Returns analysis through the lens of virtue ethics, rational acceptance,
        and the cultivation of wisdom and tranquility.
        """
        analysis = self._analyze_stoic_wisdom(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Stoic Philosophy / Imperial Rome",
            "tension": tension,
            "virtue_analysis": analysis["virtue"],
            "dichotomy_of_control": analysis["control"],
            "logos_alignment": analysis["logos"],
            "prohairesis": analysis["prohairesis"],
            "amor_fati": analysis["amor_fati"],
            "memento_mori": analysis["memento_mori"],
            "cosmopolitan_view": analysis["cosmopolitanism"],
            "present_moment": analysis["present"],
            "indifferents": analysis["indifferents"],
            "ataraxia": analysis["ataraxia"],
            "practical_wisdom": analysis["practical_wisdom"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "stoic_meditation",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_stoic_wisdom(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Stoic analysis of the prompt."""
        virtue = self._analyze_virtue(prompt)
        control = self._analyze_dichotomy_of_control(prompt)
        logos = self._analyze_logos(prompt)
        prohairesis = self._analyze_prohairesis(prompt)
        amor_fati = self._analyze_amor_fati(prompt)
        memento_mori = self._analyze_memento_mori(prompt)
        cosmopolitanism = self._analyze_cosmopolitanism(prompt)
        present = self._analyze_present_moment(prompt)
        indifferents = self._analyze_indifferents(prompt)
        ataraxia = self._analyze_ataraxia(prompt)
        practical_wisdom = self._derive_practical_wisdom(prompt)

        reasoning = self._construct_reasoning(
            prompt, virtue, control, logos, prohairesis, amor_fati,
            memento_mori, cosmopolitanism, present, indifferents, ataraxia
        )

        return {
            "reasoning": reasoning,
            "virtue": virtue,
            "control": control,
            "logos": logos,
            "prohairesis": prohairesis,
            "amor_fati": amor_fati,
            "memento_mori": memento_mori,
            "cosmopolitanism": cosmopolitanism,
            "present": present,
            "indifferents": indifferents,
            "ataraxia": ataraxia,
            "practical_wisdom": practical_wisdom,
        }

    def _analyze_virtue(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the four cardinal virtues.

        The Stoics held that virtue is the sole good and vice the sole evil.
        The four cardinal virtues are:
        - Wisdom (sophia): Understanding what is truly good
        - Courage (andreia): Endurance of hardship for the good
        - Justice (dikaiosyne): Giving each their due
        - Temperance (sophrosyne): Moderation and self-control
        """
        return {
            "wisdom": {
                "description": "The knowledge of what is truly good, bad, and indifferent",
                "application": "What wisdom does this situation require?",
                "insight": "True wisdom lies in knowing that virtue alone is good",
            },
            "courage": {
                "description": "The endurance of pain and hardship for what is right",
                "application": "What fears must be faced? What must be endured?",
                "insight": "Courage is not absence of fear but right action despite it",
            },
            "justice": {
                "description": "Giving each person and thing their proper due",
                "application": "What obligations arise? Who is affected?",
                "insight": "We are members of one great city, the cosmos",
            },
            "temperance": {
                "description": "Moderation in desires and emotional responses",
                "application": "What passions require governance?",
                "insight": "The disciplined mind is free; the undisciplined is enslaved",
            },
            "unity": "The virtues are unified; one cannot truly possess one without all",
        }

    def _analyze_dichotomy_of_control(self, prompt: str) -> Dict[str, Any]:
        """
        Apply the fundamental Stoic distinction.

        Epictetus (Marcus's teacher through his writings) taught:
        'Some things are up to us (eph' hemin) and some are not.'
        This is the foundation of Stoic tranquility.
        """
        return {
            "up_to_us": {
                "description": "Our judgments, impulses, desires, aversions - our prohairesis",
                "examples": [
                    "Our interpretation of events",
                    "Our responses and reactions",
                    "Our values and commitments",
                    "Our efforts and intentions",
                ],
                "implication": "These alone are the proper focus of our concern",
            },
            "not_up_to_us": {
                "description": "Body, reputation, office, external outcomes",
                "examples": [
                    "Others' opinions and actions",
                    "Health and illness",
                    "Success and failure of projects",
                    "Life and death",
                ],
                "implication": "Concerning these, we should be indifferent",
            },
            "application": "What in this situation is truly within my control?",
            "wisdom": "Focus energy only on what is up to us; accept the rest",
            "common_errors": [
                "Believing externals are good or bad in themselves",
                "Trying to control what cannot be controlled",
                "Neglecting what is truly in our power",
            ],
        }

    def _analyze_logos(self, prompt: str) -> Dict[str, Any]:
        """
        Examine alignment with universal reason.

        For the Stoics, the cosmos is governed by divine reason (Logos).
        Living according to nature means living according to this
        rational order that permeates all things.
        """
        return {
            "cosmic_order": {
                "description": "The universe operates according to rational law",
                "implication": "Events unfold necessarily, governed by providence",
                "attitude": "What happens is part of the rational order",
            },
            "human_participation": {
                "description": "Human reason is a fragment of the cosmic logos",
                "implication": "We can understand and align with universal reason",
                "practice": "Use reason to perceive what accords with nature",
            },
            "living_according_to_nature": {
                "description": "Following both universal and human nature",
                "universal": "Accepting the cosmic order as it unfolds",
                "human": "Exercising our rational and social capacities",
            },
            "providence": "What seems evil may serve the good of the whole",
            "application": "How does this situation reflect the rational order?",
        }

    def _analyze_prohairesis(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the faculty of moral choice.

        Prohairesis is our capacity for choice, our moral character -
        the only thing that is truly our own and cannot be taken from us.
        It is the citadel of the self.
        """
        return {
            "nature": {
                "description": "The ruling faculty that makes us who we are",
                "function": "To judge impressions and choose responses",
                "sovereignty": "Nothing external can harm it without consent",
            },
            "cultivation": {
                "attention": "Watch the impressions that arise",
                "judgment": "Test them against reality and reason",
                "choice": "Assent only to true impressions",
            },
            "discipline": {
                "of_desire": "Desire only what is up to us",
                "of_action": "Act with reservation (hupexairesis)",
                "of_assent": "Withhold assent from unclear impressions",
            },
            "freedom": "True freedom is the proper use of prohairesis",
            "application": "What choice of character does this moment offer?",
        }

    def _analyze_amor_fati(self, prompt: str) -> Dict[str, Any]:
        """
        Explore the love of fate.

        Marcus teaches not merely acceptance but active embrace of
        whatever happens as part of the cosmic order.
        """
        return {
            "acceptance": {
                "description": "What happens could not have been otherwise",
                "basis": "Events flow from the causal order of nature",
                "practice": "Do not wish things were different",
            },
            "embrace": {
                "description": "Go beyond acceptance to welcoming",
                "insight": "What befalls us is woven into our fate",
                "practice": "Say yes to the present moment fully",
            },
            "transformation": {
                "description": "Use obstacles as material for virtue",
                "method": "The impediment to action advances action",
                "wisdom": "What stands in the way becomes the way",
            },
            "gratitude": "Even hardships are opportunities for growth",
            "application": "How can I embrace what is happening?",
        }

    def _analyze_memento_mori(self, prompt: str) -> Dict[str, Any]:
        """
        Contemplate mortality as philosophical practice.

        Marcus frequently reminded himself of death - not morbidly,
        but as a way to clarify values and motivate virtuous action.
        """
        return {
            "awareness": {
                "description": "Death may come at any moment",
                "practice": "Begin each day as if it might be your last",
                "effect": "Strips away trivialities, reveals essentials",
            },
            "perspective": {
                "description": "All things pass; empires and emperors alike",
                "insight": "Alexander and his mule driver both became dust",
                "wisdom": "Fame is smoke, bodies decay, memory fades",
            },
            "urgency": {
                "description": "Time is limited and precious",
                "implication": "Act virtuously now; there may be no later",
                "question": "If this were my last day, would I act thus?",
            },
            "equanimity": {
                "description": "Death is natural, not evil",
                "basis": "It is the dissolution of elements, a return to nature",
                "attitude": "Await it calmly as one of nature's operations",
            },
            "application": "How does mortality illuminate this situation?",
        }

    def _analyze_cosmopolitanism(self, prompt: str) -> Dict[str, Any]:
        """
        Consider the universal human community.

        Marcus saw himself as a citizen of the world-city (cosmopolis),
        bound by reason to all rational beings.
        """
        return {
            "universal_citizenship": {
                "description": "We are all citizens of one great city",
                "basis": "Shared reason unites all humans",
                "implication": "Duties extend to all humanity",
            },
            "social_nature": {
                "description": "Humans are made for cooperation",
                "image": "Like bees in a hive, we thrive together",
                "error": "Antisocial behavior is against nature",
            },
            "justice_to_all": {
                "description": "Even enemies deserve fair treatment",
                "practice": "Do not be disturbed by others' faults",
                "wisdom": "We are born for each other",
            },
            "common_good": {
                "description": "What benefits the whole benefits the part",
                "duty": "Work for the common good as emperor and as man",
                "priority": "The good of the rational community comes first",
            },
            "application": "How does this affect the broader human community?",
        }

    def _analyze_present_moment(self, prompt: str) -> Dict[str, Any]:
        """
        Focus on the present as the only reality.

        Marcus emphasized that only the present moment exists and
        is within our power. Past and future are beyond our reach.
        """
        return {
            "temporal_reality": {
                "description": "Only the present moment is real",
                "past": "Gone and unchangeable",
                "future": "Not yet and uncertain",
                "present": "The only point of contact with reality",
            },
            "duration": {
                "description": "Even the longest life is but a point in eternity",
                "insight": "What we lose at death is only the present moment",
                "equality": "In this sense, the longest and shortest lives are equal",
            },
            "attention": {
                "description": "Give full attention to the task at hand",
                "practice": "Do each act as if it were your last",
                "error": "Mind-wandering wastes the only time we have",
            },
            "power": {
                "description": "We can only act in the present",
                "implication": "All virtue is exercised now",
                "practice": "Make the present moment sufficient",
            },
            "application": "What does this present moment require?",
        }

    def _analyze_indifferents(self, prompt: str) -> Dict[str, Any]:
        """
        Examine things that are neither good nor bad in themselves.

        The Stoics taught that only virtue is good and only vice is bad.
        Everything else - health, wealth, reputation - is 'indifferent',
        though some indifferents are 'preferred' according to nature.
        """
        return {
            "doctrine": {
                "description": "Only virtue is good; only vice is bad",
                "implication": "Externals have no power over happiness",
                "basis": "The sage is happy even on the rack",
            },
            "preferred_indifferents": {
                "description": "Things naturally selected but not truly good",
                "examples": ["Health", "Wealth", "Reputation", "Life itself"],
                "status": "May be pursued but not as if essential to happiness",
            },
            "dispreferred_indifferents": {
                "description": "Things naturally avoided but not truly evil",
                "examples": ["Sickness", "Poverty", "Obscurity", "Death"],
                "status": "May be avoided but should not disturb equanimity",
            },
            "proper_use": {
                "description": "Indifferents are material for virtue",
                "insight": "How we handle them reveals character",
                "practice": "Use preferred indifferents virtuously; bear dispreferred well",
            },
            "application": "What externals am I mistaking for true goods or evils?",
        }

    def _analyze_ataraxia(self, prompt: str) -> Dict[str, Any]:
        """
        Consider the goal of tranquility.

        The Stoic sage achieves ataraxia - freedom from disturbance -
        through proper use of reason and acceptance of nature.
        """
        return {
            "nature": {
                "description": "Unperturbedness, tranquility of soul",
                "basis": "Comes from correct judgments about what matters",
                "manifestation": "Calm amid any circumstance",
            },
            "sources_of_disturbance": {
                "false_judgments": "Believing externals are good or evil",
                "irrational_passions": "Excessive desires and fears",
                "fighting_fate": "Resisting what cannot be changed",
            },
            "cultivation": {
                "judgment": "Test impressions before assenting",
                "acceptance": "Welcome what happens as part of nature",
                "focus": "Attend only to what is up to us",
            },
            "inner_citadel": {
                "description": "The mind retreats into itself",
                "method": "Nothing external can harm the ruling faculty",
                "practice": "Maintain tranquility within regardless of without",
            },
            "application": "What disturbs my tranquility here? Is the judgment correct?",
        }

    def _derive_practical_wisdom(self, prompt: str) -> Dict[str, Any]:
        """
        Extract practical guidance for action.

        Marcus's Meditations are practical exercises, not abstract theory.
        He sought not just understanding but transformation.
        """
        return {
            "morning_meditation": {
                "practice": "Prepare for the day's challenges",
                "expectation": "You will meet difficult people",
                "attitude": "They act from ignorance; do not be disturbed",
            },
            "evening_examination": {
                "practice": "Review the day's actions",
                "questions": "Where did I go wrong? What was left undone?",
                "purpose": "Self-correction and growth",
            },
            "view_from_above": {
                "practice": "See events from cosmic perspective",
                "effect": "Human affairs appear small",
                "wisdom": "This too shall pass",
            },
            "reserve_clause": {
                "practice": "Undertake actions 'with reservation'",
                "formula": "I will do X, fate permitting",
                "protection": "Prepares for disappointment without attachment",
            },
            "philosophical_exercises": [
                "Remind yourself what is up to you",
                "Practice negative visualization",
                "Consider impermanence",
                "Recall that you are part of nature",
            ],
        }

    def _construct_reasoning(
        self, prompt: str, virtue: Dict, control: Dict, logos: Dict,
        prohairesis: Dict, amor_fati: Dict, memento_mori: Dict,
        cosmopolitanism: Dict, present: Dict, indifferents: Dict, ataraxia: Dict
    ) -> str:
        """Construct comprehensive Stoic reasoning."""
        return f"""Stoic Meditation on: "{prompt}"

DICHOTOMY OF CONTROL
First, we must distinguish what is up to us from what is not.
{control['up_to_us']['description']}. In this situation, I must identify
what is truly within my power - my judgments, choices, and responses -
and release attachment to external outcomes.

VIRTUE AS THE SOLE GOOD
{virtue['wisdom']['description']}. The question is not what will happen,
but how I will respond with virtue. {virtue['unity']}

ALIGNMENT WITH LOGOS
{logos['cosmic_order']['description']}. Whatever happens is part of
the rational order of the universe. {logos['living_according_to_nature']['universal']}

THE RULING FACULTY
{prohairesis['nature']['description']}. Nothing external can harm my
prohairesis without my consent. The discipline of assent, desire, and
action protects the inner citadel.

AMOR FATI
{amor_fati['transformation']['description']}. {amor_fati['transformation']['wisdom']}
Whatever obstacle appears becomes material for virtue.

MEMENTO MORI
{memento_mori['awareness']['description']}. If this were my last day,
how would I act? This awareness strips away the trivial and reveals
what truly matters.

COSMOPOLITAN PERSPECTIVE
{cosmopolitanism['universal_citizenship']['description']}. My actions
affect the whole human community. {cosmopolitanism['social_nature']['description']}

THE PRESENT MOMENT
{present['temporal_reality']['description']}. All power and virtue
exist only in this moment. What does the present require of me?

REGARDING INDIFFERENTS
{indifferents['doctrine']['description']}. I must not mistake externals
for true goods or evils. They are material for demonstrating character.

PATH TO ATARAXIA
{ataraxia['nature']['description']}. Through right judgment and
acceptance of nature, the soul finds its proper tranquility.
{ataraxia['inner_citadel']['description']}

Thus reason and nature counsel: Focus on virtue, accept what comes,
act for the common good, and maintain the inner citadel of tranquility."""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Stoicism emphasizes resolution of tension through acceptance.
        Higher tension indicates areas requiring Stoic practice.
        """
        tension_factors = []

        # Tension from control issues
        control = analysis["control"]
        if control.get("common_errors"):
            tension_factors.append(0.3)

        # Tension from disturbed ataraxia
        ataraxia = analysis["ataraxia"]
        if ataraxia.get("sources_of_disturbance"):
            tension_factors.append(0.25)

        # Tension from mortality awareness
        memento_mori = analysis["memento_mori"]
        if memento_mori.get("urgency"):
            tension_factors.append(0.2)

        # Tension from indifferent confusion
        indifferents = analysis["indifferents"]
        if indifferents.get("application"):
            tension_factors.append(0.15)

        # Base tension from human condition
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
