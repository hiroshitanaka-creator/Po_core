"""Integration tests: Experiment framework pipeline.

Tests storage → analyzer → promoter working together,
verifying the full A/B experiment lifecycle.
"""

import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from po_core.domain.experiment import (
    ExperimentAnalysis,
    ExperimentDefinition,
    ExperimentSample,
    ExperimentStatus,
    ExperimentVariant,
)
from po_core.experiments.analyzer import ExperimentAnalyzer
from po_core.experiments.promoter import ExperimentPromoter
from po_core.experiments.storage import ExperimentStorage


def _make_sample(variant_name, metrics, i=0):
    """Helper to create an ExperimentSample."""
    return ExperimentSample(
        request_id=f"req_{variant_name}_{i}",
        variant_name=variant_name,
        metrics=metrics,
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def experiment_env():
    """Set up a full experiment environment with storage, analyzer, and data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = ExperimentStorage(str(Path(tmpdir) / "results"))
        analyzer = ExperimentAnalyzer(storage)

        # Create experiment definition
        definition = ExperimentDefinition(
            id="pareto_safety_test",
            description="Test safety weight adjustment",
            baseline=ExperimentVariant(
                name="baseline",
                config_path=str(Path(tmpdir) / "configs" / "baseline.yaml"),
            ),
            variants=[
                ExperimentVariant(
                    name="safety_040",
                    config_path=str(Path(tmpdir) / "configs" / "safety_040.yaml"),
                ),
            ],
            metrics=["pareto_front_size", "degraded"],
            sample_size=30,
            significance_level=0.05,
        )

        # Create mock config files for promoter
        configs_dir = Path(tmpdir) / "configs"
        configs_dir.mkdir()
        (configs_dir / "baseline.yaml").write_text("weights: {safety: 0.25}")
        (configs_dir / "safety_040.yaml").write_text("weights: {safety: 0.40}")

        storage.save_definition(definition)

        yield {
            "tmpdir": tmpdir,
            "storage": storage,
            "analyzer": analyzer,
            "definition": definition,
        }


class TestExperimentLifecycle:
    """Test the full experiment lifecycle: define → collect → analyze → promote."""

    def test_define_and_collect_samples(self, experiment_env):
        """Experiment samples can be collected and persisted."""
        storage = experiment_env["storage"]

        # Simulate collecting 30 samples
        for i in range(30):
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "baseline",
                    {"pareto_front_size": 5 + (i % 3), "degraded": i < 3},
                    i,
                ),
            )
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "safety_040",
                    {"pareto_front_size": 7 + (i % 3), "degraded": i < 1},
                    i,
                ),
            )

        # Verify
        samples = storage.load_samples("pareto_safety_test")
        assert len(samples) == 60  # 30 baseline + 30 variant

        baseline_count = sum(1 for s in samples if s.variant_name == "baseline")
        variant_count = sum(1 for s in samples if s.variant_name == "safety_040")
        assert baseline_count == 30
        assert variant_count == 30

    def test_analyze_produces_valid_result(self, experiment_env):
        """Analysis produces valid ExperimentAnalysis with significance tests."""
        storage = experiment_env["storage"]
        analyzer = experiment_env["analyzer"]

        # Collect samples with clear difference
        for i in range(30):
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "baseline",
                    {"pareto_front_size": 5.0 + (i % 3) * 0.5, "degraded": i < 9},
                    i,
                ),
            )
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "safety_040",
                    {"pareto_front_size": 8.0 + (i % 3) * 0.5, "degraded": i < 3},
                    i,
                ),
            )

        analysis = analyzer.analyze("pareto_safety_test")

        assert isinstance(analysis, ExperimentAnalysis)
        assert analysis.experiment_id == "pareto_safety_test"
        assert analysis.baseline_stats.n == 30
        assert len(analysis.variant_stats) == 1
        assert analysis.variant_stats[0].n == 30
        assert len(analysis.significance_tests) == 2  # 2 metrics
        assert analysis.analyzed_at is not None

    def test_analyze_save_and_reload(self, experiment_env):
        """Analysis can be saved and reloaded with full fidelity."""
        storage = experiment_env["storage"]
        analyzer = experiment_env["analyzer"]

        for i in range(30):
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "baseline",
                    {"pareto_front_size": 5.0 + (i % 5) * 0.1, "degraded": i < 3},
                    i,
                ),
            )
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "safety_040",
                    {"pareto_front_size": 8.0 + (i % 5) * 0.1, "degraded": i < 1},
                    i,
                ),
            )

        analysis = analyzer.analyze("pareto_safety_test")
        storage.save_analysis(analysis)

        # Reload
        loaded = storage.load_analysis("pareto_safety_test")

        assert loaded is not None
        assert isinstance(loaded, ExperimentAnalysis)
        assert loaded.experiment_id == analysis.experiment_id
        assert loaded.winner == analysis.winner
        assert loaded.recommendation == analysis.recommendation
        assert loaded.baseline_stats.n == analysis.baseline_stats.n
        assert len(loaded.significance_tests) == len(analysis.significance_tests)

        # Verify significance test fidelity
        for orig, reloaded in zip(
            analysis.significance_tests, loaded.significance_tests
        ):
            assert orig.metric_name == reloaded.metric_name
            assert abs(orig.p_value - reloaded.p_value) < 1e-10
            assert orig.is_significant == reloaded.is_significant

    def test_full_lifecycle_with_promotion(self, experiment_env):
        """Full lifecycle: define → collect → analyze → promote (dry_run)."""
        storage = experiment_env["storage"]
        analyzer = experiment_env["analyzer"]
        tmpdir = experiment_env["tmpdir"]

        # Collect clearly winning samples
        for i in range(30):
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "baseline",
                    {"pareto_front_size": 3.0 + (i % 2), "degraded": i < 10},
                    i,
                ),
            )
            storage.append_sample(
                "pareto_safety_test",
                _make_sample(
                    "safety_040",
                    {"pareto_front_size": 8.0 + (i % 2), "degraded": i < 2},
                    i,
                ),
            )

        # Analyze
        analysis = analyzer.analyze("pareto_safety_test")
        storage.save_analysis(analysis)

        # Promote (dry_run to avoid file system side effects)
        main_config = Path(tmpdir) / "configs" / "baseline.yaml"
        promoter = ExperimentPromoter(
            storage=storage,
            main_config_path=str(main_config),
            backup_dir=str(Path(tmpdir) / "backups"),
        )

        # If winner exists, dry_run should succeed
        if analysis.winner is not None:
            result = promoter.promote("pareto_safety_test", dry_run=True)
            assert result is True

    def test_status_tracking_through_lifecycle(self, experiment_env):
        """Experiment status transitions correctly through lifecycle."""
        storage = experiment_env["storage"]

        # Initial status
        defn = storage.load_definition("pareto_safety_test")
        assert defn.status == ExperimentStatus.PENDING

        # Running
        storage.update_status("pareto_safety_test", ExperimentStatus.RUNNING)
        defn = storage.load_definition("pareto_safety_test")
        assert defn.status == ExperimentStatus.RUNNING

        # Completed
        storage.update_status("pareto_safety_test", ExperimentStatus.COMPLETED)
        defn = storage.load_definition("pareto_safety_test")
        assert defn.status == ExperimentStatus.COMPLETED

    def test_multiple_experiments_isolation(self, experiment_env):
        """Multiple experiments don't interfere with each other."""
        storage = experiment_env["storage"]

        # Create second experiment
        exp2 = ExperimentDefinition(
            id="pareto_freedom_test",
            description="Test freedom weight",
            baseline=ExperimentVariant(name="baseline", config_path="b.yaml"),
            variants=[ExperimentVariant(name="v1", config_path="v.yaml")],
            metrics=["metric1"],
        )
        storage.save_definition(exp2)

        # Add samples to each
        datetime.now(timezone.utc)
        storage.append_sample(
            "pareto_safety_test", _make_sample("baseline", {"pareto_front_size": 5}, 0)
        )
        storage.append_sample(
            "pareto_freedom_test", _make_sample("baseline", {"metric1": 0.5}, 0)
        )

        # Verify isolation
        s1 = storage.load_samples("pareto_safety_test")
        s2 = storage.load_samples("pareto_freedom_test")
        assert len(s1) == 1
        assert len(s2) == 1
        assert "pareto_front_size" in s1[0].metrics
        assert "metric1" in s2[0].metrics

        # List shows both
        experiments = storage.list_experiments()
        assert "pareto_safety_test" in experiments
        assert "pareto_freedom_test" in experiments
