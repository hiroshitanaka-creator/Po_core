## Summary
- 変更概要:
- 背景/目的:

## 必須チェック（SSOT / 進捗 / テスト報告）
- [ ] SSOT `docs/厳格固定ルール.md` を読んだ
- [ ] `docs/status.md` を更新した（どこを動かしたかを記載）
- [ ] 実行したテストコマンドと結果を下記に記載した
- [ ] 影響範囲とロールバック手順を下記に記載した

## Status Update
- 更新箇所（Completed / Meta / Next など）:
- 更新内容:

## Test Report
- [ ] `pytest -q`
- [ ] その他:

実行ログ（コマンドと結果）:
- 

## Impact / Rollback
- 影響範囲:
- ロールバック手順:

## Policy Change Protocol v1（policy定数変更時のみ必須）
- [ ] policy定数変更なし（該当しない）
- [ ] policy_lab レポート（JSON）を添付した
- [ ] policy_lab レポート（Markdown）を添付した
- [ ] impacted_requirements 上位（例: Top 3）を本文へ記載した
- [ ] golden差分がある場合、再生成で更新した（手編集なし）
- [ ] golden差分要約（対象ケース/主要差分/妥当性）を本文へ記載した

## Evidence
- policy_lab artifacts:
  - JSON:
  - Markdown:
- impacted_requirements (Top):
  1.
  2.
  3.

## Validation
- [ ] `pytest -q` を実行し全通

## Determinism & Compatibility Checklist
- [ ] 凍結golden（`case_001` / `case_009`）を変更していない
- [ ] schema互換性を確認した（`tests/test_input_schema.py` / `tests/test_output_schema.py`）
- [ ] golden契約を確認した（`tests/test_golden_e2e.py`）
- [ ] 互換性に影響がある場合、`docs/operations/migration_guide_v1.md` を更新した

## Notes
- 追加の注意事項・制約:
