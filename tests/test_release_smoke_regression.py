from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _load_release_smoke_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "release_smoke.py"
    spec = importlib.util.spec_from_file_location("release_smoke_test_module", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unrelated_distribution_metadata_is_ignored(monkeypatch) -> None:
    module = _load_release_smoke_module()

    imported_init = Path("/workspace/Po_core/src/po_core/__init__.py")
    stale_init = Path("/tmp/site-packages/po_core/__init__.py")
    module.po_core.__file__ = str(imported_init)

    class FakeDistribution:
        def locate_file(self, path: str) -> Path:
            assert path == "po_core/__init__.py"
            return stale_init

    monkeypatch.setattr(module.importlib.metadata, "distribution", lambda name: FakeDistribution())
    version_called = {"count": 0}

    def fake_version(name: str) -> str:
        version_called["count"] += 1
        return "1.0.2"

    monkeypatch.setattr(module.importlib.metadata, "version", fake_version)

    dist_version, note = module._resolve_checked_distribution_version("po-core-flyingpig")

    assert dist_version is None
    assert "ignoring unrelated installed distribution metadata" in note
    assert str(stale_init) in note
    assert str(imported_init) in note
    assert version_called["count"] == 0


def test_matching_distribution_metadata_keeps_version_check_active(monkeypatch) -> None:
    module = _load_release_smoke_module()

    imported_init = Path("/workspace/Po_core/src/po_core/__init__.py")
    module.po_core.__file__ = str(imported_init)

    class FakeDistribution:
        def locate_file(self, path: str) -> Path:
            assert path == "po_core/__init__.py"
            return imported_init

    monkeypatch.setattr(module.importlib.metadata, "distribution", lambda name: FakeDistribution())
    monkeypatch.setattr(
        module.importlib.metadata, "version", lambda name: "1.0.2"
    )
    monkeypatch.setattr(module.po_core, "__version__", "1.0.3")
    monkeypatch.setattr(
        module,
        "build_test_system",
        lambda: SimpleNamespace(
            aggregator=SimpleNamespace(config=SimpleNamespace(source="package:runtime/pareto_table.yaml"))
        ),
    )
    monkeypatch.setattr(module, "run", lambda prompt: {"status": "ok"})
    monkeypatch.setattr(module, "_assert_rest_server_path", lambda: None)
    monkeypatch.setattr(module, "_assert_console_scripts", lambda: None)
    monkeypatch.setattr(module.resources, "files", lambda name: Path("src/po_core/config"))
    monkeypatch.setattr(module.inspect, "getfile", lambda obj: "src/po_core/viewer/__init__.py")
    monkeypatch.setattr(module.cli_main, "name", "main")

    monkeypatch.setattr(module, "ENTRYPOINTS", ())
    monkeypatch.setattr(module.sys, "argv", ["release_smoke.py"])

    try:
        module.main()
    except SystemExit as exc:
        assert str(exc) == "version mismatch: dist=1.0.2 package=1.0.3"
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected version mismatch to remain enforced")
