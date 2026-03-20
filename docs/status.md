# Status Snapshot (Release SSOT)

最優先ルール（単一真実）：[docs/厳格固定ルール.md](/docs/厳格固定ルール.md)
最新進捗：このファイル（[docs/status.md](/docs/status.md)）
公開手順（再現可能Runbook）：[docs/operations/publish_playbook.md](/docs/operations/publish_playbook.md)

この文書は release-facing SSOT を固定するためのスナップショットです。会話上の断片的な説明よりも、このファイルと `src/po_core/__init__.py` の記述を優先します。

## Current Release State

- Repository target version: `1.0.2`
- Package version SSOT: `src/po_core/__init__.py` の `__version__`
- Public release evidence in-repo: none yet for `1.0.2`
- External publish status: **pending external publish**
- Maintainer rule: TestPyPI / PyPI での公開を主張してよいのは、対応する workflow URL・index URL・install smoke などの証跡が repo 内へ追加された後だけ

## Release Readiness Facts

- `pyproject.toml` は version を `po_core.__version__` から動的読込する。
- README / QUICKSTART / QUICKSTART_EN / CHANGELOG / REPOSITORY_STRUCTURE / この `docs/status.md` は、`1.0.2` を repository target version として扱う。
- Release workflow (`.github/workflows/publish.yml`) は存在するが、実行済み publish の事実は `1.0.2` についてまだ repo 内に記録されていない。
- `po-core-flyingpig==1.0.2` を index から install する user-facing 手順は、`1.0.2` の公開証跡が無い間は案内しない。source checkout (`pip install -e .`) を優先案内する。

## Current Blockers Before External Publish

1. TestPyPI または PyPI の `1.0.2` 公開証跡が未作成。
2. 公開後 smoke（index install / import / minimum runtime path）の repo 内固定が未実施。
3. trusted publishing / secrets / release run の実行結果が `1.0.2` では未確認。

## Notes

- このファイルは「公開済み」と「公開準備済み」を区別する。
- 既存の publish playbook は運用手順として有効だが、それ自体は公開事実の証拠ではない。
- conservative wording として、証跡不在時は常に **pending external publish** を用いる。
