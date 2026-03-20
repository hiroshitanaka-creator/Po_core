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
- Canonical evidence boundary: public docs may say only what the in-repo evidence proves. Today that means **PyPI publication is evidenced**; TestPyPI publication, workflow-run success, and smoke verification remain unevidenced until their exact URLs/transcripts are recorded.
- Next-cycle operator rule: use `docs/release/release_candidate_handoff_v1.0.2.md` as the compact pre-publish checklist, and use the playbook only for the full step-by-step procedure.

## Canonical public wording

- **Roster count:** “Po_core uses **42 integrated runtime personas**.” This is the public roster count because one slot is a compliance sentinel; avoid phrasing that implies 42 simultaneously active human philosophers.
- **Evidence boundary:** “For `1.0.2`, the repository evidences **PyPI publication** only. TestPyPI state, workflow-run success, and clean install/import/smoke success remain outside the evidence boundary until operator artifacts are fixed in-repo.”

## Release Readiness Facts

- `pyproject.toml` は version を `po_core.__version__` から動的読込する。
- README / QUICKSTART / QUICKSTART_EN / CHANGELOG / REPOSITORY_STRUCTURE / この `docs/status.md` は、`1.0.2` を repository target version として扱う。
- Release workflow (`.github/workflows/publish.yml`) は存在し、PyPI version page evidence により `1.0.2` の PyPI publication fact は repo 内へ固定された。
- `po-core-flyingpig==1.0.2` の PyPI install 手順は案内可能になった。
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

- 2026-03-20: Phase 1 release blocker として `black --check src tests` の失敗を解消するため、black 準拠の最小整形を runtime REST/CLI と関連テストへ適用した。
- 2026-03-20: release-facing SSOT として、本 snapshot に Phase 1 実施状況を追記した。

## Next

- `isort --check-only src tests` / `mypy src/po_core/domain/ src/po_core/experiments/ src/po_core/app/ src/po_core/ports/` / release gates の再実行結果を Phase 1 証跡として確認し、追加 blocker があれば切り出す。
- TestPyPI publication state / workflow run URL / clean install-import-runtime smoke transcript は、引き続き evidence boundary 外として operator artifact 固定待ち。
