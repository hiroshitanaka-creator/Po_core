import type { paths } from "./generated/openapi.js";

type ReasonRequest =
  paths["/v1/reason"]["post"]["requestBody"]["content"]["application/json"];
type ReasonResponse =
  paths["/v1/reason"]["post"]["responses"]["200"]["content"]["application/json"];

export interface PoCoreClientOptions {
  baseUrl: string;
  apiKey?: string;
  fetchImpl?: typeof fetch;
}

export class PoCoreClient {
  private readonly baseUrl: string;
  private readonly apiKey?: string;
  private readonly fetchImpl: typeof fetch;

  constructor(options: PoCoreClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.apiKey = options.apiKey;
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  async reason(
    input: string,
    options: {
      philosophers?: string[];
      session_id?: string;
      metadata?: Record<string, unknown>;
    } = {}
  ): Promise<ReasonResponse> {
    const body: ReasonRequest = {
      input,
      ...(options.philosophers !== undefined && { philosophers: options.philosophers }),
      ...(options.session_id !== undefined && { session_id: options.session_id }),
      metadata: options.metadata ?? {},
    };
    const headers: Record<string, string> = { "content-type": "application/json" };

    if (this.apiKey) {
      headers["x-api-key"] = this.apiKey;
    }

    const response = await this.fetchImpl(`${this.baseUrl}/v1/reason`, {
      method: "POST",
      headers,
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`Po_core reason call failed: ${response.status} ${response.statusText}`);
    }

    return (await response.json()) as ReasonResponse;
  }
}

export type { ReasonRequest, ReasonResponse };
