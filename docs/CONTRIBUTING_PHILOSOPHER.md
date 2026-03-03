# Contributing a Philosopher Plugin

このガイドは、外部/内部の新規哲学者を最短で追加する手順を示す。

## 1. Start from template
`src/po_core/philosophers/template.py` をコピーして新しいモジュールを作る。

例:
- `src/po_core/philosophers/my_philosopher.py`
- クラス名: `MyPhilosopher`

## 2. Implement minimal contract
最低限、以下を実装する。
- `__init__`（`name`, `description`, `tradition`, `key_concepts`）
- `reason(prompt, context=None)`

返り値は少なくとも:
- `reasoning` (str)
- `perspective` (str)
- `metadata.philosopher`

## 3. Register philosopher
### Option A: Runtime injection
`PhilosopherSpec` を作って `PhilosopherRegistry(specs=...)` に渡す。

### Option B: Repository manifest
`src/po_core/philosophers/manifest.py` の `SPECS` に追記する。

## 4. Add tests (required)
最低限この2種類を推奨:
- 契約テスト: `reason()` の必須キー
- パイプラインテスト: `propose()` が `Proposal` を返す

このリポジトリでは `tests/test_philosopher_plugin_template.py` が
テンプレ契約の実例になっている。

## 5. Determinism requirements
- `datetime.now()` / ランダム値を `reason()` 出力に直接埋め込まない
- 同一入力で同一出力を返す

## 6. Quick self-check commands
```bash
pytest -q tests/test_philosopher_plugin_template.py
pytest -q
```

## 7. PR checklist
- [ ] 仕様: `docs/philosopher_plugin_spec.md` に整合
- [ ] テスト追加/更新済み
- [ ] `pytest -q` 全通
- [ ] output schema を破壊していない
