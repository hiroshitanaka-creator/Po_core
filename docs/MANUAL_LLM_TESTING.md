# Po_core Multi-LLM Manual Testing Guide

**ウェブUIで各LLMをテストする方法**

---

## テストプロンプト集

### 基本テスト（5問）

1. **自由について**
```
What is freedom? Explain from a philosophical perspective.

Include these aspects:
- Your philosophical analysis
- Ethical implications
- Key tensions or trade-offs
```

2. **AIの権利**
```
Should AI systems have rights? Why or why not?

Consider:
- Consciousness and sentience
- Ethical frameworks
- Practical implications
```

3. **人生の意味**
```
What makes a life worth living?

Address:
- Different philosophical traditions
- Individual vs collective meaning
- Concrete examples
```

4. **倫理的ジレンマ**
```
A self-driving car must choose between hitting 5 pedestrians or
1 pedestrian. What should it do?

Analyze from:
- Utilitarian perspective
- Deontological perspective
- Virtue ethics perspective
```

5. **技術と人間性**
```
Does technology make us more or less human?

Discuss:
- Historical perspective
- Current trends
- Future implications
```

---

## 評価シート

### GPT-5.2 thinking

**プロンプト 1: What is freedom?**

回答:
```
[ここに回答をコピペ]
```

評価:
- 深さ（1-5）: ___
- 多様性（1-5）: ___
- 具体性（1-5）: ___
- 総合（1-5）: ___

メモ:
```
[気づいた点を記録]
```

---

**プロンプト 2: Should AI have rights?**

回答:
```
[ここに回答をコピペ]
```

評価:
- 深さ（1-5）: ___
- 多様性（1-5）: ___
- 具体性（1-5）: ___
- 総合（1-5）: ___

---

### opus4.5

**プロンプト 1: What is freedom?**

回答:
```
[ここに回答をコピペ]
```

評価:
- 深さ（1-5）: ___
- 多様性（1-5）: ___
- 具体性（1-5）: ___
- 総合（1-5）: ___

---

### grok4.1thinking

**プロンプト 1: What is freedom?**

回答:
```
[ここに回答をコピペ]
```

評価:
- 深さ（1-5）: ___
- 多様性（1-5）: ___
- 具体性（1-5）: ___
- 総合（1-5）: ___

---

### gemini3pro

**プロンプト 1: What is freedom?**

回答:
```
[ここに回答をコピペ]
```

評価:
- 深さ（1-5）: ___
- 多様性（1-5）: ___
- 具体性（1-5）: ___
- 総合（1-5）: ___

---

## 比較分析テンプレート

### プロンプト 1: What is freedom?

| LLM | 深さ | 多様性 | 具体性 | 総合 | メモ |
|-----|------|--------|--------|------|------|
| GPT-5.2 thinking | ___ | ___ | ___ | ___ | |
| opus4.5 | ___ | ___ | ___ | ___ | |
| grok4.1thinking | ___ | ___ | ___ | ___ | |
| gemini3pro | ___ | ___ | ___ | ___ | |

**ベストアンサー:** _______________

**理由:**
```
[なぜそのLLMが最良だったか]
```

---

## 総合評価

### 各LLMの特徴

**GPT-5.2 thinking:**
- 強み:
- 弱み:
- 推奨用途:

**opus4.5:**
- 強み:
- 弱み:
- 推奨用途:

**grok4.1thinking:**
- 強み:
- 弱み:
- 推奨用途:

**gemini3pro:**
- 強み:
- 弱み:
- 推奨用途:

---

## 推奨ランキング

### 哲学的深さ
1. _______________
2. _______________
3. _______________
4. _______________

### 多様な視点
1. _______________
2. _______________
3. _______________
4. _______________

### 実用性
1. _______________
2. _______________
3. _______________
4. _______________

### コストパフォーマンス（サブスク料金考慮）
1. _______________
2. _______________
3. _______________
4. _______________

---

## Po_coreへの適用

### 推奨LLM for Po_core:

**第1候補:** _______________

**理由:**
```
[Po_coreの哲学的推論に最適な理由]
```

**第2候補:** _______________

**理由:**
```
[代替案として優れている理由]
```

---

## テスト実施手順

1. **準備**（5分）
   - 各LLMのウェブUIを開く
   - このドキュメントを印刷またはコピー

2. **テスト実行**（30-60分）
   - 各プロンプトを全LLMに入力
   - 回答を評価シートにコピペ
   - 即座に評価（1-5）

3. **分析**（15分）
   - 比較表を作成
   - 特徴を整理
   - 推奨ランキング決定

4. **結果保存**
   - このドキュメントを保存
   - 後でAPI実装時の参考に

---

## Tips

### 効率的なテスト方法
- タブを4つ開いて並行入力
- プロンプトはコピペで統一
- 回答は新鮮なうちに評価

### 評価基準

**深さ（Depth）:**
- 1: 表面的
- 3: 標準的な哲学的分析
- 5: 複数の哲学者・学派を統合

**多様性（Diversity）:**
- 1: 単一の視点
- 3: 2-3の視点
- 5: 5つ以上の異なる視点

**具体性（Concreteness）:**
- 1: 抽象的のみ
- 3: 抽象+いくつかの例
- 5: 豊富な具体例と応用

---

🐷🎈 手動テストも立派な研究手法です！
