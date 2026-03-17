"""Generate minimal TypeScript API types from docs/openapi/po_core.openapi.json."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = REPO_ROOT / "docs/openapi/po_core.openapi.json"
OUTPUT_PATH = REPO_ROOT / "clients/typescript/src/generated/openapi.ts"


def _ensure_openapi_file() -> None:
    if OPENAPI_PATH.exists():
        return
    from po_core.app.rest.server import create_app

    schema = create_app().openapi()
    OPENAPI_PATH.parent.mkdir(parents=True, exist_ok=True)
    OPENAPI_PATH.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _resolve_ref(ref: str, openapi: dict) -> dict:
    """Resolve a JSON $ref string like '#/components/schemas/Foo' to its schema."""
    if not ref.startswith("#/"):
        return {}
    parts = ref.lstrip("#/").split("/")
    node = openapi
    for part in parts:
        node = node.get(part, {})
    return node


def _schema_to_ts(schema: dict, openapi: dict, indent: int = 0) -> str:
    """Recursively convert an OpenAPI JSON Schema to a TypeScript type string."""
    pad = "  " * indent
    inner_pad = "  " * (indent + 1)

    # Resolve $ref first
    if "$ref" in schema:
        schema = _resolve_ref(schema["$ref"], openapi)

    t = schema.get("type")
    if "enum" in schema:
        return " | ".join(json.dumps(v) for v in schema["enum"])
    if t == "string":
        return "string"
    if t == "number":
        return "number"
    if t == "integer":
        return "number"
    if t == "boolean":
        return "boolean"
    if t == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            items = _resolve_ref(items["$ref"], openapi)
        return f"{_schema_to_ts(items, openapi, indent)}[]"
    if t == "object" or "properties" in schema:
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        additional = schema.get("additionalProperties")
        if not props and additional is not None:
            # additionalProperties: true / schema → Record<string, ...>
            if isinstance(additional, dict):
                return f"Record<string, {_schema_to_ts(additional, openapi, indent)}>"
            return "Record<string, unknown>"
        if not props:
            return "Record<string, unknown>"
        fields = []
        for name, prop in props.items():
            opt = "" if name in required else "?"
            ts_type = _schema_to_ts(prop, openapi, indent + 1)
            if "\n" in ts_type:
                fields.append(f"{inner_pad}{name}{opt}: {ts_type};")
            else:
                fields.append(f"{inner_pad}{name}{opt}: {ts_type};")
        return "{\n" + "\n".join(fields) + "\n" + pad + "}"
    # anyOf / oneOf / allOf — join with union for simplicity
    for combiner in ("anyOf", "oneOf"):
        if combiner in schema:
            parts = [_schema_to_ts(s, openapi, indent) for s in schema[combiner]]
            return " | ".join(parts)
    if "allOf" in schema:
        merged: dict = {}
        for sub in schema["allOf"]:
            sub = _resolve_ref(sub.get("$ref", ""), openapi) if "$ref" in sub else sub
            merged.setdefault("properties", {}).update(sub.get("properties", {}))
            merged.setdefault("required", []).extend(sub.get("required", []))
        merged["type"] = "object"
        return _schema_to_ts(merged, openapi, indent)
    return "unknown"


def main() -> None:
    _ensure_openapi_file()
    openapi = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    reason = openapi["paths"]["/v1/reason"]["post"]
    req_schema = reason["requestBody"]["content"]["application/json"]["schema"]
    resp_schema = reason["responses"]["200"]["content"]["application/json"]["schema"]

    req_ts = _schema_to_ts(req_schema, openapi, indent=3)
    resp_ts = _schema_to_ts(resp_schema, openapi, indent=3)

    body = f"""// AUTO-GENERATED FROM docs/openapi/po_core.openapi.json - DO NOT EDIT.
export interface paths {{
  \"/v1/reason\": {{
    post: {{
      requestBody: {{
        content: {{
          \"application/json\": {req_ts};
        }};
      }};
      responses: {{
        200: {{
          content: {{
            \"application/json\": {resp_ts};
          }};
        }};
      }};
    }};
  }};
}}

export interface components {{}}
"""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(body, encoding="utf-8")
    print(f"Generated TypeScript API types at {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
