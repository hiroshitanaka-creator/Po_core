# Release Runbook (TestPyPI → PyPI)

このドキュメントは Phase 15（5-F）の公開手順を固定するための運用Runbookです。

## 1. 事前確認（publish workflow 点検結果）

- `./.github/workflows/publish.yml` は存在し、以下を満たしている。
  - `build` ジョブで `python -m build` と `twine check dist/*` を実行。
  - `workflow_dispatch` で `target=testpypi|pypi` を選択可能。
  - TestPyPI 公開ジョブは `repository-url: https://test.pypi.org/legacy/` を使用。
  - PyPI 公開ジョブは release publish または `target=pypi` で実行。
  - いずれも `id-token: write` を使う Trusted Publishing 前提。

## 2. リリース前チェック（ローカル）

```bash
pytest -q
python -m pip install --upgrade build twine
python -m build
twine check dist/*
```

## 3. TestPyPI 公開手順

1. GitHub の `Settings > Environments` で `testpypi` environment を作成済みであることを確認。
2. TestPyPI 側で Trusted Publisher（GitHub Actions OIDC）を `po-core-flyingpig` に紐付ける。
3. GitHub Actions から `Publish to PyPI` workflow を `workflow_dispatch` で起動し、`target=testpypi` を選択。
4. 成功後、TestPyPI の project page を確認する。

## 4. TestPyPI スモークテスト最小コマンド

クリーンな仮想環境で次を実行:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig
python -c "import po_core; print(po_core.__version__)"
python -c "from po_core import run; out = run('テスト入力', run_fast=True); print(type(out).__name__)"
```

期待値:
- import が成功する。
- `po_core.__version__` が TestPyPI に上げた版数と一致する。
- `run(...)` が例外なく戻り値を返す。

## 5. 本番 PyPI 公開手順

1. TestPyPI スモーク成功後、`Settings > Environments` の `pypi` environment 制約を確認。
2. PyPI 側で Trusted Publisher（GitHub Actions OIDC）設定を確認。
3. 以下のいずれかで publish を実行。
   - GitHub Release を `published` にする（タグ運用）。
   - `workflow_dispatch` で `target=pypi` を選択。
4. 公開後に本番PyPIで `pip install po-core-flyingpig` が可能か確認する。

## 6. ロールバック/失敗時の基本方針

- ワークフロー失敗時は、まず `build` と `twine check` の失敗ログを優先確認。
- Trusted Publishing の失敗（OIDC/permission）は environment 設定と publisher 紐付けを再確認。
- PyPI は同一バージョン再アップロード不可のため、必要ならバージョンをインクリメントして再実行する。
