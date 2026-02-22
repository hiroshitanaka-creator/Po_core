# ADR 0001: Output Format Selection (JSON + Markdown)

**Date:** 2026-02-22
**Status:** Accepted
**Deciders:** Po_core project

---

## Context

Po_coreは意思決定支援の出力を生成する。出力は「機械（CI/他システム）」と「人間（意思決定者）」の両方が消費する必要がある。

## Decision

出力フォーマットを以下の2層とする：

1. **JSON（MUST）** — 機械可読、スキーマ適合必須（`output_schema_v1.json`）
2. **Markdown（SHOULD）** — 人間可読、`rendered.markdown` フィールドに格納

## Rationale

- JSONはスキーマ検証が可能で、CI（jsonschema）による自動検証と「契約としての強度」を保てる
- Markdownは人間の確認・共有に使いやすい
- 両者を別フィールドに分離することで、スキーマ検証を JSON だけに集中できる
- XMLやYAML出力は採用しない（JSONが既存ツールチェーンとの親和性が高い）

## Consequences

- 出力テストはJSONに集中する（Markdownはオプション）
- `output_schema_v1.json` が唯一の真実（Single Source of Truth）
- Markdownの形式は自由（スキーマ検証対象外）
- 将来的なフォーマット追加は `extensions` フィールドで吸収する

## Alternatives Considered

| 代替案 | 却下理由 |
|-------|---------|
| YAML出力 | ツールサポートが分散、スキーマ検証が複雑 |
| XML出力 | 冗長、Pythonエコシステムとの親和性が低い |
| Markdown only | 機械検証不可、CI殴りができない |
