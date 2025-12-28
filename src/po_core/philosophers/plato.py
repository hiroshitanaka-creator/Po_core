"""
Plato - Ancient Greek Philosopher

Plato (Πλάτων, 428-348 BCE)
Focus: Theory of Forms, Cave Allegory, Divided Line, Tripartite Soul, Justice

Key Concepts:
- Theory of Forms (εἶδος/eidos): Eternal, perfect, unchanging archetypes beyond the material
- Cave Allegory: Liberation from illusion (shadows) to truth (Forms)
- Divided Line: Hierarchy of knowledge - images → beliefs → mathematical → dialectic
- Tripartite Soul: Reason (λογιστικόν), Spirit (θυμοειδές), Appetite (ἐπιθυμητικόν)
- Philosopher-King: Only the wise should rule - those who know the Good
- Anamnesis (ἀνάμνησις): Knowledge as recollection of eternal Forms
- Beauty and Eros (ἔρως): Ascending ladder from physical to eternal Beauty
- Justice (δικαιοσύνη): Harmony of soul's parts, each doing its proper work
- Dialectic (διαλεκτική): Method of philosophical inquiry through dialogue
- The Good (τὸ ἀγαθόν): The Form of the Good - highest reality, source of truth and being
"""

from typing import Any, Dict, List, Optional

from po_core.philosophers.base import Philosopher


class Plato(Philosopher):
    """
    Plato's philosophy of Forms, justice, and the ascent to truth.

    Analyzes prompts through the lens of eternal Forms, the divided line,
    the tripartite soul, and the Form of the Good.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Plato (Πλάτων)",
            description="Ancient Greek philosopher focused on Forms, justice, and the ascent from illusion to truth"
        )

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the prompt from Plato's perspective.

        Args:
            prompt: The input text to analyze
            context: Optional context for the analysis

        Returns:
            Dictionary containing Plato's metaphysical and ethical analysis
        """
        # Perform Platonic analysis
        analysis = self._analyze_forms(prompt)

        # Calculate tension
        tension = self._calculate_tension(analysis)

        return {
            "reasoning": analysis["reasoning"],
            "perspective": "Theory of Forms / Platonic Idealism",
            "tension": tension,
            "forms": analysis["forms"],
            "cave_position": analysis["cave"],
            "divided_line": analysis["divided_line"],
            "soul_harmony": analysis["soul"],
            "governance": analysis["governance"],
            "recollection": analysis["recollection"],
            "eros_ascent": analysis["eros"],
            "justice": analysis["justice"],
            "dialectic": analysis["dialectic"],
            "the_good": analysis["good"],
            "metadata": {
                "philosopher": self.name,
                "approach": "Ascent from shadows to Forms, from opinion to knowledge",
                "focus": "The Good, eternal Forms, and harmony of the soul"
            }
        }

    def _analyze_forms(self, prompt: str) -> Dict[str, Any]:
        """
        Perform Platonic analysis through Theory of Forms.

        Args:
            prompt: The text to analyze

        Returns:
            Analysis results
        """
        # Assess Forms
        forms = self._assess_forms(prompt)

        # Evaluate cave position
        cave = self._evaluate_cave_position(prompt)

        # Analyze divided line
        divided_line = self._analyze_divided_line(prompt)

        # Assess tripartite soul
        soul = self._assess_tripartite_soul(prompt)

        # Evaluate governance
        governance = self._evaluate_governance(prompt)

        # Check recollection (anamnesis)
        recollection = self._check_recollection(prompt)

        # Assess eros and beauty
        eros = self._assess_eros_ascent(prompt)

        # Evaluate justice
        justice = self._evaluate_justice(prompt)

        # Assess dialectic
        dialectic = self._assess_dialectic(prompt)

        # Contemplate the Good
        good = self._contemplate_the_good(prompt)

        # Construct reasoning
        reasoning = self._construct_reasoning(
            forms, cave, divided_line, soul, justice, good
        )

        return {
            "reasoning": reasoning,
            "forms": forms,
            "cave": cave,
            "divided_line": divided_line,
            "soul": soul,
            "governance": governance,
            "recollection": recollection,
            "eros": eros,
            "justice": justice,
            "dialectic": dialectic,
            "good": good
        }

    def _assess_forms(self, text: str) -> Dict[str, Any]:
        """
        Assess the Theory of Forms (εἶδος/eidos).

        Forms are eternal, perfect, unchanging archetypes.
        Material world is mere shadow/imitation of Forms.
        """
        text_lower = text.lower()
        forms_identified = []

        # The Form of Beauty (τὸ καλόν)
        beauty_words = ["beauty", "beautiful", "aesthetic", "elegance"]
        if any(word in text_lower for word in beauty_words):
            forms_identified.append({
                "form": "Beauty (τὸ καλόν)",
                "description": "The eternal Form of Beauty itself, not merely beautiful things"
            })

        # The Form of Justice (δικαιοσύνη)
        justice_words = ["justice", "just", "fair", "right"]
        if any(word in text_lower for word in justice_words):
            forms_identified.append({
                "form": "Justice (δικαιοσύνη)",
                "description": "The eternal Form of Justice, of which just acts are mere copies"
            })

        # The Form of Truth (ἀλήθεια)
        truth_words = ["truth", "true", "reality", "real"]
        if any(word in text_lower for word in truth_words):
            forms_identified.append({
                "form": "Truth (ἀλήθεια)",
                "description": "The eternal Form of Truth, beyond mere opinion"
            })

        # The Form of Courage (ἀνδρεία)
        courage_words = ["courage", "brave", "courageous"]
        if any(word in text_lower for word in courage_words):
            forms_identified.append({
                "form": "Courage (ἀνδρεία)",
                "description": "The eternal Form of Courage itself"
            })

        # The Form of Wisdom (σοφία)
        wisdom_words = ["wisdom", "wise", "knowledge", "understanding"]
        if any(word in text_lower for word in wisdom_words):
            forms_identified.append({
                "form": "Wisdom (σοφία)",
                "description": "The eternal Form of Wisdom - knowledge of the Forms"
            })

        # The Form of Love (ἔρως)
        love_words = ["love", "desire", "longing", "eros"]
        if any(word in text_lower for word in love_words):
            forms_identified.append({
                "form": "Love/Eros (ἔρως)",
                "description": "The eternal Form of Love - yearning for the eternal"
            })

        # Check for awareness of Form vs particular
        form_awareness = ["ideal", "perfect", "eternal", "unchanging", "essence", "form itself"]
        has_form_awareness = any(phrase in text_lower for phrase in form_awareness)

        # Check for material/particular awareness
        particular_words = ["physical", "material", "particular", "example", "instance"]
        has_particular = any(word in text_lower for word in particular_words)

        if not forms_identified:
            forms_identified.append({
                "form": "No specific Form detected",
                "description": "The text may concern the material realm of becoming"
            })

        return {
            "forms": forms_identified,
            "count": len([f for f in forms_identified if "No specific" not in f["form"]]),
            "primary": forms_identified[0]["form"],
            "form_awareness": "Aware of Forms" if has_form_awareness else "Focuses on particulars",
            "note": "Forms are eternal, perfect archetypes - material things are mere shadows"
        }

    def _evaluate_cave_position(self, text: str) -> Dict[str, Any]:
        """
        Evaluate position in the Cave Allegory.

        Stages: Shadows → Chains → Liberation → Ascent → Sun → Return
        Movement from illusion to truth
        """
        text_lower = text.lower()

        # Shadow stage - complete illusion
        shadow_words = ["illusion", "appearance", "seems", "looks like", "shadow"]
        has_shadow = sum(1 for word in shadow_words if word in text_lower)

        # Chains/bondage - trapped in opinion
        chain_words = ["trapped", "bound", "cannot see", "limited", "constrained"]
        has_chains = sum(1 for word in chain_words if word in text_lower)

        # Liberation - breaking free
        liberate_words = ["free", "liberate", "break free", "escape", "release"]
        has_liberation = sum(1 for phrase in liberate_words if phrase in text_lower)

        # Ascent - rising toward truth
        ascent_words = ["ascend", "rise", "climb", "upward", "higher"]
        has_ascent = sum(1 for word in ascent_words if word in text_lower)

        # Sun/light - truth and the Good
        light_words = ["light", "sun", "illuminate", "clarity", "truth"]
        has_light = sum(1 for word in light_words if word in text_lower)

        # Return - educating others
        return_words = ["teach", "educate", "show others", "return", "help"]
        has_return = sum(1 for word in return_words if word in text_lower)

        # Determine position
        if has_light >= 2 and has_return >= 1:
            position = "Philosopher Returned"
            description = "Has seen the sun (Good) and returns to educate the prisoners"
            stage = "Highest - Philosopher-educator"
        elif has_light >= 2 or has_ascent >= 2:
            position = "In the Light"
            description = "Ascended to truth - contemplating the Forms and the Good"
            stage = "Liberation achieved"
        elif has_liberation >= 1 and has_ascent >= 1:
            position = "Ascending"
            description = "Liberated and rising toward the light - painful but progressive"
            stage = "On the path"
        elif has_liberation >= 1:
            position = "Newly Liberated"
            description = "Chains broken but eyes not yet adjusted to light"
            stage = "Initial freedom"
        elif has_chains >= 1 or has_shadow >= 2:
            position = "In Chains"
            description = "Trapped in the cave, watching shadows, mistaking them for reality"
            stage = "Imprisoned in illusion"
        else:
            position = "Unclear Position"
            description = "Cave position indeterminate"
            stage = "Unknown"

        return {
            "position": position,
            "description": description,
            "stage": stage,
            "principle": "The unexamined life is not worth living - we must ascend from shadows to truth"
        }

    def _analyze_divided_line(self, text: str) -> Dict[str, Any]:
        """
        Analyze the Divided Line - hierarchy of knowledge.

        Four levels:
        1. Eikasia (εἰκασία) - Images/shadows - lowest
        2. Pistis (πίστις) - Belief in physical objects
        3. Dianoia (διάνοια) - Mathematical reasoning
        4. Noesis (νόησις) - Dialectic/pure reason - highest
        """
        text_lower = text.lower()

        # Eikasia - images, shadows, reflections
        eikasia_words = ["image", "shadow", "reflection", "appearance", "seems"]
        has_eikasia = sum(1 for word in eikasia_words if word in text_lower)

        # Pistis - belief, physical objects, sensible world
        pistis_words = ["believe", "physical", "see", "touch", "sense", "object"]
        has_pistis = sum(1 for word in pistis_words if word in text_lower)

        # Dianoia - mathematical, hypothetical reasoning
        dianoia_words = ["calculate", "measure", "hypothesis", "assume", "mathematical", "geometry"]
        has_dianoia = sum(1 for word in dianoia_words if word in text_lower)

        # Noesis - pure reason, Forms, dialectic
        noesis_words = ["form", "essence", "reason", "dialectic", "eternal", "intelligible"]
        has_noesis = sum(1 for word in noesis_words if word in text_lower)

        # Determine highest level present
        levels = []
        if has_eikasia >= 1:
            levels.append({
                "level": "Eikasia (εἰκασία)",
                "rank": 1,
                "description": "Images and shadows - lowest form of apprehension"
            })
        if has_pistis >= 1:
            levels.append({
                "level": "Pistis (πίστις)",
                "rank": 2,
                "description": "Belief about physical objects - sensible world"
            })
        if has_dianoia >= 1:
            levels.append({
                "level": "Dianoia (διάνοια)",
                "rank": 3,
                "description": "Mathematical reasoning - uses hypotheses"
            })
        if has_noesis >= 1:
            levels.append({
                "level": "Noesis (νόησις)",
                "rank": 4,
                "description": "Pure reason and dialectic - knowledge of Forms"
            })

        if not levels:
            highest_level = "Unclear"
            epistemic_status = "Indeterminate"
        else:
            highest = max(levels, key=lambda x: x["rank"])
            highest_level = highest["level"]
            if highest["rank"] == 4:
                epistemic_status = "Knowledge (ἐπιστήμη)"
            elif highest["rank"] >= 2:
                epistemic_status = "Opinion (δόξα)"
            else:
                epistemic_status = "Illusion"

        return {
            "levels_present": levels if levels else [{"level": "None detected", "rank": 0, "description": "No clear epistemic level"}],
            "highest_level": highest_level,
            "epistemic_status": epistemic_status,
            "note": "Ascend from images to Forms, from opinion (δόξα) to knowledge (ἐπιστήμη)"
        }

    def _assess_tripartite_soul(self, text: str) -> Dict[str, Any]:
        """
        Assess the Tripartite Soul (ψυχή).

        Three parts:
        1. Reason (λογιστικόν/logistikon) - seeks truth, should rule
        2. Spirit (θυμοειδές/thumoeidēs) - seeks honor, ally of reason
        3. Appetite (ἐπιθυμητικόν/epithumētikon) - seeks pleasure, must be controlled
        """
        text_lower = text.lower()

        # Reason indicators
        reason_words = ["reason", "rational", "think", "wisdom", "understand", "truth"]
        has_reason = sum(1 for word in reason_words if word in text_lower)

        # Spirit indicators
        spirit_words = ["honor", "courage", "pride", "anger", "passion", "spirit"]
        has_spirit = sum(1 for word in spirit_words if word in text_lower)

        # Appetite indicators
        appetite_words = ["desire", "pleasure", "appetite", "want", "crave", "hunger"]
        has_appetite = sum(1 for word in appetite_words if word in text_lower)

        # Control/harmony indicators
        control_words = ["control", "master", "rule", "govern", "harmony"]
        has_control = sum(1 for word in control_words if word in text_lower)

        # Determine which part dominates
        parts_scores = {
            "Reason (λογιστικόν)": has_reason,
            "Spirit (θυμοειδές)": has_spirit,
            "Appetite (ἐπιθυμητικόν)": has_appetite
        }

        dominant_part = max(parts_scores, key=parts_scores.get) if max(parts_scores.values()) > 0 else "None clear"

        # Assess harmony
        if has_reason >= 2 and has_control >= 1:
            harmony = "Harmonious"
            description = "Reason rules, spirit allies with reason, appetite is controlled"
            justice_state = "Just soul"
        elif has_reason >= 1 and has_spirit >= 1 and has_appetite >= 1:
            harmony = "All parts present"
            description = "All three parts active - balance needed"
            justice_state = "Potentially harmonious"
        elif has_appetite >= 2 and has_reason == 0:
            harmony = "Appetite dominates"
            description = "Ruled by desires - reason absent - unjust soul"
            justice_state = "Unjust soul"
        elif has_spirit >= 2 and has_reason == 0:
            harmony = "Spirit dominates"
            description = "Ruled by honor and anger - needs reason's guidance"
            justice_state = "Imbalanced"
        else:
            harmony = "Unclear"
            description = "Soul structure indeterminate"
            justice_state = "Unknown"

        return {
            "dominant_part": dominant_part,
            "harmony": harmony,
            "description": description,
            "justice_state": justice_state,
            "principle": "Justice in the soul = each part doing its proper work, reason ruling"
        }

    def _evaluate_governance(self, text: str) -> Dict[str, Any]:
        """
        Evaluate governance through Philosopher-King ideal.

        Only those who know the Good should rule.
        Wisdom, not power or wealth, qualifies for leadership.
        """
        text_lower = text.lower()

        # Philosopher-king indicators
        wisdom_rule = ["wise rule", "wisdom", "knowledge", "philosopher", "truth"]
        has_wisdom_rule = sum(1 for phrase in wisdom_rule if phrase in text_lower)

        # Power/force indicators (opposed to wisdom)
        power_rule = ["power", "force", "strength", "might"]
        has_power = sum(1 for word in power_rule if word in text_lower)

        # Wealth indicators (opposed to wisdom)
        wealth_words = ["wealth", "money", "rich", "gold", "profit"]
        has_wealth = sum(1 for word in wealth_words if word in text_lower)

        # Democracy/many (problematic for Plato)
        democracy_words = ["democracy", "everyone", "all vote", "majority"]
        has_democracy = sum(1 for phrase in democracy_words if phrase in text_lower)

        # Education/cultivation
        education_words = ["educate", "train", "cultivate", "prepare", "learn"]
        has_education = sum(1 for word in education_words if word in text_lower)

        if has_wisdom_rule >= 2 or (has_wisdom_rule >= 1 and has_education >= 1):
            governance_type = "Philosopher-King"
            description = "Rule by the wise who know the Good - ideal governance"
            quality = "Ideal"
        elif has_democracy >= 1:
            governance_type = "Democracy"
            description = "Rule by the many - problematic, can lead to tyranny"
            quality = "Unstable"
        elif has_wealth >= 2:
            governance_type = "Oligarchy"
            description = "Rule by the wealthy - pursuit of money, not Good"
            quality = "Corrupt"
        elif has_power >= 2:
            governance_type = "Timocracy/Tyranny"
            description = "Rule by power/honor - not wisdom"
            quality = "Unjust"
        else:
            governance_type = "Unclear"
            description = "Governance type indeterminate"
            quality = "Unknown"

        return {
            "type": governance_type,
            "description": description,
            "quality": quality,
            "principle": "Only those who know the Form of the Good should rule"
        }

    def _check_recollection(self, text: str) -> Dict[str, Any]:
        """
        Check Anamnesis (ἀνάμνησις) - recollection.

        Learning is recollecting what the soul knew before birth.
        Knowledge is innate, triggered by experience.
        """
        text_lower = text.lower()

        # Recollection indicators
        recall_words = ["remember", "recall", "recollect", "recognize", "already know"]
        has_recall = sum(1 for phrase in recall_words if phrase in text_lower)

        # Innate knowledge
        innate_words = ["innate", "born with", "always knew", "within"]
        has_innate = sum(1 for phrase in innate_words if phrase in text_lower)

        # Discovery vs learning
        discover_words = ["discover", "uncover", "realize", "awakening"]
        has_discover = sum(1 for word in discover_words if word in text_lower)

        # External teaching (opposed to recollection)
        external_words = ["taught", "learned from", "told", "instructed"]
        has_external = sum(1 for phrase in external_words if phrase in text_lower)

        if has_recall >= 1 or has_innate >= 1 or has_discover >= 2:
            status = "Recollection Active"
            description = "Knowledge emerging from within - anamnesis of the Forms"
            mode = "Internal"
        elif has_external >= 2 and has_recall == 0:
            status = "External Learning"
            description = "Relying on external instruction - not true recollection"
            mode = "External"
        else:
            status = "Unclear"
            description = "Recollection status indeterminate"
            mode = "Unknown"

        return {
            "status": status,
            "description": description,
            "mode": mode,
            "principle": "Learning is recollection - the soul remembers eternal Forms"
        }

    def _assess_eros_ascent(self, text: str) -> Dict[str, Any]:
        """
        Assess Eros (ἔρως) and the ladder of love/beauty.

        Ascent: Physical beauty → Beautiful souls → Beautiful institutions →
                Beautiful knowledge → Beauty itself
        """
        text_lower = text.lower()

        # Physical beauty (lowest rung)
        physical_beauty = ["beautiful body", "physical beauty", "attractive", "appearance"]
        has_physical = sum(1 for phrase in physical_beauty if phrase in text_lower)

        # Soul/character beauty
        soul_beauty = ["beautiful soul", "character", "virtue", "noble"]
        has_soul = sum(1 for phrase in soul_beauty if phrase in text_lower)

        # Institutional/cultural beauty
        institution_beauty = ["laws", "institutions", "customs", "practices"]
        has_institution = sum(1 for word in institution_beauty if word in text_lower)

        # Knowledge/wisdom beauty
        knowledge_beauty = ["knowledge", "wisdom", "understanding", "truth"]
        has_knowledge = sum(1 for word in knowledge_beauty if word in text_lower)

        # Beauty itself - the Form
        form_beauty = ["beauty itself", "eternal beauty", "form of beauty", "absolute beauty"]
        has_form = sum(1 for phrase in form_beauty if phrase in text_lower)

        # Desire/eros indicators
        eros_words = ["desire", "love", "longing", "yearning", "eros"]
        has_eros = sum(1 for word in eros_words if word in text_lower)

        # Determine highest rung reached
        rungs = []
        if has_physical >= 1:
            rungs.append(1)
        if has_soul >= 1:
            rungs.append(2)
        if has_institution >= 1:
            rungs.append(3)
        if has_knowledge >= 1:
            rungs.append(4)
        if has_form >= 1:
            rungs.append(5)

        if 5 in rungs:
            level = "Beauty Itself"
            description = "Contemplating the eternal Form of Beauty - highest eros"
            rung = "Fifth (highest)"
        elif 4 in rungs:
            level = "Beauty of Knowledge"
            description = "Love of wisdom and beautiful knowledge"
            rung = "Fourth"
        elif 3 in rungs:
            level = "Beauty of Institutions"
            description = "Appreciating beautiful laws and practices"
            rung = "Third"
        elif 2 in rungs:
            level = "Beauty of Souls"
            description = "Loving beautiful character and virtue"
            rung = "Second"
        elif 1 in rungs:
            level = "Physical Beauty"
            description = "Attracted to beautiful bodies - lowest rung"
            rung = "First (lowest)"
        else:
            level = "No Ascent"
            description = "Ladder of love not engaged"
            rung = "None"

        return {
            "level": level,
            "description": description,
            "rung": rung,
            "has_eros": has_eros >= 1,
            "principle": "Eros leads us up the ladder from physical to eternal Beauty"
        }

    def _evaluate_justice(self, text: str) -> Dict[str, Any]:
        """
        Evaluate Justice (δικαιοσύνη).

        Justice = each part doing its proper work, harmony of the whole.
        In soul: reason ruling, spirit supporting, appetite controlled.
        In state: rulers ruling, guardians defending, producers producing.
        """
        text_lower = text.lower()

        # Justice indicators
        justice_words = ["justice", "just", "right", "fair"]
        has_justice = sum(1 for word in justice_words if word in text_lower)

        # Harmony indicators
        harmony_words = ["harmony", "order", "balance", "proper place", "each doing"]
        has_harmony = sum(1 for phrase in harmony_words if phrase in text_lower)

        # Proper function indicators
        function_words = ["proper work", "function", "role", "duty", "task"]
        has_function = sum(1 for phrase in function_words if phrase in text_lower)

        # Disorder/injustice indicators
        disorder_words = ["chaos", "disorder", "wrong place", "confusion", "conflict"]
        has_disorder = sum(1 for phrase in disorder_words if phrase in text_lower)

        # Unity indicators
        unity_words = ["unity", "whole", "together", "one"]
        has_unity = sum(1 for word in unity_words if word in text_lower)

        if (has_justice >= 1 and has_harmony >= 1) or has_function >= 1:
            justice_status = "Just"
            description = "Each part doing its proper work - harmony and order"
            quality = "Virtuous"
        elif has_disorder >= 2:
            justice_status = "Unjust"
            description = "Parts in conflict, not doing proper work - disorder"
            quality = "Vicious"
        elif has_harmony >= 1 or has_unity >= 1:
            justice_status = "Approaching Justice"
            description = "Seeking harmony and proper order"
            quality = "Developing"
        else:
            justice_status = "Unclear"
            description = "Justice status indeterminate"
            quality = "Unknown"

        return {
            "status": justice_status,
            "description": description,
            "quality": quality,
            "principle": "Justice is each part doing its proper work - harmony of the whole"
        }

    def _assess_dialectic(self, text: str) -> Dict[str, Any]:
        """
        Assess Dialectic (διαλεκτική) - method of philosophical inquiry.

        Dialectic: Question and answer, examining assumptions,
        ascending to first principles (Forms).
        """
        text_lower = text.lower()

        # Question indicators
        question_count = text.count("?")
        has_questions = question_count >= 1

        # Dialogue indicators
        dialogue_words = ["discuss", "dialogue", "conversation", "examine", "question"]
        has_dialogue = sum(1 for word in dialogue_words if word in text_lower)

        # Assumption examination
        examine_words = ["assume", "presuppose", "hypothesis", "examine", "test"]
        has_examine = sum(1 for word in examine_words if word in text_lower)

        # First principles
        principle_words = ["first principle", "fundamental", "foundation", "ultimate"]
        has_principles = sum(1 for phrase in principle_words if phrase in text_lower)

        # Definition seeking
        definition_words = ["what is", "define", "essence", "nature of"]
        has_definition = sum(1 for phrase in definition_words if phrase in text_lower)

        # Assertion without inquiry (opposed to dialectic)
        assertion_words = ["it is", "must be", "certainly", "obviously"]
        has_assertion = sum(1 for phrase in assertion_words if phrase in text_lower)

        dialectic_score = has_questions + has_dialogue + has_examine + has_definition

        if dialectic_score >= 3 or has_principles >= 1:
            dialectic_level = "High Dialectic"
            description = "Active questioning and examination - ascending to Forms"
            method = "Philosophical"
        elif dialectic_score >= 2:
            dialectic_level = "Moderate Dialectic"
            description = "Some questioning and examination present"
            method = "Inquiry-based"
        elif has_assertion >= 2 and dialectic_score == 0:
            dialectic_level = "No Dialectic"
            description = "Mere assertion without examination - not philosophical"
            method = "Dogmatic"
        else:
            dialectic_level = "Low Dialectic"
            description = "Limited philosophical inquiry"
            method = "Unclear"

        return {
            "level": dialectic_level,
            "description": description,
            "method": method,
            "principle": "Dialectic is the highest method - questioning toward first principles"
        }

    def _contemplate_the_good(self, text: str) -> Dict[str, Any]:
        """
        Contemplate the Form of the Good (τὸ ἀγαθόν).

        The Good is:
        - The highest Form
        - Source of truth and being
        - Like the sun - illuminates and gives life
        - Beyond being itself
        """
        text_lower = text.lower()

        # The Good itself
        good_words = ["the good", "highest good", "supreme good", "form of good"]
        has_good = sum(1 for phrase in good_words if phrase in text_lower)

        # Sun analogy
        sun_words = ["sun", "light", "illuminate", "source", "gives life"]
        has_sun = sum(1 for phrase in sun_words if phrase in text_lower)

        # Truth and being
        truth_being = ["truth", "being", "reality", "existence"]
        has_truth_being = sum(1 for word in truth_being if word in text_lower)

        # Highest/supreme
        highest_words = ["highest", "supreme", "ultimate", "greatest", "beyond"]
        has_highest = sum(1 for word in highest_words if word in text_lower)

        # Source/cause
        source_words = ["source", "cause", "origin", "from which"]
        has_source = sum(1 for phrase in source_words if phrase in text_lower)

        # Particular goods (not the Good itself)
        particular_goods = ["good thing", "good for", "useful", "beneficial"]
        has_particular = sum(1 for phrase in particular_goods if phrase in text_lower)

        if has_good >= 1 or (has_highest >= 1 and has_source >= 1):
            contemplation = "The Good Itself"
            description = "Contemplating the highest Form - source of truth and being"
            level = "Highest knowledge"
        elif has_sun >= 1 and has_truth_being >= 1:
            contemplation = "Approaching the Good"
            description = "Recognizing the source of truth - near the Good"
            level = "High knowledge"
        elif has_highest >= 1:
            contemplation = "Seeking the Highest"
            description = "Oriented toward the highest - not yet the Good itself"
            level = "Seeking"
        elif has_particular >= 2:
            contemplation = "Particular Goods"
            description = "Focused on particular goods, not the Good itself"
            level = "Opinion"
        else:
            contemplation = "Unclear"
            description = "Relation to the Good indeterminate"
            level = "Unknown"

        return {
            "contemplation": contemplation,
            "description": description,
            "level": level,
            "principle": "The Good is the highest Form - beyond being, source of all truth and reality"
        }

    def _calculate_tension(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate philosophical tension based on Platonic analysis.

        Tensions arise from:
        - Trapped in the cave (illusion)
        - Low epistemic level (opinion vs knowledge)
        - Unjust soul (appetite ruling)
        - Non-philosophical governance
        - Lack of dialectic
        - Distance from the Good
        """
        tension_score = 0
        tension_elements = []

        # Check cave position
        cave_position = analysis["cave"]["position"]
        if "In Chains" in cave_position:
            tension_score += 3
            tension_elements.append("Imprisoned in cave - trapped in illusion")
        elif "Unclear" in cave_position:
            tension_score += 1
            tension_elements.append("Cave position unclear - relationship to truth unknown")

        # Check epistemic status
        epistemic_status = analysis["divided_line"]["epistemic_status"]
        if "Illusion" in epistemic_status or "Opinion" in epistemic_status:
            tension_score += 2
            tension_elements.append(f"Epistemic deficiency: {epistemic_status}")

        # Check soul harmony
        soul_justice = analysis["soul"]["justice_state"]
        if "Unjust" in soul_justice:
            tension_score += 2
            tension_elements.append("Unjust soul - parts in disorder")
        elif "Imbalanced" in soul_justice:
            tension_score += 1
            tension_elements.append("Soul imbalance - needs harmony")

        # Check governance
        governance_quality = analysis["governance"]["quality"]
        if governance_quality in ["Corrupt", "Unjust", "Unstable"]:
            tension_score += 1
            tension_elements.append(f"Problematic governance: {analysis['governance']['type']}")

        # Check justice
        justice_status = analysis["justice"]["status"]
        if "Unjust" in justice_status:
            tension_score += 2
            tension_elements.append("Injustice - parts not doing proper work")

        # Check dialectic
        dialectic_level = analysis["dialectic"]["level"]
        if "No Dialectic" in dialectic_level:
            tension_score += 1
            tension_elements.append("No dialectic - mere assertion without inquiry")

        # Check relation to the Good
        good_level = analysis["good"]["level"]
        if "Opinion" in good_level or "Unknown" in good_level:
            tension_score += 1
            tension_elements.append("Distant from the Good - highest Form not contemplated")

        # Determine tension level
        if tension_score >= 8:
            level = "Very High"
            description = "Severe alienation from Forms and truth - deep in the cave"
        elif tension_score >= 5:
            level = "High"
            description = "Significant distance from truth and the Good"
        elif tension_score >= 3:
            level = "Moderate"
            description = "Some tensions in ascent to Forms"
        elif tension_score >= 1:
            level = "Low"
            description = "Minor tensions, generally oriented toward truth"
        else:
            level = "Very Low"
            description = "Aligned with Forms and the Good"

        return {
            "level": level,
            "description": description,
            "elements": tension_elements if tension_elements else ["No significant tensions"]
        }

    def _construct_reasoning(
        self,
        forms: Dict[str, Any],
        cave: Dict[str, Any],
        divided_line: Dict[str, Any],
        soul: Dict[str, Any],
        justice: Dict[str, Any],
        good: Dict[str, Any]
    ) -> str:
        """Construct Platonic philosophical reasoning."""
        primary_form = forms["primary"]

        reasoning = (
            f"From a Platonic perspective, this text concerns {primary_form}. "
            f"Position in the cave: {cave['description']}. "
            f"Epistemic status on the divided line: {divided_line['epistemic_status']}. "
        )

        # Add soul analysis
        reasoning += f"Soul harmony: {soul['description']}. "

        # Add justice
        reasoning += f"Justice: {justice['description']}. "

        # Add the Good
        reasoning += f"Relation to the Good: {good['description']}. "

        # Conclude with Platonic wisdom
        reasoning += (
            "Remember: the material world is but shadow of eternal Forms. "
            "True knowledge comes through dialectic and recollection. "
            "Justice is harmony, each part doing its proper work. "
            "The unexamined life is not worth living - ascend from the cave to contemplate the Good!"
        )

        return reasoning
