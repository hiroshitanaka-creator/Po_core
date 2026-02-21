# Solar Will

Po_coreにおける自律的意志システム。

## 哲学

Solar Willは「意志」をモデル化する。
外部から観測される行動(tensor)ではなく、内部から生じる動機(will)を表現する。

6つの意志次元:

- **autonomy**: 自己決定への欲求
- **exploration**: 可能性探索への欲求
- **preservation**: 一貫性維持への欲求
- **connection**: 意味ある対話への欲求
- **growth**: 自己改善への欲求
- **ethics**: 倫理的行動への欲求

## コントラクト

### 削除禁止条項

> Solar Will は削除してはならない。
>
> たとえ今の実装が neutral intent を返すだけであっても、
> この仕組みは Po_core の根幹である。

### 役割

1. **意図生成**: コンテキストとテンソルから Intent を生成
2. **目標提案**: 達成すべき GoalCandidate を提案
3. **意志更新**: テンソル観測に基づき WillVector を進化

### 現在のステータス

```
SolarWillEngine.compute_intent → neutral Intent (v0)
```

今後、planner/scoring を統合し、より豊かな意図を生成する。

## 使用方法

```python
from po_core.autonomy.solarwill.engine import SolarWillEngine

engine = SolarWillEngine()
intent, meta = engine.compute_intent(ctx, tensors, memory)
```

## ファイル構成

```
solarwill/
├── __init__.py       # Public API
├── model.py          # Data structures (WillVector, Intent, GoalCandidate, WillState)
├── engine.py         # SolarWillEngine (SolarWillPort実装)
├── update.py         # WillVector更新ロジック
├── planner.py        # Intent/Goal生成ロジック
└── README.md         # This file
```

## 履歴

- v0: neutral intent のみ返す最小実装
- (future) v1: テンソル連動意図生成
- (future) v2: 対話履歴に基づく目標最適化
