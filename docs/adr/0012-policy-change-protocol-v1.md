# ADR 0012: Policy Change Protocol v1

**Date:** 2026-02-28
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

`policy_v1` 等の政策定数（閾値・重み・裁定順序）を変更すると、recommendation/ethics/trace/golden に連鎖影響が出る。

しかし「雰囲気で変更して expected を合わせる」運用は、Po_core の最優先要件である決定性・説明責任・安全な変更管理を壊す。

そのため、policy変更時に必須の儀式（protocol）を固定し、PRレビューで機械的に検証できる状態にする。

## Decision

policy定数を変更するPRでは、以下を **必須** とする。

1. **policy_lab レポート添付（JSON + Markdown）**
   - policy差分を評価した `policy_lab` の成果物を PR に添付する。
   - 最低限、次の2形式を含める。
     - 機械可読: `*.json`
     - 人間可読: `*.md`

2. **PR本文に impacted_requirements 上位を明記**
   - `policy_lab` が算出した `impacted_requirements` の上位項目（例: Top 3）をPR本文へ記載する。
   - 「何が、なぜ影響を受けるか」をレポート参照付きで説明する。

3. **必要時のgolden再生成（手編集禁止）**
   - 変更影響で golden 差分が発生する場合は、決定論パラメータで再生成する。
   - `scenarios/*_expected.json` の手編集は禁止（生成物のみを採用）。
   - PR本文に golden 差分要約（対象ケース、主要差分、妥当性）を記載する。

## Operational Protocol (PR Ritual)

policy定数変更を含むPRは、以下を順番に満たす。

1. policy変更内容を実装（変更理由をコミットメッセージに明示）
2. `policy_lab` 実行でレポート（json/md）を生成
3. レポートから `impacted_requirements` 上位を抽出
4. 必要なgoldenを再生成（手編集禁止）
5. `pytest -q` を実行して全通を確認
6. PR本文に以下を記載
   - policy_lab 添付物の場所
   - impacted_requirements 上位
   - （golden差分がある場合）差分要約

## Rationale

- 政策変更の根拠を成果物で固定し、レビューの主観依存を減らせる
- impacted_requirements の明示で、仕様影響範囲の説明責任を満たせる
- golden再生成を手編集禁止にすることで、契約変更の追跡可能性を維持できる

## Consequences

- policy変更PRの準備コストは上がるが、監査可能性が向上する
- PR本文のフォーマットが半自動化しやすくなる
- golden差分があるPRでは「生成手順」がレビュー対象となる

## Non-Goals

- policy内容（閾値そのもの）の妥当性を本ADR単体で保証すること
- policy_lab の評価アルゴリズム詳細を固定すること（別ADRで管理）

## Alternatives Considered

| 代替案 | 却下理由 |
|---|---|
| PR説明のみで運用（添付物なし） | 証跡が弱く、再現不能になりやすい |
| impacted_requirements 記載を任意化 | 影響説明が抜け落ち、レビューが属人化する |
| golden手編集を許可 | 差分由来が不明瞭になり、契約管理が壊れる |
