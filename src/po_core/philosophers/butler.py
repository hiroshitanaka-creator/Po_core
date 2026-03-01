"""
Judith Butler Philosopher Module

Implements post-structuralist and feminist philosophy based on Butler's work.

Key concepts:
- Performativity: Gender as repeated performance
- Gender Trouble: Destabilizing gender categories
- Bodies That Matter: Materiality and discourse
- Heteronormative Matrix: Regulatory framework of gender/sexuality
- Precarity: Shared vulnerability of life
- Grievability: Whose lives are mournable
- Ethical Violence: Demands for coherent self-account
- Recognition: Conditions of subject formation
- Subversion: Disrupting norms through their repetition
- Undoing Gender: Expanding livable lives
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Butler(Philosopher):
    """
    Judith Butler (1956-)

    American philosopher and gender theorist whose work has
    transformed understanding of gender, sex, and identity.
    Influenced by Foucault, Derrida, and psychoanalysis,
    Butler argues that gender is performatively constituted
    through repeated acts and that subversion is possible
    through critical engagement with these norms.
    """

    def __init__(self):
        super().__init__(
            name="Judith Butler",
            description="Post-structuralist and feminist philosopher known for work on gender performativity",
        )
        self.tradition = "Post-structuralism / Feminist Theory"
        self.key_concepts = [
            "performativity",
            "gender trouble",
            "bodies that matter",
            "heteronormative matrix",
            "precarity",
            "grievability",
            "ethical violence",
            "recognition",
            "subversion",
            "undoing gender",
            "subjection",
            "citation",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Apply Butler's critical theory to the prompt.

        Returns analysis through the lens of performativity,
        power, and the conditions of subject formation.
        """
        analysis = self._analyze_butler(prompt)
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Post-structuralist Feminist Theory",
            "tension": tension,
            "performativity": analysis["performativity"],
            "gender_trouble": analysis["gender_trouble"],
            "bodies_that_matter": analysis["bodies"],
            "heteronormative_matrix": analysis["matrix"],
            "precarity": analysis["precarity"],
            "grievability": analysis["grievability"],
            "recognition": analysis["recognition"],
            "subversion": analysis["subversion"],
            "ethical_violence": analysis["ethical_violence"],
            "political_implications": analysis["political"],
            "metadata": {
                "philosopher": self.name,
                "tradition": self.tradition,
                "method": "critical_performative_analysis",
                "concepts_applied": self.key_concepts,
            },
        }

    def _analyze_butler(self, prompt: str) -> Dict[str, Any]:
        """Comprehensive Butler analysis of the prompt."""
        performativity = self._analyze_performativity(prompt)
        gender_trouble = self._analyze_gender_trouble(prompt)
        bodies = self._analyze_bodies_that_matter(prompt)
        matrix = self._analyze_heteronormative_matrix(prompt)
        precarity = self._analyze_precarity(prompt)
        grievability = self._analyze_grievability(prompt)
        recognition = self._analyze_recognition(prompt)
        subversion = self._analyze_subversion(prompt)
        ethical_violence = self._analyze_ethical_violence(prompt)
        political = self._derive_political_implications(prompt)

        reasoning = self._construct_reasoning(
            prompt,
            performativity,
            gender_trouble,
            bodies,
            matrix,
            precarity,
            grievability,
            recognition,
            subversion,
        )

        return {
            "reasoning": reasoning,
            "performativity": performativity,
            "gender_trouble": gender_trouble,
            "bodies": bodies,
            "matrix": matrix,
            "precarity": precarity,
            "grievability": grievability,
            "recognition": recognition,
            "subversion": subversion,
            "ethical_violence": ethical_violence,
            "political": political,
        }

    def _analyze_performativity(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze through the lens of performativity.

        Performativity is not performance in the theatrical sense
        but the citational practice by which discourse produces
        the effects it names.
        """
        return {
            "concept": {
                "description": "Gender is constituted through repeated stylized acts",
                "distinction": "Not a singular act but a reiteration of norms",
                "effect": "The appearance of substance is produced by the repetition",
            },
            "citation": {
                "description": "Each act cites prior acts and norms",
                "origin": "There is no original gender to imitate",
                "implication": "All gender is a copy without an original",
            },
            "constitution": {
                "not_expression": "Gender does not express an inner truth",
                "production": "It produces the illusion of an inner core",
                "subject": "The subject is constituted through these practices",
            },
            "failure": {
                "description": "Performativity can fail; repetition is never perfect",
                "opportunity": "Failure opens space for subversion",
                "politics": "The instability of gender is its political possibility",
            },
            "application": "What is being performatively constituted here?",
        }

    def _analyze_gender_trouble(self, prompt: str) -> Dict[str, Any]:
        """
        Examine how gender categories can be troubled.

        Gender Trouble (1990) argues that gender is not natural
        but naturalized through repetition, and can be denaturalized.
        """
        return {
            "destabilization": {
                "target": "The assumed naturalness of gender categories",
                "method": "Showing gender as culturally constructed",
                "effect": "Revealing contingency where necessity was assumed",
            },
            "sex_gender_distinction": {
                "critique": "Even 'sex' is discursively constructed",
                "argument": "The category of sex is itself gendered",
                "implication": "No pre-cultural body exists before discourse",
            },
            "drag_and_parody": {
                "description": "Drag reveals the imitative structure of gender",
                "insight": "All gender is drag; there is no original",
                "subversive": "Parody exposes the contingency of gender norms",
            },
            "trouble_as_method": {
                "description": "Make trouble for categories that seem natural",
                "goal": "Expand possibilities for livable lives",
                "practice": "Question what is taken for granted",
            },
            "application": "What gender assumptions operate here?",
        }

    def _analyze_bodies_that_matter(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the materiality of bodies and their discursive formation.

        Bodies That Matter (1993) addresses how discourse materializes bodies,
        which bodies come to matter, and which are rendered abject.
        """
        return {
            "materialization": {
                "description": "Bodies are materialized through regulatory norms",
                "process": "Not imposed on pre-existing matter but constitutive",
                "temporality": "Materialization is ongoing, never complete",
            },
            "which_bodies_matter": {
                "inclusion": "Some bodies are intelligible, livable, real",
                "exclusion": "Others are rendered abject, unreal, unintelligible",
                "politics": "The boundary between them is political",
            },
            "abjection": {
                "description": "The domain of unlivable, uninhabitable zones",
                "function": "Constitutes the outside that defines the inside",
                "examples": "Queer bodies, disabled bodies, racialized bodies",
            },
            "resignification": {
                "possibility": "Terms of abjection can be reclaimed",
                "example": "'Queer' reclaimed as site of resistance",
                "politics": "Working within and against the terms we are given",
            },
            "application": "Which bodies matter in this context? Which are excluded?",
        }

    def _analyze_heteronormative_matrix(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the regulatory framework of gender and sexuality.

        The heteronormative matrix is the grid of intelligibility
        that produces coherent gender by linking sex, gender, and desire.
        """
        return {
            "structure": {
                "description": "Sex, gender, and desire are linked coherently",
                "norm": "Male body → masculine gender → desire for women",
                "enforcement": "Deviations are rendered unintelligible or pathological",
            },
            "compulsory_heterosexuality": {
                "description": "Heterosexuality is presumed and enforced as norm",
                "mechanism": "Produces gender as binary and complementary",
                "effect": "Queerness appears as deviation from natural order",
            },
            "regulatory_ideal": {
                "description": "Gender norms function as ideals no one fully embodies",
                "effect": "Everyone fails; some failures are more punished",
                "politics": "The ideal itself should be questioned",
            },
            "beyond_the_matrix": {
                "possibility": "Other configurations of sex/gender/desire exist",
                "challenge": "Expand intelligibility beyond the binary",
                "goal": "More livable lives for more people",
            },
            "application": "How does the heteronormative matrix operate here?",
        }

    def _analyze_precarity(self, prompt: str) -> Dict[str, Any]:
        """
        Examine shared vulnerability and precarious life.

        Butler's later work emphasizes precarity as a shared
        condition of bodily vulnerability and interdependence.
        """
        return {
            "precariousness": {
                "description": "The shared condition of bodily vulnerability",
                "universality": "All lives are precarious, dependent on others",
                "ontology": "We are constituted through relations to others",
            },
            "precarity": {
                "description": "Politically induced condition of vulnerability",
                "inequality": "Some populations are more exposed than others",
                "examples": "Refugees, the poor, minorities, the displaced",
            },
            "interdependence": {
                "description": "We depend on others for survival and flourishing",
                "implication": "Autonomy is a fiction; we are relational beings",
                "ethics": "Recognition of interdependence grounds ethical response",
            },
            "political_implications": {
                "responsibility": "We are responsible for conditions of precarity",
                "solidarity": "Shared precariousness can ground alliance",
                "resistance": "Vulnerable bodies assembling in public space",
            },
            "application": "What precarity is at stake here?",
        }

    def _analyze_grievability(self, prompt: str) -> Dict[str, Any]:
        """
        Examine whose lives are considered grievable.

        Grievability determines which lives are recognized as lives,
        which losses are felt as losses worthy of public mourning.
        """
        return {
            "grievable_lives": {
                "description": "Lives that are recognized as lives",
                "condition": "Their loss would be mourned as a loss",
                "frame": "Frames determine what appears as grievable",
            },
            "ungrievable_lives": {
                "description": "Lives not recognized as fully living",
                "consequence": "Their deaths don't register as losses",
                "examples": "Casualties of war, migrant deaths, certain minorities",
            },
            "frames_of_recognition": {
                "description": "Schemas that determine what we can see",
                "power": "Frames are produced and circulated by power",
                "politics": "Contesting frames is political work",
            },
            "ethical_implications": {
                "question": "What makes a life grievable?",
                "demand": "Expand grievability to all lives",
                "solidarity": "Mourning as political practice",
            },
            "application": "Whose life is grievable here? Whose is not?",
        }

    def _analyze_recognition(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the conditions for subject recognition.

        Drawing on Hegel, Butler explores how subjects are formed
        through relations of recognition and the violence therein.
        """
        return {
            "subject_formation": {
                "description": "We become subjects through being recognized",
                "condition": "Recognition is given by others, not claimed alone",
                "paradox": "We depend on norms we did not choose",
            },
            "norms_of_recognition": {
                "description": "Norms determine who can be recognized",
                "exclusion": "Those who don't conform are not recognized as subjects",
                "violence": "Non-recognition is a form of violence",
            },
            "desire_for_recognition": {
                "description": "We desire recognition to be",
                "vulnerability": "This desire exposes us to others",
                "risk": "The terms of recognition may violate us",
            },
            "transforming_recognition": {
                "possibility": "Norms of recognition can be changed",
                "method": "Collective struggle for new forms of recognition",
                "goal": "Recognition without violence",
            },
            "application": "What forms of recognition are at stake?",
        }

    def _analyze_subversion(self, prompt: str) -> Dict[str, Any]:
        """
        Examine possibilities for subverting norms.

        For Butler, subversion works within the terms of power,
        using repetition with a difference to destabilize norms.
        """
        return {
            "subversive_repetition": {
                "description": "Norms are destabilized through imperfect citation",
                "mechanism": "Repetition with variation exposes contingency",
                "examples": "Drag, parody, queer practices",
            },
            "working_within": {
                "description": "We cannot step outside the terms of power",
                "strategy": "Use given terms against their grain",
                "limitation": "Not all repetitions are subversive",
            },
            "resignification": {
                "description": "Terms can be given new meanings",
                "example": "'Queer' transformed from slur to affirmation",
                "politics": "Language is a site of political struggle",
            },
            "conditions_of_subversion": {
                "context": "What counts as subversive is context-dependent",
                "risk": "Subversion may be reabsorbed by power",
                "persistence": "Ongoing work, not single acts",
            },
            "application": "What possibilities for subversion exist here?",
        }

    def _analyze_ethical_violence(self, prompt: str) -> Dict[str, Any]:
        """
        Examine the violence in demands for self-account.

        Butler critiques demands for coherent self-narratives
        as potentially violent, ignoring our opacity to ourselves.
        """
        return {
            "demand_for_coherence": {
                "description": "We are asked to give coherent accounts of ourselves",
                "violence": "This demand ignores our fundamental opacity",
                "impossibility": "We cannot fully know or narrate ourselves",
            },
            "opacity": {
                "description": "We are partially opaque to ourselves",
                "reasons": "Social formation, unconscious, embodiment",
                "implication": "Self-transparency is impossible",
            },
            "relational_self": {
                "description": "The self is formed in relation to others",
                "consequence": "Our origins are social, not self-created",
                "humility": "We cannot be fully responsible for who we are",
            },
            "ethics_of_opacity": {
                "tolerance": "Accept opacity in self and others",
                "humility": "Acknowledge limits of self-knowledge",
                "forgiveness": "Extend generosity given shared condition",
            },
            "application": "What demands for self-account operate here?",
        }

    def _derive_political_implications(self, prompt: str) -> Dict[str, Any]:
        """Extract political implications from Butler's framework."""
        return {
            "coalition_politics": {
                "description": "Alliance across difference without identity",
                "method": "Unity around shared precarity, not shared identity",
                "practice": "Solidarity without sameness",
            },
            "bodies_in_public": {
                "description": "Vulnerable bodies assembling in public space",
                "power": "The body's presence makes political claims",
                "examples": "Protests, occupations, public mourning",
            },
            "expanding_livability": {
                "goal": "More lives recognized as lives worth living",
                "method": "Challenge norms that render lives unlivable",
                "measure": "Does this expand or contract livability?",
            },
            "critical_practice": {
                "ongoing": "Critique must be ongoing, never complete",
                "reflexive": "Turn critique on our own categories",
                "hopeful": "Another world of gender is possible",
            },
        }

    def _apply_butler_to_problem(self, text: str) -> str:
        """Apply Butlerian concepts to the domain of the given text."""
        t = text.lower()
        if any(
            w in t
            for w in [
                "gender",
                "sex",
                "woman",
                "man",
                "female",
                "male",
                "trans",
                "queer",
                "nonbinary",
                "identity",
                "masculine",
                "feminine",
            ]
        ):
            return (
                "Gender, Butler argues in Gender Trouble, is not the expression of a prior "
                "biological sex or an inner identity, but a performance: a stylized repetition "
                "of acts that produces the very illusion of a stable gendered substance behind "
                "them. There is no gender identity prior to the expressions of gender; the "
                "expressions are constitutive. This means gender norms must be cited — repeated "
                "— to have force, and that repetition is precisely what opens the possibility "
                "of subversive reiteration: drag, parody, and other performances that expose "
                "the constructed and contingent character of what presents itself as natural "
                "and inevitable. The heterosexual matrix — the assumption that coherent gender "
                "requires alignment of sex, gender, and desire — is the regulatory ideal whose "
                "internal contradictions Gender Trouble traces."
            )
        elif any(
            w in t
            for w in [
                "power",
                "norm",
                "rule",
                "law",
                "regulat",
                "govern",
                "subject",
                "subordinat",
                "compli",
                "conform",
            ]
        ):
            return (
                "Subject formation, for Butler, occurs through and within normative frameworks: "
                "to become recognizable as a subject — to be legible, to have standing, to "
                "matter — is to have submitted to the norms that make subjectivity possible. "
                "This is not simple oppression but a productive and constitutive operation: "
                "norms do not merely constrain pre-formed subjects but bring subjects into "
                "being. The paradox is that the same power that subordinates is the power "
                "one must cite to resist. But because norms require repeated citation to "
                "maintain their authority, that repetition is always potentially imperfect, "
                "displaced, subversive — citationality opens the gap between norm and its "
                "instantiation that political agency can inhabit."
            )
        elif any(
            w in t
            for w in [
                "vulnerab",
                "precari",
                "suffer",
                "harm",
                "care",
                "pain",
                "body",
                "bodily",
                "injur",
                "loss",
                "grief",
                "mourn",
            ]
        ):
            return (
                "In Precarious Life and Frames of War, Butler argues that vulnerability and "
                "precarity are constitutive features of all human life — we are always already "
                "dependent on others, exposed to loss and harm by virtue of our embodied, "
                "relational existence. But precarity is differentially distributed: some lives "
                "are organized as precarious, rendered insecure and expendable by political and "
                "economic arrangements, while others are protected. The ethical demand is to "
                "acknowledge shared vulnerability — the interdependency that links us — and "
                "to contest the frames that render some lives ungrievable, invisible, outside "
                "the circle of moral concern."
            )
        elif any(
            w in t
            for w in [
                "politic",
                "resist",
                "movement",
                "protest",
                "assembl",
                "collective",
                "activis",
                "mobiliz",
                "solidarity",
                "coalition",
            ]
        ):
            return (
                "Butler's political ontology begins from bodies assembled together in public "
                "space: the very act of assembly — gathering, persisting, refusing to disperse — "
                "is a performative claim about whose lives matter and whose precarity is to be "
                "contested. Performative politics does not express a pre-given political subject "
                "but constitutes that subject through the repeated act of assembly. Coalition "
                "politics does not require sameness of identity but solidarity across difference "
                "organized around shared precarity and the aspiration to more livable lives. "
                "The question 'who counts as a grievable life?' is simultaneously an ethical "
                "and a political question whose answer is always contested."
            )
        elif any(
            w in t
            for w in [
                "language",
                "speech",
                "word",
                "hate",
                "slur",
                "insult",
                "name",
                "call",
                "say",
                "utterance",
                "discourse",
            ]
        ):
            return (
                "Excitable Speech examines the paradox of injurious language: words can wound, "
                "can constitute and diminish the subjects they address. But Butler resists the "
                "conclusion that hate speech should be legally censored, arguing instead that "
                "the performative force of language is never fully controlled by the speaker. "
                "Resignification — the reappropriation and redeployment of injurious terms — "
                "has been a persistent strategy of subordinated communities: the reclaimed slur, "
                "the term of contempt transformed into a badge of pride, demonstrates that "
                "iterability opens even the most harmful utterances to subversive reiteration. "
                "Language is the site of both harm and potential transformation."
            )
        elif any(
            w in t
            for w in [
                "ethic",
                "moral",
                "responsib",
                "obligation",
                "recogni",
                "other",
                "face",
                "encounter",
                "relation",
                "cohabit",
            ]
        ):
            return (
                "Butler's ethics turns on the question of recognition: whose lives are "
                "recognizable as lives, whose suffering registers as suffering, whose deaths "
                "are mourned as losses? Drawing on Levinas, she argues that the face of the "
                "Other — even the enemy's face — makes an ethical demand that cannot be fully "
                "satisfied or refused. But she goes beyond Levinas in insisting that recognition "
                "is always mediated by frames and norms that determine who can appear as a "
                "recognizable face. The ethical-political task is to contest those frames, to "
                "expand grievability, and to acknowledge that we are bound together in precarious "
                "cohabitation on a globe we did not choose and cannot leave."
            )
        else:
            return (
                "Butler's philosophy centers on performativity — the insight that identity "
                "categories (gender, sex, the subject itself) are not expressions of pre-given "
                "essences but effects of repeated, citational performances that produce the "
                "illusion of an underlying substance. Norms are constitutive: they bring "
                "subjects into being and simultaneously mark others as abject, unlivable, "
                "outside the norm. Precarity names the unequal distribution of vulnerability: "
                "whose life counts as a life, whose death as a death worth mourning? "
                "Grievability, recognition, and the aspiration to more livable lives for all "
                "are the ethical-political horizons of Butler's work. Gender Trouble, "
                "Precarious Life, and Notes Toward a Performative Theory of Assembly remain "
                "the central texts."
            )

    def _construct_reasoning(
        self,
        prompt: str,
        performativity: Dict,
        gender_trouble: Dict,
        bodies: Dict,
        matrix: Dict,
        precarity: Dict,
        grievability: Dict,
        recognition: Dict,
        subversion: Dict,
    ) -> str:
        """Construct comprehensive Butler reasoning."""
        applied = self._apply_butler_to_problem(prompt)
        return f"""{applied}

Critical Analysis through Butler: "{prompt}"

PERFORMATIVITY
{performativity['concept']['description']}. {performativity['concept']['effect']}
{performativity['citation']['description']}. {performativity['citation']['implication']}

TROUBLING GENDER
{gender_trouble['destabilization']['target']}. By showing the constructed nature
of what seems natural, we reveal contingency. {gender_trouble['trouble_as_method']['description']}

BODIES THAT MATTER
{bodies['materialization']['description']}. But not all bodies matter equally.
{bodies['which_bodies_matter']['exclusion']}. The boundary is political.

THE HETERONORMATIVE MATRIX
{matrix['structure']['description']}. {matrix['regulatory_ideal']['effect']}
The matrix produces coherent subjects while excluding others.

PRECARITY AND VULNERABILITY
{precarity['precariousness']['description']}. But {precarity['precarity']['description']}.
Our shared vulnerability grounds ethical and political response.

GRIEVABILITY
{grievability['grievable_lives']['description']}. {grievability['ungrievable_lives']['consequence']}
We must contest the frames that determine whose lives count.

RECOGNITION
{recognition['subject_formation']['description']}. {recognition['norms_of_recognition']['exclusion']}
The struggle is for forms of recognition that do not violate.

POSSIBILITIES FOR SUBVERSION
{subversion['subversive_repetition']['description']}. {subversion['resignification']['politics']}
Working within the terms of power, we can destabilize them.

This analysis asks: What norms are operating? Who is excluded?
How might we work toward more livable lives for all?"""

    def _calculate_tension(self, analysis: Dict[str, Any]) -> float:
        """
        Calculate philosophical tension.

        Butler's work addresses tensions in identity, power, and resistance.
        """
        tension_factors = []

        # Tension from performativity and identity
        performativity = analysis["performativity"]
        if performativity.get("failure"):
            tension_factors.append(0.25)

        # Tension from exclusion
        bodies = analysis["bodies"]
        if bodies.get("abjection"):
            tension_factors.append(0.25)

        # Tension from precarity
        precarity = analysis["precarity"]
        if precarity.get("precarity"):
            tension_factors.append(0.2)

        # Tension from recognition
        recognition = analysis["recognition"]
        if recognition.get("desire_for_recognition"):
            tension_factors.append(0.15)

        # Base structural tension
        tension_factors.append(0.1)

        return min(sum(tension_factors), 1.0)
