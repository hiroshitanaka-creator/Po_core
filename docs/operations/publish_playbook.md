# Publish Playbook（TestPyPI → PyPI, Reproducible Release）

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：[docs/status.md](/docs/status.md)
最終オペレータ引き継ぎ（次回リリース用・簡潔版）：[docs/release/release_candidate_handoff_v1.0.3.md](/docs/release/release_candidate_handoff_v1.0.3.md)

このプレイブックは、`.github/workflows/publish.yml` を**人依存なく再現可能**に運用するための固定手順です。

---

## 1. 事前条件（必須）

以下がすべて満たされるまで publish を開始しない。

1. **version整合**
   - `src/po_core/__init__.py` の `__version__` がリリース予定版数になっている（`pyproject.toml` は `project.dynamic = ["version"]` でここから動的読込する）。
   - 開発依存の単一真実源は `tools/dev-requirements.txt` とし、`project.optional-dependencies.dev` / `dependency-groups.dev` は `python scripts/check_dev_dependencies.py` で同期確認済みである。
   - `CHANGELOG.md` の `Unreleased` が更新済みで、リリース内容が説明されている。
2. **publish must-pass checks green**
   - ローカルで以下が成功している（release開始可否の判定条件）。
     - `python scripts/check_dev_dependencies.py`
     - `pytest tests/test_release_readiness.py -v`
     - `pytest tests/acceptance/ -v -m acceptance`
     - `pytest tests/test_output_schema.py -v`
     - `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v`
     - `pytest tests/ -v`
     - `bandit -r src/ scripts/ -c pyproject.toml`
     - `pip-audit` を base / `llm` / `docs` / `viz` の各 dependency surface ごとに clean virtualenv で実行
     - `python -m build`
     - `twine check dist/*`
   - built wheel / sdist を Python 3.10 / 3.11 / 3.12 の clean env で smoke し、`python scripts/release_smoke.py --check-entrypoints` が通っている。smoke は package import/version/resource checks に加えて、REST startup refusal when auth is misconfigured, authenticated startup success, `/v1/health`, `/v1/reason`, deterministic `/v1/reason/stream`, and each console script `--help` plus `po-core version` / `po-core status` / `po-core prompt smoke --format json` / `po-self` / `po-experiment list` を timeout 付きで検証する。
   - ここでいう security gate の対象は、静的解析では `src/` と release/ops の `scripts/`、依存監査では base install と optional extras（`llm`, `docs`, `viz`）である。`dev` extra は CI 自身の実行用ツールとして install されるが、release artifact surface としての `pip-audit` 対象は base + optional extras を明示列挙する。
3. **段階的リリース経路（machine-enforced）**
   - PyPI publish は **同一コミット SHA** に対する `testpypi` environment の successful deployment が GitHub API で確認できた場合にのみ進める。
   - successful TestPyPI deployment が無い、または success 状態でない場合、`publish-guard` が `Run workflow with target=testpypi first.` を含む明示エラーで停止する。
   - つまり PyPI は documentation 上のお願いではなく、GitHub Actions 上で **TestPyPI success が前提条件**になる。
4. **タグ運用と provenance の整合**
   - `workflow_dispatch` / release の publish は `refs/heads/main` または `refs/tags/vX.Y.Z` 以外から publish しない。
   - publish guard は `git merge-base --is-ancestor <publish-sha> origin/main` で、公開対象コミットが `origin/main` 到達可能であることを必須条件として検証する。
   - `vX.Y.Z` タグの `X.Y.Z` は `src/po_core/__init__.py` の `__version__` と一致していなければならない（例: `v1.0.3` ↔ `__version__ = "1.0.3"`）。
   - 同一版数の再公開はしない（PyPIは同一versionの再upload不可）。
5. **Trusted Publishing前提**
   - GitHub Environments に `testpypi` / `pypi` が存在する。
   - TestPyPI/PyPI 側 Trusted Publisher（GitHub Actions OIDC）が設定済み。

---

## 2. リリース直前チェック（コピペ実行）

```bash
python scripts/check_dev_dependencies.py
pytest tests/test_release_readiness.py -v
pytest tests/acceptance/ -v -m acceptance
pytest tests/test_output_schema.py -v
pytest tests/test_golden_e2e.py tests/test_input_schema.py -v
pytest tests/ -v
python -m pip install --upgrade pip
python -m pip install --upgrade build twine bandit pip-audit
bandit -r src/ scripts/ -c pyproject.toml
for surface in base llm docs viz; do
  python -m venv ".audit-${surface}"
  . ".audit-${surface}/bin/activate"
  python -m pip install --upgrade pip pip-audit
  if [ "${surface}" = "base" ]; then
    python -m pip install -e .
  else
    python -m pip install -e ".[${surface}]"
  fi
  pip-audit
  deactivate
  rm -rf ".audit-${surface}"
done
python -m build
twine check dist/*
```

必須コマンド（dependency-SSOT / release-readiness / pytest / security / build/twine）がすべて成功してから GitHub Actions 側の publish を実行する。publish ワークフローでも同じ blocker 群に加えて `python tools/import_graph.py --check --print` を実行し、import-guard を release 前提条件として再検証する。artifact smoke は `scripts/release_smoke.py` に集約し、wheel / sdist の両方で同じ deterministic smoke コマンド群を timeout 付きで再実行する。security では `bandit -r src/ scripts/ -c pyproject.toml` を用いて release-critical scripts も fail-closed に静的解析し、`pip-audit` は base / `llm` / `docs` / `viz` の各 dependency surface を個別 virtualenv で監査する。

---

## 3. TestPyPI 公開手順（workflow_dispatch）

1. GitHub Actions で `Publish to PyPI` ワークフローを開く。
2. `Run workflow` を選択。
3. `target` に `testpypi` を指定して実行。
4. `publish-testpypi` ジョブ成功を確認する。これは後続の PyPI publish を開放する machine-enforced prerequisite でもある。
5. `publish-guard` ジョブが以下を通過していることを確認する。
   - ref が `refs/heads/main` または `refs/tags/vX.Y.Z`
   - publish 対象 SHA が `origin/main` 到達可能
   - タグ実行時は `vX.Y.Z` と `src/po_core/__init__.py` の `__version__` が一致
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
- もし public PyPI version page だけ先に確認できた場合は、まず公開済み版に対する real publication-only evidence（例: `docs/release/pypi_publication_v1.0.2.md`）を追加し、workflow/TestPyPI/smoke の未取得部分は別 evidence file に未取得として分離する。未公開 target version に対しては publication evidence file を捏造せず、candidate-state docs に pending と記録する。

---

## 4. PyPI 本番公開手順

TestPyPI スモーク成功後にのみ実行する。加えて workflow は GitHub API で **同一 SHA の successful `testpypi` deployment** を確認できない限り PyPI へ進まない。

### 4-A. 推奨: Release publish トリガ

1. `src/po_core/__init__.py` の `__version__` がリリース対象版数であることを確認する。
2. `origin/main` 上のレビュー済みコミットに対して `vX.Y.Z` タグを付ける（`X.Y.Z == __version__`）。
3. GitHub Release をそのタグで `published` にする。
4. `Publish to PyPI` ワークフローが `release` イベントで起動する。
5. `publish-guard` が以下 3 条件を通過したことを確認する。
   - tagged commit is reachable from `origin/main`
   - tag version matches package version (`src/po_core/__init__.py`)
   - prior successful TestPyPI deployment exists for the same commit SHA
6. `publish-pypi` ジョブ成功を確認。

### 4-B. 手動: workflow_dispatch トリガ

1. GitHub Actions で `Publish to PyPI` を `Run workflow`。
2. `main` ブランチ、または `vX.Y.Z` タグ（必要なら tag version = package version）を選択する。
3. `target` に `pypi` を指定して実行。
4. `publish-guard` が provenance 検証に加えて、同一 SHA の successful TestPyPI deployment prerequisite を通過したことを確認する。
5. `publish-pypi` ジョブ成功を確認。

公開後の最小検証:

```bash
python -m pip install --upgrade po-core-flyingpig==<VERSION>
python -c "import po_core; print(po_core.__version__)"
```

---

## 4-C. Philosopher execution mode の扱い

- release smoke / publish 手順のために `PO_PHILOSOPHER_EXECUTION_MODE` を `thread` へ戻さない。
- 現行の安全な REST default は `process` であり、public server path は `thread` mode を `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を伴う開発時以外で拒否する。
- release smoke は package install, resource packaging, CLI wiring, REST startup/auth behavior, and deterministic API commands の健全性を確認するものであり、unsafe execution mode を昇格条件の都合で許可しない。

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
- Publish route: workflow_dispatch target=testpypi → release=<tag> or workflow_dispatch target=pypi（PyPI は same-SHA TestPyPI success が prerequisite）
- TestPyPI smoke: pass/fail（ログURL）
- PyPI smoke: pass/fail（ログURL）
- Rollback action (if any): none / <details>
```
