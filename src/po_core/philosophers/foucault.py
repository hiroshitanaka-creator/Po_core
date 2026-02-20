"""
Michel Foucault - French Post-Structuralist Philosopher and Historian

Michel Foucault (1926-1984)
Focus: Power/Knowledge, Discourse, Disciplinary Power, Biopower, Genealogy

Key Concepts:
- Power/Knowledge (Pouvoir/Savoir): Power and knowledge are inseparable
- Discourse: Systems determining what can be said and thought
- Disciplinary Power: Surveillance, normalization, examination
- Panopticon: Bentham's prison as model of modern disciplinary society
- Biopower/Biopolitics: Power over life itself, management of populations
- Archaeology: Method analyzing conditions of discourse formation
- Genealogy: Method tracing contingent historical emergence, not origins
- Subject/Subjectivation: How power produces subjects and subjectivities
- Governmentality: The art of government, conduct of conduct
- Care of the Self: Ethics as aesthetic self-formation (ancient Greeks)
- Episteme: Underlying framework organizing knowledge in an era
"""

from typing import Any, Dict, Optional

from po_core.philosophers.base import Philosopher


class Foucault(Philosopher):
    """
    Michel Foucault's philosophy of power, knowledge, and discourse.

    Analyzes prompts through the lens of power/knowledge relations,
    disciplinary mechanisms, biopolitics, and discourse formation.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Michel Foucault",
            description="Post-structuralist focused on power/knowledge, discourse, discipline, and biopower",
        )
        self.tradition = "Post-Structuralism / Critical Theory"
        self.key_concepts = [
            "power/knowledge",
            "discourse",
            "discipline and punish",
            "biopower",
            "genealogy",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Foucault's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Foucault's power/knowledge analysis
        """
        # Perform Foucauldian analysis
        analysis = self._analyze_power_knowledge(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Archaeology/Genealogy of Power and Knowledge",
            "power_knowledge": analysis["power_knowledge"],
            "discourse": analysis["discourse"],
            "disciplinary_power": analysis["disciplinary_power"],
            "panopticon": analysis["panopticon"],
            "biopower": analysis["biopower"],
            "archaeology": analysis["archaeology"],
            "genealogy": analysis["genealogy"],
            "subjectivation": analysis["subjectivation"],
            "governmentality": analysis["governmentality"],
            "care_of_self": analysis["care_of_self"],
            "episteme": analysis["episteme"],
            "tension": {
                "level": "Moderate",
                "description": "Tension between power and resistance, knowledge and control",
                "elements": [
                    "Power produces knowledge yet knowledge reinforces power",
                    "Discourse shapes subjects who may resist that shaping",
                    "Freedom exists only within relations of power",
                ],
            },
            "metadata": {
                "philosopher": self.name,
                "approach": "Genealogical and archaeological analysis",
                "focus": "Power/knowledge, discourse, and disciplinary mechanisms",
            },
        }

    def _analyze_power_knowledge(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Foucauldian power/knowledge analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze power/knowledge relations
        power_knowledge = self._assess_power_knowledge(prompt)

        # Analyze discourse
        discourse = self._analyze_discourse(prompt)

        # Assess disciplinary power
        disciplinary_power = self._assess_disciplinary_power(prompt)

        # Check for panopticon
        panopticon = self._check_panopticon(prompt)

        # Analyze biopower/biopolitics
        biopower = self._analyze_biopower(prompt)

        # Check archaeological approach
        archaeology = self._check_archaeology(prompt)

        # Check genealogical approach
        genealogy = self._check_genealogy(prompt)

        # Analyze subjectivation
        subjectivation = self._analyze_subjectivation(prompt)

        # Assess governmentality
        governmentality = self._assess_governmentality(prompt)

        # Check care of the self
        care_of_self = self._check_care_of_self(prompt)

        # Identify episteme
        episteme = self._identify_episteme(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            power_knowledge, discourse, disciplinary_power, biopower, subjectivation
        )

        return {
            "reasoning": reasoning,
            "power_knowledge": power_knowledge,
            "discourse": discourse,
            "disciplinary_power": disciplinary_power,
            "panopticon": panopticon,
            "biopower": biopower,
            "archaeology": archaeology,
            "genealogy": genealogy,
            "subjectivation": subjectivation,
            "governmentality": governmentality,
            "care_of_self": care_of_self,
            "episteme": episteme,
        }

    def _assess_power_knowledge(self, text: str) -> Dict[str, Any]:
        """
        Assess power/knowledge (pouvoir/savoir) relations.

        Power and knowledge directly imply one another.
        No power relation without constitution of a field of knowledge,
        no knowledge that does not presuppose power relations.
        """
        text_lower = text.lower()

        # Power indicators
        power_words = [
            "power",
            "control",
            "authority",
            "domination",
            "govern",
            "rule",
            "regulate",
        ]
        has_power = sum(1 for word in power_words if word in text_lower)

        # Knowledge indicators
        knowledge_words = [
            "knowledge",
            "truth",
            "science",
            "expertise",
            "know",
            "information",
            "data",
        ]
        has_knowledge = sum(1 for word in knowledge_words if word in text_lower)

        # Mutual implication indicators
        mutual_words = [
            "legitimize",
            "justify",
            "validate",
            "authorize",
            "enable",
            "support",
        ]
        sum(1 for word in mutual_words if word in text_lower)

        # Expert/professional knowledge
        expert_words = [
            "expert",
            "professional",
            "specialist",
            "doctor",
            "psychiatrist",
            "scientist",
        ]
        has_expert = sum(1 for word in expert_words if word in text_lower)

        # Truth regime indicators
        truth_words = ["truth", "fact", "objective", "scientific", "proven", "evidence"]
        has_truth = sum(1 for word in truth_words if word in text_lower)

        if has_power >= 1 and has_knowledge >= 1:
            relation = "Power/Knowledge Nexus"
            description = "Power and knowledge are inseparably intertwined - each produces the other"
            status = "Foucauldian"
        elif has_expert >= 1 or (has_knowledge >= 1 and has_truth >= 1):
            relation = "Expert Knowledge as Power"
            description = "Knowledge claims function as techniques of power"
            status = "Disciplinary"
        elif has_power >= 2 and has_knowledge == 0:
            relation = "Power without Knowledge"
            description = "Power conceived without its knowledge dimension"
            status = "Incomplete"
        elif has_knowledge >= 2 and has_power == 0:
            relation = "Knowledge without Power"
            description = "Knowledge conceived as neutral, separate from power"
            status = "Traditional (Pre-Foucauldian)"
        else:
            relation = "Unclear"
            description = "Power/knowledge relation unclear"
            status = "Indeterminate"

        return {
            "relation": relation,
            "description": description,
            "status": status,
            "principle": "There is no power relation without the correlative constitution of a field of knowledge",
        }

    def _analyze_discourse(self, text: str) -> Dict[str, Any]:
        """
        Analyze discourse.

        Discourse: System of statements that construct objects, subjects, and truths.
        Not just language, but practices determining what can be said and thought.
        """
        text_lower = text.lower()

        # Discourse indicators
        discourse_words = [
            "discourse",
            "language",
            "statement",
            "speech",
            "say",
            "speak",
            "talk",
        ]
        has_discourse = sum(1 for word in discourse_words if word in text_lower)

        # Rules/norms indicators
        rules_words = [
            "rule",
            "norm",
            "regulation",
            "standard",
            "convention",
            "acceptable",
        ]
        has_rules = sum(1 for word in rules_words if word in text_lower)

        # Exclusion/prohibition indicators
        exclusion_words = [
            "exclude",
            "prohibit",
            "forbidden",
            "cannot say",
            "unspeakable",
            "taboo",
        ]
        has_exclusion = sum(1 for word in exclusion_words if word in text_lower)

        # Truth production indicators
        truth_prod = [
            "produce truth",
            "construct",
            "constitute",
            "create meaning",
            "define",
        ]
        has_truth_prod = sum(1 for phrase in truth_prod if phrase in text_lower)

        # What can be said/thought
        sayable_words = [
            "what can be said",
            "thinkable",
            "intelligible",
            "make sense",
            "possible to",
        ]
        has_sayable = sum(1 for phrase in sayable_words if phrase in text_lower)

        if has_discourse >= 1 and (has_rules >= 1 or has_exclusion >= 1):
            type_discourse = "Discursive Formation"
            description = "System of rules determining what can be said, who can speak, and what counts as truth"
            regime = "Constitutive"
        elif has_truth_prod >= 1 or has_sayable >= 1:
            type_discourse = "Truth Production"
            description = "Discourse actively produces truths and objects, not just represents them"
            regime = "Productive"
        elif has_exclusion >= 2:
            type_discourse = "Discursive Exclusion"
            description = "Discourse operates through exclusion and prohibition"
            regime = "Prohibitive"
        elif has_discourse >= 1:
            type_discourse = "Language Use"
            description = "Simple language use - not yet Foucauldian discourse analysis"
            regime = "Traditional"
        else:
            type_discourse = "Unclear"
            description = "Discourse status unclear"
            regime = "Indeterminate"

        return {
            "type": type_discourse,
            "description": description,
            "regime": regime,
            "principle": "Discourse produces the objects of which it speaks",
        }

    def _assess_disciplinary_power(self, text: str) -> Dict[str, Any]:
        """
        Assess disciplinary power.

        Disciplinary power: Operates through surveillance, normalization, and examination.
        Creates docile bodies. Emerged in 17th-18th centuries (military, schools, hospitals).
        """
        text_lower = text.lower()

        # Surveillance indicators
        surveillance_words = [
            "surveillance",
            "watch",
            "monitor",
            "observe",
            "inspect",
            "supervise",
            "track",
        ]
        has_surveillance = sum(1 for word in surveillance_words if word in text_lower)

        # Normalization indicators
        normalization_words = [
            "normal",
            "abnormal",
            "deviant",
            "standard",
            "average",
            "normalize",
        ]
        has_normalization = sum(1 for word in normalization_words if word in text_lower)

        # Examination indicators
        examination_words = [
            "examination",
            "test",
            "evaluate",
            "assess",
            "measure",
            "grade",
            "rank",
        ]
        has_examination = sum(1 for word in examination_words if word in text_lower)

        # Institutional indicators
        institution_words = [
            "school",
            "prison",
            "hospital",
            "army",
            "factory",
            "clinic",
            "asylum",
        ]
        has_institution = sum(1 for word in institution_words if word in text_lower)

        # Docile bodies indicators
        docile_words = [
            "obedient",
            "compliant",
            "disciplined",
            "trained",
            "controlled",
            "docile",
        ]
        sum(1 for word in docile_words if word in text_lower)

        # Timetable/organization indicators
        organization_words = [
            "schedule",
            "timetable",
            "organize",
            "regulate",
            "routine",
            "ordered",
        ]
        sum(1 for word in organization_words if word in text_lower)

        discipline_score = has_surveillance + has_normalization + has_examination

        if discipline_score >= 2:
            presence = "Strong Disciplinary Power"
            description = "Operates through surveillance, normalization, and examination - produces docile bodies"
            mechanism = "Panoptic"
        elif has_institution >= 1 and discipline_score >= 1:
            presence = "Institutional Discipline"
            description = "Disciplinary mechanisms operating in institutional contexts"
            mechanism = "Institutional"
        elif has_normalization >= 2:
            presence = "Normalizing Power"
            description = "Power operates through norm and deviation from norm"
            mechanism = "Normalizing"
        elif discipline_score >= 1:
            presence = "Emerging Discipline"
            description = "Elements of disciplinary power present"
            mechanism = "Partial"
        else:
            presence = "No Clear Discipline"
            description = "Disciplinary power not evident"
            mechanism = "Absent"

        return {
            "presence": presence,
            "description": description,
            "mechanism": mechanism,
            "principle": "Discipline produces subjected and practiced bodies, 'docile' bodies",
        }

    def _check_panopticon(self, text: str) -> Dict[str, Any]:
        """
        Check for panopticon.

        Panopticon: Bentham's prison design - central tower, peripheral cells.
        Visibility assures automatic functioning of power.
        Model for modern disciplinary society.
        """
        text_lower = text.lower()

        # Panopticon direct indicators
        panopticon_words = ["panopticon", "bentham", "central tower", "visibility"]
        has_panopticon = sum(1 for phrase in panopticon_words if phrase in text_lower)

        # Visibility/seeing indicators
        visibility_words = [
            "visible",
            "see",
            "seen",
            "visibility",
            "transparent",
            "exposed",
        ]
        has_visibility = sum(1 for word in visibility_words if word in text_lower)

        # Surveillance/observation
        surveillance_words = [
            "surveillance",
            "watch",
            "observe",
            "monitor",
            "gaze",
            "look",
        ]
        has_surveillance = sum(1 for word in surveillance_words if word in text_lower)

        # Internalization indicators
        internalize_words = [
            "internalize",
            "self-regulate",
            "self-monitor",
            "assume",
            "feel watched",
        ]
        has_internalize = sum(1 for phrase in internalize_words if phrase in text_lower)

        # Automatic functioning
        automatic_words = ["automatic", "constant", "always", "permanent", "continuous"]
        sum(1 for word in automatic_words if word in text_lower)

        if has_panopticon >= 1:
            presence = "Direct Panopticon"
            description = "Explicit panoptic mechanism - visibility ensures power"
            model = "Benthamite"
        elif has_visibility >= 1 and has_surveillance >= 1:
            presence = "Panoptic Logic"
            description = (
                "Operates through visibility and surveillance - induces self-regulation"
            )
            model = "Panoptic"
        elif has_internalize >= 1:
            presence = "Internalized Surveillance"
            description = "Power internalized through assumption of constant visibility"
            model = "Self-disciplining"
        elif has_surveillance >= 2 or has_visibility >= 2:
            presence = "Surveillance Society"
            description = "Elements of panoptic surveillance present"
            model = "Surveillant"
        else:
            presence = "No Panopticon"
            description = "Panoptic mechanisms not evident"
            model = "Non-panoptic"

        return {
            "presence": presence,
            "description": description,
            "model": model,
            "principle": "He who is subjected to a field of visibility inscribes in himself the power relation",
        }

    def _analyze_biopower(self, text: str) -> Dict[str, Any]:
        """
        Analyze biopower/biopolitics.

        Biopower: Power over life itself, emerged 18th-19th centuries.
        Anatomo-politics (individual body) + biopolitics (population).
        Management of life: birth rates, death rates, health, hygiene, reproduction.
        """
        text_lower = text.lower()

        # Life/biological indicators
        life_words = [
            "life",
            "death",
            "birth",
            "health",
            "disease",
            "body",
            "biological",
        ]
        has_life = sum(1 for word in life_words if word in text_lower)

        # Population indicators
        population_words = [
            "population",
            "demographic",
            "birthrate",
            "mortality",
            "public health",
            "epidemic",
        ]
        has_population = sum(1 for word in population_words if word in text_lower)

        # Management/regulation indicators
        management_words = [
            "manage",
            "regulate",
            "control",
            "optimize",
            "administer",
            "govern",
        ]
        has_management = sum(1 for word in management_words if word in text_lower)

        # Medical/health indicators
        medical_words = [
            "medicine",
            "medical",
            "doctor",
            "hospital",
            "clinic",
            "treatment",
            "cure",
        ]
        has_medical = sum(1 for word in medical_words if word in text_lower)

        # Race/species indicators
        race_words = ["race", "species", "genetic", "heredity", "breeding", "eugenics"]
        has_race = sum(1 for word in race_words if word in text_lower)

        # Statistics/knowledge of population
        stats_words = ["statistics", "data", "measure", "calculate", "quantify", "rate"]
        has_stats = sum(1 for word in stats_words if word in text_lower)

        if has_population >= 1 and has_management >= 1:
            type_biopower = "Biopolitics"
            description = (
                "Power over populations - regulation of life processes at species level"
            )
            level = "Population"
        elif has_life >= 1 and has_medical >= 1:
            type_biopower = "Anatomo-politics"
            description = (
                "Power over individual bodies - optimization of life and health"
            )
            level = "Individual Body"
        elif has_race >= 1 or (has_population >= 1 and has_stats >= 1):
            type_biopower = "Biopower Regime"
            description = (
                "Knowledge and management of life - making live and letting die"
            )
            level = "Biopolitical"
        elif has_medical >= 2:
            type_biopower = "Medical Power"
            description = "Medical/clinical power over bodies and health"
            level = "Clinical"
        else:
            type_biopower = "No Clear Biopower"
            description = "Biopower not evident"
            level = "Absent"

        return {
            "type": type_biopower,
            "description": description,
            "level": level,
            "principle": "Biopower: the power to make live and let die (vs sovereign power: take life or let live)",
        }

    def _check_archaeology(self, text: str) -> Dict[str, Any]:
        """
        Check archaeological method.

        Archaeology: Analyzes conditions making discourse possible.
        Not history of ideas, but historical a priori.
        What rules allow certain statements to emerge as true?
        """
        text_lower = text.lower()

        # Archaeological method indicators
        archaeology_words = [
            "archaeology",
            "archaeological",
            "archive",
            "historical a priori",
        ]
        has_archaeology = sum(1 for phrase in archaeology_words if phrase in text_lower)

        # Conditions of possibility
        conditions_words = [
            "conditions",
            "possibility",
            "possible",
            "allow",
            "enable",
            "permit",
        ]
        has_conditions = sum(1 for word in conditions_words if word in text_lower)

        # Discourse formation
        formation_words = ["formation", "emerge", "appear", "arise", "constitute"]
        has_formation = sum(1 for word in formation_words if word in text_lower)

        # Rules/system indicators
        rules_words = ["rule", "system", "structure", "order", "organize", "regulate"]
        has_rules = sum(1 for word in rules_words if word in text_lower)

        # Discontinuity indicators (vs continuous history)
        discontinuity_words = [
            "discontinuity",
            "break",
            "rupture",
            "shift",
            "transformation",
        ]
        has_discontinuity = sum(1 for word in discontinuity_words if word in text_lower)

        if has_archaeology >= 1:
            method = "Archaeological"
            description = "Analyzing conditions of possibility for discourse formation"
            approach = "Foucauldian Archaeology"
        elif has_conditions >= 1 and has_formation >= 1:
            method = "Conditions Analysis"
            description = "Examining what makes certain statements possible"
            approach = "Archaeological tendency"
        elif has_discontinuity >= 1:
            method = "Discontinuous History"
            description = "History as ruptures and transformations, not continuity"
            approach = "Anti-continuous"
        elif has_rules >= 1 and has_formation >= 1:
            method = "Systems Analysis"
            description = "Analyzing systematic rules and formations"
            approach = "Structural"
        else:
            method = "No Archaeology"
            description = "Archaeological method not evident"
            approach = "Non-archaeological"

        return {
            "method": method,
            "description": description,
            "approach": approach,
            "principle": "Archaeology describes discourses as practices specified by rules of formation",
        }

    def _check_genealogy(self, text: str) -> Dict[str, Any]:
        """
        Check genealogical method.

        Genealogy: Nietzsche-inspired. History of the present, not origins.
        Traces contingent emergence, not necessary development.
        Shows how present is result of power struggles, accidents, not inevitability.
        """
        text_lower = text.lower()

        # Genealogy direct indicators
        genealogy_words = ["genealogy", "genealogical", "nietzsche"]
        has_genealogy = sum(1 for word in genealogy_words if word in text_lower)

        # Contingency indicators
        contingency_words = [
            "contingent",
            "accident",
            "chance",
            "arbitrary",
            "could have been otherwise",
        ]
        has_contingency = sum(1 for phrase in contingency_words if phrase in text_lower)

        # Historical emergence (not origin)
        emergence_words = ["emergence", "emerge", "arose", "came to be", "developed"]
        has_emergence = sum(1 for word in emergence_words if word in text_lower)

        # Power struggle indicators
        struggle_words = [
            "struggle",
            "conflict",
            "battle",
            "fight",
            "contest",
            "domination",
        ]
        has_struggle = sum(1 for word in struggle_words if word in text_lower)

        # Present/history of present
        present_words = ["present", "now", "today", "current", "contemporary"]
        has_present = sum(1 for word in present_words if word in text_lower)

        # Anti-origin indicators
        anti_origin = [
            "no origin",
            "not original",
            "not natural",
            "constructed",
            "invented",
        ]
        has_anti_origin = sum(1 for phrase in anti_origin if phrase in text_lower)

        if has_genealogy >= 1 or (has_contingency >= 1 and has_emergence >= 1):
            method = "Genealogical"
            description = (
                "Tracing contingent historical emergence - history of the present"
            )
            approach = "Nietzschean Genealogy"
        elif has_struggle >= 1 and has_emergence >= 1:
            method = "Power History"
            description = "History as power struggles and contingent outcomes"
            approach = "Genealogical tendency"
        elif has_anti_origin >= 1:
            method = "Anti-Origin"
            description = "Rejecting natural origins - showing historical construction"
            approach = "Constructivist"
        elif has_emergence >= 1 and has_present >= 1:
            method = "History of Present"
            description = "Examining how present emerged historically"
            approach = "Historical"
        else:
            method = "No Genealogy"
            description = "Genealogical method not evident"
            approach = "Non-genealogical"

        return {
            "method": method,
            "description": description,
            "approach": approach,
            "principle": "Genealogy: gray, meticulous, documentary - history of the present, not origins",
        }

    def _analyze_subjectivation(self, text: str) -> Dict[str, Any]:
        """
        Analyze subject/subjectivation.

        Subjectivation: Process by which subjects are produced through power relations.
        Subject as both subjected to others (assujettissement) and
        tied to own identity through self-knowledge.
        """
        text_lower = text.lower()

        # Subject/self indicators
        subject_words = [
            "subject",
            "self",
            "identity",
            "individual",
            "person",
            "who i am",
        ]
        has_subject = sum(1 for phrase in subject_words if phrase in text_lower)

        # Production/constitution indicators
        production_words = [
            "produce",
            "constitute",
            "create",
            "form",
            "make",
            "construct",
        ]
        has_production = sum(1 for word in production_words if word in text_lower)

        # Subjection indicators (subjected to)
        subjection_words = [
            "subjected",
            "submission",
            "obedience",
            "control",
            "dominated",
        ]
        has_subjection = sum(1 for word in subjection_words if word in text_lower)

        # Self-knowledge indicators
        self_knowledge = [
            "know myself",
            "self-knowledge",
            "introspection",
            "examine myself",
            "confession",
        ]
        has_self_knowledge = sum(1 for phrase in self_knowledge if phrase in text_lower)

        # Identity formation
        formation_words = [
            "become",
            "formation",
            "shaped",
            "molded",
            "fashioned",
            "develop",
        ]
        has_formation = sum(1 for word in formation_words if word in text_lower)

        # Technologies of self
        tech_self = [
            "practice",
            "technique",
            "exercise",
            "discipline myself",
            "work on myself",
        ]
        has_tech_self = sum(1 for phrase in tech_self if phrase in text_lower)

        if has_subject >= 1 and has_production >= 1:
            process = "Subject Production"
            description = "Subjects are produced through discourse and power relations, not pre-given"
            mode = "Constitutive"
        elif has_subjection >= 1 or (has_subject >= 1 and has_self_knowledge >= 1):
            process = "Double Subjection"
            description = "Subject as both subjected to power and tied to own identity"
            mode = "Assujettissement"
        elif has_tech_self >= 1:
            process = "Technologies of Self"
            description = "Techniques through which individuals act upon themselves"
            mode = "Self-formation"
        elif has_formation >= 1:
            process = "Identity Formation"
            description = "Process of becoming a particular kind of subject"
            mode = "Formative"
        else:
            process = "Unclear"
            description = "Subjectivation process unclear"
            mode = "Indeterminate"

        return {
            "process": process,
            "description": description,
            "mode": mode,
            "principle": "The subject is a form, not a substance - produced through historical practices",
        }

    def _assess_governmentality(self, text: str) -> Dict[str, Any]:
        """
        Assess governmentality.

        Governmentality: The art of government, conduct of conduct.
        How to govern oneself, others, the state, populations.
        Neoliberalism as form of governmentality - making individuals entrepreneurs of self.
        """
        text_lower = text.lower()

        # Government/govern indicators
        govern_words = ["govern", "government", "rule", "administrate", "manage"]
        has_govern = sum(1 for word in govern_words if word in text_lower)

        # Conduct indicators
        conduct_words = ["conduct", "behavior", "act", "behave", "guide", "direct"]
        has_conduct = sum(1 for word in conduct_words if word in text_lower)

        # Self-government indicators
        self_govern = [
            "self-govern",
            "self-regulate",
            "self-control",
            "govern myself",
            "self-management",
        ]
        has_self_govern = sum(1 for phrase in self_govern if phrase in text_lower)

        # Population/state indicators
        pop_state = ["population", "state", "society", "public", "collective"]
        has_pop_state = sum(1 for word in pop_state if word in text_lower)

        # Neoliberal indicators
        neoliberal_words = [
            "market",
            "entrepreneur",
            "competition",
            "choice",
            "responsibility",
            "investment",
        ]
        has_neoliberal = sum(1 for word in neoliberal_words if word in text_lower)

        # Rationality/calculation
        rationality_words = [
            "rationality",
            "calculate",
            "optimize",
            "efficiency",
            "rational",
        ]
        sum(1 for word in rationality_words if word in text_lower)

        if has_govern >= 1 and has_conduct >= 1:
            type_gov = "Governmentality"
            description = "Conduct of conduct - how conduct is directed and shaped"
            rationality = "Governmental"
        elif has_self_govern >= 1:
            type_gov = "Self-Government"
            description = "Governing oneself according to certain rationalities"
            rationality = "Self-regulatory"
        elif has_neoliberal >= 2:
            type_gov = "Neoliberal Governmentality"
            description = (
                "Individuals as entrepreneurs of themselves - self as enterprise"
            )
            rationality = "Neoliberal"
        elif has_govern >= 1 and has_pop_state >= 1:
            type_gov = "State Governmentality"
            description = "Government of populations and territories"
            rationality = "State"
        else:
            type_gov = "Unclear"
            description = "Governmentality unclear"
            rationality = "Indeterminate"

        return {
            "type": type_gov,
            "description": description,
            "rationality": rationality,
            "principle": "Governmentality: the conduct of conduct - how to govern and be governed",
        }

    def _check_care_of_self(self, text: str) -> Dict[str, Any]:
        """
        Check care of the self.

        Care of the Self (souci de soi): Ancient Greek/Roman ethics.
        Ethics as aesthetics of existence - making life a work of art.
        Not obedience to moral code, but self-formation through practices.
        """
        text_lower = text.lower()

        # Care of self direct indicators
        care_self = [
            "care of self",
            "care of myself",
            "souci de soi",
            "epimeleia heautou",
        ]
        has_care_self = sum(1 for phrase in care_self if phrase in text_lower)

        # Self-practice indicators
        practice_words = [
            "practice",
            "exercise",
            "cultivate",
            "work on myself",
            "train",
        ]
        has_practice = sum(1 for phrase in practice_words if phrase in text_lower)

        # Aesthetics of existence
        aesthetic_words = [
            "art",
            "beauty",
            "style",
            "craft",
            "aesthetic",
            "create myself",
        ]
        has_aesthetic = sum(1 for phrase in aesthetic_words if phrase in text_lower)

        # Ancient ethics indicators
        ancient_words = ["greek", "ancient", "stoic", "epicurean", "philosophical life"]
        sum(1 for phrase in ancient_words if phrase in text_lower)

        # Self-transformation
        transform_words = [
            "transform",
            "change myself",
            "become",
            "fashioning",
            "shaping",
        ]
        has_transform = sum(1 for phrase in transform_words if phrase in text_lower)

        # Moral code (opposed to care of self)
        code_words = ["obey", "rule", "command", "law", "must", "obligation", "duty"]
        has_code = sum(1 for word in code_words if word in text_lower)

        if has_care_self >= 1:
            presence = "Care of Self"
            description = (
                "Ethics as aesthetic self-formation - making life a work of art"
            )
            ethics_type = "Greek/Roman"
        elif has_aesthetic >= 1 and has_practice >= 1:
            presence = "Aesthetic Existence"
            description = "Ethics as aesthetics - self as work of art"
            ethics_type = "Aesthetic"
        elif has_practice >= 1 and has_transform >= 1:
            presence = "Self-Cultivation"
            description = "Working on self through practices and exercises"
            ethics_type = "Practice-based"
        elif has_code >= 2:
            presence = "Moral Code"
            description = "Ethics as obedience to rules - Christian/modern model"
            ethics_type = "Code-based"
        else:
            presence = "Unclear"
            description = "Care of self status unclear"
            ethics_type = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "ethics_type": ethics_type,
            "principle": "Make your life a work of art - ethics as aesthetics of existence",
        }

    def _identify_episteme(self, text: str) -> Dict[str, Any]:
        """
        Identify episteme.

        Episteme: Underlying epistemological framework of an era.
        Not worldview, but conditions determining what counts as knowledge.
        Renaissance, Classical, Modern epistemes (The Order of Things).
        """
        text_lower = text.lower()

        # Episteme direct indicators
        episteme_words = ["episteme", "epistemological", "framework", "order of things"]
        has_episteme = sum(1 for phrase in episteme_words if phrase in text_lower)

        # Era/period indicators
        era_words = ["era", "age", "period", "epoch", "time", "modern", "classical"]
        sum(1 for word in era_words if word in text_lower)

        # Knowledge/thought indicators
        knowledge_words = ["knowledge", "thought", "thinking", "know", "understand"]
        has_knowledge = sum(1 for word in knowledge_words if word in text_lower)

        # Underlying/fundamental
        fundamental_words = [
            "underlying",
            "fundamental",
            "basis",
            "foundation",
            "ground",
            "deep",
        ]
        has_fundamental = sum(1 for word in fundamental_words if word in text_lower)

        # Order/organization
        order_words = [
            "order",
            "organize",
            "arrange",
            "classify",
            "system",
            "structure",
        ]
        sum(1 for word in order_words if word in text_lower)

        # Specific epistemes
        renaissance_words = [
            "renaissance",
            "resemblance",
            "similarity",
            "correspondence",
        ]
        classical_words = ["classical", "representation", "table", "taxonomy", "order"]
        modern_words = ["modern", "man", "human sciences", "finitude", "anthropology"]

        has_renaissance = sum(1 for word in renaissance_words if word in text_lower)
        has_classical = sum(1 for word in classical_words if word in text_lower)
        has_modern = sum(1 for word in modern_words if word in text_lower)

        if has_episteme >= 1:
            type_episteme = "Episteme"
            description = (
                "Underlying epistemological framework organizing knowledge in an era"
            )
            period = "Explicit"
        elif has_renaissance >= 2:
            type_episteme = "Renaissance Episteme"
            description = "Knowledge organized through resemblance and similitude"
            period = "Renaissance (16th century)"
        elif has_classical >= 2:
            type_episteme = "Classical Episteme"
            description = "Knowledge organized through representation and taxonomy"
            period = "Classical Age (17th-18th century)"
        elif has_modern >= 2:
            type_episteme = "Modern Episteme"
            description = (
                "Knowledge organized around Man as empirical-transcendental doublet"
            )
            period = "Modern (19th-20th century)"
        elif has_fundamental >= 1 and has_knowledge >= 1:
            type_episteme = "Epistemological Framework"
            description = "Fundamental framework organizing knowledge and thought"
            period = "Unspecified"
        else:
            type_episteme = "Unclear"
            description = "Episteme unclear"
            period = "Indeterminate"

        return {
            "type": type_episteme,
            "description": description,
            "period": period,
            "principle": "Episteme: the strategic apparatus which permits separating out true from false statements",
        }

    def _construct_reasoning(
        self,
        power_knowledge: Dict[str, Any],
        discourse: Dict[str, Any],
        disciplinary_power: Dict[str, Any],
        biopower: Dict[str, Any],
        subjectivation: Dict[str, Any],
    ) -> str:
        """Construct Foucauldian genealogical/archaeological reasoning."""
        reasoning = (
            f"From a Foucauldian perspective, power/knowledge operates as: {power_knowledge['description']}. "
            f"Discourse: {discourse['description']}. "
            f"Disciplinary mechanisms: {disciplinary_power['description']}. "
        )

        # Add biopower
        reasoning += f"Biopower: {biopower['description']}. "

        # Add subjectivation
        reasoning += f"Subjectivation: {subjectivation['description']}. "

        # Conclude with Foucauldian principles
        reasoning += (
            "Remember: Power is everywhere, not because it embraces everything, but because it comes from everywhere. "
            "Knowledge and power are integrated with one another. "
            "Where there is power, there is resistance."
        )

        return reasoning
