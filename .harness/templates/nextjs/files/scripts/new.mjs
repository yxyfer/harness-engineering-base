#!/usr/bin/env node
// Creates a feature, a part of a feature, or an experiment in the layered
// source tree, with its entry point, README and registrations. It refuses to
// overwrite anything. Run from the application root:
//
//   npm run new-feature -- <name> [--uses a,b]
//   npm run new-feature -- <name> --part-of <feature>
//   npm run new-experiment -- <name> --destination feature|part:<feature>
//                                    [--server] [--billed] [--owner <who>]
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { parseArgs } from 'node:util';

const NAME = /^[a-z][a-z0-9]*(-[a-z0-9]+)*$/;
const root = process.cwd();

function fail(message) {
  console.error(message);
  process.exit(1);
}
const path = (...parts) => join(root, ...parts);
const read = (...parts) => readFileSync(path(...parts), 'utf8');
const title = (name) =>
  name.replace(/-/g, ' ').replace(/^./, (letter) => letter.toUpperCase());

function create(file, content) {
  if (existsSync(path(file))) fail(`${file} already exists; nothing changed.`);
  mkdirSync(path(file, '..'), { recursive: true });
  writeFileSync(path(file), content);
  console.log(`created ${file}`);
}

function stub(name, values) {
  return read('.harness/stubs', `${name}.md`).replace(
    /\{\{(\w+)\}\}/g,
    (_, key) => values[key] ?? '',
  );
}

/** Inserts a line before a marker comment, or reports where to add it. */
function insertBefore(file, marker, line) {
  const text = read(file);
  const at = text.indexOf(marker);
  if (at < 0) {
    console.warn(
      `${file} has no "${marker}" marker; add this yourself:\n${line}`,
    );
    return;
  }
  const before = text.slice(0, at).replace(/\n*$/, '\n');
  writeFileSync(path(file), `${before}${line}\n\n${text.slice(at)}`);
  console.log(`updated ${file}`);
}

const INDEX =
  '// The public entry point. Export only what other areas may use.\nexport {};\n';

function newFeature(name, options) {
  const registryFile = 'src/config/features.json';
  const registry = JSON.parse(read(registryFile));
  if (options['part-of']) {
    const feature = options['part-of'];
    if (!(feature in registry)) fail(`Unknown feature "${feature}".`);
    const folder = `src/features/${feature}/${name}`;
    create(`${folder}/index.ts`, INDEX);
    create(
      `${folder}/README.md`,
      stub('part', { title: title(name), feature }),
    );
    insertBefore(
      `src/features/${feature}/README.md`,
      '<!-- parts:end -->',
      `| [${name}](${name}/README.md) | TODO | \`${name}/\` |`,
    );
    return;
  }
  const uses = (options.uses ?? '')
    .split(',')
    .map((used) => used.trim())
    .filter(Boolean);
  for (const used of uses)
    if (!(used in registry)) fail(`Unknown feature "${used}" in --uses.`);
  if (name in registry) fail(`${name} is already in ${registryFile}.`);
  const folder = `src/features/${name}`;
  create(`${folder}/index.ts`, INDEX);
  create(
    `${folder}/README.md`,
    stub('feature', {
      title: title(name),
      uses: uses.length
        ? uses.map((used) => `\`${used}\``).join(', ')
        : 'nothing',
    }),
  );
  registry[name] = uses;
  writeFileSync(path(registryFile), `${JSON.stringify(registry, null, 2)}\n`);
  console.log(`updated ${registryFile}`);
  insertBefore(
    'src/README.md',
    '<!-- features:end -->',
    `| [${name}](features/${name}/README.md) | TODO | ${uses.join(', ') || 'nothing'} |`,
  );
}

function newExperiment(name, options) {
  const destination = options.destination ?? '';
  let destinationText;
  if (destination === 'feature') destinationText = 'a feature of its own';
  else if (/^part:[a-z0-9-]+$/.test(destination))
    destinationText = `part of \`${destination.slice(5)}\``;
  else fail('--destination must be "feature" or "part:<feature>".');

  const registryFile = 'src/config/experiments.ts';
  if (read(registryFile).includes(`id: '${name}'`))
    fail(`${name} is already registered; never reuse an experiment ID.`);
  const folder = `src/experimental/${name}`;
  create(`${folder}/index.ts`, INDEX);
  if (options.server)
    create(
      `${folder}/server.ts`,
      "import 'server-only';\n\n// Server entry point for routes and Server Actions.\nexport {};\n",
    );
  create(
    `${folder}/README.md`,
    stub('experiment', { title: title(name), destination: destinationText }),
  );
  const entry = [
    '  {',
    `    id: '${name}',`,
    `    name: '${title(name)}',`,
    "    description: 'TODO: what changes when this is on.',",
    `    source: '${folder}',`,
    `    owner: '${(options.owner ?? 'owner').replace(/'/g, '')}',`,
    "    stage: 'testers',",
    ...(options.billed ? ['    billed: true,'] : []),
    '  },',
  ].join('\n');
  const text = read(registryFile);
  const marker = '  // new experiments above this line';
  if (!text.includes(marker)) fail(`${registryFile} has no marker comment.`);
  writeFileSync(
    path(registryFile),
    text.replace(marker, `${entry}\n${marker}`),
  );
  console.log(`updated ${registryFile}`);
  insertBefore(
    'src/experimental/README.md',
    '<!-- experiments:end -->',
    `| [${name}](${name}/README.md) | ${destinationText} |`,
  );
}

const [kind, name, ...rest] = process.argv.slice(2);
if (!['feature', 'experiment'].includes(kind) || !name || !NAME.test(name))
  fail(
    'Usage: new.mjs feature|experiment <lower-case-name> [options]; see the header of scripts/new.mjs.',
  );
const { values } = parseArgs({
  args: rest,
  options: {
    uses: { type: 'string' },
    'part-of': { type: 'string' },
    destination: { type: 'string' },
    owner: { type: 'string' },
    server: { type: 'boolean' },
    billed: { type: 'boolean' },
  },
});
if (kind === 'feature') newFeature(name, values);
else newExperiment(name, values);
console.log('Next: fill in the TODOs, then run `npm run context`.');
