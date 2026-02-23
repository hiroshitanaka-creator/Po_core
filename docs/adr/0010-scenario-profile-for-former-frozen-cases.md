# ADR-0010: case_001/case_009 の short_id 特例を scenario_profile feature へ移管

- Status: Accepted
- Date: 2026-02-23
- Supersedes: ADR-0004/0006/0007/0008/0009 における「case_001/case_009 は short_id 分岐で固定」記述

## Context

従来は `case_001` / `case_009` を `short_id` で直接分岐し、出力を固定していた。
この方式は「ファイル名/ID依存の永久特例」であり、features→rules の設計原則に反する。

## Decision

- 入力 `extensions.scenario_profile` を仕様上の明示シグナルとして利用する。
- `parse_input.extract_features()` で `features.scenario_profile` を抽出する。
- 各 engine / tracer の特例は `short_id` ではなく `features.scenario_profile` で分岐する。
  - `job_change_transition_v1`（旧 case_001 特例相当）
  - `values_clarification_v1`（旧 case_009 特例相当）
- `case_001.yaml` / `case_009.yaml` は上記 profile を明示する。

## Consequences

- 「ファイル名依存」から「入力仕様として明示」へ移行できる。
- 同じ profile を持つ新規ケースでも同ルールを再利用可能になる。
- `case_001` / `case_009` の出力は regenerate により再固定し、golden diff で監視する。
- CI では `case_001/009` 向け `short_id` 直分岐の再導入を禁止するテストを追加する。
