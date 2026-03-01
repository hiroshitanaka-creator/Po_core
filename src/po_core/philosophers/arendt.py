"""
Hannah Arendt Philosopher Module

Hannah Arendt (1906-1975) was a German-American political philosopher known for her
analysis of totalitarianism, the nature of political action, and the human condition.

Key Concepts:
1. Vita Activa - Three modes of human activity:
   - Labor: Biological necessity (life process)
   - Work: Fabrication of lasting world
   - Action: Political activity, beginning new things

2. Natality - The human capacity for new beginnings, birth of the new

3. Public vs Private Realm:
   - Public: Space of appearance, political action
   - Private: Realm of necessity and intimacy

4. Plurality - The human condition of living together as distinct beings

5. Banality of Evil - Evil can be thoughtless, ordinary bureaucratic behavior

6. Totalitarianism - Domination through terror and ideology

7. Political Judgment - Faculty of thinking and judging in the public sphere

8. Freedom - Freedom realized through action in the public realm
"""

from typing import Any, Dict

from po_core.philosophers.base import Philosopher


class Arendt(Philosopher):
    """
    Hannah Arendt: Political philosopher of action, natality, and the human condition.

    Arendt's philosophy centers on the vita activa (active life) and the importance
    of political action in the public sphere. She emphasizes human plurality, natality
    (the capacity for new beginnings), and the distinction between public and private
    realms.
    """

    def __init__(self):
        super().__init__(
            name="Hannah Arendt",
            description="Political philosopher analyzing action, natality, plurality, and the human condition in the public sphere",
        )
        self.tradition = "Political Philosophy"
        self.key_concepts = [
            "vita activa",
            "natality",
            "plurality",
            "banality of evil",
            "public realm",
        ]

    def reason(
        self, text: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Analyze text through Arendtian political philosophy.

        Args:
            text: The text to analyze
            context: Optional context dictionary

        Returns:
            Dictionary containing Arendtian analysis
        """
        vita_activa = self._analyze_vita_activa(text)
        natality = self._assess_natality(text)
        public_private = self._detect_public_private(text)
        plurality = self._evaluate_plurality(text)
        evil_analysis = self._analyze_evil(text)
        totalitarian = self._detect_totalitarian(text)
        judgment = self._assess_judgment(text)
        freedom = self._evaluate_freedom(text)

        summary = self._generate_summary(
            vita_activa,
            natality,
            public_private,
            plurality,
            evil_analysis,
            totalitarian,
            judgment,
            freedom,
        )
        summary = self._apply_arendt_to_problem(text) + " " + summary

        tension = self._calculate_tension(
            vita_activa,
            natality,
            public_private,
            plurality,
            evil_analysis,
            totalitarian,
            judgment,
            freedom,
        )

        return {
            # Standard contract keys
            "reasoning": summary,
            "perspective": "Political Philosophy / Vita Activa",
            "tension": tension,
            "metadata": {"philosopher": self.name},
            # Philosopher-specific concept analyses
            "vita_activa": vita_activa,
            "natality": natality,
            "public_private_realm": public_private,
            "plurality": plurality,
            "evil_analysis": evil_analysis,
            "totalitarian_elements": totalitarian,
            "political_judgment": judgment,
            "freedom": freedom,
            # Backward-compat keys (used by existing tests)
            "philosopher": self.name,
            "description": self.description,
            "analysis": {
                "vita_activa": vita_activa,
                "natality": natality,
                "public_private_realm": public_private,
                "plurality": plurality,
                "evil_analysis": evil_analysis,
                "totalitarian_elements": totalitarian,
                "political_judgment": judgment,
                "freedom": freedom,
            },
            "summary": summary,
        }

    def _analyze_vita_activa(self, text: str) -> Dict[str, Any]:
        """
        Analyze the vita activa: Labor, Work, Action.

        Labor - biological necessity, cyclical, leaves no lasting trace
        Work - fabrication, creates durable world of things
        Action - political activity, reveals who we are, begins something new
        """
        text_lower = text.lower()

        # Labor indicators - biological necessity, repetition, consumption
        labor_words = [
            "labor",
            "work",
            "necessity",
            "biological",
            "survival",
            "consumption",
            "eat",
            "sleep",
            "maintain",
            "routine",
            "repetitive",
            "cycle",
            "metabolic",
            "body",
            "need",
        ]

        # Work indicators - fabrication, durability, object world
        work_words = [
            "build",
            "create",
            "make",
            "fabricate",
            "produce",
            "artifact",
            "tool",
            "craft",
            "construct",
            "design",
            "permanent",
            "durable",
            "world",
            "object",
            "thing",
        ]

        # Action indicators - political activity, beginning, appearing
        action_words = [
            "act",
            "action",
            "political",
            "public",
            "together",
            "begin",
            "start",
            "initiative",
            "speech",
            "appear",
            "reveal",
            "show",
            "citizen",
            "community",
            "collective",
        ]

        labor_score = sum(1 for word in labor_words if word in text_lower)
        work_score = sum(1 for word in work_words if word in text_lower)
        action_score = sum(1 for word in action_words if word in text_lower)

        dominant = "labor"
        if work_score > labor_score and work_score > action_score:
            dominant = "work"
        elif action_score > labor_score and action_score > work_score:
            dominant = "action"

        return {
            "dominant_mode": dominant,
            "labor_present": labor_score > 0,
            "work_present": work_score > 0,
            "action_present": action_score > 0,
            "scores": {
                "labor": labor_score,
                "work": work_score,
                "action": action_score,
            },
            "interpretation": self._interpret_vita_activa(
                dominant, labor_score, work_score, action_score
            ),
        }

    def _interpret_vita_activa(
        self, dominant: str, labor: int, work: int, action: int
    ) -> str:
        """Interpret the vita activa analysis."""
        if dominant == "action":
            return "Text emphasizes political action - the highest form of human activity, revealing who we are through speech and deeds in the public sphere."
        elif dominant == "work":
            return "Text emphasizes fabrication and worldbuilding - creating durable objects that constitute our shared world."
        else:
            return "Text emphasizes labor - the biological necessity of maintaining life, the endless cycle of production and consumption."

    def _assess_natality(self, text: str) -> Dict[str, Any]:
        """
        Assess natality - the human capacity for new beginnings.

        Natality is Arendt's concept of birth as the human capacity to begin
        something new, to initiate action. It counters the traditional philosophical
        emphasis on mortality.
        """
        text_lower = text.lower()

        natality_words = [
            "new",
            "begin",
            "beginning",
            "start",
            "birth",
            "born",
            "initiative",
            "initiate",
            "novel",
            "create",
            "emerge",
            "first",
            "original",
            "fresh",
            "innovation",
            "possibility",
        ]

        has_natality = sum(1 for word in natality_words if word in text_lower)
        natality_present = has_natality >= 2

        return {
            "natality_present": natality_present,
            "new_beginning_capacity": natality_present,
            "score": has_natality,
            "interpretation": (
                "Text expresses natality - the capacity to begin something new, the miracle of action."
                if natality_present
                else "Text shows limited emphasis on new beginnings or natality."
            ),
        }

    def _detect_public_private(self, text: str) -> Dict[str, Any]:
        """
        Detect public vs private realm.

        Public realm - space of appearance, political action, plurality
        Private realm - household, necessity, intimacy, property
        """
        text_lower = text.lower()

        public_words = [
            "public",
            "political",
            "citizen",
            "community",
            "together",
            "common",
            "shared",
            "collective",
            "society",
            "state",
            "democracy",
            "republic",
            "civic",
            "assembly",
            "appearance",
        ]

        private_words = [
            "private",
            "personal",
            "individual",
            "home",
            "family",
            "household",
            "intimate",
            "secret",
            "property",
            "own",
            "alone",
            "self",
            "inner",
            "domestic",
            "privacy",
        ]

        public_score = sum(1 for word in public_words if word in text_lower)
        private_score = sum(1 for word in private_words if word in text_lower)

        dominant_realm = (
            "public"
            if public_score > private_score
            else "private" if private_score > public_score else "balanced"
        )

        return {
            "dominant_realm": dominant_realm,
            "public_score": public_score,
            "private_score": private_score,
            "public_present": public_score > 0,
            "private_present": private_score > 0,
            "interpretation": self._interpret_realm(
                dominant_realm, public_score, private_score
            ),
        }

    def _interpret_realm(self, dominant: str, public: int, private: int) -> str:
        """Interpret the public/private realm analysis."""
        if dominant == "public":
            return "Text emphasizes the public realm - the space of appearance where action and speech reveal who we are as political beings."
        elif dominant == "private":
            return "Text emphasizes the private realm - the sphere of necessity, intimacy, and property, hidden from public view."
        else:
            return "Text balances public and private realms - recognizing both the political sphere and the realm of necessity."

    def _evaluate_plurality(self, text: str) -> Dict[str, Any]:
        """
        Evaluate plurality - the human condition of living together as distinct beings.

        Plurality is the condition of human action: we are all human but no two
        people are ever the same. This distinctness is revealed through speech and action.
        """
        text_lower = text.lower()

        plurality_words = [
            "plural",
            "plurality",
            "diverse",
            "different",
            "distinct",
            "together",
            "others",
            "multiple",
            "various",
            "many",
            "unique",
            "individual",
            "collective",
            "community",
            "differences",
        ]

        has_plurality = sum(1 for word in plurality_words if word in text_lower)
        plurality_present = has_plurality >= 2

        return {
            "plurality_present": plurality_present,
            "living_together": plurality_present,
            "score": has_plurality,
            "interpretation": (
                "Text acknowledges plurality - humans living together as distinct beings, the condition of political action."
                if plurality_present
                else "Text shows limited recognition of plurality and human distinctness."
            ),
        }

    def _analyze_evil(self, text: str) -> Dict[str, Any]:
        """
        Analyze evil - particularly the banality of evil.

        Arendt's concept from her Eichmann study: evil can be thoughtless,
        ordinary bureaucratic behavior without reflection or moral consideration.
        """
        text_lower = text.lower()

        evil_words = ["evil", "wrong", "immoral", "bad", "wicked", "harm"]
        banal_words = [
            "banal",
            "ordinary",
            "routine",
            "bureaucratic",
            "thoughtless",
            "unthinking",
            "normal",
            "everyday",
            "conventional",
            "system",
            "procedure",
            "process",
            "duty",
            "orders",
            "obedience",
        ]

        has_evil = sum(1 for word in evil_words if word in text_lower)
        has_banal = sum(1 for word in banal_words if word in text_lower)

        banality_of_evil = has_evil > 0 and has_banal >= 2

        return {
            "evil_present": has_evil > 0,
            "banality_of_evil": banality_of_evil,
            "thoughtlessness": has_banal >= 2,
            "interpretation": (
                "Text suggests the banality of evil - evil as thoughtless, ordinary behavior within systems."
                if banality_of_evil
                else (
                    "Evil as thoughtlessness not strongly present."
                    if has_banal >= 2
                    else "Limited engagement with evil or its ordinary nature."
                )
            ),
        }

    def _detect_totalitarian(self, text: str) -> Dict[str, Any]:
        """
        Detect totalitarian elements.

        Arendt's analysis: totalitarianism uses terror and ideology to dominate
        completely, destroying the public realm and human plurality.
        """
        text_lower = text.lower()

        totalitarian_words = [
            "totalitarian",
            "total",
            "domination",
            "control",
            "terror",
            "ideology",
            "propaganda",
            "dictator",
            "authoritarian",
            "tyranny",
            "oppression",
            "surveillance",
            "conform",
            "uniform",
            "mass",
        ]

        has_totalitarian = sum(1 for word in totalitarian_words if word in text_lower)
        totalitarian_present = has_totalitarian >= 2

        return {
            "totalitarian_elements": totalitarian_present,
            "score": has_totalitarian,
            "interpretation": (
                "Text shows totalitarian elements - domination through terror and ideology, destroying plurality."
                if totalitarian_present
                else "Limited totalitarian themes present."
            ),
        }

    def _assess_judgment(self, text: str) -> Dict[str, Any]:
        """
        Assess political judgment.

        Arendt's concept of judgment (influenced by Kant): the faculty of thinking
        and judging, especially in political matters. Thinking what we are doing.
        """
        text_lower = text.lower()

        judgment_words = [
            "judge",
            "judgment",
            "think",
            "thinking",
            "reflect",
            "consider",
            "deliberate",
            "reason",
            "evaluate",
            "assess",
            "understand",
            "comprehend",
            "examine",
            "question",
            "critical",
        ]

        has_judgment = sum(1 for word in judgment_words if word in text_lower)
        judgment_present = has_judgment >= 2

        return {
            "judgment_present": judgment_present,
            "thinking": judgment_present,
            "score": has_judgment,
            "interpretation": (
                "Text engages political judgment - thinking what we are doing, reflecting on action."
                if judgment_present
                else "Limited engagement with judgment or reflective thinking."
            ),
        }

    def _evaluate_freedom(self, text: str) -> Dict[str, Any]:
        """
        Evaluate freedom - freedom as political action in the public realm.

        For Arendt, freedom is not an inner state but is realized through
        action in the public political sphere.
        """
        text_lower = text.lower()

        freedom_words = [
            "freedom",
            "free",
            "liberty",
            "liberate",
            "autonomous",
            "independence",
            "self-govern",
            "choice",
            "spontaneous",
            "act",
        ]

        political_words = [
            "political",
            "public",
            "action",
            "together",
            "citizen",
            "community",
            "collective",
            "participate",
            "engage",
        ]

        has_freedom = sum(1 for word in freedom_words if word in text_lower)
        has_political = sum(1 for word in political_words if word in text_lower)

        political_freedom = has_freedom > 0 and has_political > 0

        return {
            "freedom_present": has_freedom > 0,
            "political_freedom": political_freedom,
            "freedom_score": has_freedom,
            "political_score": has_political,
            "interpretation": (
                "Text expresses political freedom - freedom realized through action in the public sphere."
                if political_freedom
                else (
                    "Freedom without strong political dimension."
                    if has_freedom > 0
                    else "Limited engagement with freedom."
                )
            ),
        }

    def _apply_arendt_to_problem(self, text: str) -> str:
        """Apply Arendt's philosophy proactively to the given problem."""
        t = text.lower()
        is_politics_public = any(
            w in t
            for w in [
                "politics",
                "public",
                "democrat",
                "citizen",
                "government",
                "debate",
                "assembly",
                "republic",
                "participat",
            ]
        )
        is_evil_wrongdoing = any(
            w in t
            for w in [
                "evil",
                "atrocity",
                "wrong",
                "harm",
                "crime",
                "perpetrat",
                "eichmann",
                "obedien",
                "bureauc",
            ]
        )
        is_totalitarianism = any(
            w in t
            for w in [
                "totalitar",
                "authoritar",
                "dictat",
                "fascism",
                "nazism",
                "stalinist",
                "terror",
                "propaganda",
                "regime",
            ]
        )
        is_freedom_action = any(
            w in t
            for w in [
                "freedom",
                "liberty",
                "action",
                "new beginning",
                "natality",
                "spontan",
                "initiative",
                "plural",
                "praxis",
            ]
        )
        is_technology_automation = any(
            w in t
            for w in [
                "technolog",
                "automat",
                "labor",
                "work",
                "job",
                "machine",
                "social",
                "consumer",
                "economy",
            ]
        )
        is_judgment_thinking = any(
            w in t
            for w in [
                "judgment",
                "think",
                "opinion",
                "perspect",
                "kant",
                "reflective",
                "conscience",
                "moral",
                "deliberat",
            ]
        )

        if is_politics_public:
            return (
                "Arendt's political philosophy insists that the public realm — the space of appearance "
                "where human beings gather as equals to speak and act — is irreducible to any other domain "
                "of human activity. Action (praxis), the highest form of the vita activa, is not the "
                "making of things (work) or the metabolism of biological life (labor) but the disclosure "
                "of who we are through deed and word in the presence of others. The political is therefore "
                "essentially plural: it exists only where there are many perspectives, many voices, "
                "genuine disagreement — for Arendt, unanimous agreement is not the perfection of politics "
                "but its destruction. The public realm cannot be reduced to economics, administration, or "
                "expert management without ceasing to be political in Arendt's sense; it requires the "
                "active participation of citizens whose natality — capacity for new beginnings — keeps "
                "political life from settling into mere repetition."
            )
        elif is_evil_wrongdoing:
            return (
                "Arendt's report on the Eichmann trial produced one of the most unsettling concepts in "
                "modern moral philosophy: the banality of evil. Eichmann was not a monster, a sadist, "
                "or an ideological fanatic — he was an efficient bureaucrat who had stopped thinking, "
                "who had abdicated the specifically human capacity for judgment in favor of rule-following "
                "and career advancement. Evil on this analysis is not the product of demonic will but "
                "of the failure to think — specifically, to think from others' perspectives, to exercise "
                "the reflective judgment that would have made Eichmann's actions impossible. The "
                "implication is deeply disturbing: the greatest danger is not the exceptional monster "
                "but the ordinary functionary who has made himself thoughtless, who has traded the "
                "discomfort of genuine thinking for the security of procedure. The obligation to think "
                "for oneself is not merely intellectual but moral and political."
            )
        elif is_totalitarianism:
            return (
                "Arendt's analysis of totalitarianism identifies it as a genuinely novel form of "
                "government — not merely tyranny or dictatorship but a system that seeks to destroy "
                "the very fabric of human plurality. Totalitarian movements render human beings "
                "superfluous: first the enemies, then the members, then anyone at all — because "
                "the logic of ideological consistency demands that the world conform to the idea, "
                "regardless of the human cost. What makes totalitarianism possible is not some "
                "aberration of human nature but the specific conditions of modernity: the collapse "
                "of class structures, the loneliness of mass society, the availability of terror "
                "as a permanent principle of government rather than a temporary instrument. Against "
                "totalitarianism, Arendt insists on plurality — the irreducible fact that the world "
                "is inhabited by many human beings, each unique, each capable of beginning something "
                "new, and that this plurality is not an obstacle to political life but its very ground."
            )
        elif is_freedom_action:
            return (
                "For Arendt, freedom is not an inner property of the will — not the freedom Rousseau "
                "sought in solitary self-legislation — but a worldly phenomenon that appears only when "
                "people act together in the public realm. Freedom is co-extensive with action: it exists "
                "in the moment of initiative, in the capacity to begin something unprecedented, to "
                "interrupt the causal chains of the world with a new beginning. Natality — the fact "
                "that each human being is born and thus brings genuine novelty into the world — is for "
                "Arendt the ontological ground of political freedom. Because each person is a beginning, "
                "politics is never fully determined; the future is never simply the projection of the "
                "present. This is both hopeful and demanding: it means that no situation is ever "
                "completely closed, but also that freedom is inseparable from the risk of action, "
                "whose consequences can never be fully controlled or predicted."
            )
        elif is_technology_automation:
            return (
                "Arendt analyzes modernity as characterized by the expansion of the social realm — "
                "neither genuinely public nor genuinely private — at the expense of both. Automation "
                "threatens to universalize the condition of the laborer: human beings reduced to "
                "biological metabolism, consuming and producing, with no participation in the public "
                "realm where action and speech can disclose who they are. A society of laborers without "
                "labor (the prospect of full automation) does not become a society of free citizens; "
                "it becomes a society of consumers with no public life, no space of appearance, no "
                "political freedom in Arendt's sense. The Human Condition is an extended argument that "
                "the reduction of human activity to labor and work — to making and consuming — at the "
                "expense of action destroys what is distinctively human about human existence, leaving "
                "only the biological cycle of production and consumption."
            )
        elif is_judgment_thinking:
            return (
                "Arendt's unfinished project on judgment, drawing on Kant's Critique of Judgment, "
                "identifies reflective judgment as the key political faculty: the capacity to think "
                "without predetermined concepts, to subsume the particular under a universal that does "
                "not yet exist and must be found in the judging itself. Political judgment is not "
                "deductive — it cannot simply apply general rules to cases — but requires enlarged "
                "mentality (Kant's erweiterte Denkungsart): the ability to think from others' "
                "standpoints without simply adopting them, to represent to oneself how the world "
                "appears from many perspectives. Thinking without banisters — Arendt's phrase for "
                "her own intellectual situation after the collapse of traditional authority — is the "
                "condition of genuine moral and political thinking in the modern world. The refusal "
                "to think in this way is not merely intellectual laziness but the precondition of "
                "the thoughtlessness that makes the banality of evil possible."
            )
        else:
            return (
                "Hannah Arendt's political philosophy is organized around the distinction between "
                "labor (biological life processes), work (fabricating a durable world), and action "
                "(speech and deed in the public realm) — the three modes of the vita activa. Action "
                "is highest because it is the domain of freedom, natality, and plurality: the "
                "distinctively human capacity to begin something new in the company of equals. "
                "The public realm — the space of appearance — is constituted by this plurality "
                "and destroyed whenever one voice, one perspective, one logic achieves total dominance. "
                "Natality, the fact of birth and new beginning, is for Arendt the fundamental human "
                "condition: the guarantee that the world need not remain as it is. The banality of evil "
                "— the Eichmann insight — reveals that the greatest moral and political danger is not "
                "demonic will but the abdication of thinking, the refusal of judgment, the retreat "
                "from the public realm into private ambition and bureaucratic procedure."
            )

    def _generate_summary(
        self,
        vita_activa: Dict[str, Any],
        natality: Dict[str, Any],
        public_private: Dict[str, Any],
        plurality: Dict[str, Any],
        evil_analysis: Dict[str, Any],
        totalitarian: Dict[str, Any],
        judgment: Dict[str, Any],
        freedom: Dict[str, Any],
    ) -> str:
        """Generate an Arendtian summary of the analysis."""
        parts = []

        parts.append(
            f"The text emphasizes {vita_activa['dominant_mode']} within the vita activa."
        )

        if natality["natality_present"]:
            parts.append(
                "It expresses natality - the human capacity for new beginnings."
            )

        if public_private["dominant_realm"] != "balanced":
            parts.append(f"The {public_private['dominant_realm']} realm dominates.")

        if plurality["plurality_present"]:
            parts.append(
                "It acknowledges human plurality - living together as distinct beings."
            )

        if evil_analysis["banality_of_evil"]:
            parts.append(
                "It suggests the banality of evil - thoughtless, ordinary wrongdoing."
            )

        if totalitarian["totalitarian_elements"]:
            parts.append(
                "Totalitarian elements present - domination destroying plurality."
            )

        if judgment["judgment_present"]:
            parts.append("It engages political judgment - thinking what we are doing.")

        if freedom["political_freedom"]:
            parts.append(
                "It expresses political freedom - freedom through action in the public sphere."
            )

        return " ".join(parts)

    def _calculate_tension(
        self,
        vita_activa: Dict[str, Any],
        natality: Dict[str, Any],
        public_private: Dict[str, Any],
        plurality: Dict[str, Any],
        evil_analysis: Dict[str, Any],
        totalitarian: Dict[str, Any],
        judgment: Dict[str, Any],
        freedom: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate political-philosophical tensions in the text."""
        elements = []

        # Tension: labor dominates without action — loss of political life
        if (
            vita_activa["dominant_mode"] == "labor"
            and not vita_activa["action_present"]
        ):
            elements.append("Labor dominates without action — political life is absent")
        # Tension: labor vs action within vita activa
        elif vita_activa["labor_present"] and vita_activa["action_present"]:
            elements.append(
                "Tension between labor (necessity) and action (political freedom)"
            )

        # Tension: only private realm, no public sphere
        if public_private["private_present"] and not public_private["public_present"]:
            elements.append(
                "Private realm without public sphere — space of appearance is absent"
            )
        # Tension: public vs private coexistence
        elif public_private["public_present"] and public_private["private_present"]:
            elements.append(
                "Tension between public political sphere and private realm of necessity"
            )

        # Tension: totalitarian elements threaten plurality
        if totalitarian["totalitarian_elements"]:
            elements.append(
                "Totalitarian domination threatens plurality and political freedom"
            )
        # Tension: banality of evil — thoughtless wrongdoing
        if evil_analysis["banality_of_evil"]:
            elements.append(
                "Banality of evil — thoughtless, ordinary wrongdoing present"
            )

        # Tension: freedom vs totalitarianism
        if freedom["freedom_present"] and totalitarian["totalitarian_elements"]:
            elements.append("Tension between freedom and totalitarian control")
        # Tension: natality vs evil
        if natality["natality_present"] and evil_analysis["evil_present"]:
            elements.append("Tension between capacity for new beginnings and evil")
        # Tension: plurality threatened
        if plurality["plurality_present"] and totalitarian["totalitarian_elements"]:
            elements.append(
                "Tension between human plurality and totalitarian uniformity"
            )

        n = len(elements)
        if n >= 3:
            level = "High"
            desc = "Multiple political tensions active — rich engagement with Arendtian themes of power, freedom, and evil."
        elif n >= 2:
            level = "Moderate"
            desc = "Some political tensions present — text engages with competing aspects of the human condition."
        elif n >= 1:
            level = "Low"
            desc = "Mild tension within political-philosophical themes."
        else:
            level = "Very Low"
            desc = "Minimal political tension; text does not strongly engage competing Arendtian themes."
            elements = ["No significant Arendtian tensions detected"]

        return {
            "level": level,
            "score": n,
            "description": desc,
            "elements": elements,
        }
