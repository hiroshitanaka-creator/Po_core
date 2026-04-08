# ADR-0015: Architecture Invariants — Technical Debt Remediation

**Status:** Accepted  
**Date:** 2026-04-08  
**Author:** Claude Code (refactoring session `claude/refactor-po-core-debt-LvYFS`)

---

## Context

A structured technical-debt audit identified seven root-cause categories across the
production codebase.  This ADR records the decisions made in each phase and the
invariants that future changes must preserve.

---

## Decision

### Invariant 1 — Philosopher Roster Single Source of Truth (Phase 1)

**Problem:** `PhilosopherPartyMachine.available_philosophers`, `OPTIMAL_4_COMBOS`,
`HIGH_TENSION_PAIRS`, and `HARMONIOUS_CLUSTERS` contained hardcoded IDs (`rawls`,
`mill`) absent from the canonical 42-philosopher manifest.

**Decision:** 
- `PhilosopherPartyMachine.available_philosophers` is now derived at `__init__`
  time directly from `manifest.SPECS` (excludes `DUMMY_PHILOSOPHER_ID`).
- `OPTIMAL_4_COMBOS`, `HIGH_TENSION_PAIRS`, `HARMONIOUS_CLUSTERS` are validated
  against the manifest at module-import time via `validate_philosopher_ids()`.
  Any drift raises `ValueError` immediately.
- Removed: `rawls` → replaced by `beauvoir`/`arendt`; `mill` → replaced by `epicurus`.

**Invariant:** All philosopher IDs in research constants and `PhilosopherPartyMachine`
MUST be present in `manifest.SPECS`.  The import-time guard enforces this.

**Tests:** `tests/test_regression_debt.py::TestRosterDrift`

---

### Invariant 2 — Philosopher Loader Contract (Phase 2)

**Problem:** `select_and_load()` docstring said "エラーは無視" and silently dropped
`LoadError` instances.  The `load()` docstring referenced "39人" (stale).

**Decision:**
- Added `LoadReport` dataclass: `loaded: List[str]`, `errors: List[LoadError]`,
  `ok: bool`, `raise_if_errors()`.
- `select_and_load()` now logs a `warning` for any `LoadError` via `logger.warning`.
- Added `select_and_load_with_report()` → `(philosophers, errors)` for callers
  that need the full report.
- `load()` contract is explicit: `enabled=True` failure → `RuntimeError` (fail-fast);
  `enabled=False` failure → `LoadError` collected and returned.

**Invariant:** `select_and_load()` must log warnings for errors; callers requiring
visibility must use `select_and_load_with_report()`.

**Tests:** `tests/test_regression_debt.py::TestPhilosopherLoadingPolicy`

---

### Invariant 3 — Unified API Configuration (Phase 3)

**Problem:** `app/api.py` created `_legacy_api_settings = APISettings()` at module
import time, creating a frozen config object independent of the canonical
`get_api_settings()` singleton.  Auth settings changed after import were not
reflected in the legacy `/generate` endpoint.

**Decision:**
- Removed `_legacy_api_settings`.  The legacy surface now reads `get_api_settings()`
  (the canonical lazy singleton from `app/rest/config.py`) everywhere.
- Both surfaces — legacy `/generate` and canonical `/v1/reason` — share the same
  config source of truth.

**Invariant:** All API surfaces must read settings from `get_api_settings()`.  No
module-level frozen `APISettings()` instances are permitted.

**Tests:** `tests/test_regression_debt.py::TestLegacyApiBehavior`

---

### Invariant 4 — Truthful safety_mode in API Responses (Phase 4)

**Problem:** `ensemble.run_turn()` did not include `safety_mode` in its result dict.
The REST router (`routers/reason.py`) fabricated `safety_mode="NORMAL"` as the
default when the core did not provide it, hiding degraded/blocked states.

**Decision:**
- `run_turn()` and `async_run_turn()` now include `"safety_mode": mode.value` in
  every result dict (including early-exit paths).
- The REST router's fallback changed from `"NORMAL"` to `"UNKNOWN"`.  Fabricating
  safety is always wrong; an explicit `UNKNOWN` is honest.

**Invariant:** `run_turn()` MUST include `safety_mode` in its result.  The REST
layer MUST NOT infer safety from missing data — use `UNKNOWN` as the safe default.

**Tests:** `tests/test_regression_debt.py::TestSafetyModeFabrication`

---

### Invariant 5 — Process Executor Failure Taxonomy (Phase 5)

**Problem:** `_run_one_in_subprocess()` used `except Exception:` on `queue.get()`,
collapsing timeout, child crash, bootstrap failure, and IPC errors into a single
`timed_out=True` with the same error message.

**Decision:**
- Added helper functions: `_child_crash_error(exit_code, timeout_s)`,
  `_bootstrap_failure_error(exit_code)`.
- `_run_one_in_subprocess()` now catches `queue.Empty` specifically, then inspects
  `proc.exitcode` to distinguish:
  - `exitcode != 0 AND elapsed < bootstrap_grace * 3` → bootstrap failure
  - `exitcode != 0 AND elapsed ≥ bootstrap_grace * 3` → child crash
  - `exitcode is None or 0` → hard timeout
  - Any other exception on queue.get() → IPC queue error (logged as warning)
- All crash/bootstrap failures are logged via `logger.warning`.

**Invariant:** Timeout, crash, bootstrap failure, and IPC errors must produce
distinct error strings.  No `except Exception: pass` around process lifecycle.

**Tests:** `tests/test_regression_debt.py::TestProcessExecutorFailureTaxonomy`

---

### Invariant 6 — Observable Failures in Critical Paths (Phase 6a/6b)

**Problem:**
- `InMemoryTracer.emit()` swallowed listener exceptions with `except Exception: pass`.
- `ensemble.py` shadow Pareto path had `except Exception: pass`.
- `ensemble.py` intention-gate ExplanationChain had `except Exception: pass`.

**Decision:**
- `InMemoryTracer.emit()` now calls `logger.warning(...)` with `exc_info=True` on
  listener failure.  The tracer itself still survives; tracing is best-effort.
- Shadow Pareto path logs `logger.warning(...)` with `exc_info=True`.
- IntentionGate ExplanationChain path logs `logger.warning(...)`.

**Invariant:** `except Exception: pass` is BANNED in critical paths.  Suppressed
failures must emit at least a `logger.warning` so they appear in logs.

**Tests:** `tests/test_regression_debt.py::TestListenerFailureObservability`,
`tests/test_regression_debt.py::TestCriticalExceptionSwallowing`

---

### Invariant 7 — Version Metadata Single Source of Truth (Phase 6c)

**Problem:** `output_adapter.py` had hardcoded `_POCORE_VERSION = "1.0.0"` and
`_GENERATOR_VERSION = "1.0.0"` that diverged from `po_core.__version__ = "1.0.3"`.

**Decision:**
- Replaced hardcoded constants with `_get_pocore_version()` and
  `_get_generator_version()` helper functions that call `po_core.__version__`.
- Module-level `_POCORE_VERSION` / `_GENERATOR_VERSION` are now resolved via
  `__getattr__` for backward compatibility.
- The call sites in `adapt_to_schema()` use `_get_pocore_version()` /
  `_get_generator_version()` directly.

**Invariant:** Version metadata in output MUST be derived from `po_core.__version__`.
No hardcoded version strings allowed in `output_adapter.py`.

**Tests:** `tests/test_regression_debt.py::TestOutputMetadataVersion`

---

## Consequences

### Positive
- Roster drift is caught at import time — no silent production mismatch.
- Load failures are always logged; never silently dropped.
- Both API surfaces share one config source — auth/CORS divergence eliminated.
- `safety_mode` in API responses is now truthful.
- Crash vs timeout vs bootstrap failure are distinguishable in logs.
- All suppressed exceptions emit warnings — observable in structured logs.
- Output version metadata tracks the package automatically.

### Negative / Trade-offs
- `PhilosopherPartyMachine.__init__` now imports `manifest.SPECS` on construction
  (negligible startup cost; manifests are in-process data).
- The `_POCORE_VERSION` / `_GENERATOR_VERSION` backward-compat shim uses
  `__getattr__` which is slightly unconventional.

### Deferred
- Full JSON-based philosopher IPC (replacing pickle `philosopher_worker.py`).
- Moving `po_core.database` to optional dependency.
- Async rate limiter via `slowapi` for programmatic callers.
- `AllowlistRegistry.select_and_load()` type alignment with the new
  `select_and_load_with_report()` signature.

---

## Enforcement

All invariants in this ADR are enforced by `tests/test_regression_debt.py`.
This test file is part of the default CI suite and must pass on every PR.
