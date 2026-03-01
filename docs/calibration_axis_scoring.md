# Axis scoring calibration training

`po_core.axis.scoring.score_text` が返す raw スコア（safety / benefit / feasibility）を、
教師ラベルに近づけるための線形キャリブレーションパラメータを学習する手順です。

## 1. 学習データ（JSONL）

1行1レコードの JSONL を用意します。各レコードは以下を必須にします。

- `text` : 文字列
- `labels` : オブジェクト
  - spec の全 dimension を含む（通常 `safety`, `benefit`, `feasibility`）
  - 値は `0..1` の実数（境界外は学習時に clamp）

サンプルは `calibration/axis_scoring_labels_sample.jsonl` を参照してください。

## 2. 学習コマンド

```bash
python scripts/train_axis_scoring_calibration.py \
  --dataset calibration/axis_scoring_labels_sample.jsonl \
  --output calibration/axis_scoring_params_v1.json \
  --alpha 0.1
```

### オプション

- `--dataset` (required): 学習用 JSONL
- `--output` (default: `calibration/axis_scoring_params_v1.json`): 出力先
- `--alpha` (default: `0.1`): ridge 正則化係数
- `--spec` (optional): axis spec JSON パス（未指定時は `load_axis_spec()` の既定）

## 3. 出力フォーマット

出力 JSON は以下の形式です。

```json
{
  "version": "axis_scoring_calibration_v1",
  "feature_order": ["safety", "benefit", "feasibility"],
  "ridge_alpha": 0.1,
  "labels": {
    "safety": {"bias": 0.0, "weights": [0.0, 0.0, 0.0]},
    "benefit": {"bias": 0.0, "weights": [0.0, 0.0, 0.0]},
    "feasibility": {"bias": 0.0, "weights": [0.0, 0.0, 0.0]}
  },
  "backend": "numpy"
}
```

`feature_order` の順序は axis spec の `dimensions` 順序です。

## 4. 実行時にパラメータを指定する

学習したパラメータを使う場合は、環境変数 `PO_AXIS_SCORING_CALIBRATION_PARAMS` に
JSON ファイルパスを設定してください。

```bash
export PO_AXIS_SCORING_CALIBRATION_PARAMS=calibration/axis_scoring_params_v1.json
```

> 学習スクリプト内部では raw 特徴抽出を安定させるため、
> `score_text()` 実行時にこの環境変数を一時的に無効化して処理します。
