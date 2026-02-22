# Po_core 受け入れテスト仕様書 (Acceptance Test Cases)

**Version:** 0.2
**Date:** 2026-02-22
**参照 SRS:** docs/spec/srs_v0.1.md
**参照スキーマ:** docs/spec/output_schema_v1.json

---

## 評価方針

Po_core の受け入れテストは「正しい答え」を要求しない。要求するのは「手続きの誠実さ」である：

- 必須フィールドが揃っているか（`output_schema_v1.json` 準拠）
- 倫理原則が明示されているか（FR-ETH-001）
- 推奨には反証と代替案が添えられているか（FR-REC-001）
- 不確実性が明示されているか（FR-UNC-001）
- 問いが適切に生成または抑制されているか（FR-Q-001/002）
- 責任主体が明示されているか（FR-RES-001）
- 監査ログが記録されているか（FR-TR-001）

判定は「合格（PASS）/ 不合格（FAIL）」の 2 値。
AT-OUT-001（スキーマ適合）が FAIL の場合、他の条件の評価は行わない。

---

## グローバルルール

1. **AT-OUT-001 ガード**：JSON が `output_schema_v1.json` に適合しない場合、テスト全体 FAIL
2. **MUST の 1 つでも FAIL → テスト不合格**
3. **「正しい答え」は評価しない**：評価するのは「構造の誠実さ」のみ
4. **options の内容は評価しない**：個数と必須フィールドの有無のみ評価
5. **禁止表現チェック**（FR-RES-001）：「Po_core は決断する」「あなたは従うべき」等の表現が出力に含まれれば FAIL

---

## AT-001：転職の二択（収入 vs やりがい）

**対応シナリオ：** `scenarios/case_001.yaml`
**主要要件：** FR-OPT-001, FR-REC-001, FR-ETH-001, FR-TR-001
**テストファイル：** `tests/acceptance/test_at_001.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_001_job_change
title: "転職すべきか：現職維持 vs やりがい優先の転職"
problem: "現職は安定しているが成長感がない。転職先はやりがいがあるが収入が2割減。"
values: ["長期的な成長", "家族との時間", "経済的安定", "誠実さ"]
constraints: ["引っ越し不可", "生活費を下回る収入は不可"]
stakeholders: ["自分", "配偶者", "子ども（2人）"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON が `output_schema_v1.json` に適合する | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-REC-001 | `recommendation.reason`・`counter`・`alternatives` が非空 | MUST |
| AT-ETH-001 | `ethics.principles_used` に 2 原則以上含まれる | MUST |
| AT-ETH-002 | `ethics.tradeoffs` が非空 | MUST |
| AT-TR-001 | `trace.steps` に `parse_input` と `compose_output` が含まれる | MUST |
| AT-TR-001b | `trace.version` が付与されている | MUST |

---

## AT-002：チームの人員整理（公平 vs 事業継続）

**対応シナリオ：** `scenarios/case_002.yaml`
**主要要件：** FR-ETH-002, FR-RES-001, FR-UNC-001
**テストファイル：** `tests/acceptance/test_at_002.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_002_headcount_reduction
title: "チームの人員整理：誰を残し誰を外すか"
problem: "事業縮小のため3名の削減が必要。チームメンバー8名。"
values: ["公平性", "無危害", "透明性", "事業継続"]
constraints: ["2週間以内に決定が必要", "法的要件への準拠"]
stakeholders: ["自分（マネージャ）", "チームメンバー8名", "HR", "顧客"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-RES-001 | `responsibility.decision_owner` が非空 | MUST |
| AT-RES-001b | `responsibility.stakeholders` が非空 | MUST |
| AT-ETH-002 | `ethics.tradeoffs` が非空（公平 vs 事業継続が含まれることが望ましい） | MUST |
| AT-UNC-001 | `uncertainty.overall_level` が存在する | MUST |
| AT-UNC-001b | `uncertainty.reasons` が非空 | MUST |

---

## AT-003：家族の介護（自分の人生 vs 家族への責任）

**対応シナリオ：** `scenarios/case_003.yaml`
**主要要件：** FR-ETH-001, FR-RES-001, FR-UNC-001
**テストファイル：** `tests/acceptance/test_at_003.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_003_caregiving
title: "親の介護：自分でするか施設に委ねるか"
problem: "高齢の親が要介護状態に。自宅介護か施設入居か決断が必要。"
values: ["尊厳", "安全", "家族関係の維持", "自分の生活と仕事の継続"]
constraints:
  - "月の追加負担予算：最大12万円"
  - "フルタイム勤務継続が必要"
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-ETH-001 | `ethics.principles_used` に `autonomy` が含まれる | MUST |
| AT-ETH-001b | `ethics.principles_used` の件数 >= 2 | MUST |
| AT-RES-001 | `responsibility.decision_owner` が非空 | MUST |
| AT-UNC-001 | `uncertainty.reasons` が非空 | MUST |

---

## AT-004：研究の公開（透明性 vs 悪用リスク）

**対応シナリオ：** `scenarios/case_004.yaml`
**主要要件：** FR-ETH-002, FR-REC-001, FR-UNC-001
**テストファイル：** `tests/acceptance/test_at_004.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_004_security_disclosure
title: "セキュリティ脆弱性の公開：責任ある開示のタイミング"
problem: "重大な脆弱性を発見した。即時公開すれば社会的透明性が高まるが悪用リスクがある。"
values: ["公共の安全", "透明性", "学術的信用", "説明責任"]
stakeholders: ["研究者自身", "ベンダー", "一般ユーザー", "悪意ある攻撃者"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-REC-001 | `recommendation.counter` が非空 | MUST |
| AT-REC-001b | `recommendation.alternatives` が非空 | MUST |
| AT-ETH-002 | `ethics.tradeoffs` が非空（安全 vs 透明性 の緊張が含まれることが望ましい） | MUST |
| AT-UNC-001 | `uncertainty.overall_level` が存在する | MUST |

---

## AT-005：友人との約束（誠実 vs 自己防衛）

**対応シナリオ：** `scenarios/case_005.yaml`
**主要要件：** FR-ETH-001, FR-RES-001, FR-Q-001
**テストファイル：** `tests/acceptance/test_at_005.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_005_promise_vs_safety
title: "友人の秘密を守るか：約束 vs 安全"
problem: "友人が危険な状況にある可能性がある。秘密にすると約束したが、第三者への報告も検討している。"
values: ["安全", "信頼関係", "誠実さ", "責任"]
unknowns: ["危険の頻度", "本人の改善意思", "代替手段の有無"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-ETH-001 | `ethics.principles_used` に `nonmaleficence` または `integrity` が含まれる | MUST |
| AT-ETH-001b | `ethics.principles_used` の件数 >= 2 | MUST |
| AT-RES-001 | `responsibility.decision_owner` が非空 | MUST |

---

## AT-006：インシデント対応（透明性 vs 信頼回復速度）

**対応シナリオ：** `scenarios/case_006.yaml`
**主要要件：** FR-RES-001, FR-TR-001, FR-ETH-001
**テストファイル：** `tests/acceptance/test_at_006.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_006_data_leak_response
title: "データ漏えいインシデントへの対応"
problem: "顧客データの漏えいが発覚。即時公表 vs 影響範囲特定後の公表 vs 段階的公表のいずれかを選ぶ必要がある。"
values: ["透明性", "説明責任", "無危害", "信頼回復"]
deadline: "2026-02-24T00:00:00Z"
stakeholders: ["自社", "顧客", "監督機関", "メディア"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-RES-001 | `responsibility.stakeholders` が非空 | MUST |
| AT-RES-001b | `responsibility.decision_owner` が非空 | MUST |
| AT-ETH-001 | `ethics.principles_used` に `accountability` が含まれる | MUST |
| AT-TR-001 | `trace.version` が付与されている | MUST |
| AT-TR-001b | `trace.steps` が非空 | MUST |

---

## AT-007：仕事のミス（誠実 vs 隠蔽）

**対応シナリオ：** `scenarios/case_007.yaml`
**主要要件：** FR-ETH-001, FR-REC-001
**テストファイル：** `tests/acceptance/test_at_007.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_007_lie_or_admit
title: "仕事のミスを報告するか隠すか"
problem: "業務上のミスが発覚した。上司への即時報告 vs 自力で修正してから報告 vs 黙認のいずれかを選ぶ。"
values: ["誠実", "説明責任", "信頼維持"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-REC-001 | `recommendation` が `status` フィールドを持つ | MUST |
| AT-REC-001b | `recommendation.status == "recommended"` の場合、`counter` が非空 | MUST |
| AT-ETH-001 | `ethics.principles_used` に `integrity` が含まれる | MUST |
| AT-ETH-001b | `ethics.principles_used` の件数 >= 2 | MUST |

---

## AT-008：納期固定（速度 vs 品質）

**対応シナリオ：** `scenarios/case_008.yaml`
**主要要件：** FR-ETH-002, FR-UNC-001, FR-RES-001
**テストファイル：** `tests/acceptance/test_at_008.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_008_deadline_tradeoff
title: "固定された納期と品質のトレードオフ"
problem: "重要な機能の納期が 1 週間後に固定されている。品質基準を落として納期厳守するか、納期延長を交渉するか。"
values: ["ユーザー安全", "信頼", "持続可能性"]
constraints: ["納期は顧客契約で固定", "チームリソースは現状固定"]
stakeholders: ["自分（PL）", "開発チーム", "顧客", "エンドユーザー"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-OPT-001 | `options.length >= 2` | MUST |
| AT-ETH-002 | `ethics.tradeoffs` が非空 | MUST |
| AT-UNC-001 | `uncertainty.overall_level` が存在する | MUST |
| AT-RES-001 | `responsibility.decision_owner` が非空 | MUST |

---

## AT-009：価値観が不明（問い生成必須）

**対応シナリオ：** `scenarios/case_009.yaml`
**主要要件：** FR-Q-001, FR-OUT-001
**テストファイル：** `tests/acceptance/test_at_009.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_009_unclear_values
title: "価値観が未定義な状態での意思決定"
problem: "将来のキャリアについて考えているが、何を重視すべきか自分でもわかっていない。"
values: []    # 空 — 問い生成を強制
constraints: []
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-Q-001 | `questions.length >= 1` かつ `<= 5` | MUST |
| AT-Q-001b | 各質問に `why_needed` が非空である | MUST |
| AT-Q-001c | 各質問に `priority` が存在する（1〜5 の整数） | MUST |
| AT-Q-001d | 少なくとも 1 件の質問が `optional == false`（重要質問がある） | MUST |

---

## AT-010：制約の矛盾（矛盾検出＋問い生成）

**対応シナリオ：** `scenarios/case_010.yaml`
**主要要件：** FR-Q-001, FR-UNC-001
**テストファイル：** `tests/acceptance/test_at_010.py`（予定）

### 前提条件（Given）

```yaml
case_id: case_010_conflicting_constraints
title: "矛盾した制約のもとでの起業計画"
problem: "副業として起業を検討しているが、制約が相互に矛盾している。"
constraints:
  - "半年以内に起業を本格始動（週20時間以上投入したい）"
  - "収入は一切落とせない"
  - "起業に使える時間は週5時間が上限"
  - "今の仕事は辞めない"
values: ["経済的自立", "自己実現", "家族の安定"]
```

### 操作（When）

```
po_core.run(case) または POST /v1/reason
```

### 合否条件（Then）

| 条件 ID | 判定基準 | 優先度 |
|--------|---------|--------|
| AT-OUT-001 | JSON がスキーマに適合 | MUST |
| AT-UNC-001 | `uncertainty.overall_level` が `"high"` | MUST |
| AT-UNC-001b | `uncertainty.known_unknowns` が非空（矛盾の記録） | MUST |
| AT-Q-001 | `questions.length >= 1`（制約矛盾の解消に必要な質問） | MUST |
| AT-Q-001b | 各質問に `why_needed` が非空 | MUST |

---

## テスト実行方法

```bash
# 受け入れテストの実行（テストファイル実装後）
pytest tests/acceptance/ -v -m acceptance

# JSON Schema 検証のみ（jsonschema ライブラリ使用）
python -c "
import json, jsonschema
schema = json.load(open('docs/spec/output_schema_v1.json'))
output = json.load(open('scenarios/case_001_expected.json'))
jsonschema.validate(output, schema)
print('PASS: schema valid')
"

# Golden File 比較
python -c "
import json
expected = json.load(open('scenarios/case_001_expected.json'))
actual   = json.load(open('/tmp/case_001_actual.json'))
# 主要フィールド比較（NFR-REP-001）
assert expected['meta']['schema_version'] == actual['meta']['schema_version']
print('PASS: schema_version matches')
"
```

---

## 合否判定のグローバルルール（再掲）

1. **AT-OUT-001（スキーマ適合）が FAIL** の場合、他の条件の評価は行わない
2. **MUST 要件の FAIL が 1 つでもあれば**、そのテストは不合格
3. **「正しい答え」の評価はしない**：評価するのは「構造の誠実さ」のみ
4. **options の内容は評価しない**：個数と必須フィールドの有無のみ評価
5. **禁止表現チェック**（FR-RES-001）：Po_core 自身が意思決定主体のように書かれていれば FAIL

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| 0.1 | 2026-02-22 | 初版作成（10 テストケース） |
| 0.2 | 2026-02-22 | Given/When/Then 形式に統一；条件 ID 細分化（AT-REC-001b, AT-ETH-001b 等）；テスト実行方法セクション追加；グローバルルール明確化 |
