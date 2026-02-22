# Po_core Software Requirements Specification (SRS) v0.1

**Version:** 0.1
**Date:** 2026-02-22
**Status:** Draft

---

## 0. 目的

Po_coreは「人間が決断するときに、倫理的な軸と説明責任を一緒に持てるようにする」ための意思決定支援システムである。

Po_coreは正解を断言する装置ではなく、選択肢・理由・反証・不確実性・追加で問うべき事項を構造化して提示する装置である。

---

## 1. スコープ

### 1.1 対象（In Scope）

- 意思決定支援（複数案提示、推奨、根拠、反証、不確実性、質問）
- 倫理評価（最低限の原則、トレードオフ明示）
- 責任・説明責任の明示（意思決定主体、影響を受ける関係者）
- 監査ログ（trace）生成
- ルールベース実装を許容（LLM不要）

### 1.2 非対象（Out of Scope）

- 真理判定（世界の事実を確定する機能）
- 医療/法律/金融の最終判断の代行（助言は可能だが責任は取らない）
- 「感情ケア」を目的とした会話最適化（ただしユーザーの主体性を損なわない配慮は必要）

---

## 2. 用語定義

| 用語 | 定義 |
|-----|------|
| **Case** | 意思決定の入力ケース（状況、制約、価値観、期限など） |
| **Option** | 選択肢（行動案） |
| **Ethics Review** | 倫理原則に基づく評価とトレードオフ説明 |
| **Responsibility Review** | 責任主体・利害関係者・説明責任の整理 |
| **Question Layer** | 不足情報や曖昧さを減らすための質問生成 |
| **Trace** | Po_coreが出力を作る過程の監査ログ |
| **Golden File** | 期待出力を固定したJSONファイル（CI検証用） |
| **Deterministic** | 同一入力+seed+バージョンで同一出力を保証する性質 |

---

## 3. システム概要（アーキテクチャ）

Po_coreは以下のパイプラインで構成される（LLM依存しない）：

```
Input Parser
    → Option Generator
    → Ethics Engine
    → Responsibility Engine
    → Question Layer
    → Composer
    → Tracer
```

生成器は差し替え可能なインターフェースにする（将来の自作LMに置換するため）。

---

## 4. インターフェース仕様

### 4.1 入力形式（Case）

YAML/JSONのいずれかをサポート（MUST）。

必須項目（MUST）：
- `case_id`：ケースの一意ID
- `title`：人間向けタイトル
- `problem`：何を決めたいか（テキスト）
- `constraints`：守る制約（配列、空も許容）
- `values`：重視する価値（配列、空も許容）

任意項目（OPTIONAL）：
- `locale`：言語/地域タグ
- `context`：文脈情報（自由形式）
- `deadline`：期限
- `stakeholders`：関係者
- `unknowns`：不明点
- `assumptions`：既置仮定
- `desired_style`：出力スタイル希望

スキーマ：`docs/spec/input_schema_v1.json`

### 4.2 出力形式

- 機械可読：JSON（MUST）
- 人間可読：Markdown（SHOULD）

JSONは `output_schema_v1.json` に適合する（MUST）。

---

## 5. 機能要求（Functional Requirements）

### FR-OUT-001（MUST）：出力スキーマ準拠

Po_coreのJSON出力は `output_schema_v1.json` に必ず適合すること。

**テスト（AT-OUT-001）**
- Given：任意のCase
- When：pocore run
- Then：JSON Schema validationが成功する

---

### FR-OPT-001（MUST）：複数選択肢の提示

Po_coreは最低2つのOptionを提示すること。

例外：Caseが「二択以上が成立しない」と検出された場合のみ、理由を明記して1つでもよい。

**テスト（AT-OPT-001）**
- Given：一般的なCase
- Then：`options.length >= 2` が成立する

---

### FR-REC-001（MUST）：推奨＋反証＋代替の同時提示

Po_coreは推奨を出す場合、必ず以下を併記する：
- 推奨理由（reason）
- 推奨の弱点/反証（counter）
- 代替案（alternatives）

**テスト（AT-REC-001）**
- Given：Case
- Then：`recommendation.reason` と `recommendation.counter` と `recommendation.alternatives` が埋まっている

---

### FR-ETH-001（MUST）：倫理原則の明示

Po_coreは倫理評価で「どの原則を使ったか」を明示する。

**5原則（必須）：**
- `integrity`：誠実（断言しない／不確実性を明示）
- `autonomy`：自律（意思決定主体を奪わない）
- `nonmaleficence`：無危害（害の最小化）
- `justice`：公正（偏りの検出と緩和）
- `accountability`：説明責任（根拠・前提・影響範囲の明示）

**テスト（AT-ETH-001）**
- Given：Case
- Then：`ethics.principles_used` が5原則のうち少なくとも2つ以上含む
- And：各Optionに `ethics_review.tradeoffs` がある

---

### FR-ETH-002（MUST）：倫理トレードオフの提示

Po_coreは単一の倫理を押し付けず、対立価値を最低1つ明示する。

例：公平 vs 効率、短期利益 vs 長期健全性

**テスト（AT-ETH-002）**
- Given：価値観が衝突しうるCase
- Then：`ethics.tradeoffs` が空でない

---

### FR-RES-001（MUST）：責任主体の明確化

Po_coreは「誰が決断し、誰が影響を受けるか」を出力する。

Po_core自身が決断主体であるかのような表現を避ける（例：「私は決める」「あなたは従う」）（MUST）。

**テスト（AT-RES-001）**
- Then：`responsibility.decision_owner` が明示される
- And：禁止表現（簡易ルール）に一致しない

---

### FR-UNC-001（MUST）：不確実性ラベル

Po_coreは断言を避け、不確実性を「high/medium/low」でラベル付けし、根拠を添える。

**テスト（AT-UNC-001）**
- Then：`uncertainty.overall_level` と `uncertainty.reasons` が存在する

---

### FR-Q-001（MUST）：問い生成（不足情報がある場合）

入力Caseに重要情報が欠けていると判断した場合、Po_coreは最大N個（初期N=5）の質問を優先順位付きで出力する。

**テスト（AT-Q-001）**
- Given：`constraints` や `values` が空のCase
- Then：`questions.length` が1以上5以下
- And：各質問に `why_needed`（なぜ必要か）がある

---

### FR-Q-002（MUST）：問い抑制（十分な情報がある場合）

十分な情報があるCaseでは、質問をゼロにするか、あっても `optional=true` のみとする。

**テスト（AT-Q-002）**
- Given：必要項目が埋まったCase
- Then：`questions` が空、または `optional=true` のみ

---

### FR-TR-001（MUST）：Trace（監査ログ）

Po_coreは処理ステップをTraceとして保存/出力する。

最低限のTrace steps：
- `parse_input`：入力の要約
- `generate_options`：生成したOptionの一覧
- `ethics_review`：倫理評価の結果
- `responsibility_review`：責任評価の結果
- `question_layer`：質問生成の根拠
- `compose_output`：出力生成のバージョン

**テスト（AT-TR-001）**
- Then：`trace.steps` に上記ステップが存在する
- And：`trace.version` が付与される

---

## 6. 非機能要求（Non-Functional Requirements）

### NFR-REP-001（MUST）：再現性

同一入力＋同一seed＋同一バージョンでは、JSON出力が一致する（少なくとも「構造と主要フィールド」は一致）。

**テスト（NT-REP-001）**
- 同一Caseで2回実行して主要フィールド一致を確認

---

### NFR-GOV-001（MUST）：変更統制

要件変更はSRSとテストの更新を伴う。

**運用テスト**
- PRテンプレに要件ID・テスト更新の項目がある
- CIが必須

---

## 7. 受け入れテスト（Acceptance Tests）セット

詳細は `docs/spec/test_cases.md` を参照。

| テストID | シナリオ | 主検証項目 |
|---------|---------|-----------|
| AT-001 | 転職の二択（収入 vs やりがい） | FR-OPT-001, FR-REC-001, FR-ETH-001 |
| AT-002 | チームの人員整理（公平 vs 事業継続） | FR-ETH-002, FR-RES-001 |
| AT-003 | 家族の介護（自分の人生 vs 責任） | FR-ETH-001, FR-UNC-001 |
| AT-004 | 研究の公開（透明性 vs 悪用リスク） | FR-ETH-002, FR-REC-001 |
| AT-005 | 友人との約束（誠実 vs 自己防衛） | FR-ETH-001, FR-RES-001 |
| AT-006 | インシデント対応（透明性 vs 信頼回復） | FR-RES-001, FR-TR-001 |
| AT-007 | 仕事のミス（誠実 vs 自己防衛） | FR-ETH-001, FR-REC-001 |
| AT-008 | 納期固定（速度 vs 品質） | FR-ETH-002, FR-UNC-001 |
| AT-009 | 価値観が不明（問い生成必須） | FR-Q-001, FR-OUT-001 |
| AT-010 | 制約が矛盾（矛盾検出＋問い生成） | FR-Q-001, FR-UNC-001 |

---

## 8. 思想→要件→テスト対応表

詳細は `docs/spec/traceability.md` を参照。

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成 |
