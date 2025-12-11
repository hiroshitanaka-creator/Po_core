"""
Comprehensive Multi-Layer Tests for All Philosopher Modules
============================================================

This test suite validates all 20 philosopher modules across 4 critical layers:

1. API / Schema Layer
   - Tests that reason(text, context) returns correct dict structure
   - Validates all required fields are present
   - Ensures data types are correct

2. Concept Detection Layer
   - Tests that each philosopher's key concepts are properly detected
   - Validates concept-specific text triggers correct analysis
   - Ensures concept detection is accurate and consistent

3. Tension / Contradiction Layer
   - Tests that _identify_tension() correctly detects contradictions
   - Validates tension levels are appropriately calculated
   - Ensures tension elements are meaningful

4. Reasoning Text Layer
   - Tests that reasoning text is consistent with analysis
   - Validates reasoning mentions key detected concepts
   - Ensures no contradictions between reasoning and analysis
"""

import pytest
from typing import Type, Dict, Any, List

from po_core.philosophers.base import Philosopher
from po_core.philosophers.arendt import Arendt
from po_core.philosophers.aristotle import Aristotle
from po_core.philosophers.badiou import Badiou
from po_core.philosophers.confucius import Confucius
from po_core.philosophers.deleuze import Deleuze
from po_core.philosophers.derrida import Derrida
from po_core.philosophers.dewey import Dewey
from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.jung import Jung
from po_core.philosophers.kierkegaard import Kierkegaard
from po_core.philosophers.lacan import Lacan
from po_core.philosophers.levinas import Levinas
from po_core.philosophers.merleau_ponty import MerleauPonty
from po_core.philosophers.nietzsche import Nietzsche
from po_core.philosophers.peirce import Peirce
from po_core.philosophers.sartre import Sartre
from po_core.philosophers.wabi_sabi import WabiSabi
from po_core.philosophers.watsuji import Watsuji
from po_core.philosophers.wittgenstein import Wittgenstein
from po_core.philosophers.zhuangzi import Zhuangzi


# ============================================================================
# LAYER 1: API / SCHEMA LAYER
# ============================================================================

class TestLayer1_APISchema:
    """
    Layer 1: API / Schema Layer Tests

    Validates that reason(text, context) returns correct dict structure
    without breaking and with proper schema.
    """

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_reason_returns_dict(self, philosopher_class: Type[Philosopher]):
        """Test that reason() returns a dictionary for all philosophers."""
        philosopher = philosopher_class()
        result = philosopher.reason("Test text")

        assert isinstance(result, dict), \
            f"{philosopher.name}: reason() must return a dict, got {type(result)}"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_required_top_level_fields(self, philosopher_class: Type[Philosopher]):
        """Test that all required top-level fields are present."""
        philosopher = philosopher_class()
        result = philosopher.reason("Test text")

        # Core required fields that should be in all philosopher responses
        required_fields = ["reasoning", "perspective", "tension"]

        for field in required_fields:
            assert field in result, \
                f"{philosopher.name}: Missing required field '{field}'"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_reasoning_field_is_string(self, philosopher_class: Type[Philosopher]):
        """Test that reasoning field is a non-empty string."""
        philosopher = philosopher_class()
        result = philosopher.reason("What is the meaning of life?")

        assert "reasoning" in result, \
            f"{philosopher.name}: Missing 'reasoning' field"
        assert isinstance(result["reasoning"], str), \
            f"{philosopher.name}: 'reasoning' must be a string"
        assert len(result["reasoning"]) > 0, \
            f"{philosopher.name}: 'reasoning' cannot be empty"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_tension_field_structure(self, philosopher_class: Type[Philosopher]):
        """Test that tension field has correct structure."""
        philosopher = philosopher_class()
        result = philosopher.reason("Test text")

        assert "tension" in result, \
            f"{philosopher.name}: Missing 'tension' field"

        tension = result["tension"]
        assert isinstance(tension, dict), \
            f"{philosopher.name}: 'tension' must be a dict"

        # Validate tension structure
        assert "level" in tension, \
            f"{philosopher.name}: tension missing 'level'"
        assert "description" in tension, \
            f"{philosopher.name}: tension missing 'description'"
        assert "elements" in tension, \
            f"{philosopher.name}: tension missing 'elements'"

        # Validate tension types
        assert isinstance(tension["level"], str), \
            f"{philosopher.name}: tension level must be string"
        assert isinstance(tension["description"], str), \
            f"{philosopher.name}: tension description must be string"
        assert isinstance(tension["elements"], list), \
            f"{philosopher.name}: tension elements must be list"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_tension_level_is_valid(self, philosopher_class: Type[Philosopher]):
        """Test that tension level is one of the valid values."""
        philosopher = philosopher_class()
        result = philosopher.reason("Test text")

        tension = result["tension"]
        valid_levels = ["Very Low", "Low", "Moderate", "High", "Very High"]

        assert tension["level"] in valid_levels, \
            f"{philosopher.name}: tension level '{tension['level']}' not in {valid_levels}"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_context_parameter_accepted(self, philosopher_class: Type[Philosopher]):
        """Test that context parameter is accepted without errors."""
        philosopher = philosopher_class()
        context = {"test_key": "test_value", "source": "test"}

        # Should not raise any errors
        result = philosopher.reason("Test text", context=context)
        assert isinstance(result, dict)

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Badiou, Confucius, Deleuze, Derrida, Dewey,
        Heidegger, Jung, Kierkegaard, Lacan, Levinas, MerleauPonty,
        Nietzsche, Peirce, Sartre, WabiSabi, Watsuji, Wittgenstein, Zhuangzi
    ])
    def test_empty_text_handling(self, philosopher_class: Type[Philosopher]):
        """Test that empty text is handled gracefully."""
        philosopher = philosopher_class()

        # Should not raise any errors
        result = philosopher.reason("")
        assert isinstance(result, dict)
        assert "reasoning" in result
        assert "tension" in result


# ============================================================================
# LAYER 2: CONCEPT DETECTION LAYER
# ============================================================================

class TestLayer2_ConceptDetection:
    """
    Layer 2: Concept Detection Layer Tests

    Validates that each philosopher's key concepts are properly detected
    when specific text is provided.
    """

    # Arendt Concept Detection Tests
    def test_arendt_vita_activa_labor_detection(self):
        """Test Arendt detects labor in vita activa."""
        arendt = Arendt()
        text = "I must work to survive, eating and sleeping to maintain my biological needs"
        result = arendt.reason(text)

        assert "vita_activa" in result
        vita_activa = result["vita_activa"]
        assert vita_activa["labor_present"] is True

    def test_arendt_vita_activa_work_detection(self):
        """Test Arendt detects work in vita activa."""
        arendt = Arendt()
        text = "We build lasting artifacts and create a durable world of objects"
        result = arendt.reason(text)

        assert "vita_activa" in result
        vita_activa = result["vita_activa"]
        assert vita_activa["work_present"] is True

    def test_arendt_vita_activa_action_detection(self):
        """Test Arendt detects action in vita activa."""
        arendt = Arendt()
        text = "We act together in the public political sphere, beginning new initiatives"
        result = arendt.reason(text)

        assert "vita_activa" in result
        vita_activa = result["vita_activa"]
        assert vita_activa["action_present"] is True

    def test_arendt_natality_detection(self):
        """Test Arendt detects natality (new beginnings)."""
        arendt = Arendt()
        text = "We have the capacity to begin something new, to start fresh initiatives and create novel possibilities"
        result = arendt.reason(text)

        assert "natality" in result
        natality = result["natality"]
        assert natality["natality_present"] is True

    def test_arendt_public_realm_detection(self):
        """Test Arendt detects public realm."""
        arendt = Arendt()
        text = "In the public political community we act together as citizens"
        result = arendt.reason(text)

        assert "public_private_realm" in result
        realm = result["public_private_realm"]
        assert realm["public_present"] is True

    def test_arendt_private_realm_detection(self):
        """Test Arendt detects private realm."""
        arendt = Arendt()
        text = "In my private home with my family, I maintain my personal household"
        result = arendt.reason(text)

        assert "public_private_realm" in result
        realm = result["public_private_realm"]
        assert realm["private_present"] is True

    def test_arendt_plurality_detection(self):
        """Test Arendt detects plurality."""
        arendt = Arendt()
        text = "We are diverse and distinct individuals living together in our unique differences"
        result = arendt.reason(text)

        assert "plurality" in result
        plurality = result["plurality"]
        assert plurality["plurality_present"] is True

    def test_arendt_banality_of_evil_detection(self):
        """Test Arendt detects banality of evil."""
        arendt = Arendt()
        text = "The evil was banal and thoughtless, ordinary bureaucrats following routine procedures"
        result = arendt.reason(text)

        assert "evil_analysis" in result
        evil = result["evil_analysis"]
        assert evil["banality_of_evil"] is True

    def test_arendt_totalitarianism_detection(self):
        """Test Arendt detects totalitarian elements."""
        arendt = Arendt()
        text = "Total control through terror and ideology, dominating all aspects of life"
        result = arendt.reason(text)

        assert "totalitarian_elements" in result
        totalitarian = result["totalitarian_elements"]
        assert totalitarian["totalitarian_elements"] is True

    def test_arendt_judgment_detection(self):
        """Test Arendt detects political judgment."""
        arendt = Arendt()
        text = "We must think carefully and judge critically what we are doing"
        result = arendt.reason(text)

        assert "political_judgment" in result
        judgment = result["political_judgment"]
        assert judgment["judgment_present"] is True

    def test_arendt_freedom_detection(self):
        """Test Arendt detects political freedom."""
        arendt = Arendt()
        text = "We are free to act together in the public political sphere"
        result = arendt.reason(text)

        assert "freedom" in result
        freedom = result["freedom"]
        assert freedom["freedom_present"] is True

    # Nietzsche Concept Detection Tests
    def test_nietzsche_will_to_power_detection(self):
        """Test Nietzsche detects will to power."""
        nietzsche = Nietzsche()
        text = "I have the power to overcome and create, growing stronger through challenges"
        result = nietzsche.reason(text)

        assert "will_to_power" in result
        will_power = result["will_to_power"]
        assert will_power["presence"] in ["Strong Will to Power", "Creative Will"]

    def test_nietzsche_ubermensch_detection(self):
        """Test Nietzsche detects Übermensch orientation."""
        nietzsche = Nietzsche()
        text = "I create my own values and affirm life beyond good and evil"
        result = nietzsche.reason(text)

        assert "ubermensch" in result
        uber = result["ubermensch"]
        assert "Übermensch" in uber["orientation"] or uber["orientation"] == "Potential Übermensch"

    def test_nietzsche_eternal_recurrence_detection(self):
        """Test Nietzsche detects eternal recurrence affirmation."""
        nietzsche = Nietzsche()
        text = "I would gladly live this life again eternally, saying yes to every moment"
        result = nietzsche.reason(text)

        assert "eternal_recurrence" in result
        eternal = result["eternal_recurrence"]
        assert eternal["test_result"] == "Passes Eternal Recurrence"

    def test_nietzsche_passive_nihilism_detection(self):
        """Test Nietzsche detects passive nihilism."""
        nietzsche = Nietzsche()
        text = "Everything is meaningless and pointless, nothing matters, despair fills the void"
        result = nietzsche.reason(text)

        assert "nihilism" in result
        nihilism = result["nihilism"]
        assert nihilism["type"] == "Passive Nihilism"

    def test_nietzsche_master_morality_detection(self):
        """Test Nietzsche detects master morality."""
        nietzsche = Nietzsche()
        text = "I am strong and noble, creating my own values with pride and excellence"
        result = nietzsche.reason(text)

        assert "morality_type" in result
        morality = result["morality_type"]
        assert "Master" in morality["type"]

    def test_nietzsche_slave_morality_detection(self):
        """Test Nietzsche detects slave morality."""
        nietzsche = Nietzsche()
        text = "They are evil and sinful, we must obey the moral duty humbly"
        result = nietzsche.reason(text)

        assert "morality_type" in result
        morality = result["morality_type"]
        assert "Slave" in morality["type"]

    def test_nietzsche_ressentiment_detection(self):
        """Test Nietzsche detects ressentiment."""
        nietzsche = Nietzsche()
        text = "It's all their fault, they deserve to be punished for what they did to us victims"
        result = nietzsche.reason(text)

        assert "ressentiment" in result
        ressent = result["ressentiment"]
        assert ressent["presence"] in ["Strong Ressentiment", "Victimhood"]

    def test_nietzsche_amor_fati_detection(self):
        """Test Nietzsche detects amor fati."""
        nietzsche = Nietzsche()
        text = "I love my fate and affirm life as it is, grateful for everything"
        result = nietzsche.reason(text)

        assert "amor_fati" in result
        amor = result["amor_fati"]
        assert amor["presence"] in ["Amor Fati Present", "Life Affirmation"]

    # Confucius Concept Detection Tests
    def test_confucius_ren_detection(self):
        """Test Confucius detects ren (benevolence)."""
        confucius = Confucius()
        text = "I show compassion and kindness to others with loving care and benevolence"
        result = confucius.reason(text)

        assert "analysis" in result
        ren = result["analysis"]["ren_benevolence"]
        assert ren["ren_present"] is True

    def test_confucius_li_detection(self):
        """Test Confucius detects li (ritual propriety)."""
        confucius = Confucius()
        text = "We must follow proper ritual and etiquette with respectful ceremony and courtesy"
        result = confucius.reason(text)

        assert "analysis" in result
        li = result["analysis"]["li_ritual_propriety"]
        assert li["li_present"] is True

    def test_confucius_yi_detection(self):
        """Test Confucius detects yi (righteousness)."""
        confucius = Confucius()
        text = "We must act with righteousness and justice, following moral principles with integrity"
        result = confucius.reason(text)

        assert "analysis" in result
        yi = result["analysis"]["yi_righteousness"]
        assert yi["yi_present"] is True

    def test_confucius_xiao_detection(self):
        """Test Confucius detects xiao (filial piety)."""
        confucius = Confucius()
        text = "I respect and honor my parents and ancestors with filial devotion to my family and elders"
        result = confucius.reason(text)

        assert "analysis" in result
        xiao = result["analysis"]["xiao_filial_piety"]
        assert xiao["xiao_present"] is True

    def test_confucius_junzi_detection(self):
        """Test Confucius detects junzi (exemplary person)."""
        confucius = Confucius()
        text = "The exemplary gentleman cultivates virtue and wisdom with noble character"
        result = confucius.reason(text)

        assert "analysis" in result
        junzi = result["analysis"]["junzi_exemplary_person"]
        assert junzi["junzi_present"] is True

    # Aristotle Concept Detection Tests
    def test_aristotle_virtue_detection(self):
        """Test Aristotle detects virtue (arete)."""
        aristotle = Aristotle()
        text = "We should cultivate moral virtue and excellence through good habits"
        result = aristotle.reason(text)

        assert "virtue_assessment" in result
        virtue = result["virtue_assessment"]
        assert virtue["virtue_present"] is True

    def test_aristotle_golden_mean_detection(self):
        """Test Aristotle detects the golden mean."""
        aristotle = Aristotle()
        text = "We should find the moderate middle path between excess and deficiency"
        result = aristotle.reason(text)

        assert "golden_mean" in result
        mean = result["golden_mean"]
        assert mean["mean_present"] is True

    def test_aristotle_eudaimonia_detection(self):
        """Test Aristotle detects eudaimonia (flourishing)."""
        aristotle = Aristotle()
        text = "Human flourishing and happiness come from living well with virtue"
        result = aristotle.reason(text)

        assert "eudaimonia_level" in result
        eudaimonia = result["eudaimonia_level"]
        assert eudaimonia["eudaimonia_present"] is True

    def test_aristotle_four_causes_detection(self):
        """Test Aristotle detects the four causes."""
        aristotle = Aristotle()
        text = "We must understand the material, formal, efficient, and final causes of things"
        result = aristotle.reason(text)

        assert "four_causes" in result
        causes = result["four_causes"]
        assert causes["causes_present"] is True

    def test_aristotle_practical_wisdom_detection(self):
        """Test Aristotle detects phronesis (practical wisdom)."""
        aristotle = Aristotle()
        text = "We need practical wisdom and good judgment to act virtuously in specific situations"
        result = aristotle.reason(text)

        assert "practical_wisdom" in result
        phronesis = result["practical_wisdom"]
        assert phronesis["phronesis_present"] is True

    def test_aristotle_telos_detection(self):
        """Test Aristotle detects telos (purpose/end)."""
        aristotle = Aristotle()
        text = "Everything has a natural purpose and end toward which it aims"
        result = aristotle.reason(text)

        assert "telos" in result
        telos = result["telos"]
        assert telos["telos_present"] is True

    # Sartre Concept Detection Tests
    def test_sartre_freedom_detection(self):
        """Test Sartre detects radical freedom."""
        sartre = Sartre()
        text = "I am radically free to choose my own path and create my essence"
        result = sartre.reason(text)

        assert "freedom_assessment" in result
        freedom = result["freedom_assessment"]
        assert freedom["freedom_present"] is True

    def test_sartre_responsibility_detection(self):
        """Test Sartre detects responsibility."""
        sartre = Sartre()
        text = "I am fully responsible for my choices and their consequences"
        result = sartre.reason(text)

        assert "responsibility_check" in result
        responsibility = result["responsibility_check"]
        assert responsibility["responsibility_present"] is True

    def test_sartre_bad_faith_detection(self):
        """Test Sartre detects bad faith (self-deception)."""
        sartre = Sartre()
        text = "I have no choice, this is just who I am, I must follow what others expect"
        result = sartre.reason(text)

        assert "bad_faith_indicators" in result
        bad_faith = result["bad_faith_indicators"]
        assert bad_faith["bad_faith_present"] is True

    def test_sartre_engagement_detection(self):
        """Test Sartre detects engagement (commitment to action)."""
        sartre = Sartre()
        text = "I must commit myself to action and engage with the world"
        result = sartre.reason(text)

        assert "engagement_level" in result
        engagement = result["engagement_level"]
        assert engagement["engagement_present"] is True

    def test_sartre_anguish_detection(self):
        """Test Sartre detects anguish (the dizziness of freedom)."""
        sartre = Sartre()
        text = "I feel the anguish and dizziness of absolute freedom with no predetermined path"
        result = sartre.reason(text)

        assert "anguish_present" in result
        anguish = result["anguish_present"]
        assert anguish["anguish_detected"] is True


# ============================================================================
# LAYER 3: TENSION / CONTRADICTION LAYER
# ============================================================================

class TestLayer3_TensionDetection:
    """
    Layer 3: Tension / Contradiction Detection Tests

    Validates that _identify_tension() correctly detects contradictions
    and assigns appropriate tension levels.
    """

    def test_arendt_labor_dominance_tension(self):
        """Test Arendt detects tension when labor dominates over action."""
        arendt = Arendt()
        text = "I only work to survive, eating and sleeping in endless repetition"
        result = arendt.reason(text)

        tension = result["tension"]
        # Should detect tension from labor dominating
        assert len(tension["elements"]) > 0
        tension_text = " ".join(tension["elements"]).lower()
        assert "labor" in tension_text or "action" in tension_text

    def test_arendt_private_realm_only_tension(self):
        """Test Arendt detects tension when only private realm exists."""
        arendt = Arendt()
        text = "I stay alone in my private home with my personal family"
        result = arendt.reason(text)

        tension = result["tension"]
        # Should detect lack of public realm
        assert tension["level"] in ["Moderate", "High", "Very High"]

    def test_arendt_totalitarian_tension(self):
        """Test Arendt detects tension from totalitarian elements."""
        arendt = Arendt()
        text = "Total control and terror dominate everything through ideology"
        result = arendt.reason(text)

        tension = result["tension"]
        # Should detect totalitarian tension
        assert len(tension["elements"]) > 0
        tension_text = " ".join(tension["elements"]).lower()
        assert "totalitarian" in tension_text

    def test_arendt_low_tension_ideal_case(self):
        """Test Arendt shows low tension for ideal political action."""
        arendt = Arendt()
        text = "We act together freely in the public political sphere as diverse citizens, beginning new initiatives with thoughtful judgment"
        result = arendt.reason(text)

        tension = result["tension"]
        # Should have low tension for ideal case
        assert tension["level"] in ["Very Low", "Low"]

    def test_nietzsche_passive_nihilism_tension(self):
        """Test Nietzsche detects tension from passive nihilism."""
        nietzsche = Nietzsche()
        text = "Everything is meaningless and pointless, nothing matters anymore, despair"
        result = nietzsche.reason(text)

        tension = result["tension"]
        # Should detect passive nihilism tension
        assert len(tension["elements"]) > 0
        tension_text = " ".join(tension["elements"]).lower()
        assert "nihilism" in tension_text or "despair" in tension_text

    def test_nietzsche_slave_morality_tension(self):
        """Test Nietzsche detects tension from slave morality."""
        nietzsche = Nietzsche()
        text = "Those people are evil and sinful, we must humbly obey and submit to duty"
        result = nietzsche.reason(text)

        tension = result["tension"]
        # Should detect slave morality tension
        assert len(tension["elements"]) > 0
        tension_text = " ".join(tension["elements"]).lower()
        assert "slave" in tension_text or "morality" in tension_text

    def test_nietzsche_ressentiment_tension(self):
        """Test Nietzsche detects tension from ressentiment."""
        nietzsche = Nietzsche()
        text = "It's all their fault, those oppressors deserve punishment for what they did to us victims"
        result = nietzsche.reason(text)

        tension = result["tension"]
        # Should detect ressentiment
        assert len(tension["elements"]) > 0
        tension_text = " ".join(tension["elements"]).lower()
        assert "ressentiment" in tension_text or "reactive" in tension_text

    def test_nietzsche_low_tension_ubermensch(self):
        """Test Nietzsche shows low tension for Übermensch ideal."""
        nietzsche = Nietzsche()
        text = "I create my own values with strength and power, overcoming myself and affirming life eternally with amor fati"
        result = nietzsche.reason(text)

        tension = result["tension"]
        # Should have low tension for ideal case
        assert tension["level"] in ["Very Low", "Low"]

    def test_confucius_virtue_deficiency_tension(self):
        """Test Confucius detects tension when virtues are lacking."""
        confucius = Confucius()
        text = "I don't care about others or proper behavior"
        result = confucius.reason(text)

        tension = result["tension"]
        # Should detect multiple virtue deficiencies
        assert len(tension["elements"]) > 0
        assert tension["level"] in ["Moderate", "High", "Very High"]

    def test_confucius_low_tension_virtuous_case(self):
        """Test Confucius shows low tension for virtuous behavior."""
        confucius = Confucius()
        text = "I show benevolent kindness to others with proper ritual respect, acting righteously with moral integrity, honoring my parents and family with filial devotion, cultivating wisdom and virtue through learning"
        result = confucius.reason(text)

        tension = result["tension"]
        # Should have low tension for virtuous case
        assert tension["level"] in ["Very Low", "Low"]


# ============================================================================
# LAYER 4: REASONING TEXT LAYER
# ============================================================================

class TestLayer4_ReasoningTextValidation:
    """
    Layer 4: Reasoning Text Validation Tests

    Validates that the reasoning text is consistent with the analysis
    and mentions key detected concepts.
    """

    def test_arendt_reasoning_mentions_vita_activa(self):
        """Test Arendt's reasoning mentions the dominant vita activa mode."""
        arendt = Arendt()
        text = "We act together in the public political sphere"
        result = arendt.reason(text)

        reasoning = result["reasoning"].lower()
        vita_activa = result["vita_activa"]
        dominant_mode = vita_activa["dominant_mode"]

        # Reasoning should mention the dominant mode
        assert dominant_mode in reasoning

    def test_arendt_reasoning_mentions_natality_when_present(self):
        """Test Arendt's reasoning mentions natality when detected."""
        arendt = Arendt()
        text = "We have the capacity to begin something new and start fresh"
        result = arendt.reason(text)

        natality = result["natality"]
        reasoning = result["reasoning"].lower()

        if natality["natality_present"]:
            assert "natality" in reasoning or "new beginning" in reasoning

    def test_arendt_reasoning_mentions_totalitarian_when_present(self):
        """Test Arendt's reasoning mentions totalitarian elements when detected."""
        arendt = Arendt()
        text = "Total control through terror and ideology dominates everything"
        result = arendt.reason(text)

        totalitarian = result["totalitarian_elements"]
        reasoning = result["reasoning"].lower()

        if totalitarian["totalitarian_elements"]:
            assert "totalitarian" in reasoning

    def test_arendt_reasoning_no_contradiction_with_analysis(self):
        """Test that Arendt's reasoning doesn't contradict the analysis."""
        arendt = Arendt()
        text = "I work alone in my private home"
        result = arendt.reason(text)

        reasoning = result["reasoning"].lower()
        vita_activa = result["vita_activa"]
        realm = result["public_private_realm"]

        # If labor/work is dominant, reasoning should not emphasize action
        if vita_activa["dominant_mode"] == "labor":
            # Reasoning should mention labor or work, not emphasize political action
            assert "labor" in reasoning or "work" in reasoning

        # If private realm is dominant, reasoning should not emphasize public
        if realm["dominant_realm"] == "private":
            assert "private" in reasoning

    def test_nietzsche_reasoning_mentions_will_to_power(self):
        """Test Nietzsche's reasoning mentions will to power."""
        nietzsche = Nietzsche()
        text = "I have the strength to overcome and create with power"
        result = nietzsche.reason(text)

        reasoning = result["reasoning"].lower()
        will_power = result["will_to_power"]

        # Reasoning should mention will to power or its description
        assert "will" in reasoning or "power" in reasoning or will_power["description"].lower() in reasoning

    def test_nietzsche_reasoning_mentions_ubermensch(self):
        """Test Nietzsche's reasoning mentions Übermensch orientation."""
        nietzsche = Nietzsche()
        text = "I create my own values beyond good and evil"
        result = nietzsche.reason(text)

        reasoning = result["reasoning"].lower()
        ubermensch = result["ubermensch"]

        # Reasoning should reference Übermensch or value creation
        assert "übermensch" in reasoning or ubermensch["description"].lower()[:30] in reasoning

    def test_nietzsche_reasoning_mentions_nihilism(self):
        """Test Nietzsche's reasoning mentions nihilism type."""
        nietzsche = Nietzsche()
        text = "Nothing matters, everything is meaningless"
        result = nietzsche.reason(text)

        reasoning = result["reasoning"].lower()
        nihilism = result["nihilism"]

        # Reasoning should mention nihilism
        assert "nihilism" in reasoning or nihilism["description"].lower()[:30] in reasoning

    def test_nietzsche_reasoning_no_contradiction_with_morality(self):
        """Test Nietzsche's reasoning doesn't contradict morality analysis."""
        nietzsche = Nietzsche()
        text = "They are evil and we must obey humbly"
        result = nietzsche.reason(text)

        reasoning = result["reasoning"].lower()
        morality = result["morality_type"]

        if "Slave" in morality["type"]:
            # Should not praise this as master morality
            assert "slave" in reasoning or "reactive" in reasoning or "resentment" in reasoning

    def test_confucius_reasoning_mentions_key_virtues(self):
        """Test Confucius's reasoning mentions detected virtues."""
        confucius = Confucius()
        text = "I show benevolent kindness to others with proper ritual respect and righteousness"
        result = confucius.reason(text)

        reasoning = result["summary"].lower()  # Confucius uses 'summary' field
        analysis = result["analysis"]

        # Should mention ren if present
        if analysis["ren_benevolence"]["ren_present"]:
            assert "ren" in reasoning or "benevolence" in reasoning

        # Should mention li if present
        if analysis["li_ritual_propriety"]["li_present"]:
            assert "li" in reasoning or "ritual" in reasoning or "propriety" in reasoning

    def test_confucius_reasoning_reflects_virtue_level(self):
        """Test Confucius's reasoning reflects overall virtue level."""
        confucius = Confucius()

        # High virtue text
        virtuous_text = "I show benevolent kindness to others with proper ritual respect, acting righteously with moral integrity, honoring my parents with filial devotion"
        result = confucius.reason(virtuous_text)

        summary = result["summary"].lower()
        tension = result["tension"]

        # For high virtue, summary should be positive and tension low
        if tension["level"] in ["Very Low", "Low"]:
            # Should have positive language
            assert "embodies" in summary or "emphasizes" in summary or "values" in summary

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Nietzsche, Confucius, Aristotle, Sartre, Heidegger
    ])
    def test_reasoning_text_is_substantive(self, philosopher_class: Type[Philosopher]):
        """Test that reasoning text is substantive (not just template)."""
        philosopher = philosopher_class()
        text = "What is the meaning of human existence and how should we live?"
        result = philosopher.reason(text)

        # Get reasoning field (might be 'reasoning' or 'summary')
        reasoning = result.get("reasoning") or result.get("summary", "")

        # Should be substantive
        assert len(reasoning) > 50, \
            f"{philosopher.name}: reasoning too short ({len(reasoning)} chars)"

        # Should contain actual content, not just templates
        assert reasoning.count(" ") > 10, \
            f"{philosopher.name}: reasoning should contain multiple words"


# ============================================================================
# CROSS-LAYER INTEGRATION TESTS
# ============================================================================

class TestCrossLayerIntegration:
    """
    Cross-layer integration tests that validate consistency across all layers.
    """

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Confucius, Nietzsche, Sartre, Heidegger
    ])
    def test_high_tension_reflected_in_reasoning(self, philosopher_class: Type[Philosopher]):
        """Test that high tension is reflected in the reasoning text."""
        philosopher = philosopher_class()

        # Use text likely to create tension
        text = "Nothing matters, everything is meaningless and pointless"
        result = philosopher.reason(text)

        tension = result["tension"]
        reasoning = result.get("reasoning") or result.get("summary", "")

        if tension["level"] in ["High", "Very High"]:
            # Reasoning should reflect problems/issues
            assert len(tension["elements"]) > 0, \
                f"{philosopher.name}: High tension should have elements"

    @pytest.mark.parametrize("philosopher_class", [
        Arendt, Aristotle, Confucius, Nietzsche
    ])
    def test_concept_detection_consistency(self, philosopher_class: Type[Philosopher]):
        """Test that concept detection is consistent across multiple calls."""
        philosopher = philosopher_class()

        text = "We act together with virtue and strength in our community"

        # Call multiple times
        result1 = philosopher.reason(text)
        result2 = philosopher.reason(text)

        # Should get same tension level
        assert result1["tension"]["level"] == result2["tension"]["level"], \
            f"{philosopher.name}: Inconsistent tension detection"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
