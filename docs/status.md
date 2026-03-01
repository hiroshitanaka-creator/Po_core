# Status Snapshot (A〜F)

この文書は、A〜F完了時点の状態を会話コンテキスト非依存で固定するためのスナップショット。

## Completed
- **A**: 入力正規化として `features` 抽出レイヤを導入し、case固有分岐増殖を抑制した。
- **B**: recommendation裁定閾値を `policy_v1` に集約し、裁定ロジックを決定論で一元化した。
- **C**: trace（generic）に `unknowns_count` / `stakeholders_count` / `days_to_deadline` 観測値を追加し、監査性を強化した。
- **D**: ethics guardrails v1 を拡張しつつ、recommendation裁定への非干渉（非介入）契約を明文化した。
- **E**: recommendationの裁定経路を `arbitration_code` として保持できるようにし、裁定理由の可観測性を上げた。
- **F**: ethicsをruleset化し、`rule_id` と `rules_fired` により「どの規則が発火したか」を追跡可能にした。

## Contracts
- **凍結golden**: `scenarios/case_001_expected.json` / `scenarios/case_009_expected.json` は凍結契約（改変禁止）。
- **決定性**: 同一入力 + 同一 `seed` + 同一 `now` + 同一バージョンで出力JSON完全一致（wall-clock/乱数禁止）。
- **golden更新手順**: 仕様根拠（ADR/SRS）を先に固定し、決定論パラメータで生成→保存→`pytest -q` 全通を確認する。
- **責務境界**:
  - `features` は観測のみ（判断を入れない）
  - `engines` はルール判定と生成
  - `recommendation` は最終裁定の単独責務
  - `ethics` はガードレール/トレードオフ提示（裁定はしない）

## Next
- **G（追加golden 2本）**:
  1. `unknowns × deadline` の組み合わせで、時間圧があるが未知情報が残るケースの裁定境界を固定する。
  2. stakeholders外部性（利害関係者複数）で、責任/倫理の観測とrule発火を固定する。

## Deliberation Protocol v1 (PR-4)
- 新しい内部プロトコル `Propose -> Critique -> Synthesize` を `src/po_core/deliberation/protocol.py` に追加。
- feature flag `PO_DEBATE_V1=1` 時、Ensemble/PartyMachine 内部で protocol v1 を実行し、最終出力互換を維持したまま相互批判の観測が可能。
- synthesis report は `open_questions` と `disagreements` を含み、批判フェーズが空になりにくいようにデフォルト批判ルールを実装。
