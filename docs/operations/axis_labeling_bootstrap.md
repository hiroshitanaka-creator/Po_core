# 最初のラベル付けをどう始めるか（運用メモ）

## 目的

FreedomPressureV2 の軸スコアを校正可能にするため、最初の教師データを少量で立ち上げる手順です。

## 最小スタート（1日で可能）

1. **対象ドメインを1つに絞る**
   - 例: `career`（進路・転職相談）
2. **50〜100件のテキストを収集**
   - 既存FAQ、過去相談文、社内サンプルなど
3. **6軸を0.0〜1.0でラベル付け**
   - `choice`, `responsibility`, `urgency`, `ethics`, `social`, `authenticity`
4. **JSONL化して保存**
   - 形式は `calibration/dataset_format.md` に準拠
5. **校正パラメータを学習**
   - `python scripts/train_axis_calibration.py --dataset <jsonl>`
6. **A/B確認**
   - `PO_CALIBRATION_PARAMS` 未設定（heuristic）と設定あり（calibrated）を比較

## ラベル品質のコツ

- まずは2人ラベリングで10件だけ重複し、軸定義のズレを調整する。
- `0.5` を多用しすぎない（情報量が下がる）。
- 迷うケースには `meta.note` を残し、後で基準を更新する。

## 追加運用

- 週次で20件追加→再学習→差分確認を繰り返す。
- ドメイン別（career/legal/healthなど）に params を分ける場合は
  `PO_CALIBRATION_PARAMS` の切替で運用可能。
