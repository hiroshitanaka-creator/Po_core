from __future__ import annotations

import json

import pytest

from po_core.axis.spec import load_axis_spec


def test_load_default_axis_spec() -> None:
    spec = load_axis_spec()

    assert spec.spec_version == "1.0.0"
    assert spec.axis_name == "decision_axis"
    assert len(spec.dimensions) >= 1


def test_axis_spec_rejects_duplicate_dimension_id(tmp_path) -> None:
    path = tmp_path / "dup_axis.json"
    path.write_text(
        json.dumps(
            {
                "spec_version": "1.0.0",
                "axis_name": "decision_axis",
                "dimensions": [
                    {
                        "dimension_id": "dup",
                        "title": "A",
                        "description": "",
                        "scale_min": 0,
                        "scale_max": 1,
                        "weight": 0.5,
                    },
                    {
                        "dimension_id": "dup",
                        "title": "B",
                        "description": "",
                        "scale_min": 0,
                        "scale_max": 1,
                        "weight": 0.5,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate dimension_id"):
        load_axis_spec(str(path))


def test_axis_spec_rejects_invalid_weight(tmp_path) -> None:
    path = tmp_path / "weight_axis.json"
    path.write_text(
        json.dumps(
            {
                "spec_version": "1.0.0",
                "axis_name": "decision_axis",
                "dimensions": [
                    {
                        "dimension_id": "risk",
                        "title": "Risk",
                        "description": "",
                        "scale_min": 0,
                        "scale_max": 1,
                        "weight": 1.2,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="weight"):
        load_axis_spec(str(path))


def test_axis_spec_rejects_invalid_scale(tmp_path) -> None:
    path = tmp_path / "scale_axis.json"
    path.write_text(
        json.dumps(
            {
                "spec_version": "1.0.0",
                "axis_name": "decision_axis",
                "dimensions": [
                    {
                        "dimension_id": "risk",
                        "title": "Risk",
                        "description": "",
                        "scale_min": 1,
                        "scale_max": 1,
                        "weight": 0.3,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="scale_max"):
        load_axis_spec(str(path))
