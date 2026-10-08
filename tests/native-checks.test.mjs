import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  copyFileSync,
  mkdtempSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const kitRoot = fileURLToPath(new URL('../', import.meta.url));
const validSource = "export const probe = 'synthetic fixture';\n";

function createFixture(context) {
  const root = mkdtempSync(join(tmpdir(), 'harness-native-checks-'));
  context.after(() => rmSync(root, { recursive: true, force: true }));
  for (const file of [
    '.prettierrc.json',
    '.prettierignore',
    'eslint.config.mjs',
    'package.json',
  ]) {
    copyFileSync(join(kitRoot, file), join(root, file));
  }
  symlinkSync(join(kitRoot, 'node_modules'), join(root, 'node_modules'), 'dir');
  writeFileSync(join(root, 'native-probe.mjs'), validSource);
  return root;
}

function runCommand(root, command) {
  const environment = {
    ...process.env,
    npm_config_cache: join(root, 'npm-cache'),
  };
  delete environment.NODE_TEST_CONTEXT;
  const result = spawnSync('npm', ['run', command], {
    cwd: root,
    encoding: 'utf8',
    timeout: 30000,
    env: environment,
  });
  assert.equal(result.error, undefined, result.error?.message);
  assert.equal(result.signal, null, 'Native command must exit normally');
  return { status: result.status, output: result.stdout + result.stderr };
}

const faults = [
  {
    name: 'Prettier rejects unformatted source',
    source: "export const probe={name:'fixture'}\n",
    command: 'format:check',
    diagnostic: /native-probe\.mjs/,
  },
  {
    name: 'ESLint rejects an undefined JavaScript value',
    source: 'export const probe = missingValue;\n',
    command: 'lint',
    diagnostic: /no-undef/,
  },
];

function assertPassing(root) {
  for (const command of ['format:check', 'lint']) {
    const result = runCommand(root, command);
    assert.equal(result.status, 0, result.output);
  }
}

test('kit quality commands detect failures without a framework install', async (context) => {
  const root = createFixture(context);
  await context.test('valid source passes every kit check', () => {
    assertPassing(root);
  });
  for (const fault of faults) {
    await context.test(fault.name, () => {
      const path = join(root, 'native-probe.mjs');
      try {
        writeFileSync(path, fault.source);
        const result = runCommand(root, fault.command);
        assert.equal(result.status, 1, result.output);
        assert.match(result.output, fault.diagnostic);
      } finally {
        writeFileSync(path, validSource);
      }
    });
  }
  await context.test('restored source passes after the failure probes', () => {
    assertPassing(root);
  });
});
