# Reproducibility Runbook (Bench / Paper / Trace)

Phase 25 向けに、再現手順を 1 コマンド実行にまとめた運用手順。

## Quick start

```bash
python scripts/phase25_reproduce.py --profile external
```

## Profiles

- `external`: 外部利用者向け最小検証（schema + golden + traceability）
- `full`: 開発者向け包括検証（external + full pytest）

## What each profile runs

### external

1. `pytest -q tests/test_input_schema.py`
2. `pytest -q tests/test_output_schema.py`
3. `pytest -q tests/test_golden_e2e.py`
4. `pytest -q tests/test_traceability.py`

### full

- `external` の全項目
- `pytest -q`

## Optional bench/paper commands

必要に応じて、以下を別途実行する。

- ベンチ: `pytest -q tests/benchmarks/test_pipeline_perf.py::test_bench_smoke_critical -s`
- 実験パイプライン smoke: `pytest -q tests/integration/test_experiment_pipeline.py`

## Dry run (command preview)

```bash
python scripts/phase25_reproduce.py --profile full --dry-run
```

## CI embedding example

```bash
python scripts/phase25_reproduce.py --profile full
```

失敗時は最初の failing command を表示し、即時終了する。


## TestPyPI publish verification (v0.2.0rc1)

Phase 5-F（PyPI公開）の運用手順。`publish.yml` は `workflow_dispatch` で `target=testpypi` を受け取り、TestPyPI 公開ジョブを起動する。

### 1) GitHub Actions で公開実行

```bash
# GitHub CLI 利用時（推奨）
gh workflow run publish.yml -f target=testpypi

# 互換運用: environment 入力を使う運用をしている場合
#（現行 workflow は target 入力）
gh workflow run publish.yml -f environment=testpypi
```

実行後に Actions UI で `Publish to TestPyPI` ジョブ成功を確認する。

### 2) TestPyPI から install/import smoke test

```bash
python -m venv .venv-testpypi
source .venv-testpypi/bin/activate
python -m pip install --upgrade pip

# TestPyPI を優先しつつ依存は PyPI を参照
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  po-core-flyingpig==0.2.0rc1

python -c "import po_core; print(po_core.__name__)"
```

期待値:
- `pip install` が成功する
- import コマンドで `po_core` が表示される

### 3) 失敗時の切り分け（PR記載テンプレ）

PR本文に以下3点を必ず残す。

- **原因 (Cause):** どのステップで失敗したか（build / trusted publishing / install / import）
- **対策 (Fix):** その場で行った修正（workflow入力値、環境設定、依存関係など）
- **再発防止 (Prevention):** 次回の事前チェック（release tag運用、workflow_dispatch入力、twine check、smoke test自動化）

#### よくある失敗例

- OIDC trusted publishing 未設定（PyPI/TestPyPI 側の project settings mismatch）
- `workflow_dispatch` 入力名の不一致（`target` と `environment` の取り違え）
- TestPyPIに同一バージョンが既に存在（`skip_existing` で公開はスキップされる）
- install時に `--extra-index-url https://pypi.org/simple` を付け忘れ依存解決失敗
