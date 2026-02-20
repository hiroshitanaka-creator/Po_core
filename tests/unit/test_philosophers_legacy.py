"""Unit tests for philosopher modules."""

import pytest

from po_core.philosophers.derrida import Derrida
from po_core.philosophers.heidegger import Heidegger
from po_core.philosophers.nietzsche import Nietzsche
from po_core.philosophers.sartre import Sartre
from po_core.philosophers.wittgenstein import Wittgenstein

pytestmark = pytest.mark.skip(
    reason="Legacy philosopher test with outdated API expectations — to be migrated in Phase 1"
)


class TestPhilosopherBase:
    """Tests for the base Philosopher class."""

    def test_philosopher_initialization(self):
        """Test that philosopher can be initialized with name and description."""
        philosopher = Heidegger()
        assert philosopher.name == "Martin Heidegger"
        assert "Phenomenologist" in philosopher.description
        assert philosopher._context == {}

    def test_philosopher_repr(self):
        """Test philosopher string representation."""
        philosopher = Heidegger()
        repr_str = repr(philosopher)
        assert "Heidegger" in repr_str
        assert "name=" in repr_str

    def test_philosopher_str(self):
        """Test philosopher human-readable string."""
        philosopher = Heidegger()
        str_repr = str(philosopher)
        assert "🧠" in str_repr
        assert philosopher.name in str_repr


class TestHeidegger:
    """Tests for Heidegger philosopher module."""

    def test_heidegger_reason_basic(self, sample_prompt):
        """Test basic reasoning functionality."""
        heidegger = Heidegger()
        result = heidegger.reason(sample_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "key_concepts" in result
        assert "metadata" in result
        assert result["perspective"] == "Phenomenological / Existential"
        assert result["metadata"]["philosopher"] == "Martin Heidegger"

    def test_heidegger_reason_with_context(self, sample_prompt):
        """Test reasoning with additional context."""
        heidegger = Heidegger()
        context = {"previous_response": "We discussed freedom"}
        result = heidegger.reason(sample_prompt, context)

        assert "reasoning" in result
        assert isinstance(result["reasoning"], str)

    def test_heidegger_temporal_analysis(self):
        """Test Heidegger's temporal dimension analysis."""
        heidegger = Heidegger()

        # Test with past-oriented prompt
        past_prompt = "What was the meaning of existence before?"
        result = heidegger.reason(past_prompt)
        assert "temporal_dimension" in result
        assert result["temporal_dimension"]["has_past"] is True

        # Test with future-oriented prompt
        future_prompt = "What will be the meaning of existence?"
        result = heidegger.reason(future_prompt)
        assert result["temporal_dimension"]["has_future"] is True

        # Test with present-oriented prompt
        present_prompt = "What is the meaning of existence now?"
        result = heidegger.reason(present_prompt)
        assert result["temporal_dimension"]["has_present"] is True


class TestNietzsche:
    """Tests for Nietzsche philosopher module."""

    @pytest.fixture
    def nietzsche(self):
        """Fixture to create Nietzsche instance."""
        return Nietzsche()

    def test_nietzsche_initialization(self, nietzsche):
        """Test Nietzsche philosopher initialization."""
        assert nietzsche.name == "Friedrich Nietzsche"
        assert (
            "Will to Power" in nietzsche.description
            or "will to power" in nietzsche.description.lower()
        )

    def test_nietzsche_reason_structure(self, nietzsche, sample_prompt):
        """Test that Nietzsche's reasoning has expected structure."""
        result = nietzsche.reason(sample_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "metadata" in result
        assert isinstance(result["reasoning"], str)
        assert len(result["reasoning"]) > 0


class TestSartre:
    """Tests for Sartre philosopher module."""

    @pytest.fixture
    def sartre(self):
        """Fixture to create Sartre instance."""
        return Sartre()

    def test_sartre_initialization(self, sartre):
        """Test Sartre philosopher initialization."""
        assert sartre.name == "Jean-Paul Sartre"
        assert (
            "Existentialism" in sartre.description
            or "existentialism" in sartre.description.lower()
        )

    def test_sartre_reason_structure(self, sartre, sample_prompt):
        """Test that Sartre's reasoning has expected structure."""
        result = sartre.reason(sample_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "metadata" in result


class TestDerrida:
    """Tests for Derrida philosopher module."""

    @pytest.fixture
    def derrida(self):
        """Fixture to create Derrida instance."""
        return Derrida()

    def test_derrida_initialization(self, derrida):
        """Test Derrida philosopher initialization."""
        assert derrida.name == "Jacques Derrida"
        assert (
            "Deconstruction" in derrida.description
            or "deconstruction" in derrida.description.lower()
        )

    def test_derrida_reason_structure(self, derrida, sample_prompt):
        """Test that Derrida's reasoning has expected structure."""
        result = derrida.reason(sample_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "metadata" in result


class TestWittgenstein:
    """Tests for Wittgenstein philosopher module."""

    @pytest.fixture
    def wittgenstein(self):
        """Fixture to create Wittgenstein instance."""
        return Wittgenstein()

    def test_wittgenstein_initialization(self, wittgenstein):
        """Test Wittgenstein philosopher initialization."""
        assert wittgenstein.name == "Ludwig Wittgenstein"

    def test_wittgenstein_reason_structure(self, wittgenstein, sample_prompt):
        """Test that Wittgenstein's reasoning has expected structure."""
        result = wittgenstein.reason(sample_prompt)

        assert "reasoning" in result
        assert "perspective" in result
        assert "metadata" in result


class TestPhilosopherInteraction:
    """Tests for interactions between multiple philosophers."""

    def test_multiple_philosophers_same_prompt(self, sample_prompt):
        """Test that different philosophers produce different analyses."""
        heidegger = Heidegger()
        nietzsche = Nietzsche()

        heidegger_result = heidegger.reason(sample_prompt)
        nietzsche_result = nietzsche.reason(sample_prompt)

        # Both should have valid results
        assert "reasoning" in heidegger_result
        assert "reasoning" in nietzsche_result

        # Different perspectives
        assert heidegger_result["perspective"] != nietzsche_result["perspective"]

    def test_philosopher_consistency(self, sample_prompt):
        """Test that same philosopher produces consistent structure."""
        philosopher = Heidegger()

        result1 = philosopher.reason(sample_prompt)
        result2 = philosopher.reason(sample_prompt)

        # Structure should be consistent
        assert set(result1.keys()) == set(result2.keys())
