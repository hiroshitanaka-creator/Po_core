"""
Simone de Beauvoir - Existentialist Feminist Philosopher

Simone de Beauvoir (1908-1986)
Focus: Gender as Constructed, The Other, Immanence vs Transcendence, Situated Freedom

Key Concepts:
- "One is not born a woman, one becomes one": Gender is constructed, not innate
- The Other: Woman defined as the eternal Other to man's Subject
- Immanence vs Transcendence: Women confined to immanence, denied transcendence
- Situated Freedom: Freedom always exercised within a concrete historical situation
- Oppression: How patriarchy systematically limits women's possibilities
- Ambiguity: Embracing moral and existential ambiguity
- Projects: Existence defined through self-chosen projects
- Bad Faith in Gender Roles: Accepting imposed feminine identities
- Reciprocity: Genuine mutual recognition between subjects
- Lived Experience: Philosophy must be grounded in concrete lived experience
- The Second Sex: Women as defined by their relation to men, not autonomously
- Economic Independence: Essential for women's freedom
- Myth of Femininity: Cultural myths that naturalize women's oppression
- Body as Situation: The body as a situation to transcend, not destiny
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Beauvoir(Philosopher):
    """
    Simone de Beauvoir's existentialist feminist perspective.

    Analyzes prompts through the lens of gender construction, the Other,
    immanence vs transcendence, situated freedom, and oppression.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Simone de Beauvoir",
            description="Existentialist feminist focused on gender as constructed, the Other, and situated freedom",
        )
        self.tradition = "Existentialist Feminism"
        self.key_concepts = ['situated freedom', 'the Other (gendered)', 'ambiguity', 'becoming woman', 'ethics of liberation']

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Beauvoir's existentialist feminist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Beauvoir's existentialist feminist analysis
        """
        # Perform existentialist feminist analysis
        analysis = self._analyze_existence_and_gender(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Existentialist Feminist",
            "tension": tension,
            "gender_construction": analysis["gender_construction"],
            "the_other": analysis["the_other"],
            "immanence_transcendence": analysis["immanence_transcendence"],
            "situated_freedom": analysis["situated_freedom"],
            "oppression": analysis["oppression"],
            "ambiguity": analysis["ambiguity"],
            "projects": analysis["projects"],
            "bad_faith_gender": analysis["bad_faith_gender"],
            "reciprocity": analysis["reciprocity"],
            "lived_experience": analysis["lived_experience"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Existentialist feminist analysis",
                "focus": "Gender construction, the Other, situated freedom, and oppression",
            },
        }

    def _analyze_existence_and_gender(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Beauvoirean existentialist feminist analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze gender construction
        gender_construction = self._analyze_gender_construction(prompt)

        # Analyze the Other
        the_other = self._analyze_the_other(prompt)

        # Analyze immanence vs transcendence
        immanence_transcendence = self._analyze_immanence_transcendence(prompt)

        # Analyze situated freedom
        situated_freedom = self._analyze_situated_freedom(prompt)

        # Analyze oppression
        oppression = self._analyze_oppression(prompt)

        # Analyze ambiguity
        ambiguity = self._analyze_ambiguity(prompt)

        # Analyze projects
        projects = self._analyze_projects(prompt)

        # Analyze bad faith in gender roles
        bad_faith_gender = self._analyze_bad_faith_gender(prompt)

        # Analyze reciprocity
        reciprocity = self._analyze_reciprocity(prompt)

        # Analyze lived experience
        lived_experience = self._analyze_lived_experience(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            gender_construction,
            the_other,
            immanence_transcendence,
            situated_freedom,
            oppression,
            ambiguity,
            projects,
            bad_faith_gender,
            reciprocity,
            lived_experience,
        )

        return {
            "reasoning": reasoning,
            "gender_construction": gender_construction,
            "the_other": the_other,
            "immanence_transcendence": immanence_transcendence,
            "situated_freedom": situated_freedom,
            "oppression": oppression,
            "ambiguity": ambiguity,
            "projects": projects,
            "bad_faith_gender": bad_faith_gender,
            "reciprocity": reciprocity,
            "lived_experience": lived_experience,
        }

    def _analyze_gender_construction(self, text: str) -> Dict[str, Any]:
        """
        Analyze gender construction: "One is not born a woman, one becomes one."

        Gender is not biological destiny but a social construction created through
        repetition of social norms, expectations, and myths. Woman is made, not born.
        """
        text_lower = text.lower()

        # Construction indicators
        construction_words = [
            "become",
            "made",
            "constructed",
            "shaped",
            "formed",
            "learned",
            "taught",
            "socialized",
            "conditioned",
        ]

        # Essentialism indicators (opposing view)
        essence_words = [
            "born",
            "natural",
            "innate",
            "biological",
            "nature",
            "essentially",
            "inherently",
            "by nature",
        ]

        # Gender role indicators
        gender_words = [
            "woman",
            "man",
            "feminine",
            "masculine",
            "gender",
            "female",
            "male",
            "girl",
            "boy",
            "lady",
            "gentleman",
        ]

        construction_count = sum(1 for word in construction_words if word in text_lower)
        essence_count = sum(1 for word in essence_words if word in text_lower)
        gender_count = sum(1 for word in gender_words if word in text_lower)

        # Check for explicit construction language
        has_construction = construction_count >= 2 and gender_count >= 1

        if has_construction:
            status = "Gender as Constructed"
            description = "Gender recognized as socially constructed, not innate"
            level = "High awareness"
        elif essence_count > construction_count and gender_count >= 1:
            status = "Gender as Essential"
            description = "Gender treated as natural or biological essence"
            level = "Essentialist"
        elif gender_count >= 1:
            status = "Gender Present but Unclear"
            description = "Gender mentioned but construction/essence unclear"
            level = "Ambiguous"
        else:
            status = "Gender Not Thematized"
            description = "Gender not explicitly addressed"
            level = "Absent"

        return {
            "status": status,
            "description": description,
            "awareness_level": level,
            "construction_score": construction_count,
            "essence_score": essence_count,
            "beauvoirean_principle": "One is not born, but rather becomes, a woman",
            "insight": "No biological, psychological, or economic fate determines woman's figure in society",
        }

    def _analyze_the_other(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Other: Woman as the eternal Other to man's Subject.

        Man is the Subject, the Absolute; woman is the Other, defined always
        in relation to man, never as autonomous subject. This is the fundamental
        asymmetry of patriarchy.
        """
        text_lower = text.lower()

        # Othering indicators
        other_words = [
            "other",
            "different",
            "alien",
            "foreign",
            "opposite",
            "not like",
            "apart from",
            "excluded",
            "marginal",
        ]

        # Subject/object indicators
        subject_words = ["subject", "self", "autonomous", "independent", "free agent"]
        object_words = [
            "object",
            "defined by",
            "in relation to",
            "dependent",
            "secondary",
            "derivative",
            "relative to",
        ]

        # Asymmetry indicators
        asymmetry_words = [
            "asymmetry",
            "unequal",
            "hierarchy",
            "dominant",
            "subordinate",
            "superior",
            "inferior",
            "power over",
        ]

        # Relation to men/man
        relation_to_man = any(
            phrase in text_lower
            for phrase in [
                "in relation to men",
                "defined by men",
                "for men",
                "compared to men",
                "relative to men",
                "man as",
            ]
        )

        other_count = sum(1 for word in other_words if word in text_lower)
        subject_count = sum(1 for word in subject_words if word in text_lower)
        object_count = sum(1 for word in object_words if word in text_lower)
        asymmetry_count = sum(1 for word in asymmetry_words if word in text_lower)

        if other_count >= 2 and (object_count >= 1 or relation_to_man):
            status = "The Other Present"
            description = (
                "Othering dynamic evident - one group defined as Other to the Subject"
            )
            mode = "Subject/Other asymmetry"
        elif asymmetry_count >= 2:
            status = "Asymmetry Present"
            description = "Hierarchical asymmetry between groups"
            mode = "Power asymmetry"
        elif other_count >= 1:
            status = "Otherness Implicit"
            description = "Some othering but relation unclear"
            mode = "Potential othering"
        else:
            status = "The Other Not Explicit"
            description = "Subject/Other dynamic not thematized"
            mode = "Symmetry or absence"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "other_score": other_count,
            "asymmetry_score": asymmetry_count,
            "relation_to_dominant": relation_to_man or asymmetry_count >= 1,
            "principle": "She is the Other in a totality of which man is the Subject",
            "insight": "The category of the Other is as primordial as consciousness itself",
        }

    def _analyze_immanence_transcendence(self, text: str) -> Dict[str, Any]:
        """
        Analyze immanence vs transcendence: the fundamental existential tension.

        Transcendence: Self-surpassing, project-making, creative freedom
        Immanence: Confinement to given conditions, repetition, lack of futurity
        Women are systematically confined to immanence and denied transcendence.
        """
        text_lower = text.lower()

        # Transcendence indicators
        transcendence_words = [
            "transcend",
            "surpass",
            "overcome",
            "project",
            "create",
            "future",
            "possibility",
            "freedom",
            "autonomy",
            "agency",
            "transform",
            "change",
        ]

        # Immanence indicators
        immanence_words = [
            "confined",
            "trapped",
            "limited",
            "repetition",
            "routine",
            "cyclical",
            "maintenance",
            "domestic",
            "reproductive",
            "given",
            "fixed",
            "static",
            "unchanging",
            "stuck",
        ]

        # Denial of transcendence
        denial_words = [
            "denied",
            "prevented",
            "blocked",
            "unable to",
            "cannot",
            "forbidden",
            "restricted",
            "barriers to",
        ]

        transcendence_count = sum(
            1 for word in transcendence_words if word in text_lower
        )
        immanence_count = sum(1 for word in immanence_words if word in text_lower)
        denial_count = sum(1 for word in denial_words if word in text_lower)

        # Check for explicit tension
        has_tension = transcendence_count >= 2 and immanence_count >= 2

        if has_tension:
            status = "Full Tension"
            description = (
                "Both transcendence and immanence present - existential tension"
            )
            balance = "Dialectical"
        elif immanence_count > transcendence_count + 1:
            status = "Immanence Dominant"
            description = "Confinement to given conditions, transcendence denied"
            balance = "Confined to immanence"
        elif transcendence_count > immanence_count + 1:
            status = "Transcendence Dominant"
            description = "Project-making and self-surpassing emphasized"
            balance = "Oriented toward transcendence"
        elif denial_count >= 2:
            status = "Transcendence Denied"
            description = "Blocked from self-surpassing and project-making"
            balance = "Systematic denial"
        else:
            status = "Implicit or Absent"
            description = "Immanence/transcendence tension not explicit"
            balance = "Unclear"

        return {
            "status": status,
            "description": description,
            "balance": balance,
            "transcendence_score": transcendence_count,
            "immanence_score": immanence_count,
            "denial_score": denial_count,
            "principle": "Every subject posits itself as transcendent; woman is doomed to immanence",
            "insight": "The drama of woman lies in the conflict between her fundamental aspiration and her situation",
        }

    def _analyze_situated_freedom(self, text: str) -> Dict[str, Any]:
        """
        Analyze situated freedom: Freedom is always exercised within a situation.

        Freedom is not abstract but concrete, always exercised within historical,
        social, and material conditions. We are free, but our freedom is situated.
        """
        text_lower = text.lower()

        # Freedom indicators
        freedom_words = [
            "freedom",
            "free",
            "choice",
            "choose",
            "autonomy",
            "agency",
            "liberation",
            "emancipation",
        ]

        # Situation indicators
        situation_words = [
            "situation",
            "context",
            "conditions",
            "circumstances",
            "historical",
            "social",
            "material",
            "concrete",
            "economic",
            "political",
            "cultural",
        ]

        # Constraint indicators
        constraint_words = [
            "limited by",
            "shaped by",
            "constrained",
            "bounded",
            "within",
            "given",
            "facticity",
        ]

        freedom_count = sum(1 for word in freedom_words if word in text_lower)
        situation_count = sum(1 for word in situation_words if word in text_lower)
        constraint_count = sum(1 for word in constraint_words if word in text_lower)

        # Check for situated freedom (freedom + situation together)
        has_situated_freedom = freedom_count >= 1 and situation_count >= 2

        if has_situated_freedom:
            status = "Situated Freedom"
            description = "Freedom recognized as exercised within concrete conditions"
            awareness = "High"
        elif freedom_count >= 2 and situation_count == 0:
            status = "Abstract Freedom"
            description = "Freedom without acknowledgment of situation"
            awareness = "Limited"
        elif situation_count >= 2 and constraint_count >= 1:
            status = "Situation Emphasized"
            description = "Concrete conditions emphasized, freedom less clear"
            awareness = "Partial"
        elif freedom_count >= 1:
            status = "Freedom Present"
            description = "Freedom mentioned but situation unclear"
            awareness = "Moderate"
        else:
            status = "Neither Freedom nor Situation"
            description = "Situated freedom not thematized"
            awareness = "Absent"

        return {
            "status": status,
            "description": description,
            "awareness": awareness,
            "freedom_score": freedom_count,
            "situation_score": situation_count,
            "constraint_score": constraint_count,
            "principle": "Freedom is not abstract; it is always situated freedom",
            "insight": "One is not born free; one becomes free by transcending one's situation",
        }

    def _analyze_oppression(self, text: str) -> Dict[str, Any]:
        """
        Analyze oppression: How systems limit possibilities for certain groups.

        Oppression is not just individual prejudice but systematic limitation of
        possibilities, particularly how patriarchy limits women's transcendence.
        """
        text_lower = text.lower()

        # Oppression indicators
        oppression_words = [
            "oppression",
            "oppressed",
            "subjugation",
            "domination",
            "exploitation",
            "subordination",
            "marginalization",
        ]

        # System indicators
        system_words = [
            "system",
            "systemic",
            "structural",
            "institutional",
            "patriarchy",
            "patriarchal",
            "society",
            "culture",
        ]

        # Limitation indicators
        limitation_words = [
            "limited",
            "denied",
            "prevented",
            "restricted",
            "blocked",
            "barriers",
            "obstacles",
            "excluded",
        ]

        # Women/gender specific
        gender_specific = any(
            word in text_lower
            for word in ["women", "woman", "female", "feminine", "gender"]
        )

        oppression_count = sum(1 for word in oppression_words if word in text_lower)
        system_count = sum(1 for word in system_words if word in text_lower)
        limitation_count = sum(1 for word in limitation_words if word in text_lower)

        if oppression_count >= 1 and system_count >= 1:
            status = "Systematic Oppression"
            description = "Oppression recognized as systematic, not individual"
            level = "High awareness"
        elif oppression_count >= 1:
            status = "Oppression Present"
            description = "Oppression acknowledged but systemic nature unclear"
            level = "Moderate awareness"
        elif limitation_count >= 2 and system_count >= 1:
            status = "Systematic Limitation"
            description = "Systematic limitation of possibilities"
            level = "Implicit oppression"
        elif limitation_count >= 1:
            status = "Limitation Present"
            description = "Some limitation but not clearly systematic"
            level = "Low awareness"
        else:
            status = "Oppression Not Explicit"
            description = "Oppression not thematized"
            level = "Absent"

        return {
            "status": status,
            "description": description,
            "awareness_level": level,
            "oppression_score": oppression_count,
            "systemic_score": system_count,
            "limitation_score": limitation_count,
            "gender_specific": gender_specific,
            "principle": "Oppression is systematic limitation of possibilities",
            "insight": "Patriarchy confines women to immanence, denying them transcendence",
        }

    def _analyze_ambiguity(self, text: str) -> Dict[str, Any]:
        """
        Analyze ambiguity: Embracing moral and existential ambiguity.

        The human condition is fundamentally ambiguous - we are both freedom and
        facticity, subject and object, transcendence and immanence. Ethics must
        embrace this ambiguity rather than flee to false absolutes.
        """
        text_lower = text.lower()

        # Ambiguity indicators
        ambiguity_words = [
            "ambiguity",
            "ambiguous",
            "paradox",
            "tension",
            "both",
            "contradiction",
            "complex",
            "nuanced",
        ]

        # Complexity indicators
        complexity_words = [
            "complicated",
            "multifaceted",
            "layered",
            "conflicting",
            "uncertain",
            "unclear",
            "mixed",
            "neither nor",
        ]

        # Absolute/certain language (opposing view)
        absolute_words = [
            "absolute",
            "certain",
            "clearly",
            "obviously",
            "definitely",
            "pure",
            "simple",
            "either or",
        ]

        ambiguity_count = sum(1 for word in ambiguity_words if word in text_lower)
        complexity_count = sum(1 for word in complexity_words if word in text_lower)
        absolute_count = sum(1 for word in absolute_words if word in text_lower)

        # Check for embracing ambiguity
        embraces_ambiguity = ambiguity_count >= 1 or complexity_count >= 2

        if embraces_ambiguity and absolute_count <= 1:
            status = "Ambiguity Embraced"
            description = "Acknowledges complexity and ambiguity of existence"
            mode = "Nuanced thinking"
        elif absolute_count > ambiguity_count + complexity_count:
            status = "Absolutist"
            description = "Seeks certainty and absolute answers"
            mode = "Flight from ambiguity"
        elif ambiguity_count >= 1:
            status = "Ambiguity Present"
            description = "Some recognition of ambiguity"
            mode = "Partial acknowledgment"
        else:
            status = "Ambiguity Not Thematized"
            description = "Complexity and ambiguity not addressed"
            mode = "Unclear"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "ambiguity_score": ambiguity_count,
            "complexity_score": complexity_count,
            "absolutist_score": absolute_count,
            "principle": "The human condition is fundamentally ambiguous",
            "insight": "We must assume our fundamental ambiguity rather than flee from it",
        }

    def _analyze_projects(self, text: str) -> Dict[str, Any]:
        """
        Analyze projects: Existence defined through self-chosen projects.

        We create ourselves through our projects - future-oriented undertakings
        that give meaning to our existence. Authentic existence requires
        self-chosen projects, not imposed roles.
        """
        text_lower = text.lower()

        # Project indicators
        project_words = [
            "project",
            "goal",
            "aim",
            "plan",
            "purpose",
            "create",
            "build",
            "work toward",
            "aspiration",
        ]

        # Self-chosen indicators
        self_chosen_words = [
            "choose",
            "choose for myself",
            "my own",
            "autonomy",
            "self-determined",
            "authentic",
            "own choice",
        ]

        # Imposed/external indicators
        imposed_words = [
            "imposed",
            "expected",
            "supposed to",
            "must",
            "duty",
            "obligation",
            "role",
            "traditional",
        ]

        project_count = sum(1 for word in project_words if word in text_lower)
        self_chosen_count = sum(1 for word in self_chosen_words if word in text_lower)
        imposed_count = sum(1 for word in imposed_words if word in text_lower)

        if project_count >= 2 and self_chosen_count >= 1:
            status = "Self-Chosen Projects"
            description = "Existence defined through autonomous projects"
            authenticity = "Authentic"
        elif project_count >= 1:
            status = "Projects Present"
            description = "Future-oriented undertakings present"
            authenticity = "Unclear authenticity"
        elif imposed_count >= 2:
            status = "Imposed Roles"
            description = "Roles imposed rather than projects chosen"
            authenticity = "Inauthentic"
        else:
            status = "Projects Not Explicit"
            description = "Project-making not thematized"
            authenticity = "Absent"

        return {
            "status": status,
            "description": description,
            "authenticity": authenticity,
            "project_score": project_count,
            "self_chosen_score": self_chosen_count,
            "imposed_score": imposed_count,
            "principle": "We create ourselves through our projects",
            "insight": "Authentic existence requires self-chosen projects, not acceptance of imposed roles",
        }

    def _analyze_bad_faith_gender(self, text: str) -> List[str]:
        """
        Analyze bad faith in gender roles: Accepting imposed gender identities.

        Bad faith occurs when we accept gender roles as natural destiny rather
        than recognizing them as socially constructed and changeable. The "eternal
        feminine" is a myth that women internalize in bad faith.
        """
        text_lower = text.lower()
        indicators = []

        # Type 1: Naturalizing gender
        if any(
            phrase in text_lower
            for phrase in [
                "women are naturally",
                "men are naturally",
                "feminine nature",
                "masculine nature",
                "born to be",
                "natural role",
            ]
        ):
            indicators.append(
                "Naturalizing gender - treating social construction as nature (bad faith)"
            )

        # Type 2: Accepting imposed femininity
        if any(
            phrase in text_lower
            for phrase in [
                "eternal feminine",
                "true woman",
                "real woman",
                "feminine ideal",
                "lady",
                "proper woman",
                "should be feminine",
            ]
        ):
            indicators.append(
                "Accepting imposed femininity - internalizing the myth (bad faith)"
            )

        # Type 3: Gender as destiny
        if any(
            phrase in text_lower
            for phrase in [
                "women's destiny",
                "men's destiny",
                "destined to",
                "meant to be",
                "biology is destiny",
                "anatomy is destiny",
            ]
        ):
            indicators.append(
                "Gender as destiny - denying freedom and construction (bad faith)"
            )

        # Type 4: Complicity with oppression
        if any(
            phrase in text_lower
            for phrase in [
                "prefer it this way",
                "comfortable with",
                "accept my place",
                "natural order",
                "the way things are",
            ]
        ):
            indicators.append(
                "Complicity with oppression - accepting limitation (bad faith)"
            )

        # Type 5: Self-objectification
        if any(
            phrase in text_lower
            for phrase in [
                "for men",
                "to please",
                "attractive to",
                "male gaze",
                "how i look to them",
                "object",
            ]
        ):
            indicators.append(
                "Self-objectification - accepting object status (possible bad faith)"
            )

        # Type 6: Romantic mystification
        if any(
            phrase in text_lower
            for phrase in [
                "saved by love",
                "complete me",
                "find myself in",
                "romantic love",
                "need a man",
                "need a woman",
            ]
        ):
            indicators.append(
                "Romantic mystification - seeking completion in the Other (bad faith)"
            )

        if not indicators:
            indicators.append(
                "No obvious gender bad faith - potential for authentic existence"
            )

        return indicators

    def _analyze_reciprocity(self, text: str) -> Dict[str, Any]:
        """
        Analyze reciprocity: Genuine mutual recognition between subjects.

        Authentic human relations require reciprocity - mutual recognition of each
        other as both subject and object, freedom and body. The Other must be
        recognized as subject, not reduced to object.
        """
        text_lower = text.lower()

        # Reciprocity indicators
        reciprocity_words = [
            "reciprocity",
            "mutual",
            "both",
            "together",
            "recognize each other",
            "respect",
            "equal",
        ]

        # Recognition indicators
        recognition_words = [
            "recognize",
            "acknowledge",
            "see as",
            "respect",
            "dignity",
            "subject",
            "person",
            "human",
        ]

        # Asymmetry indicators (opposing)
        asymmetry_words = [
            "one-sided",
            "unequal",
            "dominate",
            "subordinate",
            "use",
            "exploit",
            "object",
            "thing",
        ]

        reciprocity_count = sum(1 for word in reciprocity_words if word in text_lower)
        recognition_count = sum(1 for word in recognition_words if word in text_lower)
        asymmetry_count = sum(1 for word in asymmetry_words if word in text_lower)

        if reciprocity_count >= 2 or (
            reciprocity_count >= 1 and recognition_count >= 2
        ):
            status = "Reciprocity Present"
            description = "Mutual recognition between subjects"
            mode = "Authentic relation"
        elif recognition_count >= 2:
            status = "Recognition Present"
            description = "Recognition but reciprocity unclear"
            mode = "Potential reciprocity"
        elif asymmetry_count >= 2:
            status = "Asymmetry Dominant"
            description = "One-sided relation, not reciprocal"
            mode = "Lack of reciprocity"
        else:
            status = "Reciprocity Not Explicit"
            description = "Mutual recognition not thematized"
            mode = "Unclear"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "reciprocity_score": reciprocity_count,
            "recognition_score": recognition_count,
            "asymmetry_score": asymmetry_count,
            "principle": "Authentic relations require mutual recognition as subjects",
            "insight": "Each consciousness seeks to posit itself as subject; reciprocity demands we recognize the Other as subject too",
        }

    def _analyze_lived_experience(self, text: str) -> Dict[str, Any]:
        """
        Analyze lived experience: Philosophy grounded in concrete experience.

        Beauvoir insists philosophy must be grounded in lived, concrete experience,
        not abstract universals. Women's lived experience reveals truths that
        male-centered philosophy has obscured.
        """
        text_lower = text.lower()

        # Lived experience indicators
        lived_words = [
            "experience",
            "lived",
            "concrete",
            "embodied",
            "felt",
            "experienced",
            "real",
            "actual",
        ]

        # Body/embodiment indicators
        body_words = [
            "body",
            "embodied",
            "embodiment",
            "physical",
            "flesh",
            "corporeal",
            "bodily",
            "material",
        ]

        # Abstract/universal indicators (opposing)
        abstract_words = [
            "abstract",
            "universal",
            "general",
            "theoretical",
            "ideal",
            "pure",
            "disembodied",
            "objective",
        ]

        # Personal/particular indicators
        particular_words = [
            "particular",
            "specific",
            "individual",
            "personal",
            "my experience",
            "i feel",
            "i experience",
        ]

        lived_count = sum(1 for word in lived_words if word in text_lower)
        body_count = sum(1 for word in body_words if word in text_lower)
        abstract_count = sum(1 for word in abstract_words if word in text_lower)
        particular_count = sum(1 for word in particular_words if word in text_lower)

        if lived_count >= 2 or (lived_count >= 1 and body_count >= 1):
            status = "Lived Experience Emphasized"
            description = "Philosophy grounded in concrete, embodied experience"
            mode = "Phenomenological"
        elif particular_count >= 2:
            status = "Particular Experience"
            description = "Emphasis on specific, personal experience"
            mode = "Situated"
        elif abstract_count > lived_count + body_count:
            status = "Abstract Approach"
            description = (
                "Abstract or universal approach, not grounded in lived experience"
            )
            mode = "Theoretical"
        else:
            status = "Lived Experience Implicit"
            description = "Concrete experience not explicitly emphasized"
            mode = "Unclear"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "lived_score": lived_count,
            "body_score": body_count,
            "abstract_score": abstract_count,
            "particular_score": particular_count,
            "principle": "Philosophy must be grounded in lived, concrete experience",
            "insight": "Women's lived experience reveals what male-centered philosophy obscures",
        }

    def _construct_reasoning(
        self,
        gender_construction: Dict[str, Any],
        the_other: Dict[str, Any],
        immanence_transcendence: Dict[str, Any],
        situated_freedom: Dict[str, Any],
        oppression: Dict[str, Any],
        ambiguity: Dict[str, Any],
        projects: Dict[str, Any],
        bad_faith_gender: List[str],
        reciprocity: Dict[str, Any],
        lived_experience: Dict[str, Any],
    ) -> str:
        """Construct Beauvoirean existentialist feminist reasoning."""
        reasoning = (
            f"From Beauvoir's existentialist feminist perspective: "
            f"{gender_construction['description']}. "
        )

        # Add the Other if present
        if the_other["status"] != "The Other Not Explicit":
            reasoning += f"The Subject/Other dynamic: {the_other['description']}. "

        # Add immanence/transcendence
        reasoning += f"Regarding immanence and transcendence: {immanence_transcendence['description']}. "

        # Add situated freedom
        if situated_freedom["status"] != "Neither Freedom nor Situation":
            reasoning += f"Freedom analysis: {situated_freedom['description']}. "

        # Add oppression if present
        if oppression["status"] != "Oppression Not Explicit":
            reasoning += f"Oppression: {oppression['description']}. "

        # Add bad faith analysis
        primary_bad_faith = bad_faith_gender[0]
        if "No obvious gender bad faith" not in primary_bad_faith:
            reasoning += f"Bad faith in gender: {primary_bad_faith}. "

        # Add reciprocity
        if reciprocity["status"] in ["Reciprocity Present", "Asymmetry Dominant"]:
            reasoning += f"Human relations: {reciprocity['description']}. "

        # Add ambiguity
        if ambiguity["status"] != "Ambiguity Not Thematized":
            reasoning += f"Existential complexity: {ambiguity['description']}. "

        # Add projects
        if projects["status"] != "Projects Not Explicit":
            reasoning += f"Projects and authenticity: {projects['description']}. "

        # Add lived experience
        if lived_experience["mode"] == "Phenomenological":
            reasoning += f"Grounding: {lived_experience['description']}. "

        # Conclude with Beauvoirean principles
        reasoning += (
            "Remember: one is not born, but rather becomes, a woman. "
            "Gender is constructed through social myths and expectations. "
            "Women must refuse immanence and claim transcendence through self-chosen projects. "
            "Authentic freedom is situated freedom - we are free within our concrete historical situation."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate existential feminist tension.

        Tensions arise from:
        - Gender essentialism (denying construction)
        - Subject/Other asymmetry
        - Confinement to immanence
        - Oppression and limitation
        - Bad faith in gender roles
        - Lack of reciprocity
        - Flight from ambiguity
        """
        tension_score = 0
        tension_elements = []

        # Check gender construction
        gender = analysis["gender_construction"]
        if gender["awareness_level"] == "Essentialist":
            tension_score += 2
            tension_elements.append("Gender essentialism - denying social construction")

        # Check the Other
        other = analysis["the_other"]
        if other["mode"] == "Subject/Other asymmetry":
            tension_score += 2
            tension_elements.append("Subject/Other asymmetry - fundamental inequality")

        # Check immanence/transcendence
        immanence_transcendence = analysis["immanence_transcendence"]
        if immanence_transcendence["balance"] == "Confined to immanence":
            tension_score += 2
            tension_elements.append("Confined to immanence - transcendence denied")
        elif immanence_transcendence["balance"] == "Systematic denial":
            tension_score += 3
            tension_elements.append(
                "Systematic denial of transcendence - profound oppression"
            )

        # Check oppression
        oppression = analysis["oppression"]
        if oppression["awareness_level"] in ["High awareness", "Implicit oppression"]:
            tension_score += 1
            tension_elements.append(f"Oppression present - {oppression['description']}")

        # Check bad faith
        bad_faith = analysis["bad_faith_gender"]
        if len(bad_faith) >= 3:
            tension_score += 2
            tension_elements.append("Multiple forms of gender bad faith")
        elif "No obvious gender bad faith" not in bad_faith[0]:
            tension_score += 1
            tension_elements.append(f"Gender bad faith: {bad_faith[0]}")

        # Check reciprocity
        reciprocity = analysis["reciprocity"]
        if reciprocity["mode"] == "Lack of reciprocity":
            tension_score += 1
            tension_elements.append("Lack of reciprocity - asymmetric relations")

        # Check ambiguity
        ambiguity = analysis["ambiguity"]
        if ambiguity["mode"] == "Flight from ambiguity":
            tension_score += 1
            tension_elements.append("Flight from ambiguity - seeking false absolutes")

        # Check projects
        projects = analysis["projects"]
        if projects["authenticity"] == "Inauthentic":
            tension_score += 1
            tension_elements.append("Imposed roles rather than self-chosen projects")

        # Determine tension level
        if tension_score >= 7:
            level = "Very High"
            description = "Deep existential feminist crisis - multiple forms of oppression and bad faith"
        elif tension_score >= 5:
            level = "High"
            description = (
                "Significant tensions - confinement to immanence and denial of freedom"
            )
        elif tension_score >= 3:
            level = "Moderate"
            description = "Some existential feminist tensions present"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, potential for authentic existence"
        else:
            level = "Very Low"
            description = (
                "Aligned with authentic, reciprocal existence and situated freedom"
            )

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
