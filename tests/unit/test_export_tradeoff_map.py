from __future__ import annotations

import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "export_tradeoff_map.py"
)
_SPEC = importlib.util.spec_from_file_location("export_tradeoff_map", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def test_render_markdown_contains_axis_vectors_table_header() -> None:
    markdown = _MODULE._render_markdown(
        {
            "meta": {},
            "axis": {
                "scoreboard": {},
                "disagreements": [],
                "axis_vectors": [
                    {
                        "author": "kant",
                        "axis_scores": {
                            "safety": 0.7,
                            "benefit": 0.5,
                            "feasibility": 0.6,
                        },
                        "confidence": 0.8,
                        "policy": "allow",
                    }
                ],
            },
            "influence": {"influence_graph": []},
        }
    )

    assert (
        "| author | safety | benefit | feasibility | confidence | policy |" in markdown
    )
