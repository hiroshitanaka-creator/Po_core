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


def _schema_to_ts(schema: dict) -> str:
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
        return f"{_schema_to_ts(schema.get('items', {}))}[]"
    if t == "object":
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        fields = []
        for name, prop in props.items():
            opt = "" if name in required else "?"
            fields.append(f"  {name}{opt}: {_schema_to_ts(prop)};")
        if not fields:
            return "Record<string, unknown>"
        return "{\n" + "\n".join(fields) + "\n}"
    return "unknown"


def main() -> None:
    _ensure_openapi_file()
    openapi = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    reason = openapi["paths"]["/v1/reason"]["post"]
    req_schema = reason["requestBody"]["content"]["application/json"]["schema"]
    resp_schema = reason["responses"]["200"]["content"]["application/json"]["schema"]

    body = f"""// AUTO-GENERATED FROM docs/openapi/po_core.openapi.json - DO NOT EDIT.
export interface paths {{
  \"/v1/reason\": {{
    post: {{
      requestBody: {{
        content: {{
          \"application/json\": {_schema_to_ts(req_schema)};
        }};
      }};
      responses: {{
        200: {{
          content: {{
            \"application/json\": {_schema_to_ts(resp_schema)};
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
