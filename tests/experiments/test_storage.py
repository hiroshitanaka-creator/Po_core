"""Tests for experiment storage."""

import json
import tempfile
from pathlib import Path
from typing import List

import pytest

from po_core.domain.experiment import (
    ExperimentDefinition,
    ExperimentSample,
    ExperimentStatus,
    ExperimentVariant,
    ExperimentAnalysis,
    VariantStatistics,
    SignificanceTest,
)
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
def sample_definition():
    """Create a sample experiment definition."""
    return ExperimentDefinition(
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
            ExperimentVariant(
                name="variant_b",
                config_path="configs/variant_b.yaml",
            ),
        ],
        metrics=["metric1", "metric2"],
        sample_size=10,
        significance_level=0.05,
        status=ExperimentStatus.PENDING,
    )


def test_save_and_load_definition(storage, sample_definition):
    """Test saving and loading experiment definition."""
    # Save definition
    storage.save_definition(sample_definition)

    # Load definition
    loaded = storage.load_definition("test_exp")

    assert loaded is not None
    assert loaded.id == sample_definition.id
    assert loaded.description == sample_definition.description
    assert loaded.baseline == sample_definition.baseline
    assert loaded.variants == sample_definition.variants
    assert loaded.metrics == sample_definition.metrics
    assert loaded.sample_size == sample_definition.sample_size


def test_load_nonexistent_definition(storage):
    """Test loading a non-existent experiment."""
    loaded = storage.load_definition("nonexistent")
    assert loaded is None


def test_append_and_load_samples(storage, sample_definition):
    """Test appending and loading experiment samples."""
    # Save definition first
    storage.save_definition(sample_definition)

    # Create sample data
    samples = [
        ExperimentSample(
            experiment_id="test_exp",
            input_id="input_1",
            variant_name="baseline",
            metrics={"metric1": 0.5, "metric2": 0.8},
        ),
        ExperimentSample(
            experiment_id="test_exp",
            input_id="input_1",
            variant_name="variant_a",
            metrics={"metric1": 0.6, "metric2": 0.7},
        ),
        ExperimentSample(
            experiment_id="test_exp",
            input_id="input_2",
            variant_name="baseline",
            metrics={"metric1": 0.4, "metric2": 0.9},
        ),
    ]

    # Append samples
    for sample in samples:
        storage.append_sample("test_exp", sample)

    # Load samples
    loaded_samples = storage.load_samples("test_exp")

    assert len(loaded_samples) == 3
    assert all(isinstance(s, ExperimentSample) for s in loaded_samples)
    assert loaded_samples[0].input_id == "input_1"
    assert loaded_samples[0].variant_name == "baseline"
    assert loaded_samples[0].metrics["metric1"] == 0.5


def test_save_and_load_analysis(storage, sample_definition):
    """Test saving and loading experiment analysis."""
    # Save definition first
    storage.save_definition(sample_definition)

    # Create analysis
    analysis = ExperimentAnalysis(
        experiment_id="test_exp",
        variant_statistics={
            "baseline": VariantStatistics(
                variant_name="baseline",
                metric_stats={
                    "metric1": {"mean": 0.5, "std": 0.1, "n": 10},
                },
            ),
            "variant_a": VariantStatistics(
                variant_name="variant_a",
                metric_stats={
                    "metric1": {"mean": 0.6, "std": 0.1, "n": 10},
                },
            ),
        },
        significance_tests=[
            SignificanceTest(
                metric_name="metric1",
                baseline_mean=0.5,
                variant_mean=0.6,
                delta=0.1,
                delta_percent=20.0,
                p_value=0.01,
                is_significant=True,
                test_type="t-test",
                effect_size=1.0,
            ),
        ],
        winner="variant_a",
        recommendation="promote",
    )

    # Save analysis
    storage.save_analysis(analysis)

    # Load analysis
    loaded = storage.load_analysis("test_exp")

    assert loaded is not None
    assert loaded.experiment_id == "test_exp"
    assert loaded.winner == "variant_a"
    assert loaded.recommendation == "promote"
    assert len(loaded.significance_tests) == 1
    assert loaded.significance_tests[0].p_value == 0.01


def test_list_experiments(storage, sample_definition):
    """Test listing all experiments."""
    # Create multiple experiments
    exp1 = sample_definition
    exp2 = ExperimentDefinition(
        id="test_exp_2",
        description="Second test",
        baseline=sample_definition.baseline,
        variants=sample_definition.variants,
        metrics=sample_definition.metrics,
        sample_size=20,
    )

    storage.save_definition(exp1)
    storage.save_definition(exp2)

    # List experiments
    experiments = storage.list_experiments()

    assert len(experiments) == 2
    assert "test_exp" in experiments
    assert "test_exp_2" in experiments


def test_update_definition_status(storage, sample_definition):
    """Test updating experiment status."""
    # Save initial definition
    storage.save_definition(sample_definition)

    # Update status
    updated = ExperimentDefinition(
        id=sample_definition.id,
        description=sample_definition.description,
        baseline=sample_definition.baseline,
        variants=sample_definition.variants,
        metrics=sample_definition.metrics,
        sample_size=sample_definition.sample_size,
        significance_level=sample_definition.significance_level,
        status=ExperimentStatus.RUNNING,
    )
    storage.save_definition(updated)

    # Load and check
    loaded = storage.load_definition("test_exp")
    assert loaded.status == ExperimentStatus.RUNNING
