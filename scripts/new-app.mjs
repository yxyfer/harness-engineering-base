#!/usr/bin/env node
// Sets up a Next.js application with the harness layout, checks and contract.
//
//   npm run new-app -- <directory> [--name "Display name"]
//
// An empty or missing directory gets a new app from create-next-app at the
// latest stable release, then the layout, with dependencies installed and
// pinned. A directory with a package.json is an existing app: only missing
// files are added, nothing is overwritten or installed, and what needs a
// manual merge is listed. This is a one-off copy; there is no sync.
import { spawnSync } from 'node:child_process';
import {
  cpSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const kitRoot = fileURLToPath(new URL('../', import.meta.url));
const templateRoot = join(kitRoot, '.harness/templates/nextjs/files');

// Kit files every app gets a copy of, so the app never depends on the kit's path.
const SHARED = {
  '.harness/standards': '.harness/standards',
  '.harness/templates/architecture.md': '.harness/templates/architecture.md',
  'docs/WORKFLOW.md': 'docs/WORKFLOW.md',
  'project/FORMAT.md': 'docs/FORMAT.md',
  'scripts/check-framework-versions.mjs':
    'scripts/check-framework-versions.mjs',
  '.editorconfig': '.editorconfig',
  '.prettierrc.json': '.prettierrc.json',
  '.prettierignore': '.prettierignore',
  '.node-version': '.node-version',
};

// create-next-app writes these; in a new app the harness versions replace them.
const REPLACED_IN_NEW_APP = new Set([
  'eslint.config.mjs',
  'tsconfig.json',
  'AGENTS.md',
  'CLAUDE.md',
]);

const SCRIPTS = {
  setup: 'npm ci --ignore-scripts && npm run check:versions -- .',
  format: 'prettier --write .',
  'format:check': 'prettier --check .',
  lint: 'eslint . --max-warnings=0',
  typecheck: 'next typegen && tsc --noEmit',
  check: 'npm run format:check && npm run lint && npm run typecheck',
  'self-test': 'node --test tests/*.test.mjs',
  test: 'node --import tsx --test "tests/**/*.test.ts" "src/**/*.test.ts"',
  context: 'node scripts/context.mjs',
  'context:check': 'node scripts/context.mjs --check',
  'new-feature': 'node scripts/new.mjs feature',
  'new-experiment': 'node scripts/new.mjs experiment',
  'check:versions': 'node scripts/check-framework-versions.mjs',
  verify:
    'npm run check:versions -- . && npm run check && npm run self-test && npm test && npm run context:check && npm run build',
};
const DEV_DEPENDENCIES = ['tsx', 'prettier'];
const DEPENDENCIES = ['server-only'];

const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: { name: { type: 'string' } },
});
if (positionals.length !== 1) {
  console.error(
    'Usage: npm run new-app -- <directory> [--name "Display name"]',
  );
  process.exit(1);
}
const target = resolve(positionals[0]);
const fresh =
  !existsSync(target) ||
  (statSync(target).isDirectory() && readdirSync(target).length === 0);
if (!fresh && !existsSync(join(target, 'package.json'))) {
  console.error(
    `${target} is neither empty nor an npm app (no package.json); nothing changed.`,
  );
  process.exit(1);
}

function run(command, args, cwd) {
  console.log(`$ ${command} ${args.join(' ')}`);
  const result = spawnSync(command, args, { cwd, stdio: 'inherit' });
  if (result.status !== 0) {
    console.error(`${command} failed; the directory may be half set up.`);
    process.exit(result.status ?? 1);
  }
}

if (fresh) {
  mkdirSync(dirname(target), { recursive: true });
  run(
    'npx',
    [
      '--yes',
      'create-next-app@latest',
      target,
      '--typescript',
      '--eslint',
      '--app',
      '--src-dir',
      '--import-alias',
      '@/*',
      '--use-npm',
      '--no-tailwind',
      '--skip-install',
      '--disable-git',
      '--yes',
    ],
    dirname(target),
  );
}

const packageFile = join(target, 'package.json');
const manifest = JSON.parse(readFileSync(packageFile, 'utf8'));
const name = values.name ?? manifest.name ?? basename(target);
const created = [];
const kept = [];
const merge = [];

function files(root, prefix = '') {
  return readdirSync(join(root, prefix), { withFileTypes: true }).flatMap(
    (entry) => {
      const path = join(prefix, entry.name);
      return entry.isDirectory() ? files(root, path) : [path];
    },
  );
}

function place(source, destination, render = (text) => text) {
  const path = join(target, destination);
  const replace = fresh && REPLACED_IN_NEW_APP.has(destination);
  if (existsSync(path) && !replace) {
    kept.push(destination);
    if (REPLACED_IN_NEW_APP.has(destination)) merge.push(destination);
    return;
  }
  mkdirSync(dirname(path), { recursive: true });
  if (/\.(md|json)$/.test(destination) || destination.endsWith('.mjs'))
    writeFileSync(path, render(readFileSync(source, 'utf8')));
  else cpSync(source, path);
  created.push(destination);
}

const withName = (text) => text.replaceAll('{{name}}', name);
for (const file of files(templateRoot))
  place(
    join(templateRoot, file),
    file,
    file.endsWith('.md') ? withName : undefined,
  );
for (const [from, to] of Object.entries(SHARED)) {
  const source = join(kitRoot, from);
  if (!existsSync(source)) continue;
  if (statSync(source).isDirectory())
    for (const file of files(source)) place(join(source, file), join(to, file));
  else place(source, to);
}

// Generated context must not be reformatted, or its freshness check fails.
const ignoreFile = join(target, '.prettierignore');
if (
  !fresh &&
  existsSync(ignoreFile) &&
  !/^context\/$/m.test(readFileSync(ignoreFile, 'utf8'))
)
  merge.push('.prettierignore: add the line "context/"');

// Scripts: add what is missing; in a new app the harness owns them all.
manifest.scripts ??= {};
for (const [script, command] of Object.entries(SCRIPTS)) {
  const current = manifest.scripts[script];
  if (current === undefined || fresh) manifest.scripts[script] = command;
  else if (current !== command)
    merge.push(
      `package.json script "${script}": keep "${current}" or use "${command}"`,
    );
}
manifest.engines ??= { node: '>=24.10.0', npm: '>=11.6.0' };
writeFileSync(packageFile, `${JSON.stringify(manifest, null, 2)}\n`);

// The kit revision this app was set up from, for later manual updates.
const revision = spawnSync('git', ['rev-parse', 'HEAD'], {
  cwd: kitRoot,
  encoding: 'utf8',
}).stdout?.trim();
const upstream = join(target, '.harness/UPSTREAM.md');
if (!existsSync(upstream)) {
  mkdirSync(dirname(upstream), { recursive: true });
  writeFileSync(
    upstream,
    `# Harness source\n\nSet up by \`new-app\` from kit revision \`${revision || 'unknown'}\` on ${new Date().toISOString().slice(0, 10)}.\nTo update, compare the kit's current templates with this app's copies, merge what applies by hand, record the new revision here and run \`npm run verify\`.\n`,
  );
  created.push('.harness/UPSTREAM.md');
}

/** Replaces ranges such as ^16.4.0 with the exact installed version. */
function pinExact() {
  const pinned = JSON.parse(readFileSync(packageFile, 'utf8'));
  let changed = false;
  for (const group of ['dependencies', 'devDependencies'])
    for (const [dependency, range] of Object.entries(pinned[group] ?? {})) {
      if (/^\d+\.\d+\.\d+$/.test(range)) continue;
      const installed = join(
        target,
        'node_modules',
        dependency,
        'package.json',
      );
      if (!existsSync(installed)) continue;
      pinned[group][dependency] = JSON.parse(
        readFileSync(installed, 'utf8'),
      ).version;
      changed = true;
    }
  if (changed)
    writeFileSync(packageFile, `${JSON.stringify(pinned, null, 2)}\n`);
  return changed;
}

if (fresh) {
  // create-next-app's own pins can trail npm's latest stable releases; the
  // version gate would then fail on a brand-new app. Take latest explicitly,
  // and the lint config at exactly the installed Next.js version.
  run(
    'npm',
    [
      'install',
      '--save-exact',
      'next@latest',
      'react@latest',
      'react-dom@latest',
      ...DEPENDENCIES,
    ],
    target,
  );
  const next = JSON.parse(
    readFileSync(join(target, 'node_modules/next/package.json'), 'utf8'),
  ).version;
  run(
    'npm',
    [
      'install',
      '--save-exact',
      '--save-dev',
      `eslint-config-next@${next}`,
      '@types/node@24',
      ...DEV_DEPENDENCIES,
    ],
    target,
  );
  if (pinExact()) run('npm', ['install'], target);
  run('npm', ['run', 'format'], target);
}
run('node', ['scripts/context.mjs'], target);

const shown = (list) => list.map((item) => `  ${item}`).join('\n');
console.log(
  `\n${name}: ${created.length} files added, ${kept.length} existing files kept.`,
);
if (merge.length)
  console.log(
    `\nMerge by hand (the harness version is in the kit's templates):\n${shown(merge)}`,
  );
if (!fresh)
  console.log(
    `\nExisting app: nothing was installed. Add the dependencies yourself:\n  npm install --save-exact --save-dev ${DEV_DEPENDENCIES.join(' ')}\n  npm install --save-exact ${DEPENDENCIES.join(' ')}`,
  );
console.log(
  `\nNext, in ${relative(process.cwd(), target) || '.'}:\n  npm run verify\n  npm run new-feature -- <name>   (when the first capability appears)\n  npm run new-experiment -- <name> --destination feature`,
);
