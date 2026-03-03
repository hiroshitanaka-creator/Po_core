# Migration Guide v1 (for External Integrators)

本ガイドは、Po_core を外部利用するチーム向けの移行手順。

## 1. Who should read this

- `output_schema_v1.json` へ依存する downstream 実装
- golden 比較で回帰検知している CI
- `run_case_file()` をバッチ実行している運用

## 2. Safe Upgrade Checklist

1. 新バージョンの `CHANGELOG.md` を読む
2. `docs/operations/compatibility_policy_v1.md` の breaking 判定を確認
3. staging で以下を固定値で実行
   - `seed=0`
   - `deterministic=True`
   - `now="2026-02-22T00:00:00Z"`
4. 既存goldenとの差分をレビュー
5. 本番へ段階投入

## 3. If output adds optional fields

- downstream の JSON parser は unknown key を許容する
- strict validation の場合は `additionalProperties` 方針を確認
- 既存必須キーの意味変更がないことを確認

## 4. If arbitration behavior changes

以下を監視する。

- `recommendation.arbitration_code`
- `trace[*].compose_output.metrics.arbitration_code`
- ethics `rules_fired`

差分が出た場合は、仕様変更（ADR）に紐づくことを確認する。

## 5. Rollback Plan

- 直前安定タグを保持する（例: `v0.2.0b3`）
- CIで `pytest -q tests/test_golden_e2e.py` を gate にする
- 互換性問題時は直前タグへロールバックし、ADRに再計画を記載

## 6. One-command verification

以下 1 コマンドで再現チェックを実行可能。

```bash
python scripts/phase25_reproduce.py --profile external
```

詳細は `docs/operations/reproducibility_runbook.md` を参照。
