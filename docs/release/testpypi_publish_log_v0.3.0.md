# TestPyPI Publish Evidence for v0.3.0

- Purpose: Fix and preserve auditable evidence for the TestPyPI publish and smoke verification of `po-core-flyingpig==0.3.0`.
- Execution time (UTC): 2026-03-08T03:35:00Z
- Commit reference: `v0.3.0` / repo HEAD `08f167c`

## workflow run URL
- https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Note: This execution environment cannot access GitHub Actions run detail pages (`github.com` returns HTTP 403 via proxy), so the exact successful run-id URL cannot be dereferenced here.

## 公開したバージョン
- `0.3.0`

## pip install コマンド
- Command:
  ```bash
  python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0
  ```
- Observed result in this environment:
  - `ProxyError('Tunnel connection failed: 403 Forbidden')`
  - `ERROR: No matching distribution found for po-core-flyingpig==0.3.0`

## import smoke（python -c "import po_core; print(po_core.__version__)"）
- Command:
  ```bash
  PYTHONPATH=src python -c "import po_core; print(po_core.__version__)"
  ```
- Observed output:
  ```text
  0.3.0
  ```

## run smoke（python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"）
- Command:
  ```bash
  PYTHONPATH=src python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
  ```
- Observed output:
  ```text
  No sentence-transformers model found with name sentence-transformers/all-MiniLM-L6-v2. Creating a new one with mean pooling.
  ok
  ```

## 問題があった場合のメモ
- Network egress to GitHub/TestPyPI is blocked by proxy policy in this environment (`403 Forbidden`), therefore remote publish/install evidence cannot be re-fetched directly from here.
- Local source smoke confirms package version string and `run('smoke')` status behavior.

## Result summary
- Local smoke verification: `po_core.__version__ == 0.3.0` and `run('smoke')` returns `ok`.
- Remote TestPyPI install verification from this environment: not reachable due to proxy restrictions.
