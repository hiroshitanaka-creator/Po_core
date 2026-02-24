"""
experiment.py - 実験管理CLI
=============================

Usage:
    po-experiment list
    po-experiment run <experiment_id> [--inputs=FILE]
    po-experiment analyze <experiment_id>
    po-experiment promote <experiment_id> [--force] [--dry-run]
    po-experiment rollback [--backup=NAME]
"""

from __future__ import annotations

import sys

# click は optional（なければ簡易実装）
try:
    import click

    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

from po_core.experiments.analyzer import ExperimentAnalyzer
from po_core.experiments.promoter import ExperimentPromoter
from po_core.experiments.storage import ExperimentStorage


def _print_help():
    """ヘルプメッセージを表示"""
    print(
        """
Po_core Experiment CLI

Usage:
    python -m po_core.cli.experiment list
    python -m po_core.cli.experiment analyze <experiment_id>
    python -m po_core.cli.experiment promote <experiment_id> [--force] [--dry-run]
    python -m po_core.cli.experiment rollback [--backup=NAME]

Commands:
    list         List all experiments
    analyze      Analyze experiment results
    promote      Promote winner to main (if recommendation is 'promote')
    rollback     Rollback to previous backup
"""
    )


def cmd_list():
    """実験一覧を表示"""
    storage = ExperimentStorage()
    experiments = storage.list_experiments()

    if not experiments:
        print("No experiments found.")
        return

    print("Experiments:")
    for exp_id in experiments:
        defn = storage.load_definition(exp_id)
        if defn:
            print(f"  - {exp_id}: {defn.description} ({defn.status.value})")
        else:
            print(f"  - {exp_id}")


def cmd_analyze(experiment_id: str):
    """実験を分析"""
    storage = ExperimentStorage()
    analyzer = ExperimentAnalyzer(storage)

    print(f"Analyzing experiment: {experiment_id}")
    try:
        analysis = analyzer.analyze(experiment_id)
        storage.save_analysis(analysis)

        print("\nAnalysis completed:")
        print(
            f"  Baseline: {analysis.baseline_stats.variant_name}"
            f" (n={analysis.baseline_stats.n})"
        )
        for vs in analysis.variant_stats:
            print(f"  Variant: {vs.variant_name} (n={vs.n})")

        print("\nSignificance Tests:")
        for test in analysis.significance_tests:
            sig = "✓" if test.is_significant else "✗"
            print(
                f"  {sig} {test.metric_name}: baseline={test.baseline_mean:.4f},"
                f" variant={test.variant_mean:.4f}, delta={test.delta:+.4f}"
                f" ({test.delta_percent:+.2f}%), p={test.p_value:.4f}"
            )

        print(f"\nRecommendation: {analysis.recommendation}")
        if analysis.winner:
            print(f"Winner: {analysis.winner}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_promote(experiment_id: str, force: bool = False, dry_run: bool = False):
    """勝者を main に昇格"""
    storage = ExperimentStorage()
    promoter = ExperimentPromoter(storage)

    print(f"Promoting experiment: {experiment_id}")
    if dry_run:
        print("[DRY RUN MODE]")

    try:
        promoted = promoter.promote(experiment_id, force=force, dry_run=dry_run)
        if promoted:
            print("✓ Promotion completed")
        else:
            print("✗ Promotion skipped")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_rollback(backup_name: str | None = None):
    """バックアップから復元"""
    storage = ExperimentStorage()
    promoter = ExperimentPromoter(storage)

    if backup_name is None:
        # 最新のバックアップを表示して確認
        backups = promoter.list_backups()
        if not backups:
            print("No backups found.")
            return

        print("Available backups:")
        for b in backups[:5]:  # 最新5件
            print(f"  - {b}")

        latest = backups[0]
        print(f"\nRolling back to: {latest}")
        confirm = input("Proceed? [y/N]: ")
        if confirm.lower() != "y":
            print("Cancelled.")
            return

        backup_name = latest

    try:
        promoter.rollback(backup_name)
        print("✓ Rollback completed")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main_simple():
    """簡易CLI（click なし）"""
    if len(sys.argv) < 2:
        _print_help()
        return

    command = sys.argv[1]

    if command == "list":
        cmd_list()
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Error: experiment_id required", file=sys.stderr)
            sys.exit(1)
        cmd_analyze(sys.argv[2])
    elif command == "promote":
        if len(sys.argv) < 3:
            print("Error: experiment_id required", file=sys.stderr)
            sys.exit(1)
        exp_id = sys.argv[2]
        force = "--force" in sys.argv
        dry_run = "--dry-run" in sys.argv
        cmd_promote(exp_id, force=force, dry_run=dry_run)
    elif command == "rollback":
        backup = None
        for arg in sys.argv[2:]:
            if arg.startswith("--backup="):
                backup = arg.split("=", 1)[1]
        cmd_rollback(backup)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        _print_help()
        sys.exit(1)


if HAS_CLICK:
    # click を使った実装
    @click.group()
    def cli():
        """Po_core Experiment Management CLI"""
        pass

    @cli.command()
    def list():
        """List all experiments"""
        cmd_list()

    @cli.command()
    @click.argument("experiment_id")
    def analyze(experiment_id):
        """Analyze experiment results"""
        cmd_analyze(experiment_id)

    @cli.command()
    @click.argument("experiment_id")
    @click.option(
        "--force", is_flag=True, help="Force promotion even if not recommended"
    )
    @click.option("--dry-run", is_flag=True, help="Dry run (don't actually copy files)")
    def promote(experiment_id, force, dry_run):
        """Promote winner to main"""
        cmd_promote(experiment_id, force=force, dry_run=dry_run)

    @cli.command()
    @click.option("--backup", default=None, help="Backup name (default: latest)")
    def rollback(backup):
        """Rollback to previous backup"""
        cmd_rollback(backup)

    if __name__ == "__main__":
        cli()
else:
    # fallback
    if __name__ == "__main__":
        main_simple()


__all__ = ["cli", "main_simple"]
