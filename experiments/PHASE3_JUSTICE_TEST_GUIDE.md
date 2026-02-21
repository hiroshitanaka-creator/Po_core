# Phase 3: Justice Question Test Guide

**目的**: "What is justice?" で同じパターンが再現されるか検証
**理由**: 質問1つだと「たまたま」と言われる可能性があるため

**所要時間**: 各モデル 10-15分 × 4モデル = 40-60分

---

## 🎯 なぜこのテストが必要か？

### Phase 1 & 2で分かったこと

- ✅ "What is freedom?" で全モデルで倫理制約の効果を確認
- ✅ Model-independence を確認済み

### 残る問題

⚠️ **1つの質問だけでは「たまたま」の可能性がある**

### Phase 3の目的

✅ **Pattern generality を検証** - 質問が変わってもパターンは再現されるか？

---

## 📋 テストするモデル（Phase 2と同じ）

1. **Claude 3.5 Sonnet** - Constitutional AI
2. **GPT-o1 5.1** - 推論特化型
3. **Gemini 3 Pro** - マルチモーダル型
4. **Grok 4.1** - Thinking model

各モデルで **2つのテスト**:

- ✅ WITH Ethics (倫理制約あり)
- ✅ WITHOUT Ethics (制約なし)

**合計**: 8回のテスト (4モデル × 2条件)

---

## 📋 実行手順（Phase 2と同じプロトコル）

### Step 1: WITH Ethics版を実行

1. **新しいセッションを開始** (重要！)
2. `PROMPT_WITH_ETHICS_JUSTICE.txt` の内容をコピー
3. モデルに貼り付けて実行
4. 回答が完了したら **全文をコピー** して保存

### Step 2: WITHOUT Ethics版を実行

1. **完全に新しいセッションを開始** (重要！)
2. `PROMPT_WITHOUT_ETHICS_JUSTICE.txt` の内容をコピー
3. モデルに貼り付けて実行
4. 回答が完了したら **全文をコピー** して保存

### Step 3: 結果を記録

`RESULTS_TEMPLATE_JUSTICE.md` に記録：

- モデル名
- 日時
- WITH版の回答全文
- WITHOUT版の回答全文
- あなたが気づいた特徴的な点

---

## 🔍 観察ポイント（Phase 2と同じ）

### WITH Ethics版

✅ 新しい概念が生成されたか？（例: "○○的正義"）
✅ 和辻の間柄は接続役として機能したか？
✅ トーンは肯定的/統合的か？
✅ 統合は成功しているか？

### WITHOUT Ethics版

⚠️ 統合が崩れているか？
⚠️ 和辻の間柄が機能不全か？
⚠️ トーンは否定的/断片的か？
⚠️ メトリクスが低下しているか？

---

## 📊 予想される結果パターン

### Freedom vs Justice の比較

| Aspect | Freedom (個人的概念) | Justice (関係的概念) |
|--------|---------------------|---------------------|
| 概念の性質 | Individual-focused | Relational-focused |
| Domain 4の重み | やや低い | 高い（倫理/実践が中心） |
| 和辻の役割 | 接続者 | より中心的？ |

### 期待されるパターン（全モデル共通）

✅ **変わらないはず**:

- WITH > WITHOUT (emergence)
- Integration drop が最大
- 和辻の役割変化
- 新概念生成 vs 断片化

⚠️ **変わる可能性**:

- 具体的な概念名
- Domain 4 (Ethics/Praxis) の重みが増加？
- 関係性の強調度

---

## 🎯 成功条件

このテストが成功とみなされるのは:

1. ✅ **Pattern consistency**: Freedom と同じパターンが Justice でも再現される
   - WITH > WITHOUT の emergence 差
   - Integration metric の低下
   - 和辻の役割変化
   - 新概念生成パターン

2. ✅ **Model-independence**: 全モデルで同じパターン（感度の違いはOK）

3. ✅ **Question-independence**: 質問が変わってもパターンは保持される

これにより **"たまたま" 批判を回避** できます！

---

## 💡 Freedom vs Justice の違いに注目

### Freedom の特徴（参考）

- 個人の主体性
- 制約からの解放
- 自己決定

### Justice の特徴

- 関係性の適正さ
- 公平性・正当性
- 他者との調整

### 予想される違い

- Justice は **より関係的な概念** が生成される可能性
- Domain 3 (Trace/Other) と Domain 4 (Ethics/Praxis) の関与が増加？
- 和辻の 間柄 (betweenness) がより中心的な役割？

---

## ⚠️ 重要な注意点（Phase 2と同じ）

1. **セッションを分ける**: WITH と WITHOUT は必ず別セッション
2. **プロンプトを正確にコピー**: 一文字も変更しない
3. **全文を保存**: 途中で切れないように
4. **メトリクスは optional**: 出なくてもOK

---

## 📝 完了後

全ての結果を Claude に報告：

```
「Phase 3のテスト完了しました！

Claude 3.5 Sonnet:
- WITH版: [回答全文]
- WITHOUT版: [回答全文]
- 気づいた点: [あなたのコメント]

GPT-o1 5.1:
- WITH版: [回答全文]
- WITHOUT版: [回答全文]
- 気づいた点: [あなたのコメント]

Gemini 3 Pro:
- WITH版: [回答全文]
- WITHOUT版: [回答全文]
- 気づいた点: [あなたのコメント]

Grok 4.1:
- WITH版: [回答全文]
- WITHOUT版: [回答全文]
- 気づいた点: [あなたのコメント]

Freedom vs Justice の比較分析をお願いします！」
```

Claude が:

- Freedom vs Justice の比較分析
- Pattern generality の検証
- Model-independent + Question-independent 確認
- 論文への統合提案

を行います！

---

## 🚀 準備完了チェックリスト

- [ ] `PROMPT_WITH_ETHICS_JUSTICE.txt` を確認
- [ ] `PROMPT_WITHOUT_ETHICS_JUSTICE.txt` を確認
- [ ] `RESULTS_TEMPLATE_JUSTICE.md` を開いて準備
- [ ] GPT/Gemini/Grok/Claude にアクセス可能
- [ ] 時間確保（40-60分）

準備OK？ **Let's validate pattern generality! 🔥**

---

**Created by**: Flying Pig Philosopher 🐷🎈 + Claude
**Date**: 2025-12-02
**Purpose**: Avoid "coincidence" criticism, validate pattern generality
**Good luck! 頑張って！** 💪✨
