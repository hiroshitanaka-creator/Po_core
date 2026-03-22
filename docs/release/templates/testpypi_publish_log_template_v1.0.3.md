# TestPyPI Publish Record Template for v1.0.3 (Not Evidence)

> この文書は **証跡（evidence）ではなく記録テンプレート** です。
> successful workflow run URL や TestPyPI install 成功の実証跡を取得後、実値を記入して evidence へ昇格する。

- Purpose: TestPyPI publish 記録を残すためのテンプレート
- Release target version: `1.0.3`
- Release tag: `v1.0.3`
- Template created at commit: `cd1244b` (claude/audit-po-core-1.0.3-IyRXH)

## workflow run URL
- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL: `TODO: paste successful /actions/runs/<id> URL here`

## 公開したバージョン
- `1.0.3`

## pip install コマンド (TestPyPI)
```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==1.0.3
```
Record observed output:
```text
TODO: paste successful install output
```

## import smoke
```bash
python -c "import po_core; print(po_core.__version__)"
```
Expected: `1.0.3`
Record observed output:
```text
TODO: paste observed output
```

## run smoke
```bash
python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
```
Expected: `ok`
Record observed output:
```text
TODO: paste observed output
```

## release_smoke.py --check-entrypoints (clean venv)
```bash
python scripts/release_smoke.py --check-entrypoints
```
Record observed output:
```text
TODO: paste full transcript
```

## Promotion to evidence checklist
- [ ] Successful TestPyPI run URL recorded
- [ ] `pip install` 実成功ログ記入済み
- [ ] import smoke 実出力記入済み (expected: `1.0.3`)
- [ ] run smoke 実出力記入済み (expected: `ok`)
- [ ] `release_smoke.py --check-entrypoints` 全通過の transcript 記入済み
- [ ] このファイルを `docs/release/testpypi_publish_log_v1.0.3.md` にリネームして evidence 固定
- [ ] `docs/status.md` を更新 (`Latest published = 1.0.3`)
- [ ] `docs/release/pypi_publication_v1.0.3.md` を作成して PyPI URL 固定

## Rule: do not fabricate evidence
remote 証跡（run URL / install 成功ログ / smoke 実出力）の捏造禁止。未取得なら pending として記録する。
