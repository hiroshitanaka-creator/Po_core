"""Tests for experiment analyzer."""

import tempfile
from datetime import datetime, timezone
from pathlib import Path

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


def _make_sample(variant_name, metrics, i=0):
    """Helper to create an ExperimentSample."""
    return ExperimentSample(
        request_id=f"req_{variant_name}_{i}",
        variant_name=variant_name,
        metrics=metrics,
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def sample_experiment(storage):
    """Create a sample experiment with data showing significant difference."""
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

    for i in range(20):
        # Baseline: metric1 mean ~0.5, metric2 mean ~0.8
        storage.append_sample("test_exp", _make_sample(
            "baseline",
            {"metric1": 0.5 + (i % 5) * 0.02, "metric2": 0.8 + (i % 3) * 0.01},
            i,
        ))
        # Variant A: metric1 mean ~0.7, metric2 mean ~0.6
        storage.append_sample("test_exp", _make_sample(
            "variant_a",
            {"metric1": 0.7 + (i % 5) * 0.02, "metric2": 0.6 + (i % 3) * 0.01},
            i,
        ))

    return "test_exp"


def test_analyze_computes_statistics(analyzer, sample_experiment):
    """Test that analyzer computes correct statistics."""
    analysis = analyzer.analyze(sample_experiment)

    assert analysis is not None
    assert analysis.baseline_stats.variant_name == "baseline"
    assert len(analysis.variant_stats) == 1
    assert analysis.variant_stats[0].variant_name == "variant_a"

    # Check baseline stats
    baseline_m1 = analysis.baseline_stats.metrics["metric1"]
    assert 0.5 <= baseline_m1["mean"] <= 0.6
    assert baseline_m1["n"] == 20


def test_analyze_detects_significant_difference(analyzer, sample_experiment):
    """Test that analyzer detects significant differences."""
    analysis = analyzer.analyze(sample_experiment)

    # Find metric1 tests
    metric1_tests = [t for t in analysis.significance_tests if t.metric_name == "metric1"]
    assert len(metric1_tests) == 1

    test = metric1_tests[0]
    assert test.variant_mean > test.baseline_mean
    assert test.delta > 0
    assert test.p_value < 0.05
    assert test.is_significant


def test_analyze_effect_size(analyzer, sample_experiment):
    """Test that effect size is computed."""
    analysis = analyzer.analyze(sample_experiment)

    metric1_tests = [t for t in analysis.significance_tests if t.metric_name == "metric1"]
    assert len(metric1_tests) == 1
    assert metric1_tests[0].effect_size is not None
    assert metric1_tests[0].effect_size > 0


def test_analyze_no_significant_difference():
    """Test analyzer when there's no significant difference."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = ExperimentStorage(tmpdir)
        analyzer = ExperimentAnalyzer(storage)

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

        for i in range(20):
            storage.append_sample("no_diff_exp", _make_sample(
                "baseline", {"metric1": 0.5 + (i % 5) * 0.02}, i,
            ))
            storage.append_sample("no_diff_exp", _make_sample(
                "variant_a", {"metric1": 0.5 + (i % 5) * 0.02}, i,
            ))

        analysis = analyzer.analyze("no_diff_exp")

        assert not analysis.significance_tests[0].is_significant
        assert analysis.winner is None
        assert analysis.recommendation == "continue"


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

        for i in range(20):
            storage.append_sample("multi_var_exp", _make_sample(
                "baseline", {"metric1": 0.5 + (i % 5) * 0.01}, i,
            ))
            storage.append_sample("multi_var_exp", _make_sample(
                "variant_a", {"metric1": 0.6 + (i % 5) * 0.01}, i,
            ))
            storage.append_sample("multi_var_exp", _make_sample(
                "variant_b", {"metric1": 0.75 + (i % 5) * 0.01}, i,
            ))

        analysis = analyzer.analyze("multi_var_exp")

        # variant_b should win (highest improvement)
        assert analysis.winner == "variant_b"
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
            metrics=["degraded"],
            sample_size=20,
        )

        storage.save_definition(definition)

        for i in range(20):
            storage.append_sample("bool_exp", _make_sample(
                "baseline", {"degraded": i < 6}, i,  # 30% degraded
            ))
            storage.append_sample("bool_exp", _make_sample(
                "variant_a", {"degraded": i < 2}, i,  # 10% degraded
            ))

        analysis = analyzer.analyze("bool_exp")

        baseline_stats = analysis.baseline_stats.metrics["degraded"]
        assert 0.25 <= baseline_stats["mean"] <= 0.35


def test_analyze_nonexistent_experiment(analyzer):
    """Test analyzer raises for non-existent experiment."""
    with pytest.raises(ValueError, match="not found"):
        analyzer.analyze("nonexistent")


def test_analyze_no_samples(storage, analyzer):
    """Test analyzer raises for experiment with no samples."""
    definition = ExperimentDefinition(
        id="empty_exp",
        description="Empty",
        baseline=ExperimentVariant(name="baseline", config_path="c.yaml"),
        variants=[ExperimentVariant(name="v", config_path="v.yaml")],
        metrics=["m"],
    )
    storage.save_definition(definition)

    with pytest.raises(ValueError, match="No samples found"):
        analyzer.analyze("empty_exp")


def test_analyze_round_trip_with_storage(analyzer, storage, sample_experiment):
    """Test that analysis can be saved and loaded back correctly."""
    analysis = analyzer.analyze(sample_experiment)
    storage.save_analysis(analysis)

    loaded = storage.load_analysis(sample_experiment)
    assert loaded is not None
    assert loaded.experiment_id == analysis.experiment_id
    assert loaded.winner == analysis.winner
    assert loaded.recommendation == analysis.recommendation
    assert len(loaded.significance_tests) == len(analysis.significance_tests)
    assert loaded.baseline_stats.n == analysis.baseline_stats.n
