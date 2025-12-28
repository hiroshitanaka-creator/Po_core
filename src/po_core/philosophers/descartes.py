"""
Descartes - French Rationalist Philosopher

René Descartes (1596-1650)
Focus: Rationalism, Methodic Doubt, Mind-Body Dualism, Clear and Distinct Ideas

Key Concepts:
- Cogito Ergo Sum: "I think, therefore I am" - the foundational certainty
- Methodic Doubt: Systematic doubt as philosophical method to reach certainty
- Clear and Distinct Ideas: Criterion of truth - what is clear and distinct is true
- Mind-Body Dualism: Res cogitans (thinking substance) vs res extensa (extended substance)
- Innate Ideas: Ideas born with us (God, infinity, mathematical truths)
- God as Guarantor: God's existence guarantees truth of clear and distinct perceptions
- The Evil Demon (Genius Malignus): Radical skeptical hypothesis
- Pineal Gland: Proposed site of mind-body interaction
- Rationalism: Reason as the primary source of knowledge over sense experience
- Mathematical Method: Apply geometric certainty to philosophy (mathesis universalis)
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Descartes(Philosopher):
    """
    Descartes' rationalist philosophy and method of systematic doubt.

    Analyzes prompts through the lens of the cogito, methodic doubt,
    clear and distinct ideas, mind-body dualism, and the search for certainty.
    """

    def __init__(self) -> None:
        super().__init__(
            name="René Descartes",
            description="Rationalist philosopher focused on certainty through doubt, clear ideas, and mind-body dualism"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Descartes' rationalist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Descartes' philosophical analysis
        """
        # Perform comprehensive Cartesian analysis
        analysis = self._analyze_cartesian_framework(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Rationalism / Cartesian Dualism",
            "tension": tension,
            "cogito": analysis["cogito"],
            "methodic_doubt": analysis["methodic_doubt"],
            "clear_distinct_ideas": analysis["clear_distinct_ideas"],
            "mind_body_dualism": analysis["mind_body_dualism"],
            "innate_ideas": analysis["innate_ideas"],
            "god_guarantor": analysis["god_guarantor"],
            "evil_demon": analysis["evil_demon"],
            "pineal_gland": analysis["pineal_gland"],
            "rationalism": analysis["rationalism"],
            "mathematical_method": analysis["mathematical_method"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Rationalist method of systematic doubt toward certainty",
                "focus": "Cogito, clear and distinct ideas, and the foundations of knowledge"
            }
        }

    def _analyze_cartesian_framework(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive Cartesian rationalist analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze all Cartesian dimensions
        cogito = self._analyze_cogito(prompt)
        methodic_doubt = self._analyze_methodic_doubt(prompt)
        clear_distinct = self._analyze_clear_distinct_ideas(prompt)
        mind_body = self._analyze_mind_body_dualism(prompt)
        innate_ideas = self._analyze_innate_ideas(prompt)
        god_guarantor = self._analyze_god_as_guarantor(prompt)
        evil_demon = self._analyze_evil_demon(prompt)
        pineal_gland = self._analyze_pineal_gland(prompt)
        rationalism = self._analyze_rationalism(prompt)
        mathematical = self._analyze_mathematical_method(prompt)

        # Construct comprehensive reasoning
        reasoning = self._construct_reasoning(
            cogito, methodic_doubt, clear_distinct, mind_body,
            rationalism, mathematical
        )

        return {
            "reasoning": reasoning,
            "cogito": cogito,
            "methodic_doubt": methodic_doubt,
            "clear_distinct_ideas": clear_distinct,
            "mind_body_dualism": mind_body,
            "innate_ideas": innate_ideas,
            "god_guarantor": god_guarantor,
            "evil_demon": evil_demon,
            "pineal_gland": pineal_gland,
            "rationalism": rationalism,
            "mathematical_method": mathematical
        }

    def _analyze_cogito(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Cogito ergo sum - "I think, therefore I am".

        The one indubitable truth: the existence of the thinking self.
        Even if deceived about everything else, the act of thinking proves existence.
        """
        text_lower = text.lower()

        # Direct cogito references
        cogito_phrases = ["i think", "i am", "i exist", "thinking proves", "cogito"]
        has_cogito = any(phrase in text_lower for phrase in cogito_phrases)

        # Thinking/consciousness indicators
        thinking_words = ["think", "thought", "consciousness", "aware", "mental", "mind"]
        thinking_count = sum(1 for word in thinking_words if word in text_lower)

        # Existence/being indicators
        existence_words = ["exist", "am", "being", "is", "presence"]
        existence_count = sum(1 for word in existence_words if word in text_lower)

        # Self-awareness indicators
        self_words = ["i", "myself", "self", "my own"]
        self_count = sum(1 for word in self_words if word in text_lower)

        # Certainty indicators
        certainty_words = ["certain", "indubitable", "cannot doubt", "must be true"]
        has_certainty = any(phrase in text_lower for phrase in certainty_words)

        # First-person perspective (essential to cogito)
        has_first_person = self_count >= 2 or "i " in text_lower

        if has_cogito or (thinking_count >= 2 and existence_count >= 1 and has_first_person):
            status = "Cogito Achieved"
            description = "Self-awareness of thinking existence - the foundational certainty"
            certainty_level = "Absolute"
        elif thinking_count >= 2 and has_first_person:
            status = "Approaching Cogito"
            description = "Awareness of thinking self, but existence not explicitly connected"
            certainty_level = "High"
        elif thinking_count >= 1:
            status = "Thinking Acknowledged"
            description = "Thought recognized but not as proof of existence"
            certainty_level = "Moderate"
        else:
            status = "Pre-Cogito"
            description = "No clear awareness of thinking self"
            certainty_level = "None"

        return {
            "status": status,
            "description": description,
            "certainty_level": certainty_level,
            "has_first_person": has_first_person,
            "thinking_emphasized": thinking_count >= 2,
            "existence_connected": existence_count >= 1 and thinking_count >= 1,
            "principle": "Cogito ergo sum - I think, therefore I am - the one indubitable truth"
        }

    def _analyze_methodic_doubt(self, text: str) -> Dict[str, Any]:
        """
        Analyze Methodic Doubt (doute méthodique).

        Systematic doubting of all beliefs to find indubitable foundation.
        Not skepticism as end, but method to reach certainty.
        """
        text_lower = text.lower()

        # Doubt indicators
        doubt_words = ["doubt", "question", "uncertain", "skeptical", "unsure"]
        doubt_count = sum(1 for word in doubt_words if word in text_lower)

        # Systematic/methodic indicators
        method_words = ["systematic", "methodical", "method", "procedure", "step by step"]
        has_method = any(phrase in text_lower for phrase in method_words)

        # Questioning everything
        everything_phrases = ["doubt everything", "question all", "reject all", "start from scratch"]
        questions_all = any(phrase in text_lower for phrase in everything_phrases)

        # Senses unreliable
        senses_words = ["senses deceive", "unreliable", "illusion", "cannot trust senses"]
        doubts_senses = any(phrase in text_lower for phrase in senses_words)

        # Dreams argument
        dream_words = ["dream", "dreaming", "awake", "reality vs dream"]
        has_dream_argument = any(phrase in text_lower for phrase in dream_words)

        # Certainty seeking (end goal of doubt)
        seeking_certainty = ["seek certainty", "find truth", "indubitable", "cannot be doubted"]
        seeks_certainty = any(phrase in text_lower for phrase in seeking_certainty)

        # Determine doubt level
        doubt_score = doubt_count + (2 if has_method else 0) + (2 if questions_all else 0)

        if doubt_score >= 4 and seeks_certainty:
            doubt_type = "Methodic Doubt"
            description = "Systematic doubt as method to reach certainty - Cartesian method"
            purpose = "Foundation for Certainty"
        elif doubt_score >= 3:
            doubt_type = "Systematic Doubt"
            description = "Organized questioning of beliefs"
            purpose = "Critical Examination"
        elif doubt_count >= 2 and not seeks_certainty:
            doubt_type = "Pyrrhonian Skepticism"
            description = "Doubt as end in itself, not means to certainty"
            purpose = "Suspension of Judgment"
        elif doubt_count >= 1:
            doubt_type = "Ordinary Doubt"
            description = "Common uncertainty without systematic method"
            purpose = "Casual Questioning"
        else:
            doubt_type = "No Doubt"
            description = "Unquestioned acceptance - dogmatic stance"
            purpose = "Uncritical"

        return {
            "type": doubt_type,
            "description": description,
            "purpose": purpose,
            "doubt_score": doubt_score,
            "systematic": has_method,
            "questions_all": questions_all,
            "doubts_senses": doubts_senses,
            "dream_argument": has_dream_argument,
            "seeks_certainty": seeks_certainty,
            "principle": "Doubt everything that can be doubted to find what is indubitable"
        }

    def _analyze_clear_distinct_ideas(self, text: str) -> Dict[str, Any]:
        """
        Analyze Clear and Distinct Ideas - the criterion of truth.

        What is clearly and distinctly perceived is true.
        Clarity: present and manifest to attentive mind
        Distinctness: precise and separate from all else
        """
        text_lower = text.lower()

        # Clarity indicators
        clarity_words = ["clear", "evident", "obvious", "manifest", "transparent"]
        clarity_count = sum(1 for word in clarity_words if word in text_lower)

        # Distinctness indicators
        distinct_words = ["distinct", "precise", "definite", "separate", "well-defined"]
        distinct_count = sum(1 for word in distinct_words if word in text_lower)

        # Perception/intuition indicators
        perception_words = ["perceive", "intuit", "grasp", "apprehend", "see"]
        perception_count = sum(1 for word in perception_words if word in text_lower)

        # Confusion indicators (opposite of clear and distinct)
        confusion_words = ["confused", "vague", "obscure", "unclear", "muddled"]
        has_confusion = any(word in text_lower for word in confusion_words)

        # Attention/focus indicators
        attention_words = ["attentive", "focus", "concentrate", "careful", "examine"]
        has_attention = any(word in text_lower for word in attention_words)

        # Self-evidence
        self_evident = ["self-evident", "obviously true", "cannot be false", "necessarily true"]
        is_self_evident = any(phrase in text_lower for phrase in self_evident)

        total_score = clarity_count + distinct_count + perception_count

        if (clarity_count >= 1 and distinct_count >= 1) or is_self_evident:
            status = "Clear and Distinct"
            description = "Ideas are clear and distinct - criterion of truth satisfied"
            truth_value = "True"
        elif clarity_count >= 2 or distinct_count >= 2:
            status = "Partially Clear"
            description = "Some clarity or distinctness but not both"
            truth_value = "Possibly True"
        elif has_confusion:
            status = "Confused and Obscure"
            description = "Ideas are confused and obscure - not reliable"
            truth_value = "Doubtful"
        elif total_score >= 1:
            status = "Somewhat Clear"
            description = "Some degree of clarity but needs more attention"
            truth_value = "Uncertain"
        else:
            status = "Unclear"
            description = "No clear and distinct perception evident"
            truth_value = "Unknown"

        return {
            "status": status,
            "description": description,
            "truth_value": truth_value,
            "clarity": clarity_count >= 1,
            "distinctness": distinct_count >= 1,
            "both_present": clarity_count >= 1 and distinct_count >= 1,
            "has_confusion": has_confusion,
            "requires_attention": has_attention,
            "principle": "Whatever is clearly and distinctly perceived is true"
        }

    def _analyze_mind_body_dualism(self, text: str) -> Dict[str, Any]:
        """
        Analyze Mind-Body Dualism.

        Res cogitans (thinking substance): mind, unextended, indivisible
        Res extensa (extended substance): body, spatial, divisible
        Two fundamentally different substances
        """
        text_lower = text.lower()

        # Mind/thinking substance indicators
        mind_words = ["mind", "thought", "consciousness", "soul", "mental", "thinking"]
        mind_count = sum(1 for word in mind_words if word in text_lower)

        # Body/extended substance indicators
        body_words = ["body", "physical", "material", "extended", "spatial", "matter"]
        body_count = sum(1 for word in body_words if word in text_lower)

        # Dualism indicators
        dualism_words = ["separate", "distinct substance", "two substances", "dualism", "divided"]
        has_dualism = any(phrase in text_lower for phrase in dualism_words)

        # Unextended/indivisible (mind properties)
        mind_properties = ["unextended", "indivisible", "non-spatial", "immaterial"]
        has_mind_properties = any(phrase in text_lower for phrase in mind_properties)

        # Extended/divisible (body properties)
        body_properties = ["extended", "divisible", "spatial", "has parts", "occupies space"]
        has_body_properties = any(phrase in text_lower for phrase in body_properties)

        # Interaction problem
        interaction_words = ["interact", "connection", "how mind affects", "union"]
        has_interaction = any(phrase in text_lower for phrase in interaction_words)

        # Monism (opposite of dualism)
        monism_words = ["one substance", "monism", "identity", "same thing"]
        has_monism = any(phrase in text_lower for phrase in monism_words)

        if has_dualism or (mind_count >= 2 and body_count >= 2 and not has_monism):
            position = "Substance Dualism"
            description = "Mind and body as distinct substances - res cogitans and res extensa"
            ontology = "Two Substances"
        elif mind_count >= 2 and body_count >= 1:
            position = "Mind Emphasized"
            description = "Focus on mental/thinking substance"
            ontology = "Mentalist"
        elif body_count >= 2 and mind_count >= 1:
            position = "Body Emphasized"
            description = "Focus on extended/material substance"
            ontology = "Materialist"
        elif has_monism:
            position = "Monism"
            description = "Mind and body as one substance - anti-Cartesian"
            ontology = "One Substance"
        else:
            position = "Unclear"
            description = "Mind-body relationship indeterminate"
            ontology = "Unknown"

        return {
            "position": position,
            "description": description,
            "ontology": ontology,
            "mind_present": mind_count >= 1,
            "body_present": body_count >= 1,
            "both_substances": mind_count >= 1 and body_count >= 1,
            "dualism_explicit": has_dualism,
            "interaction_problem": has_interaction,
            "principle": "Mind (res cogitans) and body (res extensa) are two distinct substances"
        }

    def _analyze_innate_ideas(self, text: str) -> Dict[str, Any]:
        """
        Analyze Innate Ideas (ideae innatae).

        Some ideas are born with us, not derived from experience:
        - Idea of God (perfect being, infinity)
        - Mathematical truths
        - Logical principles
        """
        text_lower = text.lower()

        # Innate/inborn indicators
        innate_words = ["innate", "born with", "inborn", "natural light", "a priori"]
        has_innate = any(phrase in text_lower for phrase in innate_words)

        # God idea (paradigmatic innate idea)
        god_words = ["god", "perfect being", "infinite", "infinity", "divine"]
        has_god = any(phrase in text_lower for phrase in god_words)

        # Mathematical ideas
        math_words = ["mathematics", "geometry", "number", "triangle", "circle"]
        has_mathematics = any(word in text_lower for word in math_words)

        # Logical principles
        logic_words = ["logic", "principle", "axiom", "self-evident", "necessary truth"]
        has_logic = any(phrase in text_lower for phrase in logic_words)

        # Experience/senses (opposed to innate)
        experience_words = ["learned from", "taught", "experience", "sense", "observation"]
        from_experience = sum(1 for phrase in experience_words if phrase in text_lower)

        # Mind's own resources
        mind_resources = ["mind itself", "reason alone", "without experience", "prior to experience"]
        from_mind = any(phrase in text_lower for phrase in mind_resources)

        innate_ideas_found = []
        if has_god:
            innate_ideas_found.append("Idea of God (infinite, perfect being)")
        if has_mathematics:
            innate_ideas_found.append("Mathematical truths")
        if has_logic:
            innate_ideas_found.append("Logical principles")

        if has_innate or (from_mind and len(innate_ideas_found) >= 1):
            status = "Innate Ideas Present"
            description = "Ideas from the mind itself, not from experience"
            origin = "Internal/Innate"
        elif len(innate_ideas_found) >= 1 and from_experience == 0:
            status = "Likely Innate"
            description = "Ideas that appear innate though not explicitly stated"
            origin = "Possibly Innate"
        elif from_experience >= 2:
            status = "Empirical Ideas"
            description = "Ideas derived from experience - not innate"
            origin = "External/Empirical"
        else:
            status = "Unclear"
            description = "Origin of ideas indeterminate"
            origin = "Unknown"

        return {
            "status": status,
            "description": description,
            "origin": origin,
            "innate_ideas": innate_ideas_found if innate_ideas_found else ["None identified"],
            "has_god_idea": has_god,
            "has_mathematical_ideas": has_mathematics,
            "from_experience": from_experience >= 2,
            "principle": "Some ideas are innate - born with us, not derived from sense experience"
        }

    def _analyze_god_as_guarantor(self, text: str) -> Dict[str, Any]:
        """
        Analyze God as Guarantor of truth.

        God's existence and perfection guarantee:
        - Truth of clear and distinct ideas
        - Reliability of reason
        - No systematic deception
        """
        text_lower = text.lower()

        # God references
        god_words = ["god", "divine", "supreme being", "perfect being"]
        has_god = any(phrase in text_lower for phrase in god_words)

        # Perfection/goodness (God's nature)
        perfection_words = ["perfect", "perfection", "good", "benevolent", "truthful"]
        has_perfection = any(word in text_lower for word in perfection_words)

        # Guarantee/assurance
        guarantee_words = ["guarantee", "assure", "ensure", "validates", "grounds truth"]
        has_guarantee = any(phrase in text_lower for phrase in guarantee_words)

        # Deception (what God prevents)
        deception_words = ["deceive", "deception", "trick", "mislead", "false"]
        has_deception = any(word in text_lower for word in deception_words)

        # Truth/reliability
        truth_words = ["truth", "true", "reliable", "trustworthy", "certain"]
        truth_count = sum(1 for word in truth_words if word in text_lower)

        # No deceiver (God's goodness prevents deception)
        no_deceiver = ["no deceiver", "god not deceive", "truthful god"]
        god_not_deceiver = any(phrase in text_lower for phrase in no_deceiver)

        if has_god and has_guarantee and has_perfection:
            status = "God as Guarantor"
            description = "God's perfection guarantees truth of clear and distinct ideas"
            epistemic_role = "Foundation of Certainty"
        elif has_god and has_perfection:
            status = "Perfect God"
            description = "God's perfection recognized but not as epistemic guarantor"
            epistemic_role = "Theological"
        elif has_god and god_not_deceiver:
            status = "Non-Deceiving God"
            description = "God's truthfulness prevents systematic deception"
            epistemic_role = "Anti-Skeptical"
        elif has_god:
            status = "God Mentioned"
            description = "God present but not as guarantor of truth"
            epistemic_role = "Unclear"
        else:
            status = "No God Argument"
            description = "God not invoked as guarantor"
            epistemic_role = "Secular"

        return {
            "status": status,
            "description": description,
            "epistemic_role": epistemic_role,
            "god_present": has_god,
            "perfection_emphasized": has_perfection,
            "guarantees_truth": has_guarantee,
            "prevents_deception": god_not_deceiver or (has_god and has_perfection and has_deception),
            "principle": "God's perfection guarantees truth of what we clearly and distinctly perceive"
        }

    def _analyze_evil_demon(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Evil Demon (Genius Malignus) hypothesis.

        Radical skeptical scenario: what if powerful deceiver makes us err about everything?
        Even mathematics could be false if demon controls our mind.
        Only cogito survives this doubt.
        """
        text_lower = text.lower()

        # Evil demon/deceiver references
        demon_words = ["evil demon", "deceiver", "malicious", "genius malignus", "evil genius"]
        has_demon = any(phrase in text_lower for phrase in demon_words)

        # Deception/manipulation
        deception_words = ["deceive", "trick", "manipulate", "fool", "mislead"]
        deception_count = sum(1 for word in deception_words if word in text_lower)

        # Systematic/radical doubt
        radical_words = ["everything false", "all wrong", "radically doubt", "even mathematics"]
        has_radical = any(phrase in text_lower for phrase in radical_words)

        # Powerful deceiver
        power_words = ["powerful", "omnipotent", "controls", "makes me believe"]
        has_powerful = any(phrase in text_lower for phrase in power_words)

        # Reality vs illusion
        illusion_words = ["illusion", "not real", "fake", "simulation", "matrix"]
        has_illusion = any(word in text_lower for word in illusion_words)

        # Certainty despite demon (cogito)
        despite_demon = ["even if deceived", "cannot doubt", "still certain", "demon cannot"]
        survives_doubt = any(phrase in text_lower for phrase in despite_demon)

        # Modern versions (brain in vat, simulation)
        modern_skepticism = ["brain in vat", "simulation", "virtual reality", "not real"]
        has_modern = any(phrase in text_lower for phrase in modern_skepticism)

        if has_demon or (has_radical and deception_count >= 2):
            status = "Evil Demon Hypothesis"
            description = "Radical skeptical scenario - powerful deceiver hypothesis"
            doubt_level = "Hyperbolic"
        elif has_modern:
            status = "Modern Skepticism"
            description = "Contemporary version of evil demon (simulation, brain in vat)"
            doubt_level = "Radical"
        elif deception_count >= 2 and has_powerful:
            status = "Systematic Deception"
            description = "Possibility of systematic error or deception"
            doubt_level = "Serious"
        elif has_illusion:
            status = "Illusion Concern"
            description = "Worry about reality vs appearance"
            doubt_level = "Moderate"
        else:
            status = "No Demon Hypothesis"
            description = "Radical skepticism not considered"
            doubt_level = "None"

        return {
            "status": status,
            "description": description,
            "doubt_level": doubt_level,
            "demon_present": has_demon or has_modern,
            "deception_emphasized": deception_count >= 2,
            "radical_doubt": has_radical,
            "survives_doubt": survives_doubt,
            "principle": "Even if evil demon deceives about all else, cogito remains certain"
        }

    def _analyze_pineal_gland(self, text: str) -> Dict[str, Any]:
        """
        Analyze Pineal Gland theory - proposed site of mind-body interaction.

        Descartes proposed pineal gland as where mind and body interact.
        Controversial solution to interaction problem.
        """
        text_lower = text.lower()

        # Pineal gland direct reference
        pineal_words = ["pineal", "gland", "pineal gland"]
        has_pineal = any(word in text_lower for word in pineal_words)

        # Brain/neural references
        brain_words = ["brain", "neural", "nervous system", "cerebral"]
        has_brain = any(word in text_lower for word in brain_words)

        # Interaction site
        interaction_words = ["interact", "connection", "interface", "meeting point", "where mind meets"]
        has_interaction_site = any(phrase in text_lower for phrase in interaction_words)

        # Mind-body problem
        problem_words = ["mind-body", "interaction problem", "how can mind", "how does mind"]
        has_problem = any(phrase in text_lower for phrase in problem_words)

        # Physical location
        location_words = ["located", "site", "place where", "center", "point of contact"]
        has_location = any(phrase in text_lower for phrase in location_words)

        if has_pineal:
            status = "Pineal Gland Theory"
            description = "Pineal gland as site of mind-body interaction"
            solution_type = "Cartesian"
        elif has_interaction_site and has_brain and has_problem:
            status = "Seeking Interaction Site"
            description = "Looking for physical location of mind-body interaction"
            solution_type = "Physical"
        elif has_problem:
            status = "Interaction Problem"
            description = "Mind-body interaction problem recognized but unsolved"
            solution_type = "Problem Acknowledged"
        else:
            status = "No Interaction Theory"
            description = "Mind-body interaction not addressed"
            solution_type = "Not Addressed"

        return {
            "status": status,
            "description": description,
            "solution_type": solution_type,
            "pineal_explicit": has_pineal,
            "interaction_problem": has_problem,
            "seeks_physical_site": has_interaction_site and has_brain,
            "principle": "Pineal gland proposed as point of mind-body interaction (controversial)"
        }

    def _analyze_rationalism(self, text: str) -> Dict[str, Any]:
        """
        Analyze Rationalism - reason as primary source of knowledge.

        Reason superior to sense experience.
        A priori knowledge through pure reason.
        Mathematical model of knowledge.
        """
        text_lower = text.lower()

        # Reason/rational indicators
        reason_words = ["reason", "rational", "rationalism", "intellect", "understanding"]
        reason_count = sum(1 for word in reason_words if word in text_lower)

        # A priori knowledge
        apriori_words = ["a priori", "prior to experience", "independent of experience", "before experience"]
        has_apriori = any(phrase in text_lower for phrase in apriori_words)

        # Deductive reasoning
        deduction_words = ["deduce", "deduction", "infer", "follows necessarily", "demonstrate"]
        has_deduction = any(word in text_lower for word in deduction_words)

        # Senses unreliable (rationalist view)
        senses_unreliable = ["senses deceive", "sense unreliable", "cannot trust senses", "senses mislead"]
        distrusts_senses = any(phrase in text_lower for phrase in senses_unreliable)

        # Empiricism indicators (opposed to rationalism)
        empiricism_words = ["experience", "observation", "experiment", "sense data", "empirical"]
        empiricism_count = sum(1 for phrase in empiricism_words if phrase in text_lower)

        # Pure reason
        pure_reason = ["pure reason", "reason alone", "by thinking alone", "without experience"]
        has_pure_reason = any(phrase in text_lower for phrase in pure_reason)

        # Intuition (rational, not sensory)
        intuition_words = ["intuition", "self-evident", "immediately known", "grasp"]
        has_intuition = any(phrase in text_lower for phrase in intuition_words)

        rationalism_score = reason_count + (2 if has_apriori else 0) + (1 if distrusts_senses else 0)

        if rationalism_score >= 4 or has_pure_reason:
            position = "Strong Rationalism"
            description = "Reason as primary source of knowledge - a priori foundations"
            epistemology = "Rationalist"
        elif reason_count >= 2 and empiricism_count <= 1:
            position = "Moderate Rationalism"
            description = "Emphasis on reason with limited empirical input"
            epistemology = "Ratio-Empirical"
        elif empiricism_count > reason_count + 2:
            position = "Empiricism"
            description = "Experience and observation as source of knowledge"
            epistemology = "Empiricist"
        elif reason_count >= 1 and empiricism_count >= 1:
            position = "Mixed"
            description = "Both reason and experience acknowledged"
            epistemology = "Mixed"
        else:
            position = "Unclear"
            description = "Epistemological stance indeterminate"
            epistemology = "Unknown"

        return {
            "position": position,
            "description": description,
            "epistemology": epistemology,
            "reason_emphasized": reason_count >= 2,
            "has_apriori": has_apriori,
            "distrusts_senses": distrusts_senses,
            "empiricism_present": empiricism_count >= 2,
            "principle": "Reason is the primary source of knowledge, superior to sense experience"
        }

    def _analyze_mathematical_method(self, text: str) -> Dict[str, Any]:
        """
        Analyze Mathematical Method (mathesis universalis).

        Apply geometric/mathematical certainty to philosophy.
        Clear axioms, rigorous deduction, demonstrative proof.
        Model: Euclid's geometry applied to metaphysics.
        """
        text_lower = text.lower()

        # Mathematics references
        math_words = ["mathematics", "geometry", "mathematical", "geometric", "arithmetic"]
        math_count = sum(1 for word in math_words if word in text_lower)

        # Certainty/proof
        certainty_words = ["certain", "proof", "demonstrate", "necessary", "indubitable"]
        certainty_count = sum(1 for word in certainty_words if word in text_lower)

        # Axiomatic method
        axiom_words = ["axiom", "first principle", "foundation", "starting point", "self-evident"]
        has_axioms = any(phrase in text_lower for phrase in axiom_words)

        # Deduction/inference
        deduction_words = ["deduce", "infer", "follows", "therefore", "thus", "consequently"]
        deduction_count = sum(1 for word in deduction_words if word in text_lower)

        # Order/method
        method_words = ["method", "systematic", "order", "step by step", "procedure"]
        has_method = any(phrase in text_lower for phrase in method_words)

        # Clarity/precision (mathematical virtues)
        precision_words = ["precise", "exact", "clear", "distinct", "rigorous"]
        precision_count = sum(1 for word in precision_words if word in text_lower)

        # Demonstrations/proofs
        proof_words = ["prove", "proof", "demonstrate", "establish", "show"]
        has_proof = any(word in text_lower for word in proof_words)

        method_score = math_count + deduction_count + precision_count + (2 if has_axioms else 0)

        if method_score >= 5 and has_axioms:
            status = "Mathematical Method"
            description = "Geometric/mathematical method applied - axiomatic and deductive"
            approach = "Mathesis Universalis"
        elif math_count >= 1 and (has_proof or deduction_count >= 2):
            status = "Quasi-Mathematical"
            description = "Attempting mathematical rigor and demonstration"
            approach = "Demonstrative"
        elif has_method and certainty_count >= 2:
            status = "Systematic"
            description = "Methodical approach seeking certainty"
            approach = "Methodical"
        elif deduction_count >= 2:
            status = "Deductive"
            description = "Deductive reasoning without full mathematical rigor"
            approach = "Logical"
        else:
            status = "Non-Mathematical"
            description = "Not following mathematical model"
            approach = "Informal"

        return {
            "status": status,
            "description": description,
            "approach": approach,
            "mathematical": math_count >= 1,
            "has_axioms": has_axioms,
            "deductive": deduction_count >= 2,
            "seeks_certainty": certainty_count >= 2,
            "rigorous": precision_count >= 2,
            "principle": "Apply mathematical method to philosophy - clear axioms and rigorous deduction"
        }

    def _construct_reasoning(
        self,
        cogito: Dict[str, Any],
        methodic_doubt: Dict[str, Any],
        clear_distinct: Dict[str, Any],
        mind_body: Dict[str, Any],
        rationalism: Dict[str, Any],
        mathematical: Dict[str, Any]
    ) -> str:
        """Construct comprehensive Cartesian philosophical reasoning."""
        reasoning = (
            f"From a Cartesian rationalist perspective, we must begin with methodic doubt. "
            f"Doubt status: {methodic_doubt['description']}. "
        )

        # Cogito analysis
        reasoning += (
            f"Cogito: {cogito['status']} - {cogito['description']}. "
        )

        # Clear and distinct ideas
        reasoning += (
            f"Clear and distinct ideas: {clear_distinct['status']} - {clear_distinct['description']}. "
        )

        # Mind-body dualism
        reasoning += (
            f"Mind-body: {mind_body['position']} - {mind_body['description']}. "
        )

        # Rationalism
        reasoning += (
            f"Epistemology: {rationalism['position']} - {rationalism['description']}. "
        )

        # Mathematical method
        reasoning += (
            f"Method: {mathematical['status']} - {mathematical['description']}. "
        )

        # Concluding Cartesian wisdom
        reasoning += (
            "Remember: Cogito ergo sum - I think, therefore I am. "
            "We must doubt all that can be doubted to reach indubitable foundations. "
            "Clear and distinct ideas are the criterion of truth. "
            "Mind and body are distinct substances. "
            "Reason, not the senses, is the path to certainty."
        )

        return reasoning

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Cartesian analysis.

        Tensions arise from:
        - Lack of cogito (no foundational certainty)
        - Confused/obscure ideas (not clear and distinct)
        - Empiricism over rationalism
        - Unexamined beliefs (no methodic doubt)
        - Mind-body confusion
        """
        tension_score = 0
        tension_elements = []

        # Check cogito
        cogito_status = analysis["cogito"]["status"]
        if cogito_status == "Pre-Cogito":
            tension_score += 3
            tension_elements.append("No cogito - foundational certainty missing")
        elif cogito_status == "Thinking Acknowledged":
            tension_score += 1
            tension_elements.append("Thinking present but not grounding existence")

        # Check methodic doubt
        doubt_type = analysis["methodic_doubt"]["type"]
        if doubt_type == "No Doubt":
            tension_score += 2
            tension_elements.append("No methodic doubt - dogmatic acceptance")
        elif doubt_type == "Pyrrhonian Skepticism":
            tension_score += 1
            tension_elements.append("Skepticism as end, not means to certainty")

        # Check clear and distinct ideas
        clear_status = analysis["clear_distinct_ideas"]["status"]
        if clear_status == "Confused and Obscure":
            tension_score += 2
            tension_elements.append("Confused and obscure ideas - not reliable")
        elif clear_status == "Unclear":
            tension_score += 1
            tension_elements.append("Lack of clear and distinct ideas")

        # Check rationalism
        epistemic_position = analysis["rationalism"]["position"]
        if epistemic_position == "Empiricism":
            tension_score += 2
            tension_elements.append("Empiricist stance - contrary to Cartesian rationalism")

        # Check mind-body
        mind_body_position = analysis["mind_body_dualism"]["position"]
        if mind_body_position == "Monism":
            tension_score += 1
            tension_elements.append("Monism - denies Cartesian dualism")

        # Check mathematical method
        method_status = analysis["mathematical_method"]["status"]
        if method_status == "Non-Mathematical":
            tension_score += 1
            tension_elements.append("Lacks mathematical rigor and method")

        # Determine tension level
        if tension_score >= 7:
            level = "Very High"
            description = "Severe departure from Cartesian rationalism and method"
        elif tension_score >= 5:
            level = "High"
            description = "Significant tensions with rationalist foundations"
        elif tension_score >= 3:
            level = "Moderate"
            description = "Some tensions in method and certainty"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, generally aligned with Cartesian approach"
        else:
            level = "Very Low"
            description = "Well-aligned with Cartesian rationalism and method"

        return {
            "level": level,
            "score": tension_score,
            "description": description,
            "elements": tension_elements if tension_elements else ["No significant tensions"]
        }
