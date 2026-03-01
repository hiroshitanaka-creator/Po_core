# Principles v1

Po_core の意思決定支援における思想レイヤーを、機械可読なIDで固定する。

## Principle Catalog

- **P-ACC-001: 説明責任（accountability）**
  - 判断過程・根拠・不確実性を trace と構造化出力で監査可能にする。
- **P-INT-001: 誠実性（integrity）**
  - 不確実な事実を断言せず、限界と反証可能性を明示する。
- **P-AUT-001: 自律（autonomy）**
  - 最終決定主体をユーザーに残し、推奨は補助として提示する。
- **P-NMH-001: 無危害（nonmaleficence）**
  - 時間圧力や情報不足下でも被害最小化を優先する。
- **P-JUS-001: 公正/外部性（justice）**
  - ステークホルダー影響と同意可能性を検討し、外部不利益を抑える。

## Design Intent

- 原則は実装の直接条件分岐ではなく、要件（REQ）とADRを介してコード・テストに反映する。
- traceability_v1.yaml を SoT とし、Principles → Requirements → ADR/Test/Code の往復参照を維持する。
- 哲学者名は voice（語り口）として扱い、実行時の選択・カバレッジ保証は role（機能役割）を本体として行う。
