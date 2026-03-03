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
