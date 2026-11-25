import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  copyFileSync,
  mkdirSync,
  mkdtempSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

// Runs this application's own lint configuration over a synthetic source tree,
// so the import boundaries are proven to fail, not only described.
const appRoot = fileURLToPath(new URL('../', import.meta.url));

const allowed = {
  'src/config/features.json': JSON.stringify({
    catalogue: [],
    orders: ['catalogue'],
  }),
  'src/config/experiments.ts': 'export const EXPERIMENTS = [];\n',
  'src/core/clock.ts': 'export const now = () => 0;\n',
  'src/components/badge.ts':
    "import { now } from '@/core/clock';\nexport const badge = now;\n",
  'src/features/catalogue/sizes.ts': 'export const size = 1;\n',
  'src/features/catalogue/internal/cache.ts': 'export const cache = 1;\n',
  'src/features/orders/list.ts':
    "import { size } from '../catalogue/sizes';\nimport { save } from '@/app/actions';\nexport const list = [size, save];\n",
  'src/experimental/pilot/index.ts':
    "import { list } from '@/features/orders/list';\nimport { inner } from './inner';\nexport const pilot = [list, inner];\n",
  'src/experimental/pilot/inner.ts': 'export const inner = 1;\n',
  'src/experimental/pilot/server.ts': 'export const read = 1;\n',
  'src/app/api/pilot/route.ts':
    "import { read } from '@/experimental/pilot/server';\nexport const GET = () => read;\n",
  'src/experimental/other/index.ts': 'export const other = 1;\n',
  'src/app/actions.ts': "'use server';\nexport async function save() {}\n",
  'src/app/page.ts':
    "import { pilot } from '@/experimental/pilot';\nexport default pilot;\n",
};

const faults = [
  {
    name: 'a stable feature importing an experiment through the alias',
    file: 'src/features/orders/fault.ts',
    source:
      "import { pilot } from '@/experimental/pilot';\nexport const x = pilot;\n",
    diagnostic: /Stable features never depend on experiments/,
  },
  {
    name: 'a stable feature importing an experiment by relative path',
    file: 'src/features/orders/fault.ts',
    source:
      "import { pilot } from '../../experimental/pilot/index';\nexport const x = pilot;\n",
    diagnostic: /Stable features never depend on experiments/,
  },
  {
    name: 'core importing a feature for its types only',
    file: 'src/core/fault.ts',
    source:
      "import type { list } from '@/features/orders/list';\nexport type X = typeof list;\n",
    diagnostic: /Core may use only core/,
  },
  {
    name: 'core re-exporting an experiment',
    file: 'src/core/fault.ts',
    source: "export * from '@/experimental/pilot';\n",
    diagnostic: /Core may use only core/,
  },
  {
    name: 'core loading app routing with a dynamic import',
    file: 'src/core/fault.ts',
    source: "export const load = () => import('@/app/page');\n",
    diagnostic: /Core may use only core/,
  },
  {
    name: 'shared UI importing a feature',
    file: 'src/components/fault.ts',
    source:
      "import { list } from '@/features/orders/list';\nexport const x = list;\n",
    diagnostic: /Shared UI may use only/,
  },
  {
    name: 'a feature importing one it does not list as a dependency',
    file: 'src/features/catalogue/fault.ts',
    source:
      "import { list } from '@/features/orders/list';\nexport const x = list;\n",
    diagnostic: /catalogue may use only the features listed/,
  },
  {
    name: "a feature reaching into another feature's internals",
    file: 'src/features/orders/fault.ts',
    source:
      "import { cache } from '@/features/catalogue/internal/cache';\nexport const x = cache;\n",
    diagnostic: /catalogue\/internal is private/,
  },
  {
    name: 'a feature importing a page instead of a Server Action',
    file: 'src/features/orders/fault.ts',
    source: "import page from '@/app/page';\nexport const x = page;\n",
    diagnostic: /Only Server Action modules/,
  },
  {
    name: 'one experiment importing another',
    file: 'src/experimental/other/fault.ts',
    source:
      "import { pilot } from '@/experimental/pilot';\nexport const x = pilot;\n",
    diagnostic: /Experiments stay independent/,
  },
  {
    name: "an entry point bypassing an experiment's public entry",
    file: 'src/app/fault.ts',
    source:
      "import { inner } from '@/experimental/pilot/inner';\nexport const x = inner;\n",
    diagnostic: /only through its index or server entry point/,
  },
];

function write(root, file, source) {
  mkdirSync(dirname(join(root, file)), { recursive: true });
  writeFileSync(join(root, file), source);
}

function lint(root) {
  const environment = { ...process.env };
  delete environment.NODE_TEST_CONTEXT;
  const result = spawnSync(
    process.execPath,
    [join(appRoot, 'node_modules/eslint/bin/eslint.js'), 'src'],
    { cwd: root, encoding: 'utf8', timeout: 120000, env: environment },
  );
  assert.equal(result.error, undefined, result.error?.message);
  assert.equal(result.signal, null, 'ESLint must exit normally');
  return { status: result.status, output: result.stdout + result.stderr };
}

test('lint rejects imports that cross a module boundary', async (context) => {
  const root = mkdtempSync(join(tmpdir(), '.app-boundaries-'));
  context.after(() => rmSync(root, { recursive: true, force: true }));
  for (const file of [
    'eslint.config.mjs',
    'eslint.boundaries.mjs',
    'tsconfig.json',
    'package.json',
  ])
    copyFileSync(join(appRoot, file), join(root, file));
  symlinkSync(join(appRoot, 'node_modules'), join(root, 'node_modules'), 'dir');
  for (const [file, source] of Object.entries(allowed))
    write(root, file, source);

  await context.test('the allowed directions pass', () => {
    const result = lint(root);
    assert.equal(result.status, 0, result.output);
  });
  for (const fault of faults)
    await context.test(`rejects ${fault.name}`, () => {
      write(root, fault.file, fault.source);
      try {
        const result = lint(root);
        assert.equal(result.status, 1, result.output);
        assert.match(result.output, /import\/no-restricted-paths/);
        assert.match(result.output, fault.diagnostic);
      } finally {
        rmSync(join(root, fault.file));
      }
    });
  await context.test('the tree passes again once the faults are gone', () => {
    const result = lint(root);
    assert.equal(result.status, 0, result.output);
  });
});
