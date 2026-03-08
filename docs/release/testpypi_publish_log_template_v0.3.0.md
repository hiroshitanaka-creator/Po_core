# TestPyPI Publish Record Template for v0.3.0 (Not Evidence)

> この文書は **証跡（evidence）ではなく記録テンプレート** です。  
> 理由: この実行環境では GitHub/TestPyPI への outbound access が `HTTP 403` で遮断され、
> successful workflow run URL や TestPyPI install 成功の実証跡を取得できないため。

- Purpose: TestPyPI publish 記録を残すためのテンプレート（証跡取得可能な環境で実値を記入する）。
- Execution time (UTC): 2026-03-08T04:20:00Z
- Release target tag reference: `v0.3.0`
- Template last updated at commit: `14f9168`

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

## Local source smoke observed in this environment
- Command:
  ```bash
  PYTHONPATH=src python -c "import po_core; print(po_core.__version__)"
  ```
- Observed output:
  ```text
  0.3.0
  ```
- Command:
  ```bash
  PYTHONPATH=src python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
  ```
- Observed output:
  ```text
  ok
  ```
- Note: local environment emitted a sentence-transformers initialization message before the final status output.

## 問題があった場合のメモ
- この環境での実測:
  - TestPyPI install は `ProxyError: Tunnel connection failed: 403 Forbidden` で失敗
  - GitHub/TestPyPI の outbound access が 403 で制限され、remote 証跡の取得不可

## Result summary
- Status: Template only（証跡は未固定）。
- Next action: release 実行権限・ネットワーク到達性がある環境で successful run URL と smoke 実結果を記入し、evidence 文書へ昇格する。
- Future note: `docs/release/templates/` 配下への整理は将来検討（今回は構成変更しない）。

When all checklist items are complete, rename this file to `docs/release/testpypi_publish_log_v0.3.0.md`.

## Promotion to evidence checklist
- [ ] Successful TestPyPI run URL（`https://github.com/.../actions/runs/<id>`）を記入する。
- [ ] `pip install` の実成功ログを記入する。
- [ ] import smoke（`python -c "import po_core; print(po_core.__version__)"`）の実出力を記入する。
- [ ] run smoke（`python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"`）の実出力を記入する。
- [ ] ファイル名を `docs/release/testpypi_publish_log_v0.3.0.md` に変更して evidence として固定する。
- [ ] `docs/status.md` の文言を「template」から「evidence固定」に更新する。
