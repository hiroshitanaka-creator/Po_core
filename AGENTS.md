# AGENTS.md — Po_core Agent Playbook (Repo Constitution)

このリポジトリで作業するAIコーディングエージェント（Codex等）向けの運用規約。
目的は **「仕様 → テスト → 実装」のトレーサビリティ**を崩さずに、Po_coreを増築すること。

Po_coreは“賢い文章生成”よりも、**決定性（determinism）**・**説明責任（accountability）**・**安全な変更管理**を優先する。

---

## 0. 最優先ゴール

1) `pytest -q` を常に全通させる  
2) 既存のgolden（期待出力）を **勝手に書き換えない**  
3) 「ケースが増えるほど if が増える地獄」を回避する  
   - 新規対応は **features → rules** で吸収する（case固有分岐を増やさない）

---

## 1. 絶対禁止（破ったら失格）

### 1.1 既存goldenの改変禁止（凍結契約）
以下ファイルは **一切変更禁止**（内容・整形・キー順・改行も禁止）：
- `scenarios/case_001_expected.json`
- `scenarios/case_009_expected.json`

※ これらは “現物仕様（executable specification）” として凍結されている。

### 1.2 逃げの禁止
- `meta` / `trace` を削除してテストを通すのは禁止
- `tests/test_golden_e2e.py` を弱体化して通すのは禁止
- `docs/spec/input_schema_v1.json` / `docs/spec/output_schema_v1.json` を雑に緩めるのは禁止
- 「とりあえず expected を更新して通す」は禁止  
  - golden更新は **仕様変更（ADR/SRS変更）**とセットでのみ許可（後述）

---

## 2. テストと実行コマンド

### 2.1 ローカル（CI相当）
- 最低限：  
  - `pytest -q`

### 2.2 よく使うチェック（推奨）
- `pytest -q tests/test_input_schema.py`
- `pytest -q tests/test_output_schema.py`
- `pytest -q tests/test_golden_e2e.py`

---

## 3. 重要なファイル（必ず読む）

- スキーマ（契約）  
  - `docs/spec/input_schema_v1.json`  
  - `docs/spec/output_schema_v1.json`

- golden diff（E2E契約）  
  - `tests/test_golden_e2e.py`

- シナリオ  
  - `scenarios/*.yaml`（入力）  
  - `scenarios/*_expected.json`（期待出力）

- 実行パイプライン（責務境界の中心）  
  - `src/pocore/runner.py`  
  - `src/pocore/orchestrator.py`  
  - `src/pocore/parse_input.py`  
  - `src/pocore/utils.py`  
  - `src/pocore/engines/*`  
  - `src/pocore/tracer.py`

- ADR（設計決定の拘束力がある文書）
  - `docs/adr/*.md`

---

## 4. “決定性”は仕様（Determinism Contract）

### 4.1 決定性の意味
同一入力（case）＋同一 `seed` ＋同一 `now`（created_at）＋同一バージョンで、
**出力JSONが完全一致**すること。

### 4.2 禁止される非決定性
- wall-clock（`datetime.now()` 等）を直接使う
- UUID等のランダムIDを出す
- dict/listの順序が環境で揺れる生成
- 実行環境依存の値（パス、OS名、CPU数など）を出力に混ぜる

### 4.3 推奨手段
- `now`（= `meta.created_at`）は外部注入（テストが固定文字列を渡す）
- `trace` の時刻は `now + 決定的オフセット` で作る
- `options/questions/steps` の順序はソート規約で固定
  - options: `option_id`
  - questions: `(priority, question_id)`
  - steps: pipeline order

---

## 5. Golden（期待出力）の扱い

### 5.1 goldenの位置づけ
`scenarios/*_expected.json` は **実行可能な仕様書（executable specification）**。
- “ログ”ではない
- “作文”ではない
- CIが殴る現物

### 5.2 goldenを追加する（推奨フロー）
新しいケースをgolden化する時は、次の手順を守る：

1) `scenarios/case_0XX.yaml` を追加（入力スキーマ適合）
2) `run_case_file()` を **決定論パラメータ**で実行し actual JSON を得る  
   - `seed=0`
   - `deterministic=True`
   - `now="2026-02-22T00:00:00Z"` のような固定文字列
3) その actual を `scenarios/case_0XX_expected.json` として保存
4) `pytest -q` 全通を確認
5) 追加したgoldenが “何のfeatureを鍛えるか” をPR本文に明記

### 5.3 goldenを更新する（原則禁止、やるなら儀式）
既存goldenを更新する場合、必ず以下が必要：

- 仕様変更の根拠（ADR/SRSの更新）
- golden更新理由（何がどう変わったか、なぜ正当か）
- `pytest -q` 全通ログ
- レビューで「仕様変更として妥当」と承認されること

※凍結対象（case_001/009）は、明示的に「凍結解除ADR」がない限り更新禁止。

---

## 6. Feature設計（case分岐増殖を止める規約）

### 6.1 方針
新しいケースを通すために `if short_id == ...` を増やさない。  
対応は原則：
- `parse_input` が `features` を増やす
- engines が `features` を見てルールで分岐する

### 6.2 Feature追加のDoD
新しいfeatureを追加するなら必須：
- `src/pocore/parse_input.py`（抽出）
- `tests/test_features.py` にユニットテスト追加（仕様固定）
- 必要なら `docs/adr/` に1本追加（featureの意味・判定ルール）

### 6.3 Featureの役割（責務）
- featuresは **“観測”**：入力から抽出するだけ（推奨や価値判断を入れない）
- 倫理・責任・推奨は **engines** の責務
- 出力の組み立ては **orchestrator** の責務

---

## 7. 責務境界（スパゲッティ防止のための線引き）

### 7.1 parse_input（正規化・観測）
- 入力dictを壊さず、派生情報（features）を作る
- 禁止：推奨文・倫理判断・責任判断の生成

### 7.2 engines（ルールベースの判断）
- 入力（case）＋ features を受けて、次を生成/補強：
  - options（選択肢）
  - ethics/responsibility（評価）
  - questions（不足情報の問い）
  - recommendation（推奨/保留）
  - uncertainty（不確実性サマリ）
- 禁止：ファイルI/O、wall-clock、ランダム

### 7.3 tracer（説明責任ログ）
- `trace` は決定論で生成（nowからオフセット）
- traceが肥大化する場合、詳細は `extensions.trace_debug` 等に隔離（スキーマ拡張と整合させる）

### 7.4 runner（実行口）
- 入力の読み込み（YAML/JSON）とスキーマ検証
- orchestratorへ引き渡し
- 出力スキーマ検証

---

## 8. PRチェックリスト（Definition of Done）

- [ ] 既存凍結golden（case_001/009）を触っていない
- [ ] `pytest -q` 全通
- [ ] 新feature追加なら `tests/test_features.py` にテストがある
- [ ] 新golden追加なら「鍛えたfeature」と「狙い」をPR本文に明記
- [ ] 非決定性（時刻・UUID・乱数）が出力に混入していない
- [ ] スキーマ（input/output）に適合している

---

## 9. よくある事故と対策（短縮メモ）

- **テストが毎回落ちる** → たいてい時刻/順序/IDが揺れている。deterministic契約を疑え。
- **ケース対応のために if が増えた** → features設計に逃がせ。ifは腐る。
- **goldenを更新したくなった** → まずADR。仕様変更を文章で固定してから更新。

---

この規約に反する変更は、Po_coreの目的（説明責任と安全な意思決定支援）を破壊する。

---

## 10. 追記事実（E/F反映）

- trace（generic）の `compose_output.metrics` には recommendation の `arbitration_code` が記録される。  
- ethics は ruleset で運用し、各評価は `rule_id` を持つ。  
- trace から ethics の `rules_fired`（発火ルール集合）を観測できる。  

※上記は事実追記のみ。既存の凍結契約・禁止事項・責務境界はそのまま有効。
