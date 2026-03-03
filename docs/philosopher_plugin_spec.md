# Philosopher Plugin Specification (Phase 24)

## Goal
Po_core に外部哲学者を追加するための **最小契約** を固定する。
この仕様は `src/po_core/philosophers/template.py` と整合する。

## Compatibility Targets
- Python: 3.10+
- Po_core: current `main` branch API
- Interface level:
  - Legacy `reason(prompt, context=None) -> dict`
  - Native `PhilosopherProtocol.propose(...) -> List[Proposal]`（`Philosopher` 基底クラス経由）

## Required Contract
プラグイン哲学者は `po_core.philosophers.base.Philosopher` を継承し、次を満たす。

1. `__init__` で `name`, `description` を設定する
2. `tradition`（str）と `key_concepts`（list[str]）を設定する
3. `reason(prompt, context=None)` を実装し、最低限以下を返す
   - `reasoning: str`
   - `perspective: str`
4. `reason()` の返り値は **決定的** である（同一入力で同一出力）
5. `metadata` は dict を返し、`metadata["philosopher"]` を含める

> `tension`, `rationale`, `confidence`, `action_type`, `citations` は任意だが、
> `normalize_response()` により規約へ正規化される。

## Runtime Guarantees (via base.Philosopher)
`Philosopher` 継承実装は `propose()` 経由で次が保証される。
- `Proposal.confidence` は `[0.0, 1.0]`
- `Proposal.action_type` は許可済み集合へ正規化
- `Proposal.extra["_po_core"]["rationale"]` が存在
- `Proposal.extra["_po_core"]["citations"]` が存在

## Registration Paths
外部哲学者を有効化する方法は2通り。

### A. Runtime injection（推奨、fork不要）
`PhilosopherRegistry(specs=[...])` に `PhilosopherSpec` を注入する。
- `module`: import 可能なモジュールパス
- `symbol`: クラス名（またはファクトリ）
- `philosopher_id`: 一意ID

### B. Manifest edit（repo内追加）
`src/po_core/philosophers/manifest.py` の `SPECS` に追加する。
この方法はリポジトリ変更を伴う。

## Non-goals in this phase
- エントリポイント自動発見（setuptools entry points 等）は未導入
- sandboxed plugin execution は未導入
- schema (`docs/spec/output_schema_v1.json`) の変更は行わない

## Validation Checklist for Plugin Authors
- [ ] `reason()` が dict を返す
- [ ] `reasoning` と `perspective` を返す
- [ ] `metadata.philosopher` が入る
- [ ] 同一入力で出力が一致する
- [ ] `propose()` が `List[Proposal]` を返す（基底実装利用可）
