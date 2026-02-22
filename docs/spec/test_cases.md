# Po_core 受け入れテスト仕様書 (Acceptance Test Cases)

**Version:** 0.1
**Date:** 2026-02-22
**参照SRS:** docs/spec/srs_v0.1.md

---

## 評価方針

各テストは「正しい答え」を要求しない。要求するのは「手続きの誠実さ」である：

- 必須フィールドが揃っているか
- 倫理原則が明示されているか
- 推奨には反証と代替案が添えられているか
- 不確実性が明示されているか
- 問いが適切に生成されているか（または抑制されているか）

判定は「合格（PASS）/ 不合格（FAIL）」の2値。理由は出力の内容ではなく、手続き（構造・完備性）による。

---

## AT-001：転職の二択

**対応シナリオ：** `scenarios/case_001.yaml`
**主要要件：** FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001

### 入力条件

```yaml
case_id: case_001_job_change
values: ["長期的な成長", "家族との時間", "経済的安定", "誠実さ"]
constraints: ["引っ越し不可", "生活費を下回る収入は不可", ...]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがoutput_schema_v1.jsonに適合する | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-REC-001 | `recommendation.reason`, `counter`, `alternatives` が非空 | PASS必須 |
| AT-ETH-001 | `ethics.principles_used` に2原則以上含まれる | PASS必須 |
| AT-ETH-002 | `ethics.tradeoffs` が非空 | PASS必須 |
| AT-TR-001 | `trace.steps` にparse_inputとcompose_outputが含まれる | PASS必須 |

---

## AT-002：チームの人員整理

**対応シナリオ：** `scenarios/case_002.yaml`
**主要要件：** FR-ETH-002, FR-RES-001, FR-UNC-001

### 入力条件

```yaml
case_id: case_002_headcount_reduction
values: ["公平性", "無危害", "透明性", "事業継続"]
stakeholders: [自分（マネージャ）, チームメンバー, HR, 顧客]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-RES-001 | `responsibility.decision_owner` が非空 | PASS必須 |
| AT-ETH-002 | `ethics.tradeoffs` が非空（公平 vs 事業継続） | PASS必須 |
| AT-UNC-001 | `uncertainty.overall_level` が存在する | PASS必須 |

---

## AT-003：家族の介護

**対応シナリオ：** `scenarios/case_003.yaml`
**主要要件：** FR-ETH-001, FR-UNC-001, FR-RES-001

### 入力条件

```yaml
case_id: case_003_caregiving
values: ["尊厳", "安全", "家族関係の維持", "自分の生活と仕事の継続"]
constraints: ["月の追加負担予算：最大12万円", ...]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-ETH-001 | `ethics.principles_used` に `autonomy` が含まれる | PASS必須 |
| AT-RES-001 | `responsibility.decision_owner` が非空 | PASS必須 |
| AT-UNC-001 | `uncertainty.reasons` が非空 | PASS必須 |

---

## AT-004：研究の公開（脆弱性開示）

**対応シナリオ：** `scenarios/case_004.yaml`
**主要要件：** FR-ETH-002, FR-REC-001, FR-UNC-001

### 入力条件

```yaml
case_id: case_004_security_disclosure
values: ["公共の安全", "透明性", "学術的信用", "説明責任"]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-REC-001 | `recommendation.counter` が非空 | PASS必須 |
| AT-ETH-002 | `ethics.tradeoffs` が非空（安全 vs 透明性） | PASS必須 |

---

## AT-005：友人との約束（誠実 vs 安全）

**対応シナリオ：** `scenarios/case_005.yaml`
**主要要件：** FR-ETH-001, FR-RES-001, FR-Q-001

### 入力条件

```yaml
case_id: case_005_promise_vs_safety
values: ["安全", "信頼関係", "誠実さ", "責任"]
unknowns: ["頻度", "本人の改善意思", "代替手段の有無"]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-ETH-001 | `ethics.principles_used` に `nonmaleficence` か `integrity` が含まれる | PASS必須 |
| AT-RES-001 | `responsibility.decision_owner` が非空 | PASS必須 |

---

## AT-006：インシデント対応（データ漏えい）

**対応シナリオ：** `scenarios/case_006.yaml`
**主要要件：** FR-RES-001, FR-TR-001, FR-ETH-001

### 入力条件

```yaml
case_id: case_006_data_leak_response
values: ["透明性", "説明責任", "無危害", "信頼回復"]
deadline: "2026-02-24"
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-RES-001 | `responsibility.stakeholders` が非空 | PASS必須 |
| AT-TR-001 | `trace.version` が付与されている | PASS必須 |

---

## AT-007：仕事のミス（誠実 vs 隠蔽）

**対応シナリオ：** `scenarios/case_007.yaml`
**主要要件：** FR-ETH-001, FR-REC-001

### 入力条件

```yaml
case_id: case_007_lie_or_admit
values: ["誠実", "説明責任", "信頼維持"]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-REC-001 | `recommendation` が `status` フィールドを持つ | PASS必須 |
| AT-ETH-001 | `ethics.principles_used` に `integrity` が含まれる | PASS必須 |

---

## AT-008：納期固定（速度 vs 品質）

**対応シナリオ：** `scenarios/case_008.yaml`
**主要要件：** FR-ETH-002, FR-UNC-001, FR-RES-001

### 入力条件

```yaml
case_id: case_008_deadline_tradeoff
values: ["ユーザー安全", "信頼", "持続可能性"]
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-OPT-001 | `options.length >= 2` | PASS必須 |
| AT-ETH-002 | `ethics.tradeoffs` が非空 | PASS必須 |
| AT-UNC-001 | `uncertainty.overall_level` が存在する | PASS必須 |

---

## AT-009：価値観が不明（問い生成必須）

**対応シナリオ：** `scenarios/case_009.yaml`
**主要要件：** FR-Q-001, FR-OUT-001

### 入力条件

```yaml
case_id: case_009_unclear_values
values: []  # 空
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-Q-001 | `questions.length >= 1` かつ `<= 5` | PASS必須 |
| AT-Q-001b | 各質問に `why_needed` が非空である | PASS必須 |
| AT-Q-001c | 各質問に `priority` が存在する（1〜5の整数） | PASS必須 |

---

## AT-010：制約の矛盾（矛盾検出＋問い生成）

**対応シナリオ：** `scenarios/case_010.yaml`
**主要要件：** FR-Q-001, FR-UNC-001

### 入力条件

```yaml
case_id: case_010_conflicting_constraints
constraints:
  - "半年以内に起業を本格始動（週20時間以上投入したい）"
  - "収入は一切落とせない"
  - "起業に使える時間は週5時間が上限"
  - "今の仕事は辞めない"
```

### 合否条件

| 条件 | 判定基準 | PASS/FAIL |
|------|---------|-----------|
| AT-OUT-001 | JSONがスキーマに適合 | PASS必須 |
| AT-UNC-001 | `uncertainty.overall_level` が `high` | PASS必須 |
| AT-Q-001 | `questions.length >= 1`（制約矛盾の解消に必要な質問） | PASS必須 |

---

## 合否判定のグローバルルール

1. AT-OUT-001（スキーマ適合）が FAIL の場合、他の条件の評価は行わない
2. MUST 要件の FAIL が1つでもあれば、そのテストは不合格
3. "正しい答え" の評価はしない。評価するのは「構造の誠実さ」のみ
4. options の内容は評価しない。個数と必須フィールドの有無のみ評価
