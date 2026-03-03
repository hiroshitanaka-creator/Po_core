import assert from 'node:assert/strict';
import { PoCoreClient } from './dist/client.js';

const fetchCalls = [];
const fetchMock = async (input, init) => {
  fetchCalls.push({ url: String(input), init });
  return new Response(
    JSON.stringify({
      request_id: 'req-1',
      session_id: 'sess-1',
      status: 'approved',
      response: 'Answer',
      philosophers: [],
      tensors: {},
      safety_mode: 'NORMAL',
      processing_time_ms: 1,
      created_at: '2026-02-22T00:00:00Z'
    }),
    { status: 200, headers: { 'content-type': 'application/json' } }
  );
};

const client = new PoCoreClient({
  baseUrl: 'https://api.example.com',
  apiKey: 'secret',
  fetchImpl: fetchMock
});

const result = await client.reason('What is justice?');
assert.equal(result.status, 'approved');
assert.equal(fetchCalls[0]?.url, 'https://api.example.com/v1/reason');
assert.equal(fetchCalls[0]?.init?.headers['x-api-key'], 'secret');
console.log('ok - PoCoreClient.reason');
