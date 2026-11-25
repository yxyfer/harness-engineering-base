import assert from 'node:assert/strict';
import { test } from 'node:test';
import { summarise } from '../.harness/templates/nextjs/files/scripts/bench.mjs';

// Synthetic stream-json lines in the shape Claude Code prints.
const assistant = (id, input, cacheRead, cacheWrite, output) =>
  JSON.stringify({
    type: 'assistant',
    message: {
      id,
      usage: {
        input_tokens: input,
        cache_read_input_tokens: cacheRead,
        cache_creation_input_tokens: cacheWrite,
        output_tokens: output,
      },
    },
  });

test('the benchmark counts steps, start, peak and total input', () => {
  const summary = summarise([
    JSON.stringify({ type: 'system', subtype: 'init' }),
    assistant('m1', 10, 60000, 4000, 100),
    assistant('m1', 10, 60000, 4000, 100), // the same message streamed twice
    JSON.stringify({ type: 'user', message: { content: [] } }),
    assistant('m2', 5, 64000, 6000, 300),
    'not json',
    assistant('m3', 5, 70000, 0, 50),
  ]);
  assert.deepEqual(summary, {
    steps: 3,
    start: 64010,
    peak: 70005,
    input: 64010 + 70005 + 70005,
    output: 450,
  });
});

test('a transcript without assistant usage has no summary', () => {
  assert.equal(summarise(['{"type":"system"}', '']), null);
});
