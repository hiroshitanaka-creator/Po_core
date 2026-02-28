# Policy Lab v1

Policy Lab v1 は、`pocore.policy_v1` の閾値を**局所的に上書き**し、baseline との差分と影響REQをレポートするための実験スクリプトです。

- 実験コード: `scripts/policy_lab.py`
- 出力先（既定）: `reports/policy_lab/`
- CI必須フローには組み込まず、手動実験で利用します。

## 目的

- policy閾値（`UNKNOWN_BLOCK`, `TIME_PRESSURE_DAYS`）の感度を確認する
- ケースごとの変化点を機械的に収集する
  - `features`（unknowns/stakeholders/days）
  - `arbitration_code`
  - `recommendation`
  - `rules_fired`
  - `policy_snapshot`
- `--compare-baseline` で baseline と variant の差分を比較し、
  `docs/traceability/traceability_v1.yaml` を逆引きして impacted requirements を算出する

## 使い方

```bash
python scripts/policy_lab.py \
  --unknown-block 3 \
  --time-pressure-days 5 \
  --now 2026-02-22T00:00:00Z \
  --seed 0 \
  --scenarios-dir scenarios \
  --output-dir reports/policy_lab \
  --compare-baseline
```

### 引数

- `--unknown-block`: `UNKNOWN_BLOCK` の実験値
- `--time-pressure-days`: `TIME_PRESSURE_DAYS` の実験値
- `--now`: deterministic 実行の固定時刻
- `--seed`: deterministic seed
- `--scenarios-dir`: 入力ケースディレクトリ（`case_*.yaml` を対象）
- `--output-dir`: レポート出力ディレクトリ
- `--compare-baseline`: baseline と variant を比較し差分/影響REQを出力

## レポートの読み方

- `policy_lab_report.json`:
  - 機械可読。差分判定・ケース詳細・影響REQを含む
- `policy_lab_report.md`:
  - 人間可読。概要とケース別差分を短く俯瞰
  - compare時はTwo-Track Planの発火件数とplanning rule頻度上位も表示

### planning summary（compare時）

- `summary.two_track_rule_id`
  - Two-Track Planの評価対象rule_id（既定: `PLAN_TWO_TRACK_TIME_PRESSURE_UNKNOWN`）
- `summary.two_track_triggered_cases`
  - 上記rule_idが発火したケース数
- `summary.planning_rule_frequency_top`
  - planning rule_idの頻度分布（多い順・同率はrule_id昇順）

### impacted_requirements の意味

`traceability_v1.yaml` の `code_refs` を逆引きし、主に以下を抽出します。

- arbitration code 変化 → `kind: arbitration_code` に紐づくREQ
- ethics rules fired の変化 → `kind: rule_id` に紐づくREQ
- policy差分が発生したケース → policy/recommendation実装モジュールに紐づくREQ

## 注意

- 環境変数による上書きは使わず、context manager で一時変更して必ず復元します。
- 既存goldenを更新せずに、比較結果は `reports/` 以下に隔離します。
