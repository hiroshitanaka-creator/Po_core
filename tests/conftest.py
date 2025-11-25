import json
from pathlib import Path

import pytest


@pytest.fixture()
def sample_prompt() -> str:
    return "What does it mean to live authentically?"


@pytest.fixture()
def load_json_output():
    def _loader(result) -> dict:
        return json.loads(result.output.strip())

    return _loader


@pytest.fixture()
def ensemble_snapshot() -> dict:
    return json.loads(Path("tests/fixtures/ensemble_snapshot.json").read_text())
