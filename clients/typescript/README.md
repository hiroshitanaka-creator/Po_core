# Po_core TypeScript SDK

Minimal TypeScript client for the official `POST /v1/reason` contract generated from the repository OpenAPI schema.

- Python package release SSOT remains `src/po_core/__init__.py` (`1.0.2` in this repo snapshot).
- This SDK README describes the same official REST contract used in `QUICKSTART.md` / `QUICKSTART_EN.md`; it does **not** claim separate npm publication evidence.
- If the server keeps the recommended default `PO_SKIP_AUTH=false`, pass a non-empty API key so the client sends `x-api-key`.

## Generate API Types (from OpenAPI)

From repo root:

```bash
PYTHONPATH=src python scripts/export_openapi.py
python scripts/generate_ts_openapi_types.py
```

This updates:

- `docs/openapi/po_core.openapi.json`
- `clients/typescript/src/generated/openapi.ts`

## Build & Test

```bash
cd clients/typescript
npm run build
npm run test
```

## Usage

```ts
import { PoCoreClient } from "@po-core/sdk";

const client = new PoCoreClient({
  baseUrl: "https://your-po-core-api.example.com",
  apiKey: process.env.PO_API_KEY,
});

const result = await client.reason("How should I decide under uncertainty?");
console.log(result.response);
```

## npm Publish Runbook

1. Bump version in `clients/typescript/package.json`.
2. Regenerate OpenAPI + TS types.
3. Validate locally (`npm run build && npm run test`).
4. Create package tarball:
   ```bash
   cd clients/typescript
   npm pack
   ```
5. Publish:
   ```bash
   npm publish --access public
   ```
6. Verify package and tag release notes.

CI workflow: `.github/workflows/typescript-sdk.yml` runs SDK build/test and manual dry-run packaging.
