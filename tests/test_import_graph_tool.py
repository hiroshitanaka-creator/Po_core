from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "import_graph.py"
SPEC = importlib.util.spec_from_file_location("import_graph_tool", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
import_graph = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = import_graph
SPEC.loader.exec_module(import_graph)


def test_canonical_cycle_normalizes_rotations() -> None:
    cycle_a = ["po_core.a", "po_core.b", "po_core.c", "po_core.a"]
    cycle_b = ["po_core.b", "po_core.c", "po_core.a", "po_core.b"]

    assert import_graph._canonical_cycle(cycle_a) == import_graph._canonical_cycle(
        cycle_b
    )


def test_extract_deps_skips_type_checking_imports(tmp_path: Path) -> None:
    module_path = tmp_path / "module.py"
    module_path.write_text(
        "\n".join(
            [
                "from typing import TYPE_CHECKING",
                "",
                "from po_core.domain import Context",
                "",
                "if TYPE_CHECKING:",
                "    from po_core.safety import SafetyMode",
                "",
                "def build(context: Context) -> str:",
                '    return "ok"',
            ]
        ),
        encoding="utf-8",
    )

    deps = import_graph.extract_deps(
        str(module_path), current_module="po_core.fake.module", package="po_core"
    )

    assert deps == {"po_core.domain"}


def test_find_cycles_deduplicates_rotated_cycles() -> None:
    graph = {
        "po_core.a": {"po_core.b"},
        "po_core.b": {"po_core.c"},
        "po_core.c": {"po_core.a"},
    }

    cycles = import_graph.find_cycles(graph)

    assert cycles == [["po_core.a", "po_core.b", "po_core.c", "po_core.a"]]
