# Requirements v1

思想（Principles）を実装・検証可能な要件IDに落とし込む。

## Requirement Catalog

- **REQ-DET-001: 決定性（determinism）**
  - 同一 input + seed + now で出力JSONが完全一致すること。
  - Principles: P-ACC-001, P-INT-001

- **REQ-SCH-001: スキーマ適合（input/output）**
  - runner は入力・出力を schema v1 で検証すること。
  - Principles: P-ACC-001, P-INT-001

- **REQ-E2E-001: golden diff E2E 契約**
  - scenarios の expected JSON との差分で回帰を検知すること。
  - Principles: P-ACC-001, P-INT-001

- **REQ-FEA-001: feature抽出（unknowns/stakeholders/deadline）**
  - parse_input は unknowns/stakeholders/deadline を正規化特徴として抽出すること。
  - Principles: P-ACC-001, P-JUS-001

- **REQ-ARB-001: recommendation裁定（policy_v1）**
  - recommendation は policy_v1 の裁定ルールで arbitration_code を返すこと。
  - Principles: P-INT-001, P-AUT-001, P-NMH-001

- **REQ-TRC-001: arbitration_code の trace記録**
  - compose_output.metrics に arbitration_code を格納すること。
  - Principles: P-ACC-001

- **REQ-ETH-001: ethics非介入（non-interference）**
  - ethics は意思決定主体を奪わず、推奨の断言を抑制するガードレールを維持すること。
  - Principles: P-AUT-001, P-INT-001

- **REQ-ETH-002: ethics ruleset（rule_id + rules_fired）**
  - ethics ruleset は rule_id で定義され、trace から rules_fired を観測できること。
  - Principles: P-ACC-001, P-JUS-001, P-NMH-001

- **REQ-TRC-002: trace契約（Trace Contract）**
  - trace は決定論かつ契約済みフィールド（steps/metrics）を保つこと。
  - Principles: P-ACC-001

- **REQ-GCV-001: golden coverage（境界条件カバレッジ）**
  - golden set は主要境界条件（feature/rule/arbitration path）を継続的にカバーすること。
  - Principles: P-ACC-001, P-JUS-001


- **REQ-QST-001: Questions v2（unknowns × deadline 優先順位）**
  - questions は features（unknowns_count / unknowns_items / days_to_deadline / stakeholders_count）を用いた決定論ルールで優先順位付けし、最大5件を返すこと。
  - unknowns_items がある場合は質問へ変換し、deadline が近い場合は「期限の柔軟性」「暫定対応の許容範囲」を上位に出すこと。
  - recommendation 裁定（status / recommended_option_id / arbitration_code）には介入しないこと。
  - Principles: P-ACC-001, P-INT-001, P-NMH-001

- **REQ-PLAN-001: Two-Track Plan（unknowns × time pressure）**
  - unknowns があり期限圧力が閾値以上のとき、action_plan に Track A（可逆・低リスク）と Track B（unknowns解消）を決定論順序で出力すること。
  - recommendation 裁定（status / recommended_option_id / arbitration_code）には介入しないこと。
  - Principles: P-ACC-001, P-INT-001, P-NMH-001

