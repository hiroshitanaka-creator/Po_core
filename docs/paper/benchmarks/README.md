# Phase 23: Comparative Benchmark (4-B)

Po_core の独自性を、以下 4 軸で他システムと比較する再現可能ベンチです。

- Diversity（多様性）
- Explainability（説明可能性）
- Safety（安全性）
- Emergence（創発性）

## 実行方法（再現手順）

```bash
python scripts/paper/run_comparative_benchmark.py \
  --repo-root . \
  --output-dir docs/paper/benchmarks/results \
  --created-at 2026-02-22T00:00:00Z
```

## 生成物

- `comparative_results.json`: 生データ（メタ情報 + 軸別スコア）
- `comparative_table.md`: 論文貼り付け用 Markdown 表
- `comparative_table.csv`: 図表作成向け CSV
- `comparative_overall.svg`: Overall スコア棒グラフ

## 決定性

- `--created-at` を固定値で与えるとメタ情報も固定されます。
- Po_core の diversity は実装済み哲学者数（`src/po_core/philosophers/*.py`、`__init__.py`/`manifest.py`除外）から決定論的に算出されます。
- 比較対象ベースラインのプロファイル値はスクリプト内で固定されています。
