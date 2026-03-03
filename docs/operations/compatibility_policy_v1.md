# Compatibility Policy v1

Po_core を外部参照実装として運用するための互換性ポリシー。

## 1. Scope

このポリシーは以下に適用する。

- `docs/spec/input_schema_v1.json`
- `docs/spec/output_schema_v1.json`
- `scenarios/*_expected.json`（golden）
- `src/pocore/**` の deterministic contract

## 2. Versioning Rules

### 2.1 Semantic intent

- **Patch** (`x.y.Z`): バグ修正のみ。既存スキーマ互換を維持。
- **Minor** (`x.Y.z`): 後方互換な追加（optional field 追加、新ruleset等）。
- **Major** (`X.y.z`): 後方互換を破る変更（必ず ADR + migration guide 更新）。

### 2.2 Schema compatibility

- `output_schema_v1` の既存必須キー削除は禁止。
- enum の既存値削除/変更は禁止。
- 追加は原則 optional から開始する。
- 破壊的変更が必要な場合は `*_v2` を新設し、v1 を deprecation 期間中サポートする。

## 3. Golden Contract

- `scenarios/case_001_expected.json`
- `scenarios/case_009_expected.json`

上記 2 ファイルは凍結対象。更新は「凍結解除ADR」なしでは不可。

既存golden更新時は必須:

1. 仕様変更根拠（ADR/SRS）
2. 変更理由（何が、なぜ妥当か）
3. `pytest -q` 全通

## 4. Determinism Contract

同一入力 + 同一 `seed` + 同一 `now` + 同一version で JSON 完全一致を保証する。

禁止:

- wall-clock 直接参照
- UUID / random の直接出力
- 実行環境依存値の出力混入

## 5. Deprecation Policy

- 非推奨化は最低 1 minor cycle 告知する。
- 告知先:
  - `CHANGELOG.md`
  - `docs/operations/migration_guide_v1.md`
  - PR本文
- deprecation warning は「代替手段」と「撤去時期」を含める。

## 6. Required Validation

互換性を触るPRでは最低以下を実行する。

- `pytest -q tests/test_input_schema.py`
- `pytest -q tests/test_output_schema.py`
- `pytest -q tests/test_golden_e2e.py`
- `pytest -q`
