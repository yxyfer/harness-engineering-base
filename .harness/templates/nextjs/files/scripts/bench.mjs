#!/usr/bin/env node
// Measures what fixed tasks cost an agent in this application: steps, the
// context the session starts with, its peak, and the total input sent across
// steps (every step re-sends the conversation). Runs Claude Code headless in
// plan mode, which cannot edit files. Compare runs before and after a change
// to the contract, the READMEs or the context map.
//
//   npm run bench -- [--tasks .harness/bench.json] [--runs 2] [--model <id>]
//
// Needs the `claude` CLI signed in. Results print as a table; with --save they
// are appended to .harness/bench-results.jsonl.
import { spawnSync } from 'node:child_process';
import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { parseArgs } from 'node:util';

/** Summarises a Claude Code stream-json transcript (one JSON object a line). */
export function summarise(lines) {
  const seen = new Set();
  const steps = [];
  for (const line of lines) {
    let event;
    try {
      event = JSON.parse(line);
    } catch {
      continue;
    }
    const message = event.message;
    if (event.type !== 'assistant' || !message?.usage) continue;
    if (message.id && seen.has(message.id)) continue;
    seen.add(message.id);
    const usage = message.usage;
    steps.push({
      context:
        (usage.input_tokens ?? 0) +
        (usage.cache_read_input_tokens ?? 0) +
        (usage.cache_creation_input_tokens ?? 0),
      output: usage.output_tokens ?? 0,
    });
  }
  if (!steps.length) return null;
  const contexts = steps.map((step) => step.context);
  return {
    steps: steps.length,
    start: contexts[0],
    peak: Math.max(...contexts),
    input: contexts.reduce((a, b) => a + b, 0),
    output: steps.reduce((a, step) => a + step.output, 0),
  };
}

const SUFFIX =
  '\n\nThis is a read-only measurement: do not edit files. Answer in under 200 words.';

function runTask(prompt, model) {
  const args = [
    '-p',
    prompt + SUFFIX,
    '--output-format',
    'stream-json',
    '--verbose',
    '--permission-mode',
    'plan',
  ];
  if (model) args.push('--model', model);
  const result = spawnSync('claude', args, {
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
    timeout: 15 * 60 * 1000,
  });
  if (result.error) throw result.error;
  return summarise(result.stdout.split('\n'));
}

const k = (n) => `${Math.round(n / 1000)}k`;

if (import.meta.main) {
  const { values } = parseArgs({
    options: {
      tasks: { type: 'string', default: '.harness/bench.json' },
      runs: { type: 'string', default: '1' },
      model: { type: 'string' },
      save: { type: 'boolean' },
    },
  });
  if (!existsSync(values.tasks)) {
    console.error(`${values.tasks} not found: a JSON list of { id, prompt }.`);
    process.exit(1);
  }
  const tasks = JSON.parse(readFileSync(values.tasks, 'utf8')).filter(
    (task) => !task.prompt.includes('<edit'),
  );
  const date = new Date().toISOString();
  console.log('| Task | Run | Steps | Start | Peak | Total input | Output |');
  console.log('| --- | --- | --- | --- | --- | --- | --- |');
  for (const task of tasks)
    for (let run = 1; run <= Number(values.runs); run += 1) {
      const summary = runTask(task.prompt, values.model);
      if (!summary) {
        console.log(`| ${task.id} | ${run} | failed | | | | |`);
        continue;
      }
      console.log(
        `| ${task.id} | ${run} | ${summary.steps} | ${k(summary.start)} | ${k(summary.peak)} | ${k(summary.input)} | ${k(summary.output)} |`,
      );
      if (values.save)
        appendFileSync(
          '.harness/bench-results.jsonl',
          `${JSON.stringify({ date, task: task.id, run, ...summary })}\n`,
        );
    }
}
