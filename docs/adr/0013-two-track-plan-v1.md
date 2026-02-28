# ADR 0013: Two-Track Plan v1（unknowns × time pressure）

**Date:** 2026-02-28
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

`unknowns` が残っている状態で期限圧力が高いとき、Po_core は recommendation を強く断定させるのではなく、
「被害拡大を防ぎつつ判断確度を上げる行動支援」を優先する必要がある。

既存方針（ADR-0006, ADR-0008）では recommendation 裁定は policy_v1 の専権であり、
generator/planning/ethics/responsibility が裁定へ介入しないことが前提となっている。

## Decision

unknowns × time pressure 条件では、planning（generator）が **Two-Track Plan** を action_plan に出力する。

- Trigger:
  - `unknowns_count > 0`
  - `days_to_deadline` が整数
  - `days_to_deadline <= TIME_PRESSURE_DAYS`（policy_v1 定義の圧力閾値）
- Output:
  - Track A（可逆・低リスクの即応）
  - Track B（unknowns解消のための情報収集）
  - 順序は決定論で `Track A -> Track B`
  - `unknowns_items` がある場合は Track B に優先反映
- Non-Interference:
  - recommendation の `status / recommended_option_id / arbitration_code` は変更しない

## Rationale

- 期限圧力下で recommendation を断定しすぎるリスクを避ける
- 不確実性を放置せず、判断可能状態に収束させる
- 既存の policy専権（recommendation）と責務分離を維持できる

## Consequences

- action_plan は状況依存で Two-Track 形式に置換される（generic feature path）
- planning rule_id（`PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN`）を trace で観測可能にする
- golden には Two-Track の決定論出力が固定される

## Non-Goals

- recommendation 裁定ロジックの変更
- deadline圧力閾値（`TIME_PRESSURE_DAYS`）そのものの変更
- parse_input での追加判断（parse_input は観測のみ）
