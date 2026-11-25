import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

// The plan is the tree of README.md files beside the code (docs/FORMAT.md).
// These checks keep the tree complete, the feature registry sound and the
// always-read documents small. They do not judge what a document says.
const appRoot = fileURLToPath(new URL('../', import.meta.url));
const src = join(appRoot, 'src');

// Rough token budgets (4 characters a token). A document over budget costs
// every session that reads it: move detail down to the README that owns it,
// and history to Git and docs/DECISIONS.md.
const BUDGET = {
  'AGENTS.md': 2500,
  'src/README.md': 2500,
  'docs/ARCHITECTURE.md': 5000,
  area: 2500,
};
const tokens = (text) => Math.ceil(text.length / 4);

const folders = (...path) => {
  const full = join(src, ...path);
  return existsSync(full)
    ? readdirSync(full, { withFileTypes: true })
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)
    : [];
};
const read = (...path) => {
  const file = join(src, ...path);
  assert.ok(existsSync(file), `src/${path.join('/')} is missing`);
  return readFileSync(file, 'utf8');
};
const required = ['## What it does', '## How it works', '## Open work'];
// More than this many "Next" items in one document is a backlog, not a plan.
const MAX_NEXT = 5;

// Every open item starts with its state, so status can be rolled up.
const STATE = /^[-*] \*\*(Next|In progress|Waiting on [^:*]+|To decide)\b/;

function openItems(text) {
  const start = text.indexOf('\n## Open work');
  if (start < 0) return [];
  const rest = text
    .slice(start + 1)
    .split('\n')
    .slice(1);
  const end = rest.findIndex((line) => line.startsWith('## '));
  return rest
    .slice(0, end < 0 ? undefined : end)
    .filter((line) => /^[-*] /.test(line));
}

function checkDocument(name, text, headings) {
  for (const heading of headings)
    assert.ok(text.includes(heading), `${name}: missing "${heading}"`);
  const items = openItems(text);
  const next = items.filter((item) => /^[-*] \*\*Next\b/.test(item)).length;
  assert.ok(
    next <= MAX_NEXT,
    `${name}: ${next} items marked Next; keep at most ${MAX_NEXT} and move the rest to To decide or delete them`,
  );
  for (const item of items)
    assert.match(
      item,
      STATE,
      `${name}: open item needs a state (**Next:**, **In progress:**, **Waiting on …:**, **To decide:**): ${item.slice(0, 80)}`,
    );
  assert.ok(
    tokens(text) <= BUDGET.area,
    `${name}: about ${tokens(text)} tokens, budget ${BUDGET.area}`,
  );
}

test('every feature and part has a document, listed by its parent', () => {
  const index = read('README.md');
  for (const feature of folders('features')) {
    const document = read('features', feature, 'README.md');
    checkDocument(`features/${feature}`, document, [
      ...required,
      'Start with:',
    ]);
    assert.ok(
      index.includes(`(features/${feature}/README.md)`),
      `src/README.md does not list ${feature}`,
    );
    for (const part of folders('features', feature)) {
      if (part === 'internal') continue;
      const file = join(src, 'features', feature, part, 'README.md');
      if (!existsSync(file)) continue; // a small part is a row in "Parts"
      checkDocument(`features/${feature}/${part}`, readFileSync(file, 'utf8'), [
        '## What it does',
        '## How it works',
      ]);
      assert.ok(
        document.includes(`(${part}/README.md)`),
        `features/${feature}/README.md does not list ${part}`,
      );
    }
  }
});

test('every experiment has a document that says how to turn it off', () => {
  const index = read('experimental', 'README.md');
  for (const experiment of folders('experimental')) {
    const document = read('experimental', experiment, 'README.md');
    checkDocument(`experimental/${experiment}`, document, [
      ...required,
      'Start with:',
      '## Turning it off',
    ]);
    assert.match(
      document,
      /Destination:\s+(a\s+feature\s+of\s+its\s+own|part\s+of\s+`[a-z0-9-]+`)/,
      `${experiment}: destination`,
    );
    assert.ok(
      index.includes(`(${experiment}/README.md)`),
      `src/experimental/README.md does not list ${experiment}`,
    );
  }
});

test('the feature registry matches the folders and has no cycle', () => {
  const registry = JSON.parse(read('config', 'features.json'));
  const present = folders('features');
  for (const feature of present)
    assert.ok(feature in registry, `${feature} is not in features.json`);
  for (const [feature, uses] of Object.entries(registry)) {
    assert.ok(present.includes(feature), `${feature} has no folder`);
    for (const used of uses)
      assert.ok(used in registry, `${feature} uses unknown ${used}`);
  }
  const visiting = new Set();
  const done = new Set();
  const visit = (feature, path) => {
    if (done.has(feature)) return;
    assert.ok(
      !visiting.has(feature),
      `cycle: ${[...path, feature].join(' -> ')}`,
    );
    visiting.add(feature);
    for (const used of registry[feature] ?? []) visit(used, [...path, feature]);
    visiting.delete(feature);
    done.add(feature);
  };
  for (const feature of Object.keys(registry)) visit(feature, []);
});

test('the documents every session reads stay within budget', () => {
  for (const [file, budget] of Object.entries(BUDGET)) {
    if (file === 'area' || !existsSync(join(appRoot, file))) continue;
    const size = tokens(readFileSync(join(appRoot, file), 'utf8'));
    assert.ok(
      size <= budget,
      `${file}: about ${size} tokens, budget ${budget}`,
    );
  }
});
