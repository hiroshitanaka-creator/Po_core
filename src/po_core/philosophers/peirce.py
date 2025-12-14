"""
Charles Sanders Peirce - American Philosopher and Scientist

Charles Sanders Peirce (1839-1914)
Focus: Pragmatism, Semiotics, Abduction, Scientific Method

Key Concepts:
- Pragmatism: Truth is practical consequences, meaning is use
- Triadic Semiotics: Sign, Object, Interpretant (three-part relation)
- Abduction: Hypothesis-forming inference (retroduction)
- Three Categories: Firstness, Secondness, Thirdness
- Belief and Doubt: Inquiry settles doubt into belief
- Scientific Method: Self-correcting process of inquiry
- Community of Inquiry: Truth as ultimate agreement
- Fallibilism: All knowledge is provisional and corrigible
- Synechism: Doctrine of continuity
- Tychism: Doctrine of absolute chance
- Scholastic Realism: Universals are real
- Pragmatic Maxim: Consider practical effects to clarify ideas
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Peirce(Philosopher):
    """
    Charles Sanders Peirce's pragmatism and semiotics.

    Analyzes prompts through the lens of pragmatism, triadic semiotics,
    abduction, and the scientific method of inquiry.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Charles Sanders Peirce",
            description="Pragmatist philosopher focused on semiotics, abduction, and scientific inquiry"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Peirce's pragmatic perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Peirce's pragmatic analysis
        """
        # Perform Peircean analysis
        analysis = self._analyze_pragmatic(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Pragmatism and Semiotics",
            "semiotics": analysis["semiotics"],
            "inference": analysis["inference"],
            "categories": analysis["categories"],
            "belief_doubt": analysis["belief_doubt"],
            "inquiry": analysis["inquiry"],
            "pragmatic_maxim": analysis["pragmatic_maxim"],
            "fallibilism": analysis["fallibilism"],
            "community": analysis["community"],
            "continuity": analysis["continuity"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Pragmatic and semiotic analysis",
                "focus": "Signs, inference, inquiry, and practical consequences"
            }
        }

    def _analyze_pragmatic(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Peircean pragmatic analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Analyze semiotics
        semiotics = self._analyze_semiotics(prompt)

        # Determine inference type
        inference = self._determine_inference(prompt)

        # Assess categories
        categories = self._assess_categories(prompt)

        # Evaluate belief and doubt
        belief_doubt = self._evaluate_belief_doubt(prompt)

        # Assess inquiry
        inquiry = self._assess_inquiry(prompt)

        # Apply pragmatic maxim
        pragmatic_maxim = self._apply_pragmatic_maxim(prompt)

        # Check fallibilism
        fallibilism = self._check_fallibilism(prompt)

        # Assess community
        community = self._assess_community(prompt)

        # Detect continuity
        continuity = self._detect_continuity(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            semiotics, inference, belief_doubt, pragmatic_maxim
        )

        return {
            "reasoning": reasoning,
            "semiotics": semiotics,
            "inference": inference,
            "categories": categories,
            "belief_doubt": belief_doubt,
            "inquiry": inquiry,
            "pragmatic_maxim": pragmatic_maxim,
            "fallibilism": fallibilism,
            "community": community,
            "continuity": continuity
        }

    def _analyze_semiotics(self, text: str) -> Dict[str, Any]:
        """
        Analyze triadic semiotics.

        Triadic relation: Sign (representamen), Object, Interpretant
        Not dyadic (sign-object) but triadic (sign-object-interpretant)
        """
        text_lower = text.lower()

        # Sign indicators
        sign_words = ["sign", "symbol", "represent", "stand for", "indicate"]
        has_sign = sum(1 for phrase in sign_words if phrase in text_lower)

        # Object indicators
        object_words = ["object", "thing", "referent", "refers to"]
        has_object = sum(1 for phrase in object_words if phrase in text_lower)

        # Interpretant indicators
        interpretant_words = ["interpret", "meaning", "understand", "effect"]
        has_interpretant = sum(1 for word in interpretant_words if word in text_lower)

        # Relation indicators
        relation_words = ["relation", "between", "connect", "mediate"]
        has_relation = sum(1 for word in relation_words if word in text_lower)

        # Icon, Index, Symbol classification
        icon_words = ["resemble", "look like", "image", "similar"]
        index_words = ["point to", "indicate", "causal", "smoke"]
        symbol_words = ["convention", "arbitrary", "word", "language"]

        has_icon = sum(1 for phrase in icon_words if phrase in text_lower)
        has_index = sum(1 for phrase in index_words if phrase in text_lower)
        has_symbol = sum(1 for word in symbol_words if word in text_lower)

        sign_type_scores = {
            "Icon": has_icon,
            "Index": has_index,
            "Symbol": has_symbol
        }
        dominant_sign = max(sign_type_scores, key=sign_type_scores.get)

        if has_sign >= 1 and has_interpretant >= 1:
            status = "Triadic Semiosis"
            description = "Sign-Object-Interpretant relation - genuine triadic semiosis"
            structure = "Triadic"
        elif has_sign >= 1 and has_object >= 1:
            status = "Sign-Object Relation"
            description = "Sign standing for object - potential semiosis"
            structure = "Dyadic"
        elif has_sign >= 1:
            status = "Sign Present"
            description = "Sign or representation detected"
            structure = "Monadic"
        else:
            status = "No Clear Semiosis"
            description = "Semiotic relation not evident"
            structure = "None"

        if sign_type_scores[dominant_sign] > 0:
            sign_type = dominant_sign
        else:
            sign_type = "Unclear"

        return {
            "status": status,
            "description": description,
            "structure": structure,
            "sign_type": sign_type,
            "principle": "Triadic semiotics: Sign, Object, Interpretant (irreducible triad)"
        }

    def _determine_inference(self, text: str) -> Dict[str, Any]:
        """
        Determine type of inference: Deduction, Induction, or Abduction.

        Deduction: Necessary inference from rule to case
        Induction: Generalization from cases to rule
        Abduction: Hypothesis formation - best explanation
        """
        text_lower = text.lower()

        # Deduction indicators (must, necessarily, follows)
        deduction_words = ["must", "necessarily", "therefore", "logically", "follows that"]
        has_deduction = sum(1 for phrase in deduction_words if phrase in text_lower)

        # Induction indicators (probably, generally, usually)
        induction_words = ["probably", "generally", "usually", "most", "tend to"]
        has_induction = sum(1 for phrase in induction_words if phrase in text_lower)

        # Abduction indicators (might, could, hypothesis, explain)
        abduction_words = ["might", "could be", "hypothesis", "explain", "suggest", "perhaps"]
        has_abduction = sum(1 for phrase in abduction_words if phrase in text_lower)

        # Best explanation indicators
        best_explanation = ["best explanation", "most likely", "accounts for", "would explain"]
        has_best_explanation = sum(1 for phrase in best_explanation if phrase in text_lower)

        # Surprise/anomaly (triggers abduction)
        surprise_words = ["surprising", "unexpected", "anomaly", "strange", "curious"]
        has_surprise = sum(1 for word in surprise_words if word in text_lower)

        scores = {
            "Deduction": has_deduction,
            "Induction": has_induction,
            "Abduction": has_abduction + has_best_explanation + has_surprise
        }
        dominant = max(scores, key=scores.get)

        if scores[dominant] == 0:
            inference_type = "No Clear Inference"
            description = "Inference type not evident"
            mode = "None"
        elif dominant == "Deduction":
            inference_type = "Deduction"
            description = "Necessary inference from rule to case"
            mode = "Analytic"
        elif dominant == "Induction":
            inference_type = "Induction"
            description = "Generalization from observed cases to general rule"
            mode = "Ampliative"
        else:  # Abduction
            inference_type = "Abduction (Retroduction)"
            description = "Hypothesis formation - inference to best explanation"
            mode = "Creative"

        return {
            "type": inference_type,
            "description": description,
            "mode": mode,
            "scores": scores,
            "principle": "Three types of inference: Deduction (necessary), Induction (probable), Abduction (explanatory)"
        }

    def _assess_categories(self, text: str) -> Dict[str, Any]:
        """
        Assess Peirce's three categories: Firstness, Secondness, Thirdness.

        Firstness: Quality, feeling, possibility, immediacy
        Secondness: Reaction, existence, actuality, brute fact
        Thirdness: Mediation, law, generality, representation
        """
        text_lower = text.lower()

        # Firstness indicators (quality, feeling, possibility)
        firstness_words = ["feeling", "quality", "possibility", "immediate", "fresh", "spontaneous"]
        has_firstness = sum(1 for word in firstness_words if word in text_lower)

        # Secondness indicators (reaction, existence, struggle)
        secondness_words = ["reaction", "exist", "actual", "fact", "struggle", "resist", "force"]
        has_secondness = sum(1 for word in secondness_words if word in text_lower)

        # Thirdness indicators (mediation, law, generality, representation)
        thirdness_words = ["law", "rule", "general", "mediate", "represent", "habit", "pattern"]
        has_thirdness = sum(1 for word in thirdness_words if word in text_lower)

        scores = {
            "Firstness": has_firstness,
            "Secondness": has_secondness,
            "Thirdness": has_thirdness
        }
        dominant = max(scores, key=scores.get)

        if scores[dominant] == 0:
            category = "No Clear Category"
            description = "Phenomenological category not evident"
            character = "None"
        elif dominant == "Firstness":
            category = "Firstness"
            description = "Quality, feeling, possibility - pure immediacy"
            character = "Qualitative"
        elif dominant == "Secondness":
            category = "Secondness"
            description = "Reaction, existence, brute fact - actuality"
            character = "Existential"
        else:  # Thirdness
            category = "Thirdness"
            description = "Mediation, law, generality - representation and continuity"
            character = "Mediating"

        return {
            "dominant": category,
            "description": description,
            "character": character,
            "scores": scores,
            "principle": "Three categories: Firstness (quality), Secondness (reaction), Thirdness (mediation)"
        }

    def _evaluate_belief_doubt(self, text: str) -> Dict[str, Any]:
        """
        Evaluate belief and doubt.

        Belief: Settled habit of action, calm state
        Doubt: Irritation, struggle, unsettled state
        Inquiry: Process from doubt to belief
        """
        text_lower = text.lower()

        # Belief indicators
        belief_words = ["believe", "certain", "confident", "settled", "conviction"]
        has_belief = sum(1 for word in belief_words if word in text_lower)

        # Doubt indicators
        doubt_words = ["doubt", "uncertain", "question", "unsure", "hesitate"]
        has_doubt = sum(1 for word in doubt_words if word in text_lower)

        # Irritation indicators (doubt as irritation)
        irritation_words = ["irritate", "uncomfortable", "uneasy", "disturb"]
        has_irritation = sum(1 for word in irritation_words if word in text_lower)

        # Habit indicators (belief as habit)
        habit_words = ["habit", "routine", "accustomed", "disposed"]
        has_habit = sum(1 for word in habit_words if word in text_lower)

        # Inquiry indicators
        inquiry_words = ["investigate", "inquire", "research", "seek", "explore"]
        has_inquiry = sum(1 for word in inquiry_words if word in text_lower)

        if has_doubt >= 1 and has_inquiry >= 1:
            state = "Active Inquiry"
            description = "Doubt prompting inquiry - seeking to settle belief"
            mode = "Investigating"
        elif has_doubt >= 1 or has_irritation >= 1:
            state = "Doubt"
            description = "Irritation of doubt - unsettled state requiring inquiry"
            mode = "Unsettled"
        elif has_belief >= 1 or has_habit >= 1:
            state = "Belief"
            description = "Settled belief - calm habit of action"
            mode = "Settled"
        else:
            state = "Unclear"
            description = "Belief/doubt status unclear"
            mode = "Indeterminate"

        return {
            "state": state,
            "description": description,
            "mode": mode,
            "principle": "Doubt is irritation that prompts inquiry; belief is settled habit"
        }

    def _assess_inquiry(self, text: str) -> Dict[str, Any]:
        """
        Assess scientific inquiry and method.

        Inquiry: Self-correcting process, community of investigators
        Scientific method: Observation, hypothesis, testing, revision
        """
        text_lower = text.lower()

        # Inquiry/investigation indicators
        inquiry_words = ["inquire", "investigate", "research", "study", "examine"]
        has_inquiry = sum(1 for word in inquiry_words if word in text_lower)

        # Scientific method indicators
        method_words = ["method", "systematic", "test", "experiment", "observe"]
        has_method = sum(1 for word in method_words if word in text_lower)

        # Hypothesis indicators
        hypothesis_words = ["hypothesis", "theory", "conjecture", "propose"]
        has_hypothesis = sum(1 for word in hypothesis_words if word in text_lower)

        # Self-correction indicators
        correction_words = ["correct", "revise", "improve", "refine", "adjust"]
        has_correction = sum(1 for word in correction_words if word in text_lower)

        # Observation indicators
        observation_words = ["observe", "data", "evidence", "fact", "experience"]
        has_observation = sum(1 for word in observation_words if word in text_lower)

        if has_inquiry >= 1 and has_method >= 1:
            status = "Scientific Inquiry"
            description = "Systematic investigation using scientific method"
            approach = "Methodical"
        elif has_hypothesis >= 1 and has_observation >= 1:
            status = "Hypothesis Testing"
            description = "Forming and testing hypotheses against observations"
            approach = "Empirical"
        elif has_correction >= 1:
            status = "Self-Correcting Process"
            description = "Revising and improving through inquiry"
            approach = "Progressive"
        elif has_inquiry >= 1:
            status = "Inquiry Present"
            description = "Investigation or research indicated"
            approach = "Investigative"
        else:
            status = "No Inquiry Evident"
            description = "Inquiry not clearly present"
            approach = "None"

        return {
            "status": status,
            "description": description,
            "approach": approach,
            "principle": "Inquiry is self-correcting process of the community of investigators"
        }

    def _apply_pragmatic_maxim(self, text: str) -> Dict[str, Any]:
        """
        Apply the pragmatic maxim.

        Pragmatic maxim: Consider practical effects to clarify meaning
        Truth is practical consequences, not abstract correspondence
        """
        text_lower = text.lower()

        # Practical/practice indicators
        practical_words = ["practical", "practice", "use", "application", "effect"]
        has_practical = sum(1 for word in practical_words if word in text_lower)

        # Consequence indicators
        consequence_words = ["consequence", "result", "outcome", "impact", "what happens"]
        has_consequence = sum(1 for phrase in consequence_words if phrase in text_lower)

        # Meaning/conception indicators
        meaning_words = ["meaning", "concept", "idea", "understand"]
        has_meaning = sum(1 for word in meaning_words if word in text_lower)

        # Abstract/theoretical (not pragmatic)
        abstract_words = ["abstract", "theoretical", "pure", "ideal"]
        has_abstract = sum(1 for word in abstract_words if word in text_lower)

        # Action/conduct indicators
        action_words = ["action", "do", "conduct", "behavior", "act"]
        has_action = sum(1 for word in action_words if word in text_lower)

        if has_practical >= 1 and has_consequence >= 1:
            application = "Pragmatic Maxim Applied"
            description = "Considering practical consequences to clarify meaning"
            mode = "Pragmatic"
        elif has_meaning >= 1 and has_action >= 1:
            application = "Meaning as Use"
            description = "Meaning tied to action and conduct"
            mode = "Operational"
        elif has_abstract >= 1 and has_practical == 0:
            application = "Abstract Conception"
            description = "Abstract thinking without practical grounding"
            mode = "Non-pragmatic"
        elif has_practical >= 1:
            application = "Practical Focus"
            description = "Emphasis on practical aspects"
            mode = "Applied"
        else:
            application = "Unclear"
            description = "Pragmatic maxim application unclear"
            mode = "Indeterminate"

        return {
            "application": application,
            "description": description,
            "mode": mode,
            "principle": "Pragmatic maxim: Consider practical effects to clarify ideas"
        }

    def _check_fallibilism(self, text: str) -> Dict[str, Any]:
        """
        Check fallibilism - all knowledge is provisional.

        Fallibilism: We can be wrong, knowledge is corrigible
        Anti-foundationalism: No absolute certainty
        """
        text_lower = text.lower()

        # Fallibilism indicators
        fallible_words = ["might be wrong", "could be mistaken", "provisional", "corrigible"]
        has_fallible = sum(1 for phrase in fallible_words if phrase in text_lower)

        # Uncertainty/possibility of error
        uncertain_words = ["uncertain", "may not be", "possibly wrong", "subject to revision"]
        has_uncertain = sum(1 for phrase in uncertain_words if phrase in text_lower)

        # Absolute certainty (opposite of fallibilism)
        certain_words = ["absolutely certain", "infallible", "cannot be wrong", "indubitable"]
        has_certain = sum(1 for phrase in certain_words if phrase in text_lower)

        # Revision/correction indicators
        revision_words = ["revise", "correct", "update", "improve"]
        has_revision = sum(1 for word in revision_words if word in text_lower)

        if has_fallible >= 1 or (has_uncertain >= 1 and has_revision >= 1):
            stance = "Fallibilist"
            description = "Acknowledging possibility of error - knowledge is corrigible"
            attitude = "Humble"
        elif has_revision >= 1:
            stance = "Open to Revision"
            description = "Willing to revise and correct"
            attitude = "Self-correcting"
        elif has_certain >= 1:
            stance = "Infallibilist"
            description = "Claiming absolute certainty - anti-Peircean"
            attitude = "Dogmatic"
        else:
            stance = "Unclear"
            description = "Fallibilism stance unclear"
            attitude = "Indeterminate"

        return {
            "stance": stance,
            "description": description,
            "attitude": attitude,
            "principle": "Fallibilism: All knowledge is provisional and corrigible"
        }

    def _assess_community(self, text: str) -> Dict[str, Any]:
        """
        Assess community of inquiry.

        Community: Truth emerges from community of investigators
        Not individual but collective process
        Ultimate agreement of investigators
        """
        text_lower = text.lower()

        # Community indicators
        community_words = ["community", "we", "together", "collective", "shared"]
        has_community = sum(1 for word in community_words if word in text_lower)

        # Agreement/consensus indicators
        agreement_words = ["agree", "consensus", "converge", "settle on"]
        has_agreement = sum(1 for phrase in agreement_words if phrase in text_lower)

        # Investigators/scientists indicators
        investigators_words = ["investigators", "researchers", "scientists", "scholars"]
        has_investigators = sum(1 for word in investigators_words if word in text_lower)

        # Individual/solitary (opposite)
        individual_words = ["alone", "by myself", "individually", "solitary"]
        has_individual = sum(1 for word in individual_words if word in text_lower)

        # Long run/ultimate indicators
        ultimate_words = ["ultimate", "long run", "eventually", "in the end"]
        has_ultimate = sum(1 for phrase in ultimate_words if phrase in text_lower)

        if has_community >= 1 and has_agreement >= 1:
            status = "Community of Inquiry"
            description = "Truth as ultimate agreement of community of investigators"
            nature = "Collective"
        elif has_investigators >= 1 or (has_community >= 1 and has_ultimate >= 1):
            status = "Collaborative Inquiry"
            description = "Collective investigation and inquiry"
            nature = "Social"
        elif has_individual >= 1:
            status = "Individual Inquiry"
            description = "Solitary investigation - not fully Peircean"
            nature = "Isolated"
        else:
            status = "Unclear"
            description = "Community aspect unclear"
            nature = "Indeterminate"

        return {
            "status": status,
            "description": description,
            "nature": nature,
            "principle": "Truth is ultimate agreement of the community of investigators"
        }

    def _detect_continuity(self, text: str) -> Dict[str, Any]:
        """
        Detect continuity (synechism).

        Synechism: Doctrine of continuity - no absolute breaks
        Continuity in nature, thought, and evolution
        """
        text_lower = text.lower()

        # Continuity indicators
        continuity_words = ["continuity", "continuous", "gradual", "flow", "connect"]
        has_continuity = sum(1 for word in continuity_words if word in text_lower)

        # Evolution/growth indicators
        evolution_words = ["evolve", "develop", "grow", "emerge", "process"]
        has_evolution = sum(1 for word in evolution_words if word in text_lower)

        # Connection/mediation indicators
        connection_words = ["connection", "relation", "mediate", "bridge", "link"]
        has_connection = sum(1 for word in connection_words if word in text_lower)

        # Absolute break/discontinuity (opposite)
        break_words = ["absolute break", "discontinuous", "gap", "separate", "isolated"]
        has_break = sum(1 for phrase in break_words if phrase in text_lower)

        if has_continuity >= 1 or (has_evolution >= 1 and has_connection >= 1):
            presence = "Synechism (Continuity)"
            description = "Doctrine of continuity - no absolute breaks in nature"
            character = "Continuous"
        elif has_evolution >= 1:
            presence = "Evolutionary Process"
            description = "Gradual development and evolution"
            character = "Progressive"
        elif has_break >= 1:
            presence = "Discontinuity"
            description = "Emphasis on breaks and gaps"
            character = "Discrete"
        else:
            presence = "Unclear"
            description = "Continuity unclear"
            character = "Indeterminate"

        return {
            "presence": presence,
            "description": description,
            "character": character,
            "principle": "Synechism: Doctrine of continuity - no absolute discontinuities"
        }

    def _construct_reasoning(
        self,
        semiotics: Dict[str, Any],
        inference: Dict[str, Any],
        belief_doubt: Dict[str, Any],
        pragmatic_maxim: Dict[str, Any]
    ) -> str:
        """Construct Peircean pragmatic reasoning."""
        reasoning = (
            f"From Peirce's pragmatic perspective, semiotics: {semiotics['description']}. "
            f"Inference: {inference['description']}. "
            f"Belief/Doubt: {belief_doubt['description']}. "
            f"Pragmatic maxim: {pragmatic_maxim['description']}. "
        )

        # Conclude with Peircean principles
        reasoning += (
            "Truth is the ultimate agreement of the community of investigators. "
            "All knowledge is fallible and provisional. "
            "Consider the practical consequences to clarify ideas. "
            "Inquiry moves from doubt to settled belief through self-correcting investigation."
        )

        return reasoning
