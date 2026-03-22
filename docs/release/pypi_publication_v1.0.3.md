# PyPI Publication Evidence — po-core-flyingpig v1.0.3

> This file records evidence of the public PyPI publication of `po-core-flyingpig==1.0.3`.
> Evidence is limited to what was actually verified. No fake URLs or transcripts.

- Version: `1.0.3`
- Evidence status: **PyPI publication CONFIRMED via public API (2026-03-22)**
- Auditor: claude/fix-pypi-1.0.3-evidence-1F5kR (automated session)

---

## Publication confirmation

`po-core-flyingpig==1.0.3` is publicly available on PyPI.

Evidence source: PyPI JSON API (`https://pypi.org/pypi/po-core-flyingpig/1.0.3/json`),
queried `2026-03-22` by this session (unauthenticated, public endpoint).

### Confirmed PyPI metadata

| Field | Value |
|-------|-------|
| Package name | `po-core-flyingpig` |
| Version | `1.0.3` |
| PyPI release URL | https://pypi.org/project/po-core-flyingpig/1.0.3/ |
| PyPI project URL | https://pypi.org/project/po-core-flyingpig/ |
| Wheel upload time (UTC) | `2026-03-22T15:10:30` |
| SDist upload time (UTC) | `2026-03-22T15:10:32` |
| Wheel filename | `po_core_flyingpig-1.0.3-py3-none-any.whl` |
| SDist filename | `po_core_flyingpig-1.0.3.tar.gz` |
| Wheel SHA256 | `758d07a8ec04ff09ec0307415218e1b1b806a5c7fec083d1f7c1f49890324155` |
| SDist SHA256 | `c3aa925055ea0bc12f7595cdb590f9634abca6afb449f2c5dc79596c26a8a8d6` |
| Wheel URL | https://files.pythonhosted.org/packages/01/7f/8298c3da7ff4995784a9d847a8766641f8b108776eb21e0a95b432514ad1/po_core_flyingpig-1.0.3-py3-none-any.whl |
| Requires-Python | `>=3.10` |
| Summary | `AI system integrating philosophers as dynamic tensors for responsible meaning generation` |
| Author-email | `Flying Pig Project <flyingpig0229+github@gmail.com>` |

### All published releases on PyPI (as of 2026-03-22)

```
0.2.0b4, 1.0.0, 1.0.1, 1.0.2, 1.0.3
```

`1.0.3` is the latest version.

---

## TestPyPI prerequisite

TestPyPI publication also confirmed for `1.0.3`:
- TestPyPI release URL: https://test.pypi.org/project/po-core-flyingpig/1.0.3/
- Wheel upload time (UTC): `2026-03-22T13:44:50` (published ~1.5 hours before PyPI)

The TestPyPI upload preceded the PyPI upload, consistent with the `publish.yml` workflow
gate (TestPyPI must succeed before PyPI publish is allowed).

---

## GitHub Actions workflow run URL

- Publish workflow page: https://github.com/hiroshitanaka-creator/Po_core/actions/workflows/publish.yml
- Successful `publish-testpypi` run URL: **pending** — GitHub API rate-limited during this session
- Successful `publish-pypi` run URL: **pending** — GitHub API rate-limited during this session
- Triggering ref: **pending** — not retrievable
- Triggering commit SHA: **pending** — not retrievable

Note: the upload timestamps from PyPI/TestPyPI APIs confirm the actual publication occurred.
The workflow run URL(s) are supplementary evidence; their absence does not invalidate publication.

---

## Clean-environment install evidence

`pip install --no-deps po-core-flyingpig==1.0.3` in a clean Python 3.11 venv (2026-03-22):

```
Collecting po-core-flyingpig==1.0.3
  Using cached po_core_flyingpig-1.0.3-py3-none-any.whl.metadata (43 kB)
Using cached po_core_flyingpig-1.0.3-py3-none-any.whl (957 kB)
Installing collected packages: po-core-flyingpig
Successfully installed po-core-flyingpig-1.0.3
```

Full deps install + import + smoke transcript: **pending** (large CUDA/torch deps; install was
initiated but did not complete within this session's time constraints).

---

## Prior publication record

For comparison, the prior version evidence is in `docs/release/pypi_publication_v1.0.2.md`.
This file supersedes that for the `1.0.3` release.
