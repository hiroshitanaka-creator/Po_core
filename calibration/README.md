# Axis Scoring Calibration Workflow

This directory documents a reproducible workflow for training and applying axis scoring calibration parameters.

## 1) Prepare labeled JSONL

Use JSONL (`.jsonl`) where each line is one record with:

- `text` (string): input text to score
- `labels` (object): gold labels per axis (numeric, coerced to `float` and clipped to `[0, 1]`)
- `meta` (object, optional): extra annotation context (ignored by trainer)

Example:

```json
{"text":"今すぐ決断しないと機会を失うかもしれない。","labels":{"choice":0.8,"responsibility":0.6,"urgency":0.9,"ethics":0.5,"social":0.4,"authenticity":0.7},"meta":{"lang":"ja","domain":"career"}}
{"text":"時間をかけて関係者に相談してから決めたい。","labels":{"choice":0.5,"responsibility":0.8,"urgency":0.2,"ethics":0.7,"social":0.9,"authenticity":0.6}}
```

Notes:

- Training requires labels for all axis dimensions defined by the active spec.
- Keep dataset order stable for reproducibility.
- See also: `calibration/dataset_format.md`.

## 2) Train calibration parameters

Run the trainer:

```bash
python scripts/train_axis_scoring_calibration.py \
  --dataset path/to/axis_labels.jsonl \
  --output calibration/params_v1.json \
  --alpha 0.5
```

Optional:

- `--spec path/to/spec.yaml` to load a non-default axis spec.

The output JSON contains:

- `version`
- `feature_order`
- `ridge_alpha`
- `labels` (`bias` + `weights` per axis)
- `backend` (`numpy` or `fallback`)

## 3) Enable calibration at runtime

Set this environment variable to the trained params path:

```bash
export PO_AXIS_SCORING_CALIBRATION_PARAMS=/absolute/path/to/calibration/params_v1.json
```

When not set, default behavior is unchanged (raw axis scoring).

## 4) Evaluate / sanity-check

If you want holdout MAE metrics, use the evaluation script:

```bash
python scripts/eval_axis_scoring_calibration.py \
  --dataset path/to/axis_labels.jsonl \
  --params calibration/params_v1.json \
  --seed 0 \
  --split 0.2
```

Quick sanity check (runtime load path):

```bash
PO_AXIS_SCORING_CALIBRATION_PARAMS=calibration/params_v1.json \
python -c "from po_core.axis.scoring import score_text; print(score_text('テスト入力'))"
```

For deterministic comparisons, keep dataset/spec/seed/split fixed.
