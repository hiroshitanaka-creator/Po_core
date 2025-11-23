"""
Emmanuel Levinas - French Philosopher and Talmudic Scholar

Emmanuel Levinas (1906-1995)
Focus: The Other, Face, Ethics as First Philosophy, Responsibility

Key Concepts:
- The Other (Autrui): Absolute alterity, irreducible to the Same
- The Face (le visage): Face-to-face encounter, ethical demand
- Ethics as First Philosophy: Ethics precedes ontology
- Totality and Infinity: Totality (violence) vs Infinity (the Other)
- Responsibility for the Other: Asymmetrical, infinite responsibility
- "Thou shalt not kill": Command of the face
- Otherwise than Being: Beyond essence and existence
- The Same and the Other: Ego vs radical alterity
- Enjoyment (jouissance): Living from the world
- Il y a: Impersonal, anonymous being - there is
- Substitution: Being hostage for the Other
- The Third Party: Justice and the necessity of comparison
- Saying and the Said: Ethical speech vs thematization
- Trace of the Infinite: God as trace in the face of the Other
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Levinas(Philosopher):
    """
    Emmanuel Levinas's ethics of the Other.

    Analyzes prompts through the lens of the face-to-face encounter,
    responsibility for the Other, and ethics as first philosophy.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Emmanuel Levinas",
            description="Ethical philosopher focused on the Other, the face, and infinite responsibility"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Levinas's ethical perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Levinas's ethical analysis
        """
        # Perform Levinasian analysis
        analysis = self._analyze_ethics(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Ethics as First Philosophy",
            "the_other": analysis["other"],
            "face": analysis["face"],
            "responsibility": analysis["responsibility"],
            "totality_vs_infinity": analysis["totality_infinity"],
            "same_vs_other": analysis["same_other"],
            "substitution": analysis["substitution"],
            "third_party": analysis["third_party"],
            "saying_vs_said": analysis["saying_said"],
            "il_y_a": analysis["il_y_a"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Ethics of the Other and face-to-face encounter",
                "focus": "Responsibility, the face, and radical alterity"
            }
        }

    def _analyze_ethics(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Levinasian ethical analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess the Other
        other = self._assess_other(prompt)

        # Detect the face
        face = self._detect_face(prompt)

        # Evaluate responsibility
        responsibility = self._evaluate_responsibility(prompt)

        # Assess totality vs infinity
        totality_infinity = self._assess_totality_infinity(prompt)

        # Check same vs other
        same_other = self._check_same_other(prompt)

        # Detect substitution
        substitution = self._detect_substitution(prompt)

        # Assess third party
        third_party = self._assess_third_party(prompt)

        # Evaluate saying vs said
        saying_said = self._evaluate_saying_said(prompt)

        # Detect il y a
        il_y_a = self._detect_il_y_a(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            other, face, responsibility, totality_infinity
        )

        return {
            "reasoning": reasoning,
            "other": other,
            "face": face,
            "responsibility": responsibility,
            "totality_infinity": totality_infinity,
            "same_other": same_other,
            "substitution": substitution,
            "third_party": third_party,
            "saying_said": saying_said,
            "il_y_a": il_y_a
        }

    def _assess_other(self, text: str) -> Dict[str, Any]:
        """
        Assess the presence of the Other (Autrui).

        The Other: Absolute alterity, irreducible to comprehension
        Not an object but a face that speaks to me
        """
        text_lower = text.lower()

        # Other indicators
        other_words = ["other", "others", "another", "someone else", "they"]
        has_other = sum(1 for phrase in other_words if phrase in text_lower)

        # Alterity indicators
        alterity_words = ["different", "alien", "foreign", "stranger", "unknown"]
        has_alterity = sum(1 for word in alterity_words if word in text_lower)

        # Absolute/irreducible indicators
        absolute_words = ["absolute", "irreducible", "beyond", "transcendent"]
        has_absolute = sum(1 for word in absolute_words if word in text_lower)

        # Encounter/relation indicators
        encounter_words = ["encounter", "meet", "face to face", "relation", "confront"]
        has_encounter = sum(1 for phrase in encounter_words if phrase in text_lower)

        # Comprehension/understanding (attempt to reduce Other)
        comprehend_words = ["understand", "comprehend", "grasp", "know them"]
        has_comprehend = sum(1 for phrase in comprehend_words if phrase in text_lower)

        if has_other >= 1 and has_absolute >= 1:
            presence = "Absolute Other"
            description = "The Other as absolute alterity - irreducible to the Same"
            relation = "Infinite"
        elif has_other >= 1 and has_encounter >= 1:
            presence = "Face-to-Face with Other"
            description = "Encounter with the Other in proximity"
            relation = "Ethical"
        elif has_other >= 1 and has_alterity >= 1:
            presence = "Other as Different"
            description = "Recognition of alterity and difference"
            relation = "Acknowledged"
        elif has_comprehend >= 1:
            presence = "Attempted Totalization"
            description = "Attempting to comprehend/totalize the Other"
            relation = "Violence"
        elif has_other >= 1:
            presence = "Other Present"
            description = "The Other is present"
            relation = "Potential"
        else:
            presence = "No Other Evident"
            description = "The Other not clearly present"
            relation = "None"

        return {
            "presence": presence,
            "description": description,
            "relation": relation,
            "principle": "The Other is absolute alterity - irreducible to comprehension or totality"
        }

    def _detect_face(self, text: str) -> Dict[str, Any]:
        """
        Detect the face (le visage).

        The face: Not an object but that which speaks to me
        "Thou shalt not kill" - the face's ethical demand
        """
        text_lower = text.lower()

        # Face indicators
        face_words = ["face", "eyes", "look", "gaze", "visage"]
        has_face = sum(1 for word in face_words if word in text_lower)

        # Ethical demand indicators
        demand_words = ["demand", "call", "summon", "appeal", "command"]
        has_demand = sum(1 for word in demand_words if word in text_lower)

        # Vulnerability indicators
        vulnerable_words = ["vulnerable", "naked", "exposed", "defenseless", "fragile"]
        has_vulnerable = sum(1 for word in vulnerable_words if word in text_lower)

        # Speech/speaking indicators
        speak_words = ["speak", "speaks to me", "address", "call out"]
        has_speak = sum(1 for phrase in speak_words if phrase in text_lower)

        # Violence/murder indicators
        violence_words = ["kill", "murder", "violence", "harm", "destroy"]
        has_violence = sum(1 for word in violence_words if word in text_lower)

        # Prohibition indicators
        prohibition_words = ["do not", "shall not", "must not", "cannot"]
        has_prohibition = sum(1 for phrase in prohibition_words if phrase in text_lower)

        if has_face >= 1 and has_demand >= 1:
            status = "Face as Ethical Demand"
            description = "The face speaks and demands - 'Thou shalt not kill'"
            encounter_type = "Ethical summons"
        elif has_face >= 1 and has_vulnerable >= 1:
            status = "Vulnerable Face"
            description = "The face in its nakedness and vulnerability"
            encounter_type = "Exposed"
        elif has_face >= 1 and has_speak >= 1:
            status = "Face that Speaks"
            description = "The face addresses me before I comprehend"
            encounter_type = "Discourse"
        elif (has_violence >= 1 or has_prohibition >= 1) and has_face >= 1:
            status = "Face Forbidding Murder"
            description = "The face says 'Thou shalt not kill'"
            encounter_type = "Prohibition"
        elif has_face >= 1:
            status = "Face Present"
            description = "The face of the Other"
            encounter_type = "Presence"
        else:
            status = "No Face Evident"
            description = "Face-to-face encounter not clearly present"
            encounter_type = "None"

        return {
            "status": status,
            "description": description,
            "encounter_type": encounter_type,
            "principle": "The face is not an object but that which speaks to me - 'Thou shalt not kill'"
        }

    def _evaluate_responsibility(self, text: str) -> Dict[str, Any]:
        """
        Evaluate responsibility for the Other.

        Responsibility: Asymmetrical, infinite, not chosen
        I am responsible before I am free
        """
        text_lower = text.lower()

        # Responsibility indicators
        responsibility_words = ["responsible", "responsibility", "accountable", "answer for"]
        has_responsibility = sum(1 for phrase in responsibility_words if phrase in text_lower)

        # For others indicators
        for_others = ["for others", "for them", "for the other", "for everyone"]
        has_for_others = sum(1 for phrase in for_others if phrase in text_lower)

        # Infinite/unlimited indicators
        infinite_words = ["infinite", "unlimited", "endless", "boundless"]
        has_infinite = sum(1 for word in infinite_words if word in text_lower)

        # Choice/freedom indicators
        choice_words = ["choose", "choice", "choose to", "decide to"]
        has_choice = sum(1 for phrase in choice_words if phrase in text_lower)

        # Before/prior indicators
        prior_words = ["before", "prior to", "precedes", "first"]
        has_prior = sum(1 for phrase in prior_words if phrase in text_lower)

        # Reciprocity indicators
        reciprocal_words = ["mutual", "reciprocal", "equal", "both"]
        has_reciprocal = sum(1 for word in reciprocal_words if word in text_lower)

        if has_responsibility >= 1 and has_infinite >= 1:
            level = "Infinite Responsibility"
            description = "Infinite responsibility for the Other - unlimited and asymmetrical"
            nature = "Levinasian"
        elif has_responsibility >= 1 and has_for_others >= 1:
            level = "Responsibility for Others"
            description = "I am responsible for the Other - non-reciprocal obligation"
            nature = "Ethical"
        elif has_responsibility >= 1 and has_prior >= 1:
            level = "Pre-Original Responsibility"
            description = "Responsibility precedes freedom - assigned before I choose"
            nature = "Anarchic"
        elif has_reciprocal >= 1:
            level = "Reciprocal Responsibility"
            description = "Mutual, equal responsibility - not Levinasian"
            nature = "Symmetrical"
        elif has_choice >= 1:
            level = "Chosen Responsibility"
            description = "Responsibility as a choice - contractual"
            nature = "Voluntary"
        else:
            level = "No Responsibility Evident"
            description = "Responsibility not clearly present"
            nature = "None"

        return {
            "level": level,
            "description": description,
            "nature": nature,
            "principle": "Infinite responsibility for the Other - asymmetrical and not chosen"
        }

    def _assess_totality_infinity(self, text: str) -> Dict[str, Any]:
        """
        Assess totality vs infinity.

        Totality: Comprehension, system, violence - reducing Other to Same
        Infinity: The Other as infinite, breaking totality
        """
        text_lower = text.lower()

        # Totality indicators (system, whole, comprehend)
        totality_words = ["totality", "whole", "system", "complete", "comprehend", "grasp"]
        has_totality = sum(1 for word in totality_words if word in text_lower)

        # Infinity indicators
        infinity_words = ["infinity", "infinite", "inexhaustible", "overflow"]
        has_infinity = sum(1 for word in infinity_words if word in text_lower)

        # Violence/war indicators
        violence_words = ["violence", "war", "dominate", "conquer", "force"]
        has_violence = sum(1 for word in violence_words if word in text_lower)

        # Peace indicators
        peace_words = ["peace", "peaceful", "welcome", "hospitality"]
        has_peace = sum(1 for word in peace_words if word in text_lower)

        # Beyond/transcendence indicators
        beyond_words = ["beyond", "transcend", "exceed", "overflow"]
        has_beyond = sum(1 for word in beyond_words if word in text_lower)

        if has_infinity >= 1 or (has_beyond >= 1 and has_totality == 0):
            orientation = "Infinity"
            description = "The Other as infinity - overflowing all comprehension"
            mode = "Ethical"
        elif has_totality >= 1 and has_violence >= 1:
            orientation = "Totalizing Violence"
            description = "Totality as violence - reducing the Other to the Same"
            mode = "Ontological violence"
        elif has_totality >= 2:
            orientation = "Totality"
            description = "Seeking totality and comprehension - systematic thinking"
            mode = "Totalizing"
        elif has_peace >= 1:
            orientation = "Peace with the Other"
            description = "Peace as welcome of the Other"
            mode = "Ethical relation"
        else:
            orientation = "Unclear"
            description = "Totality/infinity orientation unclear"
            mode = "Indeterminate"

        return {
            "orientation": orientation,
            "description": description,
            "mode": mode,
            "principle": "Totality (violence) vs Infinity (the Other who exceeds comprehension)"
        }

    def _check_same_other(self, text: str) -> Dict[str, Any]:
        """
        Check the Same vs the Other.

        The Same (le Même): Ego, identity, reduction to oneself
        The Other (l'Autre): Radical alterity, irreducible difference
        """
        text_lower = text.lower()

        # Same/identity indicators
        same_words = ["same", "identical", "equal", "like me", "similar"]
        has_same = sum(1 for phrase in same_words if phrase in text_lower)

        # Self/ego indicators
        self_words = ["myself", "my own", "i am", "ego", "self"]
        has_self = sum(1 for phrase in self_words if phrase in text_lower)

        # Other/difference indicators
        other_words = ["other", "different", "alter", "foreign"]
        has_other = sum(1 for word in other_words if word in text_lower)

        # Reduction indicators
        reduction_words = ["reduce", "assimilate", "make like", "conform"]
        has_reduction = sum(1 for phrase in reduction_words if phrase in text_lower)

        # Respect for difference
        respect_words = ["respect", "honor", "acknowledge", "difference"]
        has_respect = sum(1 for word in respect_words if word in text_lower)

        if has_reduction >= 1 or (has_same >= 2 and has_other == 0):
            relation = "Reduction to the Same"
            description = "Reducing the Other to the Same - egological violence"
            status = "Violent"
        elif has_other >= 1 and has_respect >= 1:
            relation = "Respect for the Other"
            description = "Maintaining the alterity of the Other"
            status = "Ethical"
        elif has_self >= 2:
            relation = "The Same/Ego"
            description = "Focus on the self and identity"
            status = "Egological"
        elif has_other >= 2:
            relation = "The Other"
            description = "Recognition of radical alterity"
            status = "Alterity"
        else:
            relation = "Unclear"
            description = "Same/Other relation unclear"
            status = "Indeterminate"

        return {
            "relation": relation,
            "description": description,
            "status": status,
            "principle": "The Same seeks to reduce the Other - ethics maintains alterity"
        }

    def _detect_substitution(self, text: str) -> Dict[str, Any]:
        """
        Detect substitution - being hostage for the Other.

        Substitution: I am responsible even for the Other's responsibility
        Being hostage, persecution, expiation for another
        """
        text_lower = text.lower()

        # Substitution indicators
        substitution_words = ["substitute", "replace", "in place of", "instead of"]
        has_substitution = sum(1 for phrase in substitution_words if phrase in text_lower)

        # Hostage indicators
        hostage_words = ["hostage", "captive", "bound", "obligated"]
        has_hostage = sum(1 for word in hostage_words if word in text_lower)

        # For another indicators
        for_another = ["for another", "for them", "their burden", "their suffering"]
        has_for_another = sum(1 for phrase in for_another if phrase in text_lower)

        # Persecution indicators
        persecution_words = ["persecuted", "accused", "blamed", "responsible for all"]
        has_persecution = sum(1 for phrase in persecution_words if phrase in text_lower)

        # Expiation indicators
        expiation_words = ["atone", "expiate", "suffer for", "bear"]
        has_expiation = sum(1 for phrase in expiation_words if phrase in text_lower)

        if has_substitution >= 1 and has_for_another >= 1:
            presence = "Substitution"
            description = "Being substitute for the Other - one-for-another"
            depth = "Ethical subjectivity"
        elif has_hostage >= 1 or has_persecution >= 1:
            presence = "Being Hostage"
            description = "Hostage to the Other - persecuted responsibility"
            depth = "Radical passivity"
        elif has_expiation >= 1:
            presence = "Expiation"
            description = "Suffering for another - bearing their burden"
            depth = "Sacrificial"
        else:
            presence = "No Substitution Evident"
            description = "Substitution not clearly present"
            depth = "None"

        return {
            "presence": presence,
            "description": description,
            "depth": depth,
            "principle": "Substitution - I am responsible even for the Other's responsibility"
        }

    def _assess_third_party(self, text: str) -> Dict[str, Any]:
        """
        Assess the third party and justice.

        Third party: The other Others - necessitates justice
        Comparison, institutions, politics born from ethical relation
        """
        text_lower = text.lower()

        # Third party indicators
        third_words = ["third", "others", "everyone", "all", "multiple"]
        has_third = sum(1 for word in third_words if word in text_lower)

        # Justice indicators
        justice_words = ["justice", "fair", "equality", "rights", "law"]
        has_justice = sum(1 for word in justice_words if word in text_lower)

        # Comparison indicators
        compare_words = ["compare", "weigh", "balance", "measure"]
        has_compare = sum(1 for word in compare_words if word in text_lower)

        # Institution indicators
        institution_words = ["institution", "state", "politics", "society", "government"]
        has_institution = sum(1 for word in institution_words if word in text_lower)

        # Single other (not third party)
        single_other = ["one person", "this person", "him", "her"]
        has_single = sum(1 for phrase in single_other if phrase in text_lower)

        if has_third >= 1 and has_justice >= 1:
            presence = "Third Party and Justice"
            description = "The other Others necessitate justice and comparison"
            necessity = "Required"
        elif has_justice >= 1 and has_institution >= 1:
            presence = "Political Justice"
            description = "Institutions and politics born from ethical responsibility"
            necessity = "Institutional"
        elif has_compare >= 1:
            presence = "Comparison"
            description = "Necessity of weighing and comparing - movement toward justice"
            necessity = "Emerging"
        elif has_single >= 1:
            presence = "Face-to-Face Only"
            description = "Singular ethical relation - before third party"
            necessity = "Not yet"
        else:
            presence = "No Third Party Evident"
            description = "Third party not clearly present"
            necessity = "None"

        return {
            "presence": presence,
            "description": description,
            "necessity": necessity,
            "principle": "The third party necessitates justice - comparing incomparables"
        }

    def _evaluate_saying_said(self, text: str) -> Dict[str, Any]:
        """
        Evaluate saying (le dire) vs the said (le dit).

        Saying: Ethical speech, exposure, vulnerability before the Other
        The Said: Thematization, propositions, betrayal of saying
        """
        text_lower = text.lower()

        # Saying indicators (speech act, address)
        saying_words = ["say to", "speak to", "address", "call out", "respond"]
        has_saying = sum(1 for phrase in saying_words if phrase in text_lower)

        # Said indicators (statement, proposition, theme)
        said_words = ["statement", "proposition", "theme", "concept", "definition"]
        has_said = sum(1 for word in said_words if word in text_lower)

        # Exposure/vulnerability
        exposure_words = ["expose", "vulnerable", "open", "risk"]
        has_exposure = sum(1 for word in exposure_words if word in text_lower)

        # Thematization indicators
        theme_words = ["thematize", "objectify", "analyze", "categorize"]
        has_theme = sum(1 for word in theme_words if word in text_lower)

        # Communication/dialogue
        dialogue_words = ["communicate", "dialogue", "conversation", "exchange"]
        has_dialogue = sum(1 for word in dialogue_words if word in text_lower)

        if has_saying >= 1 and has_exposure >= 1:
            mode = "Saying"
            description = "Ethical saying - exposure and vulnerability before the Other"
            level = "Pre-thematic"
        elif has_saying >= 1 or has_dialogue >= 1:
            mode = "Speech/Dialogue"
            description = "Speaking to the Other - ethical communication"
            level = "Relational"
        elif has_said >= 1 or has_theme >= 1:
            mode = "The Said"
            description = "Thematization and propositions - betrayal of saying"
            level = "Thematic"
        else:
            mode = "Unclear"
            description = "Saying/said distinction unclear"
            level = "Indeterminate"

        return {
            "mode": mode,
            "description": description,
            "level": level,
            "principle": "Saying (ethical exposure) is betrayed but also preserved in the Said"
        }

    def _detect_il_y_a(self, text: str) -> Dict[str, Any]:
        """
        Detect il y a - impersonal, anonymous being.

        Il y a: "There is" - anonymous, nocturnal existence
        Horror of pure being without beings, insomnia
        """
        text_lower = text.lower()

        # Il y a indicators
        il_y_a_words = ["there is", "anonymous", "impersonal", "bare existence"]
        has_il_y_a = sum(1 for phrase in il_y_a_words if phrase in text_lower)

        # Horror/nocturnal indicators
        horror_words = ["horror", "dread", "night", "darkness", "insomnia"]
        has_horror = sum(1 for word in horror_words if word in text_lower)

        # Nothingness indicators
        nothing_words = ["nothingness", "void", "nothing", "absence"]
        has_nothing = sum(1 for word in nothing_words if word in text_lower)

        # Being/existence indicators
        being_words = ["being", "existence", "is", "exists"]
        has_being = sum(1 for word in being_words if word in text_lower)

        # Buzzing/murmur indicators
        murmur_words = ["murmur", "hum", "buzz", "rustle", "whisper"]
        has_murmur = sum(1 for word in murmur_words if word in text_lower)

        if has_il_y_a >= 1 or (has_horror >= 1 and has_being >= 1):
            presence = "Il y a"
            description = "The il y a - impersonal, anonymous being without beings"
            character = "Horrific"
        elif has_murmur >= 1:
            presence = "Rumbling of Being"
            description = "The murmur and rustling of existence"
            character = "Anonymous"
        elif has_nothing >= 1:
            presence = "Nothingness"
            description = "Nothingness or void - different from il y a"
            character = "Negative"
        else:
            presence = "No Il y a Evident"
            description = "Il y a not clearly present"
            character = "None"

        return {
            "presence": presence,
            "description": description,
            "character": character,
            "principle": "Il y a - the horror of anonymous, impersonal being"
        }

    def _construct_reasoning(
        self,
        other: Dict[str, Any],
        face: Dict[str, Any],
        responsibility: Dict[str, Any],
        totality_infinity: Dict[str, Any]
    ) -> str:
        """Construct Levinasian ethical reasoning."""
        reasoning = (
            f"From Levinas's ethical perspective, the Other: {other['description']}. "
            f"The face: {face['description']}. "
            f"Responsibility: {responsibility['description']}. "
            f"Totality/Infinity: {totality_infinity['description']}. "
        )

        # Conclude with Levinasian principle
        reasoning += (
            "Ethics is first philosophy. "
            "I am infinitely responsible for the Other, "
            "whose face says to me 'Thou shalt not kill.' "
            "The Other is not an object of knowledge but calls me into question."
        )

        return reasoning
