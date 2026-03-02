# ADR Guide

## 1. 目的
ADR（Architecture Decision Record）は、Po_coreにおける重要な設計判断を、
**なぜそう決めたか**まで含めて記録するための文書です。

- 変更統制（誰が見ても判断の根拠が追える）
- 仕様と実装のトレーサビリティ維持
- 後続PRでの再発明や場当たり対応の抑止

## 2. 採番ルール
- 保存先: `docs/adr/`
- ファイル名: `NNNN-short-title.md`
  - 例: `0015-sample-decision.md`
- `NNNN` は4桁ゼロ埋め連番（既存最大 +1）
- 既存ADRの修正が必要でも、原則は新規ADRで supersede/append を明示する

## 3. ステータス
各ADRの冒頭に、最低限以下を明記します。

- Status: Proposed | Accepted | Superseded
- Date: `YYYY-MM-DD`
- Decision Makers: （任意）
- Supersedes / Superseded by: （該当時）

## 4. 書き方（推奨テンプレ）
以下の順番で簡潔に記述します。

1. Context（背景/制約/問題）
2. Decision（採用する方針）
3. Consequences（利点・欠点・トレードオフ）
4. Alternatives considered（不採用案と理由）
5. Validation（どうテストで固定するか）
6. Traceability（関連REQ/AT/テスト/コード）

## 5. ADRが必要になるタイミング
次のいずれかに当てはまる場合、ADRを作成または更新します。

- 出力契約・スキーマ・goldenの意味を変える変更
- ルールの責務境界（parse_input / engines / orchestrator / tracer）を変える変更
- 推奨ロジック、倫理評価、trace契約などの恒久方針を変える変更
- 将来のPRにも継続して影響する設計判断

軽微なリファクタ、誤字修正、明確なバグ修正のみで設計判断を増やさない場合は、
PR本文で「ADR不要理由」を明記します。

## 6. PRとの連携
PRでは以下を必ず記載します。

- 関連Requirement ID / Acceptance Test
- ADRの有無（不要なら理由）
- 実行したテスト（最低 `pytest -q`）
- 影響範囲とリスク

これにより「仕様 → ADR → テスト → 実装」の追跡可能性を維持します。
