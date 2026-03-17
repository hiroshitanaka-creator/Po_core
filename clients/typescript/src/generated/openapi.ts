// AUTO-GENERATED FROM docs/openapi/po_core.openapi.json - DO NOT EDIT.
export interface paths {
  "/v1/reason": {
    post: {
      requestBody: {
        content: {
          "application/json": {
            input: string;
            session_id?: string;
            metadata?: Record<string, unknown>;
            philosophers?: string[];
          };
        };
      };
      responses: {
        200: {
          content: {
            "application/json": {
              request_id: string;
              session_id: string;
              status: string;
              response: string;
              philosophers: {
                name: string;
                proposal: string;
                weight: number;
                provider?: string;
                model?: string;
                llm_fallback?: boolean;
                fallback_reason?: string;
              }[];
              tensors: {
                freedom_pressure?: number;
                semantic_delta?: number;
                blocked_tensor?: number;
              };
              safety_mode: string;
              processing_time_ms: number;
              created_at: string;
              degraded: boolean;
              llm_fallback: boolean;
              fallback_reasons: string[];
            };
          };
        };
      };
    };
  };
}

export interface components {}
