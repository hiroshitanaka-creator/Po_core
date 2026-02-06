"""
promoter.py - 勝者の自動昇格
==============================

目的:
- 分析結果から勝者を判定
- 勝者の設定ファイルを main に昇格（コピー）
- バックアップを作成（ロールバック可能）

DEPENDENCY RULES:
- domain + experiments のみ依存
- ファイル操作のみ（git操作は外部）
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from po_core.domain.experiment import ExperimentAnalysis, ExperimentStatus
from po_core.experiments.storage import ExperimentStorage


class ExperimentPromoter:
    """
    実験の勝者を自動的に main に昇格するクラス。

    昇格の流れ:
    1. 分析結果を確認（recommendation が "promote" か）
    2. 現在の main 設定をバックアップ
    3. 勝者の設定ファイルを main にコピー
    4. 実験のステータスを PROMOTED に更新
    """

    def __init__(
        self,
        storage: ExperimentStorage,
        main_config_path: str = "02_architecture/philosophy/pareto_table.yaml",
        backup_dir: str = "experiments/backups",
    ) -> None:
        """
        Args:
            storage: 実験結果を保存するストレージ
            main_config_path: main の Pareto 設定ファイルパス
            backup_dir: バックアップ保存先ディレクトリ
        """
        self.storage = storage
        self.main_config_path = Path(main_config_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def promote(self, experiment_id: str, *, force: bool = False, dry_run: bool = False) -> bool:
        """
        実験の勝者を main に昇格する。

        Args:
            experiment_id: 実験ID
            force: recommendation が "promote" でなくても強制的に昇格
            dry_run: 実際にはコピーせず、ログのみ出力

        Returns:
            昇格したかどうか

        Raises:
            ValueError: 実験が見つからない、分析結果がない等
        """
        # 1. 実験定義と分析結果を読み込み
        definition = self.storage.load_definition(experiment_id)
        if definition is None:
            raise ValueError(f"Experiment {experiment_id} not found")

        analysis = self.storage.load_analysis(experiment_id)
        if analysis is None:
            raise ValueError(f"Analysis not found for experiment {experiment_id}")

        # 2. 推奨アクションを確認（型安全にアクセス）
        if not force and analysis.recommendation != "promote":
            print(f"[{experiment_id}] Recommendation is '{analysis.recommendation}', not 'promote'. Skipping.")
            return False

        winner_name = analysis.winner
        if winner_name is None:
            print(f"[{experiment_id}] No winner determined. Skipping.")
            return False

        # 3. 勝者の設定ファイルパスを取得
        winner_variant = None
        for v in definition.variants:
            if v.name == winner_name:
                winner_variant = v
                break

        if winner_variant is None:
            raise ValueError(f"Winner variant '{winner_name}' not found in definition")

        winner_config_path = Path(winner_variant.config_path)
        if not winner_config_path.exists():
            raise FileNotFoundError(f"Winner config file not found: {winner_config_path}")

        # 4. バックアップを作成
        if self.main_config_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"pareto_table_{timestamp}.yaml"

            if dry_run:
                print(f"[DRY RUN] Would backup {self.main_config_path} -> {backup_path}")
            else:
                shutil.copy2(self.main_config_path, backup_path)
                print(f"[{experiment_id}] Backed up to {backup_path}")

        # 5. 勝者の設定を main にコピー
        if dry_run:
            print(f"[DRY RUN] Would promote {winner_config_path} -> {self.main_config_path}")
        else:
            shutil.copy2(winner_config_path, self.main_config_path)
            print(f"[{experiment_id}] Promoted {winner_name} to {self.main_config_path}")

        # 6. 実験のステータスを PROMOTED に更新
        if not dry_run:
            self.storage.update_status(experiment_id, ExperimentStatus.PROMOTED)

        return True

    def rollback(self, backup_name: Optional[str] = None) -> None:
        """
        バックアップから main を復元する。

        Args:
            backup_name: バックアップファイル名（指定しなければ最新）

        Raises:
            FileNotFoundError: バックアップが見つからない
        """
        if backup_name is None:
            # 最新のバックアップを探す
            backups = sorted(self.backup_dir.glob("pareto_table_*.yaml"), reverse=True)
            if not backups:
                raise FileNotFoundError("No backups found")
            backup_path = backups[0]
        else:
            backup_path = self.backup_dir / backup_name
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup not found: {backup_path}")

        # 復元
        shutil.copy2(backup_path, self.main_config_path)
        print(f"Rolled back to {backup_path}")

    def list_backups(self) -> List[str]:
        """バックアップの一覧を返す"""
        return [b.name for b in sorted(self.backup_dir.glob("pareto_table_*.yaml"), reverse=True)]


__all__ = ["ExperimentPromoter"]
