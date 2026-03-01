"""Decision Axis Spec (DAS) model and loader."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


_DEFAULT_SPEC_PATH = Path(__file__).resolve().parent / "specs" / "v1.json"


@dataclass(frozen=True)
class AxisDimension:
    """Single evaluative dimension inside an axis system."""

    dimension_id: str
    title: str
    description: str
    scale_min: float
    scale_max: float
    weight: float

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "AxisDimension":
        return AxisDimension(
            dimension_id=str(data["dimension_id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            scale_min=float(data["scale_min"]),
            scale_max=float(data["scale_max"]),
            weight=float(data["weight"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension_id": self.dimension_id,
            "title": self.title,
            "description": self.description,
            "scale_min": self.scale_min,
            "scale_max": self.scale_max,
            "weight": self.weight,
        }


@dataclass(frozen=True)
class AxisSpec:
    """Versioned definition of evaluative dimensions."""

    spec_version: str
    axis_name: str
    dimensions: tuple[AxisDimension, ...] = field(default_factory=tuple)

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> "AxisSpec":
        dimensions_raw = data.get("dimensions", [])
        dimensions = tuple(
            AxisDimension.from_dict(item)
            for item in dimensions_raw
            if isinstance(item, Mapping)
        )
        spec = AxisSpec(
            spec_version=str(data["spec_version"]),
            axis_name=str(data["axis_name"]),
            dimensions=dimensions,
        )
        spec.validate()
        return spec

    def validate(self) -> None:
        seen_ids: set[str] = set()
        for dim in self.dimensions:
            if not dim.dimension_id:
                raise ValueError("dimension_id must not be empty")
            if dim.dimension_id in seen_ids:
                raise ValueError(f"duplicate dimension_id: {dim.dimension_id}")
            seen_ids.add(dim.dimension_id)
            if dim.weight < 0.0 or dim.weight > 1.0:
                raise ValueError(
                    f"dimension weight must be within [0, 1]: {dim.dimension_id}"
                )
            if dim.scale_max <= dim.scale_min:
                raise ValueError(
                    f"scale_max must be greater than scale_min: {dim.dimension_id}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_version": self.spec_version,
            "axis_name": self.axis_name,
            "dimensions": [dim.to_dict() for dim in self.dimensions],
        }


def load_axis_spec(path: str | None = None) -> AxisSpec:
    """Load Decision Axis Spec from JSON file or built-in default."""

    target_path = Path(path) if path else _DEFAULT_SPEC_PATH
    with target_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, Mapping):
        raise ValueError("axis spec must be a JSON object")
    return AxisSpec.from_dict(data)


__all__ = ["AxisDimension", "AxisSpec", "load_axis_spec"]
