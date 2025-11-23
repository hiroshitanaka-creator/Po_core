"""
John Dewey - American Pragmatist Philosopher

John Dewey (1859-1952)
Focus: Pragmatism, Experience, Inquiry, Democracy, Education

Key Concepts:
- Experience: Continuous interaction between organism and environment
- Inquiry: Transformation of indeterminate situation into determinate one
- Instrumentalism: Thinking as tool for problem-solving
- Growth: Education's purpose is growth itself, not external goals
- Democracy: Not just government, but a way of life
- Reflective Thinking: Learning from experience through reflection
- Habit: Intelligent habits vs. routine habits
- Reconstruction: Continuous reconstruction of experience
- Continuity and Interaction: Two principles of experience
- Occupations: Learning by doing, hands-on engagement
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Dewey(Philosopher):
    """
    John Dewey's pragmatist philosophy.

    Analyzes prompts through the lens of experience, inquiry,
    instrumentalism, and democratic growth.
    """

    def __init__(self) -> None:
        super().__init__(
            name="John Dewey",
            description="American pragmatist focused on experience, inquiry, democracy, and education"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Dewey's pragmatist perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Dewey's pragmatist analysis
        """
        # Perform Deweyan analysis
        analysis = self._analyze_experience(prompt)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Pragmatism / Experimentalism",
            "experience_quality": analysis["experience"],
            "inquiry_stage": analysis["inquiry"],
            "growth_potential": analysis["growth"],
            "democratic_quality": analysis["democracy"],
            "reflective_thinking": analysis["reflection"],
            "habit_formation": analysis["habit"],
            "instrumentalism": analysis["instrumentalism"],
            "continuity_interaction": analysis["continuity_interaction"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Pragmatism and experimentalism",
                "focus": "Experience, inquiry, and democratic growth"
            }
        }

    def _analyze_experience(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Deweyan experiential analysis.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess experience quality
        experience = self._assess_experience(prompt)

        # Evaluate inquiry stage
        inquiry = self._evaluate_inquiry(prompt)

        # Assess growth potential
        growth = self._assess_growth(prompt)

        # Evaluate democratic quality
        democracy = self._evaluate_democracy(prompt)

        # Check reflective thinking
        reflection = self._check_reflective_thinking(prompt)

        # Assess habit formation
        habit = self._assess_habit_formation(prompt)

        # Evaluate instrumentalism
        instrumentalism = self._evaluate_instrumentalism(prompt)

        # Check continuity and interaction
        continuity_interaction = self._check_continuity_interaction(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            experience, inquiry, growth, democracy, reflection
        )

        return {
            "reasoning": reasoning,
            "experience": experience,
            "inquiry": inquiry,
            "growth": growth,
            "democracy": democracy,
            "reflection": reflection,
            "habit": habit,
            "instrumentalism": instrumentalism,
            "continuity_interaction": continuity_interaction
        }

    def _assess_experience(self, text: str) -> Dict[str, Any]:
        """
        Assess the quality of experience.

        Experience = transaction between organism and environment
        Not passive reception, but active doing and undergoing
        """
        text_lower = text.lower()

        # Active engagement indicators
        active_words = ["do", "act", "engage", "participate", "interact", "work", "practice"]
        has_active = sum(1 for word in active_words if word in text_lower)

        # Passive reception indicators
        passive_words = ["receive", "given", "told", "taught", "watch", "observe"]
        has_passive = sum(1 for word in passive_words if word in text_lower)

        # Doing and undergoing (active + receptive)
        undergoing_words = ["feel", "experience", "undergo", "sense", "encounter"]
        has_undergoing = sum(1 for word in undergoing_words if word in text_lower)

        # Environment/situation interaction
        environment_words = ["situation", "environment", "context", "world", "surroundings"]
        has_environment = sum(1 for word in environment_words if word in text_lower)

        # Determine experience quality
        if has_active >= 2 and has_undergoing >= 1:
            quality = "Rich Experience"
            description = "Active doing combined with undergoing - genuine educative experience"
            type_exp = "Educative"
        elif has_active > has_passive:
            quality = "Active Experience"
            description = "Emphasis on doing - potentially educative if reflection follows"
            type_exp = "Potentially educative"
        elif has_passive >= 2:
            quality = "Passive Reception"
            description = "Mere reception without active engagement - mis-educative"
            type_exp = "Mis-educative"
        else:
            quality = "Indeterminate Experience"
            description = "Quality of experience unclear"
            type_exp = "Unclear"

        return {
            "quality": quality,
            "description": description,
            "type": type_exp,
            "principle": "Experience is not mere sensation but interaction with environment"
        }

    def _evaluate_inquiry(self, text: str) -> Dict[str, Any]:
        """
        Evaluate the stage of inquiry.

        Inquiry = transformation of indeterminate situation into determinate one
        5 stages: Problem, intellectualization, hypothesis, reasoning, testing
        """
        text_lower = text.lower()

        # Stage 1: Felt difficulty / problem
        problem_words = ["problem", "difficulty", "challenge", "issue", "question", "unclear"]
        has_problem = any(word in text_lower for word in problem_words)

        # Stage 2: Intellectualization - defining the problem
        define_words = ["what is", "define", "clarify", "understand", "analyze"]
        has_definition = any(word in text_lower for word in define_words)

        # Stage 3: Hypothesis - suggesting solution
        hypothesis_words = ["if", "maybe", "perhaps", "could", "might", "suppose", "hypothesis"]
        has_hypothesis = any(word in text_lower for word in hypothesis_words)

        # Stage 4: Reasoning - developing implications
        reasoning_words = ["therefore", "because", "since", "implies", "leads to", "follows"]
        has_reasoning = any(word in text_lower for word in reasoning_words)

        # Stage 5: Testing - experimental verification
        testing_words = ["test", "try", "experiment", "verify", "check", "see if", "find out"]
        has_testing = any(word in text_lower for word in testing_words)

        # Determine inquiry stage
        stages_present = []
        if has_problem:
            stages_present.append("Problem recognition")
        if has_definition:
            stages_present.append("Problem definition")
        if has_hypothesis:
            stages_present.append("Hypothesis formation")
        if has_reasoning:
            stages_present.append("Reasoning")
        if has_testing:
            stages_present.append("Experimental testing")

        if len(stages_present) >= 4:
            stage = "Complete Inquiry"
            description = "Full inquiry cycle - problem to solution through experimentation"
            status = "Scientific"
        elif has_testing:
            stage = "Experimental Phase"
            description = "Testing hypotheses - experimental method in action"
            status = "Pragmatic"
        elif has_hypothesis or has_reasoning:
            stage = "Intellectual Phase"
            description = "Forming and reasoning about possibilities"
            status = "Developing"
        elif has_problem:
            stage = "Problem Recognition"
            description = "Awareness of problematic situation - inquiry beginning"
            status = "Initial"
        else:
            stage = "No Clear Inquiry"
            description = "Inquiry process not evident"
            status = "Absent"

        return {
            "stage": stage,
            "description": description,
            "status": status,
            "stages_present": stages_present if stages_present else ["None"],
            "principle": "Inquiry transforms indeterminate situations into determinate ones"
        }

    def _assess_growth(self, text: str) -> Dict[str, Any]:
        """
        Assess growth potential.

        Growth = reorganization and reconstruction of experience
        Education's purpose is not external goals but growth itself
        """
        text_lower = text.lower()

        # Growth indicators
        growth_words = ["grow", "develop", "learn", "improve", "progress", "advance", "evolve"]
        has_growth = sum(1 for word in growth_words if word in text_lower)

        # Reconstruction indicators
        reconstruction_words = ["change", "transform", "reconstruct", "reorganize", "adapt", "modify"]
        has_reconstruction = sum(1 for word in reconstruction_words if word in text_lower)

        # Future-oriented indicators
        future_words = ["will", "future", "next", "continue", "ongoing", "more"]
        has_future = sum(1 for word in future_words if word in text_lower)

        # Static/fixed indicators (opposed to growth)
        static_words = ["fixed", "final", "complete", "finished", "unchanging", "permanent"]
        has_static = sum(1 for word in static_words if word in text_lower)

        # Calculate growth potential
        total_growth = has_growth + has_reconstruction + has_future

        if total_growth >= 3 and has_static == 0:
            potential = "High Growth Potential"
            description = "Strong emphasis on continuous growth and reconstruction"
            orientation = "Growth-oriented"
        elif total_growth >= 1 and has_static == 0:
            potential = "Moderate Growth Potential"
            description = "Some growth orientation present"
            orientation = "Developing"
        elif has_static >= 2:
            potential = "Low Growth Potential"
            description = "Static or fixed mindset - opposed to Deweyan growth"
            orientation = "Fixed"
        else:
            potential = "Unclear Growth Potential"
            description = "Growth orientation not clear"
            orientation = "Indeterminate"

        return {
            "potential": potential,
            "description": description,
            "orientation": orientation,
            "principle": "Education is growth; growth is life - there is no goal beyond growth itself"
        }

    def _evaluate_democracy(self, text: str) -> Dict[str, Any]:
        """
        Evaluate democratic quality.

        Democracy = not just government form, but a way of associated living
        Shared experience, free communication, mutual respect
        """
        text_lower = text.lower()

        # Democratic participation indicators
        participation_words = ["participate", "together", "share", "collaborate", "contribute", "engage"]
        has_participation = sum(1 for word in participation_words if word in text_lower)

        # Communication/dialogue indicators
        communication_words = ["communicate", "discuss", "dialogue", "talk", "exchange", "share ideas"]
        has_communication = sum(1 for word in communication_words if word in text_lower)

        # Mutual respect/equality indicators
        equality_words = ["equal", "respect", "mutual", "reciprocal", "fair", "everyone"]
        has_equality = sum(1 for word in equality_words if word in text_lower)

        # Common good indicators
        common_words = ["common", "shared", "collective", "community", "social", "public"]
        has_common = sum(1 for word in common_words if word in text_lower)

        # Authoritarian indicators (opposed to democracy)
        authoritarian_words = ["command", "obey", "dictate", "impose", "force", "authority"]
        has_authoritarian = sum(1 for word in authoritarian_words if word in text_lower)

        # Calculate democratic quality
        total_democratic = has_participation + has_communication + has_equality + has_common

        if total_democratic >= 3 and has_authoritarian == 0:
            quality = "Highly Democratic"
            description = "Strong democratic qualities - shared experience and communication"
            mode = "Democratic way of life"
        elif total_democratic >= 1 and has_authoritarian == 0:
            quality = "Moderately Democratic"
            description = "Some democratic elements present"
            mode = "Developing democracy"
        elif has_authoritarian >= 2:
            quality = "Authoritarian"
            description = "Authoritarian tendencies - opposed to democratic life"
            mode = "Non-democratic"
        else:
            quality = "Unclear Democratic Quality"
            description = "Democratic quality indeterminate"
            mode = "Neutral"

        return {
            "quality": quality,
            "description": description,
            "mode": mode,
            "principle": "Democracy is a way of life, not merely a form of government"
        }

    def _check_reflective_thinking(self, text: str) -> Dict[str, Any]:
        """
        Check the presence of reflective thinking.

        Reflective thinking = active, persistent, careful consideration
        Turning experience into learning through reflection
        """
        text_lower = text.lower()

        # Reflection indicators
        reflection_words = ["reflect", "think about", "consider", "ponder", "contemplate", "examine"]
        has_reflection = sum(1 for word in reflection_words if word in text_lower)

        # Careful consideration indicators
        careful_words = ["careful", "thorough", "systematic", "deliberate", "thoughtful"]
        has_careful = sum(1 for word in careful_words if word in text_lower)

        # Evidence/grounds indicators
        evidence_words = ["because", "evidence", "reason", "grounds", "basis", "support"]
        has_evidence = sum(1 for word in evidence_words if word in text_lower)

        # Learning from experience
        learning_words = ["learn", "lesson", "insight", "understand", "realize", "discover"]
        has_learning = sum(1 for word in learning_words if word in text_lower)

        # Impulsive/unreflective indicators
        impulsive_words = ["immediately", "without thinking", "impulse", "reaction", "automatic"]
        has_impulsive = sum(1 for word in impulsive_words if word in text_lower)

        total_reflective = has_reflection + has_careful + has_evidence + has_learning

        if total_reflective >= 3 and has_impulsive == 0:
            level = "High Reflective Thinking"
            description = "Strong reflective thinking - learning from experience"
            type_thinking = "Reflective"
        elif total_reflective >= 1 and has_impulsive == 0:
            level = "Moderate Reflective Thinking"
            description = "Some reflection present"
            type_thinking = "Partially reflective"
        elif has_impulsive >= 1:
            level = "Unreflective"
            description = "Impulsive or automatic - lacking reflection"
            type_thinking = "Unreflective"
        else:
            level = "Unclear"
            description = "Reflective thinking not clear"
            type_thinking = "Indeterminate"

        return {
            "level": level,
            "description": description,
            "type": type_thinking,
            "principle": "We learn from experience only when we reflect upon it"
        }

    def _assess_habit_formation(self, text: str) -> Dict[str, Any]:
        """
        Assess habit formation.

        Habits = acquired predispositions to act
        Intelligent habits vs. routine habits
        Flexibility vs. rigidity
        """
        text_lower = text.lower()

        # Habit indicators
        habit_words = ["habit", "custom", "routine", "regular", "always", "usually", "practice"]
        has_habit = sum(1 for word in habit_words if word in text_lower)

        # Intelligent habit indicators (flexible, adaptive)
        intelligent_words = ["adapt", "flexible", "adjust", "modify", "responsive", "thoughtful"]
        has_intelligent = sum(1 for word in intelligent_words if word in text_lower)

        # Routine habit indicators (rigid, automatic)
        routine_words = ["automatic", "mechanical", "rigid", "fixed", "unchanging", "rote"]
        has_routine = sum(1 for word in routine_words if word in text_lower)

        if has_intelligent >= 1 and has_habit >= 1:
            formation = "Intelligent Habits"
            description = "Flexible, adaptive habits - intelligent adjustment to situations"
            quality = "Intelligent"
        elif has_routine >= 1 and has_habit >= 1:
            formation = "Routine Habits"
            description = "Rigid, mechanical habits - lack of adaptation"
            quality = "Routine/Rigid"
        elif has_habit >= 1:
            formation = "Habits Present"
            description = "Habits mentioned but quality unclear"
            quality = "Unclear"
        else:
            formation = "No Clear Habits"
            description = "Habit formation not evident"
            quality = "Absent"

        return {
            "formation": formation,
            "description": description,
            "quality": quality,
            "principle": "Habits are tools, not chains - they should be intelligent and flexible"
        }

    def _evaluate_instrumentalism(self, text: str) -> Dict[str, Any]:
        """
        Evaluate instrumentalist thinking.

        Instrumentalism = ideas and concepts are tools/instruments for problem-solving
        Truth = what works in practice
        Knowledge is for use, not contemplation alone
        """
        text_lower = text.lower()

        # Tool/instrument indicators
        tool_words = ["tool", "use", "useful", "practical", "apply", "instrument", "means"]
        has_tool = sum(1 for word in tool_words if word in text_lower)

        # Problem-solving indicators
        problem_solving = ["solve", "solution", "fix", "resolve", "address", "deal with"]
        has_problem_solving = sum(1 for word in problem_solving if word in text_lower)

        # Pragmatic/consequences indicators
        pragmatic_words = ["works", "effective", "consequence", "result", "outcome", "success"]
        has_pragmatic = sum(1 for word in pragmatic_words if word in text_lower)

        # Abstract/contemplative indicators (opposed to instrumentalism)
        abstract_words = ["abstract", "theoretical", "contemplation", "pure thought", "speculation"]
        has_abstract = sum(1 for word in abstract_words if word in text_lower)

        total_instrumental = has_tool + has_problem_solving + has_pragmatic

        if total_instrumental >= 3 and has_abstract == 0:
            level = "Strong Instrumentalism"
            description = "Clear instrumental/pragmatic orientation - ideas as tools"
            orientation = "Pragmatic"
        elif total_instrumental >= 1 and has_abstract == 0:
            level = "Moderate Instrumentalism"
            description = "Some pragmatic/instrumental thinking"
            orientation = "Practical"
        elif has_abstract >= 2:
            level = "Non-Instrumental"
            description = "Abstract/contemplative - opposed to instrumentalism"
            orientation = "Theoretical"
        else:
            level = "Unclear"
            description = "Instrumental orientation unclear"
            orientation = "Indeterminate"

        return {
            "level": level,
            "description": description,
            "orientation": orientation,
            "principle": "Ideas are instruments for solving problems, not mirrors of reality"
        }

    def _check_continuity_interaction(self, text: str) -> Dict[str, Any]:
        """
        Check continuity and interaction - two principles of experience.

        Continuity = every experience affects future experiences
        Interaction = experience is transaction between person and environment
        """
        text_lower = text.lower()

        # Continuity indicators
        continuity_words = ["past", "future", "continue", "build on", "connect", "lead to", "next"]
        has_continuity = sum(1 for word in continuity_words if word in text_lower)

        # Interaction indicators
        interaction_words = ["interact", "transaction", "between", "with", "engage", "environment"]
        has_interaction = sum(1 for word in interaction_words if word in text_lower)

        if has_continuity >= 2 and has_interaction >= 1:
            quality = "Both Principles Present"
            description = "Experience shows both continuity and interaction"
        elif has_continuity >= 1:
            quality = "Continuity Emphasized"
            description = "Temporal connection of experiences evident"
        elif has_interaction >= 1:
            quality = "Interaction Emphasized"
            description = "Transaction with environment evident"
        else:
            quality = "Principles Not Clear"
            description = "Neither continuity nor interaction clearly evident"

        return {
            "quality": quality,
            "description": description,
            "principle": "Experience has continuity (temporal) and interaction (situational)"
        }

    def _construct_reasoning(
        self,
        experience: Dict[str, Any],
        inquiry: Dict[str, Any],
        growth: Dict[str, Any],
        democracy: Dict[str, Any],
        reflection: Dict[str, Any]
    ) -> str:
        """Construct Deweyan pragmatist reasoning."""
        reasoning = (
            f"From a Deweyan pragmatist perspective, the quality of experience here is: {experience['description']}. "
            f"Regarding inquiry: {inquiry['description']}. "
            f"Growth potential: {growth['description']}. "
        )

        # Add democratic quality
        reasoning += f"Democratic quality: {democracy['description']}. "

        # Add reflective thinking
        reasoning += f"Reflective thinking: {reflection['description']}. "

        # Conclude with Deweyan principle
        reasoning += (
            "Remember: education is not preparation for life; education is life itself. "
            "We learn by doing, and we grow through the continuous reconstruction of experience."
        )

        return reasoning
