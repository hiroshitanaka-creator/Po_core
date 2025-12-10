"""
Tests for Philosopher Party Machine

Comprehensive tests for the automated philosopher combination system.
"""
import pytest
from unittest.mock import patch

from po_core.party_machine import (
    PhilosopherPartyMachine,
    PartyMood,
    PhilosophicalTheme,
    PartyConfig,
    OPTIMAL_4_COMBOS,
    HIGH_TENSION_PAIRS,
    HARMONIOUS_CLUSTERS,
)


class TestPartyMachineBasics:
    """Test basic party machine functionality."""

    def test_party_machine_initialization(self):
        """Test that party machine initializes correctly."""
        machine = PhilosopherPartyMachine(verbose=False)

        assert machine is not None
        assert hasattr(machine, "available_philosophers")
        assert len(machine.available_philosophers) > 0

    def test_party_machine_has_all_moods(self):
        """Test that all moods are available."""
        moods = list(PartyMood)

        assert PartyMood.CALM in moods
        assert PartyMood.BALANCED in moods
        assert PartyMood.CHAOTIC in moods
        assert PartyMood.CRITICAL in moods

    def test_party_machine_has_all_themes(self):
        """Test that all themes are available."""
        themes = list(PhilosophicalTheme)

        assert PhilosophicalTheme.ETHICS in themes
        assert PhilosophicalTheme.EXISTENCE in themes
        assert PhilosophicalTheme.KNOWLEDGE in themes
        assert PhilosophicalTheme.POLITICS in themes


class TestPartySuggestions:
    """Test party suggestion functionality."""

    def test_suggest_party_returns_config(self):
        """Test that suggest_party returns a valid config."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config is not None
        assert isinstance(config, PartyConfig)
        assert config.theme == "ethics"
        assert config.mood == PartyMood.BALANCED
        assert len(config.philosophers) > 0

    def test_suggest_party_ethics_theme(self):
        """Test party suggestion for ethics theme."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CALM)

        assert config is not None
        assert "ethics" in config.theme.lower()
        assert config.philosophers is not None

    def test_suggest_party_existence_theme(self):
        """Test party suggestion for existence theme."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="existence", mood=PartyMood.BALANCED)

        assert config is not None
        assert "existence" in config.theme.lower()

    def test_suggest_party_with_custom_prompt(self):
        """Test party suggestion with custom prompt."""
        machine = PhilosopherPartyMachine(verbose=False)

        custom_prompt = "What is the nature of AI consciousness?"
        config = machine.suggest_party(
            theme="consciousness",
            mood=PartyMood.BALANCED,
            custom_prompt=custom_prompt,
        )

        assert config.theme == custom_prompt

    def test_suggest_party_calm_mood_size(self):
        """Test that calm mood produces smaller groups."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CALM)

        # Calm mood should produce smaller groups (4-6)
        assert 4 <= len(config.philosophers) <= 6

    def test_suggest_party_chaotic_mood_size(self):
        """Test that chaotic mood produces larger groups."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CHAOTIC)

        # Chaotic mood should produce larger groups (15-20)
        assert len(config.philosophers) >= 15


class TestThemeMatching:
    """Test theme matching functionality."""

    def test_match_theme_direct_match(self):
        """Test direct theme matching."""
        machine = PhilosopherPartyMachine(verbose=False)

        theme = machine._match_theme("ethics")

        assert theme == PhilosophicalTheme.ETHICS

    def test_match_theme_keyword_match(self):
        """Test keyword-based theme matching."""
        machine = PhilosopherPartyMachine(verbose=False)

        # "moral" should match ETHICS
        theme = machine._match_theme("What is moral responsibility?")

        assert theme == PhilosophicalTheme.ETHICS

    def test_match_theme_existence_keywords(self):
        """Test existence theme keyword matching."""
        machine = PhilosopherPartyMachine(verbose=False)

        # Use explicit existence keyword
        theme = machine._match_theme("What is the nature of being and existence?")

        assert theme == PhilosophicalTheme.EXISTENCE

    def test_match_theme_fallback_to_meaning(self):
        """Test that unknown themes fall back to MEANING."""
        machine = PhilosopherPartyMachine(verbose=False)

        theme = machine._match_theme("xyz random nonsense")

        assert theme == PhilosophicalTheme.MEANING


class TestPhilosopherSelection:
    """Test philosopher selection logic."""

    def test_select_philosophers_returns_correct_size(self):
        """Test that selection returns requested size."""
        machine = PhilosopherPartyMachine(verbose=False)

        philosophers = machine._select_philosophers(
            theme=PhilosophicalTheme.ETHICS,
            mood=PartyMood.BALANCED,
            size=8,
        )

        assert len(philosophers) == 8

    def test_select_philosophers_no_duplicates(self):
        """Test that selection has no duplicates."""
        machine = PhilosopherPartyMachine(verbose=False)

        philosophers = machine._select_philosophers(
            theme=PhilosophicalTheme.ETHICS,
            mood=PartyMood.BALANCED,
            size=10,
        )

        assert len(philosophers) == len(set(philosophers))

    def test_select_philosophers_uses_optimal_combos_for_small_groups(self):
        """Test that optimal combos are used for groups of 4 or less."""
        machine = PhilosopherPartyMachine(verbose=False)

        # For ethics with size 4, should use optimal combo
        philosophers = machine._select_philosophers(
            theme=PhilosophicalTheme.ETHICS,
            mood=PartyMood.BALANCED,
            size=4,
        )

        assert len(philosophers) == 4
        # Should be one of the optimal combos for ethics
        optimal_combos = OPTIMAL_4_COMBOS[PhilosophicalTheme.ETHICS]
        assert any(
            set(philosophers) == set(combo[:4]) for combo in optimal_combos
        )

    def test_select_philosophers_calm_mood_uses_harmonious(self):
        """Test that calm mood tends to use harmonious philosophers."""
        machine = PhilosopherPartyMachine(verbose=False)

        philosophers = machine._select_philosophers(
            theme=PhilosophicalTheme.ETHICS,
            mood=PartyMood.CALM,
            size=8,
        )

        assert len(philosophers) == 8
        # Should have some philosophers from harmonious clusters
        all_harmonious = [p for cluster in HARMONIOUS_CLUSTERS.values() for p in cluster]
        assert any(p in all_harmonious for p in philosophers)


class TestTensionAndEmergence:
    """Test tension and emergence estimation."""

    def test_estimate_tension_returns_valid_range(self):
        """Test that tension is in valid range [0, 1]."""
        machine = PhilosopherPartyMachine(verbose=False)

        tension = machine._estimate_tension(
            philosophers=["aristotle", "nietzsche", "sartre"],
            mood=PartyMood.BALANCED,
        )

        assert 0.0 <= tension <= 1.0

    def test_estimate_tension_higher_for_chaotic(self):
        """Test that chaotic mood produces higher tension."""
        machine = PhilosopherPartyMachine(verbose=False)

        philosophers = ["kant", "nietzsche", "aristotle", "derrida"]

        tension_calm = machine._estimate_tension(philosophers, PartyMood.CALM)
        tension_chaotic = machine._estimate_tension(philosophers, PartyMood.CHAOTIC)

        assert tension_chaotic > tension_calm

    def test_estimate_tension_detects_high_tension_pairs(self):
        """Test that high tension pairs are detected."""
        machine = PhilosopherPartyMachine(verbose=False)

        # Include multiple high tension pairs
        philosophers = ["kant", "nietzsche", "confucius", "sartre"]

        tension = machine._estimate_tension(philosophers, PartyMood.BALANCED)

        # Should have non-zero tension due to pairs
        assert tension > 0.0

    def test_estimate_emergence_returns_valid_range(self):
        """Test that emergence is in valid range [0, 1]."""
        machine = PhilosopherPartyMachine(verbose=False)

        emergence = machine._estimate_emergence(
            philosophers=["aristotle", "nietzsche", "sartre"],
            tension=0.7,
        )

        assert 0.0 <= emergence <= 1.0

    def test_estimate_emergence_higher_with_more_tension(self):
        """Test that higher tension correlates with higher emergence."""
        machine = PhilosopherPartyMachine(verbose=False)

        philosophers = ["aristotle", "nietzsche", "sartre", "kant"]

        emergence_low_tension = machine._estimate_emergence(philosophers, 0.2)
        emergence_high_tension = machine._estimate_emergence(philosophers, 0.8)

        # Higher tension should generally lead to higher emergence
        assert emergence_high_tension >= emergence_low_tension


class TestConfigGeneration:
    """Test config generation and reasoning."""

    def test_config_has_all_fields(self):
        """Test that generated config has all required fields."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert hasattr(config, "theme")
        assert hasattr(config, "mood")
        assert hasattr(config, "philosophers")
        assert hasattr(config, "expected_size")
        assert hasattr(config, "expected_tension")
        assert hasattr(config, "expected_emergence")
        assert hasattr(config, "reasoning")

    def test_config_expected_size_matches_philosophers(self):
        """Test that expected size matches actual philosopher count."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config.expected_size == len(config.philosophers)

    def test_config_reasoning_not_empty(self):
        """Test that reasoning is generated."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config.reasoning is not None
        assert len(config.reasoning) > 0


class TestMultipleMoods:
    """Test behavior with different moods."""

    def test_calm_mood_produces_valid_config(self):
        """Test calm mood."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CALM)

        assert config.mood == PartyMood.CALM
        assert len(config.philosophers) >= 4

    def test_balanced_mood_produces_valid_config(self):
        """Test balanced mood."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config.mood == PartyMood.BALANCED
        assert len(config.philosophers) >= 8

    def test_chaotic_mood_produces_valid_config(self):
        """Test chaotic mood."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CHAOTIC)

        assert config.mood == PartyMood.CHAOTIC
        assert len(config.philosophers) >= 15

    def test_critical_mood_produces_valid_config(self):
        """Test critical mood."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.CRITICAL)

        assert config.mood == PartyMood.CRITICAL


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_suggest_party_with_verbose_false(self):
        """Test that verbose=False suppresses output."""
        machine = PhilosopherPartyMachine(verbose=False)

        # Should not raise any errors
        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config is not None

    def test_suggest_party_all_themes(self):
        """Test party suggestion for all themes."""
        machine = PhilosopherPartyMachine(verbose=False)

        for theme in PhilosophicalTheme:
            config = machine.suggest_party(theme=theme.value, mood=PartyMood.BALANCED)
            assert config is not None
            assert len(config.philosophers) > 0

    def test_suggest_party_all_moods(self):
        """Test party suggestion for all moods."""
        machine = PhilosopherPartyMachine(verbose=False)

        for mood in PartyMood:
            config = machine.suggest_party(theme="ethics", mood=mood)
            assert config is not None
            assert len(config.philosophers) > 0

    def test_philosopher_selection_respects_available_list(self):
        """Test that selection only uses available philosophers."""
        machine = PhilosopherPartyMachine(verbose=False)

        config = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        # All selected philosophers should be in available list
        for philosopher in config.philosophers:
            assert philosopher in machine.available_philosophers


class TestResearchBasedData:
    """Test research-based data structures."""

    def test_optimal_4_combos_exist(self):
        """Test that optimal 4-philosopher combos exist."""
        assert len(OPTIMAL_4_COMBOS) > 0
        assert PhilosophicalTheme.ETHICS in OPTIMAL_4_COMBOS

    def test_optimal_4_combos_have_4_philosophers(self):
        """Test that optimal combos have exactly 4 philosophers."""
        for theme, combos in OPTIMAL_4_COMBOS.items():
            for combo in combos:
                assert len(combo) == 4

    def test_high_tension_pairs_exist(self):
        """Test that high tension pairs are defined."""
        assert len(HIGH_TENSION_PAIRS) > 0
        assert all(len(pair) == 2 for pair in HIGH_TENSION_PAIRS)

    def test_harmonious_clusters_exist(self):
        """Test that harmonious clusters are defined."""
        assert len(HARMONIOUS_CLUSTERS) > 0
        assert "continental" in HARMONIOUS_CLUSTERS
        assert "analytic" in HARMONIOUS_CLUSTERS
        assert "eastern" in HARMONIOUS_CLUSTERS


class TestDeterminism:
    """Test deterministic behavior where applicable."""

    def test_same_seed_produces_same_result(self):
        """Test that same random seed produces same result."""
        import random

        machine = PhilosopherPartyMachine(verbose=False)

        # Test with fixed seed
        random.seed(42)
        config1 = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        random.seed(42)
        config2 = machine.suggest_party(theme="ethics", mood=PartyMood.BALANCED)

        assert config1.philosophers == config2.philosophers
        assert config1.expected_size == config2.expected_size
