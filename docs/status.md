# Status Snapshot (Release SSOT)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）
公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は release-facing SSOT を固定するためのスナップショットです。release state に関する主張は、このファイル・`src/po_core/__init__.py`・`docs/release/` 配下の証跡ファイルが示す範囲に限定します。

## Current Release State

- Repository target version: `1.0.3`
- Latest published public version: `1.0.3`
- Package version SSOT: `src/po_core/__init__.py` の `__version__`
- Public release evidence in-repo: `docs/release/pypi_publication_v1.0.3.md` fixes PyPI publication evidence for `1.0.3`
- TestPyPI evidence in-repo: `docs/release/testpypi_publish_log_v1.0.3.md`
- Post-publish smoke evidence in-repo: `docs/release/smoke_verification_v1.0.3.md` (post-publish section updated 2026-03-22; full-deps smoke transcript appended 2026-04-28)
- External publish status: **`1.0.3` published on PyPI** — https://pypi.org/project/po-core-flyingpig/1.0.3/
- PyPI upload timestamp: `2026-03-22T15:10:30` UTC (confirmed via PyPI JSON API)
- TestPyPI upload timestamp: `2026-03-22T13:44:50` UTC (confirmed via TestPyPI JSON API)
- Pending evidence: GitHub Actions workflow run URL(s) — not retrievable via available MCP tooling (no `list_workflow_runs` endpoint); PyPI JSON API serves as proof of publication. No other evidence gaps remain.

## Canonical public wording

- **Mission truth:** Po_core is a **philosophy-driven AI decision-support system**. It provides structured options, reasons, counterarguments, uncertainty, and additional questions. It is controlled by SolarWill and W_Ethics Gate. It prioritizes ethics, accountability, auditability, and structured reasoning. It is **not** a truth oracle, **not** an emotional-care chatbot, and **not** a final-decision replacement for medical/legal/financial judgment.
- **Roster count:** “Po_core uses **42 philosophers**.” The internal `dummy` slot is a compliance/sentinel helper and must not be counted as one of the 42 in public docs, metadata, tests, or API totals.
- **Evidence boundary:** “For `1.0.3`, the repository evidences **PyPI and TestPyPI publication** (confirmed via public API 2026-03-22) and **clean install/import/CLI smoke** from a fresh Python 3.11.15 venv (completed 2026-04-28, see `docs/release/smoke_verification_v1.0.3.md`). Workflow run URL(s) are not retrievable via available tooling; PyPI JSON API is the proof of publication.”

## Release Readiness Facts

- `pyproject.toml` は version を `po_core.__version__` から動的読込する。
- README / QUICKSTART / QUICKSTART_EN / CHANGELOG / REPOSITORY_STRUCTURE / この `docs/status.md` は、`1.0.3` を repository target version として扱う。
- Release workflow (`.github/workflows/publish.yml`) は same-SHA TestPyPI prerequisite を含む strict gate を維持している。
- `docs/release/pypi_publication_v1.0.3.md` により `1.0.3` の public PyPI publication fact は repo 内へ固定されている（確認 2026-03-22）。
- `docs/release/testpypi_publish_log_v1.0.3.md` により `1.0.3` の TestPyPI publication fact は repo 内へ固定されている（確認 2026-03-22）。
- `docs/release/smoke_verification_v1.0.3.md` は post-publish evidence state へ更新済み（2026-03-22）。
- `docs/release/release_candidate_handoff_v1.0.3.md` は historical pre-publish context として保持。
- Public REST defaults remain fail-closed by design: localhost-only CORS (browser restriction only; direct HTTP clients bypass CORS), server binds `0.0.0.0` by default (restrict with firewall or set `PO_HOST=127.0.0.1`), `process` execution mode by default, and explicit refusal of `thread` mode unless a development override is set.
- Package metadata remains `Development Status :: 4 - Beta`; repository evidence does not justify a stronger stability claim.

## Runtime Acceptance Status (2026-04-28)

All four runtime gaps from `tests/acceptance/test_runtime_acceptance.py` have been
evaluated on `main @ fb6c672`.  See `docs/completion_matrix.md` for per-test detail.

| Gap | Status | Resolution |
|-----|--------|------------|
| RT-GAP-001 | ✅ RESOLVED | `CaseSignals(values_present=False)` + `_apply_case_signals()` in `ensemble.py` overrides `action_type` to `'clarify'` for empty-values input. |
| RT-GAP-002 | ✅ RESOLVED | `_SCENARIO_ROUTING` in `ensemble.py` routes each `scenario_type` to a different `(preferred_tags, limit_override)` pair; AT-009 → Confucius, AT-010 → Nietzsche — distinct Pareto winners, non-identical `proposal.content`. |
| RT-GAP-003 | ✅ RESOLVED | `CaseSignals(has_constraint_conflict=True)` + `_apply_case_signals()` injects `constraint_conflict=True` into result dict for conflicting-constraints input. |
| RT-GAP-004 | ✅ RESOLVED | `run_case(case: dict)` added to `po_core.app.api` and exported from `po_core`. Wraps `build_user_input` + `from_case_dict` + `run()` + `adapt_to_schema`; returns `output_schema_v1`-compliant dict. xfail removed from test suite. |

**completion_matrix.md totals: 152 pass / 0 fail / 0 not-yet**

## Remaining Evidence Gaps (post-publication)

All evidence gaps are now closed:

1. ~~GitHub Actions workflow run URL(s)~~ — not retrievable via available MCP tooling; PyPI JSON API is proof of publication.
2. ~~Full deps install/import/smoke transcript~~ — completed 2026-04-28 in clean Python 3.11.15 venv; see `docs/release/smoke_verification_v1.0.3.md`.

## Notes

- このファイルは「公開済み」と「公開準備済み」を明示的に区別する。
- 既存の publish playbook は運用手順として有効だが、それ自体は公開事実の証拠ではない。
- `1.0.3` の pre-publish readiness tests は、未公開版に対して fake な PyPI/smoke evidence を要求してはならない。一方で、公開済みと主張するなら対応する証跡が必須である。

## Next

Post-release follow-up:

- Stage 2 planning: v1.1.x feature work, ecosystem expansion (see ROADMAP_FINAL_FORM.md).

## Completed

- 2026-04-30: TENSOR-TR-1 resolved. No production code changes required — TensorComputed payload already carries `metrics` (freedom_pressure, semantic_delta, blocked_tensor, interaction_tensor) and `version`. `TestTensorComputedTrace` (3 tests) added: payload has all 4 required metric keys + version; SafetyModeInferred.freedom_pressure == TensorComputed.metrics["freedom_pressure"] within 1e-9; all metric values are int/float or None. Runtime 52→55, total 149→152. Session: `feat/tensor-tr-1-tensor-computed-trace`.
- 2026-04-30: SEL-TR-1 resolved. `Selection` dataclass extended with `max_risk`, `cost_budget`, `limit` (effective), and `require_tags` (effective) — populated from `SelectionPlan` and the effective values computed in `registry.select()`. `PhilosophersSelected` payload extended with all six rationale keys: `max_risk`, `cost_budget`, `limit_override`, `preferred_tags`, `limit`, `require_tags`. `AllowlistRegistry.select()` and test helpers updated. `TestPhilosopherSelectionRationale` (4 tests) added: case_001 verifies limit_override=None/preferred_tags=None with non-None effective values; AT-009 verifies limit==limit_override==3 and require_tags==preferred_tags; AT-010 same; distinct rosters confirmed. Runtime 48→52, total 145→149. Session: `feat/sel-tr-1-philosopher-selection-trace`.
- 2026-04-30: MODE-TR-2 resolved. `_build_safety_mode_inferred_payload(mode, fp_value, config)` extracted as a pure function from `_run_phase_pre` in `ensemble.py`; inline reason block replaced with a call to the helper. `tests/unit/test_safety_mode_inferred_branches.py` created: 7 tests covering all 4 branches (missing/normal/warn/critical) and 3 boundary/config cases. Tests run in 0.08s (no pipeline). Unit gate added to summary: 7 pass. Total 138→145. Session: `feat/mode-tr-2-safetymode-branch-coverage`.
- 2026-04-29: MODE-TR-1 resolved. `SafetyModeInferred` TraceEvent added to `_run_phase_pre` in `ensemble.py`, emitted immediately after `infer_safety_mode()`. Payload: `mode`, `freedom_pressure` (float or None), `warn_threshold`, `critical_threshold`, `missing_mode`, `source_metric="freedom_pressure"`, `reason` (one of: `"freedom_pressure_missing"` / `"freedom_pressure < warn_threshold"` / `"warn_threshold <= freedom_pressure < critical_threshold"` / `"freedom_pressure >= critical_threshold"`). `TestSafetyModeInferredTrace` (3 tests) added: event present with all 7 keys; mode agrees with `PhilosophersSelected`/`ParetoFrontComputed`/`ParetoWinnerSelected`; reason is numerically consistent with freedom_pressure vs. thresholds. Runtime 45→48, total 135→138. Session: `feat/mode-tr-1-safetymode-inference-trace`.
- 2026-04-29: AGG-TR-4 resolved. `TestActionGateTraceContract` (2 tests) added to `tests/acceptance/test_runtime_acceptance.py`. Normal path: `ParetoWinnerSelected → AggregateCompleted → DecisionEmitted(degraded=False, origin="pareto")` all share the same `proposal_id`; full 3-event chain is now assertion-locked. Override path: `_FakeRejectParetoGate` rejects the Pareto-aggregated candidate (identified by `PARETO_DEBUG` in extra) while allowing per-philosopher prescreening and fallback; asserts `SafetyOverrideApplied(from=winner, to=fallback)` + `DecisionEmitted(degraded=True, candidate=winner, final=fallback, gate.rule_ids present)` + `result.proposal.proposal_id == fallback.proposal_id`. No production code changes required (trace infrastructure was already complete). Runtime 43→45, total 133→135. Session: `feat/agg-tr-4-actiongate-trace`.
- 2026-04-29: AGG-TR-3 resolved. `ParetoWeights` in `domain/pareto_config.py` extended with `emergence: float = 0.0` field; `to_dict()` now includes emergence. `ParetoConfig.defaults()` updated: NORMAL emergence=0.10, WARN=0.05, CRITICAL=0.00. Dead `_weights_for_mode()` function removed from `aggregator/pareto.py`. `pareto_table.py` loader updated to read emergence from YAML (backward-compatible). Packaged `config/runtime/pareto_table.yaml` updated with emergence keys. `TestParetoSafetyModeWeights` (3 tests) added: NORMAL/WARN/CRITICAL weights mutually distinct, CRITICAL safety=max/freedom+emergence=0, ParetoFrontComputed and ParetoWinnerSelected carry matching mode/weights with emergence key present and nonzero in NORMAL mode. `test_packaged_pareto_table_emergence_weights` added to loader test suite. Runtime 40→43, packaging 12→13, total 129→133. Session: `feat/agg-tr-3-safetymode-weights-trace`.
- 2026-04-29: AGG-TR-2 resolved. `weighted_score` added to `winner_payload` in `ParetoAggregator` (`aggregator/pareto.py`). `TestParetoWinnerScoreExplainability` (3 tests): score recomputable from `scores × weights` within 1e-4; all 6 objective keys in winner scores and front rows. Runtime 37→40, total 126→129. Session: `feat/agg-tr-1-pareto-trace-contract`.
- 2026-04-29: AGG-TR-1 resolved. `ParetoWinnerSelected` payload missing `weights` key exposed and fixed in `trace/pareto_events.py`. `TestParetoWinnerTraceContract` (3 tests) added: winner trace matches final result, required payload keys present, `AggregateCompleted` proposal_id agrees. Runtime 34→37, total 123→126. Session: `feat/agg-tr-1-pareto-trace-contract`.
- 2026-04-29: TR-1 resolved. `CaseSignalsApplied` TraceEvent added to `run_turn` and `async_run_turn`. Emitted only when `_apply_case_signals()` makes at least one mutation (`if _changes:`). Payload: `values_present`, `has_constraint_conflict`, `scenario_type`, `action_type_before`, `action_type_after`, `constraint_conflict_added`, `applied_changes`. `_apply_case_signals()` refactored to return `(result, changes)`. `TestCaseSignalsTraceVisibility` (5 tests) added: AT-009/AT-010 positive + AT-001 negative (no event when no mutation). `completion_matrix.md` runtime 29→34, total 118→123. Session: `feat/case-signals-trace`.
- 2026-04-28: RT-GAP-004 resolved. `run_case(case: dict)` + `async_run_case` added to `po_core.app.api`, exported from `po_core.__init__`. Uses `build_user_input` + `from_case_dict` + `run()` + `adapt_to_schema`; returns `output_schema_v1`-compliant dict. `_case_metadata()` matches StubComposer determinism contract (seed is not None → `"2026-03-03T00:00:00Z"`). `TestRunCaseSchemaConformance` (7 tests) added; xfail removed. `docs/status.md` + `docs/completion_matrix.md` updated. Session: `claude/implement-rt-gap-004`.
- 2026-04-28: Runtime acceptance gaps closed on `main`. RT-GAP-001/002/003 resolved via `CaseSignals` + `_SCENARIO_ROUTING` in pipeline layer. RT-GAP-004 documented as `xfail(strict=True)`; design note at `docs/design/rt_gap_004_run_case_proposal.md`. PyPI release evidence closed: clean full-deps install/import/CLI smoke transcript recorded in `docs/release/smoke_verification_v1.0.3.md`. `completion_matrix.md` updated to 110 pass / 0 fail / 0 not-yet. `docs/status.md` updated to reflect closures. Session: `docs/runtime-acceptance-closure`.
- 2026-03-22: `1.0.3` PyPI and TestPyPI publication confirmed via public API. `docs/release/pypi_publication_v1.0.3.md` and `docs/release/testpypi_publish_log_v1.0.3.md` created. `docs/release/smoke_verification_v1.0.3.md` updated to post-publish evidence state. `docs/status.md` updated: Latest published public version → `1.0.3`, External publish status → `1.0.3 published on PyPI`. Session: claude/fix-pypi-1.0.3-evidence-1F5kR.
- 2026-03-22 (post-fix closure): Phase-G audit closure completed. All 3 Phase-F P1 blockers resolved: `publish.yml` now uses `pytest tests/ -v -m "not slow"` (benchmark failures no longer block CI publish), `src/pocore/runner.py` now resolves schemas via `po_core.schemas.resource_path()` (valid in wheel install), `pyproject.toml` license is SPDX inline string. Bandit Medium reduced from 3 to 2 (pickle.loads nosec B301 added). All P2 docs/version findings resolved. Release readiness 24/24, schema/golden 103/103, import_graph violations=0/cycles=0, twine check PASSED. Current publish blocker count: 0. See `audit/phase_g_closure_report.md` and `audit/finding_resolution_matrix.md`.
- 2026-03-22: 全ローカルゲート通過済み — `pytest tests/ -v` 3868/3869 passed (benchmark timing), release_readiness 24/24, acceptance tests pass, schema 103/103, import_graph violations=0/cycles=0, bandit High=0, twine check PASSED。local smoke (`scripts/release_smoke.py --check-entrypoints`) 全通過。CHANGELOG の `[Unreleased]` を `[1.0.3]` へ統合。`docs/release/smoke_verification_v1.0.3.md` にローカル smoke 結果を記録。`docs/release/templates/testpypi_publish_log_template_v1.0.3.md` 作成。
- 2026-03-21: release SSOT を `1.0.3` target / `1.0.2` latest published public version に分離し、pre-publish candidate state と post-publish evidence state を明示的に分けた。
- 2026-03-21: release-readiness tests を更新し、`1.0.3` pre-publish candidate state では fake publication evidence を要求せず、公開主張には依然として証跡を必須にした。
- 2026-03-21: prompt SSOT を再整合し、draft prompt docs/template から `defer` を除去して runtime action contract と一致させた。
- 2026-03-21: public truth realignment として、42-philosopher canonical count / dummy helper semantics / `/v1/philosophers` public manifest filtering を docs・metadata・tests・REST router へ同期した.
- 2026-03-21: runtime safety hardening として、REST server の execution mode default を `process` に変更し、unsafe `thread` mode は `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を伴う開発時以外で拒否するようにした。
- 2026-03-21: `scripts/release_smoke.py --check-entrypoints` が、import 済み checkout とは別物の stale site-packages metadata を checkout 検証時の version mismatch と誤判定しないよう修正した。これは local/main checkout validation に対する false release blocker 修正である。
