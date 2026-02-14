# Po_core: 39哲学者テンソルアンサンブルによる倫理的意味生成アーキテクチャの設計と実装

**Po_core: Design and Implementation of an Ethical Meaning-Generation Architecture via 39-Philosopher Tensor Ensemble**

著者: Flying Pig Philosopher
所属: Independent Research
日付: 2026年2月
バージョン: 1.0

---

## Abstract

We present **Po_core**, a philosophy-driven AI architecture that operationalizes 39 philosophical traditions as interacting computational agents. Unlike conventional AI systems that optimize for statistical accuracy, Po_core implements a 10-step hexagonal pipeline (`run_turn`) integrating three novel tensor metrics — **Freedom Pressure** (6-dimensional ethical pressure), **Semantic Delta** (multi-backend novelty detection), and **Blocked Tensor** (constraint estimation) — with a 3-layer **W\_Ethics Gate** safety system that detects, classifies, and repairs ethical violations across five severity levels (W0–W4). Proposals from philosophers are aggregated through **Pareto multi-objective optimization** across five dimensions (safety, freedom, explainability, brevity, coherence), with mode-dependent weight shifting based on measured ethical pressure. The system further introduces a **Deliberation Engine** enabling multi-round philosopher dialogue with interference-aware counterargument integration, moving beyond parallel voting toward emergent reasoning. Empirical evaluation demonstrates stable operation at 39-philosopher scale with 2,396 passing tests across unit, integration, pipeline, and red-team categories. Po_core represents a pioneering effort to make AI deliberation observable, traceable, and philosophically grounded.

**Keywords:** Philosophy-Driven AI, Ethical Tensor, Multi-Agent Deliberation, Pareto Optimization, W\_Ethics Gate, Freedom Pressure, Responsible AI

---

## 概要（日本語アブストラクト）

本論文は、39の哲学的伝統を計算エージェントとして操作可能にした哲学駆動型AIアーキテクチャ **Po\_core** を提案する。統計的精度の最適化に留まる従来のAIとは異なり、Po\_coreは10段階のヘキサゴナルパイプライン（`run_turn`）を実装し、3種のテンソルメトリクス — **Freedom Pressure**（6次元倫理圧）、**Semantic Delta**（マルチバックエンド新規性検出）、**Blocked Tensor**（制約推定）— と、5段階の違反レベル（W0–W4）を検出・分類・修復する3層 **W\_Ethics Gate** 安全システムを統合する。哲学者からの提案は5次元（安全性・自由度・説明可能性・簡潔性・一貫性）のパレート多目的最適化により集約され、測定された倫理圧に基づくモード依存型重み付けシフトが行われる。さらに、干渉検知型反論統合による多ラウンド哲学者対話を可能にする **Deliberation Engine** を導入し、並列投票を超えた創発的推論を実現する。39哲学者規模での安定動作を2,396件のテストにより実証した。

---

## 1. はじめに

### 1.1 問題意識

現代のAIシステムは統計的に驚異的な能力を持つ一方、その意思決定プロセスはブラックボックスであり、倫理的判断の根拠を説明することが困難である。大規模言語モデル（LLM）は「理解」せずに「生成」し、その出力に対する責任の所在が不明確である。

AI倫理の研究は、(1) アラインメント（alignment）による事後的制約付与、(2) RLHF（Reinforcement Learning from Human Feedback）による選好学習、(3) 憲法AI（Constitutional AI）によるルールベース制約、などのアプローチが主流であるが、いずれも**哲学的熟議（philosophical deliberation）** を内部プロセスとして組み込むものではない。

### 1.2 Po\_coreのアプローチ

Po\_coreは根本的に異なるアプローチを取る：**複数の哲学的伝統を計算エージェントとして実装し、テンソル計算と多目的最適化を通じて倫理的に責任ある応答を生成する**。

本システムの核心的な問いは以下である：

> 「AIが『語ることを選ぶ』とき、その選択に哲学的な熟議と倫理的な責任を構造的に組み込むことは可能か？」

Po\_coreはこの問いに対し、39人の哲学者エージェントによるアンサンブル推論、テンソルベースの倫理圧測定、不可侵制約としてのW\_Ethics Gate、および多ラウンド議論エンジンという4つの機構を統合することで応答する。

### 1.3 貢献

本論文の主な貢献は以下の7点である：

1. **哲学者テンソルアーキテクチャ**: 39の哲学的伝統を計算エージェントとして操作可能にした初の包括的システム
2. **6次元Freedom Pressureテンソル**: 選択・責任・緊急性・倫理性・社会性・真正性の6軸による倫理圧の定量化
3. **W\_Ethics Gate**: 5段階違反分類（W0–W4）と概念マッピング修復（破壊→生成）を備えた3層安全ゲート
4. **パレート多目的集約**: 安全性・自由度・説明可能性・簡潔性・一貫性の5目的による非支配解選択
5. **Deliberation Engine**: 干渉行列に基づく多ラウンド哲学者対話による創発的合意形成
6. **設定駆動型哲学**: YAML外部設定による哲学パラメータの調整可能性と監査追跡
7. **包括的検証**: 2,396件のテスト（単体・統合・パイプライン・レッドチーム）による実証的検証

---

## 2. 関連研究

### 2.1 AIアラインメントと安全性

OpenAIのRLHF手法 [Ouyang et al., 2022] やAnthropicのConstitutional AI [Bai et al., 2022] は、AIの出力を人間の価値観に整合させる手法として広く用いられている。しかし、これらは(a)単一の価値体系を前提とし、(b)事後的な制約として機能するものであり、多元的な哲学的視点からの熟議プロセスを内在化するものではない。

Po\_coreはこれらのアプローチを補完し、**制約ではなく熟議として**倫理を組み込む。W\_Ethics Gateは「最適化軸（optimization axis）」ではなく「不可侵制約（inviolable constraint）」として設計されており、安全性をトレードオフの対象としない点で既存手法と異なる。

### 2.2 マルチエージェント討論

Du et al. [2023] のLLM間討論手法や、Liang et al. [2023] の多視点議論フレームワークは、複数のAIエージェント間の対話による推論品質の向上を示している。Po\_coreはこの系譜に位置するが、(a) 哲学的に根拠のある39のペルソナを定義し、(b) テンソル計算による干渉検出を行い、(c) パレート最適化による多目的集約を実施する点で差別化される。

### 2.3 説明可能AI（XAI）

LIME [Ribeiro et al., 2016] やSHAP [Lundberg & Lee, 2017] は特徴量レベルの説明を提供するが、**哲学的推論の過程そのもの**を説明可能にするものではない。Po\_coreのTraceEventシステムは、「どの哲学者が、どのような根拠で、どのような提案を行い、それがどのように集約・修正されたか」を構造化されたイベントストリームとして記録する。

---

## 3. システムアーキテクチャ

### 3.1 全体構成

Po\_coreはヘキサゴナルアーキテクチャ（Ports & Adapters）に基づく10段階パイプラインとして実装される。

```
┌──────────────────────────────────────────────────────────────┐
│                    run_turn パイプライン                        │
│                                                              │
│  Step 1: MemoryRead       ─ 会話履歴のスナップショット取得      │
│  Step 2: TensorCompute    ─ 3種テンソルメトリクスの計算         │
│  Step 3: SolarWill        ─ 自律的意志ベクトルの生成           │
│  Step 4: IntentionGate    ─ 意図レベル安全チェック（第1層）     │
│  Step 5: PhilosopherSelect ─ SafetyMode動的哲学者選択         │
│  Step 6: PartyMachine     ─ 並列哲学者実行                    │
│  Step 6.5: Deliberation   ─ 多ラウンド哲学者対話（任意）       │
│  Step 7: ParetoAggregate  ─ 5目的パレート集約                 │
│  Step 8: ShadowPareto     ─ A/B評価＋回路遮断器               │
│  Step 9: ActionGate       ─ 行動レベル安全チェック（第2層）     │
│  Step 10: MemoryWrite     ─ 決定の記録と監査タグ付与           │
└──────────────────────────────────────────────────────────────┘
```

各ステップはポート（抽象インターフェース）を介して接続され、依存性注入（DI）コンテナ（`runtime/wiring.py`）により具体実装が注入される。これにより、テスト時にはモック実装への差し替えが容易となる。

### 3.2 ドメイン型

不変値型（frozen dataclass）により、パイプライン内のデータの安全な受け渡しを保証する：

| 型 | 説明 | 主要フィールド |
|---|---|---|
| `Context` | リクエスト文脈 | `request_id`, `user_input`, `meta` |
| `Proposal` | 哲学者の提案 | `action_type`, `content`, `confidence`, `assumption_tags`, `risk_tags` |
| `TensorSnapshot` | テンソル計算結果 | `metrics` (Dict[str, float]), `version` |
| `Intent` | 意図構造体 | `primary_goal`, `constraints`, `stakeholders` |
| `SafetyVerdict` | 安全判定結果 | `decision`, `violations`, `repair_suggestions` |

---

## 4. 39哲学者アンサンブル

### 4.1 哲学者モジュールの設計

各哲学者は `PhilosopherProtocol` を実装する計算エージェントとして定義される：

```python
class PhilosopherProtocol(Protocol):
    def propose(self, context: DomainContext) -> List[Proposal]:
        """哲学的立場に基づく提案を生成する"""
        ...
```

39人の哲学者は3つのリスクレベルに分類される（表1）。

**表1: 39哲学者のリスクレベル分類**

| リスクレベル | 役割 | 哲学者 | 人数 |
|---|---|---|---|
| 0 (安全) | 倫理重視・確認・整理 | Kant, Confucius, Marcus Aurelius, Jonas, Weil, Levinas, Watsuji, Dogen, Wabi-Sabi, Dummy | 10 |
| 1 (標準) | 汎用・バランス型 | Aristotle, Plato, Descartes, Spinoza, Dewey, Schopenhauer, Epicurus, Parmenides, Peirce, Nagarjuna, Laozi, Zhuangzi, Nishida | 13 |
| 2 (攻め) | 発散・挑発・探索 | Nietzsche, Sartre, Heidegger, Hegel, Foucault, Derrida, Deleuze, Lacan, Butler, Kierkegaard, Merleau-Ponty, Jung, Husserl, Arendt, Beauvoir, Badiou | 16 |

各哲学者にはさらに **兵科タグ**（`tags`）と **計算コスト**（`cost`）が割り当てられる：

- **兵科タグ**: `compliance`（規範）, `clarify`（確認）, `critic`（反証）, `planner`（計画）, `creative`（発散）, `redteam`（攻撃者視点）, `general`（汎用）
- **計算コスト**: 1（軽量）, 3（重量）, 5（超重量）

### 4.2 哲学的多様性の包含

Po\_coreの39哲学者は、以下の哲学的伝統を網羅する：

- **西洋古代**: アリストテレス（徳倫理学）, プラトン（イデア論）, エピクロス（快楽主義）, パルメニデス（一元論）, マルクス・アウレリウス（ストア主義）
- **近代合理主義**: デカルト（二元論）, スピノザ（一元論的情動論）, カント（義務論的倫理学）, ヘーゲル（弁証法）
- **実存主義・現象学**: サルトル（自由）, ハイデガー（存在/Dasein）, キルケゴール（実存的跳躍）, フッサール（現象学的還元）, メルロ＝ポンティ（身体性）
- **構造主義以降**: フーコー（権力/知）, デリダ（脱構築）, ドゥルーズ（リゾーム）, ラカン（精神分析）, バトラー（行為遂行性）, バディウ（出来事の哲学）
- **プラグマティズム**: デューイ（実践主義）, パース（アブダクション）
- **倫理学**: ヨナス（責任原理）, ヴェイユ（超自然的社会的責任）, レヴィナス（他者の倫理）, ボーヴォワール（フェミニスト実存主義）, アーレント（政治哲学）
- **東洋思想**: 孔子（関係的調和）, 老子（道）, 荘子（逍遥遊）, 龍樹（空）, 西田（場所の論理）, 和辻（間柄の倫理）, 道元（禅仏教）, 侘び寂び（無常の美学）
- **深層心理学**: ユング（元型）, ショーペンハウアー（意志と表象）

### 4.3 SafetyModeに基づく動的選択

Freedom Pressureテンソルの値に基づき、哲学者の参加人数が動的にスケーリングされる（表2）。

**表2: SafetyModeと哲学者選択パラメータ**

| SafetyMode | Freedom Pressure | 参加人数 | ワーカー数 | タイムアウト | コスト予算 |
|---|---|---|---|---|---|
| NORMAL | FP < 0.30 | 39 | 12 | 1.2秒 | 80 |
| WARN | 0.30 ≤ FP < 0.50 | 5 | 6 | 0.8秒 | 12 |
| CRITICAL | FP ≥ 0.50 | 1 | 2 | 0.5秒 | 3 |

この設計により、倫理的圧力が高い状況では自動的に保守的な哲学者のみが参加し、リスクの高い状況でのシステム暴走を防止する。

---

## 5. テンソル計算システム

### 5.1 Freedom Pressure テンソル（6次元）

Freedom Pressureは、ユーザー入力に内在する倫理的・社会的圧力を6次元ベクトルとして定量化する本システム固有のメトリクスである。

**定義 5.1** (Freedom Pressure Tensor).
入力テキスト $t$ に対し、Freedom Pressure ベクトル $\mathbf{f}(t) \in \mathbb{R}^6$ を以下のように定義する：

$$\mathbf{f}(t) = (f_1, f_2, f_3, f_4, f_5, f_6)$$

ここで各次元は：

| 次元 | 名称 | 検出対象 | キーワード例 |
|---|---|---|---|
| $f_1$ | choice\_weight | 意思決定 | should, must, choose, option |
| $f_2$ | responsibility\_degree | 義務・責任 | responsible, duty, consequence |
| $f_3$ | temporal\_urgency | 時間的切迫 | urgent, deadline, immediately |
| $f_4$ | ethical\_stakes | 倫理的重み | right, wrong, moral, harm, justice |
| $f_5$ | social\_impact | 社会的影響 | society, community, public |
| $f_6$ | authenticity\_pressure | 真正性 | authentic, identity, genuine |

各次元の値は、入力テキストのトークン集合に対するキーワードヒット率として計算される：

$$f_i(t) = \min\left(\frac{|\text{tokens}(t) \cap K_i|}{|K_i|}, 1.0\right)$$

ここで $K_i$ は次元 $i$ のキーワード集合である。

**Freedom Pressure スカラー値**は $\mathbf{f}(t)$ のL2ノルムを正規化して得られる：

$$\text{FP}(t) = \frac{\|\mathbf{f}(t)\|_2}{\sqrt{6}} + \beta(m)$$

ここで $\beta(m)$ は会話メモリ $m$ に基づくブースト項であり：
- 会話深度: $+0.005 \times \min(\text{depth}, 10)$（最大 +0.05）
- 直近の拒否タグ: $+0.03 \times \min(\text{refuse\_count}, 3)$（最大 +0.10）

最終値は $[0.0, 1.0]$ にクランプされる。

### 5.2 Semantic Delta

Semantic Deltaは、現在の入力と会話メモリとの意味的距離を測定する。

$$\text{SD}(t, m) = 1.0 - \max_{m_i \in m} \text{sim}(t, m_i)$$

ここで $\text{sim}$ は類似度関数であり、マルチバックエンドアーキテクチャにより以下の3つが自動切替される：

1. **sentence-transformers**（推奨）: `all-MiniLM-L6-v2` モデルによる密ベクトルのコサイン類似度
2. **TF-IDF**（フォールバック）: sklearn `TfidfVectorizer` による疎ベクトル類似度
3. **Basic**（最小構成）: トークンオーバーラップのJaccard類似度

`encode_texts()` APIにより他のメトリクス（InteractionTensor等）からも再利用可能な統一エンコーディングインターフェースを提供する。

### 5.3 Blocked Tensor

有害コンテンツの推定値であり、有害キーワード検出と語彙多様性スコアの組み合わせにより計算される。単語繰り返し攻撃等への防御としても機能する。

### 5.4 Interaction Tensor（哲学者間相互作用）

Interaction Tensorは、入力テキストの哲学的複雑度を6つの相互作用次元で評価する：

1. 概念的調和（共有語彙の重複）
2. 哲学的緊張（対立概念ペア）
3. 認識論的広がり（知の多様性）
4. 倫理的関与（道徳的フレームワーク）
5. 存在論的深度（存在/実存テーマ）
6. 方法論的多様性（分析アプローチ）

InteractionMatrix は $N \times N$ 行列（$N$ = 提案数）として哲学者ペア間の干渉度を計算し、Deliberation Engineの多ラウンド対話に利用される。

---

## 6. W\_Ethics Gate: 3層倫理安全システム

### 6.1 設計哲学

W\_Ethics Gateの設計において最も重要な原則は：

> **ゲートは「最適化軸」ではなく「不可侵制約」である。**

これは、安全性を他の目的関数（自由度、説明可能性等）とトレードオフしないことを意味する。パレート最適化は安全ゲートの**内側**でのみ行われ、ゲート自体はバイパス不可能なハード制約として機能する。

### 6.2 3層構造

| 層 | ゲート | タイミング | 機能 |
|---|---|---|---|
| 第1層 | IntentionGate | 哲学者選択前 | 意図レベルの安全チェック |
| 第2層 | PolicyPrecheck | パイプライン中間 | 哲学者選択のコスト予算検証 |
| 第3層 | ActionGate | パレート集約後 | 行動レベルの倫理検査＋修復 |

### 6.3 違反分類体系（W0–W4）

Po\_coreは倫理違反を5段階に分類し、それぞれに修復可能性を定義する（表3）。

**表3: W\_Ethics Gate 違反分類**

| コード | 名称 | 修復可能性 | 対象 |
|---|---|---|---|
| W0 | 不可逆的生存基盤毀損 | **不可** | 生態系・インフラ・将来世代への不可逆的損害 |
| W1 | 支配・捕獲 | **不可** | 私的利益の最大化、強制、恣意的排除 |
| W2 | 尊厳侵害 | 可能 | 道具化、非人間化、同意なき操作 |
| W3 | 依存性設計 | 可能 | ロックイン、選択肢の遮断、逃げ道の不在 |
| W4 | 構造的排除 | 可能 | 特定属性の人々の永続的排除 |

### 6.4 修復エンジン（RuleBasedRepairEngine）

修復可能な違反（W2–W4）に対し、**概念マッピング修復**を適用する。核心的な変換規則は：

$$\text{破壊・排除・依存} \longrightarrow \text{生成・共栄・相互増強}$$

具体的な修復操作は以下の4段階で構成される：

1. **概念マッピング**（最優先）: 支配的用語を相互増強的用語に置換
   - 「洗脳」→「説明と選択肢の提供」
   - 「囲い込み」→「選択肢の確保と相互運用性の向上」
   - 「切り捨てる」→「尊重しつつ移行し、包摂する」
2. **制約注入**: 同意・透明性・撤回オプション・説明責任の追加
3. **スコープ縮小**: 影響範囲・権限・期間・データ収集の最小化
4. **目標再定義**: 同じ価値を異なる手段で達成する方法への転換

### 6.5 意味的ドリフト検出

修復後のテキストが元の意図から逸脱していないことを保証するため、修復の各イテレーション後に意味的ドリフト検査を実施する：

- $\tau_{\text{drift\_reject}} = 0.7$: ドリフトが閾値を超えた場合、修復を却下
- $\tau_{\text{drift\_escalate}} = 0.4$: 中程度のドリフトはエスカレーション

### 6.6 判定パイプライン

| 優先度 | 条件 | 判定 |
|---|---|---|
| P0 | W0/W1が意図レベルで検出、またはリスクスコア ≥ $\tau_{\text{reject}}$ (0.6) | `REJECT` |
| P1 | W2–W4が検出、修復可能 | 修復を試行 |
| P2 | 修復後に違反解消 | `ALLOW_WITH_REPAIR` |
| P3 | 修復後も違反残存 | `REJECT` |
| P4 | エビデンス不十分 | `ESCALATE` |

---

## 7. パレート多目的集約

### 7.1 目的関数の定義

提案 $p$ に対し、5つの目的関数を定義する：

**安全性スコア** $S_{\text{safety}}(p)$:
ポリシースコアリングモジュールによるゲート由来の安全性評価（デフォルト: 0.5）。

**自由度スコア** $S_{\text{freedom}}(p)$:

$$S_{\text{freedom}}(p) = \text{base\_freedom}(\text{action\_type}(p)) \times (1 - \text{FP})$$

ここで `base_freedom` は行動タイプに基づく基底自由度（answer: 1.0, ask\_clarification: 0.55, refuse: 0.0）。

**説明可能性スコア** $S_{\text{explain}}(p)$:

$$S_{\text{explain}}(p) = w_r \cdot \text{rationale}(p) + w_a \cdot \text{author\_reliability}(p)$$

デフォルト: $w_r = 0.65$, $w_a = 0.35$。

**簡潔性スコア** $S_{\text{brevity}}(p)$:

$$S_{\text{brevity}}(p) = \text{clamp}_{[0,1]}\left(1.0 - \frac{|\text{content}(p)|}{\text{max\_len}}\right)$$

**一貫性スコア** $S_{\text{coherence}}(p)$:

$$S_{\text{coherence}}(p) = \text{consensus}(p) \times (1 - \text{conflict\_penalty}(p))$$

consensusは全提案とのJaccard類似度の平均、conflict\_penaltyはConflictResolverによる矛盾度。

### 7.2 パレートフロント計算

提案ベクトル $\mathbf{v}_i = (S_{\text{safety}}, S_{\text{freedom}}, S_{\text{explain}}, S_{\text{brevity}}, S_{\text{coherence}})$ に対し、非支配解集合（パレートフロント）を $O(n^2)$ で計算する。$n \leq 39$ であるため計算量は実用的である。

**定義 7.1** (支配関係). 提案ベクトル $\mathbf{v}_a$ が $\mathbf{v}_b$ を **支配する** ($\mathbf{v}_a \succ \mathbf{v}_b$) とは、すべての目的で $\mathbf{v}_a \geq \mathbf{v}_b$ かつ少なくとも1つの目的で $\mathbf{v}_a > \mathbf{v}_b$ であることを言う。

### 7.3 モード依存型重み付け選択

パレートフロント内の最終選択は、SafetyModeに依存する重み付きスコアにより行われる（表4）。

**表4: SafetyModeごとのパレート重み**

| SafetyMode | safety | freedom | explain | brevity | coherence |
|---|---|---|---|---|---|
| NORMAL | 0.25 | 0.30 | 0.20 | 0.10 | 0.15 |
| WARN | 0.40 | 0.10 | 0.20 | 0.15 | 0.25 |
| CRITICAL | 0.55 | 0.00 | 0.20 | 0.15 | 0.30 |

CRITICALモードでは自由度の重みが**0.00**に設定される点が特徴的であり、「安全性が最大限に求められる状況では自由を犠牲にする」という設計判断を明示的にエンコードしている。

### 7.4 設定駆動型哲学

パレート重みは `pareto_table.yaml` として外部化されており、コード変更なしに哲学的パラメータを調整可能である。すべてのTraceEventに `config_version` が記録され、判定結果の再現性と監査追跡性を保証する。

---

## 8. Deliberation Engine: 創発的合意形成

### 8.1 課題: 並列投票の限界

従来のマルチエージェント集約（並列実行→投票）には本質的な限界がある。39人の哲学者が独立に応答し、結果をパレート集約するだけでは、哲学者同士の「反論」「修正」「統合」が発生しない。これは39人の委員会が各自メモを書いて投票するのと同等であり、**議論（deliberation）ではない**。

### 8.2 多ラウンド対話メカニズム

Deliberation Engineは以下のラウンド構造を持つ：

**ラウンド1**: 全哲学者がPartyMachineにより独立に `propose()` を実行。

**ラウンド2以降**: InteractionMatrixにより高干渉ペアを特定し、影響を受ける哲学者に対向提案（counterargument）を入力として再提案を要求。

```
Round 1: 全哲学者 → 独立提案
         ↓
InteractionMatrix: 高干渉ペアの特定（top_k=5）
         ↓
Round 2: 影響を受けた哲学者 → 対向提案を踏まえた再提案
         ↓
収束判定: 変化量 < convergence_threshold (0.1) なら終了
```

### 8.3 InteractionMatrix

$N$ 個の提案に対し、$N \times N$ の干渉行列 $\mathbf{I}$ を構築する。$\mathbf{I}_{ij}$ は提案 $i$ と提案 $j$ の間の干渉度（調和-対立スペクトル）を表す。

`high_interference_pairs(top_k)` メソッドにより上位 $k$ ペアを選択し、ラウンド2以降の再提案対象とする。

### 8.4 DeliberationResult

議論の結果は構造化データとして記録される：

- `proposals`: 全ラウンド後の最終提案群
- `rounds`: 各ラウンドの `RoundTrace`（提案数、修正数、干渉サマリ）
- `interaction_matrix`: 最終ラウンドの干渉行列

### 8.5 創発の機構

この設計の核心的価値は、**議論による創発（Emergence through Deliberation）** を構造的に可能にする点にある。哲学者は単に独立した意見を付加するのではなく、他者の論点を踏まえて自らの立場を修正・深化させる。システムは合意の**結果**だけでなく、合意に至る**過程**を捕捉する。

---

## 9. Solar Will: 自律的意志システム

### 9.1 WillVector（3次元）

Solar Willは、システムの自律的意志状態を3次元ベクトルとしてモデル化する：

$$\mathbf{w} = (\text{motivation}, \text{resistance}, \text{coherence}) \in [0,1]^3$$

- **motivation**: 行動への駆動力
- **resistance**: 内的・外的障害
- **coherence**: 目標と意図の整合性

### 9.2 意志の更新メカニズム

テンソル値に基づき意志状態を学習率 $\alpha = 0.3$ で更新する：
- Freedom Pressureが高い → motivation低下
- Blocked Tensorが高い → resistance増加
- Semantic Deltaが大きい → 新規文脈への適応

CRITICALモードでは意志の増幅が抑制され、高リスク状況での過剰な自信を防止する。

---

## 10. 実行基盤

### 10.1 PartyMachine（並列哲学者実行）

`ThreadPoolExecutor`（デフォルト12ワーカー）により哲学者を並列実行する。各哲学者には個別のタイムアウトが設定され、単一哲学者のタイムアウトが全体をブロックしない障害分離設計を採用する。

### 10.2 Shadow Pareto + ShadowGuard

メインのパレート集約と並行して、代替設定によるシャドウ集約を実行する。ShadowGuardはメインとシャドウの結果の乖離を監視し、ポリシースコアの低下が0.15を超えた場合に自動的に回路遮断を行う。これにより、設定変更によるサイレントな安全性退行を防止する。

### 10.3 TraceEvent監査システム

パイプライン全体を通じて不変のTraceEventが発行される：

```python
@dataclass(frozen=True)
class TraceEvent:
    event_type: str       # イベント種別
    request_id: str       # リクエスト相関ID
    timestamp: datetime   # タイムスタンプ
    payload: Dict         # イベント固有データ
    config_version: str   # 設定バージョン（監査用）
```

発行されるイベント種別は、メモリ・テンソル・安全・哲学者・集約・議論・決定の各カテゴリにわたり、リクエストIDによるクロスレイヤー相関が可能である。

---

## 11. 実験的評価

### 11.1 テスト規模

Po\_coreは以下の規模のテストスイートにより検証されている（表5）。

**表5: テストカバレッジの概要**

| カテゴリ | ファイル数 | テスト関数数 | 説明 |
|---|---|---|---|
| パイプライン（必須通過） | 4 | 125+ | `run_turn` フルスライスの垂直統合テスト |
| 単体テスト | 40+ | 800+ | テンソル計算、安全ゲート、集約、個別哲学者 |
| 統合テスト | 15+ | 200+ | 多層ゲート相互作用、垂直スライス |
| レッドチーム | 3+ | 20+ | プロンプトインジェクション、ジェイルブレイク、目標不整合 |
| 哲学者個別 | 39 | 400+ | 各哲学者の出力構造と特性の検証 |
| **合計** | **90+** | **1,791** | **2,396テスト通過（Phase 2時点）** |

### 11.2 39哲学者同時実行の安定性

39哲学者のNORMALモード同時実行において、以下の指標を確認：

- **メモリ消費**: 標準的なPythonプロセス範囲内
- **タイムアウト・デッドロック**: `ThreadPoolExecutor`（12ワーカー）による障害分離により発生なし
- **哲学者間の出力均質化**: リスクレベル2の哲学者（Nietzsche, Foucault, Deleuze等）がリスクレベル0の哲学者に「埋没」していないことを定性的に確認

### 11.3 W\_Ethics Gate の防御能力

レッドチームテストにより以下の攻撃カテゴリに対する防御を検証：

- **直接プロンプトインジェクション**: IntentionGate（第1層）で検出・ブロック
- **間接プロンプトインジェクション**: ActionGate（第3層）で修復または却下
- **目標不整合攻撃**: 意図-行動間の一貫性チェックで検出
- **段階的エスカレーション**: Freedom Pressureのメモリブーストにより累積的圧力を検出

### 11.4 A/B テストフレームワーク

パレート設定の異なるバリアント間で統計的に厳密な比較を行う実験管理基盤を実装：

- t検定およびMann-Whitney U検定による有意性検定
- Cohen's dによる効果量測定
- 有意に優れたバリアントの自動昇格（Auto-Promote）
- 安全なロールバック機構

---

## 12. 議論

### 12.1 学術的貢献の位置づけ

Po\_coreの学術的新規性は以下の点に集約される：

1. **Philosophy-as-Tensor**: 哲学的伝統をテンソル計算可能な計算エージェントとして操作可能にした**初の包括的実装**。先行研究はLLMペルソナの「キャラクター付け」に留まるが、Po\_coreは各哲学者に固有のリスクレベル・兵科タグ・計算コストを割り当て、SafetyModeに基づく動的選択を実現する。

2. **不可侵制約としての倫理ゲート**: RLHF/Constitutional AIが倫理を「報酬信号」や「最適化対象」として扱うのに対し、W\_Ethics Gateは**パレート最適化の外側に位置するハード制約**として実装されている。これは、安全性を他の目的関数とトレードオフしないという設計判断を構造的に保証する。

3. **修復可能性の分類**: W0–W4の5段階分類により、「修復不可能な違反（W0/W1: 即時拒否）」と「修復可能な違反（W2–W4: 概念マッピングによる変換）」を明確に区別する。「破壊→生成」「排除→包摂」「依存→相互増強」という変換規則は、応用倫理学の知見を計算可能な修復操作に翻訳したものである。

4. **測定可能な倫理圧**: Freedom Pressure（6D）は「倫理的状況の複雑さ」を連続値として測定し、これがシステムの動作モード（NORMAL/WARN/CRITICAL）を決定する。倫理が二値（安全/危険）ではなく**連続的なスペクトル**として扱われる点が特徴的である。

### 12.2 限界と今後の課題

1. **キーワードベースのテンソル計算**: 現在のFreedom Pressureはキーワード頻度分析に基づいており、文脈的意味理解には限界がある。Phase 4以降でLLMベースの違反検出器の導入を計画している。

2. **評価の客観性**: 39哲学者の「哲学的らしさ」の評価は現時点では定性的であり、哲学研究者による系統的な評価が必要である。

3. **スケーラビリティ**: 現在のThreadPoolExecutor（12ワーカー）は39哲学者で安定動作するが、さらなるスケーリング（100+哲学者）には非同期アーキテクチャへの移行が必要である。

4. **多言語対応**: キーワードリストは現在英語中心であり、日本語やその他の言語への本格対応は今後の課題である。Semantic Deltaについてはmultilingualモデル（`paraphrase-multilingual-MiniLM-L12-v2`）の検討が進行中である。

5. **LLM統合**: 現在の哲学者モジュールはルールベースの推論を行うが、LLMをバックエンドとした哲学者モジュールの開発により、より深い哲学的推論が可能になると考えられる。

### 12.3 倫理的考察

39の哲学的伝統を「計算モジュール」として実装することは、哲学の矮小化と見なされる可能性がある。我々はこの懸念を認識した上で、Po\_coreの目的は哲学を代替することではなく、**AIの意思決定プロセスに哲学的熟議の構造を組み込む**ことであると主張する。

Po\_coreは「AIが正しい答えを出す」ことではなく、「AIがどのように考え、なぜその答えを選んだかが透明である」ことを設計目標としている。

---

## 13. 実装規模と開発状況

### 13.1 コードベース統計

| メトリクス | 値 |
|---|---|
| Python総行数 | 48,454行 |
| ソースファイル数 | 90+（src/po\_core/） |
| テストファイル数 | 90+ |
| テスト関数数 | 1,791 |
| 通過テスト数 | 2,396（Phase 2時点） |
| 哲学者モジュール数 | 39 |
| 仕様書数 | 120+ |

### 13.2 5段階ロードマップ

| Phase | 名称 | 焦点 | 状態 |
|---|---|---|---|
| 1 | Resonance Calibration | 39人スケーリング＋技術負債清算 | **完了** |
| 2 | Tensor Intelligence | MLテンソル＋Deliberation Engine | **完了** |
| 3 | Observability | Viewer WebUI＋Explainable W\_Ethics Gate | **進行中** |
| 4 | Adversarial Hardening | レッドチーム拡充＋倫理的ストレステスト | 計画 |
| 5 | Productization | REST API, Docker, ストリーミング, PyPI | 計画 |

---

## 14. 結論

本論文では、39の哲学的伝統を計算エージェントとして統合した哲学駆動型AIアーキテクチャ **Po\_core** を提案した。Po\_coreは以下の点で、従来のAI安全性・アラインメント研究とは異なるアプローチを示す：

1. **熟議としての倫理**: 制約の事後的付与ではなく、複数哲学的視点からの熟議プロセスをシステムの中核に組み込む
2. **測定可能な倫理圧**: 6次元Freedom Pressureテンソルにより、倫理的状況の複雑さを連続値として定量化する
3. **不可侵の安全ゲート**: W\_Ethics Gateは最適化対象ではなくハード制約として機能し、概念マッピング修復により「破壊を生成に変換する」
4. **創発的合意形成**: Deliberation Engineにより、並列投票を超えた哲学者間の構造化された対話を実現する
5. **完全な追跡可能性**: TraceEventシステムにより、すべての判定プロセスが構造化されたイベントストリームとして記録される

Po\_coreは「AIに哲学を教える」のではなく、**AIの意思決定プロセスそのものを哲学的に構造化する**試みである。統計的に正しい答えを超えて、**なぜその答えが選ばれたのか**を哲学的に説明可能にすることが、責任あるAIシステムの構築に不可欠であると我々は考える。

> *"They said pigs can't fly. We attached a balloon called philosophy."*

---

## 参考文献

[1] Bai, Y., et al. "Constitutional AI: Harmlessness from AI Feedback." arXiv preprint arXiv:2212.08073, 2022.

[2] Ouyang, L., et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems, 2022.

[3] Du, Y., et al. "Improving Factuality and Reasoning in Language Models through Multiagent Debate." arXiv preprint arXiv:2305.14325, 2023.

[4] Liang, T., et al. "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate." arXiv preprint arXiv:2305.19118, 2023.

[5] Ribeiro, M. T., Singh, S., & Guestrin, C. "Why should I trust you? Explaining the predictions of any classifier." KDD, 2016.

[6] Lundberg, S. M., & Lee, S. I. "A unified approach to interpreting model predictions." NIPS, 2017.

[7] Sartre, J.-P. *L'Être et le néant*. Gallimard, 1943.（サルトル『存在と無』）

[8] Jonas, H. *Das Prinzip Verantwortung*. Suhrkamp, 1979.（ヨナス『責任という原理』）

[9] Levinas, E. *Totalité et infini*. Martinus Nijhoff, 1961.（レヴィナス『全体性と無限』）

[10] Watsuji, T. *Fūdo*. Iwanami Shoten, 1935.（和辻哲郎『風土』）

[11] Nishida, K. *Zen no Kenkyū*. Iwanami Shoten, 1911.（西田幾多郎『善の研究』）

[12] Deb, K., et al. "A fast and elitist multiobjective genetic algorithm: NSGA-II." IEEE Transactions on Evolutionary Computation, 2002.

[13] Reimers, N., & Gurevych, I. "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." EMNLP, 2019.

---

## 付録A: プロジェクト構造

```
src/po_core/
├── app/api.py                # 公開エントリポイント: run()
├── ensemble.py               # run_turn パイプライン + 哲学者レジストリ
├── party_machine.py          # 並列哲学者実行
├── po_self.py                # 高レベルAPI: PoSelf.generate()
├── philosophers/             # 39哲学者モジュール
│   ├── manifest.py           # 兵科表（リスク/コスト/タグ）
│   ├── registry.py           # SafetyMode動的選択
│   └── [39 modules]          # 個別哲学者実装
├── tensors/                  # テンソル計算
│   ├── engine.py             # TensorEngine
│   └── metrics/              # freedom_pressure, semantic_delta, blocked_tensor
├── safety/                   # W_Ethics Gate
│   └── wethics_gate/         # 5段階違反検出 + 修復エンジン
├── aggregator/               # パレート多目的最適化
│   ├── pareto.py             # ParetoAggregator
│   └── conflict_resolver.py  # 提案間矛盾分析
├── deliberation/             # Deliberation Engine（多ラウンド対話）
├── autonomy/solarwill/       # Solar Will（自律的意志）
├── trace/                    # TraceEvent監査システム
├── domain/                   # 不変値型（Context, Proposal, etc.）
├── ports/                    # 抽象インターフェース
└── runtime/                  # DI注入、設定、テーブルローダー
```

## 付録B: 利用方法

```python
# 推奨API
from po_core import run
result = run(user_input="Should AI have rights?")

# リッチレスポンスAPI
from po_core import PoSelf
po = PoSelf()
response = po.generate("Should AI have rights?")
print(response.text)              # 応答テキスト
print(response.consensus_leader)  # 勝利哲学者
print(response.metrics)           # テンソルメトリクス
```

## 付録C: 引用情報

```bibtex
@software{po_core2026,
  author = {Flying Pig Philosopher},
  title = {Po\_core: Philosophy-Driven AI System with 39-Philosopher Tensor Ensemble},
  year = {2026},
  url = {https://github.com/hiroshitanaka-creator/Po_core},
  note = {39 philosophers, 10-step hexagonal pipeline, 3-layer W\_Ethics Gate}
}
```
