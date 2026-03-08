# TestPyPI Publish Verification Log for v0.3.0 (Environment-Limited)

- Purpose: Record what can be directly verified in this environment for `po-core-flyingpig==0.3.0`, and explicitly separate non-verifiable remote evidence.
- Execution time (UTC): 2026-03-08T03:55:00Z
- Commit/tag reference at verification: `779c6ac` / `v0.3.0`

## workflow run URL
- Workflow page URL: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL: unavailable at authoring time in this environment (GitHub access blocked by proxy with `HTTP 403`).

## 公開したバージョン
- `0.3.0`

## pip install コマンド
- Command:
  ```bash
  python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0
  ```
- Observed result:
  ```text
  ProxyError: Tunnel connection failed: 403 Forbidden
  ERROR: Could not find a version that satisfies the requirement po-core-flyingpig==0.3.0 (from versions: none)
  ERROR: No matching distribution found for po-core-flyingpig==0.3.0
  ```

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
- GitHub/TestPyPI への outbound access が proxy policy で `403 Forbidden` になり、remote publish artifact（successful run URL / TestPyPI index listing）の直接再検証は不可。
- このため本ドキュメントは「remote publish 成功の完全証跡」ではなく、「環境制約付きの検証ログ」として固定する。

## Result summary
- Local source smoke checks: pass (`po_core.__version__ == 0.3.0`, `run('smoke') == ok`).
- Remote TestPyPI install check: blocked by environment policy (`403 Forbidden`).
