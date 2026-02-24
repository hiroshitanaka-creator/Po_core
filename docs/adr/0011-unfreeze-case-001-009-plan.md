# ADR-0011: case_001 / case_009 凍結解除計画（J0/J1）

- Status: Accepted
- Date: 2026-02-24
- Depends on: ADR-0002, ADR-0003, ADR-0010

## Context

`case_001_expected.json` / `case_009_expected.json` は凍結契約として運用され、
不用意なgolden改変を防いできた。
一方で、これは「永久特例」を温存し続ける負債にもなる。

- 仕様進化（features/rules/trace改善）が正当でも、凍結だけを理由に反映できない。
- “仕様変更の正当性” と “更新手順の安全性” が分離されないまま、
  手動更新に依存すると説明責任が崩れる。

よって、凍結解除は **無秩序な更新** ではなく、
手順と受け入れ条件を明示した計画（J0/J1）として固定する。

## Decision

### 1) 二段階で解除する

- **J0（本ADRの段階）**
  - 凍結解除の方針をADRで固定する。
  - golden再生成を機械的に行うスクリプトを導入する。
  - この段階では `case_001_expected.json` / `case_009_expected.json` を変更しない。
- **J1（実更新段階）**
  - J0で導入したスクリプトで `case_001/009` を再生成し、差分レビューの上で更新する。
  - 更新後はE2E・非介入・決定性・trace契約を満たすことを確認する。

### 2) 凍結解除の受け入れ条件（J1）

J1で `case_001_expected.json` / `case_009_expected.json` を更新する場合、以下を必須条件とする。

1. **E2E契約**
   - `pytest -q` が全通する。
   - `tests/test_golden_e2e.py` の canonical比較で差分が説明可能である。
2. **非介入契約**
   - ethicsガードレールが recommendation裁定を不当に改変していないこと（既存非介入テストを維持）。
3. **決定性契約**
   - `seed=0`, `deterministic=True`, 固定 `now` で再実行して同一JSONが得られる。
4. **trace契約**
   - trace時刻・steps順序・compose_output metrics（arbitration_code含む）が契約どおりである。

### 3) expected更新ルール

- `*_expected.json` の更新は **必ず再生成スクリプトで行う**。
- 手編集（手打ち修正・整形のみ変更・キー順操作）は禁止。
- スクリプトは dry-run で差分を確認し、明示フラグなしでは上書きしない。

## Consequences

- 凍結解除を「例外運用」ではなく、監査可能な手順として管理できる。
- J1以降は差分理由をADR/テスト/traceで説明できるため、
  golden更新の安全性と説明責任を両立できる。
- 手編集禁止により、仕様起因でないノイズ差分を削減できる。
