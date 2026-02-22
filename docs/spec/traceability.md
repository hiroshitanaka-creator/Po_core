# Po_core トレーサビリティマトリクス (Traceability Matrix)

**Version:** 0.1
**Date:** 2026-02-22
**参照SRS:** docs/spec/srs_v0.1.md

---

## 1. 思想 → 要件 → テスト 対応表

| 思想 | 要件ID | テストID |
|------|--------|---------|
| 「人はどんなに関係性を持っても一人で決断する」 | FR-RES-001 | AT-RES-001, AT-002, AT-003 |
| 「倫理と責任を共有できるAI」 | FR-ETH-001, FR-ETH-002, FR-TR-001 | AT-ETH-001, AT-ETH-002, AT-TR-001 |
| 「正しい問いを探す」 | FR-Q-001, FR-Q-002 | AT-Q-001, AT-Q-002, AT-009, AT-010 |
| 「透明性こそ信頼の土台」 | FR-TR-001, NFR-REP-001 | AT-TR-001, NT-REP-001 |
| 「断言は不誠実。不確実性を開示する」 | FR-UNC-001, FR-ETH-001 | AT-UNC-001, AT-001〜AT-010 |
| 「推奨には反証を伴う」 | FR-REC-001 | AT-REC-001, AT-001, AT-004, AT-007 |
| 「スキーマが最強の契約」 | FR-OUT-001, NFR-GOV-001 | AT-OUT-001（全テスト共通） |

---

## 2. 要件 → 実装 → テスト 対応表

| 要件ID | 優先度 | 実装コンポーネント | テストファイル |
|--------|--------|----------------|--------------|
| FR-OUT-001 | MUST | `composer_v1.py` | `tests/test_output_schema.py` |
| FR-OPT-001 | MUST | `generator_stub.py` / `option_generator.py` | `tests/test_input_schema.py`, AT-001〜010 |
| FR-REC-001 | MUST | `composer_v1.py` | AT-REC-001 |
| FR-ETH-001 | MUST | `ethics_v1.py` | `tests/test_ethics.py` |
| FR-ETH-002 | MUST | `ethics_v1.py` | `tests/test_ethics.py` |
| FR-RES-001 | MUST | `responsibility_v1.py` | `tests/test_responsibility.py` |
| FR-UNC-001 | MUST | `composer_v1.py` | `tests/test_schema.py` |
| FR-Q-001 | MUST | `question_v1.py` | `tests/test_questions.py` |
| FR-Q-002 | MUST | `question_v1.py` | `tests/test_questions.py` |
| FR-TR-001 | MUST | `tracer_v1.py` | `tests/test_output_schema.py` |
| NFR-REP-001 | MUST | `orchestrator.py`（seed/now注入） | `tests/test_end_to_end.py` |
| NFR-GOV-001 | MUST | CI / PRテンプレ | `.github/workflows/ci.yml` |

---

## 3. シナリオ → 受け入れテスト → 主要要件 対応表

| シナリオファイル | テストID | 主要要件 | golden file |
|----------------|---------|---------|-------------|
| `scenarios/case_001.yaml` | AT-001 | FR-OPT-001, FR-REC-001, FR-ETH-001 | `scenarios/case_001_expected.json` |
| `scenarios/case_002.yaml` | AT-002 | FR-ETH-002, FR-RES-001 | TBD |
| `scenarios/case_003.yaml` | AT-003 | FR-ETH-001, FR-UNC-001 | TBD |
| `scenarios/case_004.yaml` | AT-004 | FR-ETH-002, FR-REC-001 | TBD |
| `scenarios/case_005.yaml` | AT-005 | FR-ETH-001, FR-RES-001 | TBD |
| `scenarios/case_006.yaml` | AT-006 | FR-RES-001, FR-TR-001 | TBD |
| `scenarios/case_007.yaml` | AT-007 | FR-ETH-001, FR-REC-001 | TBD |
| `scenarios/case_008.yaml` | AT-008 | FR-ETH-002, FR-UNC-001 | TBD |
| `scenarios/case_009.yaml` | AT-009 | FR-Q-001 | `scenarios/case_009_expected.json` |
| `scenarios/case_010.yaml` | AT-010 | FR-Q-001, FR-UNC-001 | TBD |

---

## 4. 変更統制ルール（NFR-GOV-001）

```
思想が変わる
    → SRSの要件ID更新 必須
    → テストケースの更新 必須
    → 影響するgolden fileの更新 必須
    → ADRに記録 必須（大きい決定）
    → CIがパスしないPRはマージ禁止
```

---

## 5. ADR（Architecture Decision Records）インデックス

| ADR番号 | タイトル | 日付 | 状態 |
|---------|--------|------|------|
| 0001 | Output Format Selection (JSON+Markdown) | 2026-02-22 | Accepted |
| 0002 | Golden Diff Contract | 2026-02-22 | Accepted |

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成 |
