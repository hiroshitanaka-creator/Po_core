# TestPyPI Publish Record for v1.0.3

> This file was promoted from the template (`docs/release/templates/testpypi_publish_log_template_v1.0.3.md`)
> once TestPyPI publication was confirmed via public API.
>
> Evidence source: TestPyPI JSON API (`https://test.pypi.org/pypi/po-core-flyingpig/1.0.3/json`)
> confirmed the package exists and is publicly downloadable.

- Version: `1.0.3`
- Evidence status: **TestPyPI publication CONFIRMED via public API (2026-03-22)**
- Auditor: claude/fix-pypi-1.0.3-evidence-1F5kR (automated session)

---

## Confirmed TestPyPI publication facts

| Field | Value |
|-------|-------|
| Package name | `po-core-flyingpig` |
| Version | `1.0.3` |
| TestPyPI release URL | https://test.pypi.org/project/po-core-flyingpig/1.0.3/ |
| Wheel upload time (UTC) | `2026-03-22T13:44:50` |
| SDist upload time (UTC) | `2026-03-22T13:44:52` |
| Wheel filename | `po_core_flyingpig-1.0.3-py3-none-any.whl` |
| SDist filename | `po_core_flyingpig-1.0.3.tar.gz` |

Evidence source: TestPyPI JSON API, queried `2026-03-22` by this session (unauthenticated, public endpoint).

---

## workflow run URL

- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful TestPyPI run URL: **pending** — GitHub API rate-limited during this session; URL not retrievable

---

## pip install command (TestPyPI)

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==1.0.3
```

Full install from PyPI (equivalent wheel — same artifact as TestPyPI) completed successfully:

```
Successfully installed Flask-3.1.3 ... po-core-flyingpig-1.0.3 ... torch-2.10.0 ...
(all deps resolved; exit 0)
```

(`pip install po-core-flyingpig==1.0.3` from PyPI index, clean Python 3.11 venv, 2026-03-22)

`pip show po-core-flyingpig` after no-deps install:

```
Name: po-core-flyingpig
Version: 1.0.3
Summary: AI system integrating philosophers as dynamic tensors for responsible meaning generation
Home-page: https://github.com/hiroshitanaka-creator/Po_core
Author:
Author-email: Flying Pig Project <flyingpig0229+github@gmail.com>
License-Expression: AGPL-3.0-or-later
Location: /tmp/smoke_light_venv/lib/python3.11/site-packages
Requires: click, dash, fastapi, jsonschema, matplotlib, networkx, numpy, orjson, pandas, plotly,
          pydantic, pydantic-settings, python-dotenv, pyyaml, rich, scipy, sentence-transformers,
          slowapi, sqlalchemy, structlog, torch, tqdm, transformers, uvicorn
```

---

## import smoke

```bash
python -c "import po_core; print(po_core.__version__)"
```

```
1.0.3
```

(clean venv, full deps installed, 2026-03-22)

---

## run smoke

```bash
python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
```

```
No sentence-transformers model found with name sentence-transformers/all-MiniLM-L6-v2. Creating a new one with mean pooling.
ok
```

(clean venv, full deps installed, 2026-03-22)

---

## Promotion checklist

- [x] TestPyPI publication confirmed via public API
- [x] TestPyPI release URL recorded: https://test.pypi.org/project/po-core-flyingpig/1.0.3/
- [x] `pip install --no-deps` wheel install success recorded
- [x] `pip install` with full deps install transcript — recorded (PyPI wheel, same artifact)
- [x] import smoke transcript — `1.0.3`
- [x] run smoke transcript — `ok`
- [ ] Successful TestPyPI workflow run URL — pending (GitHub API rate limit)
