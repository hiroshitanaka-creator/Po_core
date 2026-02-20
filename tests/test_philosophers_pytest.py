"""
Pytest: All 39 Philosophers
===========================

Pytest-compatible test suite for all 39 philosopher modules.
Run with: pytest tests/test_philosophers_pytest.py -v
"""

import pytest

# All 39 philosophers in the registry
PHILOSOPHER_KEYS = [
    "aristotle",
    "plato",
    "parmenides",
    "peirce",
    "kant",
    "hegel",
    "husserl",
    "heidegger",
    "schopenhauer",
    "merleau_ponty",
    "descartes",
    "spinoza",
    "kierkegaard",
    "nietzsche",
    "sartre",
    "derrida",
    "deleuze",
    "foucault",
    "badiou",
    "lacan",
    "beauvoir",
    "butler",
    "levinas",
    "arendt",
    "jonas",
    "weil",
    "marcus_aurelius",
    "epicurus",
    "wittgenstein",
    "dewey",
    "jung",
    "confucius",
    "zhuangzi",
    "laozi",
    "watsuji",
    "nishida",
    "dogen",
    "nagarjuna",
    "wabi_sabi",
]


TEST_PROMPT = "What is the nature of consciousness and how should we understand it?"


@pytest.fixture
def philosopher_registry():
    """Load the philosopher registry."""
    from po_core.ensemble import PHILOSOPHER_REGISTRY

    return PHILOSOPHER_REGISTRY


class TestPhilosopherRegistry:
    """Test the philosopher registry."""

    def test_registry_count(self, philosopher_registry):
        """Test that registry contains expected number of philosophers."""
        assert (
            len(philosopher_registry) == 39
        ), f"Expected 39 philosophers, got {len(philosopher_registry)}"

    def test_all_keys_present(self, philosopher_registry):
        """Test that all expected keys are in registry."""
        for key in PHILOSOPHER_KEYS:
            assert key in philosopher_registry, f"Missing philosopher: {key}"


class TestPhilosopherInstantiation:
    """Test philosopher instantiation."""

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_instantiation(self, philosopher_registry, key):
        """Test that each philosopher can be instantiated."""
        philosopher_class = philosopher_registry[key]
        philosopher = philosopher_class()

        assert philosopher is not None
        assert hasattr(philosopher, "name")
        assert hasattr(philosopher, "tradition")
        assert hasattr(philosopher, "key_concepts")
        assert hasattr(philosopher, "reason")

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_has_name(self, philosopher_registry, key):
        """Test that each philosopher has a non-empty name."""
        philosopher = philosopher_registry[key]()
        assert philosopher.name, f"Philosopher {key} has no name"

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_has_tradition(self, philosopher_registry, key):
        """Test that each philosopher has a non-empty tradition."""
        philosopher = philosopher_registry[key]()
        assert philosopher.tradition, f"Philosopher {key} has no tradition"

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_has_key_concepts(self, philosopher_registry, key):
        """Test that each philosopher has key concepts."""
        philosopher = philosopher_registry[key]()
        assert philosopher.key_concepts, f"Philosopher {key} has no key concepts"
        assert (
            len(philosopher.key_concepts) >= 3
        ), f"Philosopher {key} should have at least 3 key concepts"


class TestPhilosopherReasoning:
    """Test philosopher reasoning."""

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_reason_returns_dict(self, philosopher_registry, key):
        """Test that reason() returns a dictionary."""
        philosopher = philosopher_registry[key]()
        result = philosopher.reason(TEST_PROMPT)

        assert isinstance(
            result, dict
        ), f"Philosopher {key} reason() should return dict"

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_reason_has_required_fields(self, philosopher_registry, key):
        """Test that reason() returns required fields."""
        philosopher = philosopher_registry[key]()
        result = philosopher.reason(TEST_PROMPT)

        required_fields = ["reasoning", "perspective"]
        for field in required_fields:
            assert field in result, f"Philosopher {key} missing field: {field}"

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_reason_non_empty(self, philosopher_registry, key):
        """Test that reason() returns non-empty reasoning."""
        philosopher = philosopher_registry[key]()
        result = philosopher.reason(TEST_PROMPT)

        assert result["reasoning"], f"Philosopher {key} returned empty reasoning"
        assert (
            len(result["reasoning"]) > 20
        ), f"Philosopher {key} reasoning too short: {len(result['reasoning'])} chars"

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_reason_has_perspective(self, philosopher_registry, key):
        """Test that reason() returns non-empty perspective."""
        philosopher = philosopher_registry[key]()
        result = philosopher.reason(TEST_PROMPT)

        assert result["perspective"], f"Philosopher {key} returned empty perspective"


class TestPhilosopherMetadata:
    """Test philosopher metadata in reasoning results."""

    @pytest.mark.parametrize("key", PHILOSOPHER_KEYS)
    def test_philosopher_has_metadata(self, philosopher_registry, key):
        """Test that reason() includes metadata."""
        philosopher = philosopher_registry[key]()
        result = philosopher.reason(TEST_PROMPT)

        # Many philosophers include metadata, but it's not strictly required
        if "metadata" in result:
            assert isinstance(result["metadata"], dict)


class TestRunAPI:
    """Test the run_turn pipeline via po_core.run()."""

    def test_run_returns_ok(self):
        """Test po_core.run() returns ok status."""
        from po_core import run

        result = run(user_input="What is the meaning of existence?")
        assert result["status"] == "ok"
        assert "proposal" in result

    def test_run_has_request_id(self):
        """Test po_core.run() returns request_id."""
        from po_core import run

        result = run(user_input="What is truth?")
        assert "request_id" in result
        assert isinstance(result["request_id"], str)


class TestPhilosopherDiversity:
    """Test diversity of philosophical perspectives."""

    def test_unique_perspectives(self, philosopher_registry):
        """Test that philosophers have unique perspectives."""
        perspectives = []
        for key in PHILOSOPHER_KEYS:
            philosopher = philosopher_registry[key]()
            result = philosopher.reason(TEST_PROMPT)
            perspectives.append(result["perspective"])

        # Most perspectives should be unique
        unique_count = len(set(perspectives))
        assert (
            unique_count >= 30
        ), f"Expected at least 30 unique perspectives, got {unique_count}"

    def test_reasoning_diversity(self, philosopher_registry):
        """Test that philosophers produce diverse reasoning."""
        reasonings = []
        for key in PHILOSOPHER_KEYS:
            philosopher = philosopher_registry[key]()
            result = philosopher.reason(TEST_PROMPT)
            reasonings.append(result["reasoning"][:200])  # First 200 chars

        # All reasonings should be different
        unique_count = len(set(reasonings))
        assert unique_count == len(
            reasonings
        ), "Some philosophers produced identical reasoning"


# Convenience function for running tests directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
