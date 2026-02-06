"""Tests for experiment promoter."""

import tempfile
from pathlib import Path

import pytest

from po_core.domain.experiment import (
    ExperimentAnalysis,
    ExperimentDefinition,
    ExperimentStatus,
    ExperimentVariant,
    SignificanceTest,
    VariantStatistics,
)
from po_core.experiments.promoter import ExperimentPromoter
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
def promoter(storage, temp_dir):
    """Create an ExperimentPromoter instance."""
    main_config_path = temp_dir / "main_config.yaml"
    main_config_path.write_text("# Main config\nsafety: 0.25\n")
    backup_dir = temp_dir / "backups"
    return ExperimentPromoter(storage, str(main_config_path), str(backup_dir))


@pytest.fixture
def winning_experiment(storage, temp_dir):
    """Create an experiment with a clear winner."""
    configs_dir = temp_dir / "configs"
    configs_dir.mkdir()

    baseline_config = configs_dir / "baseline.yaml"
    baseline_config.write_text("# Baseline\nsafety: 0.25\n")

    winner_config = configs_dir / "winner.yaml"
    winner_config.write_text("# Winner\nsafety: 0.50\n")

    definition = ExperimentDefinition(
        id="winning_exp",
        description="Winning experiment",
        baseline=ExperimentVariant(
            name="baseline",
            config_path=str(baseline_config),
        ),
        variants=[
            ExperimentVariant(
                name="winner",
                config_path=str(winner_config),
            ),
        ],
        metrics=["metric1"],
        sample_size=20,
        status=ExperimentStatus.COMPLETED,
    )

    storage.save_definition(definition)

    analysis = ExperimentAnalysis(
        experiment_id="winning_exp",
        baseline_stats=VariantStatistics(
            variant_name="baseline",
            n=20,
            metrics={"metric1": {"mean": 0.5, "std": 0.1, "n": 20}},
        ),
        variant_stats=[
            VariantStatistics(
                variant_name="winner",
                n=20,
                metrics={"metric1": {"mean": 0.7, "std": 0.1, "n": 20}},
            ),
        ],
        significance_tests=[
            SignificanceTest(
                metric_name="metric1",
                baseline_mean=0.5,
                variant_mean=0.7,
                delta=0.2,
                delta_percent=40.0,
                p_value=0.001,
                is_significant=True,
                test_type="t_test",
                effect_size=2.0,
            ),
        ],
        winner="winner",
        recommendation="promote",
    )

    storage.save_analysis(analysis)

    return "winning_exp"


def test_promote_dry_run(promoter, winning_experiment, temp_dir):
    """Test dry run promotion."""
    main_config = temp_dir / "main_config.yaml"
    original_content = main_config.read_text()

    result = promoter.promote(winning_experiment, dry_run=True)

    assert result is True
    assert main_config.read_text() == original_content


def test_promote_success(promoter, winning_experiment, temp_dir):
    """Test successful promotion."""
    main_config = temp_dir / "main_config.yaml"

    result = promoter.promote(winning_experiment)

    assert result is True

    new_content = main_config.read_text()
    assert "safety: 0.50" in new_content

    backups_dir = temp_dir / "backups"
    assert backups_dir.exists()
    backups = list(backups_dir.glob("*.yaml"))
    assert len(backups) == 1
    assert "safety: 0.25" in backups[0].read_text()

    definition = promoter.storage.load_definition(winning_experiment)
    assert definition.status == ExperimentStatus.PROMOTED


def test_promote_no_recommendation(storage, temp_dir):
    """Test promotion when recommendation is not 'promote'."""
    main_config_path = temp_dir / "main_config.yaml"
    main_config_path.write_text("# Main config\n")

    promoter = ExperimentPromoter(storage, str(main_config_path))

    definition = ExperimentDefinition(
        id="no_promote_exp",
        description="No promote",
        baseline=ExperimentVariant(name="baseline", config_path="configs/baseline.yaml"),
        variants=[ExperimentVariant(name="variant_a", config_path="configs/variant_a.yaml")],
        metrics=["metric1"],
        sample_size=20,
    )
    storage.save_definition(definition)

    analysis = ExperimentAnalysis(
        experiment_id="no_promote_exp",
        baseline_stats=VariantStatistics(variant_name="baseline", n=0, metrics={}),
        variant_stats=[],
        significance_tests=[],
        winner=None,
        recommendation="continue",
    )
    storage.save_analysis(analysis)

    result = promoter.promote("no_promote_exp")
    assert result is False


def test_promote_with_force(storage, temp_dir):
    """Test promotion with force flag."""
    main_config_path = temp_dir / "main_config.yaml"
    main_config_path.write_text("# Main config\n")

    configs_dir = temp_dir / "configs"
    configs_dir.mkdir()
    variant_config = configs_dir / "variant_a.yaml"
    variant_config.write_text("# Variant A\n")

    promoter = ExperimentPromoter(storage, str(main_config_path))

    definition = ExperimentDefinition(
        id="force_exp",
        description="Force promote",
        baseline=ExperimentVariant(name="baseline", config_path="configs/baseline.yaml"),
        variants=[ExperimentVariant(name="variant_a", config_path=str(variant_config))],
        metrics=["metric1"],
        sample_size=20,
    )
    storage.save_definition(definition)

    analysis = ExperimentAnalysis(
        experiment_id="force_exp",
        baseline_stats=VariantStatistics(variant_name="baseline", n=0, metrics={}),
        variant_stats=[],
        significance_tests=[],
        winner="variant_a",
        recommendation="continue",
    )
    storage.save_analysis(analysis)

    result = promoter.promote("force_exp", force=True)
    assert result is True


def test_rollback(promoter, winning_experiment, temp_dir):
    """Test rollback to previous config."""
    main_config = temp_dir / "main_config.yaml"
    original_content = main_config.read_text()

    promoter.promote(winning_experiment)
    assert main_config.read_text() != original_content

    promoter.rollback()
    assert main_config.read_text() == original_content


def test_list_backups(promoter, winning_experiment, temp_dir):
    """Test listing backups."""
    backups = promoter.list_backups()
    assert len(backups) == 0

    promoter.promote(winning_experiment)

    backups = promoter.list_backups()
    assert len(backups) == 1
    assert backups[0].endswith(".yaml")


def test_rollback_no_backups(temp_dir):
    """Test rollback when no backups exist."""
    storage = ExperimentStorage(str(temp_dir / "storage"))
    main_config_path = temp_dir / "main_config.yaml"
    main_config_path.write_text("# Main config\n")
    backup_dir = temp_dir / "empty_backups"

    promoter = ExperimentPromoter(storage, str(main_config_path), str(backup_dir))

    with pytest.raises(FileNotFoundError):
        promoter.rollback()


def test_rollback_specific_backup(promoter, winning_experiment, temp_dir):
    """Test rollback to a specific backup."""
    main_config = temp_dir / "main_config.yaml"

    promoter.promote(winning_experiment)
    backups = promoter.list_backups()
    first_backup = backups[0]

    # Modify config manually
    main_config.write_text("# Modified\n")

    # Rollback to the backup (which has the original config before promotion)
    promoter.rollback(backup_name=first_backup)
    # The backup contains the original config (safety: 0.25)
    assert "safety: 0.25" in main_config.read_text()
