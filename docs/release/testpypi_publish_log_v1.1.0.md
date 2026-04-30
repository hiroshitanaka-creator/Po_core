# TestPyPI Publish Record — v1.1.0 (Evidence)

> この文書は **証跡（evidence）** です。実値を記入して template から昇格しました。

- Release target version: `1.1.0`
- Release tag: `v1.1.0` (not yet created — pending PyPI production decision)
- Workflow run: `https://github.com/hiroshitanaka-creator/Po_core/actions/runs/25149181205`
- Evidence recorded at commit: (this commit)
- Workflow run SHA: `c94a390` (`main`)
- Workflow trigger: `workflow_dispatch`, `target=testpypi`
- Workflow result: **Success** (18m 38s)

## workflow run URL

- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL: https://github.com/hiroshitanaka-creator/Po_core/actions/runs/25149181205

## 公開したバージョン

- `1.1.0`
- Artifacts: `po_core_flyingpig-1.1.0-py3-none-any.whl` + `po_core_flyingpig-1.1.0.tar.gz`

## TestPyPI JSON API 確認（公開事実の証跡）

```
GET https://test.pypi.org/pypi/po-core-flyingpig/1.1.0/json
```

```
name: po-core-flyingpig
version: 1.1.0
requires_python: >=3.10

filename: po_core_flyingpig-1.1.0-py3-none-any.whl
upload_time: 2026-04-30T05:51:03
sha256: 0a05e4365246249cd291e009224473160d69ae45a660e6ec53a8cbda98a28359

filename: po_core_flyingpig-1.1.0.tar.gz
upload_time: 2026-04-30T05:51:05
sha256: 33cc8e7b777c7f89bba84d3e797a1d28aa83be5bc668fcad675fcdcbbfec7119
```

TestPyPI index page (`https://test.pypi.org/simple/po-core-flyingpig/`) も `1.1.0` wheel + sdist を返すことを確認済み。

## pip install コマンド (TestPyPI)

```bash
python -m pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple po-core-flyingpig==1.1.0
```

**Result: BLOCKED in this environment**

```
ERROR: HTTP error 403 while getting https://test-files.pythonhosted.org/packages/.../po_core_flyingpig-1.1.0-py3-none-any.whl.metadata
x-deny-reason: host_not_allowed
```

`test-files.pythonhosted.org` への outbound ダウンロードがこの実行環境のネットワークポリシーで遮断されている。TestPyPI の index ページ (`test.pypi.org/simple/`) および JSON API は到達可能だが、ファイル CDN への直接ダウンロードは不可。

## import smoke

TestPyPI からのインストールが blocked のため、本環境では未取得。

代替証跡: RC verification Step 6（`docs/release/release_candidate_verification_v1.1.0.md`）にて、**同一 wheel** (`dist/po_core_flyingpig-1.1.0-py3-none-any.whl`, SHA256 `0a05e4365246249cd291e009224473160d69ae45a660e6ec53a8cbda98a28359`) を clean venv にローカルインストールし、以下を確認済み：

```
python -c "import po_core; print(po_core.__version__)"
→ 1.1.0
```

## run smoke

上記と同様。TestPyPI 経由インストールは blocked。RC verification Step 6 の clean wheel smoke にて確認済み：

```
run_status=ok
cli_name=main
dist_version=1.1.0
```

## release_smoke.py --check-entrypoints (clean venv)

TestPyPI 経由インストールは blocked。RC verification Step 6 の full transcript を参照（`docs/release/release_candidate_verification_v1.1.0.md` Step 6）。

## Promotion checklist

- [x] Successful TestPyPI run URL recorded: `https://github.com/hiroshitanaka-creator/Po_core/actions/runs/25149181205`
- [x] TestPyPI JSON API で `1.1.0` 公開事実（upload_time, sha256）確認済み
- [ ] `pip install` 実成功ログ記入済み — **BLOCKED** (test-files.pythonhosted.org: host_not_allowed)
- [ ] import smoke 実出力記入済み — blocked（代替: RC Step 6 で同一 wheel の clean install 確認済み）
- [ ] run smoke 実出力記入済み — blocked（同上）
- [ ] `release_smoke.py --check-entrypoints` transcript — blocked（代替: RC Step 6 参照）
- [x] `docs/status.md` 更新済み (TestPyPI: 公開確認 2026-04-30)
- [ ] PyPI 本番公開判断へ進む（別途決定）

## Rule: do not fabricate evidence

remote 証跡の捏造禁止。install/smoke 未取得は blocked として記録した。TestPyPI JSON API による公開確認は real evidence。
