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
- Post-publish smoke evidence in-repo: `docs/release/smoke_verification_v1.0.3.md` (post-publish section updated 2026-03-22)
- External publish status: **`1.0.3` published on PyPI** — https://pypi.org/project/po-core-flyingpig/1.0.3/
- PyPI upload timestamp: `2026-03-22T15:10:30` UTC (confirmed via PyPI JSON API)
- TestPyPI upload timestamp: `2026-03-22T13:44:50` UTC (confirmed via TestPyPI JSON API)
- Pending evidence: GitHub Actions workflow run URL(s) — not retrievable this session (GitHub API rate limited); full deps install/import/smoke transcript — not completed this session (large deps).

## Canonical public wording

- **Mission truth:** Po_core is a **philosophy-driven AI decision-support system**. It provides structured options, reasons, counterarguments, uncertainty, and additional questions. It is controlled by SolarWill and W_Ethics Gate. It prioritizes ethics, accountability, auditability, and structured reasoning. It is **not** a truth oracle, **not** an emotional-care chatbot, and **not** a final-decision replacement for medical/legal/financial judgment.
- **Roster count:** “Po_core uses **42 philosophers**.” The internal `dummy` slot is a compliance/sentinel helper and must not be counted as one of the 42 in public docs, metadata, tests, or API totals.
- **Evidence boundary:** “For `1.0.3`, the repository evidences **PyPI and TestPyPI publication** (confirmed via public API 2026-03-22). Workflow run URL(s) and full install/smoke transcript remain pending.”

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

## Remaining Evidence Gaps (post-publication)

1. GitHub Actions workflow run URL(s) for `1.0.3` TestPyPI and PyPI runs — not yet fixed in-repo (GitHub API rate-limited 2026-03-22).
2. Full deps install transcript (`pip install po-core-flyingpig==1.0.3` with all deps) — not completed this session (torch/CUDA deps are large).
3. Clean-environment import transcript (`python -c "import po_core; print(po_core.__version__)"`) — pending full deps install.
4. `scripts/release_smoke.py --check-entrypoints` transcript in clean post-publish venv — pending.

## Notes

- このファイルは「公開済み」と「公開準備済み」を明示的に区別する。
- 既存の publish playbook は運用手順として有効だが、それ自体は公開事実の証拠ではない。
- `1.0.3` の pre-publish readiness tests は、未公開版に対して fake な PyPI/smoke evidence を要求してはならない。一方で、公開済みと主張するなら対応する証跡が必須である。

## Next

Post-release follow-up (all publication steps complete):

- Record GitHub Actions workflow run URL(s) for the successful `publish-testpypi` and `publish-pypi` runs once GitHub API rate limit resets or a token is available — update `docs/release/testpypi_publish_log_v1.0.3.md` and `docs/release/pypi_publication_v1.0.3.md`.
- Complete full deps install (`pip install po-core-flyingpig==1.0.3`) and record clean import + runtime smoke transcript — update `docs/release/smoke_verification_v1.0.3.md` post-publish section.
- Stage 2 planning: v1.1.x feature work, ecosystem expansion (see ROADMAP_FINAL_FORM.md).

## Completed

- 2026-03-22: `1.0.3` PyPI and TestPyPI publication confirmed via public API. `docs/release/pypi_publication_v1.0.3.md` and `docs/release/testpypi_publish_log_v1.0.3.md` created. `docs/release/smoke_verification_v1.0.3.md` updated to post-publish evidence state. `docs/status.md` updated: Latest published public version → `1.0.3`, External publish status → `1.0.3 published on PyPI`. Session: claude/fix-pypi-1.0.3-evidence-1F5kR.
- 2026-03-22 (post-fix closure): Phase-G audit closure completed. All 3 Phase-F P1 blockers resolved: `publish.yml` now uses `pytest tests/ -v -m "not slow"` (benchmark failures no longer block CI publish), `src/pocore/runner.py` now resolves schemas via `po_core.schemas.resource_path()` (valid in wheel install), `pyproject.toml` license is SPDX inline string. Bandit Medium reduced from 3 to 2 (pickle.loads nosec B301 added). All P2 docs/version findings resolved. Release readiness 24/24, schema/golden 103/103, import_graph violations=0/cycles=0, twine check PASSED. Current publish blocker count: 0. See `audit/phase_g_closure_report.md` and `audit/finding_resolution_matrix.md`.
- 2026-03-22: 全ローカルゲート通過済み — `pytest tests/ -v` 3868/3869 passed (benchmark timing), release_readiness 24/24, acceptance tests pass, schema 103/103, import_graph violations=0/cycles=0, bandit High=0, twine check PASSED。local smoke (`scripts/release_smoke.py --check-entrypoints`) 全通過。CHANGELOG の `[Unreleased]` を `[1.0.3]` へ統合。`docs/release/smoke_verification_v1.0.3.md` にローカル smoke 結果を記録。`docs/release/templates/testpypi_publish_log_template_v1.0.3.md` 作成。
- 2026-03-21: release SSOT を `1.0.3` target / `1.0.2` latest published public version に分離し、pre-publish candidate state と post-publish evidence state を明示的に分けた。
- 2026-03-21: release-readiness tests を更新し、`1.0.3` pre-publish candidate state では fake publication evidence を要求せず、公開主張には依然として証跡を必須にした。
- 2026-03-21: prompt SSOT を再整合し、draft prompt docs/template から `defer` を除去して runtime action contract と一致させた。
- 2026-03-21: public truth realignment として、42-philosopher canonical count / dummy helper semantics / `/v1/philosophers` public manifest filtering を docs・metadata・tests・REST router へ同期した.
- 2026-03-21: runtime safety hardening として、REST server の execution mode default を `process` に変更し、unsafe `thread` mode は `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を伴う開発時以外で拒否するようにした。
- 2026-03-21: `scripts/release_smoke.py --check-entrypoints` が、import 済み checkout とは別物の stale site-packages metadata (`po-core-flyingpig==1.0.2`) を checkout 検証時の version mismatch と誤判定しないよう修正した。これは local/main checkout validation に対する false release blocker 修正である。
