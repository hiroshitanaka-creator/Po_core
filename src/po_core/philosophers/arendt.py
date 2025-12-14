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
            description="Political philosopher analyzing action, natality, plurality, and the human condition in the public sphere"
        )

    def reason(self, text: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
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

        return {
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
                "freedom": freedom
            },
            "summary": self._generate_summary(
                vita_activa, natality, public_private, plurality,
                evil_analysis, totalitarian, judgment, freedom
            )
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
            "labor", "work", "necessity", "biological", "survival",
            "consumption", "eat", "sleep", "maintain", "routine",
            "repetitive", "cycle", "metabolic", "body", "need"
        ]

        # Work indicators - fabrication, durability, object world
        work_words = [
            "build", "create", "make", "fabricate", "produce",
            "artifact", "tool", "craft", "construct", "design",
            "permanent", "durable", "world", "object", "thing"
        ]

        # Action indicators - political activity, beginning, appearing
        action_words = [
            "act", "action", "political", "public", "together",
            "begin", "start", "initiative", "speech", "appear",
            "reveal", "show", "citizen", "community", "collective"
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
                "action": action_score
            },
            "interpretation": self._interpret_vita_activa(dominant, labor_score, work_score, action_score)
        }

    def _interpret_vita_activa(self, dominant: str, labor: int, work: int, action: int) -> str:
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
            "new", "begin", "beginning", "start", "birth", "born",
            "initiative", "initiate", "novel", "create", "emerge",
            "first", "original", "fresh", "innovation", "possibility"
        ]

        has_natality = sum(1 for word in natality_words if word in text_lower)
        natality_present = has_natality >= 2

        return {
            "natality_present": natality_present,
            "new_beginning_capacity": natality_present,
            "score": has_natality,
            "interpretation": "Text expresses natality - the capacity to begin something new, the miracle of action." if natality_present else "Text shows limited emphasis on new beginnings or natality."
        }

    def _detect_public_private(self, text: str) -> Dict[str, Any]:
        """
        Detect public vs private realm.

        Public realm - space of appearance, political action, plurality
        Private realm - household, necessity, intimacy, property
        """
        text_lower = text.lower()

        public_words = [
            "public", "political", "citizen", "community", "together",
            "common", "shared", "collective", "society", "state",
            "democracy", "republic", "civic", "assembly", "appearance"
        ]

        private_words = [
            "private", "personal", "individual", "home", "family",
            "household", "intimate", "secret", "property", "own",
            "alone", "self", "inner", "domestic", "privacy"
        ]

        public_score = sum(1 for word in public_words if word in text_lower)
        private_score = sum(1 for word in private_words if word in text_lower)

        dominant_realm = "public" if public_score > private_score else "private" if private_score > public_score else "balanced"

        return {
            "dominant_realm": dominant_realm,
            "public_score": public_score,
            "private_score": private_score,
            "public_present": public_score > 0,
            "private_present": private_score > 0,
            "interpretation": self._interpret_realm(dominant_realm, public_score, private_score)
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
            "plural", "plurality", "diverse", "different", "distinct",
            "together", "others", "multiple", "various", "many",
            "unique", "individual", "collective", "community", "differences"
        ]

        has_plurality = sum(1 for word in plurality_words if word in text_lower)
        plurality_present = has_plurality >= 2

        return {
            "plurality_present": plurality_present,
            "living_together": plurality_present,
            "score": has_plurality,
            "interpretation": "Text acknowledges plurality - humans living together as distinct beings, the condition of political action." if plurality_present else "Text shows limited recognition of plurality and human distinctness."
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
            "banal", "ordinary", "routine", "bureaucratic", "thoughtless",
            "unthinking", "normal", "everyday", "conventional", "system",
            "procedure", "process", "duty", "orders", "obedience"
        ]

        has_evil = sum(1 for word in evil_words if word in text_lower)
        has_banal = sum(1 for word in banal_words if word in text_lower)

        banality_of_evil = has_evil > 0 and has_banal >= 2

        return {
            "evil_present": has_evil > 0,
            "banality_of_evil": banality_of_evil,
            "thoughtlessness": has_banal >= 2,
            "interpretation": "Text suggests the banality of evil - evil as thoughtless, ordinary behavior within systems." if banality_of_evil else "Evil as thoughtlessness not strongly present." if has_banal >= 2 else "Limited engagement with evil or its ordinary nature."
        }

    def _detect_totalitarian(self, text: str) -> Dict[str, Any]:
        """
        Detect totalitarian elements.

        Arendt's analysis: totalitarianism uses terror and ideology to dominate
        completely, destroying the public realm and human plurality.
        """
        text_lower = text.lower()

        totalitarian_words = [
            "totalitarian", "total", "domination", "control", "terror",
            "ideology", "propaganda", "dictator", "authoritarian", "tyranny",
            "oppression", "surveillance", "conform", "uniform", "mass"
        ]

        has_totalitarian = sum(1 for word in totalitarian_words if word in text_lower)
        totalitarian_present = has_totalitarian >= 2

        return {
            "totalitarian_elements": totalitarian_present,
            "score": has_totalitarian,
            "interpretation": "Text shows totalitarian elements - domination through terror and ideology, destroying plurality." if totalitarian_present else "Limited totalitarian themes present."
        }

    def _assess_judgment(self, text: str) -> Dict[str, Any]:
        """
        Assess political judgment.

        Arendt's concept of judgment (influenced by Kant): the faculty of thinking
        and judging, especially in political matters. Thinking what we are doing.
        """
        text_lower = text.lower()

        judgment_words = [
            "judge", "judgment", "think", "thinking", "reflect",
            "consider", "deliberate", "reason", "evaluate", "assess",
            "understand", "comprehend", "examine", "question", "critical"
        ]

        has_judgment = sum(1 for word in judgment_words if word in text_lower)
        judgment_present = has_judgment >= 2

        return {
            "judgment_present": judgment_present,
            "thinking": judgment_present,
            "score": has_judgment,
            "interpretation": "Text engages political judgment - thinking what we are doing, reflecting on action." if judgment_present else "Limited engagement with judgment or reflective thinking."
        }

    def _evaluate_freedom(self, text: str) -> Dict[str, Any]:
        """
        Evaluate freedom - freedom as political action in the public realm.

        For Arendt, freedom is not an inner state but is realized through
        action in the public political sphere.
        """
        text_lower = text.lower()

        freedom_words = [
            "freedom", "free", "liberty", "liberate", "autonomous",
            "independence", "self-govern", "choice", "spontaneous", "act"
        ]

        political_words = [
            "political", "public", "action", "together", "citizen",
            "community", "collective", "participate", "engage"
        ]

        has_freedom = sum(1 for word in freedom_words if word in text_lower)
        has_political = sum(1 for word in political_words if word in text_lower)

        political_freedom = has_freedom > 0 and has_political > 0

        return {
            "freedom_present": has_freedom > 0,
            "political_freedom": political_freedom,
            "freedom_score": has_freedom,
            "political_score": has_political,
            "interpretation": "Text expresses political freedom - freedom realized through action in the public sphere." if political_freedom else "Freedom without strong political dimension." if has_freedom > 0 else "Limited engagement with freedom."
        }

    def _generate_summary(
        self,
        vita_activa: Dict[str, Any],
        natality: Dict[str, Any],
        public_private: Dict[str, Any],
        plurality: Dict[str, Any],
        evil_analysis: Dict[str, Any],
        totalitarian: Dict[str, Any],
        judgment: Dict[str, Any],
        freedom: Dict[str, Any]
    ) -> str:
        """Generate an Arendtian summary of the analysis."""
        parts = []

        parts.append(f"The text emphasizes {vita_activa['dominant_mode']} within the vita activa.")

        if natality["natality_present"]:
            parts.append("It expresses natality - the human capacity for new beginnings.")

        if public_private["dominant_realm"] != "balanced":
            parts.append(f"The {public_private['dominant_realm']} realm dominates.")

        if plurality["plurality_present"]:
            parts.append("It acknowledges human plurality - living together as distinct beings.")

        if evil_analysis["banality_of_evil"]:
            parts.append("It suggests the banality of evil - thoughtless, ordinary wrongdoing.")

        if totalitarian["totalitarian_elements"]:
            parts.append("Totalitarian elements present - domination destroying plurality.")

        if judgment["judgment_present"]:
            parts.append("It engages political judgment - thinking what we are doing.")

        if freedom["political_freedom"]:
            parts.append("It expresses political freedom - freedom through action in the public sphere.")

        return " ".join(parts)
