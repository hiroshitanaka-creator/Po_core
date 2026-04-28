# Design Note: RT-GAP-004 — `run_case()` API proposal

Status: DRAFT  
Date: 2026-04-28  
Author: session `docs/runtime-acceptance-closure`  
Tracking test: `TestRuntimeCrossScenario::test_run_output_conforms_to_output_schema_v1`
(`xfail(strict=True)` in `tests/acceptance/test_runtime_acceptance.py`)

---

## Problem

`po_core.run(user_input: str)` returns a raw pipeline dict:

```python
{"status": "ok", "request_id": "...", "proposal": {...}, "proposals": [...]}
```

`output_schema_v1.json` requires top-level keys:
`meta`, `case_ref`, `options`, `recommendation`, `ethics`, `responsibility`,
`questions`, `uncertainty`, `trace`.

The gap is bridged today by `output_adapter.adapt_to_schema(result, case)`, which
uses case-level metadata — not pipeline content — to construct most structural fields.
The philosophical reasoning produced by `run_turn` populates only
`options[0].description` in the final schema-compliant output.

RT-GAP-004 is marked `xfail(strict=True)` to document this architectural gap
without blocking the suite.  XPASS signals readiness to remove the marker.

---

## Why not change `po_core.run(user_input: str)`

1. **Stable public contract.** `run(user_input: str)` is the recommended entry
   point documented in `CLAUDE.md` and `src/po_core/app/api.py`.  Changing its
   return shape is a breaking change for any caller that pattern-matches on
   `result["proposal"]` or `result["proposals"]`.

2. **Input type mismatch.** `user_input: str` does not carry the structured case
   fields (`values`, `constraints`, `scenario_profile`, etc.) needed to populate
   `case_ref`, `options`, `ethics`, `questions`, and `uncertainty` natively.
   Shoehorning that into a string-only signature forces callers to serialise their
   case dict to a string — worse ergonomics than a dedicated entry point.

3. **Incremental migration risk.** Changing an established API mid-stream while
   RT-GAP-001–003 fixes are still stabilising increases regression surface.

---

## Proposal: `run_case(case: dict) -> dict`

Add a new public entry point in `src/po_core/app/api.py`:

```python
def run_case(case: dict, *, settings: Optional[Settings] = None) -> dict:
    """
    Run the deliberation pipeline for a structured case dict and return a
    response conforming to output_schema_v1.

    Args:
        case: A case dict with the same structure accepted by StubComposer —
              keys include `title`, `problem`, `values`, `constraints`,
              `scenario_profile`, etc.  See docs/spec/input_schema_v1.json.
        settings: Optional Settings override; falls back to env-based defaults.

    Returns:
        A dict conforming to output_schema_v1.json.
    """
```

### Internal wiring

```
run_case(case)
  ├─ build_user_input(case)          # existing helper in output_adapter
  ├─ from_case_dict(case)            # CaseSignals — already used by run()
  ├─ build_default_system(settings)
  ├─ run_turn(ctx, deps,
  │     case_signals=signals)        # same pipeline, same signals
  └─ adapt_to_schema(result, case)   # existing output_adapter bridge
```

In the first iteration `run_case` is a thin wrapper around the existing
`run()` + `adapt_to_schema()` path, making the bridge **explicit and
co-located** with the new entry point rather than hidden in a separate module.
The philosophical reasoning still populates `options[0].description`; the
remaining `output_schema_v1` fields are assembled from the case dict.

### Async variant

```python
async def async_run_case(case: dict, *, settings: Optional[Settings] = None) -> dict:
    ...
```

Mirrors `async_run` — same pattern, delegates to `async_run_turn`.

---

## Success criteria

1. `run_case(case_dict)` returns a dict that passes `jsonschema.validate(result,
   output_schema_v1_schema)` for all 10 acceptance scenarios.
2. `TestRuntimeCrossScenario::test_run_output_conforms_to_output_schema_v1`
   is updated to call `run_case` instead of `run`, the `xfail` marker is
   removed, and the test passes green.
3. `run(user_input: str)` return shape is **unchanged** — no existing callers
   are broken.
4. `po_core.run_case` is exported from `po_core/__init__.py` so it is part of
   the public API surface.

---

## What this does NOT do

- Does not change `po_core.run()` signature or return shape.
- Does not change `run_turn` internals.
- Does not remove the `output_adapter` module — `run_case` will use it.
- Does not change any existing test that calls `run()`.
- Does not resolve the deeper architectural question of whether `run_turn`
  should eventually produce a schema-compliant output natively.  That question
  is deferred; this note only scopes the minimal surface needed to close
  RT-GAP-004.

---

## Out of scope / future work

- Streaming / SSE variant of `run_case` (can be added once the sync path is stable).
- Richer pipeline-native population of `ethics`, `responsibility`, `questions`
  fields from `run_turn` output rather than from the case dict.  That would
  reduce dependence on `output_adapter` but is a larger change and out of scope
  for RT-GAP-004.
