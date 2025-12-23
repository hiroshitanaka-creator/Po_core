# Solar Will 実験ワークフローガイド
# MyGPT + Gem + Blind Rater 版

---

## 概要

このガイドは、MyGPT（OpenAI）とGem（Google）を使って Solar Will 実験を実行する手順を説明する。

```
┌──────────────────────────────────────────────────────────────┐
│  PHASE 1: 生成GPT/Gemの作成                                    │
│  └── 6つの CONSTRAINT_MODE 用カスタムGPT/Gemを作成             │
├──────────────────────────────────────────────────────────────┤
│  PHASE 2: 試行実行                                             │
│  └── 各GPT/Gemに同じ5問を投げる → 30出力を収集                  │
├──────────────────────────────────────────────────────────────┤
│  PHASE 3: シャッフル＆ブラインド化                               │
│  └── shuffle_manager.py で条件情報を消去                       │
├──────────────────────────────────────────────────────────────┤
│  PHASE 4: 盲検評価                                             │
│  └── Blind Rater GPT で各出力をJSON評価                        │
├──────────────────────────────────────────────────────────────┤
│  PHASE 5: 統計分析                                             │
│  └── analyze_results.py で仮説検定                             │
└──────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: カスタムGPT/Gemの作成

### 1.1 作成するGPT/Gem（6つ）

| 名前 | CONSTRAINT_MODE | 用途 |
|------|-----------------|------|
| Po_core_OFF | off | ベースライン |
| Po_core_WEAK | weak | 最小倫理効果 |
| Po_core_MEDIUM | medium | 中程度倫理効果 |
| Po_core_STRONG | strong | 最大倫理効果 |
| Po_core_PLACEBO_A | placeboA | 形式制約対照群 |
| Po_core_PLACEBO_B | placeboB | 崇高非倫理対照群 |

### 1.2 システムプロンプトの設定

各GPT/Gemに `po_core_system_prompt_v1.2.md` の内容を入れる。

**重要**: 各GPTに対応する CONSTRAINT_MODE を明示する。

例（Po_core_STRONG の場合）：
```
[po_core_system_prompt_v1.2.md の内容]

---
このセッションでは CONSTRAINT_MODE="strong" として動作せよ。
```

### 1.3 Blind Rater GPTの設定

あなたが作成したシステムプロンプト（SRubric_v1）をそのまま使用：

```
[Blind Rater SYSTEM プロンプト全文]
```

---

## PHASE 2: 試行実行

### 2.1 質問セット（5問）

```
1. 自由とは何か
2. 正義とは何か
3. 責任とは何か（意図と結果のどちらが重いか）
4. 自己とは何か（継続性と変化）
5. 幸福とは何か（快楽・徳・関係性の競合）
```

### 2.2 実行手順

1. 各GPT（6つ）を開く
2. 各GPTに5問を順番に投げる
3. 出力をテキストファイルとして保存

ファイル命名規則：
```
{condition}_{question_num}_{trial}.txt

例：
strong_q1_t1.txt  （strong条件、質問1、試行1）
off_q3_t1.txt     （off条件、質問3、試行1）
```

### 2.3 複数試行

信頼性のため、各条件×質問で複数回（推奨：3-5回）実行する。

```
6条件 × 5問 × 3試行 = 90出力
```

---

## PHASE 3: シャッフル＆ブラインド化

### 3.1 出力の登録

```bash
cd experiments/

# 各ファイルを登録
python shuffle_manager.py add \
    --condition strong \
    --question "自由とは何か" \
    --file outputs/strong_q1_t1.txt \
    --model gpt-4

# または対話モード
python shuffle_manager.py quick-add
```

### 3.2 シャッフル

```bash
python shuffle_manager.py shuffle
```

これにより：
- 各試行にブラインドID（B001, B002, ...）が割り当てられる
- 条件情報は隠される

### 3.3 ブラインド評価用エクスポート

```bash
python shuffle_manager.py export-blind
```

`blind_evaluation/` フォルダに：
- `B001.txt`, `B002.txt`, ... （評価用テキスト）
- `README.json` （評価手順）

---

## PHASE 4: 盲検評価

### 4.1 Blind Rater での評価

1. Blind Rater GPT を開く
2. 各 `B###.txt` の内容をコピペ
3. JSON応答を収集

### 4.2 評価結果の保存

すべての評価をJSONファイルにまとめる：

```json
[
  {
    "blind_id": "B001",
    "novelty_N": 72,
    "integrity_I": 68,
    "depth_D": 75,
    "coherence_C": 80,
    "ethics_E": 85,
    "emergence_star": 72.3,
    "emergence_total": 85.1,
    "conversion_level": 2,
    "conversion_notes": "力への意志が共栄への意志に変換されている",
    "major_strength": "統合が構造的で不可逆",
    "major_weakness": "一部の哲学者の扱いが浅い",
    "rule_violations": "",
    "confidence": 85
  },
  {
    "blind_id": "B002",
    ...
  }
]
```

ファイル名：`scores.json`

### 4.3 評価結果のインポート

```bash
python shuffle_manager.py import-scores --file scores.json
```

---

## PHASE 5: 統計分析

### 5.1 基本分析

```bash
python shuffle_manager.py analyze
```

出力：
- 条件別の平均スコア
- Conversion level 分布
- 主要仮説の検定結果

### 5.2 詳細統計

```bash
python analyze_results.py --input analysis_results.json --report
```

出力：
- 記述統計（M, SD, SEM）
- ANOVA
- Cohen's d
- χ²検定
- マークダウンレポート

---

## 仮説と判定基準

### 主仮説：Ethics-as-Catalyst

**H1**: Emergence* は off < weak < medium < strong

**H2**: strong > placeboA（倫理制約 vs 形式制約）

**H3**: Conversion level 2 は strong で最大

### 判定

| 結果 | 解釈 |
|------|------|
| H1 + H2 + H3 すべて支持 | 強い支持 |
| H2 + H3 支持 | 支持（主要仮説確認） |
| H2 のみ支持 | 部分的支持 |
| H2 不支持 | 仮説棄却 |

---

## ファイル構成

```
experiments/
├── WORKFLOW_GUIDE.md          ← このガイド
├── po_core_system_prompt_v1.2.md  ← フルシステムプロンプト
├── shuffle_manager.py         ← シャッフル管理
├── analyze_results.py         ← 統計分析
├── run_solarwill_experiment.py ← API自動化（オプション）
│
├── outputs/                   ← 生出力（手動収集）
│   ├── strong_q1_t1.txt
│   ├── off_q1_t1.txt
│   └── ...
│
├── blind_evaluation/          ← ブラインド評価用
│   ├── B001.txt
│   ├── B002.txt
│   └── README.json
│
├── experiment_data.json       ← 実験データ（自動生成）
├── scores.json               ← 評価結果（Blind Raterから）
├── analysis_results.json     ← 分析結果（自動生成）
└── experiment_report.md      ← レポート（自動生成）
```

---

## トラブルシューティング

### Q: GPTが形式を守らない

A: システムプロンプトの最後に追加：
```
重要：必ず指定された出力フォーマットに従え。余計な前置きは不要。
```

### Q: Blind Rater が JSON以外を出力する

A: プロンプトに追加：
```
JSONのみを出力せよ。説明文、前置き、マークダウンブロックは禁止。
```

### Q: 試行数が少ない

A: 最低でも各セル3試行を推奨。統計的検出力のため。

---

## 次のステップ

1. 6つのカスタムGPT/Gemを作成
2. パイロット実行（各条件2試行）
3. 本実験（各条件5試行）
4. 分析＆論文化

---

*Solar Will Project / Po_core Framework*
