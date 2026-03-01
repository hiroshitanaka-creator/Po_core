# Trace Event Log (PR-8)

## 目的

Po_core の意思決定を **後から追跡・再現** できるようにするため、
`propose / critique / synthesize` の各段階を JSONL で記録する。

- 監査性（なぜその判断に至ったか）
- 再現性（同じ入力で report 構造を再生成）
- 変更時の説明責任（invariants テストとの接続）

## 保存先

- デフォルト: `.po_core_runs/<run_id>.jsonl`
- 設定可能: `PoSelf(trace_dir=...)` や `po-core replay --log-dir ...`

## ログに残すもの

- `run_id`
- `timestamp`
- `stage` (`propose` / `critique` / `synthesize`)
- `payload`（マスク済み）

## ログに残さない/残りにくくするもの

`payload` は保存前に簡易マスクを通す。

- email らしき文字列 → `[MASKED_EMAIL]`
- phone らしき文字列 → `[MASKED_PHONE]`
- address らしき文字列 → `[MASKED_ADDRESS]`

> 注意: これは最低限のパターンマスクであり、完全な DLP ではない。
> 本番運用では組織ポリシーに沿った追加ルールが必要。

## リプレイ

`python -m po_core.trace.replay <run_id> --log-dir .po_core_runs`

- propose イベントから prompt/context/philosophers を再構築
- 同一設定で再実行し、最低限 `report`（synthesis_report 構造）を再生成

