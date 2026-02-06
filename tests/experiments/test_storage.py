"""Tests for experiment storage."""

import json
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pytest

from po_core.domain.experiment import (
    ExperimentAnalysis,
    ExperimentDefinition,
    ExperimentSample,
    ExperimentStatus,
    ExperimentVariant,
    SignificanceTest,
    VariantStatistics,
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
    storage.save_definition(sample_definition)

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
    storage.save_definition(sample_definition)

    now = datetime.now(timezone.utc)
    samples = [
        ExperimentSample(
            request_id="req_1",
            variant_name="baseline",
            metrics={"metric1": 0.5, "metric2": 0.8},
            timestamp=now,
        ),
        ExperimentSample(
            request_id="req_2",
            variant_name="variant_a",
            metrics={"metric1": 0.6, "metric2": 0.7},
            timestamp=now,
        ),
        ExperimentSample(
            request_id="req_3",
            variant_name="baseline",
            metrics={"metric1": 0.4, "metric2": 0.9},
            timestamp=now,
        ),
    ]

    for sample in samples:
        storage.append_sample("test_exp", sample)

    loaded_samples = storage.load_samples("test_exp")

    assert len(loaded_samples) == 3
    assert all(isinstance(s, ExperimentSample) for s in loaded_samples)
    assert loaded_samples[0].request_id == "req_1"
    assert loaded_samples[0].variant_name == "baseline"
    assert loaded_samples[0].metrics["metric1"] == 0.5


def test_append_samples_batch(storage, sample_definition):
    """Test batch appending of samples."""
    storage.save_definition(sample_definition)

    now = datetime.now(timezone.utc)
    samples = [
        ExperimentSample(
            request_id=f"req_{i}",
            variant_name="baseline",
            metrics={"metric1": 0.5 + i * 0.01},
            timestamp=now,
        )
        for i in range(5)
    ]

    storage.append_samples("test_exp", samples)
    loaded = storage.load_samples("test_exp")
    assert len(loaded) == 5


def test_count_samples(storage, sample_definition):
    """Test sample counting."""
    storage.save_definition(sample_definition)

    now = datetime.now(timezone.utc)
    for i in range(3):
        storage.append_sample("test_exp", ExperimentSample(
            request_id=f"req_{i}",
            variant_name="baseline",
            metrics={"metric1": 0.5},
            timestamp=now,
        ))
    for i in range(2):
        storage.append_sample("test_exp", ExperimentSample(
            request_id=f"req_v_{i}",
            variant_name="variant_a",
            metrics={"metric1": 0.6},
            timestamp=now,
        ))

    assert storage.count_samples("test_exp") == 5
    assert storage.count_samples("test_exp", variant_name="baseline") == 3
    assert storage.count_samples("test_exp", variant_name="variant_a") == 2


def test_save_and_load_analysis(storage, sample_definition):
    """Test saving and loading experiment analysis with full reconstruction."""
    storage.save_definition(sample_definition)

    now = datetime.now(timezone.utc)
    analysis = ExperimentAnalysis(
        experiment_id="test_exp",
        baseline_stats=VariantStatistics(
            variant_name="baseline",
            n=10,
            metrics={
                "metric1": {"mean": 0.5, "std": 0.1, "min": 0.3, "max": 0.7, "median": 0.5, "n": 10},
            },
        ),
        variant_stats=[
            VariantStatistics(
                variant_name="variant_a",
                n=10,
                metrics={
                    "metric1": {"mean": 0.6, "std": 0.1, "min": 0.4, "max": 0.8, "median": 0.6, "n": 10},
                },
            ),
        ],
        significance_tests=[
            SignificanceTest(
                metric_name="metric1",
                baseline_mean=0.5,
                variant_mean=0.6,
                delta=0.1,
                delta_percent=20.0,
                p_value=0.01,
                is_significant=True,
                test_type="t_test",
                effect_size=1.0,
            ),
        ],
        winner="variant_a",
        recommendation="promote",
        analyzed_at=now,
    )

    storage.save_analysis(analysis)

    loaded = storage.load_analysis("test_exp")

    assert loaded is not None
    assert isinstance(loaded, ExperimentAnalysis)
    assert loaded.experiment_id == "test_exp"
    assert loaded.winner == "variant_a"
    assert loaded.recommendation == "promote"
    assert len(loaded.significance_tests) == 1
    assert loaded.significance_tests[0].p_value == 0.01
    assert loaded.significance_tests[0].is_significant is True
    assert loaded.significance_tests[0].effect_size == 1.0
    assert loaded.baseline_stats.variant_name == "baseline"
    assert loaded.baseline_stats.n == 10
    assert loaded.baseline_stats.metrics["metric1"]["mean"] == 0.5
    assert len(loaded.variant_stats) == 1
    assert loaded.variant_stats[0].variant_name == "variant_a"


def test_load_analysis_nonexistent(storage):
    """Test loading analysis for non-existent experiment."""
    loaded = storage.load_analysis("nonexistent")
    assert loaded is None


def test_analysis_history(storage, sample_definition):
    """Test that analysis history is maintained."""
    storage.save_definition(sample_definition)

    for i in range(3):
        analysis = ExperimentAnalysis(
            experiment_id="test_exp",
            baseline_stats=VariantStatistics(variant_name="baseline", n=10, metrics={}),
            variant_stats=[],
            significance_tests=[],
            recommendation="continue",
            analyzed_at=datetime(2024, 1, 1, i, 0, 0),
        )
        storage.save_analysis(analysis)

    history_dir = storage._exp_dir("test_exp") / "analysis_history"
    history_files = list(history_dir.glob("*.json"))
    assert len(history_files) == 3


def test_list_experiments(storage, sample_definition):
    """Test listing all experiments."""
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

    experiments = storage.list_experiments()

    assert len(experiments) == 2
    assert "test_exp" in experiments
    assert "test_exp_2" in experiments


def test_update_status(storage, sample_definition):
    """Test updating experiment status."""
    storage.save_definition(sample_definition)

    storage.update_status("test_exp", ExperimentStatus.RUNNING)

    loaded = storage.load_definition("test_exp")
    assert loaded.status == ExperimentStatus.RUNNING


def test_update_status_nonexistent(storage):
    """Test updating status for non-existent experiment raises ValueError."""
    with pytest.raises(ValueError, match="not found"):
        storage.update_status("nonexistent", ExperimentStatus.RUNNING)


def test_thread_safe_append_samples(storage, sample_definition):
    """Test that concurrent sample appends don't corrupt data."""
    storage.save_definition(sample_definition)

    now = datetime.now(timezone.utc)
    errors = []

    def append_batch(variant_name, count):
        try:
            for i in range(count):
                storage.append_sample("test_exp", ExperimentSample(
                    request_id=f"req_{variant_name}_{i}",
                    variant_name=variant_name,
                    metrics={"metric1": 0.5},
                    timestamp=now,
                ))
        except Exception as e:
            errors.append(e)

    threads = [
        threading.Thread(target=append_batch, args=("baseline", 20)),
        threading.Thread(target=append_batch, args=("variant_a", 20)),
        threading.Thread(target=append_batch, args=("variant_b", 20)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    loaded = storage.load_samples("test_exp")
    assert len(loaded) == 60
