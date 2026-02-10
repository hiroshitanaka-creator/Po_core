"""
Integration tests for Po_self philosophical ensemble system.

Tests the complete reasoning pipeline including:
- Multi-philosopher ensemble reasoning
- Tensor computation integration
- Reasoning trace generation
- Philosophical annotation
- Synthesis and response generation
"""

import json

import pytest

from po_core.philosophers import (
    Derrida,
    Heidegger,
    Nietzsche,
    Sartre,
    Wittgenstein,
)
from po_core.po_self import PhilosophicalEnsemble
from po_core.trace import TraceLevel


class TestPhilosophicalEnsembleInitialization:
    """Tests for PhilosophicalEnsemble initialization."""

    def test_ensemble_initialization(self):
        """Test basic ensemble initialization."""
        philosophers = [Sartre(), Nietzsche(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        assert len(ensemble.philosophers) == 3
        assert ensemble.enable_tracing is True
        assert ensemble.tracer is not None

    def test_ensemble_without_tracing(self):
        """Test ensemble without tracing enabled."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=False)

        assert ensemble.tracer is None

    def test_ensemble_with_empty_philosophers(self):
        """Test that ensemble requires at least one philosopher."""
        with pytest.raises(ValueError, match="at least one philosopher"):
            PhilosophicalEnsemble([])

    def test_ensemble_deterministic_mode(self):
        """Test ensemble in deterministic mode."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(
            philosophers, enable_tracing=False, deterministic=True
        )

        assert ensemble.deterministic is True


class TestPhilosophicalEnsembleReasoning:
    """Tests for the core reasoning functionality."""

    def test_basic_reasoning(self):
        """Test basic reasoning with single philosopher."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is freedom?")

        assert "response" in result
        assert "perspectives" in result
        assert "tensors" in result
        assert len(result["perspectives"]) == 1

    def test_multi_philosopher_reasoning(self):
        """Test reasoning with multiple philosophers."""
        philosophers = [Sartre(), Nietzsche(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is the meaning of existence?")

        assert len(result["perspectives"]) == 3
        assert result["response"] is not None
        assert "synthesis" in result

    def test_reasoning_with_context(self):
        """Test reasoning with additional context."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        context = {"previous_discussion": "We were discussing freedom"}

        result = ensemble.reason(
            "How does freedom relate to responsibility?", context=context
        )

        assert "response" in result
        # Context should influence reasoning (hard to verify programmatically)

    def test_reasoning_with_selected_philosophers(self):
        """Test reasoning with subset of philosophers."""
        philosophers = [Sartre(), Nietzsche(), Heidegger(), Wittgenstein()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "What is language?", active_philosophers=["wittgenstein", "heidegger"]
        )

        assert len(result["perspectives"]) == 2
        philosopher_names = [p["philosopher"] for p in result["perspectives"]]
        assert "wittgenstein" in philosopher_names
        assert "heidegger" in philosopher_names
        assert "sartre" not in philosopher_names

    def test_reasoning_with_invalid_philosopher(self):
        """Test that invalid philosopher name is ignored."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "Test question", active_philosophers=["nonexistent_philosopher"]
        )

        # Should fall back to all philosophers
        assert len(result["perspectives"]) == 1

    def test_reasoning_includes_tensors(self):
        """Test that reasoning result includes all tensor computations."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What should I do?")

        assert "tensors" in result
        assert "freedom_pressure" in result["tensors"]
        assert "semantic_profile" in result["tensors"]
        assert "blocked_content" in result["tensors"]

    def test_freedom_pressure_computation(self):
        """Test Freedom Pressure Tensor computation."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("Should I take this difficult ethical decision?")

        fp_data = result["tensors"]["freedom_pressure"]
        assert "data" in fp_data
        assert "summary" in fp_data
        assert len(fp_data["data"]) == 6  # 6 dimensions

    def test_semantic_profile_evolution(self):
        """Test Semantic Profile evolution tracking."""
        philosophers = [Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        # First question
        result1 = ensemble.reason("What is Being?")

        # Second question
        result2 = ensemble.reason("How does Being manifest in time?")

        sp_data = result2["tensors"]["semantic_profile"]
        assert "history_length" in sp_data
        assert sp_data["history_length"] >= 1

    def test_blocked_content_tracking(self):
        """Test that blocked content is tracked."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("Should I lie?")

        blocked_data = result["tensors"]["blocked_content"]
        assert "blocked_count" in blocked_data
        # May or may not have blocked content, just verify structure

    def test_philosophical_annotations(self):
        """Test that philosophical annotations are included."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is authentic freedom?")

        assert "annotations" in result
        # Should find some relevant concepts
        if len(result["annotations"]) > 0:
            annotation = result["annotations"][0]
            assert "concept" in annotation
            assert "definition" in annotation

    def test_reasoning_with_trace_export(self):
        """Test that reasoning includes trace export."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("Test prompt")

        assert "trace" in result
        trace = result["trace"]
        assert "session_id" in trace
        assert "entries" in trace
        assert len(trace["entries"]) > 0


class TestPhilosophicalEnsembleSynthesis:
    """Tests for response synthesis."""

    def test_synthesis_combines_perspectives(self):
        """Test that synthesis combines multiple perspectives."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers, deterministic=True)

        result = ensemble.reason("What is power?")

        assert "synthesis" in result
        synthesis = result["synthesis"]

        # Should reference both philosophers or combine their ideas
        assert len(synthesis) > 0

    def test_synthesis_with_high_confidence(self):
        """Test synthesis when perspectives have high confidence."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is freedom?")

        # Sartre should be confident about freedom
        perspective = result["perspectives"][0]
        assert "confidence" in perspective
        assert perspective["confidence"] > 0.5

    def test_synthesis_weights_by_confidence(self):
        """Test that synthesis considers confidence scores."""
        philosophers = [Sartre(), Nietzsche(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is freedom?")

        # All perspectives should have confidence scores
        for perspective in result["perspectives"]:
            assert "confidence" in perspective
            assert 0.0 <= perspective["confidence"] <= 1.0


class TestPhilosophicalEnsembleTracing:
    """Tests for reasoning trace functionality."""

    def test_trace_logs_all_stages(self):
        """Test that trace includes all reasoning stages."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("Test prompt")

        trace_entries = result["trace"]["entries"]

        # Should have entries for various stages
        events = [entry["event"] for entry in trace_entries]
        assert "reasoning_start" in events

    def test_trace_includes_philosopher_reasoning(self):
        """Test that trace includes philosopher reasoning."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("What is life?")

        trace_entries = result["trace"]["entries"]

        # Should have reasoning entries for philosophers
        reasoning_entries = [
            e for e in trace_entries if e["event"] == "philosopher_reasoning"
        ]
        assert len(reasoning_entries) >= 2

    def test_trace_includes_tensor_computations(self):
        """Test that trace includes tensor computations."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("Test")

        trace_entries = result["trace"]["entries"]

        # Should have tensor computation entries
        tensor_entries = [
            e for e in trace_entries if e["event"] == "tensor_computation"
        ]
        assert len(tensor_entries) >= 3  # FP, SP, Blocked

    def test_trace_can_be_exported(self):
        """Test that trace can be exported to JSON."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        ensemble.reason("Test")
        json_trace = ensemble.export_trace()

        # Should be valid JSON
        trace_data = json.loads(json_trace)
        assert "session_id" in trace_data
        assert "entries" in trace_data

    def test_trace_without_tracing_enabled(self):
        """Test that trace is None when tracing disabled."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=False)

        result = ensemble.reason("Test")

        assert "trace" not in result or result.get("trace") is None


class TestPhilosophicalEnsembleEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_prompt(self):
        """Test reasoning with empty prompt."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("")

        # Should still return valid structure
        assert "response" in result
        assert "perspectives" in result

    def test_very_long_prompt(self):
        """Test reasoning with very long prompt."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        long_prompt = "What is freedom? " * 100

        result = ensemble.reason(long_prompt)

        assert "response" in result

    def test_special_characters_in_prompt(self):
        """Test reasoning with special characters."""
        philosophers = [Wittgenstein()]
        ensemble = PhilosophicalEnsemble(philosophers)

        prompt = "What is 'meaning'? Does \"language\" <define> reality?"

        result = ensemble.reason(prompt)

        assert "response" in result

    def test_deterministic_reproducibility(self):
        """Test that deterministic mode produces consistent results."""
        philosophers = [Sartre()]

        ensemble1 = PhilosophicalEnsemble(
            philosophers, enable_tracing=False, deterministic=True
        )
        result1 = ensemble1.reason("What is freedom?")

        ensemble2 = PhilosophicalEnsemble(
            philosophers, enable_tracing=False, deterministic=True
        )
        result2 = ensemble2.reason("What is freedom?")

        # Should produce same response (since deterministic)
        assert result1["response"] == result2["response"]


@pytest.mark.slow
class TestPhilosophicalEnsemblePerformance:
    """Performance tests for ensemble reasoning."""

    def test_reasoning_with_all_philosophers(self):
        """Test reasoning with all available philosophers."""
        philosophers = [Sartre(), Nietzsche(), Heidegger(), Derrida(), Wittgenstein()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is truth?")

        assert len(result["perspectives"]) == 5
        assert result["response"] is not None

    def test_multiple_reasoning_rounds(self):
        """Test multiple reasoning rounds maintain consistency."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers)

        questions = [
            "What is freedom?",
            "How does freedom relate to responsibility?",
            "Can we escape freedom?",
        ]

        results = []
        for question in questions:
            result = ensemble.reason(question)
            results.append(result)

        # All should succeed
        assert len(results) == 3
        for result in results:
            assert "response" in result

        # Semantic profile should evolve
        last_sp = results[-1]["tensors"]["semantic_profile"]
        assert last_sp["history_length"] >= len(questions)


class TestPhilosophicalEnsembleCompleteness:
    """Tests for completeness of reasoning output."""

    def test_result_structure_completeness(self):
        """Test that result contains all expected fields."""
        philosophers = [Sartre(), Nietzsche(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("What is existence?")

        # Required top-level fields
        assert "prompt" in result
        assert "response" in result
        assert "synthesis" in result
        assert "perspectives" in result
        assert "tensors" in result
        assert "annotations" in result
        assert "trace" in result
        assert "metadata" in result

    def test_perspective_structure_completeness(self):
        """Test that each perspective has all required fields."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("Test")

        perspective = result["perspectives"][0]
        assert "philosopher" in perspective
        assert "response" in perspective
        assert "confidence" in perspective
        assert "reasoning" in perspective

    def test_tensor_structure_completeness(self):
        """Test that tensor outputs have complete structure."""
        philosophers = [Sartre()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("Test")

        tensors = result["tensors"]

        # Freedom Pressure
        fp = tensors["freedom_pressure"]
        assert "name" in fp
        assert "data" in fp
        assert "dimensions" in fp
        assert "dimension_names" in fp

        # Semantic Profile
        sp = tensors["semantic_profile"]
        assert "name" in sp
        assert "data" in sp
        assert "history_length" in sp

        # Blocked Content
        bc = tensors["blocked_content"]
        assert "name" in bc
        assert "blocked_count" in bc

    def test_metadata_completeness(self):
        """Test that metadata includes all expected information."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers, enable_tracing=True)

        result = ensemble.reason("Test")

        metadata = result["metadata"]
        assert "timestamp" in metadata
        assert "philosophers_count" in metadata
        assert "active_philosophers" in metadata
        assert "tracing_enabled" in metadata


class TestPhilosophicalEnsembleRealWorldScenarios:
    """Tests simulating real-world usage scenarios."""

    def test_existential_question(self):
        """Test handling existential philosophical question."""
        philosophers = [Sartre(), Heidegger(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "I feel overwhelmed by the choices I have to make. "
            "How can I navigate this freedom authentically?"
        )

        assert result["response"] is not None
        # Should have high freedom pressure
        fp = result["tensors"]["freedom_pressure"]["summary"]["total_pressure"]
        assert fp > 0.0

    def test_language_philosophy_question(self):
        """Test handling philosophy of language question."""
        philosophers = [Wittgenstein(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "How does language shape our understanding of reality?"
        )

        assert result["response"] is not None
        # Wittgenstein should be involved
        philosophers_involved = [p["philosopher"] for p in result["perspectives"]]
        assert "wittgenstein" in philosophers_involved

    def test_ethical_dilemma(self):
        """Test handling ethical dilemma."""
        philosophers = [Sartre(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "Is it ever acceptable to lie if it protects someone from harm?"
        )

        assert result["response"] is not None
        # Should have high ethical stakes in freedom pressure
        fp_data = result["tensors"]["freedom_pressure"]
        ethical_idx = fp_data["dimension_names"].index("ethical_stakes")
        assert fp_data["data"][ethical_idx] > 0.3

    def test_deconstruction_question(self):
        """Test handling deconstruction/postmodern question."""
        philosophers = [Derrida(), Nietzsche()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason("What is the center? Can meaning be fixed?")

        assert result["response"] is not None
        # Derrida should be active
        philosophers_involved = [p["philosopher"] for p in result["perspectives"]]
        assert "derrida" in philosophers_involved

    def test_practical_wisdom_question(self):
        """Test handling practical wisdom question."""
        philosophers = [Sartre(), Nietzsche(), Heidegger()]
        ensemble = PhilosophicalEnsemble(philosophers)

        result = ensemble.reason(
            "How should I live my life in a way that is both authentic and meaningful?"
        )

        assert result["response"] is not None
        assert len(result["perspectives"]) > 0

        # Should have annotations related to authenticity or meaning
        if len(result["annotations"]) > 0:
            concepts = [a["concept"] for a in result["annotations"]]
            # May contain authenticity, being, freedom, etc.
            assert len(concepts) > 0
