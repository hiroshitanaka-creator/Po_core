# Status Snapshot (Release SSOT)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）
公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は release-facing SSOT を固定するためのスナップショットです。会話上の断片的な説明よりも、このファイルと `src/po_core/__init__.py` の記述を優先します。

## Current Release State

- Repository target version: `1.0.2`
- Package version SSOT: `src/po_core/__init__.py` の `__version__`
- Public release evidence in-repo: `docs/release/pypi_publication_v1.0.2.md` fixes PyPI publication evidence for `1.0.2`; `docs/release/smoke_verification_v1.0.2.md` records that smoke transcript evidence is still missing
- External publish status: **published on PyPI for `1.0.2`**
- Maintainer rule: public docs may state only the release facts backed by in-repo evidence; do not claim TestPyPI publication, workflow-run success, or smoke verification until those exact URLs/transcripts are recorded

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
