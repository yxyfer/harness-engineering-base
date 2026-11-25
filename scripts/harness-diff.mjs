#!/usr/bin/env node
// Read-only: compares an application's copies of kit files with the kit at the
// revision the app recorded and with the kit now, so kit improvements can be
// taken deliberately. It changes nothing.
//
//   npm run harness:diff -- <app-directory>
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { kitFiles, kitRoot } from './kit-files.mjs';

const target = process.argv[2] && resolve(process.argv[2]);
if (!target || !existsSync(join(target, 'package.json'))) {
  console.error('Usage: npm run harness:diff -- <app-directory>');
  process.exit(1);
}
const upstreamFile = join(target, '.harness/UPSTREAM.md');
const upstream = existsSync(upstreamFile)
  ? readFileSync(upstreamFile, 'utf8')
  : '';
const revision = (upstream.match(/kit revision `([0-9a-f]{7,40})`/) ?? [])[1];
const name =
  (upstream.match(/^App name: (.+)$/m) ?? [])[1] ??
  JSON.parse(readFileSync(join(target, 'package.json'), 'utf8')).name;

// Formatting and line wrapping are not differences worth merging.
const same = (a, b) =>
  a !== null && b !== null && a.replace(/\s+/g, ' ') === b.replace(/\s+/g, ' ');

function atRevision(path) {
  if (!revision) return null;
  const result = spawnSync('git', ['show', `${revision}:${path}`], {
    cwd: kitRoot,
    encoding: 'utf8',
  });
  return result.status === 0 ? result.stdout : null;
}

const groups = {
  'Update available (unchanged in the app; safe to copy)': [],
  'Changed in both (merge by hand)': [],
  'New in the kit (not in the app)': [],
  'Changed only in the app (keep)': [],
  Current: [],
};
for (const file of kitFiles()) {
  const render = (text) =>
    text === null || !file.named ? text : text.replaceAll('{{name}}', name);
  const now = render(readFileSync(join(kitRoot, file.kit), 'utf8'));
  const then = render(atRevision(file.kit));
  const appPath = join(target, file.app);
  const app = existsSync(appPath) ? readFileSync(appPath, 'utf8') : null;
  let group;
  if (same(app, now)) group = 'Current';
  else if (app === null) group = 'New in the kit (not in the app)';
  else if (same(then, now)) group = 'Changed only in the app (keep)';
  else if (same(app, then))
    group = 'Update available (unchanged in the app; safe to copy)';
  else group = 'Changed in both (merge by hand)';
  groups[group].push(file.app);
}

console.log(
  `Kit revision recorded by the app: ${revision ?? 'none (.harness/UPSTREAM.md missing)'}`,
);
for (const [group, list] of Object.entries(groups)) {
  if (group === 'Current') {
    console.log(`\n${group}: ${list.length} files`);
    continue;
  }
  if (list.length)
    console.log(`\n${group}:\n${list.map((file) => `  ${file}`).join('\n')}`);
}
if (!revision)
  console.log(
    '\nWithout a recorded revision, kit and app changes cannot be told apart.',
  );
