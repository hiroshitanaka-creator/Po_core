"""
Integration Tests for Po_core Prototypes

Tests for the working prototypes:
- Web API Server
- Batch Analyzer
- Philosopher Comparison Tool
"""

import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skip(
    reason="Legacy BatchAnalyzer/PhilosopherComparison API removed in run_turn migration — to be migrated in Phase 1"
)


# Add examples directory to path for imports
examples_dir = Path(__file__).parent.parent.parent / "examples"
sys.path.insert(0, str(examples_dir))


class TestBatchAnalyzer:
    """Test batch_analyzer prototype."""

    def test_import_batch_analyzer(self):
        """Test that batch_analyzer can be imported."""
        from batch_analyzer import BatchAnalyzer

        assert BatchAnalyzer is not None

    def test_batch_analyzer_initialization(self):
        """Test BatchAnalyzer initializes correctly."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer()
        assert analyzer.po_self is not None
        assert analyzer.results == []

    def test_batch_analyzer_with_custom_philosophers(self):
        """Test BatchAnalyzer with custom philosophers."""
        from batch_analyzer import BatchAnalyzer

        philosophers = ["aristotle", "nietzsche"]
        analyzer = BatchAnalyzer(philosophers=philosophers)
        assert analyzer.po_self.philosophers == philosophers

    def test_analyze_single_prompt(self):
        """Test analyzing a single prompt."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        prompts = ["What is virtue?"]

        results = analyzer.analyze_batch(prompts, show_progress=False)

        assert len(results) == 1
        assert results[0]["prompt"] == "What is virtue?"
        assert "consensus_leader" in results[0]
        assert "metrics" in results[0]

    def test_analyze_multiple_prompts(self):
        """Test analyzing multiple prompts."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        prompts = ["What is virtue?", "What is justice?", "What is wisdom?"]

        results = analyzer.analyze_batch(prompts, show_progress=False)

        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["prompt"] == prompts[i]

    def test_generate_report(self):
        """Test generating analysis report."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        prompts = ["What is virtue?", "What is justice?"]

        analyzer.analyze_batch(prompts, show_progress=False)
        report = analyzer.generate_report()

        assert report.total_prompts == 2
        assert report.total_philosophers_used > 0
        assert "freedom_pressure" in report.average_metrics
        assert len(report.leader_distribution) > 0

    def test_export_json_format(self):
        """Test exporting results as JSON."""
        import json

        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        prompts = ["What is truth?"]

        analyzer.analyze_batch(prompts, show_progress=False)
        json_str = analyzer.export_json()

        # Should be valid JSON
        data = json.loads(json_str)
        assert data["total_prompts"] == 1
        assert "average_metrics" in data
        assert "results" in data

    def test_export_csv_format(self):
        """Test exporting results as CSV."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        prompts = ["What is beauty?"]

        analyzer.analyze_batch(prompts, show_progress=False)
        csv_str = analyzer.export_csv()

        # Should contain CSV header and data
        assert "Prompt" in csv_str
        assert "Consensus Leader" in csv_str
        assert "What is beauty?" in csv_str


class TestPhilosopherComparison:
    """Test philosopher_comparison prototype."""

    def test_import_philosopher_comparison(self):
        """Test that philosopher_comparison can be imported."""
        from philosopher_comparison import PhilosopherComparison

        assert PhilosopherComparison is not None

    def test_philosopher_comparison_initialization(self):
        """Test PhilosopherComparison initializes correctly."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()
        assert comparison.PHILOSOPHER_GROUPS is not None
        assert len(comparison.PHILOSOPHER_GROUPS) > 0

    def test_predefined_groups_exist(self):
        """Test that predefined philosopher groups exist."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()

        expected_groups = [
            "実存主義",
            "古典哲学",
            "現代哲学",
            "倫理学",
            "東洋哲学",
            "西洋哲学",
        ]

        for group in expected_groups:
            assert group in comparison.PHILOSOPHER_GROUPS
            assert len(comparison.PHILOSOPHER_GROUPS[group]) > 0

    def test_compare_two_groups(self):
        """Test comparing two philosopher groups."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()
        prompt = "What is virtue?"

        # Compare existentialism vs classical philosophy
        comparison.compare_groups(
            prompt=prompt, groups=["実存主義", "古典哲学"], verbose=False
        )

        # Should have responses for both groups
        assert len(comparison.responses) == 2
        assert "実存主義" in comparison.responses
        assert "古典哲学" in comparison.responses

    def test_compare_individual_philosophers(self):
        """Test comparing individual philosophers."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()
        prompt = "What is freedom?"
        philosophers = ["aristotle", "nietzsche", "sartre"]

        comparison.compare_philosophers(
            prompt=prompt, philosophers=philosophers, verbose=False
        )

        # Should have responses for all philosophers
        assert len(comparison.individual_responses) == len(philosophers)

    def test_comparison_stores_results(self):
        """Test that comparison stores results properly."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()
        comparison.compare_groups(
            prompt="What is truth?", groups=["倫理学"], verbose=False
        )

        assert "倫理学" in comparison.responses
        response_data = comparison.responses["倫理学"]

        assert "response" in response_data
        assert "philosophers" in response_data
        assert response_data["response"].prompt == "What is truth?"


class TestWebAPIServer:
    """Test web_api_server prototype structure."""

    def test_import_web_api_server(self):
        """Test that web_api_server can be imported."""
        from web_api_server import app

        assert app is not None

    def test_app_is_fastapi(self):
        """Test that app is a FastAPI instance."""
        from fastapi import FastAPI
        from web_api_server import app

        assert isinstance(app, FastAPI)

    def test_po_self_instance_exists(self):
        """Test that Po_self instance is created."""
        from web_api_server import po_self

        assert po_self is not None

    def test_sessions_storage_exists(self):
        """Test that sessions storage exists."""
        from web_api_server import sessions

        assert sessions is not None
        assert isinstance(sessions, dict)


class TestPrototypeIntegration:
    """Test integration between prototypes and core modules."""

    def test_batch_analyzer_uses_po_self(self):
        """Test that BatchAnalyzer uses Po_self correctly."""
        from batch_analyzer import BatchAnalyzer

        from po_core.po_self import PoSelf

        analyzer = BatchAnalyzer()
        assert isinstance(analyzer.po_self, PoSelf)

    def test_philosopher_comparison_uses_po_self(self):
        """Test that PhilosopherComparison uses Po_self correctly."""
        from philosopher_comparison import PhilosopherComparison

        from po_core.po_self import PoSelf

        comparison = PhilosopherComparison()

        # Run a comparison to create Po_self instance
        comparison.compare_groups(prompt="Test", groups=["倫理学"], verbose=False)

        # Check that responses use Po_self
        assert len(comparison.responses) > 0

    def test_prototypes_produce_consistent_structure(self):
        """Test that all prototypes produce consistent data structures."""
        from batch_analyzer import BatchAnalyzer
        from philosopher_comparison import PhilosopherComparison

        # Test BatchAnalyzer
        analyzer = BatchAnalyzer(philosophers=["aristotle"])
        batch_results = analyzer.analyze_batch(["What is virtue?"], show_progress=False)

        assert "prompt" in batch_results[0]
        assert "metrics" in batch_results[0]
        assert "freedom_pressure" in batch_results[0]["metrics"]

        # Test PhilosopherComparison
        comparison = PhilosopherComparison()
        comparison.compare_groups(
            prompt="What is virtue?", groups=["倫理学"], verbose=False
        )

        response = comparison.responses["倫理学"]["response"]
        assert hasattr(response, "metrics")
        assert "freedom_pressure" in response.metrics


class TestPrototypeErrorHandling:
    """Test error handling in prototypes."""

    def test_batch_analyzer_empty_prompts(self):
        """Test BatchAnalyzer with empty prompts list."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer()
        results = analyzer.analyze_batch([], show_progress=False)

        assert len(results) == 0

    def test_batch_analyzer_report_before_analysis(self):
        """Test generating report before running analysis."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer()
        report = analyzer.generate_report()

        assert report.total_prompts == 0
        assert len(report.leader_distribution) == 0

    def test_comparison_with_invalid_group(self):
        """Test comparison with non-existent group."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()

        # Should handle gracefully (might skip or use all groups)
        try:
            comparison.compare_groups(
                prompt="Test", groups=["NonExistentGroup"], verbose=False
            )
            # If it doesn't raise, check that it handled it
            assert True
        except (KeyError, ValueError):
            # It's also acceptable to raise an error
            assert True


class TestPrototypeUsability:
    """Test usability features of prototypes."""

    def test_batch_analyzer_progress_disabled(self):
        """Test that progress can be disabled."""
        from batch_analyzer import BatchAnalyzer

        analyzer = BatchAnalyzer()
        # Should not raise error when progress is disabled
        results = analyzer.analyze_batch(["What is truth?"], show_progress=False)

        assert len(results) == 1

    def test_comparison_verbose_disabled(self):
        """Test that verbose output can be disabled."""
        from philosopher_comparison import PhilosopherComparison

        comparison = PhilosopherComparison()
        # Should not raise error when verbose is disabled
        comparison.compare_groups(
            prompt="What is beauty?", groups=["古典哲学"], verbose=False
        )

        assert len(comparison.responses) > 0
