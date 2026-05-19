# Release Decision — v1.1.0 PyPI Production Publish

> **Revision history**
> - v1 (2026-05-18): Initial decision — CONDITIONAL_GO, Path A (tag c94a390) recommended.
> - **v2 (2026-05-18, this version)**: Path A downgraded. Python 3.14 likely released by 2026-05-18
>   (release cadence: 3.12→Oct 2023, 3.13→Oct 2024, 3.14→Oct 2025). `requires-python >=3.10`
>   does NOT exclude Python 3.14 installs; classifiers are not install guards. Publishing the
>   `c94a390` wheel (which contains `from importlib.abc import Traversable`, removed in Python 3.14)
>   would cause `ImportError` for Python 3.14 users. Recommended path changed to `1.1.1` patch
>   release from current `main` (`e590752`). Path B (`skip_existing: true` workaround) removed
>   as it does not provide genuine staging evidence.

## Decision

| Field | Value |
|---|---|
| **Decision** | **CONDITIONAL_GO** |
| Decision date | 2026-05-18 (revised same day) |
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

ただし、TestPyPI publish 後に PR #552（golden更新）と PR #553（Traversable import修正）が統合され、
TestPyPI SHA (`c94a390`) と現在 `origin/main` HEAD (`e590752`) に 4 commit の差がある。
`publish.yml` は同一SHA の successful TestPyPI deployment を機械的に必須条件とするため、
`e590752` から直接 PyPI publish を実行するとガードが失敗する。

**v1 からの変更点（重要）:** 初回評価では `c94a390` へのタグ付け（Path A）を推奨していたが、
これは誤りである。Python リリースサイクル（3.12: Oct 2023, 3.13: Oct 2024, 3.14: Oct 2025）から、
Python 3.14 は 2026-05-18 時点で既にリリース済みと考えられる。`requires-python = ">=3.10"` は
Python 3.14 ユーザーによるインストールを排除しない（classifier は install ガードではない）。
`c94a390` wheel には `from importlib.abc import Traversable`（Python 3.14 で削除済み）が含まれており、
Python 3.14 ユーザーが `po_core` を import しようとすると `ImportError` が発生する。

**推奨パス（改訂）:** `1.1.1` へ version bump し、current `main` (`e590752`) から
TestPyPI → PyPI の正規フローを踏むこと。Path A (c94a390 タグ) は「Python 3.14 互換リスクを
明示的に受け入れる場合に限り許容できる fast path」に降格する。

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
| `publish.yml` same-SHA guard (for PyPI from tag @ `c94a390`) | ✅ WOULD PASS | `c94a390` に successful testpypi deployment 存在。ただし c94a390 wheel は Python 3.14 compat buggy |
| Python 3.14 compatibility of `c94a390` wheel | ❌ BROKEN | `importlib.abc.Traversable` removed in Python 3.14; `c94a390` uses old import path → ImportError |
| Python 3.14 compatibility of `e590752` wheel | ✅ FIXED | PR #553 (`bb60897`) が `importlib.resources.abc.Traversable` へ修正済み |
| Trusted Publishing (OIDC) environments | ASSUMED OK | `testpypi`/`pypi` environments 存在前提（要 operator 最終確認） |

---

## Risk Classification

| Risk | Classification | Reason | Required Action |
|---|---|---|---|
| **SHA mismatch**: TestPyPI SHA (`c94a390`) ≠ origin/main HEAD (`e590752`)。`publish.yml` が same-SHA testpypi deployment を機械的に要求 | **BLOCKER** (for direct PyPI publish from main HEAD) | `e590752` から workflow_dispatch target=pypi を実行するとガードが失敗する | Path A または Recommended Path (1.1.1) で解消 |
| **Traversable import (`from importlib.abc import Traversable`) が `c94a390` wheel に残存** | **BLOCKER for Path A** / **NON_BLOCKER for Recommended Path** | Python 3.14 は release cadence (3.12→Oct 2023, 3.13→Oct 2024, 3.14→Oct 2025) から 2026-05-18 時点で既リリースと見なすべき。`requires-python >=3.10` は 3.14 install を排除しない。classifiers は install ガードではない。`c94a390` wheel を PyPI に publish すると Python 3.14 ユーザーの `import po_core` が `ImportError` になる。`e590752` (PR #553) は修正済み | **Recommended Path (1.1.1) では解消**。Path A を選ぶ場合は即座の 1.1.1 hotfix を確約すること |
| **TestPyPI `1.1.0` 再 upload 不可** (`skip_existing: false`) | **BLOCKER** (if attempting TestPyPI re-run for `e590752` as `1.1.0`) | TestPyPI に `1.1.0` が既存。`skip_existing: false` により同一バージョンの再 upload は失敗する | **Recommended Path** では version を `1.1.1` に bump することで回避 |
| **TestPyPI `skip_existing: true` 案の不適切性** | **NON_BLOCKER** (removed as option) | `skip_existing: true` は upload を skip したまま deployment success を記録する。実際の artifact が staging されず same-SHA staging の趣旨を実質的に損なう。推奨しない | 採用しないこと |
| **TestPyPI direct install blocked** (host_not_allowed) | **NON_BLOCKER** | 環境ネットワーク制限。代替証跡 (RC Step 6 same-wheel clean install) が存在。JSON API 確認済み | 本番 PyPI publish 後に clean venv 確認を取得（post-publish） |
| **PyPI production publish 未実施** | **NON_BLOCKER** | 本判定の前提として認識済み | publish 後に smoke 取得・status.md 更新 |
| **Post-publish smoke 未取得** (`smoke_verification_v1.1.0.md` placeholder) | **POST_PUBLISH_REQUIRED** | publish 後の作業。publish を妨げない | PyPI publish 後すみやかに取得し evidence state へ更新 |
| **Python 3.14 互換性（`e590752` wheel）** | **NON_BLOCKER** | PR #553 により `e590752` wheel は `importlib.resources.abc.Traversable` を使用。Python 3.14 でも動作する | Recommended Path (1.1.1 from e590752) で解消済み |
| **Bandit Low B110 annotations 未追加** (`ensemble.py:311`, `tracer.py:237`) | **NON_BLOCKER** | `-ll` CI gate は PASS。`# nosec B110` annotation は next PR 候補 | 次 PR で annotation 追加 |
| **`pocore` shim DeprecationWarning** | **NON_BLOCKER** | 意図的な shim。CLAUDE.md に削除予定として記載済み | 将来 release で削除 |
| **PyPI 同一 version 再 upload 不可** | **NON_BLOCKER** | Recommended Path では `1.1.1` として upload するため問題なし | N/A |
| **Trusted Publishing/OIDC 設定不備の可能性** | **UNKNOWN** | GitHub Environments 設定は operator 側確認が必要 | operator が `testpypi`/`pypi` environments の OIDC 設定を確認 |

---

## Blockers

### Blocking issues

**SHA / artifact 整合の問題** — 以下の2つが組み合わさり、現在の `e590752` から v1.1.0 として直接
PyPI publish することはできない。また `c94a390` を v1.1.0 として publish することも推奨しない。

**条件 1:** `publish.yml` は同一 SHA の successful testpypi deployment を機械的に要求する。
`e590752` には testpypi deployment が存在しない → `e590752` からの PyPI publish はガード失敗。

**条件 2:** `c94a390` wheel は `importlib.abc.Traversable`（Python 3.14 で削除済み）を含む。
Python 3.14 が既リリースである 2026-05 時点で、この wheel を PyPI に公開すると `requires-python >=3.10`
が許容する Python 3.14 ユーザーに `ImportError` を引き起こす。

---

**Recommended Path（推奨）: `1.1.1` patch release from current `main`**

1. `src/po_core/__init__.py` の `__version__` を `"1.1.0"` → `"1.1.1"` に bump する。
2. `CHANGELOG.md` に `## [1.1.1] - <date>` セクションを追加する。
   ```
   ## [1.1.1] - 2026-xx-xx
   ### Fixed
   - fix(schemas): import Traversable from importlib.resources.abc instead of importlib.abc
     to fix ImportError on Python 3.14 (PR #553).
   ```
3. commit & push to `main`。
4. `workflow_dispatch target=testpypi` を current `main` HEAD から実行 → TestPyPI に `1.1.1` を publish。
5. TestPyPI publish 成功を確認（JSON API / workflow run URL）。
6. GitHub Release を `v1.1.1` タグで作成し published にする（または `workflow_dispatch target=pypi`）。
7. `publish.yml` が release/dispatch イベントで起動し、same-SHA testpypi deployment を確認して通過 → PyPI に `1.1.1` を publish。
8. post-publish smoke の実施と `smoke_verification_v1.1.1.md` の作成（または v1.1.0 版を v1.1.1 に移転）。

利点:
- Python 3.14 互換 (`importlib.resources.abc.Traversable`) ✅
- publish.yml same-SHA guard を正規フローで通過 ✅
- TestPyPI に実際の artifact が staging される（genuine staging evidence）✅

---

**Path A（非推奨 — Python 3.14 互換リスクを明示的に受け入れる場合に限り許容）:
`c94a390` へのタグ付けで v1.1.0 を publish**

```bash
git tag v1.1.0 c94a390
git push origin v1.1.0
# → GitHub Release を v1.1.0 タグで作成し published にする
# → publish-guard は c94a390 の testpypi deployment を確認して通過
```

このパスを採用する場合、operator は以下を明示的に確認・合意すること:
- `c94a390` wheel の `importlib.abc.Traversable` により Python 3.14 ユーザーに `ImportError` が発生する
- PyPI publish 直後に `1.1.1` hotfix release を発行し `po_core.__version__` = `"1.1.1"` で修正版を公開する
- PyPI の yank 機能等の対応方針を事前に決めておく

**このパスは「Python 3.14 互換性リスクを意図的に承認した上で速度を優先する」場合にのみ許容する。
推奨しない。**

---

### Non-blocking issues

- Bandit B110 `# nosec` annotation 2箇所未追加 (`ensemble.py:311`, `tracer.py:237`) — CI gate は通過
- `pocore` shim DeprecationWarning — 既知・意図的
- TestPyPI direct install smoke 未取得 — RC Step 6 で代替証跡済み

---

## Required Pre-Publish Actions

以下は **Recommended Path（1.1.1 patch release）** を前提とした手順。Path A を採用する場合は
各ステップを読み替えること（ただし Path A は推奨しない）。

1. **[必須] `src/po_core/__init__.py` の `__version__` を `"1.1.1"` に bump する。**
   - `pyproject.toml` は動的読込のため変更不要。
   - `CHANGELOG.md` に `## [1.1.1] - <date>` セクションを追加し、Traversable fix (PR #553) を記載する。
   - `docs/status.md` の Repository target version を `1.1.1` に更新する。
   - commit & push to `main`。

2. **[必須] `workflow_dispatch target=testpypi` を current `main` HEAD から実行し TestPyPI に `1.1.1` を publish する。**
   - TestPyPI JSON API で `1.1.1` の upload_time と SHA256 を確認する。
   - `docs/release/testpypi_publish_log_v1.1.1.md` を作成し evidence を記録する。

3. **[必須] Trusted Publishing (OIDC) の GitHub Environments 設定確認。**
   - `testpypi` / `pypi` environments が存在し、OIDC が設定済みであることを確認する。

4. **[必須] TestPyPI publish 後、同一 SHA から PyPI publish を実行する。**
   - GitHub Release trigger (推奨) または `workflow_dispatch target=pypi`。
   - `publish-guard` が same-SHA testpypi deployment を確認して通過することを確認する。

5. **[推奨] PyPI publish 実行前に `python -m build && twine check dist/*` を再実行し artifacts を確認する。**

---

## Required Post-Publish Actions

以下は **Recommended Path（1.1.1 publish）** 完了後の手順。

1. **PyPI version page 確認**: `https://pypi.org/project/po-core-flyingpig/1.1.1/` が公開されていることを確認。
2. **clean venv install/import/run smoke の実施と記録**:
   ```bash
   python -m venv /tmp/po-core-1.1.1-smoke
   /tmp/po-core-1.1.1-smoke/bin/pip install po-core-flyingpig==1.1.1
   /tmp/po-core-1.1.1-smoke/bin/python -c "import po_core; print(po_core.__version__)"
   /tmp/po-core-1.1.1-smoke/bin/python scripts/release_smoke.py --check-entrypoints
   # Python 3.14 環境でも import po_core が成功することを確認（可能であれば）
   ```
3. **`docs/release/smoke_verification_v1.1.1.md` を作成し evidence state で記録する。**
   - `smoke_verification_v1.1.0.md` は「TestPyPI only; PyPI publish was superseded by 1.1.1」と
     注記を追記し、placeholder から説明状態に更新する。
4. **`docs/status.md` 更新**:
   - `Repository target version` → `1.1.1`
   - `Latest published public version` → `1.1.1`
   - `External publish status (v1.1.1)` → PyPI confirmed (URL付き)
   - v1.1.0 publish tasks を `Completed`（decision only; superseded by 1.1.1）として記録
5. **GitHub Actions workflow run URL の記録**: `testpypi_publish_log_v1.1.1.md` に TestPyPI + PyPI publish run URL を記録する。

---

## Recommended Publish Route

**Recommended Path: `1.1.1` patch release from current `main` using GitHub Release trigger。**

理由:
- `c94a390` wheel は `importlib.abc.Traversable` を含み Python 3.14 で `ImportError` が発生する。
  Python 3.14 は 2026-05 時点で既リリースと見なすべきであり、`requires-python >=3.10` は
  Python 3.14 ユーザーのインストールを排除しない。この状態のまま PyPI に公開することは適切ではない。
- `e590752` (PR #553 適用済み) は Python 3.14 互換。これを `1.1.1` として publish することで
  ユーザーに正しい artifact が届く。
- `skip_existing: true` workaround は genuine staging evidence を提供せず、採用しない。
- Playbook §4-A「推奨: Release publish トリガ」と一致する（バージョンが 1.1.1 になるだけ）。

実行手順概要:
```
1. __version__ = "1.1.1" に bump、CHANGELOG 更新、commit & push to main
2. workflow_dispatch target=testpypi → TestPyPI に 1.1.1 を publish
3. TestPyPI evidence を docs/release/testpypi_publish_log_v1.1.1.md に記録
4. GitHub Release を v1.1.1 タグで作成し "Publish release"
   → publish-guard が same-SHA testpypi deployment を確認して通過
   → publish-pypi ジョブ成功を確認
5. post-publish smoke 実施・docs 更新
```

---

## Final Recommendation

`Recommendation: Do NOT publish the c94a390 wheel as v1.1.0 to PyPI. Instead, bump to v1.1.1 from current main (e590752, which includes the Python 3.14 Traversable fix), run the full TestPyPI → PyPI pipeline, and publish as 1.1.1.`
