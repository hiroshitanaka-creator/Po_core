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

Full install transcript with deps: **pending** (TestPyPI-specific install not run in this session; deps are large).

Light install (no-deps, from PyPI cached wheel, verifies package integrity):

```
Collecting po-core-flyingpig==1.0.3
  Using cached po_core_flyingpig-1.0.3-py3-none-any.whl.metadata (43 kB)
Using cached po_core_flyingpig-1.0.3-py3-none-any.whl (957 kB)
Installing collected packages: po-core-flyingpig
Successfully installed po-core-flyingpig-1.0.3
```

(`pip install --no-deps po-core-flyingpig==1.0.3` against PyPI, run in clean venv on 2026-03-22 by this session)

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

Transcript with full deps: **pending** (full install still in progress at time of this session).

Note: `--no-deps` install of wheel succeeded; import requires runtime deps (torch, etc.) to be installed.

---

## run smoke

```bash
python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"
```

Transcript: **pending** (same reason as import smoke above).

---

## Promotion checklist

- [x] TestPyPI publication confirmed via public API
- [x] TestPyPI release URL recorded: https://test.pypi.org/project/po-core-flyingpig/1.0.3/
- [x] `pip install --no-deps` wheel install success recorded
- [ ] `pip install` with full deps install transcript — pending
- [ ] import smoke transcript — pending (requires full deps)
- [ ] run smoke transcript — pending (requires full deps)
- [ ] Successful TestPyPI workflow run URL — pending (GitHub API rate limit)
