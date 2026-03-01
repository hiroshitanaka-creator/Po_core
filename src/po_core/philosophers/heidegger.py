"""
Heidegger - Phenomenological Philosopher

Martin Heidegger (1889-1976)
Focus: Being and Time, Dasein (Being-there), Existential Analysis

Key Concepts:
- Dasein: Human existence as "being-in-the-world"
- Being vs. Beings: The ontological difference
- Temporality: Past, present, and future as constitutive of being
- Authenticity vs. Inauthenticity (Eigentlichkeit/Uneigentlichkeit)
- Geworfenheit: Thrownness - we are thrown into existence
- Sorge: Care - the fundamental structure of Dasein
- Befindlichkeit: Attunement/mood - how we find ourselves
- Verfallen: Fallenness - absorption in the everyday
- Das Man: The "they" - anonymous existence
- Angst: Anxiety - reveals the nothing
- Sein-zum-Tode: Being-toward-death
- Gelassenheit: Releasement/letting-be
- Lichtung: Clearing - where Being reveals itself
- Ereignis: The event of appropriation
- Technik: The essence of technology
- Aletheia: Truth as unconcealment
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Heidegger(Philosopher):
    """
    Heidegger's phenomenological perspective.

    Analyzes prompts through the lens of Being and Time,
    focusing on existence, temporality, authenticity, care, and the question of Being.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Martin Heidegger",
            description="Phenomenologist focused on Being, Time, Dasein, care, and the ontological difference",
        )
        self.tradition = "Phenomenology / Existentialism"
        self.key_concepts = [
            "Dasein",
            "Being-in-the-world",
            "care (Sorge)",
            "thrownness (Geworfenheit)",
            "authenticity",
        ]

    def reason(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the prompt from Heidegger's phenomenological perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Heidegger's philosophical analysis
        """
        # Perform comprehensive Heideggerian analysis
        analysis = self._analyze_being(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Phenomenological / Existential",
            "tension": tension,
            "key_concepts": analysis["concepts"],
            "questions": analysis["questions"],
            "temporal_dimension": analysis["temporality"],
            "authenticity_check": analysis["authenticity"],
            "geworfenheit": analysis["thrownness"],
            "sorge": analysis["care"],
            "befindlichkeit": analysis["attunement"],
            "verfallen": analysis["fallenness"],
            "angst": analysis["angst"],
            "sein_zum_tode": analysis["being_toward_death"],
            "das_man": analysis["das_man"],
            "gelassenheit": analysis["gelassenheit"],
            "lichtung": analysis["lichtung"],
            "technik": analysis["technology"],
            "aletheia": analysis["aletheia"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Being and Time analysis / Later Heidegger",
                "focus": "Dasein, temporality, care, authenticity, and the question of Being",
            },
        }

    def _analyze_being(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Heideggerian existential analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Heideggerian dimensions
        temporality = self._analyze_temporality(prompt)
        authenticity = self._assess_authenticity(prompt)
        thrownness = self._assess_thrownness(prompt)
        care = self._analyze_care(prompt)
        attunement = self._assess_attunement(prompt)
        fallenness = self._assess_fallenness(prompt)
        angst = self._analyze_angst(prompt)
        being_toward_death = self._assess_being_toward_death(prompt)
        das_man = self._assess_das_man(prompt)
        gelassenheit = self._assess_gelassenheit(prompt)
        lichtung = self._assess_lichtung(prompt)
        technology = self._analyze_technology(prompt)
        aletheia = self._assess_aletheia(prompt)

        # Identify key concepts and questions
        concepts = self._identify_concepts(prompt)
        questions = self._generate_questions(prompt, concepts)

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            prompt,
            temporality,
            authenticity,
            thrownness,
            care,
            attunement,
            angst,
            being_toward_death,
            das_man,
            concepts,
        )

        return {
            "reasoning": reasoning,
            "concepts": concepts,
            "questions": questions,
            "temporality": temporality,
            "authenticity": authenticity,
            "thrownness": thrownness,
            "care": care,
            "attunement": attunement,
            "fallenness": fallenness,
            "angst": angst,
            "being_toward_death": being_toward_death,
            "das_man": das_man,
            "gelassenheit": gelassenheit,
            "lichtung": lichtung,
            "technology": technology,
            "aletheia": aletheia,
        }

    def _analyze_temporality(self, text: str) -> Dict[str, Any]:
        """
        Analyze temporal dimensions (ecstatic temporality).

        For Heidegger, time is not linear but ecstatic:
        - Having-been (Gewesenheit) - past as still operative
        - Present (Gegenwart) - making present
        - Future (Zukunft) - coming toward oneself
        """
        text_lower = text.lower()

        # Past (Having-been) indicators
        past_words = [
            "was",
            "were",
            "had",
            "before",
            "past",
            "memory",
            "history",
            "tradition",
            "heritage",
            "origin",
            "already",
            "thrown",
        ]
        past_count = sum(1 for word in past_words if word in text_lower)

        # Future (Coming-toward) indicators
        future_words = [
            "will",
            "shall",
            "future",
            "tomorrow",
            "anticipate",
            "project",
            "possibility",
            "potential",
            "become",
            "ahead",
            "goal",
        ]
        future_count = sum(1 for word in future_words if word in text_lower)

        # Present (Making-present) indicators
        present_words = [
            "is",
            "are",
            "now",
            "today",
            "currently",
            "present",
            "immediate",
            "here",
            "moment",
            "instant",
        ]
        present_count = sum(1 for word in present_words if word in text_lower)

        # Determine temporal mode
        if future_count > past_count and future_count > present_count:
            primary_mode = "Future-oriented (Authentic)"
            description = (
                "Anticipatory projection toward possibilities - authentic temporality"
            )
        elif past_count > future_count and past_count > present_count:
            primary_mode = "Having-been (Thrownness)"
            description = "Grounded in facticity and heritage - thrown into history"
        elif present_count > past_count and present_count > future_count:
            primary_mode = "Present-focused (Possibly Fallen)"
            description = (
                "Absorbed in the present - may indicate fallenness into the 'now'"
            )
        else:
            primary_mode = "Ecstatic Unity"
            description = (
                "Unified temporality - past, present, and future interpenetrate"
            )

        # Check for authentic vs inauthentic temporality
        if future_count >= 1 and any(
            word in text_lower for word in ["death", "mortality", "finite"]
        ):
            temporal_authenticity = "Authentic"
            note = "Being-toward-death opens authentic temporality"
        elif present_count > future_count + past_count:
            temporal_authenticity = "Inauthentic"
            note = "Absorbed in the present, fleeing from finitude"
        else:
            temporal_authenticity = "Undetermined"
            note = "Temporal stance requires further analysis"

        return {
            "primary_mode": primary_mode,
            "description": description,
            "past_present": past_count > 0,
            "future_oriented": future_count > 0,
            "present_focused": present_count > 0,
            "temporal_authenticity": temporal_authenticity,
            "note": note,
            "ecstases": {
                "having_been": past_count,
                "making_present": present_count,
                "coming_toward": future_count,
            },
            "principle": "Ecstatic temporality: past, present, future as unified structure of care",
        }

    def _assess_authenticity(self, text: str) -> Dict[str, Any]:
        """
        Assess authenticity (Eigentlichkeit) vs inauthenticity (Uneigentlichkeit).

        Authentic existence: owning one's being, facing finitude
        Inauthentic existence: lost in das Man, fleeing from anxiety
        """
        text_lower = text.lower()

        # Authenticity indicators
        auth_words = [
            "choice",
            "responsibility",
            "freedom",
            "own",
            "myself",
            "decide",
            "resolve",
            "authentic",
            "genuine",
            "individual",
            "unique",
            "mortality",
            "finite",
            "death",
        ]
        auth_count = sum(1 for word in auth_words if word in text_lower)

        # Inauthenticity indicators
        inauth_words = [
            "they",
            "everyone",
            "always",
            "supposed to",
            "one does",
            "people say",
            "normal",
            "average",
            "conformity",
            "distraction",
            "busy",
            "idle talk",
            "curiosity",
            "ambiguity",
        ]
        inauth_count = sum(1 for word in inauth_words if word in text_lower)

        # Resoluteness indicators (Entschlossenheit)
        resolve_words = ["resolve", "determined", "commit", "call", "conscience"]
        has_resolve = sum(1 for word in resolve_words if word in text_lower)

        # Assess mode
        if auth_count > inauth_count and has_resolve >= 1:
            mode = "Resolute Authenticity"
            description = "Authentic Dasein - resolutely owning one's thrown projection"
            level = "High"
        elif auth_count > inauth_count:
            mode = "Tends toward Authenticity"
            description = "Movement toward owning one's being"
            level = "Medium-High"
        elif inauth_count > auth_count:
            mode = "Inauthentic (das Man)"
            description = "Lost in the 'they' - not owning one's ownmost possibilities"
            level = "Low"
        else:
            mode = "Undifferentiated"
            description = "Neither clearly authentic nor inauthentic"
            level = "Medium"

        return {
            "mode": mode,
            "description": description,
            "level": level,
            "authenticity_score": auth_count,
            "inauthenticity_score": inauth_count,
            "resoluteness": has_resolve >= 1,
            "principle": "Authenticity is owning one's ownmost being-toward-death",
        }

    def _assess_thrownness(self, text: str) -> Dict[str, Any]:
        """
        Assess Geworfenheit (thrownness).

        We are thrown into existence - we did not choose our birth, culture, body.
        Facticity: the given conditions of our existence.
        """
        text_lower = text.lower()

        # Thrownness indicators
        thrown_words = [
            "thrown",
            "given",
            "born into",
            "found myself",
            "already",
            "heritage",
            "tradition",
            "culture",
            "circumstance",
            "fate",
            "destined",
            "situation",
            "condition",
            "background",
            "history",
        ]
        thrown_count = sum(1 for word in thrown_words if word in text_lower)

        # Facticity indicators
        facticity_words = [
            "fact",
            "reality",
            "is",
            "cannot change",
            "given",
            "body",
            "gender",
            "nationality",
            "family",
            "era",
        ]
        facticity_count = sum(1 for word in facticity_words if word in text_lower)

        # Projection indicators (thrown projection)
        projection_words = ["project", "possibility", "can be", "future", "become"]
        projection_count = sum(1 for word in projection_words if word in text_lower)

        if thrown_count >= 2 and projection_count >= 1:
            status = "Thrown Projection"
            description = (
                "Awareness of both thrownness and projection - authentic understanding"
            )
        elif thrown_count >= 2:
            status = "Awareness of Thrownness"
            description = "Confronting the given conditions of existence"
        elif thrown_count >= 1:
            status = "Implicit Thrownness"
            description = "Some awareness of factical conditions"
        else:
            status = "Thrownness Concealed"
            description = "The thrown nature of existence is not explicitly addressed"

        return {
            "status": status,
            "description": description,
            "thrownness_score": thrown_count,
            "facticity_score": facticity_count,
            "projection_score": projection_count,
            "principle": "Geworfenheit: We are thrown into existence, not self-created",
        }

    def _analyze_care(self, text: str) -> Dict[str, Any]:
        """
        Analyze Sorge (care) - the fundamental structure of Dasein.

        Care = ahead-of-itself (project) + already-in (thrownness) + being-alongside (world)
        """
        text_lower = text.lower()

        # Care/concern indicators
        care_words = [
            "care",
            "concern",
            "worry",
            "matter",
            "important",
            "significant",
            "meaning",
            "purpose",
            "stake",
            "involved",
            "engaged",
        ]
        care_count = sum(1 for word in care_words if word in text_lower)

        # Ahead-of-itself (future projection)
        ahead_words = ["future", "goal", "aim", "project", "possibility", "plan"]
        ahead_count = sum(1 for word in ahead_words if word in text_lower)

        # Already-in (thrownness/facticity)
        already_words = ["already", "given", "situation", "background", "history"]
        already_count = sum(1 for word in already_words if word in text_lower)

        # Being-alongside (world engagement)
        alongside_words = [
            "with",
            "things",
            "equipment",
            "tools",
            "world",
            "environment",
        ]
        alongside_count = sum(1 for word in alongside_words if word in text_lower)

        # Determine care structure
        if care_count >= 2 or (
            ahead_count >= 1 and already_count >= 1 and alongside_count >= 1
        ):
            structure = "Full Care Structure"
            description = "Unified care: ahead-of-itself, already-in, being-alongside"
        elif care_count >= 1:
            structure = "Care Evident"
            description = "Concern and care are present"
        elif ahead_count >= 1 or already_count >= 1:
            structure = "Partial Care"
            description = "Some dimensions of care are present"
        else:
            structure = "Care Concealed"
            description = "Care structure not explicitly manifest"

        return {
            "structure": structure,
            "description": description,
            "care_score": care_count,
            "moments": {
                "ahead_of_itself": ahead_count,
                "already_in": already_count,
                "being_alongside": alongside_count,
            },
            "principle": "Sorge (Care): The fundamental structure of Dasein's being",
        }

    def _assess_attunement(self, text: str) -> Dict[str, Any]:
        """
        Assess Befindlichkeit (attunement/mood/state-of-mind).

        We always find ourselves in a mood - moods disclose the world.
        Fundamental moods: anxiety (Angst), boredom (Langeweile), wonder (Erstaunen)
        """
        text_lower = text.lower()

        # Basic mood indicators
        mood_words = {
            "anxiety": ["anxiety", "anxious", "uneasy", "unsettled", "uncanny"],
            "boredom": ["bored", "boring", "monotonous", "tedious", "empty"],
            "joy": ["joy", "joyful", "happy", "elated", "delighted"],
            "fear": ["fear", "afraid", "scared", "frightened", "terrified"],
            "wonder": ["wonder", "awe", "amazed", "astonished", "marveled"],
            "melancholy": ["sad", "melancholy", "grief", "sorrow", "depressed"],
            "hope": ["hope", "hopeful", "optimistic", "anticipate"],
            "dread": ["dread", "foreboding", "ominous", "doom"],
        }

        detected_moods = []
        for mood, words in mood_words.items():
            if any(word in text_lower for word in words):
                detected_moods.append(mood)

        # Check for fundamental moods (Grundstimmung)
        is_fundamental = (
            "anxiety" in detected_moods
            or "boredom" in detected_moods
            or "wonder" in detected_moods
        )

        if is_fundamental and "anxiety" in detected_moods:
            primary_mood = "Anxiety (Angst)"
            description = (
                "Fundamental mood - reveals the nothing and individuates Dasein"
            )
            disclosure = "Authentic disclosure of being-in-the-world"
        elif is_fundamental and "boredom" in detected_moods:
            primary_mood = "Profound Boredom"
            description = (
                "Fundamental mood - reveals the emptiness of beings as a whole"
            )
            disclosure = "Disclosure of being left empty by beings"
        elif is_fundamental and "wonder" in detected_moods:
            primary_mood = "Wonder (Erstaunen)"
            description = "Fundamental mood - reveals that beings are"
            disclosure = "Philosophical attunement to Being itself"
        elif detected_moods:
            primary_mood = ", ".join(detected_moods)
            description = "Everyday moods present"
            disclosure = "Ontic disclosure - not fundamental"
        else:
            primary_mood = "Not explicitly disclosed"
            description = "Mood not clearly articulated"
            disclosure = "Attunement is always present but may be concealed"

        return {
            "primary_mood": primary_mood,
            "description": description,
            "disclosure": disclosure,
            "detected_moods": detected_moods,
            "is_fundamental": is_fundamental,
            "principle": "Befindlichkeit: We always find ourselves in a mood that discloses the world",
        }

    def _assess_fallenness(self, text: str) -> Dict[str, Any]:
        """
        Assess Verfallen (fallenness) - absorption in the everyday world.

        Fallenness manifests as:
        - Gerede (idle talk): discourse without understanding
        - Neugier (curiosity): restless pursuit of novelty
        - Zweideutigkeit (ambiguity): everything seems understood
        """
        text_lower = text.lower()

        # Idle talk indicators
        idle_talk_words = [
            "they say",
            "people think",
            "rumor",
            "gossip",
            "chat",
            "everyone knows",
            "it is said",
            "supposedly",
        ]
        idle_talk_count = sum(1 for phrase in idle_talk_words if phrase in text_lower)

        # Curiosity (negative sense) indicators
        curiosity_words = [
            "curious",
            "novelty",
            "news",
            "distraction",
            "entertainment",
            "trending",
            "latest",
            "sensation",
        ]
        curiosity_count = sum(1 for word in curiosity_words if word in text_lower)

        # Ambiguity indicators
        ambiguity_words = [
            "obvious",
            "everyone understands",
            "clearly",
            "of course",
            "naturally",
            "goes without saying",
        ]
        ambiguity_count = sum(1 for phrase in ambiguity_words if phrase in text_lower)

        # Busy-ness indicators
        busy_words = ["busy", "hectic", "rushing", "no time", "occupied", "overwhelmed"]
        busy_count = sum(1 for word in busy_words if word in text_lower)

        total_fallen = idle_talk_count + curiosity_count + ambiguity_count + busy_count

        if total_fallen >= 4:
            status = "Deep Fallenness"
            description = (
                "Absorbed in das Man - idle talk, curiosity, and ambiguity dominate"
            )
        elif total_fallen >= 2:
            status = "Moderate Fallenness"
            description = "Signs of absorption in everyday publicness"
        elif total_fallen >= 1:
            status = "Slight Fallenness"
            description = "Some indicators of everyday absorption"
        else:
            status = "Not Evidently Fallen"
            description = "Fallenness not clearly manifest"

        return {
            "status": status,
            "description": description,
            "indicators": {
                "idle_talk": idle_talk_count,
                "curiosity": curiosity_count,
                "ambiguity": ambiguity_count,
                "busy_ness": busy_count,
            },
            "total_score": total_fallen,
            "principle": "Verfallen: Tendency to fall into the world and lose oneself",
        }

    def _analyze_angst(self, text: str) -> Dict[str, Any]:
        """
        Analyze Angst (anxiety) - the fundamental mood.

        Angst differs from fear:
        - Fear has a definite object within the world
        - Angst has no object - it reveals being-in-the-world as such
        - Angst individualizes Dasein, strips away the 'they'
        - Angst reveals the nothing (das Nichts)
        """
        text_lower = text.lower()

        # Angst indicators
        angst_words = [
            "anxiety",
            "anxious",
            "uncanny",
            "unheimlich",
            "homeless",
            "nowhere",
            "nothing",
            "dread",
            "groundless",
            "abyss",
        ]
        angst_count = sum(1 for word in angst_words if word in text_lower)

        # Fear indicators (distinct from angst)
        fear_words = ["fear", "afraid of", "scared of", "frightened by", "terrified of"]
        fear_count = sum(1 for phrase in fear_words if phrase in text_lower)

        # Nothing/nothingness indicators
        nothing_words = ["nothing", "nothingness", "void", "emptiness", "nullity"]
        nothing_count = sum(1 for word in nothing_words if word in text_lower)

        # Uncanny (Unheimlich) indicators
        uncanny_words = ["uncanny", "strange", "unfamiliar", "not at home", "alien"]
        uncanny_count = sum(1 for word in uncanny_words if word in text_lower)

        if angst_count >= 2 or (angst_count >= 1 and nothing_count >= 1):
            presence = "Angst Present"
            description = (
                "Fundamental anxiety - reveals being-in-the-world and the nothing"
            )
            authenticity = "Authentic mood"
        elif angst_count >= 1:
            presence = "Traces of Angst"
            description = "Some anxiety present - may be fleeting"
            authenticity = "Potentially authentic"
        elif fear_count >= 1:
            presence = "Fear (Not Angst)"
            description = "Fear of specific things - not fundamental angst"
            authenticity = "Ontic fear, not ontological anxiety"
        else:
            presence = "No Angst Evident"
            description = "Anxiety not manifest - perhaps fled into das Man"
            authenticity = "Everyday tranquility"

        return {
            "presence": presence,
            "description": description,
            "authenticity": authenticity,
            "angst_score": angst_count,
            "fear_score": fear_count,
            "nothing_revealed": nothing_count >= 1,
            "uncanny": uncanny_count >= 1,
            "principle": "Angst reveals the nothing and individualizes Dasein",
        }

    def _assess_being_toward_death(self, text: str) -> Dict[str, Any]:
        """
        Assess Sein-zum-Tode (being-toward-death).

        Death is:
        - Ownmost: no one can die my death for me
        - Non-relational: I am utterly alone before death
        - Not to be outstripped: death is certain
        - Indefinite: when is uncertain

        Authentic being-toward-death: anticipation (Vorlaufen)
        Inauthentic: fleeing, covering up, "one dies"
        """
        text_lower = text.lower()

        # Death/mortality indicators
        death_words = [
            "death",
            "die",
            "dying",
            "mortal",
            "mortality",
            "finite",
            "end",
            "perish",
            "demise",
            "final",
        ]
        death_count = sum(1 for word in death_words if word in text_lower)

        # Authentic anticipation indicators
        anticipation_words = [
            "anticipate",
            "face death",
            "accept mortality",
            "finite",
            "my death",
            "ownmost",
        ]
        anticipation_count = sum(
            1 for phrase in anticipation_words if phrase in text_lower
        )

        # Inauthentic fleeing indicators
        fleeing_words = [
            "one dies",
            "everybody dies",
            "someday",
            "not yet",
            "don't think about",
            "avoid",
            "distract",
        ]
        fleeing_count = sum(1 for phrase in fleeing_words if phrase in text_lower)

        if death_count >= 1 and anticipation_count >= 1:
            stance = "Authentic Anticipation"
            description = "Being-toward-death as ownmost, non-relational possibility"
            mode = "Anticipatory resoluteness"
        elif death_count >= 1 and fleeing_count >= 1:
            stance = "Inauthentic Evasion"
            description = "Fleeing from death - 'one dies' mentality"
            mode = "Covering over finitude"
        elif death_count >= 1:
            stance = "Death Acknowledged"
            description = "Mortality is mentioned but stance unclear"
            mode = "Undetermined"
        else:
            stance = "Death Concealed"
            description = "Finitude not addressed - possible flight"
            mode = "Everyday absorption"

        return {
            "stance": stance,
            "description": description,
            "mode": mode,
            "death_count": death_count,
            "anticipation": anticipation_count >= 1,
            "fleeing": fleeing_count >= 1,
            "principle": "Sein-zum-Tode: Death is ownmost, non-relational, not to be outstripped",
        }

    def _assess_das_man(self, text: str) -> Dict[str, Any]:
        """
        Assess das Man (the 'they' / the 'one').

        Das Man is the anonymous, average, public existence.
        We say 'one does this', 'they think that' - losing our ownmost self.
        """
        text_lower = text.lower()

        # Das Man indicators
        das_man_words = [
            "they",
            "everyone",
            "people",
            "one does",
            "normal",
            "average",
            "typical",
            "common",
            "public",
            "society",
            "expected",
            "supposed to",
            "should",
            "must",
        ]
        das_man_count = sum(1 for word in das_man_words if word in text_lower)

        # Individual/authentic indicators (counter das Man)
        individual_words = [
            "i",
            "myself",
            "my own",
            "individual",
            "unique",
            "personal",
            "authentic",
            "genuine",
        ]
        individual_count = sum(1 for word in individual_words if word in text_lower)

        # Conformity indicators
        conformity_words = [
            "conform",
            "fit in",
            "belong",
            "follow",
            "obey",
            "rules",
            "norms",
            "expectations",
        ]
        conformity_count = sum(1 for word in conformity_words if word in text_lower)

        if das_man_count > individual_count + 2:
            status = "Absorbed in das Man"
            description = "Lost in the 'they' - leveled down to average"
            individuality = "Low"
        elif das_man_count > individual_count:
            status = "Tendency toward das Man"
            description = "Some absorption in public interpretedness"
            individuality = "Medium"
        elif individual_count > das_man_count:
            status = "Individuated"
            description = "Standing out from das Man"
            individuality = "High"
        else:
            status = "Undifferentiated"
            description = "Neither clearly individual nor absorbed"
            individuality = "Undetermined"

        return {
            "status": status,
            "description": description,
            "individuality": individuality,
            "das_man_score": das_man_count,
            "individual_score": individual_count,
            "conformity_score": conformity_count,
            "principle": "Das Man: The anonymous 'they' that levels down and disperses Dasein",
        }

    def _assess_gelassenheit(self, text: str) -> Dict[str, Any]:
        """
        Assess Gelassenheit (releasement/letting-be).

        Later Heidegger's concept: letting beings be, releasing control.
        Contrast with technological will-to-power.
        """
        text_lower = text.lower()

        # Gelassenheit indicators
        release_words = [
            "let",
            "allow",
            "release",
            "accept",
            "surrender",
            "openness",
            "receptive",
            "patient",
            "wait",
            "listen",
        ]
        release_count = sum(1 for word in release_words if word in text_lower)

        # Control/will indicators (opposite)
        control_words = [
            "control",
            "master",
            "dominate",
            "force",
            "impose",
            "manipulate",
            "exploit",
            "demand",
            "insist",
            "will",
        ]
        control_count = sum(1 for word in control_words if word in text_lower)

        # Meditative thinking indicators
        meditative_words = [
            "meditate",
            "contemplate",
            "ponder",
            "dwell",
            "thoughtful",
            "reflective",
            "quiet",
        ]
        meditative_count = sum(1 for word in meditative_words if word in text_lower)

        if release_count > control_count and meditative_count >= 1:
            mode = "Gelassenheit"
            description = "Releasement - letting beings be in meditative openness"
            stance = "Receptive dwelling"
        elif release_count > control_count:
            mode = "Tending toward Gelassenheit"
            description = "Some openness to letting-be"
            stance = "Partially receptive"
        elif control_count > release_count:
            mode = "Calculative Will"
            description = "Will-to-control dominates - technological stance"
            stance = "Grasping"
        else:
            mode = "Undetermined"
            description = "Neither clearly releasing nor controlling"
            stance = "Neutral"

        return {
            "mode": mode,
            "description": description,
            "stance": stance,
            "release_score": release_count,
            "control_score": control_count,
            "meditative": meditative_count >= 1,
            "principle": "Gelassenheit: Letting beings be - releasement toward things",
        }

    def _assess_lichtung(self, text: str) -> Dict[str, Any]:
        """
        Assess Lichtung (clearing/lighting).

        The clearing is where Being reveals itself and conceals itself.
        Truth (aletheia) happens in the clearing.
        """
        text_lower = text.lower()

        # Clearing/openness indicators
        clearing_words = [
            "clearing",
            "open",
            "light",
            "reveal",
            "disclose",
            "manifest",
            "appear",
            "presence",
            "luminous",
        ]
        clearing_count = sum(1 for word in clearing_words if word in text_lower)

        # Concealment indicators
        conceal_words = [
            "hidden",
            "conceal",
            "withdraw",
            "mystery",
            "obscure",
            "shadow",
            "darkness",
            "secret",
            "cover",
        ]
        conceal_count = sum(1 for word in conceal_words if word in text_lower)

        # Interplay of revealing/concealing
        if clearing_count >= 1 and conceal_count >= 1:
            status = "Interplay of Clearing and Concealing"
            description = "The truth of Being: revealing and concealing belong together"
        elif clearing_count >= 2:
            status = "Clearing Present"
            description = "Openness where beings can show themselves"
        elif conceal_count >= 2:
            status = "Concealment Emphasized"
            description = "The self-withdrawing dimension of Being"
        elif clearing_count >= 1:
            status = "Traces of Clearing"
            description = "Some openness to disclosure"
        else:
            status = "Clearing Not Evident"
            description = "The clearing is not explicitly addressed"

        return {
            "status": status,
            "description": description,
            "clearing_score": clearing_count,
            "concealment_score": conceal_count,
            "interplay": clearing_count >= 1 and conceal_count >= 1,
            "principle": "Lichtung: The clearing where Being reveals and conceals itself",
        }

    def _analyze_technology(self, text: str) -> Dict[str, Any]:
        """
        Analyze the question of technology (Technik).

        Technology is not just tools but a way of revealing (Gestell/Enframing).
        Enframing challenges everything to become 'standing-reserve' (Bestand).
        """
        text_lower = text.lower()

        # Technology indicators
        tech_words = [
            "technology",
            "technical",
            "machine",
            "computer",
            "digital",
            "system",
            "device",
            "apparatus",
            "instrument",
            "efficient",
        ]
        tech_count = sum(1 for word in tech_words if word in text_lower)

        # Enframing (Gestell) indicators
        enframing_words = [
            "resource",
            "exploit",
            "optimize",
            "efficient",
            "useful",
            "productive",
            "demand",
            "order",
            "stock",
        ]
        enframing_count = sum(1 for word in enframing_words if word in text_lower)

        # Alternative revealing (poiesis) indicators
        poiesis_words = [
            "craft",
            "art",
            "create",
            "bring forth",
            "grow",
            "nurture",
            "cultivate",
            "poetic",
            "dwell",
        ]
        poiesis_count = sum(1 for word in poiesis_words if word in text_lower)

        # Saving power indicators
        saving_words = ["save", "preserve", "protect", "care for", "tend"]
        saving_count = sum(1 for word in saving_words if word in text_lower)

        if tech_count >= 1 and enframing_count >= 2:
            stance = "Enframing (Gestell)"
            description = (
                "Technological revealing - challenging forth as standing-reserve"
            )
            danger = "High"
        elif tech_count >= 1 and poiesis_count >= 1:
            stance = "Tension: Technology and Poiesis"
            description = "Awareness of both technological and poetic revealing"
            danger = "Medium"
        elif poiesis_count >= 2:
            stance = "Poietic Revealing"
            description = "Bringing-forth in the manner of craft and art"
            danger = "Low"
        elif tech_count >= 1:
            stance = "Technology Present"
            description = "Technology mentioned - stance unclear"
            danger = "Undetermined"
        else:
            stance = "Technology Not Addressed"
            description = "The question of technology is not raised"
            danger = "N/A"

        return {
            "stance": stance,
            "description": description,
            "danger_level": danger,
            "tech_score": tech_count,
            "enframing_score": enframing_count,
            "poiesis_score": poiesis_count,
            "saving_power": saving_count >= 1,
            "principle": "Where danger is, the saving power also grows",
        }

    def _assess_aletheia(self, text: str) -> Dict[str, Any]:
        """
        Assess Aletheia (truth as unconcealment).

        Truth is not correspondence but unconcealment.
        Beings emerge from concealment into presence.
        """
        text_lower = text.lower()

        # Truth/unconcealment indicators
        truth_words = [
            "truth",
            "true",
            "reveal",
            "disclose",
            "uncover",
            "discover",
            "bring to light",
            "manifest",
            "appear",
        ]
        truth_count = sum(1 for word in truth_words if word in text_lower)

        # Concealment indicators
        conceal_words = [
            "hidden",
            "conceal",
            "cover",
            "obscure",
            "secret",
            "veil",
            "mystery",
            "latent",
        ]
        conceal_count = sum(1 for word in conceal_words if word in text_lower)

        # Correspondence theory indicators
        correspond_words = [
            "correspond",
            "match",
            "accurate",
            "correct",
            "representation",
            "reflect reality",
        ]
        correspond_count = sum(1 for phrase in correspond_words if phrase in text_lower)

        if truth_count >= 1 and conceal_count >= 1:
            conception = "Aletheia"
            description = "Truth as unconcealment - emergence from concealment"
            mode = "Heideggerian"
        elif truth_count >= 1 and correspond_count >= 1:
            conception = "Correspondence"
            description = "Truth as correspondence - propositional truth"
            mode = "Traditional"
        elif truth_count >= 2:
            conception = "Truth Emphasized"
            description = "Truth is a concern but conception unclear"
            mode = "Undetermined"
        elif conceal_count >= 1:
            conception = "Lethe (Concealment)"
            description = "Emphasis on the hidden, concealed dimension"
            mode = "Mystery"
        else:
            conception = "Truth Not Addressed"
            description = "Question of truth not explicitly raised"
            mode = "N/A"

        return {
            "conception": conception,
            "description": description,
            "mode": mode,
            "truth_score": truth_count,
            "concealment_score": conceal_count,
            "correspondence": correspond_count >= 1,
            "principle": "Aletheia: Truth as unconcealment, emergence from hiddenness",
        }

    def _identify_concepts(self, text: str) -> List[str]:
        """Identify key Heideggerian concepts in the text."""
        text_lower = text.lower()
        concepts = []

        concept_map = {
            "Dasein (Being-in-the-world)": [
                "being",
                "exist",
                "existence",
                "meaning",
                "purpose",
            ],
            "Temporality": [
                "time",
                "moment",
                "duration",
                "when",
                "past",
                "future",
                "present",
            ],
            "Authenticity": ["authentic", "genuine", "true self", "own"],
            "Being-toward-death": ["death", "mortality", "finite", "end"],
            "Anxiety (Angst)": ["anxiety", "anxious", "dread", "uncanny"],
            "Care (Sorge)": ["care", "concern", "matter", "importance"],
            "Thrownness (Geworfenheit)": ["thrown", "given", "situation", "heritage"],
            "Das Man (the They)": ["they", "everyone", "people say", "normal"],
            "Fallenness (Verfallen)": ["distraction", "busy", "idle talk"],
            "World": ["world", "environment", "things", "equipment"],
            "Clearing (Lichtung)": ["clear", "open", "light", "reveal"],
            "Technology (Gestell)": ["technology", "machine", "efficient", "resource"],
            "Gelassenheit": ["let", "release", "accept", "openness"],
        }

        for concept, keywords in concept_map.items():
            if any(word in text_lower for word in keywords):
                concepts.append(concept)

        if not concepts:
            concepts.append("Being-in-the-world")

        return concepts

    def _generate_questions(self, text: str, concepts: List[str]) -> List[str]:
        """Generate Heideggerian questions based on the analysis."""
        questions = []

        # Core ontological question
        questions.append("What does it mean to be?")

        # Based on concepts
        if "Being-toward-death" in concepts:
            questions.append("How does awareness of mortality transform existence?")
        if "Authenticity" in concepts:
            questions.append("Is this an authentic mode of being, or lost in das Man?")
        if "Temporality" in concepts:
            questions.append("How do past, present, and future constitute this being?")
        if "Anxiety (Angst)" in concepts:
            questions.append("What does this anxiety reveal about being-in-the-world?")
        if "Technology (Gestell)" in concepts:
            questions.append("Is technology revealing beings as standing-reserve?")
        if "Care (Sorge)" in concepts:
            questions.append("What does it mean that Dasein is fundamentally care?")

        return questions[:5]  # Limit to 5 questions

    def _apply_heidegger_to_problem(self, text: str) -> str:
        """Apply Heidegger's ontological concepts to the specific domain of the text."""
        t = text.lower()
        if any(
            w in t
            for w in [
                "technolog",
                "ai",
                "artificial",
                "machine",
                "algorithm",
                "digital",
                "automat",
                "robot",
                "comput",
            ]
        ):
            return (
                "Heidegger's analysis of Gestell (enframing) is indispensable here: "
                "modern technology does not merely produce tools but reveals all entities — including human beings — "
                "as Bestand (standing reserve), resources to be optimized and mobilized on demand. "
                "In this revealing, Being itself becomes invisible; we encounter only calculable, "
                "manipulable stock, never the mysterious givenness of entities as such. "
                "Yet Heidegger insists there is a 'saving power' hidden within the danger: "
                "by questioning the essence of technology rather than merely its products, "
                "we open a space where a different, non-enframing revealing — poiesis, techne as bringing-forth — "
                "can once again become possible, and Being can disclose itself anew."
            )
        elif any(
            w in t
            for w in [
                "authentic",
                "identity",
                "self",
                "individual",
                "person",
                "ego",
                "who am",
            ]
        ):
            return (
                "For Heidegger, the constant temptation is to lose oneself in das Man — the anonymous 'they' — "
                "whose idle talk, curiosity, and ambiguity flatten every genuine possibility into comfortable averageness. "
                "Dasein (human being-there) is always already thrown into a world not of its choosing (Geworfenheit), "
                "bearing a definite factical situation it cannot simply discard. "
                "Authentic existence requires owning this thrownness — neither fleeing it into distraction "
                "nor pretending to transcend it — while simultaneously projecting resolutely toward "
                "one's ownmost possibilities in the light of Being-toward-death. "
                "Only this resolute ownership of finitude rescues Dasein from the grip of das Man "
                "and allows genuine selfhood to emerge from the anonymous 'they'."
            )
        elif any(
            w in t
            for w in [
                "anxiety",
                "angst",
                "dread",
                "fear",
                "unease",
                "existential",
                "unsettl",
            ]
        ):
            return (
                "Angst (anxiety), for Heidegger, is not merely a psychological state but an ontological attunement "
                "that individualizes Dasein by stripping away the comfortable familiarity of das Man. "
                "In anxiety, the world as a whole becomes uncanny (unheimlich) — no longer a cozy home — "
                "and Dasein confronts the naked fact of its own thrownness: that it is, and has to be, "
                "without any ultimate justification or fixed essence to fall back on. "
                "This groundlessness is not simply negative; it is the very condition for authentic disclosure, "
                "for only when das Man's reassurances fall silent can Dasein hear the 'call of conscience' "
                "summoning it to own its existence in full."
            )
        elif any(
            w in t
            for w in [
                "meaning",
                "being",
                "exist",
                "ontolog",
                "metaphys",
                "truth",
                "real",
            ]
        ):
            return (
                "The guiding question of Heidegger's entire thinking is the Seinsfrage — the Question of Being: "
                "what does it mean for anything to be at all? "
                "Western metaphysics since Plato has, he argues, forgotten this question, treating Being as merely "
                "the most general concept or the highest entity, producing an epoch of nihilism and Gestell. "
                "Truth, for Heidegger, is not a property of propositions but aletheia — unconcealment — "
                "the primordial event by which entities emerge from concealment into the clearing (Lichtung) "
                "that Dasein itself is; falsehood and error are derivative forms of concealment. "
                "Recovering the Question of Being thus demands a 'destruction' of the metaphysical tradition "
                "to expose the forgotten experiences of Being that were covered over in its sedimented concepts."
            )
        elif any(
            w in t
            for w in [
                "knowledge",
                "epistemolog",
                "know",
                "cognition",
                "science",
                "understand",
            ]
        ):
            return (
                "Heidegger reframes knowing through the distinction between ready-to-hand (zuhanden) "
                "and present-at-hand (vorhanden): in everyday practical engagement, equipment is transparent — "
                "the hammer withdraws into its use — and entities show up in their functional significance "
                "within the totality of involvements that is Dasein's world. "
                "Only when equipment breaks down does it become 'present-at-hand', an object of detached "
                "theoretical inspection — the mode science privileges and mistakenly takes as primary. "
                "Truth, as aletheia, is the pre-theoretical unconcealment in which Dasein, as the clearing (Lichtung), "
                "lets entities show themselves; all propositional correspondence-truth presupposes "
                "this more primordial disclosure that Dasein always already inhabits."
            )
        elif any(
            w in t
            for w in [
                "decision",
                "choice",
                "action",
                "resol",
                "commit",
                "care",
                "responsib",
            ]
        ):
            return (
                "Care (Sorge) is Heidegger's name for the fundamental structure of Dasein: "
                "Dasein is always 'ahead-of-itself' (projection into possibilities), "
                "'already-in' (thrownness into a factical situation it did not choose), "
                "and 'alongside' (absorbed in entities encountered within-the-world). "
                "Authentic decision, then, is not the free act of a will unconstrained by circumstance "
                "but resolute (Entschlossenheit) appropriation of one's thrown possibilities, "
                "undertaken in the awareness of finitude that Being-toward-death provides. "
                "Such resoluteness opens the moment of vision (Augenblick) in which Dasein "
                "can act from genuine understanding of its situation rather than from the directives of das Man."
            )
        else:
            return (
                "Heidegger invites us to ask the most fundamental question: What is the meaning of Being? "
                "Dasein — the entity that we ourselves are — is distinguished by its Being-in-the-world: "
                "not a subject facing an external object, but a care-structure always already engaged "
                "with a meaningful, historically transmitted world. "
                "Thrownness (Geworfenheit) reminds us that we find ourselves in situations not of our choosing, "
                "while projection (Entwurf) opens us toward future possibilities; "
                "authentic existence owns both poles in the light of Being-toward-death. "
                "Aletheia (unconcealment) names the primordial truth-event by which Being discloses itself "
                "through the clearing that Dasein is, prior to all theory and representation."
            )

    def _construct_reasoning(
        self,
        prompt: str,
        temporality: Dict[str, Any],
        authenticity: Dict[str, Any],
        thrownness: Dict[str, Any],
        care: Dict[str, Any],
        attunement: Dict[str, Any],
        angst: Dict[str, Any],
        being_toward_death: Dict[str, Any],
        das_man: Dict[str, Any],
        concepts: List[str],
    ) -> str:
        """Construct comprehensive Heideggerian reasoning."""
        applied = self._apply_heidegger_to_problem(prompt)
        reasoning = (
            f"{applied}\n\n"
            f"From a Heideggerian perspective, this text invites us to question "
            f"the nature of Being itself. "
            f"Temporal analysis: {temporality['primary_mode']} - {temporality['description']}. "
        )

        # Add authenticity assessment
        reasoning += (
            f"Authenticity: {authenticity['mode']} - {authenticity['description']}. "
        )

        # Add care structure
        reasoning += f"Care (Sorge): {care['structure']}. "

        # Add attunement
        if attunement["detected_moods"]:
            reasoning += f"Attunement: {attunement['primary_mood']} - {attunement['description']}. "

        # Add angst if present
        if angst["presence"] != "No Angst Evident":
            reasoning += f"Angst: {angst['description']}. "

        # Add being-toward-death
        reasoning += f"Being-toward-death: {being_toward_death['stance']}. "

        # Add das Man assessment
        reasoning += f"Das Man: {das_man['status']}. "

        # Add key concepts
        primary_concept = concepts[0] if concepts else "Being-in-the-world"
        reasoning += f"Central concept: {primary_concept}. "

        # Conclude with the question of Being
        reasoning += (
            "The question remains: What is the meaning of Being? "
            "Only by confronting anxiety, authentically owning our finitude, "
            "and dwelling thoughtfully can we approach this question."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Heideggerian analysis.

        Tensions arise from:
        - Inauthenticity (das Man / they-self)
        - Fleeing from anxiety and death
        - Fallenness into the everyday
        - Technological enframing
        - Limited temporal awareness
        """
        tension_score = 0
        tension_elements = []

        # Check authenticity
        authenticity = analysis["authenticity"]
        if authenticity["level"] == "Low":
            tension_score += 2
            tension_elements.append(f"Inauthentic mode: {authenticity['mode']}")
        elif authenticity["level"] == "Medium":
            tension_score += 1
            tension_elements.append("Unclear authentic/inauthentic status")

        # Check das Man
        das_man = analysis["das_man"]
        if das_man["individuality"] == "Low":
            tension_score += 2
            tension_elements.append("Lost in das Man")

        # Check being-toward-death
        btd = analysis["being_toward_death"]
        if "Evasion" in btd["stance"] or "Concealed" in btd["stance"]:
            tension_score += 2
            tension_elements.append("Fleeing from finitude")

        # Check fallenness
        fallenness = analysis["fallenness"]
        if fallenness["total_score"] >= 3:
            tension_score += 1
            tension_elements.append("Absorbed in fallenness")

        # Check angst
        angst = analysis["angst"]
        if angst["presence"] == "No Angst Evident":
            tension_score += 1
            tension_elements.append("Anxiety concealed - possible flight")

        # Check temporal awareness
        temporality = analysis["temporality"]
        if temporality["temporal_authenticity"] == "Inauthentic":
            tension_score += 1
            tension_elements.append("Inauthentic temporality")

        # Check technology
        technology = analysis["technology"]
        if technology["danger_level"] == "High":
            tension_score += 1
            tension_elements.append("Danger of technological enframing")

        # Determine tension level
        if tension_score >= 6:
            level = "Very High"
            description = (
                "Deep existential crisis - lost in das Man, fleeing from Being"
            )
        elif tension_score >= 4:
            level = "High"
            description = "Significant tensions in existence and authenticity"
        elif tension_score >= 2:
            level = "Moderate"
            description = "Some tensions in authentic being"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, generally authentic"
        else:
            level = "Very Low"
            description = "Aligned with authentic Dasein"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": (
                tension_elements if tension_elements else ["No significant tensions"]
            ),
        }
