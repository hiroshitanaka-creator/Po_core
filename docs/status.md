# Status Snapshot (Release SSOT)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）
公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は release-facing SSOT を固定するためのスナップショットです。会話上の断片的な説明よりも、このファイルと `src/po_core/__init__.py` の記述を優先します。

## Current Release State

- Repository target version: `1.0.2`
- Package version SSOT: `src/po_core/__init__.py` の `__version__`
- Public release evidence in-repo: `docs/release/pypi_publication_v1.0.2.md` fixes PyPI publication evidence for `1.0.2`; `docs/release/smoke_verification_v1.0.2.md` records that smoke transcript evidence is still missing
- Operator handoff bundle for the next release cycle: `docs/release/release_candidate_handoff_v1.0.2.md`
- External publish status: **published on PyPI for `1.0.2`**
- Canonical evidence boundary: public docs may say only what the in-repo evidence proves. Today that means **PyPI publication is evidenced**; TestPyPI publication, workflow-run success, and post-publish operator smoke verification remain unevidenced until their exact URLs/transcripts are recorded.
- Next-cycle operator rule: use `docs/release/release_candidate_handoff_v1.0.2.md` as the compact pre-publish checklist, and use the playbook only for the full step-by-step procedure.

## Canonical public wording

- **Roster count:** “Po_core uses **42 philosophers**.” The internal `dummy` slot is a compliance/sentinel helper and must not be counted as one of the 42 in public docs, metadata, tests, or API totals.
- **Evidence boundary:** “For `1.0.2`, the repository evidences **PyPI publication** only. TestPyPI state, workflow-run success, and clean install/import/smoke success remain outside the evidence boundary until operator artifacts are fixed in-repo.”

## Release Readiness Facts

- `pyproject.toml` は version を `po_core.__version__` から動的読込する。
- README / QUICKSTART / QUICKSTART_EN / CHANGELOG / REPOSITORY_STRUCTURE / この `docs/status.md` は、`1.0.2` を repository target version として扱う。
- Release workflow (`.github/workflows/publish.yml`) は存在し、PyPI version page evidence により `1.0.2` の PyPI publication fact は repo 内へ固定された。
- `po-core-flyingpig==1.0.2` の PyPI install 手順は案内可能になった。
- Public REST defaults are now fail-closed by design: localhost-only CORS, `process` execution mode by default, and explicit refusal of `thread` mode unless a development override is set.
- Package metadata has been downgraded to `Development Status :: 4 - Beta` because repository evidence does not justify a stronger stability claim.
- ただし TestPyPI state / workflow run URL / clean install-import-runtime smoke transcript は、現時点ではまだ repo 内に固定されていない。

## Remaining Evidence Gaps After PyPI Publication

1. TestPyPI publication の有無が `1.0.2` ではまだ固定されていない。
2. 公開後 smoke（index install / import / minimum runtime path）の operator transcript が repo 内へ未固定。
3. trusted publishing / release run の具体的 workflow URL が `1.0.2` では未記録。

## Notes

- このファイルは「公開済み」と「公開準備済み」を区別する。
- 既存の publish playbook は運用手順として有効だが、それ自体は公開事実の証拠ではない。
- conservative wording rule: publication state は available evidence の範囲だけを言う。今回の `1.0.2` では **PyPI published** までは言えるが、workflow/TestPyPI/smoke success まではまだ言わない。


## Completed

- 2026-03-21: public truth realignment として、42-philosopher canonical count / dummy helper semantics / `/v1/philosophers` public manifest filtering を docs・metadata・tests・REST router へ同期した.
- 2026-03-21: runtime safety hardening として、REST server の execution mode default を `process` に変更し、unsafe `thread` mode は `PO_ALLOW_UNSAFE_THREAD_EXECUTION=true` を伴う開発時以外で拒否するようにした。
- 2026-03-21: prompt SSOT hardening として、runtime persona prompt / parser / docs draft の JSON 契約を `reasoning` / `perspective` / `tension` / `confidence` / `action_type` / `citations` に統一した。
- 2026-03-21: release smoke realism として、`scripts/release_smoke.py` を REST startup/auth/health/reason/stream path まで拡張し、`import po_core` が eager に legacy FastAPI app を引き込まないようにした。
- 2026-03-20: Phase 1 release blocker として `black --check src tests` の失敗を解消するため、black 準拠の最小整形を runtime REST/CLI と関連テストへ適用した。
- 2026-03-20: release-facing SSOT として、本 snapshot に Phase 1 実施状況を追記した。
- 2026-03-20: Phase 3 truth-sync として `examples/README.md` の roster/install wording と `clients/typescript/README.md` の official REST/auth wording を、`1.0.2`・42/39・evidence boundary に合わせて同期した。
- 2026-03-20: Phase 4 tooling cleanup として `tools/import_graph.py` の cycle 正規化を回転不変にし、`tests/test_import_graph_tool.py` で TYPE_CHECKING 除外と cycle 重複除去の回帰テストを追加した。
- 2026-03-20: Phase 5 final sweep として、release gate 再検証を実施し、`black --check src tests` / `isort --check-only src tests` / `pytest tests/test_release_readiness.py -v` / `pytest tests/test_output_schema.py -v` / `pytest tests/test_golden_e2e.py tests/test_input_schema.py -v` / `pytest tests/acceptance/ -v -m acceptance` / `python scripts/update_traceability.py --check` / `python scripts/calc_traceability_coverage.py --min-at 8` / `python scripts/release_smoke.py --check-entrypoints` の通過を確認した。

## Next

- `examples/` と `clients/typescript/` の他ファイルに残る user-facing wording を監査し、official REST contract / auth defaults / 42-philosopher truth から逸脱する説明があれば Phase 3 の残件として切り出す。
- import-guard を CI release gate として維持しつつ、`tools/import_graph.py` の forbidden-rule coverage（特に ports/domain 境界の異常系 fixture）を必要に応じて追加する。
- `isort --check-only src tests` / `mypy src/po_core/domain/ src/po_core/experiments/ src/po_core/app/ src/po_core/ports/` / release gates の再実行結果を Phase 1 証跡として確認し、追加 blocker があれば切り出す。
- build / twine / bandit / editable install / mypy の release gate は、この環境では build backend・security tooling・外部依存解決の制約により完全再実行できなかったため、再現可能な operator 環境で再確認する。
- TestPyPI publication state / workflow run URL / clean install-import-runtime smoke transcript は、引き続き evidence boundary 外として operator artifact 固定待ち。
