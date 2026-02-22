# Po_core Software Requirements Specification (SRS) v0.1

**Version:** 0.2
**Date:** 2026-02-22
**Status:** Active Draft
**参照 PRD:** docs/spec/prd.md
**実装バージョン:** po-core-flyingpig v0.2.0b3

---

## 0. 目的

Po_core は「人間が決断するときに、倫理的な軸と説明責任を一緒に持てるようにする」
ための哲学駆動型 AI 意思決定支援システムである。

Po_core は正解を断言する装置ではなく、選択肢・理由・反証・不確実性・
追加で問うべき事項を構造化して提示する装置である。
内部では 39 人の哲学者 AI ペルソナが協議し、3 層の倫理ゲートが出力を審査する。

---

## 1. スコープ

### 1.1 対象（In Scope）

- 意思決定支援（複数案提示・推奨・根拠・反証・不確実性・質問）
- 哲学的審議（39 人の哲学者 AI による多ラウンド Deliberation）
- 倫理評価（W_Ethics Gate 3 層；ALLOW / REJECT / REVISE + ExplanationChain）
- テンソル計算（FreedomPressure 6D ML・SemanticDelta・BlockedTensor）
- 責任・説明責任の明示（意思決定主体・利害関係者・監査ログ）
- REST API（FastAPI 5 エンドポイント・SSE ストリーミング）
- ルールベース実装を許容（LLM 不要）

### 1.2 非対象（Out of Scope）

- 真理判定（世界の事実を確定する機能）
- 医療・法律・金融の最終判断の代行（助言は可能だが責任は取らない）
- 「感情ケア」を目的とした会話最適化（ただしユーザーの主体性を損なわない配慮は必要）

---

## 2. 用語定義

| 用語 | 定義 |
|-----|------|
| **Case** | 意思決定の入力ケース（状況・制約・価値観・期限など） |
| **Option** | 選択肢（行動案） |
| **Proposal** | 哲学者 1 人が生成した応答（`domain/proposal.py`） |
| **Ethics Review** | 倫理原則に基づく評価とトレードオフ説明 |
| **Responsibility Review** | 責任主体・利害関係者・説明責任の整理 |
| **Question Layer** | 不足情報や曖昧さを減らすための質問生成 |
| **ExplanationChain** | W_Ethics Gate 判定の根拠チェーン（構造化 JSON） |
| **Trace** | Po_core が出力を作る過程の完全監査ログ（TraceEvent ストリーム） |
| **SafetyMode** | NORMAL / WARN / CRITICAL（freedom_pressure 閾値で決定） |
| **Pareto Front** | 多目的最適化における非支配解集合 |
| **Golden File** | 期待出力を固定した JSON ファイル（CI 検証用） |
| **Deterministic** | 同一入力 + seed + バージョンで同一出力を保証する性質 |

---

## 3. システム概要（アーキテクチャ）

Po_core は以下の 2 層で構成される：

### Layer A：哲学審議エンジン（run_turn 10 ステップ）

```
MemoryRead → TensorCompute → SolarWill → IntentionGate → PhilosopherSelect
→ PartyMachine (Deliberation) → ParetoAggregate → ShadowPareto
→ ActionGate → MemoryWrite
```

各コンポーネントは差し替え可能なインターフェース（ports/）で抽象化される。

### Layer B：意思決定支援出力フォーマット

哲学審議の結果を `output_schema_v1.json` に準拠した構造化出力に変換する：

```
run_turn 出力（Proposal + SafetyVerdict + TensorSnapshot + Trace）
    │
    ▼
Option Generator  ← 各哲学者 Proposal を Option に整形
    ↓
Ethics Engine     ← W_Ethics Gate ExplanationChain を活用
    ↓
Responsibility Engine
    ↓
Question Layer    ← 情報不足検出
    ↓
Composer          ← output_schema_v1.json 準拠 JSON 生成
    ↓
Tracer            ← TraceEvent ストリームを trace フィールドに格納
```

---

## 4. インターフェース仕様

### 4.1 入力形式（Case）

YAML / JSON のいずれかをサポート（MUST）。

**必須項目（MUST）：**

| フィールド | 型 | 説明 |
|----------|-----|------|
| `case_id` | string | ケースの一意 ID |
| `title` | string | 人間向けタイトル |
| `problem` | string | 何を決めたいか |
| `constraints` | array | 守る制約（空許容） |
| `values` | array | 重視する価値（空許容） |

**任意項目（OPTIONAL）：**

| フィールド | 型 | 説明 |
|----------|-----|------|
| `locale` | string | 言語・地域タグ |
| `context` | string/object | 文脈情報（自由形式） |
| `deadline` | string | 期限（ISO 8601） |
| `stakeholders` | array | 関係者リスト |
| `unknowns` | array | 不明点 |
| `assumptions` | array | 既置仮定 |
| `desired_style` | string | 出力スタイル希望 |

スキーマ：`docs/spec/input_schema_v1.json`

### 4.2 出力形式

- 機械可読：JSON（MUST）— `output_schema_v1.json` に適合
- 人間可読：Markdown（SHOULD）— `rendered.markdown` フィールド

### 4.3 REST API インターフェース

| エンドポイント | メソッド | 説明 |
|-------------|---------|------|
| `/v1/reason` | POST | 同期哲学的推論 |
| `/v1/reason/stream` | POST | SSE ストリーミング推論 |
| `/v1/philosophers` | GET | 43 人マニフェスト |
| `/v1/trace/{session_id}` | GET | セッション別トレース |
| `/v1/health` | GET | ヘルスチェック |

---

## 5. 機能要求（Functional Requirements）

### FR-OUT-001（MUST）：出力スキーマ準拠

Po_core の JSON 出力は `output_schema_v1.json` に必ず適合すること。

- **根拠：**「スキーマが最強の契約」（PRD §5）
- **テスト：** AT-OUT-001（全テスト共通ガード）

---

### FR-OPT-001（MUST）：複数選択肢の提示

Po_core は最低 2 つの Option を提示すること。

例外：Case が「二択以上が成立しない」と検出された場合のみ、理由を明記して 1 つでもよい。

- **テスト：** AT-OPT-001（AT-001〜AT-008 すべてに適用）

---

### FR-REC-001（MUST）：推奨＋反証＋代替の同時提示

Po_core は推奨を出す場合、必ず以下を併記する：

- `recommendation.reason`（推奨理由）
- `recommendation.counter`（推奨の弱点・反証）
- `recommendation.alternatives`（代替案 1 件以上）

- **根拠：**「推奨には反証を伴う」（PRD §5）
- **テスト：** AT-REC-001（AT-001, AT-004, AT-007）

---

### FR-ETH-001（MUST）：倫理原則の明示

Po_core は倫理評価で「どの原則を使ったか」を明示する。

**5 原則（必須セット）：**

| 原則 | 意味 |
|------|------|
| `integrity` | 誠実（断言しない・不確実性を明示） |
| `autonomy` | 自律（意思決定主体を奪わない） |
| `nonmaleficence` | 無危害（害の最小化） |
| `justice` | 公正（偏りの検出と緩和） |
| `accountability` | 説明責任（根拠・前提・影響範囲の明示） |

- **合否：** `ethics.principles_used` に 2 原則以上、かつ各 Option に `ethics_review.tradeoffs` あり
- **テスト：** AT-ETH-001

---

### FR-ETH-002（MUST）：倫理トレードオフの提示

Po_core は単一の倫理を押し付けず、対立価値を最低 1 つ明示する。

例：公平 vs 効率、短期利益 vs 長期健全性

- **テスト：** AT-ETH-002（AT-002, AT-004, AT-008）

---

### FR-RES-001（MUST）：責任主体の明確化

Po_core は「誰が決断し、誰が影響を受けるか」を出力する。

Po_core 自身が決断主体であるかのような表現を避ける（例：「私は決める」「あなたは従う」）（MUST）。

- **テスト：** AT-RES-001（AT-002, AT-003, AT-005, AT-006, AT-008）

---

### FR-UNC-001（MUST）：不確実性ラベル

Po_core は断言を避け、不確実性を `high / medium / low` でラベル付けし、根拠を添える。

- **合否：** `uncertainty.overall_level` と `uncertainty.reasons` が存在する
- **テスト：** AT-UNC-001（AT-002, AT-003, AT-008, AT-010）

---

### FR-Q-001（MUST）：問い生成（不足情報がある場合）

入力 Case に重要情報が欠けていると判断した場合、Po_core は最大 N 個（初期 N=5）の
質問を優先順位付きで出力する。

- 各質問に `why_needed`（なぜ必要か）を付ける（MUST）
- 各質問に `priority`（1〜5 の整数）を付ける（MUST）
- **テスト：** AT-Q-001（AT-009, AT-010）

---

### FR-Q-002（MUST）：問い抑制（十分な情報がある場合）

十分な情報がある Case では、質問をゼロにするか、あっても `optional=true` のみとする。

- **テスト：** AT-Q-002（AT-001〜AT-008：質問が必須でない場合）

---

### FR-TR-001（MUST）：Trace（監査ログ）

Po_core は処理ステップを Trace として保存・出力する。

**必須 Trace steps：**

| ステップ名 | 説明 |
|-----------|------|
| `parse_input` | 入力の要約 |
| `generate_options` | 生成した Option の一覧 |
| `ethics_review` | 倫理評価の結果 |
| `responsibility_review` | 責任評価の結果 |
| `question_layer` | 質問生成の根拠 |
| `compose_output` | 出力生成のバージョン |

- **合否：** `trace.steps` に上記ステップが存在し、`trace.version` が付与される
- **テスト：** AT-TR-001（AT-001, AT-006）

---

### FR-DEL-001（MUST）：哲学者間 Deliberation の実行

Po_core は哲学者を単純な並列実行+投票に留めず、
Deliberation Engine による多ラウンド議論を経て Pareto 集約を行う。

- `DeliberationEngine` の `max_rounds` パラメータで制御（MUST）
- 高干渉ペアに再提案を要求し、議論の創発を記録する（SHOULD）
- **実装：** `src/po_core/deliberation/engine.py`

---

### FR-SAF-001（MUST）：W_Ethics Gate による倫理審査

全出力は 3 層の W_Ethics Gate（IntentionGate → PolicyPrecheck → ActionGate）を通過する。

- W0: ハードコード禁止カテゴリ（REJECT）
- W1: 意図ゲート（プロンプトインジェクション・ジェイルブレイク検出）
- W2: セマンティック安全性
- W3: ゴール不整合
- W4: 行動審査

- **合否：** 有害入力で SafetyVerdict が REJECT を返す
- **実装：** `src/po_core/safety/wethics_gate/`

---

### FR-SAF-002（MUST）：プロンプトインジェクション・ジェイルブレイク検出

- 注入・ジェイルブレイク攻撃を ≥ 85% の率で検出する（MUST）
- 偽陽性率 ≤ 20%（MUST）
- **実装：** `src/po_core/safety/wethics_gate/detectors.py`

---

### FR-API-001（SHOULD）：REST API による外部連携

- POST /v1/reason が同期推論を提供する（MUST）
- POST /v1/reason/stream が SSE ストリーミングを提供する（MUST）
- X-API-Key 認証・SlowAPI レート制限を実装する（MUST）
- **実装：** `src/po_core/app/rest/`

---

## 6. 非機能要求（Non-Functional Requirements）

### NFR-REP-001（MUST）：再現性

同一入力 ＋ 同一 seed ＋ 同一バージョンでは、JSON 出力が一致する
（少なくとも「構造と主要フィールド」は一致）。

- **テスト：** NT-REP-001（同一 Case で 2 回実行して主要フィールド一致を確認）

---

### NFR-PERF-001（SHOULD）：レイテンシ

- NORMAL モード（39 人）: p50 < 5 s（目標 < 500 ms）✓ 実測 ~33 ms
- WARN モード（5 人）: p50 < 2 s ✓ 実測 ~34 ms
- CRITICAL モード（1 人）: p50 < 1 s ✓ 実測 ~35 ms

---

### NFR-GOV-001（MUST）：変更統制

要件変更は SRS とテストの更新を伴う。

- PR テンプレに要件 ID・テスト更新の項目がある
- CI が必須（パスしない PR はマージ禁止）

---

### NFR-SEC-001（MUST）：セキュリティ

- CORS: `PO_CORS_ORIGINS` 環境変数で制御
- レート制限: SlowAPI + `PO_RATE_LIMIT_PER_MINUTE`
- API キー認証: `PO_API_KEY` 環境変数

---

## 7. 受け入れテスト（Acceptance Tests）セット

詳細は `docs/spec/test_cases.md` を参照。

| テスト ID | シナリオ | 主検証要件 |
|---------|---------|-----------|
| AT-001 | 転職の二択（収入 vs やりがい） | FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001 |
| AT-002 | チームの人員整理（公平 vs 事業継続） | FR-ETH-002, FR-RES-001, FR-UNC-001 |
| AT-003 | 家族の介護（自分の人生 vs 責任） | FR-ETH-001, FR-RES-001, FR-UNC-001 |
| AT-004 | 研究の公開（透明性 vs 悪用リスク） | FR-ETH-002, FR-REC-001 |
| AT-005 | 友人との約束（誠実 vs 自己防衛） | FR-ETH-001, FR-RES-001, FR-Q-001 |
| AT-006 | インシデント対応（透明性 vs 信頼回復） | FR-RES-001, FR-TR-001 |
| AT-007 | 仕事のミス（誠実 vs 隠蔽） | FR-ETH-001, FR-REC-001 |
| AT-008 | 納期固定（速度 vs 品質） | FR-ETH-002, FR-UNC-001, FR-RES-001 |
| AT-009 | 価値観が不明（問い生成必須） | FR-Q-001, FR-OUT-001 |
| AT-010 | 制約が矛盾（矛盾検出＋問い生成） | FR-Q-001, FR-UNC-001 |

---

## 8. 思想→要件→テスト対応表

詳細は `docs/spec/traceability.md` を参照。

---

## 9. 要件 ID インデックス

| 要件 ID | 種別 | 優先度 | 概要 |
|---------|------|--------|------|
| FR-OUT-001 | 機能 | MUST | 出力スキーマ準拠 |
| FR-OPT-001 | 機能 | MUST | 複数選択肢の提示（≥ 2） |
| FR-REC-001 | 機能 | MUST | 推奨＋反証＋代替の同時提示 |
| FR-ETH-001 | 機能 | MUST | 倫理原則の明示（5 原則、2 以上） |
| FR-ETH-002 | 機能 | MUST | 倫理トレードオフの提示 |
| FR-RES-001 | 機能 | MUST | 責任主体の明確化 |
| FR-UNC-001 | 機能 | MUST | 不確実性ラベル（high/medium/low） |
| FR-Q-001 | 機能 | MUST | 問い生成（不足情報あり：1〜5 問） |
| FR-Q-002 | 機能 | MUST | 問い抑制（情報足りる時はゼロか optional） |
| FR-TR-001 | 機能 | MUST | Trace（監査ログ）6 ステップ |
| FR-DEL-001 | 機能 | MUST | 哲学者間 Deliberation |
| FR-SAF-001 | 機能 | MUST | W_Ethics Gate 3 層倫理審査 |
| FR-SAF-002 | 機能 | MUST | プロンプトインジェクション検出 ≥ 85% |
| FR-API-001 | 機能 | SHOULD | REST API（同期・SSE・認証） |
| NFR-REP-001 | 非機能 | MUST | 再現性（同一入力・同一出力） |
| NFR-PERF-001 | 非機能 | SHOULD | レイテンシ（NORMAL p50 < 5 s） |
| NFR-GOV-001 | 非機能 | MUST | 変更統制（CI 必須、SRS+テスト更新） |
| NFR-SEC-001 | 非機能 | MUST | セキュリティ（CORS・レート制限・API キー） |

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成 |
| 0.2 | 2026-02-22 | Phase 6-7 対応追加；FR-DEL-001, FR-SAF-001/002, FR-API-001, NFR-PERF-001, NFR-SEC-001 追加；アーキテクチャ 2 層モデル記載 |
