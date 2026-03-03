from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase25_reproduce.py"
SPEC = spec_from_file_location("phase25_reproduce", MODULE_PATH)
MODULE = module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_build_commands_external():
    commands = MODULE.build_commands("external")
    assert commands == [
        ["pytest", "-q", "tests/test_input_schema.py"],
        ["pytest", "-q", "tests/test_output_schema.py"],
        ["pytest", "-q", "tests/test_golden_e2e.py"],
        ["pytest", "-q", "tests/test_traceability.py"],
    ]


def test_build_commands_full_contains_external_plus_full_pytest():
    commands = MODULE.build_commands("full")
    assert commands[:-1] == MODULE.build_commands("external")
    assert commands[-1] == ["pytest", "-q"]
