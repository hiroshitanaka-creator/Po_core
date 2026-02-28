# ADR 0014: Values Clarification Pack v1（values_empty）

**Date:** 2026-02-28
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

`values_empty == True` の入力では recommendation policy（ADR-0006）により裁定は `NO_VALUES` となる。
一方で、裁定を変えずに「価値軸を獲得する手続き」を提示しないと、
利用者は次に何をすべきか不明瞭なまま停止しやすい。

Po_core の責務境界（parse_input=観測、engines=ルール、recommendation=裁定専権）を保ちつつ、
values が空の状態を行動可能なプロトコルへ変換する必要がある。

## Decision

generic feature path で `features.values_empty == True` のとき、
**Values Clarification Pack v1** を適用する。

- Questions:
  - 価値軸獲得の質問を最大5件、決定論順序で出力する
  - 安定 `question_id` を持つ（例: `q_values_axis_1`）
  - rule_id: `Q_VALUES_CLARIFICATION_PACK_V1`
- Planning:
  - 各 option の `action_plan` を「10分で価値軸を作るミニ手順」（最大5ステップ）に置換する
  - rule_id: `PLAN_VALUES_CLARIFICATION_PACK_V1`
- Ethics:
  - `guardrails` に「価値軸が空のまま推奨を断言しない」を追加する
  - rule_id: `ETH_VALUES_EMPTY_CLARIFICATION`
- Non-interference:
  - recommendation の `status / recommended_option_id / arbitration_code` は変更しない

## Rationale

- recommendation への非介入を維持したまま、利用者の次行動を具体化できる
- values空状態に対して case分岐ではなく features→rules で一般化できる
- rule_id を持たせることで traceability と coverage の検証が可能になる

## Consequences

- values_empty の generic ケースで、questions/action_plan/guardrails が決定論的に強化される
- planning trace から `PLAN_VALUES_CLARIFICATION_PACK_V1` を観測できる
- execution coverage の must-cover planning rule に本ruleを追加する

## Non-Goals

- recommendation policy閾値や裁定順序の変更
- frozen profile（case_001/case_009）の契約出力変更
- parse_input に価値判断ロジックを追加すること
