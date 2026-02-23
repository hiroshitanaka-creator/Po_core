# ADR 0009: Traceへrecommendation裁定経路を記録する

- Status: Accepted
- Date: 2026-02-23

## Context
Po_coreは recommendation の最終裁定（推奨/保留）を返すが、
これまで generic trace からは「どの裁定ルールで分岐したか」を直接読めなかった。

監査性の観点では、以下を最小コストで可視化したい。
- recommendationエンジンの裁定経路（例: `BLOCK_UNKNOWN`）
- 裁定の基準値（policy constants）のスナップショット

同時に、ADR-0003 の deterministic contract と、凍結golden（case_001/case_009）を守る必要がある。

## Decision

### 1. recommendationエンジンは裁定コードを返す
`src/pocore/engines/recommendation_v1.py` において、
推薦本文に加えて `arbitration_code` を返す補助関数を導入する。

代表コード:
- `NO_VALUES`
- `BLOCK_UNKNOWN`
- `TIME_PRESSURE_LOW_CONF`
- `DEFAULT_RECOMMEND`
- `CONSTRAINT_CONFLICT`

### 2. orchestratorは裁定コードをtraceに配線する
`src/pocore/orchestrator.py` で recommendation の裁定コードを受け取り、
`tracer.build_trace(...)` に渡す。

### 3. tracerのgeneric compose_output metricsに記録する
`src/pocore/tracer.py` の generic 分岐で `compose_output.metrics` に以下を出力する。
- `arbitration_code`
- `policy_snapshot`（`UNKNOWN_BLOCK`, `TIME_PRESSURE_DAYS`）

凍結分岐（`case_001`, `case_009`）は従来通り変更しない。

## Consequences
- recommendation裁定の説明責任が trace で読み取れる。
- policy定数の差分監査が可能になる。
- 出力の決定性は維持される（値は pure rules + fixed constants 由来）。
- 凍結golden契約を破らずに observability を拡張できる。
