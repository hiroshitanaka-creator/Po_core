"""Tests for experiment analyzer."""

import tempfile
from pathlib import Path
from typing import Dict

import pytest

from po_core.domain.experiment import (
    ExperimentDefinition,
    ExperimentSample,
    ExperimentVariant,
)
from po_core.experiments.analyzer import ExperimentAnalyzer
from po_core.experiments.storage import ExperimentStorage


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def storage(temp_dir):
    """Create an ExperimentStorage instance."""
    return ExperimentStorage(str(temp_dir))


@pytest.fixture
def analyzer(storage):
    """Create an ExperimentAnalyzer instance."""
    return ExperimentAnalyzer(storage)


@pytest.fixture
def sample_experiment(storage):
    """Create a sample experiment with data."""
    definition = ExperimentDefinition(
        id="test_exp",
        description="Test experiment",
        baseline=ExperimentVariant(
            name="baseline",
            config_path="configs/baseline.yaml",
        ),
        variants=[
            ExperimentVariant(
                name="variant_a",
                config_path="configs/variant_a.yaml",
            ),
        ],
        metrics=["metric1", "metric2"],
        sample_size=20,
        significance_level=0.05,
    )

    storage.save_definition(definition)

    # Add samples with clear difference for variant_a
    for i in range(20):
        # Baseline: mean ~0.5
        storage.append_sample(
            "test_exp",
            ExperimentSample(
                experiment_id="test_exp",
                input_id=f"input_{i}",
                variant_name="baseline",
                metrics={
                    "metric1": 0.5 + (i % 5) * 0.02,  # 0.5 to 0.58
                    "metric2": 0.8 + (i % 3) * 0.01,  # 0.8 to 0.82
                },
            ),
        )

        # Variant A: mean ~0.7 (significantly higher)
        storage.append_sample(
            "test_exp",
            ExperimentSample(
                experiment_id="test_exp",
                input_id=f"input_{i}",
                variant_name="variant_a",
                metrics={
                    "metric1": 0.7 + (i % 5) * 0.02,  # 0.7 to 0.78
                    "metric2": 0.6 + (i % 3) * 0.01,  # 0.6 to 0.62
                },
            ),
        )

    return "test_exp"


def test_analyze_computes_statistics(analyzer, sample_experiment):
    """Test that analyzer computes correct statistics."""
    analysis = analyzer.analyze(sample_experiment)

    assert analysis is not None
    assert "baseline" in analysis.variant_statistics
    assert "variant_a" in analysis.variant_statistics

    baseline_stats = analysis.variant_statistics["baseline"]
    assert "metric1" in baseline_stats.metric_stats
    assert "metric2" in baseline_stats.metric_stats

    # Check that means are approximately correct
    metric1_stats = baseline_stats.metric_stats["metric1"]
    assert 0.5 <= metric1_stats["mean"] <= 0.6
    assert metric1_stats["n"] == 20


def test_analyze_detects_significant_difference(analyzer, sample_experiment):
    """Test that analyzer detects significant differences."""
    analysis = analyzer.analyze(sample_experiment)

    # Should find significant difference for metric1
    metric1_tests = [t for t in analysis.significance_tests if t.metric_name == "metric1"]
    assert len(metric1_tests) == 1

    test = metric1_tests[0]
    assert test.variant_mean > test.baseline_mean
    assert test.delta > 0
    # With such a clear difference (0.5 vs 0.7), should be significant
    assert test.p_value < 0.05
    assert test.is_significant


def test_analyze_determines_winner(analyzer, sample_experiment):
    """Test that analyzer determines correct winner."""
    analysis = analyzer.analyze(sample_experiment)

    # variant_a should be the winner (higher metric1)
    assert analysis.winner == "variant_a"
    assert analysis.recommendation == "promote"


def test_analyze_no_significant_difference():
    """Test analyzer when there's no significant difference."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = ExperimentStorage(tmpdir)
        analyzer = ExperimentAnalyzer(storage)

        # Create experiment with no difference
        definition = ExperimentDefinition(
            id="no_diff_exp",
            description="No difference experiment",
            baseline=ExperimentVariant(
                name="baseline",
                config_path="configs/baseline.yaml",
            ),
            variants=[
                ExperimentVariant(
                    name="variant_a",
                    config_path="configs/variant_a.yaml",
                ),
            ],
            metrics=["metric1"],
            sample_size=20,
            significance_level=0.05,
        )

        storage.save_definition(definition)

        # Add samples with same mean
        for i in range(20):
            storage.append_sample(
                "no_diff_exp",
                ExperimentSample(
                    experiment_id="no_diff_exp",
                    input_id=f"input_{i}",
                    variant_name="baseline",
                    metrics={"metric1": 0.5 + (i % 5) * 0.02},
                ),
            )
            storage.append_sample(
                "no_diff_exp",
                ExperimentSample(
                    experiment_id="no_diff_exp",
                    input_id=f"input_{i}",
                    variant_name="variant_a",
                    metrics={"metric1": 0.5 + (i % 5) * 0.02},
                ),
            )

        analysis = analyzer.analyze("no_diff_exp")

        # Should not be significant
        assert not analysis.significance_tests[0].is_significant
        assert analysis.winner == "baseline"
        assert analysis.recommendation == "keep_baseline"


def test_analyze_multiple_variants():
    """Test analyzer with multiple variants."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = ExperimentStorage(tmpdir)
        analyzer = ExperimentAnalyzer(storage)

        definition = ExperimentDefinition(
            id="multi_var_exp",
            description="Multiple variants",
            baseline=ExperimentVariant(
                name="baseline",
                config_path="configs/baseline.yaml",
            ),
            variants=[
                ExperimentVariant(
                    name="variant_a",
                    config_path="configs/variant_a.yaml",
                ),
                ExperimentVariant(
                    name="variant_b",
                    config_path="configs/variant_b.yaml",
                ),
            ],
            metrics=["metric1"],
            sample_size=20,
        )

        storage.save_definition(definition)

        # Add samples: baseline=0.5, variant_a=0.6, variant_b=0.75 (best)
        for i in range(20):
            storage.append_sample(
                "multi_var_exp",
                ExperimentSample(
                    experiment_id="multi_var_exp",
                    input_id=f"input_{i}",
                    variant_name="baseline",
                    metrics={"metric1": 0.5 + (i % 5) * 0.01},
                ),
            )
            storage.append_sample(
                "multi_var_exp",
                ExperimentSample(
                    experiment_id="multi_var_exp",
                    input_id=f"input_{i}",
                    variant_name="variant_a",
                    metrics={"metric1": 0.6 + (i % 5) * 0.01},
                ),
            )
            storage.append_sample(
                "multi_var_exp",
                ExperimentSample(
                    experiment_id="multi_var_exp",
                    input_id=f"input_{i}",
                    variant_name="variant_b",
                    metrics={"metric1": 0.75 + (i % 5) * 0.01},
                ),
            )

        analysis = analyzer.analyze("multi_var_exp")

        # variant_b should win
        assert analysis.winner == "variant_b"
        # Should have tests for both variants
        assert len(analysis.significance_tests) == 2


def test_analyze_boolean_metrics():
    """Test analyzer with boolean metrics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = ExperimentStorage(tmpdir)
        analyzer = ExperimentAnalyzer(storage)

        definition = ExperimentDefinition(
            id="bool_exp",
            description="Boolean metrics",
            baseline=ExperimentVariant(
                name="baseline",
                config_path="configs/baseline.yaml",
            ),
            variants=[
                ExperimentVariant(
                    name="variant_a",
                    config_path="configs/variant_a.yaml",
                ),
            ],
            metrics=["degraded"],  # Boolean metric
            sample_size=20,
        )

        storage.save_definition(definition)

        # Baseline: 30% degraded, Variant A: 10% degraded (better)
        for i in range(20):
            storage.append_sample(
                "bool_exp",
                ExperimentSample(
                    experiment_id="bool_exp",
                    input_id=f"input_{i}",
                    variant_name="baseline",
                    metrics={"degraded": i < 6},  # 6/20 = 30%
                ),
            )
            storage.append_sample(
                "bool_exp",
                ExperimentSample(
                    experiment_id="bool_exp",
                    input_id=f"input_{i}",
                    variant_name="variant_a",
                    metrics={"degraded": i < 2},  # 2/20 = 10%
                ),
            )

        analysis = analyzer.analyze("bool_exp")

        # Should compute stats correctly (treating bool as 0/1)
        baseline_stats = analysis.variant_statistics["baseline"]
        assert 0.25 <= baseline_stats.metric_stats["degraded"]["mean"] <= 0.35
