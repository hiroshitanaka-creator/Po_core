# Status Snapshot (Release SSOT)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）
公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は release-facing SSOT を固定するためのスナップショットです。release state に関する主張は、このファイル・`src/po_core/__init__.py`・`docs/release/` 配下の証跡ファイルが示す範囲に限定します。

## Current Release State

- Repository target version: `1.0.3`
- Latest published public version: `1.0.2`
- Package version SSOT: `src/po_core/__init__.py` の `__version__`
- Public release evidence in-repo: `docs/release/pypi_publication_v1.0.2.md` fixes PyPI publication evidence for `1.0.2`
- Current release-candidate handoff: `docs/release/release_candidate_handoff_v1.0.3.md`
- Current release-candidate placeholder: `docs/release/smoke_verification_v1.0.3.md` (local smoke PASSED 2026-03-22)
- External publish status: **published on PyPI for `1.0.2`**
- Canonical evidence boundary: the latest published public version can remain `1.0.2` until `1.0.3` is actually published. For `1.0.3` pre-publish candidate state, public docs may say only that the repository is prepared for release and that publication/smoke evidence is still pending.
- Conservative wording rule: do not claim `1.0.3` is already published, do not claim TestPyPI publication, workflow-run success, or post-publish smoke success for `1.0.3` until exact operator evidence is fixed in-repo.

## Canonical public wording

- **Mission truth:** Po_core is a **philosophy-driven AI decision-support system**. It provides structured options, reasons, counterarguments, uncertainty, and additional questions. It is controlled by SolarWill and W_Ethics Gate. It prioritizes ethics, accountability, auditability, and structured reasoning. It is **not** a truth oracle, **not** an emotional-care chatbot, and **not** a final-decision replacement for medical/legal/financial judgment.
- **Roster count:** “Po_core uses **42 philosophers**.” The internal `dummy` slot is a compliance/sentinel helper and must not be counted as one of the 42 in public docs, metadata, tests, or API totals.
- **Evidence boundary:** “For `1.0.2`, the repository evidences **PyPI publication**. For `1.0.3`, the repository currently evidences only a pre-publish candidate state.”

## Release Readiness Facts

- `pyproject.toml` は version を `po_core.__version__` から動的読込する。
- README / QUICKSTART / QUICKSTART_EN / CHANGELOG / REPOSITORY_STRUCTURE / この `docs/status.md` は、`1.0.3` を repository target version として扱う。
- Release workflow (`.github/workflows/publish.yml`) は same-SHA TestPyPI prerequisite を含む strict gate を維持している。
- `docs/release/pypi_publication_v1.0.2.md` により `1.0.2` の public PyPI publication fact は repo 内へ固定されている。
- `docs/release/release_candidate_handoff_v1.0.3.md` と `docs/release/smoke_verification_v1.0.3.md` は `1.0.3` の pre-publish candidate state を示すが、publish success の証跡ではない。
- Public REST defaults remain fail-closed by design: localhost-only CORS, `process` execution mode by default, and explicit refusal of `thread` mode unless a development override is set.
- Package metadata remains `Development Status :: 4 - Beta`; repository evidence does not justify a stronger stability claim.

## Remaining Evidence Gaps Before Stronger 1.0.3 Release Claims

1. TestPyPI publication の有無と URL が `1.0.3` では未固定。
2. PyPI publication page evidence が `1.0.3` では未固定。
3. 公開後 smoke（index install / import / minimum runtime path）の operator transcript が `1.0.3` では未固定。
4. trusted publishing / release run の具体的 workflow URL が `1.0.3` では未記録。

## Notes

- このファイルは「公開済み」と「公開準備済み」を明示的に区別する。
- 既存の publish playbook は運用手順として有効だが、それ自体は公開事実の証拠ではない。
- `1.0.3` の pre-publish readiness tests は、未公開版に対して fake な PyPI/smoke evidence を要求してはならない。一方で、公開済みと主張するなら対応する証跡が必須である。

## Next

- **Operator action:** Create GitHub Release for `v1.0.3` tag (or `workflow_dispatch` with `target=testpypi`) to trigger publish workflow on main branch.
- Record the real TestPyPI publication state and exact URL(s) for `1.0.3` once a maintainer-run publish actually exists — use `docs/release/templates/testpypi_publish_log_template_v1.0.3.md` as the template.
- Record the real PyPI publication evidence for `1.0.3` once the public version page exists — create `docs/release/pypi_publication_v1.0.3.md`.
- Record the actual GitHub Actions workflow run URL(s) used for the successful publish path.
- Record the clean install / import / smoke transcript for `po-core-flyingpig==1.0.3` after publication in `docs/release/smoke_verification_v1.0.3.md` (post-publish section).

## Completed

- 2026-03-22: 全ローカルゲート通過済み — `pytest tests/ -v` 3868/3869 passed, release_readiness 24/24, acceptance 43/43, schema 103/103, import_graph violations=0/cycles=0, bandit High=0, twine check PASSED。local smoke (`scripts/release_smoke.py --check-entrypoints`) 全通過。CHANGELOG の `[Unreleased]` を `[1.0.3]` へ統合。`docs/release/smoke_verification_v1.0.3.md` にローカル smoke 結果を記録。`docs/release/templates/testpypi_publish_log_template_v1.0.3.md` 作成。
- 2026-03-21: release SSOT を `1.0.3` target / `1.0.2` latest published public version に分離し、pre-publish candidate state と post-publish evidence state を明示的に分けた。
- 2026-03-21: release-readiness tests を更新し、`1.0.3` pre-publish candidate state では fake publication evidence を要求せず、公開主張には依然として証跡を必須にした。
- 2026-03-21: prompt SSOT を再整合し、draft prompt docs/template から `defer` を除去して runtime action contract と一致させた。
- 2026-03-21: public truth realignment として、42-philosopher canonical count / dummy helper semantics / `/v1/philosophers` public manifest filtering を docs・metadata・tests・REST router へ同期した.
- 2026-03-21: runtime safety hardening として、REST server の execution mode default を `process` に変更し、unsafe `thread` mode は `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を伴う開発時以外で拒否するようにした。
- 2026-03-21: `scripts/release_smoke.py --check-entrypoints` が、import 済み checkout とは別物の stale site-packages metadata (`po-core-flyingpig==1.0.2`) を checkout 検証時の version mismatch と誤判定しないよう修正した。これは local/main checkout validation に対する false release blocker 修正である。
