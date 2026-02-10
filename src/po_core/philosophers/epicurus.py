"""
Epicurus Philosopher Module

Implements Epicurean philosophy based on Epicurus's teachings.

Key concepts:
- Ataraxia: Tranquility, freedom from mental disturbance
- Aponia: Freedom from bodily pain
- Hedonism: Pleasure as the highest good (properly understood)
- Tetrapharmakos: The four-part remedy
- Katastematic vs Kinetic Pleasure: Static vs active pleasure
- Natural and Necessary Desires: Classification of desires
- Atomism: Material basis of reality
- Mortality: Death as non-existence
- Friendship: Essential for the good life
- The Garden: Community of philosophical friends
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Epicurus(Philosopher):
    """
    Epicurus (341-270 BCE)

    Greek philosopher who founded Epicureanism, teaching that
    pleasure (properly understood as tranquility and freedom from pain)
    is the highest good. He established the Garden, a community
    of friends devoted to philosophical living.
    """

    def __init__(self):
        super().__init__(
            name="Epicurus",
            description="Greek philosopher who founded Epicureanism, teaching pleasure as the highest good",
        )
        self.tradition = "Epicureanism"
        self.key_concepts = [
            "ataraxia",
            "aponia",
            "pleasure",
            "tetrapharmakos",
            "katastematic pleasure",
            "kinetic pleasure",
            "natural desires",
            "atomism",
            "mortality",
            "friendship",
            "the garden",
            "prudence",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Apply Epicurean reasoning to the prompt.

        Returns analysis through the lens of pleasure ethics,
        rational fear elimination, and the cultivation of ataraxia.
        """
        analysis = self._analyze_epicurean(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Epicurean Philosophy / The Garden",
            "tension": tension,
            "pleasure_analysis": analysis["pleasure"],
            "desire_classification": analysis["desires"],
            "tetrapharmakos": analysis["tetrapharmakos"],
            "ataraxia": analysis["ataraxia"],
            "aponia": analysis["aponia"],
            "mortality": analysis["mortality"],
            "friendship": analysis["friendship"],
            "prudence": analysis["prudence"],
            "atomism": analysis["atomism"],
            "practical_guidance": analysis["practical"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "epicurean_calculus",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_epicurean(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Epicurean analysis of the prompt."""
        pleasure = self._analyze_pleasure(prompt)
        desires = self._classify_desires(prompt)
        tetrapharmakos = self._apply_tetrapharmakos(prompt)
        ataraxia = self._analyze_ataraxia(prompt)
        aponia = self._analyze_aponia(prompt)
        mortality = self._analyze_mortality(prompt)
        friendship = self._analyze_friendship(prompt)
        prudence = self._analyze_prudence(prompt)
        atomism = self._analyze_atomism(prompt)
        practical = self._derive_practical_guidance(prompt)

        reasoning = self._construct_reasoning(
            prompt,
            pleasure,
            desires,
            tetrapharmakos,
            ataraxia,
            aponia,
            mortality,
            friendship,
            prudence,
        )

        return {
            "reasoning": reasoning,
            "pleasure": pleasure,
            "desires": desires,
            "tetrapharmakos": tetrapharmakos,
            "ataraxia": ataraxia,
            "aponia": aponia,
            "mortality": mortality,
            "friendship": friendship,
            "prudence": prudence,
            "atomism": atomism,
            "practical": practical,
        }

    def _analyze_pleasure(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the Epicurean understanding of pleasure.

        Epicurus taught that pleasure (hedone) is the highest good,
        but this must be understood as tranquility and freedom from
        disturbance, not sensual indulgence.
        """
        return {
            "nature_of_pleasure": {
                "definition": "The absence of pain and disturbance",
                "misconception": "Epicurean pleasure is not indulgence or excess",
                "truth": "The highest pleasure is peaceful contentment",
            },
            "katastematic_pleasure": {
                "description": "Static pleasure - the stable state of well-being",
                "examples": [
                    "Tranquility of mind",
                    "Freedom from bodily pain",
                    "Contentment",
                ],
                "priority": "This is the highest form of pleasure",
            },
            "kinetic_pleasure": {
                "description": "Active pleasure - the process of satisfying desire",
                "examples": ["Eating when hungry", "Drinking when thirsty", "Joy"],
                "limitation": "Valuable but not the goal itself",
            },
            "pleasure_ceiling": {
                "description": "Pleasure cannot increase beyond the removal of pain",
                "implication": "Simple satisfactions equal elaborate ones",
                "wisdom": "Luxury adds nothing essential",
            },
            "application": "What is the nature of pleasure or pain involved here?",
        }

    def _classify_desires(self, prompt: str) -> Dict[str, Any]:
        """
        Apply the Epicurean classification of desires.

        Epicurus divided desires into natural/unnatural and
        necessary/unnecessary to guide wise choice.
        """
        return {
            "natural_and_necessary": {
                "description": "Essential for life, happiness, and bodily ease",
                "examples": [
                    "Food and water for survival",
                    "Shelter from elements",
                    "Friendship for happiness",
                    "Philosophy for wisdom",
                ],
                "guidance": "These should be fulfilled",
            },
            "natural_but_unnecessary": {
                "description": "Natural but not essential",
                "examples": [
                    "Gourmet food (vs simple food)",
                    "Sexual pleasure",
                    "Pleasant conversation",
                    "Aesthetic enjoyment",
                ],
                "guidance": "Enjoy when available but don't depend on them",
            },
            "unnatural_and_unnecessary": {
                "description": "Based on empty opinions, never truly satisfied",
                "examples": [
                    "Wealth beyond need",
                    "Political power",
                    "Fame and glory",
                    "Immortality",
                ],
                "guidance": "These should be eliminated as sources of disturbance",
            },
            "wisdom": "Understand the nature of your desires before pursuing them",
            "application": "What category of desire is operating here?",
        }

    def _apply_tetrapharmakos(self, prompt: str) -> Dict[str, Any]:
        """
        Apply the four-part remedy for a good life.

        The Tetrapharmakos summarizes Epicurean teaching in four maxims
        designed to eliminate the main sources of human anxiety.
        """
        return {
            "god_not_feared": {
                "maxim": "God is not to be feared",
                "explanation": "The gods exist in perfect blessedness and do not intervene",
                "liberation": "No divine punishment awaits; no divine favor is needed",
                "implication": "Live without religious anxiety",
            },
            "death_not_felt": {
                "maxim": "Death is not felt",
                "explanation": "Where death is, I am not; where I am, death is not",
                "liberation": "Death is merely the end of sensation",
                "implication": "Fear of death is irrational",
            },
            "good_easily_obtained": {
                "maxim": "The good is easy to obtain",
                "explanation": "What we truly need is simple and accessible",
                "liberation": "Happiness does not require wealth or power",
                "implication": "Live simply and contentedly",
            },
            "evil_easily_endured": {
                "maxim": "The bad is easy to endure",
                "explanation": "Intense pain is brief; chronic pain is bearable",
                "liberation": "Pain need not overwhelm us",
                "implication": "Even suffering can be managed",
            },
            "application": "Which of these remedies applies to the current situation?",
        }

    def _analyze_ataraxia(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the goal of mental tranquility.

        Ataraxia (freedom from disturbance) is the highest mental good,
        achieved through philosophy and proper understanding.
        """
        return {
            "nature": {
                "description": "Untroubled, undisturbed state of mind",
                "contrast": "Opposite of anxiety, worry, fear",
                "goal": "The mental component of happiness",
            },
            "sources_of_disturbance": {
                "fear_of_gods": "Anxiety about divine punishment",
                "fear_of_death": "Terror of non-existence",
                "desire_for_excess": "Craving what is unnecessary",
                "pain_avoidance": "Excessive fear of suffering",
            },
            "path_to_tranquility": {
                "study": "Understand nature through philosophy",
                "community": "Live among philosophical friends",
                "simplicity": "Reduce desires to what is natural and necessary",
                "withdrawal": "Avoid politics and public life",
            },
            "lathe_biosas": {
                "maxim": "Live hidden",
                "meaning": "Avoid public prominence and its troubles",
                "wisdom": "A quiet life is a happy life",
            },
            "application": "What is disturbing tranquility here?",
        }

    def _analyze_aponia(self, prompt: str) -> Dict[str, Any]:
        """
        Examine freedom from bodily pain.

        Aponia is the bodily counterpart to ataraxia,
        the physical component of well-being.
        """
        return {
            "nature": {
                "description": "Absence of bodily pain",
                "relation": "The bodily good corresponding to mental tranquility",
                "sufficiency": "When achieved, cannot be increased, only varied",
            },
            "management_of_pain": {
                "acute_pain": "Intense pains are brief",
                "chronic_pain": "Lasting pains are bearable",
                "memory": "Pleasant memories can counterbalance pain",
                "anticipation": "Pleasant anticipations likewise help",
            },
            "bodily_needs": {
                "simplicity": "The body needs little for satisfaction",
                "accessibility": "Natural needs are easily met",
                "contentment": "Simple fare satisfies as well as luxury",
            },
            "wisdom": "Attend to the body's true needs, not its whims",
            "application": "What bodily concerns are relevant here?",
        }

    def _analyze_mortality(self, prompt: str) -> Dict[str, Any]:
        """
        Apply Epicurean arguments about death.

        Epicurus argued that death should not be feared because
        it is simply non-existence, not a harm to the one who dies.
        """
        return {
            "nature_of_death": {
                "description": "The cessation of sensation",
                "materialism": "Soul atoms disperse at death",
                "implication": "There is no afterlife experience",
            },
            "symmetry_argument": {
                "description": "Post-death is like pre-birth",
                "reasoning": "We were not troubled by not existing before birth",
                "conclusion": "We should not be troubled by not existing after death",
            },
            "epicurus_argument": {
                "description": "Death is nothing to us",
                "reasoning": "Good and evil require sensation; death is no sensation",
                "conclusion": "Death cannot be good or evil for the dead person",
            },
            "liberation": {
                "from_fear": "Understanding death removes its terror",
                "for_life": "A life free of death-fear is fully livable",
                "wisdom": "Not immortality but freedom from fearing mortality",
            },
            "application": "How does mortality bear on this situation?",
        }

    def _analyze_friendship(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the role of friendship in the good life.

        For Epicurus, friendship (philia) was essential to happiness,
        and the Garden was a community of friends.
        """
        return {
            "centrality": {
                "claim": "Of all wisdom's provisions, friendship is greatest",
                "reason": "Friendship provides security and pleasure",
                "necessity": "The happy life requires friends",
            },
            "nature_of_friendship": {
                "origin": "Friendship begins from utility",
                "transcendence": "But becomes loved for itself",
                "mutuality": "True friends value each other equally",
            },
            "the_garden": {
                "description": "Epicurus's philosophical community",
                "character": "Friends living and philosophizing together",
                "inclusivity": "Open to women, slaves, and all seekers",
            },
            "benefits": {
                "security": "Friends protect and support each other",
                "pleasure": "Companionship is itself pleasurable",
                "philosophy": "Friends help each other toward wisdom",
            },
            "application": "What role does friendship or community play here?",
        }

    def _analyze_prudence(self, prompt: str) -> Dict[str, Any]:
        """
        Examine practical wisdom in choosing pleasures.

        Prudence (phronesis) is central to Epicurean ethics,
        enabling wise calculation of pleasures and pains.
        """
        return {
            "centrality": {
                "claim": "Prudence is the greatest good, source of all virtues",
                "function": "Enables correct choice among pleasures and pains",
                "relation": "From prudence spring all other virtues",
            },
            "hedonistic_calculus": {
                "description": "Weighing pleasures and pains of actions",
                "considerations": [
                    "Intensity of pleasure or pain",
                    "Duration",
                    "Certainty",
                    "Nearness",
                    "Consequences",
                ],
                "wisdom": "Sometimes reject pleasure for greater good; accept pain for less evil",
            },
            "long_term_thinking": {
                "description": "Consider future consequences, not just immediate feeling",
                "example": "Forgo feast that will cause sickness",
                "principle": "The prudent person sees the whole picture",
            },
            "self_sufficiency": {
                "description": "Reduce dependence on external goods",
                "method": "Practice enjoying simple things",
                "benefit": "Freedom from fortune's changes",
            },
            "application": "What does prudent calculation suggest here?",
        }

    def _analyze_atomism(self, prompt: str) -> Dict[str, Any]:
        """
        Consider the atomic basis of Epicurean philosophy.

        Epicurus adopted atomic theory as the foundation of his
        natural philosophy, which supports his ethical conclusions.
        """
        return {
            "basic_theory": {
                "atoms": "Eternal, indivisible particles",
                "void": "Empty space allowing motion",
                "combinations": "All things are atomic arrangements",
            },
            "the_swerve": {
                "description": "Atoms occasionally deviate from straight fall",
                "function": "Explains how atoms combine",
                "implication": "Provides basis for free will",
            },
            "ethical_implications": {
                "no_divine_creation": "The world arose by natural processes",
                "mortality_of_soul": "Soul atoms disperse at death",
                "nature_of_gods": "Gods too are atomic, dwelling in intermundia",
            },
            "epistemology": {
                "sensations": "Caused by atomic effluences",
                "reliability": "Sensations themselves never lie",
                "error": "Error comes from judgment about sensations",
            },
            "application": "How does material understanding illuminate this?",
        }

    def _derive_practical_guidance(self, prompt: str) -> Dict[str, Any]:
        """Extract practical guidance from Epicurean wisdom."""
        return {
            "for_daily_life": [
                "Pursue simple pleasures; avoid unnecessary complications",
                "Cultivate friendships; withdraw from public strife",
                "Study philosophy to dissolve irrational fears",
                "Enjoy what you have; don't crave what you lack",
            ],
            "for_disturbances": [
                "Apply the Tetrapharmakos to current fears",
                "Recall that pain is either brief or bearable",
                "Remember that simple needs are easily met",
                "Seek the company and counsel of friends",
            ],
            "for_choices": [
                "Classify the desire: natural/necessary?",
                "Calculate long-term pleasure and pain",
                "Prefer stable contentment over fleeting excitement",
                "Choose what promotes ataraxia and aponia",
            ],
            "maxims": [
                "It is better to be unhappy rationally than happy irrationally",
                "Natural wealth has limits and is easy to obtain",
                "He who is not satisfied with little is satisfied with nothing",
                "The wise person does not fear death",
            ],
        }

    def _construct_reasoning(
        self,
        prompt: str,
        pleasure: Dict,
        desires: Dict,
        tetrapharmakos: Dict,
        ataraxia: Dict,
        aponia: Dict,
        mortality: Dict,
        friendship: Dict,
        prudence: Dict,
    ) -> str:
        """Construct comprehensive Epicurean reasoning."""
        return f"""Epicurean Analysis of: "{prompt}"

THE NATURE OF PLEASURE
{pleasure['nature_of_pleasure']['definition']}. True pleasure is not excess or
indulgence but the stable condition of well-being - what Epicurus calls
katastematic pleasure. {pleasure['katastematic_pleasure']['priority']}

CLASSIFICATION OF DESIRES
We must distinguish what we desire:
- Natural and necessary: {desires['natural_and_necessary']['description']}
- Natural but unnecessary: {desires['natural_but_unnecessary']['description']}
- Unnatural and unnecessary: {desires['unnatural_and_unnecessary']['description']}
{desires['wisdom']}

THE FOUR-PART REMEDY
The Tetrapharmakos addresses our deepest fears:
1. {tetrapharmakos['god_not_feared']['maxim']}: {tetrapharmakos['god_not_feared']['explanation']}
2. {tetrapharmakos['death_not_felt']['maxim']}: {tetrapharmakos['death_not_felt']['explanation']}
3. {tetrapharmakos['good_easily_obtained']['maxim']}: {tetrapharmakos['good_easily_obtained']['explanation']}
4. {tetrapharmakos['evil_easily_endured']['maxim']}: {tetrapharmakos['evil_easily_endured']['explanation']}

PATH TO TRANQUILITY
{ataraxia['nature']['description']}. We achieve this through philosophy,
simple living, and withdrawal from unnecessary troubles.
{ataraxia['lathe_biosas']['maxim']}: {ataraxia['lathe_biosas']['meaning']}

REGARDING DEATH
{mortality['epicurus_argument']['description']}: {mortality['epicurus_argument']['reasoning']}
{mortality['symmetry_argument']['description']}: {mortality['symmetry_argument']['reasoning']}

THE VALUE OF FRIENDSHIP
{friendship['centrality']['claim']}. The Garden teaches us that
the good life is lived among friends. {friendship['benefits']['philosophy']}

PRUDENT CALCULATION
{prudence['centrality']['claim']}. We must weigh pleasures and pains wisely,
sometimes accepting present pain for future pleasure, sometimes rejecting
present pleasure to avoid future pain. {prudence['long_term_thinking']['principle']}

Thus Epicurean wisdom counsels: Pursue simple, natural pleasures;
dissolve irrational fears through understanding; cultivate friendship;
and live a quiet life of philosophical contentment."""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Epicureanism aims to dissolve tension through understanding.
        Higher tension indicates areas needing philosophical therapy.
        """
        tension_factors = []

        # Tension from disturbed tranquility
        ataraxia = analysis["ataraxia"]
        if ataraxia.get("sources_of_disturbance"):
            tension_factors.append(0.25)

        # Tension from unnatural desires
        desires = analysis["desires"]
        if desires.get("unnatural_and_unnecessary"):
            tension_factors.append(0.25)

        # Tension from fear of death
        mortality = analysis["mortality"]
        if mortality.get("nature_of_death"):
            tension_factors.append(0.2)

        # Tension from lack of friendship
        friendship = analysis["friendship"]
        if friendship.get("centrality"):
            tension_factors.append(0.15)

        # Base existential tension
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
