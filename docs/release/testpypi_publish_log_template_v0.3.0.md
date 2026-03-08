# TestPyPI Publish Record Template for v0.3.0 (Not Evidence)

> この文書は **証跡（evidence）ではなく記録テンプレート** です。  
> 理由: この実行環境では GitHub/TestPyPI への outbound access が `HTTP 403` で遮断され、
> successful workflow run URL や TestPyPI install 成功の実証跡を取得できないため。

- Purpose: TestPyPI publish 記録を残すためのテンプレート（証跡取得可能な環境で実値を記入する）。
- Execution time (UTC): 2026-03-08T04:20:00Z
- Commit/tag reference at template update: `9922d0b` / `v0.3.0`

## workflow run URL
- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL（実値を記入）: `TODO: paste successful /actions/runs/1234567890 URL here`

## 公開したバージョン
- `0.3.0`

## pip install コマンド
- Command:
  ```bash
  python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0
  ```
- Record observed output（成功ログを貼る）:
  ```text
  TODO: paste successful install output
  ```

## import smoke（python -c "import po_core; print(po_core.__version__)"）
- Command:
  ```bash
  python -c "import po_core; print(po_core.__version__)"
  ```
- Record observed output:
  ```text
  TODO: paste observed output (release env expected: 0.3.0)
  ```

## run smoke（python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"）
- Command:
  ```bash
  python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
  ```
- Record observed output:
  ```text
  TODO: paste observed output (release env expected: ok)
  ```

## 問題があった場合のメモ
- この環境での実測:
  - TestPyPI install は `ProxyError: Tunnel connection failed: 403 Forbidden` で失敗
  - local source smoke (`PYTHONPATH=src`) は `0.3.0` / `ok` を確認

## Result summary
- Status: Template only（証跡は未固定）。
- Next action: release 実行権限・ネットワーク到達性がある環境で successful run URL と smoke 実結果を記入し、evidence 文書へ昇格する。
