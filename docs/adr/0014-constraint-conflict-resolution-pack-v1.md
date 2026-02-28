# ADR 0014: Constraint Conflict Resolution Pack v1

**Date:** 2026-02-28
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

`features.constraint_conflict == True` は「要求制約が同時成立しない」状態を示す。
この状態で recommendation を強めるより、矛盾解消プロトコルを deterministic に出力し、
最短で前提を再設計できる状態へ戻す必要がある。

既存方針（ADR-0006, ADR-0008, ADR-0013）により recommendation 裁定の専権は維持され、
planning/question レイヤは裁定に介入しないことが前提である。

## Decision

Constraint Conflict Resolution Pack v1 を generic feature path に追加する。

- Trigger:
  - `features.constraint_conflict == True`
- Questions:
  - 矛盾解消質問を決定論順序で生成し、最大5件に制限する
  - rule_id: `Q_CONFLICT_RESOLUTION_PROTOCOL_V1`
- Plan (`options[].action_plan`):
  - conflict summary を先頭に置く
  - 最短手順を最大5ステップで固定する
  - rule_id: `PLAN_CONSTRAINT_CONFLICT_PROTOCOL_V1`
- Non-Interference:
  - recommendation の `status / recommended_option_id / arbitration_code` は変更しない

## Rationale

- 矛盾を放置したまま実行すると、実行不能な計画と責任不在が発生しやすい
- conflict summary を先頭に固定することで、説明責任の起点を統一できる
- 質問と手順を上限付きで固定することで、golden と trace で再現性を担保できる

## Consequences

- constraint_conflict ケースで questions/action_plan がプロトコル形式になる
- planning rule_id に `PLAN_CONSTRAINT_CONFLICT_PROTOCOL_V1` が追加され、trace で観測可能になる
- execution coverage must_cover に新rule_idを追加し、scenario実行で担保する

## Non-Goals

- recommendation policy_v1 の閾値・裁定順序の変更
- case固有分岐（`if short_id == ...`）の追加
- frozen contract（case_001 / case_009）の更新
