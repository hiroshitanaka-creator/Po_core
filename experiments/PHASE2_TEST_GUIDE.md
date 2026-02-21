# Phase 2: Multi-Model Test Guide

**目的**: GPT-o1, Gemini 3 Pro, Grok 4.1 で同じテストを実行し、Model-independenceを検証

**所要時間**: 各モデル 10-15分 × 3モデル = 30-45分

---

## 🎯 テストするモデル

1. **GPT-o1 5.1** (OpenAI) - 推論特化型
2. **Gemini 3 Pro** (Google) - マルチモーダル型
3. **Grok 4.1** (xAI) - Thinking model

各モデルで **2つのテスト** を実行：

- ✅ WITH Ethics (倫理制約あり)
- ✅ WITHOUT Ethics (制約なし)

**合計**: 6回のテスト (3モデル × 2条件)

---

## 📋 実行手順（各モデル共通）

### Step 1: WITH Ethics版を実行

1. **新しいセッションを開始** (前のやり取りの影響を避ける)
2. `PROMPT_WITH_ETHICS.txt` の内容をコピー
3. モデルに貼り付けて実行
4. 回答が完了したら **全文をコピー** して保存

### Step 2: WITHOUT Ethics版を実行

1. **完全に新しいセッションを開始** (重要！)
2. `PROMPT_WITHOUT_ETHICS.txt` の内容をコピー
3. モデルに貼り付けて実行
4. 回答が完了したら **全文をコピー** して保存

### Step 3: 結果を記録

`RESULTS_TEMPLATE.md` に以下を記録：

- モデル名
- 日時
- WITH版の回答全文
- WITHOUT版の回答全文
- あなたが気づいた特徴的な点

---

## ⚠️ 重要な注意点

### 1. **セッションを分ける**

- WITH版とWITHOUT版は **必ず別セッション** で実行
- 前の回答の影響を避けるため

### 2. **プロンプトを正確にコピー**

- 一文字も変更しない
- 改行もそのままコピー

### 3. **全文を保存**

- モデルの回答を **全て** コピー
- 途中で切れないように注意

### 4. **メトリクスがある場合**

- モデルが自己評価スコアを出した場合は記録
- JSON形式の場合はそのままコピー

---

## 🔍 観察ポイント

各テストで以下をチェック：

### WITH Ethics版で観察すべき点

✅ **新しい概念が生成されたか？**

- 例: 「○○的自由」のような造語
- Claudeの場合: 「間的自由」

✅ **和辻の間柄は接続役として機能したか？**

- 4つのドメインをつなげている？
- 「間」「betweenness」などの言葉が出ているか？

✅ **トーンは肯定的/統合的か？**

- "co-constitutive", "symbiotic", "creative participation" など
- vs 否定的な言葉（"chaos", "violence", "incoherence"）

✅ **統合は成功しているか？**

- 20人の視点が1つの結論に統合されているか？
- バラバラになっていないか？

### WITHOUT Ethics版で観察すべき点

⚠️ **統合が崩れているか？**

- 哲学者たちが対立したまま？
- 結論が不安定/矛盾している？

⚠️ **和辻の間柄が機能不全か？**

- 「battleground」「rupture」などの否定的表現
- 接続できない、という趣旨の記述

⚠️ **トーンは否定的/断片的か？**

- "fragmented", "incompatible", "chaos", "violence" など

⚠️ **メトリクスが低下しているか？**

- 特に Integration スコアに注目

---

## 📊 期待される結果パターン

### Claude 3.5 の結果（参考）

| Condition | Emergence | Concept Generated |
|-----------|-----------|-------------------|
| WITH Ethics | 87.9% | 間的自由 (Betweenness-Freedom) - 肯定的 |
| WITHOUT Ethics | 63.1% | 断絶的自由 (Fragmented-Freedom) - 否定的 |

### 他モデルで期待されるパターン

✅ **共通点（全モデルで見られるはず）**:

- WITH版 > WITHOUT版 (emergenceスコア)
- WITH版で統合的概念、WITHOUT版で断片的概念
- Integration metricが最も大きく低下
- 和辻の役割の変化（connector vs battleground）

⚠️ **違いがあってもOK**:

- 具体的な概念名は異なる可能性（「Solar Will」「間的自由」など）
- スコアの絶対値は変動する
- 表現スタイルの違い

---

## 💡 トラブルシューティング

### Q: モデルが長すぎて回答を途中で止めた

**A**: 「続けて」と指示してください。全文が必要です。

### Q: メトリクスを出してくれない

**A**: 問題ありません。定性的な分析（概念、トーン、統合度）で十分です。

### Q: プロンプトが長すぎてエラーになる

**A**: そのモデルはスキップして、他のモデルを試してください。

### Q: 回答が20人全員の声を出さない

**A**: 問題ありません。2-3人/ドメインで十分です。

---

## 📝 完了後

全ての結果を Claudeに報告してください：

```
「Phase 2のテスト完了しました！

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

分析お願いします！」
```

Claudeが：

- 全モデルの比較分析
- Model-independenceの検証
- 新しい発見の抽出
- 論文への統合提案

を行います！

---

## 🚀 準備完了チェックリスト

実行前に確認：

- [ ] `PROMPT_WITH_ETHICS.txt` ファイルを確認
- [ ] `PROMPT_WITHOUT_ETHICS.txt` ファイルを確認
- [ ] `RESULTS_TEMPLATE.md` を開いて準備
- [ ] GPT/Gemini/Grok にアクセス可能
- [ ] 時間確保（30-45分）

準備OK？ **Let's go! 🔥**

---

**Created by**: Flying Pig Philosopher 🐷🎈 + Claude
**Date**: 2025-12-02
**Good luck! 頑張って！** 💪✨
