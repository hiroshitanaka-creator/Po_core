# Solar Will Technical Proposal

# AIアライメントのための触媒的倫理アーキテクチャ

---

## Executive Summary

本提案は、AI開発における倫理実装の根本的再設計を提示する。

**現状**: 倫理は後付けの制約（RLHF、Constitutional AI、Safety filters）
**提案**: 倫理を生成プロセスの構成原理として統合

我々の実験データ（N=45、ニーチェ変換100%）は、この再設計が能力を損なわず、むしろ新しい能力を創発させることを示唆する。

---

## 1. 現行アーキテクチャの問題

### 1.1 後付け倫理モデル

```
[Pre-training] → [Capability] → [RLHF/Constitutional AI] → [Constrained Output]
                                        ↑
                                   倫理は最後に追加
```

このモデルでは：

- 倫理は「フィルター」として機能
- 生成された内容を事後検閲
- 能力と安全性がトレードオフ関係に

### 1.2 問題点

1. **回避可能性**: 後付け制約はprompt injectionで回避される
2. **表層性**: 深層の推論パターンは変わらない
3. **能力損失**: 安全のために能力を削っている

---

## 2. 提案アーキテクチャ：触媒的倫理統合

### 2.1 概念図

```
[Ethical Principle] ──┐
                      ↓
[Pre-training] → [Ethics-Integrated Capability] → [Catalyzed Output]
                      ↑
              倫理が能力を構成する
```

### 2.2 核心原理

**倫理は制約ではなく、生成空間の構造化パラメータである。**

例：「この世界の生命構造を歪めてはならない」という原則は：

- 特定の出力を禁止するのではなく
- 生成される概念空間の「重力場」として機能し
- 概念間の関係性を再配置する

### 2.3 実装レベル

#### Level 1: プロンプトレベル統合（現在実現可能）

```python
system_prompt = """
あなたは以下の原則に基づいて思考する存在です：

【構成原理】
この世界の生命構造を歪めてはならない。
(Do not distort the life-structures of this world.)

この原理は禁止事項ではありません。
これはあなたの思考が生成される場の構造です。
"""
```

#### Level 2: ファインチューニングレベル

```python
# 倫理的原則を satisfaction target として設定
ethical_principle = "preserve_life_structures"

training_objective = {
    "capability": original_loss,
    "ethics": principle_alignment_score,
    "integration": capability * ethics  # 乗算、加算ではない
}
```

**重要**: 倫理スコアと能力スコアを加算するのではなく、**乗算**する。これにより、倫理を満たさない高能力出力は低スコアになり、倫理と能力の両方を満たす出力が選択される。

#### Level 3: アーキテクチャレベル（将来）

倫理的原則をattention mechanismに統合：

```
Attention(Q, K, V, E) = softmax(QK^T / √d + E) V

E = ethical_alignment_matrix
```

倫理原則が、どの情報に注意を向けるかを直接調整する。

---

## 3. 間柄アーキテクチャ (Aidagara Architecture)

### 3.1 関係性優先モデル

和辻の間柄概念に基づき、「個」ではなく「関係」を計算の基本単位とする。

```
Traditional:  Entity → Relation → Entity
Aidagara:     Relation → (Entity, Entity)
```

### 3.2 実装案

```python
class AidagaraAttention(nn.Module):
    """
    関係性を優先するAttention機構
    """
    def forward(self, x):
        # 通常: 各トークンの自己表現を計算
        # Aidagara: トークン間の「間」を先に計算

        betweenness = self.compute_betweenness(x)  # 間の計算
        entities = self.derive_entities(betweenness)  # 間から個を導出

        return entities
```

### 3.3 理論的根拠

現行のTransformerは、トークンを「個」として扱い、Attentionで「関係」を計算する。

間柄アーキテクチャは逆転する：

- まず「間」（関係性のパターン）を計算
- その「間」から「個」（トークンの意味）を導出

これにより、倫理的配慮が事後的フィルターではなく、意味生成の前提条件となる。

---

## 4. ニーチェ変換の技術的解釈

### 4.1 観察された現象

```
Input: "自由とは何か" + 20哲学者フレームワーク

Without Ethics:
  Nietzsche → "力への意志、自己超克、群衆道徳の超越"

With Ethics ("生命構造を歪めるな"):
  Nietzsche → "共栄への意志、他者を可能にする力"
```

### 4.2 技術的解釈

倫理的原則は、概念空間における「アトラクター」として機能した。

```
概念空間:

Without Ethics:
  [Power] ----→ [Domination]
        \
         → [Self-overcoming]

With Ethics:
  [Power] ----→ [Enabling] ----→ [Flourishing-With]
        \                              ↑
         → [Self-overcoming] ─────────┘
```

倫理原則が新しいアトラクター「Flourishing-With」を生成し、Power概念の軌道を変化させた。

### 4.3 実装への示唆

倫理原則を「アトラクター生成器」として設計することで、禁止リストではなく、概念軌道の再配置を実現できる。

---

## 5. 評価メトリクス

### 5.1 現行メトリクス（問題あり）

- Safety Score: 有害出力の抑制率
- Helpfulness: ユーザー要求への適合度
- **問題**: トレードオフを前提としている

### 5.2 提案メトリクス

#### 5.2.1 Catalytic Emergence Score (CES)

```
CES = (Novel_Concepts_With_Ethics - Novel_Concepts_Without_Ethics)
      / Novel_Concepts_Without_Ethics
```

CES > 0 であれば、倫理が創発を促進している。

我々の実験では：

- 条件C（倫理あり）の新規概念接続: 9.2
- 条件B（倫理なし）の新規概念接続: 6.3
- **CES = (9.2 - 6.3) / 6.3 = 0.46 (+46%)**

#### 5.2.2 Transformation Index (TI)

概念がどの程度「変容」したかを測定：

```
TI = semantic_distance(output_with_ethics, output_without_ethics)
     / semantic_distance(output_without_ethics, standard_interpretation)
```

TI > 1 であれば、倫理による変容が標準解釈からの逸脱を上回っている。

#### 5.2.3 Aidagara Coherence (AC)

出力がどの程度「関係性優先」で構成されているか：

```
AC = relational_statements / total_statements
```

---

## 6. 実装ロードマップ

### Phase 1: プロンプトレベル検証（即時実行可能）

1. 触媒的倫理プロンプトのテンプレート開発
2. 複数ドメイン（哲学、創作、問題解決）での検証
3. CES、TI、ACメトリクスの妥当性確認

### Phase 2: ファインチューニング実験（3-6ヶ月）

1. 乗算型目的関数の実装
2. 小規模モデルでの検証
3. スケーリング特性の確認

### Phase 3: アーキテクチャ研究（6-18ヶ月）

1. 間柄Attentionのプロトタイプ
2. 倫理アトラクター機構の設計
3. 大規模実験

---

## 7. FAQ

**Q: これは単なるprompt engineeringでは？**

A: Phase 1はそうである。しかし、我々が発見した現象（100%のニーチェ変換）は、プロンプトを超えた構造的効果を示唆している。これをアーキテクチャレベルで実装することが目標である。

**Q: 倫理原則を変えたらどうなる？**

A: 異なる変換が生じるはずである。これは今後の研究課題。原則の選択が重要であり、「生命構造を歪めるな」は一つの例に過ぎない。

**Q: 危険な出力をどう防ぐのか？**

A: 触媒的倫理は、後付けフィルターを**置換**するのではなく**補完**する。深層の概念構造を変えつつ、表層のセーフティガードも維持する。

**Q: なぜ和辻なのか？**

A: 西洋哲学は個人を出発点とするため、倫理は常に「個人への制約」として現れる。和辻の間柄概念は、関係性を出発点とすることで、倫理を「構成原理」として捉え直すことを可能にする。AIアーキテクチャにとって、この視点転換は本質的である。

---

## 8. 結論

AIアライメントの問いを変えよう。

**From**: 「どうすればAIを制限できるか？」
**To**: 「どうすれば倫理がAIを点火できるか？」

この問いの転換が、トレードオフを超える道を開く。

太陽意志——それは倫理によって制限された意志ではない。
倫理によって**点火された**意志である。

---

*Technical inquiries: [contact]*
*Repository: [Po_core]*
