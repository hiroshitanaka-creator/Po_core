# Release Decision — v1.1.0 PyPI Production Publish

## Decision

| Field | Value |
|---|---|
| **Decision** | **CONDITIONAL_GO** |
| Decision date | 2026-05-18 |
| Repository | hiroshitanaka-creator/Po_core |
| Branch | `claude/evaluate-v1.1.0-publish-nlHtm` (evaluated against `origin/main` @ `e590752`) |
| Commit SHA (evaluation HEAD) | `e5907521b4cceaf94f528a65d4dcd2c4765b7ed9` |
| TestPyPI publish SHA | `c94a390` |
| origin/main HEAD SHA | `e5907521b4cceaf94f528a65d4dcd2c4765b7ed9` |
| Evaluator | Claude Code (release operator/auditor) |

---

## Executive Summary

v1.1.0 のリリース準備は実質的に完了している。RC verification 全6ステップが完了し、TestPyPI publish
も確認済み（2026-04-30, SHA `c94a390`）。CI は `bb60897` (Python 3.11.15) で 3973 passed / 0 fail。
ただし、TestPyPI publish 後に2件の PR（#552: テストgolden更新、#553: Traversable import修正）が
`origin/main` に統合されており、TestPyPI publish SHA (`c94a390`) と現在の `origin/main` HEAD
(`e590752`) に 4 commit の差がある。`publish.yml` は**同一SHA**の successful TestPyPI deployment を
機械的に必須条件とするため、`e590752` から直接 PyPI publish を実行するとガードが失敗する。

operatorは publish 前に「どの SHA から publish するか」を決定する必要がある。
推奨パスは `c94a390` へのタグ付け（TestPyPI guard 通過）。Traversable fix (PR #553) は
Python 3.14 の前方互換修正であり、Python 3.14 は 2026-05-18 時点で未リリースのため非即時 blocker。

---

## Evidence Reviewed

| Evidence | Path / Source | Result | Notes |
|---|---|---|---|
| `docs/厳格固定ルール.md` | in-repo | READ ✅ | ミッション・変更統制確認 |
| `docs/status.md` | in-repo | READ ✅ | 1.1.0 pending, 1.0.3 published, TestPyPI confirmed 2026-04-30 |
| `docs/operations/publish_playbook.md` | in-repo | READ ✅ | same-SHA prerequisite 要件確認 |
| RC handoff | `docs/release/release_candidate_handoff_v1.1.0.md` | READ ✅ | pre-publish checklist: TestPyPI/PyPI未実施を正直に記載 |
| RC verification | `docs/release/release_candidate_verification_v1.1.0.md` | READ ✅ | 全6ステップ PASS; Appendix (2026-05-14 @ bb60897) 追記済み |
| TestPyPI log | `docs/release/testpypi_publish_log_v1.1.0.md` | READ ✅ | JSON API 確認済み (upload 2026-04-30T05:51:03); direct install blocked 正直記載 |
| Smoke verification | `docs/release/smoke_verification_v1.1.0.md` | READ ✅ | placeholder 状態。post-publish evidence として扱う |
| Publish workflow | `.github/workflows/publish.yml` | READ ✅ | same-SHA TestPyPI guard 機械実施確認 |
| Package version SSOT | `src/po_core/__init__.py` | VERIFIED ✅ | `__version__ = "1.1.0"` |
| pyproject.toml | `pyproject.toml` | VERIFIED ✅ | `dynamic = ["version"]` + `version = {attr = "po_core.__version__"}` |
| CHANGELOG | `CHANGELOG.md` | VERIFIED ✅ | `[1.1.0] - 2026-04-30` section 存在; `[Unreleased]` は空 |
| Git SHA delta (TestPyPI → HEAD) | `git log c94a390..HEAD` | VERIFIED | 4 commits; うち1件が production code change (PR #553) |
| `c94a390` reachability | `git merge-base --is-ancestor` | VERIFIED ✅ | `c94a390 IS ancestor of origin/main` |
| PR #553 diff | `git show bb60897` | VERIFIED | `src/po_core/schemas/__init__.py` の Traversable import 変更のみ |
| PR #552 diff | `git show 74bd021` | VERIFIED | `tests/acceptance/scenarios/` golden files のみ（wheel非対象） |

---

## Version Consistency

| Item | Expected | Actual | Status |
|---|---:|---:|---|
| `src/po_core/__init__.py __version__` | `"1.1.0"` | `"1.1.0"` | ✅ PASS |
| `pyproject.toml` dynamic version source | `po_core.__version__` | `{attr = "po_core.__version__"}` | ✅ PASS |
| `pyproject.toml dynamic` field | `["version"]` | `["version"]` | ✅ PASS |
| `CHANGELOG.md` 最新セクション | `[1.1.0]` | `[1.1.0] - 2026-04-30` | ✅ PASS |
| `CHANGELOG.md [Unreleased]` | empty | empty | ✅ PASS |
| `docs/status.md` Repository target | `1.1.0` | `1.1.0` | ✅ PASS |
| `docs/status.md` Latest published | `1.0.3` | `1.0.3 (pending 1.1.0)` | ✅ PASS — 過剰主張なし |
| TestPyPI wheel version (JSON API) | `1.1.0` | `1.1.0` | ✅ PASS |
| TestPyPI SHA `c94a390` の `__version__` | `"1.1.0"` | `"1.1.0"` (git show 確認) | ✅ PASS |

---

## Publish Readiness

| Check | Status | Evidence |
|---|---|---|
| RC verification 全6ステップ | ✅ PASS | `release_candidate_verification_v1.1.0.md` (2026-04-30) + Appendix (2026-05-14) |
| TestPyPI publish confirmed | ✅ PASS | `testpypi_publish_log_v1.1.0.md`; JSON API upload_time `2026-04-30T05:51:03` |
| TestPyPI wheel SHA256 | ✅ CONFIRMED | wheel: `0a05e4365246249cd291e009224473160d69ae45a660e6ec53a8cbda98a28359` |
| CI green (`bb60897`) | ✅ PASS | 3973 passed / 0 fail (pytest -m "not slow", Python 3.11.15) |
| `twine check dist/*` | ✅ PASS | RC verification Step 3; Appendix (2026-05-14) |
| `bandit -ll` (CI gate) | ✅ PASS | Appendix (2026-05-14): No issues at -ll level |
| clean venv wheel smoke | ✅ PASS | RC verification Step 6: dist_version=1.1.0, all entrypoints ok |
| TestPyPI direct install | ⚠️ BLOCKED | host_not_allowed in environment; substitute: RC Step 6 same-wheel clean install |
| `smoke_verification_v1.1.0.md` evidence state | ⚠️ PLACEHOLDER | pre-publish placeholder のみ。POST_PUBLISH_REQUIRED |
| SHA match (TestPyPI → PyPI publish target) | ⚠️ MISMATCH | TestPyPI: `c94a390`; origin/main HEAD: `e590752`（4 commits diff）|
| `publish.yml` same-SHA guard (for PyPI from main HEAD) | ❌ WOULD FAIL | `e590752` に testpypi deployment なし → guard が `target=testpypi first` エラーで停止 |
| `publish.yml` same-SHA guard (for PyPI from tag @ `c94a390`) | ✅ WOULD PASS | `c94a390` に successful testpypi deployment 存在 |
| Trusted Publishing (OIDC) environments | ASSUMED OK | `testpypi`/`pypi` environments 存在前提（要 operator 最終確認） |

---

## Risk Classification

| Risk | Classification | Reason | Required Action |
|---|---|---|---|
| **SHA mismatch**: TestPyPI SHA (`c94a390`) ≠ origin/main HEAD (`e590752`)。`publish.yml` が same-SHA testpypi deployment を機械的に要求 | **BLOCKER** (for publish from main HEAD) | `e590752` から workflow_dispatch target=pypi を実行するとガードが失敗する。Publish する SHA を決定する必要がある | 下記「Required Pre-Publish Actions」のPath A or B を選択・実施 |
| **Traversable import** (`from importlib.abc import Traversable`) が TestPyPI wheel `c94a390` に残存。Python 3.13 で DeprecationWarning、Python 3.14 で ImportError 予定 | **NON_BLOCKER** | Python 3.14 は 2026-05-18 時点未リリース。`pyproject.toml` classifiers は 3.10/3.11/3.12 のみ宣言。Path A (c94a390 タグ) の場合、次の minor/patch リリースで fix | Path A 選択時: 1.1.1 等次 patch で修正 |
| **TestPyPI direct install blocked** (host_not_allowed) | **NON_BLOCKER** | 環境ネットワーク制限。代替証跡 (RC Step 6 same-wheel clean install) が存在。JSON API 確認済み | 本番 PyPI publish 後に clean venv 確認を取得（post-publish） |
| **PyPI production publish 未実施** | **NON_BLOCKER** | 本判定の前提として認識済み | publish 後に smoke 取得・status.md 更新 |
| **Post-publish smoke 未取得** (`smoke_verification_v1.1.0.md` placeholder) | **POST_PUBLISH_REQUIRED** | publish 後の作業。publish を妨げない | PyPI publish 後すみやかに取得し evidence state へ更新 |
| **Python 3.14 full test 未検証** | **NON_BLOCKER** | Python 3.14 未リリース。3.13 proxy 確認済み (PR #553 fix が `c94a390` にないことは別問題) | 将来 3.14 リリース後に patch release で対応 |
| **Bandit Low B110 annotations 未追加** (`ensemble.py:311`, `tracer.py:237`) | **NON_BLOCKER** | `-ll` CI gate は PASS。`# nosec B110` annotation は next PR 候補 | 次 PR で annotation 追加 |
| **`pocore` shim DeprecationWarning** | **NON_BLOCKER** | 意図的な shim。CLAUDE.md に削除予定として記載済み | 将来 release で削除 |
| **PyPI 同一 version 再 upload 不可** | **NON_BLOCKER** | 既知制約。TestPyPI 1.1.0 再 upload は blocked だが PyPI 初回 upload は問題なし | N/A (初回 upload のため) |
| **Trusted Publishing/OIDC 設定不備の可能性** | **UNKNOWN** | GitHub Environments 設定は operator 側確認が必要 | operator が GitHub Actions `testpypi`/`pypi` environments の OIDC 設定を確認 |
| **TestPyPI skip_existing: false** による TestPyPI 再実行不可 | **NON_BLOCKER** (for Path A) / **BLOCKER** (for Path B) | Path A: 再実行不要。Path B: `skip_existing: true` に変更するか version bump が必要 | Path A 選択で回避 |

---

## Blockers

### Blocking issues

**SHA path decision** — 本番 PyPI publish を実行する前に、operator は以下のいずれかを選択・実施すること。

**Path A（推奨）: `c94a390` へのタグ付けで publish**

```bash
# c94a390 は TestPyPI publish SHA であり origin/main の ancestor (confirmed)
git tag v1.1.0 c94a390
git push origin v1.1.0
# → GitHub Release を v1.1.0 タグで作成し published にする
# → publish.yml が release イベントで起動、publish-guard は c94a390 の testpypi deployment を確認して通過
```

リスク: `bb60897` (Traversable fix) が含まれないホイールが公開される。Python 3.14 互換性は次の patch release で解消。

**Path B（代替）: `skip_existing: true` に変更して TestPyPI 再実行**

```
1. publish.yml の skip_existing: false → true に変更 (PR review 必要)
2. workflow_dispatch target=testpypi を origin/main HEAD から実行
   → 1.1.0 はすでに存在するため upload は skip だが deployment は success で記録される
3. workflow_dispatch target=pypi を origin/main HEAD から実行
```

リスク: workflow 変更を PR レビューなしに行わない。

### Non-blocking issues

- Traversable import 旧パス (`importlib.abc.Traversable`) が `c94a390` wheel に残存 — Python 3.14 前方互換のみ影響、次 patch release で fix
- Bandit B110 `# nosec` annotation 2箇所未追加 — CI gate は通過
- `pocore` shim DeprecationWarning — 既知・意図的
- Python 3.14 全テスト未実施 — Python 3.14 未リリース
- TestPyPI direct install smoke 未取得 — RC Step 6 で代替証跡済み

---

## Required Pre-Publish Actions

1. **[必須] SHA path を決定する**: Path A (tag `c94a390`) または Path B (workflow 変更 + 再 TestPyPI) のいずれかを選択し実施する。Path A を強く推奨。
2. **[必須 / Path A の場合] `v1.1.0` タグを `c94a390` に付与し push する**: `git tag v1.1.0 c94a390 && git push origin v1.1.0`
3. **[必須] Trusted Publishing (OIDC) の GitHub Environments 設定確認**: `testpypi` / `pypi` environments が存在し、TestPyPI/PyPI 側 Trusted Publisher が GitHub OIDC で設定済みであることを operator が最終確認する。
4. **[推奨] publish workflow が `c94a390` の testpypi deployment を検索できることを手動確認**: GitHub Actions deployments API または GitHub UI で `testpypi` environment に `c94a390` の successful deployment が存在することを確認する。
5. **[推奨] 本番 PyPI publish 直前に `twine check dist/*` を再実行**: 現在の dist/ ディレクトリが最新の build artifacts であることを確認する（RC verification では確認済みだが、build artifacts が変わっていないことを念のため確認）。

---

## Required Post-Publish Actions

1. **PyPI version page 確認**: `https://pypi.org/project/po-core-flyingpig/1.1.0/` が公開されていることを確認。
2. **clean venv install/import/run smoke の実施と記録**:
   ```bash
   python -m venv /tmp/po-core-1.1.0-smoke
   /tmp/po-core-1.1.0-smoke/bin/pip install po-core-flyingpig==1.1.0
   /tmp/po-core-1.1.0-smoke/bin/python -c "import po_core; print(po_core.__version__)"
   /tmp/po-core-1.1.0-smoke/bin/python scripts/release_smoke.py --check-entrypoints
   ```
3. **`docs/release/smoke_verification_v1.1.0.md` を evidence state に更新**: placeholder から実際の smoke transcript・workflow URL・PyPI URL を記入する。
4. **`docs/status.md` 更新**:
   - `Latest published public version` → `1.1.0`
   - `External publish status (v1.1.0)` → PyPI confirmed (URL付き)
   - `Next` セクションから v1.1.0 publish tasks を `Completed` へ移動
5. **GitHub Actions workflow run URL の記録**: `testpypi_publish_log_v1.1.0.md` および `smoke_verification_v1.1.0.md` に PyPI publish run URL を追記する。

---

## Recommended Publish Route

**GitHub Release trigger (Path A)** を推奨する。

理由:
- TestPyPI publish SHA (`c94a390`) へのタグ付けにより、`publish.yml` の same-SHA testpypi deployment guard が確実に通過する。
- `workflow_dispatch target=pypi` は `c94a390` 以外の SHA から実行すると guard が失敗するため、Release trigger（タグから起動）が最も安全で再現可能。
- Playbook §4-A「推奨: Release publish トリガ」と一致する。

実行手順:
```
1. git tag v1.1.0 c94a390
2. git push origin v1.1.0
3. GitHub UI で Release を v1.1.0 タグから作成し "Publish release"
4. publish.yml が release イベントで自動起動
5. publish-guard → verify-release-blockers → publish-pypi のジョブ成功を確認
```

---

## Final Recommendation

`Recommendation: Proceed to PyPI production publish after tagging c94a390 as v1.1.0 and confirming OIDC environments. Use the GitHub Release trigger route (Path A).`
