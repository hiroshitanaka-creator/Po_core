# PyPI Publish Log for v0.3.0

- Recorded at (UTC): 2026-03-08T10:45:00Z
- Target package: `po-core-flyingpig`
- Target version: `0.3.0`

## Workflow run URL
- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Publish run URL (v0.3.0): https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Note: this execution environment cannot resolve GitHub Actions run details due outbound proxy restrictions (`CONNECT tunnel failed, response 403`).

## PyPI page URL
- Project page: https://pypi.org/project/po-core-flyingpig/
- Version page (`0.3.0`): https://pypi.org/project/po-core-flyingpig/0.3.0/

## pip install (post-publish smoke command)
```bash
python -m pip install po-core-flyingpig==0.3.0
```

Observed in this environment:
```text
ERROR: Could not find a version that satisfies the requirement po-core-flyingpig==0.3.0 (from versions: none)
ERROR: No matching distribution found for po-core-flyingpig==0.3.0
```

Note: network egress is restricted in this environment (proxy `403`), so remote PyPI reachability could not be validated here.

## import smoke + `run()` minimal invocation example

```python
import po_core
from po_core import run

print(po_core.__version__)
out = run("smoke")
print(out.get("status"))
```

Executed locally against repository source (`PYTHONPATH=src`) for deterministic smoke:

```bash
PYTHONPATH=src python -c "import po_core; print(po_core.__version__)"
PYTHONPATH=src python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
```

Observed output:
```text
0.3.0
ok
```
