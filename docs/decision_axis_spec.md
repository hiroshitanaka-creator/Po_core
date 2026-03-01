# Decision Axis Spec (DAS)

## 目的

Decision Axis Spec (DAS) は、意思決定の評価座標系をコード本体から分離し、
監査可能な形でバージョン管理するための仕様です。

- **軸 (axis)**: 意思決定を評価するための座標系全体
- **次元 (dimension)**: 軸を構成する個々の評価観点（軸は複数の次元を持つ）

この分離により、アルゴリズム本体を変更せずに評価観点を管理でき、
将来の検証・比較・監査を容易にします。

## ファイル配置

- 仕様モデル: `src/po_core/axis/spec.py`
- デフォルト仕様: `src/po_core/axis/specs/v1.json`

## 仕様の基本構造

DAS は以下を最低限含みます。

- `spec_version`: 仕様バージョン（例: `1.0.0`）
- `axis_name`: 軸の識別名
- `dimensions`: 次元配列
  - `dimension_id`（一意）
  - `title`
  - `description`
  - `scale_min` / `scale_max`
  - `weight`

## Validation ルール

`load_axis_spec()` で読み込まれた仕様は、以下を検証します。

1. 次元ID重複禁止
2. `weight` は `0.0 <= weight <= 1.0`
3. `scale_max > scale_min`

## 変更ルール

DAS の変更は互換性と説明責任の観点から厳密に扱います。

- 軽微な文言修正を除き、意味的変更（次元追加・削除・重み変更・スケール変更）時は
  **必ず spec バージョンを上げる**
- 既存バージョンは凍結し、上書きせず新規バージョンファイルを追加する
  - 例: `v1.json` を変更せず `v2.json` を追加

## バージョニング方針

- 既定は SemVer 風の文字列（`major.minor.patch`）
- 互換性を壊す変更（次元削除・意味変更）は `major` を上げる
- 後方互換な拡張（次元追加、既存意味を壊さない記述追加）は `minor` を上げる
- 文言修正等の軽微変更は `patch` を上げる

## 現時点の運用

本PR時点では、DASは将来拡張のための土台のみ導入し、既存実行パスの挙動は変更しません。
