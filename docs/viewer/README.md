# Po_core Viewer (Console Prototype)

The Po_core Viewer renders saved traces directly in the console so you can inspect tension maps and ethical pressure summaries without a UI.

## Preparing traces

1. Save each trace as JSON under `data/traces/` (or any directory you pass via `--traces-dir`).
2. Filenames should match the trace identifier, e.g. `demo-001.json`.
3. Optionally set `PO_CORE_TRACES_DIR` to override the default location.

### Minimal trace shape

```json
{
  "trace_id": "demo-001",
  "title": "Sample Reasoning Trace",
  "created_at": "2024-06-01T12:00:00Z",
  "tension_map": {
    "autonomy_vs_care": 0.65,
    "law_vs_mercy": 0.45
  },
  "ethical_pressure_summary": {
    "deontological": 0.7,
    "care": 0.5
  },
  "segments": [
    {
      "philosopher": "Kant",
      "stance": "Duty-driven reasoning about the act",
      "ethical_pressure": 0.7,
      "tension": {"law_vs_mercy": 0.4}
    },
    {
      "philosopher": "Gilligan",
      "summary": "Care perspective centering relationships",
      "ethical_pressure": 0.5,
      "tension": {"autonomy_vs_care": 0.6}
    }
  ]
}
```

Values between 0 and 1 render as ASCII bars for quick scanning.

## CLI usage

Render a trace by ID:

```bash
po-core view demo-001
```

Filter segments to a single philosopher:

```bash
po-core view demo-001 --philosopher Kant
```

Load traces from a custom directory:

```bash
po-core view demo-001 --traces-dir /path/to/traces
```

Or set an environment variable:

```bash
export PO_CORE_TRACES_DIR=/path/to/traces
po-core view demo-001
```

## Output example

```
Trace: demo-001
Title: Sample Reasoning Trace
Created: 2024-06-01T12:00:00Z

Tension Map
-----------
autonomy_vs_care         ███████████████░░░░ 0.65
law_vs_mercy             ██████████░░░░░░░░░ 0.45

Ethical Pressure Summary
------------------------
care                     ██████████░░░░░░░░░ 0.50
deontological            ██████████████░░░░░ 0.70

Segments
--------
- Kant: Duty-driven reasoning about the act
  ethical pressure: ██████████████░░░░░ 0.70
  tensions: law_vs_mercy=0.40
- Gilligan: Care perspective centering relationships
  ethical pressure: ██████████░░░░░░░░░ 0.50
  tensions: autonomy_vs_care=0.60
```
