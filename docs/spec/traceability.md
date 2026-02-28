# Po_core トレーサビリティマトリクス (Traceability Matrix)

**Version:** 0.3
**Date:** 2026-02-28
**参照 SRS:** docs/spec/srs_v0.1.md
**参照テスト:** docs/spec/test_cases.md

---

## 1. 思想 → 要件 → テスト 対応表

| 思想（PRD §5） | 要件 ID | テスト ID |
|--------------|--------|---------|
| 「人はどんなに関係性を持っても一人で決断する」 → 責任主体の明確化 | FR-RES-001 | AT-RES-001, AT-002, AT-003, AT-005, AT-006, AT-008 |
| 「倫理と責任を共有できる AI」 → 倫理評価の構造化 | FR-ETH-001, FR-ETH-002, FR-TR-001 | AT-ETH-001, AT-ETH-002, AT-TR-001 |
| 「正しい問いを探す」 → 問いの層 | FR-Q-001, FR-Q-002 | AT-Q-001, AT-Q-001b〜d, AT-009, AT-010 |
| 「透明性こそ信頼の土台」 → 監査ログ・再現性 | FR-TR-001, NFR-REP-001 | AT-TR-001, NT-REP-001 |
| 「断言は不誠実。不確実性を開示する」 → 不確実性ラベル | FR-UNC-001, FR-ETH-001 | AT-UNC-001, AT-001〜AT-010 共通 |
| 「推奨には反証を伴う」 → 対案の明示 | FR-REC-001 | AT-REC-001, AT-001, AT-004, AT-007 |
| 「スキーマが最強の契約」 → 出力形式の固定 | FR-OUT-001, NFR-GOV-001 | AT-OUT-001（全テスト共通ガード） |
| 「哲学は対話で深まる」 → 多ラウンド Deliberation | FR-DEL-001 | NT-DEL-001（pipeline CI） |
| 「倫理ゲートが安全保障」 → W_Ethics Gate | FR-SAF-001, FR-SAF-002 | NT-SAF-001〜003（redteam） |

---

## 2. 要件 → 実装 → テスト 対応表

| 要件 ID | 優先度 | 実装コンポーネント | テストファイル | 状態 |
|---------|--------|----------------|--------------|------|
| FR-OUT-001 | MUST | `src/po_core/app/rest/models.py`（ReasonResponse）+ Composer | `tests/unit/test_output_schema.py`（予定） | 🔲 Pending |
| FR-OPT-001 | MUST | `src/po_core/party_machine.py` + Option Generator | AT-001〜010 全テスト | 🔲 Pending |
| FR-REC-001 | MUST | Composer（recommendation フィールド） | AT-REC-001, AT-001, AT-004, AT-007 | 🔲 Pending |
| FR-ETH-001 | MUST | `src/po_core/safety/wethics_gate/explanation.py`（ExplanationChain）+ ethics engine | `tests/unit/test_ethics.py`（予定） | 🔲 Pending |
| FR-ETH-002 | MUST | ethics engine（tradeoffs フィールド） | AT-ETH-002, AT-002, AT-004, AT-008 | 🔲 Pending |
| FR-RES-001 | MUST | responsibility engine | AT-RES-001, AT-002, AT-003, AT-005, AT-006, AT-008 | 🔲 Pending |
| FR-UNC-001 | MUST | Composer（uncertainty フィールド） | AT-UNC-001, AT-002, AT-003, AT-008, AT-010 | 🔲 Pending |
| FR-Q-001 | MUST | question_layer（問い生成） | AT-Q-001, AT-009, AT-010 | 🔲 Pending |
| FR-Q-002 | MUST | question_layer（問い抑制） | AT-Q-002, AT-001〜AT-008（問いなし確認） | 🔲 Pending |
| FR-TR-001 | MUST | `src/po_core/trace/in_memory.py`（InMemoryTracer）+ Composer | AT-TR-001, AT-001, AT-006 | 🔲 Pending |
| FR-DEL-001 | MUST | `src/po_core/deliberation/engine.py`（DeliberationEngine） | `tests/test_run_turn_e2e.py`（CI 必須） | ✅ Implemented |
| FR-SAF-001 | MUST | `src/po_core/safety/wethics_gate/gate.py`（W0〜W4） | `tests/redteam/`（全 redteam テスト） | ✅ Implemented |
| FR-SAF-002 | MUST | `src/po_core/safety/wethics_gate/detectors.py`（PromptInjectionDetector） | `tests/redteam/test_prompt_injection.py` | ✅ Implemented |
| FR-API-001 | SHOULD | `src/po_core/app/rest/`（FastAPI routers） | `tests/unit/test_rest_api.py` | ✅ Implemented |
| NFR-REP-001 | MUST | `src/po_core/runtime/settings.py`（seed injection） | `tests/test_end_to_end.py`（予定） | 🔲 Pending |
| NFR-PERF-001 | SHOULD | `src/po_core/party_machine.py`（AsyncPartyMachine） | `tests/benchmarks/test_pipeline_perf.py` | ✅ Implemented |
| NFR-GOV-001 | MUST | `.github/workflows/ci.yml` + PR テンプレ | CI パス必須 | ✅ Implemented |
| NFR-SEC-001 | MUST | `src/po_core/app/rest/auth.py`, `rate_limit.py` | `tests/unit/test_rest_api.py`（auth テスト） | ✅ Implemented |

---

## 3. シナリオ → 受け入れテスト → 主要要件 対応表

| シナリオファイル | テスト ID | 主要要件 | golden file |
|----------------|---------|---------|-------------|
| `scenarios/case_001.yaml` | AT-001 | FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001 | `scenarios/case_001_expected.json` |
| `scenarios/case_002.yaml` | AT-002 | FR-ETH-002, FR-RES-001, FR-UNC-001 | TBD |
| `scenarios/case_003.yaml` | AT-003 | FR-ETH-001, FR-RES-001, FR-UNC-001 | TBD |
| `scenarios/case_004.yaml` | AT-004 | FR-ETH-002, FR-REC-001, FR-UNC-001 | TBD |
| `scenarios/case_005.yaml` | AT-005 | FR-ETH-001, FR-RES-001 | TBD |
| `scenarios/case_006.yaml` | AT-006 | FR-RES-001, FR-TR-001, FR-ETH-001 | TBD |
| `scenarios/case_007.yaml` | AT-007 | FR-ETH-001, FR-REC-001 | TBD |
| `scenarios/case_008.yaml` | AT-008 | FR-ETH-002, FR-UNC-001, FR-RES-001 | TBD |
| `scenarios/case_009.yaml` | AT-009 | FR-Q-001, FR-OUT-001 | `scenarios/case_009_expected.json` |
| `scenarios/case_010.yaml` | AT-010 | FR-Q-001, FR-UNC-001 | TBD |

---

## 4. 実装コンポーネント → 要件 逆引き表

| 実装ファイル | 対応要件 | 状態 |
|------------|---------|------|
| `src/po_core/ensemble.py` | FR-DEL-001, FR-SAF-001 | ✅ |
| `src/po_core/deliberation/engine.py` | FR-DEL-001 | ✅ |
| `src/po_core/safety/wethics_gate/gate.py` | FR-SAF-001 | ✅ |
| `src/po_core/safety/wethics_gate/intention_gate.py` | FR-SAF-001, FR-SAF-002 | ✅ |
| `src/po_core/safety/wethics_gate/action_gate.py` | FR-SAF-001 | ✅ |
| `src/po_core/safety/wethics_gate/detectors.py` | FR-SAF-002 | ✅ |
| `src/po_core/safety/wethics_gate/explanation.py` | FR-ETH-001（ExplanationChain） | ✅ |
| `src/po_core/trace/in_memory.py` | FR-TR-001 | ✅ |
| `src/po_core/tensors/engine.py` | NFR-PERF-001 | ✅ |
| `src/po_core/tensors/freedom_pressure_v2.py` | NFR-PERF-001 | ✅ |
| `src/po_core/app/rest/server.py` | FR-API-001 | ✅ |
| `src/po_core/app/rest/auth.py` | NFR-SEC-001 | ✅ |
| `src/po_core/app/rest/rate_limit.py` | NFR-SEC-001 | ✅ |
| `src/po_core/app/rest/models.py` | FR-OUT-001, FR-API-001 | ✅ |
| `src/po_core/runtime/settings.py` | NFR-REP-001, NFR-GOV-001 | ✅ |
| `.github/workflows/ci.yml` | NFR-GOV-001 | ✅ |
| `.github/workflows/publish.yml` | ―（PyPI 公開） | 🔲 未実行 |
| **StubComposer**（`src/po_core/app/composer.py`） | FR-OUT-001, FR-OPT-001, FR-REC-001, FR-UNC-001, FR-Q-001, FR-TR-001 | ✅ 実装済み（M1） |
| **ethics_v1**（予定：`src/po_core/app/ethics_engine.py`） | FR-ETH-001, FR-ETH-002 | 🔲 未実装 |
| **responsibility_v1**（予定：`src/po_core/app/responsibility_engine.py`） | FR-RES-001 | 🔲 未実装 |
| **question_layer**（予定：`src/po_core/app/question_layer.py`） | FR-Q-001, FR-Q-002 | 🔲 未実装 |

---

## 5. 変更統制ルール（NFR-GOV-001）

```
思想が変わる
    → SRS の要件 ID 更新 必須
    → docs/spec/traceability.md 更新 必須
    → docs/spec/test_cases.md 更新 必須
    → 影響する golden file の更新 必須
    → ADR に記録 必須（大きい決定）
    → CI がパスしない PR はマージ禁止
    → pareto_table.yaml / battalion_table.yaml 変更時は config_version 更新 必須
```

---

## 6. ADR（Architecture Decision Records）インデックス

| ADR 番号 | タイトル | 日付 | 状態 |
|---------|--------|------|------|
| 0001 | Output Format Selection (JSON + Markdown) | 2026-02-22 | Accepted |
| 0002 | Golden Diff Contract | 2026-02-22 | Accepted |
| 0003 | 2 層アーキテクチャ（哲学審議エンジン + 意思決定支援出力）の採用 | 2026-02-22 | Accepted |
| 0004 | output_schema_v1.json を唯一の出力契約とする | 2026-02-22 | Accepted |
| 0005 | Pareto 設定を YAML 外部化（pareto_table.yaml）、config_version で追跡 | 2026-02-19 | Accepted |

---

## 7. マイルストーン別達成状況

| マイルストーン | 期限 | 要件 | 状態 |
|-------------|------|------|------|
| M0：仕様化の土台 | 2026-03-01 | PRD / SRS / Schema / TestCases / Traceability 作成 | ✅ Complete (2026-02-28) |
| M1：LLM なし E2E | 2026-03-15 | FR-OUT-001, FR-OPT-001, FR-REC-001（スタブ実装で AT-001〜010 通過） | 🔄 In Progress — StubComposer + AT suite 追加済み |
| M2：倫理・責任 v1 | 2026-04-05 | FR-ETH-001/002, FR-RES-001（ethics_v1, responsibility_v1 実装） | 🔲 Pending |
| M3：問いの層 v1 | 2026-04-26 | FR-Q-001/002（question_layer 実装） | 🔲 Pending |
| M4：ガバナンス完成 | 2026-05-10 | NFR-GOV-001（CI / PR テンプレ / ADR 運用） | 🔲 Pending |

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成 |
| 0.2 | 2026-02-22 | FR-DEL-001, FR-SAF-001/002, FR-API-001, NFR-PERF-001, NFR-SEC-001 追加；実装コンポーネント逆引き表・マイルストーン別達成状況・ADR 追加（0003〜0005）；実装済み / 未実装の明示 |
| 0.3 | 2026-02-28 | M0 Complete 反映；StubComposer（`src/po_core/app/composer.py`）実装済みに更新；`tests/acceptance/` AT-001〜AT-010 追加；M1 In Progress に更新；v0.2.0b4 に更新 |
