# Po_core — 最終系へのロードマップ

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](/docs/status.md)

> **策定日:** 2026-03-02
> **現在地:** Phases 1–7 完了 · M0 完了 · v0.3.0 · M1 進行中
>
> 「AIは統計的オウムである」という批判に対して、
> 哲学的熟議によって倫理的責任を持つAIが**構築できる**ことを
> コード・テスト・論文で証明する。
> それが `v1.0.0` タグが打たれる瞬間の意味であり、このロードマップの終点である。

---

## 全体地図

```
現在地 (2026-03-02)
│
│  Stage 1: 仕様の完成       [2026-03〜05]  ← M1〜M4
│  Stage 2: v1.0 リリース    [2026-06]      ← PyPI + 全AT通過
│  Stage 3: エコシステム     [2026 Q3-Q4]   ← 永続化・WebSocket・SDK
│  Stage 4: 学術的証明       [2026 Q4-2027] ← 論文・ベンチマーク・コミュニティ
│  Stage 5: 最終系           [2027〜]        ← 哲学的AI推論の参照実装
▼
```

---

## 現在地の確認 (2026-03-02)

| 層 | 状態 |
|----|------|
| **哲学エンジン** (43哲学者・Deliberation・テンソル) | ✅ 完成 |
| **安全性** (W_Ethics Gate・Red Team 100%検出) | ✅ 完成 |
| **配布** (FastAPI・Docker・SSE・AsyncPartyMachine) | ✅ 完成 |
| **自律進化** (FreedomPressureV2・MetaEthicsMonitor・3層メモリ) | ✅ 完成 |
| **AI哲学者** (Claude/GPT/Gemini/Grok スロット) | ✅ 完成 |
| **仕様化** (PRD/SRS/Schema/TestCases/Traceability) | ✅ M0 完成 |
| **E2Eスタブ + 受け入れテスト** | 🔄 M1 進行中 |
| **PyPI 公開** | 🔲 未実施 |
| **倫理・責任エンジン v1** | 🔲 未実装 |
| **問いの層 v1** | 🔲 未実装 |
| **学術論文** | 🔲 執筆中 |

---

## Stage 1: 仕様の完成 — 「証明の準備」

> **期間:** 2026-03-02 〜 2026-05-10
> **目標:** 哲学的思想がコード・テスト・要件として完全にトレース可能な状態にする

### M1: LLMなしE2E（期限: 2026-03-15）

**なぜ重要か:** スタブで全受け入れテストが通ることで、
「哲学エンジンの出力形式が仕様と一致している」ことを証明できる。
LLMへの依存なしにテストが通ることは、アーキテクチャの自律性の証明でもある。

| タスク | 成果物 | 状態 |
|--------|--------|------|
| StubComposer → `output_schema_v1.json` 準拠出力 | `src/po_core/app/composer.py` | ✅ 実装済み |
| AT-001〜AT-010 テストスイート完成 | `tests/acceptance/` | 🔄 進行中 |
| `jsonschema` CI バリデーションゲート追加 | `.github/workflows/ci.yml` | 🔲 |
| Golden files: `case_001_expected.json`, `case_009_expected.json` | `tests/acceptance/scenarios/` | 🔲 |

**完了基準:** `pytest tests/acceptance/ -v` が全10件グリーン（スタブ実装で）

---

### M2: 倫理・責任エンジン v1（期限: 2026-04-05）

**なぜ重要か:** Po_core の存在意義「倫理的責任を持つAI」の核心部分。
ExplanationChain は既に W_Ethics Gate に存在するが、
「倫理的トレードオフの構造化提示」と「責任主体の明示」は未実装。

| タスク | 成果物 | 要件ID |
|--------|--------|--------|
| ethics_v1 実装 | `src/po_core/app/ethics_engine.py` | FR-ETH-001, FR-ETH-002 |
| responsibility_v1 実装 | `src/po_core/app/responsibility_engine.py` | FR-RES-001 |
| 不確実性ラベル実装 | Composer の `uncertainty` フィールド | FR-UNC-001 |
| AT-002〜AT-008 のGolden files 作成 | `tests/acceptance/scenarios/` | 全AT |
| カバレッジレポート自動生成 | Traceability Matrix から自動算出 | NFR-GOV-001 |

**完了基準:** `AT-001〜AT-010` のうち ≥8件がGolden diffで通過

---

### M3: 問いの層 v1（期限: 2026-04-26）

**なぜ重要か:** 「正しい問いを探す」は Po_core の思想的中核。
AIが答えを出すのではなく「次に問うべきこと」を示す機能は、
Po_core を他のAIシステムと根本的に差別化する。

| タスク | 成果物 | 要件ID |
|--------|--------|--------|
| question_layer v1 実装 | `src/po_core/app/question_layer.py` | FR-Q-001, FR-Q-002 |
| 問い生成ロジック（哲学者の問い集約） | DeliberationEngine との統合 | FR-Q-001 |
| 問い抑制ロジック（決断済み案件への問い不要） | IntentionGate との統合 | FR-Q-002 |
| AT-009, AT-010 Golden files 完成 | `tests/acceptance/scenarios/` | AT-Q-001 |

**完了基準:** AT-009「問い生成シナリオ」がGolden diffで通過

---

### M4: ガバナンス完成（期限: 2026-05-10）

**なぜ重要か:** 「思想が変わればSRSとテストも変わる」という変更統制なしには、
プロジェクトの哲学的一貫性は維持できない。v1.0後の外部コントリビュータへの
オンボーディングにも必須。

| タスク | 成果物 | 要件ID |
|--------|--------|--------|
| CI で `jsonschema` 検証を必須ゲートに | `.github/workflows/ci.yml` | NFR-GOV-001 |
| PR テンプレート（要件ID参照必須） | `.github/PULL_REQUEST_TEMPLATE.md` | NFR-GOV-001 |
| ADR 運用フロー文書化 | `docs/spec/adr_guide.md` | NFR-GOV-001 |
| `config_version` 変更時の自動チェック | CI hook | NFR-GOV-001 |
| Traceability Matrix の自動更新スクリプト | `scripts/update_traceability.py` | NFR-GOV-001 |

**完了基準:** PR マージ時に自動で Traceability チェックが走る

---

## Stage 2: v1.0 リリース — 「世界への証明」

> **期間:** 2026-06（M4完了後、約2〜4週間）
> **目標:** 「哲学的AI推論が可能である」ことを PyPI + 論文 + テストで証明する

### 5-F: PyPI 公開（M4完了後即座）

```bash
# GitHub Actions の workflow_dispatch で実行
gh workflow run publish.yml -f environment=testpypi   # TestPyPI 先行確認
gh workflow run publish.yml -f environment=pypi       # 本番 PyPI
```

| チェック項目 | 状態 |
|------------|------|
| `pyproject.toml` version = `0.3.0` | ✅ |
| `publish.yml` OIDC trusted publishing | ✅ |
| `QUICKSTART.md` REST API 例 | ✅ |
| `CHANGELOG.md` エントリ | ✅ |
| TestPyPI での動作確認 | 🔲 |
| PyPI 公開 (`po-core-flyingpig`) | 🔲 |

---

### v1.0.0 タグ（PyPI公開 + 全AT通過後）

**v1.0.0 リリースの定義:**

```
✅ AT-001〜AT-010 全件通過（jsonschema + Golden diff）
✅ PyPI に po-core-flyingpig >= 1.0.0 公開
✅ CI 100% グリーン（pipeline + redteam + acceptance）
✅ CHANGELOG.md に v1.0.0 エントリ
✅ 学術論文ドラフト完成（arXiv 投稿可能状態）
✅ docs/spec/ 全文書 v1.0 に更新
```

**バージョン戦略:**

```
現在: 0.3.0  (beta)
M1:   0.3.0 (release candidate)
M4:   0.2.0    (stable, PyPI)
v1.0: 1.0.0    (全AT通過 + 論文ドラフト完成)
```

---

## Stage 3: エコシステム構築 — 「哲学の持続可能性」

> **期間:** 2026 Q3〜Q4
> **目標:** Po_core を単なるライブラリから「哲学的AI推論のプラットフォーム」へ

### 3-A: 永続化レイヤー

**現状の限界:** InMemoryTracer は再起動でトレースが消える。
監査・再現性・学術研究には永続化が必須。

| タスク | 成果物 |
|--------|--------|
| SQLite トレースDB (`TraceStore`) | `src/po_core/trace/sqlite_store.py` |
| `GET /v1/trace/{session_id}` の永続化対応 | REST router 更新 |
| セッション横断の哲学者品質統計 | `PhilosopherQualityLedger` 永続化 |
| 履歴クエリAPI (`GET /v1/trace/history`) | 新エンドポイント |

---

### 3-B: WebSocket リアルタイムストリーミング

**現状の限界:** SSE は単方向・HTTP長接続ベースで Viewer との双方向性がない。
リアルタイム哲学者議論の「ライブ観覧」は WebSocket が必要。

| タスク | 成果物 |
|--------|--------|
| WebSocket エンドポイント (`/v1/ws/reason`) | `src/po_core/app/rest/routers/ws.py` |
| InMemoryTracer → WebSocket ブリッジ | `src/po_core/trace/ws_bridge.py` |
| Viewer WebUI の WebSocket 対応 | `src/po_core/viewer/web/app.py` 更新 |
| 哲学者ごとのリアルタイム提案表示 | Dash コールバック更新 |

---

### 3-C: Human-in-the-Loop（ESCALATE判定の人間レビュー）

**現状の限界:** `ESCALATE` 判定は「人間のレビューが必要」という判定を返すが、
実際に人間がレビューする仕組みがない。これは Po_core の最重要哲学的コミットメントの欠落。

「人はどんなに関係性を持っても一人で決断する」—
AIが人間の決断を肩代わりすることへの謙虚さの表れとして、
ESCALATE は「AIは降りる」インターフェースを持つべき。

| タスク | 成果物 |
|--------|--------|
| Human Review Queue (`/v1/review/pending`) | REST router |
| レビュー結果の取り込み (`POST /v1/review/{id}/decision`) | REST router |
| Viewer タブ5「Human Review」追加 | Dash app 更新 |
| レビュー待ち中のセッション管理 | `src/po_core/app/review_store.py` |

---

### 3-D: LLMベース違反検出器（W_Ethics Gate 拡張）

**現状の限界:** W_Ethics Gate はルールベース（キーワード + パターン）。
Phase 4 コードに「in production, swap with LLM」コメントが存在する通り、
意図的に置き換え可能な設計になっている。

| タスク | 成果物 |
|--------|--------|
| `LLMViolationDetector` プロトタイプ | `src/po_core/safety/wethics_gate/llm_detector.py` |
| Claude API / ローカルモデル対応 | プラグイン設計 |
| ルールベースとのハイブリッド戦略 | `DetectorChain` |
| Red Team でのベンチマーク（ルールベースvs LLM） | `tests/redteam/test_detector_comparison.py` |

---

### 3-E: 多言語SDK・クライアント

**目標:** `po-core-flyingpig` を Python 以外から使えるようにする。

| タスク | 成果物 |
|--------|--------|
| TypeScript/Node クライアント | `clients/typescript/` |
| OpenAPI TypeScript 型自動生成 | `openapi-typescript` 連携 |
| `po-core-js` npm パッケージ | npm 公開 |

---

## Stage 4: 学術的証明 — 「なぜ飛べるのかの証明」

> **期間:** 2026 Q4 〜 2027 Q1
> **目標:** Po_core の哲学的主張を査読に耐える形で学術的に証明する

### 4-A: 学術論文

**論文タイトル案:**
> "Po_core: A Philosophy-Driven AI Deliberation Framework for Ethical Decision Support"

**主な主張（証明すべきテーゼ）:**

1. **哲学的多様性の可測性:** 43人の哲学者AIペルソナは
   Semantic Delta（コサイン類似度）で定量的に異なることを示す
2. **創発的熟議:** Deliberation Engine による多ラウンド議論は
   単純多数決より倫理的に豊かな結論を生むことを示す
3. **倫理ゲートの実効性:** W_Ethics Gate が
   100%のプロンプトインジェクション検出と≤20%偽陽性を達成することを示す
4. **説明可能性の構造化:** ExplanationChain が
   倫理判定の完全な根拠チェーンを提供することを示す

| タスク | 成果物 | 期限 |
|--------|--------|------|
| 論文ドラフト（英語） | `docs/paper/po_core_paper.pdf` | 2026 Q4 |
| 実験結果の整理（43哲学者ベンチマーク） | `docs/paper/experiments/` | 2026 Q4 |
| arXiv プレプリント投稿 | arXiv.org | 2027 Q1 |
| 査読付き会議/ジャーナル投稿 | AIES / FAccT / NeurIPS Ethics | 2027 |

---

### 4-B: 比較ベンチマーク

**他システムとの比較で Po_core の独自性を示す:**

| 比較軸 | 比較対象 | Po_core の主張 |
|--------|---------|----------------|
| 倫理的多様性 | GPT-4 / Claude 単独 | 43視点の集合的判断 > 1つの観点 |
| 説明可能性 | Chain-of-Thought | ExplanationChain は哲学的根拠を持つ |
| 安全性 | RLHF ベースモデル | W_Ethics Gate はルール+テンソル+意図検出の3層 |
| 創発性 | Mixture-of-Experts | Deliberation Engine は議論による意見修正 |

---

### 4-C: コミュニティ形成

**「哲学者プラグイン」エコシステムの構築:**

| タスク | 成果物 |
|--------|--------|
| `PhilosopherPlugin` 公式仕様 | `docs/philosopher_plugin_spec.md` |
| サードパーティ哲学者追加ガイド | `docs/CONTRIBUTING_PHILOSOPHER.md` |
| テンプレート哲学者モジュール | `src/po_core/philosophers/template.py` |
| GitHub Discussions での哲学議論場 | GitHub コミュニティ設定 |

---

## Stage 5: 最終系 — 「哲学的AI推論の参照実装」

> **期間:** 2027〜
> **目標:** Po_core が「倫理的AI推論とはこういうものだ」という
> 業界・学術界の参照実装（reference implementation）として機能する

### 最終系の3条件

```
┌────────────────────────────────────────────────────┐
│                                                    │
│  条件1: コード                                      │
│  ─────                                             │
│  po-core-flyingpig が PyPI で安定稼働               │
│  v1.0+ · AT-001〜010 全通過                        │
│  43哲学者 + AI4スロット 完全稼働                    │
│                                                    │
│  条件2: 論文                                        │
│  ─────                                             │
│  arXiv プレプリント公開                             │
│  査読付き会議/ジャーナル 採択                       │
│  「Flying Pig Philosophy」が引用される               │
│                                                    │
│  条件3: コミュニティ                                │
│  ─────                                             │
│  サードパーティ哲学者プラグインが存在               │
│  独立した研究者による実験・改良                     │
│  教育機関での AI 倫理授業での利用                   │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 最終アーキテクチャの姿

```
                    ┌─────────────────────────┐
                    │   Po_core Ecosystem      │
                    │                          │
  ┌─────────┐       │  ┌──────────────────┐   │
  │ Python  │──────▶│  │  Core Engine      │   │
  │   API   │       │  │  (43 philosophers)│   │
  └─────────┘       │  │  + LLM detectors  │   │
                    │  └──────────────────┘   │
  ┌─────────┐       │           │              │
  │  REST   │──────▶│  ┌──────────────────┐   │
  │   API   │       │  │  W_Ethics Gate    │   │
  └─────────┘       │  │  (Rules+LLM+3層) │   │
                    │  └──────────────────┘   │
  ┌─────────┐       │           │              │
  │   SDK   │──────▶│  ┌──────────────────┐   │
  │ (TS/JS) │       │  │  Persistent Trace │   │
  └─────────┘       │  │  (SQLite + Query) │   │
                    │  └──────────────────┘   │
                    │           │              │
                    │  ┌──────────────────┐   │
                    │  │  Human Review     │   │
                    │  │  (ESCALATE UI)    │   │
                    │  └──────────────────┘   │
                    │           │              │
                    │  ┌──────────────────┐   │
                    │  │  Viewer WebUI     │   │
                    │  │  (WebSocket RT)   │   │
                    │  └──────────────────┘   │
                    └─────────────────────────┘
```

---

## タイムライン一覧

```
2026-03-15  M1: LLMなしE2E完了 (AT-001〜010 スタブで全通過)
2026-04-05  M2: ethics_v1 + responsibility_v1 実装
2026-04-26  M3: question_layer v1 実装
2026-05-10  M4: ガバナンス完成 (CI全自動 + ADR運用)
2026-06-??  5-F: PyPI公開 (po-core-flyingpig 0.2.0)
2026-06-??  v1.0.0 タグ (全AT通過 + 論文ドラフト)
2026 Q3     3-A: SQLite 永続化
2026 Q3     3-B: WebSocket ストリーミング
2026 Q3     3-C: Human-in-the-Loop ESCALATE UI
2026 Q4     3-D: LLMベース違反検出器 v1
2026 Q4     3-E: TypeScript SDK
2026 Q4     4-A: 学術論文ドラフト完成
2027 Q1     4-A: arXiv プレプリント投稿
2027 Q1     4-B: 比較ベンチマーク完成
2027        4-C: コミュニティ形成 (プラグイン仕様)
2027〜      5:   最終系 (参照実装として機能)
```

---

## 優先順位と依存関係

```
M1 → M2 → M3 → M4 → 5-F → v1.0.0
 │                              │
 │                    ┌─────────┘
 │                    │
 │           3-A (永続化) ← v1.0後に着手
 │           3-B (WebSocket)
 │           3-C (Human Review)
 │           3-D (LLM Detector)
 │           3-E (TypeScript SDK)
 │                    │
 └──────── 4-A (論文) ← M4と並走可能
            4-B (ベンチマーク)
            4-C (コミュニティ)
                    │
                    ▼
              Stage 5: 最終系
```

---

## Flying Pig Philosophy との対応

| テネット | ロードマップでの具現化 |
|---------|---------------------|
| **仮説を大胆に** | 「哲学でAIを作れる」という仮説 → Stage 1-2 で実装完了 |
| **厳密に検証** | AT-001〜010 + 学術論文 → Stage 1-4 で検証 |
| **優雅に改訂** | 失敗はADRに記録・公開。Golden diffで退行を防ぐ → M4以降 |

---

## 定義: 「最終系」とは

> **Po_core の最終系とは、技術的な完成ではなく、概念的な証明の完成である。**
>
> 「AIは統計的オウムである」という批判に対して、
> 哲学的熟議によって倫理的責任を持つAIが **構築できる** ことを、
> コード・テスト・論文の三位一体で証明した状態。
>
> `git tag v1.0.0` は、その証明が完成した瞬間を刻む。

---

*策定: 2026-03-02 | 次回レビュー: M1 完了後 (2026-03-15)*
