# Po_trace Audit Logging

Po_trace records the reasoning lifecycle for ensemble and Po_self runs. The schema is deterministic and can be exported to the console or a file for later inspection.

## Trace schema

A Po_trace JSON document contains:

- `prompt`: Original request text.
- `created_at`: UTC timestamp when the trace object was instantiated.
- `level`: Trace detail level (`concise`, `verbose`, `debug`).
- `events`: Chronological events with timestamps and metadata.
- `attributions`: Per-philosopher contribution weights.
- `emissions` (verbose/debug only): Content that was surfaced per channel or philosopher.
- `reasons` (verbose/debug only): Why the content was emitted.
- `rejections` (debug only): Suppressed or rejected content with rationales.

Example (verbose):

```json
{
  "prompt": "What is wisdom?",
  "created_at": "2024-05-01T12:00:00Z",
  "level": "verbose",
  "events": [
    {"event": "ensemble_started", "timestamp": "2024-05-01T12:00:00Z", "metadata": {"philosophers": 3}},
    {"event": "ensemble_completed", "timestamp": "2024-05-01T12:00:01Z", "metadata": {"results_recorded": 3, "status": "ok"}}
  ],
  "attributions": [
    {"philosopher": "aristotle", "weight": 1.0, "note": "Deterministic weighting for demo run."}
  ],
  "emissions": [
    {"philosopher": "aristotle", "channel": "analysis", "content": "Aristotle reflects on 'What is wisdom?'."}
  ],
  "reasons": [
    {"philosopher": "aristotle", "channel": "analysis", "reason": "Weighted perspective 1 with confidence 0.88."}
  ]
}
```

## Using Po_trace programmatically

Use `run_ensemble` or `run_po_self` to generate traced runs:

```python
from po_core.ensemble import run_ensemble
from po_core.po_self import run_po_self

ensemble_result = run_ensemble("What is truth?", trace_level="verbose", trace_output="logs/ensemble.json")
po_self_result = run_po_self("What is truth?", trace_level="debug")
```

Both helpers return a `trace` key containing the JSON-ready log. When `trace_output` is set, the trace is also written to the given path.

## CLI usage

- Inspect the ensemble with trace options:
  ```bash
  po-core prompt "What is truth?" --trace-level verbose --trace-output trace.json
  ```
- Show only the trace for a prompt:
  ```bash
  po-core log "What is truth?" --trace-level debug
  ```
- Preview or inspect a stored trace file:
  ```bash
  python -m po_core.po_trace --trace-level debug --from-file trace.json
  ```
