# Po_core Product Requirements Document (PRD)

**Version:** 0.2
**Date:** 2026-02-22
**Status:** Active — Phases 1–7 Complete · Heading to v1.0
**Package:** `po-core-flyingpig` v0.2.0b3

---

## 1. 目的 (Purpose)

Po_core は「人間が決断するとき、倫理的な軸と説明責任を一緒に持てるようにする」ための
哲学駆動型 AI 意思決定支援システムである。

Po_core は正解を断言する装置ではなく、選択肢・理由・反証・不確実性・
追加で問うべき事項を **哲学的議論を通じて** 構造化して提示する装置である。

内部では 39 人の哲学者 AI ペルソナが **テンソル演算** と **多ラウンド合意形成**
を通じて協議し、3 層の倫理ゲート（W_Ethics Gate）が出力を審査する。

---

## 2. 対象ユーザー (Target Users)

| ペルソナ | 主な関心 | エントリポイント |
|---------|---------|----------------|
| 個人（複雑な意思決定） | 選択肢・反証・不確実性 | Python API / CLI |
| 組織・チーム（倫理トレードオフ可視化） | 責任主体・利害関係者 | REST API / Docker |
| 専門職（監査・説明責任） | 監査ログ・再現性 | REST API + Trace |
| 研究者・エンジニア | 哲学者 AI の比較・実験 | Python API / Viewer |

---

## 3. スコープ (Scope)

### 3.1 対象 (In Scope)

- **哲学的審議**：39 人（＋AI スロット 4 名）の哲学者による多ラウンド議論
- **意思決定支援**：複数案提示・推奨・根拠・反証・不確実性・質問
- **倫理評価**：W_Ethics Gate（3 層）による ALLOW / REJECT / REVISE 判定と根拠チェーン
- **責任・説明責任の明示**：意思決定主体・影響を受ける関係者・監査ログ
- **テンソル計算**：Freedom Pressure（6D ML）・Semantic Delta・Blocked Tensor
- **透明性**：Po_trace（完全監査ログ）・ExplanationChain・Viewer WebUI
- **REST API**：FastAPI 5 エンドポイント・SSE ストリーミング・認証・レート制限
- **実験管理**：A/B テストフレームワーク（Pareto 設定の統計的最適化）
- **JSON/YAML 形式での入出力**（`output_schema_v1.json` 準拠）

### 3.2 非対象 (Out of Scope)

- 真理判定（世界の事実を確定する機能）
- 医療・法律・金融の最終判断の代行（助言は可能だが責任は取らない）
- 「感情ケア」を目的とした会話最適化
- 外部 LLM への依存（哲学者はルールベース実装；AI スロットは任意プラグイン）

---

## 4. 成功指標 (Success Metrics)

| 指標 | 測定方法 | 目標値 | 現在値 |
|------|---------|--------|--------|
| 受け入れテスト合格率 | pytest / AT-001〜AT-010 | ≥ 8/10 (M2) | 検証中 |
| スキーマ適合率 | jsonschema 検証 | 100% | 実装済み |
| CI 通過率 | GitHub Actions | 100% | 100% ✓ |
| プロンプト注入検出率 | redteam テスト | ≥ 85% | 100% ✓ |
| 偽陽性率 | redteam テスト | ≤ 20% | < 20% ✓ |
| パイプライン p50 レイテンシ | ベンチマーク | < 5 s | ~33 ms ✓ |
| 哲学者セマンティック多様性 | Jaccard 類似度 | 全ペア < 0.85 | < 0.80 ✓ |
| 倫理原則明示率 | FR-ETH-001 | 100% | 実装済み |
| 推奨時の反証提示率 | FR-REC-001 | 100% | 実装済み |

---

## 5. 思想的前提 (Philosophical Premises)

Po_core の設計はこれらの信念に基づく：

| # | 思想 | 対応要件 |
|---|------|---------|
| 1 | **「人はどんなに関係性を持っても一人で決断する」** → 責任主体の明確化 | FR-RES-001 |
| 2 | **「倫理と責任を共有できる AI」** → 倫理評価の構造化 | FR-ETH-001/002 |
| 3 | **「正しい問いを探す」** → 問いの層 | FR-Q-001/002 |
| 4 | **「透明性こそ信頼の土台」** → 監査ログ・再現性 | FR-TR-001, NFR-REP-001 |
| 5 | **「断言は不誠実」** → 不確実性の開示 | FR-UNC-001 |
| 6 | **「推奨には反証を伴う」** → 対案の明示 | FR-REC-001 |
| 7 | **「哲学は対話で深まる」** → 多ラウンド Deliberation | FR-DEL-001 |
| 8 | **「スキーマが最強の契約」** → 出力形式の固定 | FR-OUT-001, NFR-GOV-001 |

---

## 6. コアアーキテクチャ概要

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│  run_turn (10-Step Pipeline)        │
│                                     │
│  1. MemoryRead                      │
│  2. TensorCompute  ← FP-V2, SD, BT │
│  3. SolarWill                       │
│  4. IntentionGate  ← W_Ethics L1   │
│  5. PhilosopherSelect (39 人)       │
│  6. PartyMachine + Deliberation     │
│  7. ParetoAggregate                 │
│  8. ShadowPareto (A/B)              │
│  9. ActionGate     ← W_Ethics L2   │
│  10. MemoryWrite                    │
└─────────────────────────────────────┘
    │
    ▼
Structured Output (output_schema_v1.json)
+ Po_trace (audit log)
+ ExplanationChain (W_Ethics reasoning)
```

---

## 7. ロードマップ (Roadmap)

### 完了フェーズ（Phases 1–7）

| フェーズ | 名称 | 状態 | 完了日 |
|---------|------|------|--------|
| Phase 1 | Resonance Calibration | ✅ COMPLETE | 2026-02-12 |
| Phase 2 | Tensor Intelligence | ✅ COMPLETE | 2026-02-12 |
| Phase 3 | Observability | ✅ COMPLETE | 2026-02-15 |
| Phase 4 | Adversarial Hardening | ✅ COMPLETE | 2026-02-17 |
| Phase 5 | Productization | ✅ COMPLETE (5-A〜E) | 2026-02-21 |
| Phase 6 | Autonomous Evolution | ✅ COMPLETE | 2026-02-21 |
| Phase 7 | AI Philosopher Slots | ✅ COMPLETE | 2026-02-21 |

### 仕様化フェーズ（Phases M0–M4）

| マイルストーン | 期限 | 主な成果物 | 状態 |
|--------------|------|-----------|------|
| M0：仕様化の土台 | 2026-03-01 | PRD / SRS / Schema / TestCases / Traceability | 🔄 In Progress |
| M1：LLM なし E2E | 2026-03-15 | スタブ生成器 + orchestrator + E2E テスト | 🔲 Pending |
| M2：倫理・責任 v1 | 2026-04-05 | ethics_v1 / responsibility_v1 | 🔲 Pending |
| M3：問いの層 v1 | 2026-04-26 | question_v1 | 🔲 Pending |
| M4：ガバナンス完成 | 2026-05-10 | CI / テンプレ / ADR 運用 | 🔲 Pending |

### 残タスク

| タスク | 状態 |
|--------|------|
| **PyPI 公開**（5-F）| 🔲 PENDING — `publish.yml` 準備済み、未実行 |
| v1.0 安定化 | 🔲 Pending |
| 学術論文 | 🔲 Draft in preparation |

---

## 8. 制約 (Constraints)

- Python 3.10+ で実装
- フレームワーク（FastAPI 等）は使用可
- 外部 LLM の重みへの直接依存は避ける（AI スロットは任意プラグイン）
- 変更統制：仕様変更は SRS とテストの更新を伴う（NFR-GOV-001）
- `pareto_table.yaml` / `battalion_table.yaml` 変更時は `config_version` を更新

---

## 9. 用語

| 用語 | 定義 |
|-----|------|
| **Case** | 意思決定の入力ケース（状況・制約・価値観・期限など） |
| **Option** | 選択肢（行動案） |
| **Proposal** | 哲学者 1 人が生成した応答（`domain/proposal.py`） |
| **Freedom Pressure** | 自由度・責任・緊急性等を表す 6D テンソル |
| **Semantic Delta** | 入力と記憶の意味的乖離度（0.0〜1.0） |
| **Blocked Tensor** | 有害性・制約違反の推定スコア |
| **W_Ethics Gate** | 3 層倫理ゲート（IntentionGate → PolicyPrecheck → ActionGate） |
| **SafetyMode** | NORMAL / WARN / CRITICAL（freedom_pressure で決定） |
| **ExplanationChain** | 倫理判定の根拠チェーン（構造化 JSON） |
| **Trace** | Po_core が出力を作る過程の完全監査ログ |

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成 |
| 0.2 | 2026-02-22 | Phase 6-7 完了を反映；アーキテクチャ概要・用語追加；仕様化マイルストーン追記 |
