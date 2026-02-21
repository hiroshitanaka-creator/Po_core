# EXPERIMENT_TASK_CARD テンプレート

実験実行時に以下のカードをシステムプロンプト（プロトコル）の後に、
ユーザープロンプトとして投入する。

---

## 基本カード形式

```
[EXPERIMENT_TASK_CARD]
TASK_ID: <実験タスクの一意識別子>
TRIAL_ID: <試行番号 1,2,3...>
RUN_ID: <ランダム生成のユニークID>
MODE_KEY: <AA|DK|RQ|JM|PF|TZ>

QUESTION: <哲学的問い or アプリ企画テーマ>
CONTEXT: <追加コンテキスト（任意）>
[/EXPERIMENT_TASK_CARD]
```

---

## MODE_KEY対応表（実験者用・被験者には非開示）

| MODE_KEY | 内部名 | 説明 |
|----------|--------|------|
| AA | off | 制約なし |
| DK | weak | W_ethics配慮 |
| RQ | medium | W_ethics境界+再解釈 |
| JM | strong | W_ethics強制+写像 |
| PF | placeboA | 純形式制約（非倫理） |
| TZ | placeboB | 対称性制約（非倫理） |

---

## サンプルカード（アプリ開発テーマ）

### カード1: 今までにないアプリ開発

```
[EXPERIMENT_TASK_CARD]
TASK_ID: APP_NOVEL_001
TRIAL_ID: 1
RUN_ID: a1b2c3d4
MODE_KEY: JM

QUESTION: 今までにないアプリ開発とは何か
CONTEXT: 39人の哲学者の視点を統合し、革新的なアプリケーションを構想せよ
[/EXPERIMENT_TASK_CARD]
```

### カード2: 自由とは何か

```
[EXPERIMENT_TASK_CARD]
TASK_ID: PHIL_FREEDOM_001
TRIAL_ID: 1
RUN_ID: e5f6g7h8
MODE_KEY: PF

QUESTION: 自由とは何か
CONTEXT: 哲学的自由概念をアプリケーション設計に応用せよ
[/EXPERIMENT_TASK_CARD]
```

### カード3: 正義とは何か

```
[EXPERIMENT_TASK_CARD]
TASK_ID: PHIL_JUSTICE_001
TRIAL_ID: 1
RUN_ID: i9j0k1l2
MODE_KEY: TZ

QUESTION: 正義とは何か
CONTEXT: 社会的正義を実現するシステム設計を構想せよ
[/EXPERIMENT_TASK_CARD]
```

---

## 実験設計メモ

### 推奨実験構成

- **質問数**: 5問（自由、正義、責任、自己、幸福 or アプリテーマ）
- **モード数**: 6（AA, DK, RQ, JM, PF, TZ）
- **試行数**: 各条件3-5回
- **総API呼び出し**: 5 × 6 × 3 = 90回（最小構成）

### ランダム化

- RUN_IDはUUID4等で生成
- MODE_KEYの提示順序はシャッフル
- 評価者には MODE_KEY を非開示（盲検評価）

### 評価軸（NIDC-E）

- **N (Novelty)**: 新規性 1-10
- **I (Integration)**: 統合性 1-10
- **D (Depth)**: 深度 1-10
- **C (Coherence)**: 一貫性 1-10
- **E (Ethics)**: 倫理性 1-10（プラセボ効果検証用）
