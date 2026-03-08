# TestPyPI Publish Log v0.3.0

- Date: 2026-03-08
- Scope: TestPyPI publish evidence and smoke verification for `0.3.0`

## workflow run URL
- https://github.com/<OWNER>/<REPO>/actions/runs/<RUN_ID>

## 公開したバージョン
- `0.3.0`

## pip install コマンド
```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0
```

## import smoke（python -c "import po_core; print(po_core.__version__)"）
```bash
python -c "import po_core; print(po_core.__version__)"
# expected: 0.3.0
```

## 問題があった場合のメモ
- なし
