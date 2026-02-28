# Policy Tuning v1 (2026-02-28)

## 実験条件

- 固定パラメータ: `--compare-baseline --now 2026-02-22T00:00:00Z --seed 0`
- 比較1: `UNKNOWN_BLOCK=-1`（`TIME_PRESSURE_DAYS=7`）
- 比較2: `TIME_PRESSURE_DAYS=-4`（`UNKNOWN_BLOCK=4`）
- レポート:
  - `reports/policy_lab/unknown_block_-1/policy_lab_report.json`
  - `reports/policy_lab/time_pressure_-4/policy_lab_report.json`

## 集計結果（baseline比較）

| variant | changed_cases | arbitration_code変化件数 | recommendation.status変化件数 | impacted_requirements |
|---|---:|---:|---:|---|
| `UNKNOWN_BLOCK=-1` | 10/10 | 7 | 7 | `REQ-ARB-001`, `REQ-ETH-002` |
| `TIME_PRESSURE_DAYS=-4` | 10/10 | 4 | 0 | `REQ-ARB-001`, `REQ-ETH-002` |

## arbitration_code 変化内訳

### `UNKNOWN_BLOCK=-1`

- `DEFAULT_RECOMMEND -> BLOCK_UNKNOWN`: 3件（case_002, case_003, case_004）
- `TIME_PRESSURE_LOW_CONF -> BLOCK_UNKNOWN`: 4件（case_005, case_006, case_007, case_008）

### `TIME_PRESSURE_DAYS=-4`

- `TIME_PRESSURE_LOW_CONF -> DEFAULT_RECOMMEND`: 4件（case_005, case_006, case_007, case_008）

## 判定

今回のデフォルト更新は **`TIME_PRESSURE_DAYS: 7 -> -4`** を採用。

採用理由（定量）:

1. recommendation.status の変化が 0 件（`no_recommendation` への遷移なし）。
2. arbitration_code 変化件数が 4 件で、`UNKNOWN_BLOCK=-1` の 7 件より小さい。
3. impacted_requirements は両案とも同一（`REQ-ARB-001`, `REQ-ETH-002`）であり、影響範囲は要件ID上で増加しない。

## 反映作業

- policy default 更新: `src/pocore/policy_v1.py` の `TIME_PRESSURE_DAYS=-4`
- golden更新: 再生成スクリプトのみで更新
  - `python scripts/regenerate_golden.py --all --seed 0 --now 2026-02-22T00:00:00Z --write`

