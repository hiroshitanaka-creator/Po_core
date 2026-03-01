# Axis Calibration Dataset Format (v1)

Po_core の軸スコア校正用データセットは **JSONL (1行1サンプル)** を採用します。

## 1. レコード形式

各行は次の JSON オブジェクトです。

```json
{"text":"...", "labels":{"choice":0.7,"responsibility":0.4,"urgency":0.2,"ethics":0.8,"social":0.6,"authenticity":0.5}, "meta":{"lang":"ja","domain":"career"}}
```

## 2. 必須キー

- `text` (string): 推定対象のテキスト
- `labels` (object): 0.0〜1.0 の連続値ラベル
  - 対象軸: `choice`, `responsibility`, `urgency`, `ethics`, `social`, `authenticity`

## 3. 任意キー

- `meta` (object): 付加情報
  - 例: `lang`, `domain`, `annotator`, `source`

## 4. バリデーションルール

- `labels` に未知キーがあっても学習では無視されます。
- 必須6軸が1つでも欠ける行は学習時にスキップされます。
- ラベル値は数値として解釈され、最終的に `[0,1]` にクリップされます。

## 5. 再現性

- `scripts/train_axis_calibration.py` は入力順で決定論的に学習します。
- 同一データ・同一 `--alpha` なら同一 `params_v1.json` が得られます。
