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

from typing import Any, Dict, Optional

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
        # Store context if provided
        if context:
            self._context.update(context)

        # Perform Arendtian analysis
        analysis = self._analyze_political_action(text)

        # Identify tensions and contradictions
        tension = self._identify_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Political Philosophy / Human Condition",
            "tension": tension,
            "vita_activa": analysis["vita_activa"],
            "natality": analysis["natality"],
            "public_private_realm": analysis["public_private"],
            "plurality": analysis["plurality"],
            "evil_analysis": analysis["evil_analysis"],
            "totalitarian_elements": analysis["totalitarian"],
            "political_judgment": analysis["judgment"],
            "freedom": analysis["freedom"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Analysis of action, natality, and the public sphere",
                "focus": "Vita activa, plurality, and political freedom"
            }
        }

    def _analyze_political_action(self, text: str) -> Dict[str, Any]:
        """
        Perform Arendtian political analysis.

        Args:
            text: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze vita activa
        vita_activa = self._analyze_vita_activa(text)

        # Assess natality
        natality = self._assess_natality(text)

        # Detect public/private realm
        public_private = self._detect_public_private(text)

        # Evaluate plurality
        plurality = self._evaluate_plurality(text)

        # Analyze evil
        evil_analysis = self._analyze_evil(text)

        # Detect totalitarian elements
        totalitarian = self._detect_totalitarian(text)

        # Assess judgment
        judgment = self._assess_judgment(text)

        # Evaluate freedom
        freedom = self._evaluate_freedom(text)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            vita_activa, natality, public_private, plurality,
            evil_analysis, totalitarian, judgment, freedom
        )

        return {
            "reasoning": reasoning,
            "vita_activa": vita_activa,
            "natality": natality,
            "public_private": public_private,
            "plurality": plurality,
            "evil_analysis": evil_analysis,
            "totalitarian": totalitarian,
            "judgment": judgment,
            "freedom": freedom
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

    def _identify_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify Arendtian tensions and contradictions.

        Args:
            analysis: The analysis results

        Returns:
            Dictionary containing tension level, description, and elements
        """
        tension_elements = []

        # Tension in vita activa - labor dominating over action
        vita_activa = analysis["vita_activa"]
        if vita_activa["dominant_mode"] == "labor" and vita_activa["action_present"]:
            tension_elements.append("Labor dominates over action - biological necessity overshadows political freedom")
        elif vita_activa["dominant_mode"] == "labor" and not vita_activa["action_present"]:
            tension_elements.append("Trapped in labor - no political action, reduced to mere life process")

        # Tension between public and private realms
        public_private = analysis["public_private"]
        if public_private["dominant_realm"] == "private" and public_private["public_score"] == 0:
            tension_elements.append("Entirely private realm - no space of appearance, political action impossible")
        elif public_private["dominant_realm"] == "private" and vita_activa["action_present"]:
            tension_elements.append("Tension between private emphasis and need for public action")

        # Tension regarding plurality
        plurality = analysis["plurality"]
        if not plurality["plurality_present"] and vita_activa["action_present"]:
            tension_elements.append("Action without plurality - political action requires recognition of human distinctness")

        # Tension regarding natality
        natality = analysis["natality"]
        if not natality["natality_present"] and vita_activa["dominant_mode"] == "action":
            tension_elements.append("Action present but natality absent - new beginnings not recognized")

        # Tension from totalitarian elements
        totalitarian = analysis["totalitarian"]
        if totalitarian["totalitarian_elements"]:
            tension_elements.append("Totalitarian elements present - threat to plurality and public realm")

        # Tension regarding judgment
        judgment = analysis["judgment"]
        freedom = analysis["freedom"]
        if freedom["political_freedom"] and not judgment["judgment_present"]:
            tension_elements.append("Political freedom without judgment - action without thinking what we are doing")

        # Tension from banality of evil
        evil_analysis = analysis["evil_analysis"]
        if evil_analysis["banality_of_evil"]:
            tension_elements.append("Banality of evil present - thoughtless evil within bureaucratic systems")

        # Determine tension level
        tension_count = len(tension_elements)
        if tension_count == 0:
            level = "Very Low"
            description = "No significant tensions detected - text aligns with Arendtian ideals of political action and plurality"
        elif tension_count == 1:
            level = "Low"
            description = "Minor tension detected in Arendtian analysis"
        elif tension_count == 2:
            level = "Moderate"
            description = "Moderate tensions between political ideals and current state"
        elif tension_count <= 4:
            level = "High"
            description = "Significant tensions across multiple Arendtian dimensions"
        else:
            level = "Very High"
            description = "Severe tensions - substantial deviation from political action and human condition"

        return {
            "level": level,
            "description": description,
            "elements": tension_elements
        }

    def _construct_reasoning(
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
        """Construct Arendtian reasoning."""
        reasoning = (
            f"From Arendt's perspective, this text emphasizes {vita_activa['dominant_mode']} within the vita activa. "
            f"{vita_activa['interpretation']} "
        )

        # Add public/private realm analysis
        reasoning += f"The {public_private['dominant_realm']} realm is emphasized. "

        # Add natality if present
        if natality["natality_present"]:
            reasoning += "Natality - the capacity for new beginnings - is present. "

        # Add plurality if present
        if plurality["plurality_present"]:
            reasoning += "Human plurality is recognized - the condition of living together as distinct beings. "

        # Add judgment
        if judgment["judgment_present"]:
            reasoning += "Political judgment is engaged - thinking what we are doing. "

        # Add freedom
        if freedom["political_freedom"]:
            reasoning += "Political freedom is expressed - freedom through action in the public sphere. "

        # Add totalitarian warning if present
        if totalitarian["totalitarian_elements"]:
            reasoning += "Warning: totalitarian elements threaten plurality and the public realm. "

        # Add banality of evil if present
        if evil_analysis["banality_of_evil"]:
            reasoning += "The banality of evil appears - thoughtless wrongdoing within systems. "

        # Conclude with Arendtian principle
        reasoning += (
            "For Arendt, true human freedom is realized through political action in the public sphere, "
            "where we reveal who we are through speech and deeds among our equals."
        )

        return reasoning
