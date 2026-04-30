# TestPyPI Publish Record Template for v1.1.0 (Not Evidence)

> この文書は **証跡（evidence）ではなく記録テンプレート** です。
> successful workflow run URL や TestPyPI install 成功の実証跡を取得後、実値を記入して evidence へ昇格する。

- Purpose: TestPyPI publish 記録を残すためのテンプレート
- Release target version: `1.1.0`
- Release tag: `v1.1.0`
- Template created at commit: `de78eea` (docs(release): add Step 6 clean wheel install smoke to v1.1.0 RC verification)

## workflow run URL
- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL: `TODO: paste successful /actions/runs/<id> URL here`

## 公開したバージョン
- `1.1.0`

## pip install コマンド (TestPyPI)
```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==1.1.0
```
Record observed output:
```text
TODO: paste successful install output
```

## import smoke
```bash
python -c "import po_core; print(po_core.__version__)"
```
Expected: `1.1.0`
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
- [ ] import smoke 実出力記入済み (expected: `1.1.0`)
- [ ] run smoke 実出力記入済み (expected: `ok`)
- [ ] `release_smoke.py --check-entrypoints` 全通過の transcript 記入済み
- [ ] このファイルを `docs/release/testpypi_publish_log_v1.1.0.md` にリネームして evidence 固定
- [ ] `docs/status.md` を更新 (TestPyPI: 公開済み → Latest published = 1.1.0 on TestPyPI)
- [ ] PyPI本番公開判断へ進む

## Rule: do not fabricate evidence
remote 証跡（run URL / install 成功ログ / smoke 実出力）の捏造禁止。未取得なら pending として記録する。
