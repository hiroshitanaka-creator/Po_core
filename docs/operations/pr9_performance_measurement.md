# PR-9 Performance Measurement Guide

このガイドは、PR-9（キャッシュ / 適応並列 / プリロード）の速度改善を再現可能に測るための手順です。

## 1. 前提

- 再現性優先のため、比較時は同一マシン・同一依存関係で実行する。
- 測定中は不要なバックグラウンド処理を止める。

## 2. 主要環境変数

- `PO_EMBEDDING_CACHE_SIZE` : 埋め込みLRUキャッシュサイズ（`0`で無効化）
- `PO_PRELOAD_MODELS` : `1`で起動時モデルプリロード
- `PO_PHILOSOPHER_SEQUENTIAL_THRESHOLD_MS` : 哲学者ごとのEMA遅延が閾値以下なら逐次実行
- `PO_PHILOSOPHER_LATENCY_EMA_ALPHA` : EMA更新係数

## 3. ベンチマーク実行コマンド

### 3.1 キャッシュOFF

```bash
PO_EMBEDDING_CACHE_SIZE=0 pytest -q tests/benchmarks/test_pipeline_perf.py::test_bench_smoke_critical -s
```

### 3.2 キャッシュON

```bash
PO_EMBEDDING_CACHE_SIZE=256 pytest -q tests/benchmarks/test_pipeline_perf.py::test_bench_smoke_critical -s
```

### 3.3 プリロードON（起動コスト評価）

```bash
PO_PRELOAD_MODELS=1 pytest -q tests/benchmarks/test_pipeline_perf.py::test_bench_coldstart_vs_warmup -s -m benchmark
```

### 3.4 適応並列の簡易評価

```bash
PO_PHILOSOPHER_SEQUENTIAL_THRESHOLD_MS=5 pytest -q tests/unit/test_party_machine_timeout_behavior.py -k adaptive -s
```

## 4. 同等性確認（correctness）

```bash
pytest -q tests/test_semantic_delta.py -k cache_on_off_equivalence
pytest -q tests/test_synthesis_engine.py -k cache_toggle
```

主要フィールド（`stance_distribution`, `consensus_claims`, `disagreements`, `open_questions`, `scoreboard`）が一致していることを確認する。

## 5. 目安

- ベンチは「劣化していないか」の早期検知用途。
- 厳密な比較は複数回（最低5回）で中央値を使う。
