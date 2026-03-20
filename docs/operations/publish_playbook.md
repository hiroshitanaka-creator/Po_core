# Publish Playbook（TestPyPI → PyPI, Reproducible Release）

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](/docs/status.md)

このプレイブックは、`.github/workflows/publish.yml` を**人依存なく再現可能**に運用するための固定手順です。

---

## 1. 事前条件（必須）

以下がすべて満たされるまで publish を開始しない。

1. **version整合**
   - `pyproject.toml` の `version` がリリース予定版数になっている。
   - `CHANGELOG.md` の `Unreleased` が更新済みで、リリース内容が説明されている。
2. **publish must-pass checks green**
   - ローカルで以下が成功している（release開始可否の判定条件）。
     - `pytest tests/test_release_readiness.py -v`
     - `pytest tests/acceptance/ -v -m acceptance`
     - `pytest tests/test_output_schema.py -v`
     - `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v`
     - `pytest tests/ -v`
     - `bandit -r src/ -c pyproject.toml`
     - `pip-audit`
     - `python -m build`
     - `twine check dist/*`
   - built wheel / sdist を Python 3.10 / 3.11 / 3.12 の clean env で smoke し、`po-core` / `po-self` / `po-trace` / `po-interactive` / `po-experiment` と `python scripts/release_smoke.py --check-entrypoints` が通っている。
3. **タグ運用の整合**
   - `workflow_dispatch` / release の publish は main または `vX.Y.Z` タグ以外から publish しない。
   - `vX.Y.Z` 形式のタグ方針に従う（例: `v1.0.2`）。
   - 同一版数の再公開はしない（PyPIは同一versionの再upload不可）。
4. **Trusted Publishing前提**
   - GitHub Environments に `testpypi` / `pypi` が存在する。
   - TestPyPI/PyPI 側 Trusted Publisher（GitHub Actions OIDC）が設定済み。

---

## 2. リリース直前チェック（コピペ実行）

```bash
pytest tests/test_release_readiness.py -v
pytest tests/acceptance/ -v -m acceptance
pytest tests/test_output_schema.py -v
pytest tests/test_golden_e2e.py tests/test_input_schema.py -v
pytest tests/ -v
python -m pip install --upgrade pip
python -m pip install --upgrade build twine bandit pip-audit
bandit -r src/ -c pyproject.toml
pip-audit
python -m build
twine check dist/*
```

必須コマンド（release-readiness / pytest / security / build/twine）がすべて成功してから GitHub Actions 側の publish を実行する。

---

## 3. TestPyPI 公開手順（workflow_dispatch）

1. GitHub Actions で `Publish to PyPI` ワークフローを開く。
2. `Run workflow` を選択。
3. `target` に `testpypi` を指定して実行。
4. `publish-testpypi` ジョブ成功を確認。
5. workflow YAML の publish guard が main または `vX.Y.Z` タグ以外を拒否していることを確認する。
6. TestPyPI で公開結果を確認。

確認コマンド（クリーン環境推奨）:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==<VERSION>
python -c "import po_core; print(po_core.__version__)"
python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
python -c "from po_core import run; out = run('smoke'); print(out.get('proposal', {}).get('content', ''))"
```

期待値:
- install/import/run が成功し、`TypeError` が発生しない。
- `po_core.__version__` が `<VERSION>` と一致する。

テンプレート昇格手順（evidence化）:
- Rule: remote evidence（run URL / install成功ログ / smoke実出力）を捏造しない。未取得なら pending として記録する。
- successful TestPyPI run 確認後、`docs/release/templates/testpypi_publish_log_template_<VERSION>.md` を複製して `docs/release/testpypi_publish_log_<VERSION>.md` を作成する。
- その evidence ファイルに run URL / install成功ログ / import/run smoke 実出力を実値で記入し、`docs/status.md` の該当行を template から evidence fixed 表現へ更新する。

---

## 4. PyPI 本番公開手順

TestPyPI スモーク成功後にのみ実行する。

### 4-A. 推奨: Release publish トリガ

1. `vX.Y.Z` タグを push して GitHub Release を `published` にする。
2. `Publish to PyPI` ワークフローが `release` イベントで起動する。
3. `publish-pypi` ジョブ成功を確認。

### 4-B. 手動: workflow_dispatch トリガ

1. GitHub Actions で `Publish to PyPI` を `Run workflow`。
2. `target` に `pypi` を指定して実行。
3. `publish-pypi` ジョブ成功を確認。

公開後の最小検証:

```bash
python -m pip install --upgrade po-core-flyingpig==<VERSION>
python -c "import po_core; print(po_core.__version__)"
```

---

## 5. 失敗時ロールバック手順

> 原則: **同一versionの再アップロードはしない**。原因修正後に version を上げて再実行する。

1. **build失敗**（`python -m build` / `twine check`）
   - 原因修正（パッケージメタデータ、依存、long_description等）。
   - ローカルで再度「2. リリース直前チェック」を全通。
2. **OIDC/権限失敗**（Trusted Publishing）
   - GitHub Environment（`testpypi`/`pypi`）制約を確認。
   - TestPyPI/PyPI 側 Trusted Publisher の owner/repo/workflow 条件を確認。
3. **TestPyPIで不具合発見**
   - 本番公開を停止。
   - 修正→version更新→再度 TestPyPI で検証。
4. **PyPI公開後に不具合発見**
   - 必要に応じて該当versionを yanked（削除ではなく非推奨化）。
   - 修正版を `X.Y.Z+1` で再リリース。
   - `CHANGELOG.md` と `docs/status.md` に事後記録を残す。

---

## 6. 実施記録テンプレ（PR本文に貼る）

```md
- Version: <VERSION>
- Local checks: `pytest tests/acceptance/ -v -m acceptance` / `pytest tests/test_output_schema.py -v` / `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v` / `python -m build` / `twine check dist/*` all green
- Optional best-effort: `pytest -q` pass/fail（known failing tests を記録）
- Publish route: workflow_dispatch target=<testpypi|pypi> or release=<tag>
- TestPyPI smoke: pass/fail（ログURL）
- PyPI smoke: pass/fail（ログURL）
- Rollback action (if any): none / <details>
```

