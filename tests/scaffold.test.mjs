import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import {
  existsSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Sets the layout up in an existing (synthetic) app, offline, then drives the
// generators and the app's own document, experiment and context checks there.
// Lint, types and build need Next.js; they are proven in a real app.
const kitRoot = fileURLToPath(new URL('../', import.meta.url));
const resolveHook = join(kitRoot, 'tests/support/resolve-ts.mjs');

function node(args, cwd) {
  const environment = { ...process.env };
  delete environment.NODE_TEST_CONTEXT;
  const result = spawnSync(process.execPath, args, {
    cwd,
    encoding: 'utf8',
    timeout: 60000,
    env: environment,
  });
  assert.equal(result.error, undefined, result.error?.message);
  return { status: result.status, output: result.stdout + result.stderr };
}
const ok = (result) => assert.equal(result.status, 0, result.output);
const fails = (result, pattern) => {
  assert.notEqual(result.status, 0, result.output);
  assert.match(result.output, pattern);
};

function snapshot(root, prefix = '') {
  const out = {};
  for (const entry of readdirSync(join(root, prefix), {
    withFileTypes: true,
  })) {
    const path = join(prefix, entry.name);
    if (entry.isDirectory()) Object.assign(out, snapshot(root, path));
    else
      out[path] = createHash('sha256')
        .update(readFileSync(join(root, path)))
        .digest('hex');
  }
  return out;
}

test('new-app lays out an existing app and the generators keep it consistent', async (t) => {
  const app = mkdtempSync(join(tmpdir(), 'harness-new-app-'));
  t.after(() => rmSync(app, { recursive: true, force: true }));
  writeFileSync(
    join(app, 'package.json'),
    JSON.stringify({ name: 'probe-app', scripts: { lint: 'eslint' } }, null, 2),
  );
  writeFileSync(join(app, 'AGENTS.md'), 'consumer-owned\n');
  const newApp = (args = []) =>
    node([join(kitRoot, 'scripts/new-app.mjs'), app, ...args], kitRoot);

  await t.test('adds the layout without overwriting what the app owns', () => {
    const result = newApp();
    ok(result);
    for (const file of [
      'src/README.md',
      'src/core/experiments.ts',
      'src/config/experiments.ts',
      'src/config/features.json',
      'src/experimental/README.md',
      'src/components/experiment-settings.tsx',
      'eslint.boundaries.mjs',
      'tests/boundaries.test.mjs',
      '.github/workflows/ci.yml',
      'docs/FORMAT.md',
      'docs/WORKFLOW.md',
      '.harness/standards/BASE.md',
      '.harness/stubs/experiment.md',
      'scripts/check-framework-versions.mjs',
      '.harness/UPSTREAM.md',
      'context/README.md',
    ])
      assert.ok(existsSync(join(app, file)), `${file} was not created`);
    assert.equal(
      readFileSync(join(app, 'AGENTS.md'), 'utf8'),
      'consumer-owned\n',
    );
    assert.match(result.output, /Merge by hand[\s\S]*AGENTS\.md/);
    assert.match(result.output, /script "lint": keep "eslint"/);
    assert.match(
      readFileSync(join(app, 'src/README.md'), 'utf8'),
      /^# probe-app/,
    );
    const manifest = JSON.parse(
      readFileSync(join(app, 'package.json'), 'utf8'),
    );
    assert.equal(manifest.scripts.lint, 'eslint');
    assert.equal(manifest.scripts['self-test'], 'node --test tests/*.test.mjs');
  });

  await t.test('a second run changes nothing', () => {
    const before = snapshot(app);
    ok(newApp());
    assert.deepEqual(snapshot(app), before);
  });

  await t.test('the fresh layout passes its own checks', () => {
    ok(node(['--test', 'tests/documents.test.mjs'], app));
    ok(
      node(
        ['--import', resolveHook, '--test', 'tests/experiments.test.ts'],
        app,
      ),
    );
    ok(node(['scripts/context.mjs', '--check'], app));
  });

  await t.test('generators add features, parts and experiments', () => {
    ok(node(['scripts/new.mjs', 'feature', 'catalogue'], app));
    ok(
      node(
        ['scripts/new.mjs', 'feature', 'orders', '--uses', 'catalogue'],
        app,
      ),
    );
    ok(
      node(
        ['scripts/new.mjs', 'feature', 'export', '--part-of', 'orders'],
        app,
      ),
    );
    ok(
      node(
        [
          'scripts/new.mjs',
          'experiment',
          'quick-add',
          '--destination',
          'part:orders',
          '--server',
          '--billed',
        ],
        app,
      ),
    );
    assert.deepEqual(
      JSON.parse(readFileSync(join(app, 'src/config/features.json'), 'utf8')),
      { catalogue: [], orders: ['catalogue'] },
    );
    const registry = readFileSync(
      join(app, 'src/config/experiments.ts'),
      'utf8',
    );
    assert.match(
      registry,
      /id: 'quick-add',[\s\S]*stage: 'testers',\n\s*billed: true,/,
    );
    assert.match(
      readFileSync(join(app, 'src/features/orders/README.md'), 'utf8'),
      /\[export\]\(export\/README\.md\)/,
    );
    assert.ok(existsSync(join(app, 'src/experimental/quick-add/server.ts')));
  });

  await t.test(
    'generators refuse duplicates, unknown names and bad input',
    () => {
      fails(node(['scripts/new.mjs', 'feature', 'orders'], app), /already/);
      fails(
        node(['scripts/new.mjs', 'feature', 'ship', '--uses', 'nope'], app),
        /Unknown feature/,
      );
      fails(node(['scripts/new.mjs', 'feature', 'Bad_Name'], app), /Usage/);
      fails(
        node(
          [
            'scripts/new.mjs',
            'experiment',
            'quick-add',
            '--destination',
            'feature',
          ],
          app,
        ),
        /already registered/,
      );
      fails(
        node(
          ['scripts/new.mjs', 'experiment', 'x', '--destination', 'elsewhere'],
          app,
        ),
        /destination/,
      );
    },
  );

  await t.test('the generated tree passes the app checks', () => {
    ok(node(['--test', 'tests/documents.test.mjs'], app));
    ok(
      node(
        ['--import', resolveHook, '--test', 'tests/experiments.test.ts'],
        app,
      ),
    );
    fails(node(['scripts/context.mjs', '--check'], app), /Out of date/);
    ok(node(['scripts/context.mjs'], app));
    ok(node(['scripts/context.mjs', '--check'], app));
    const map = readFileSync(join(app, 'context/README.md'), 'utf8');
    assert.match(map, /features\/orders.*\| catalogue \|/);
    assert.match(map, /experimental\/quick-add/);
  });

  await t.test('the document checks reject a broken tree', () => {
    const registryFile = join(app, 'src/config/features.json');
    const registry = readFileSync(registryFile, 'utf8');
    writeFileSync(
      registryFile,
      JSON.stringify({ catalogue: ['orders'], orders: ['catalogue'] }),
    );
    fails(node(['--test', 'tests/documents.test.mjs'], app), /cycle/);
    writeFileSync(registryFile, registry);

    const readme = join(app, 'src/features/orders/README.md');
    const text = readFileSync(readme, 'utf8');
    writeFileSync(
      readme,
      text.replace('## Open work', '## Open work\n\n- untracked idea'),
    );
    fails(node(['--test', 'tests/documents.test.mjs'], app), /needs a state/);
    writeFileSync(readme, text + 'x'.repeat(12000));
    fails(node(['--test', 'tests/documents.test.mjs'], app), /budget/);
    writeFileSync(readme, text);
    ok(node(['--test', 'tests/documents.test.mjs'], app));
  });

  await t.test(
    'the lint zones follow the folders and the feature registry',
    async () => {
      const { boundaryZones } = await import(
        pathToFileURL(join(app, 'eslint.boundaries.mjs')).href
      );
      const zones = boundaryZones(app);
      const orders = zones.find(
        (zone) => zone.target === './src/features/orders',
      );
      assert.deepEqual(orders.except, ['./orders', './catalogue']);
      assert.ok(
        zones.some(
          (zone) =>
            zone.from === './src/experimental' &&
            zone.target === './src/experimental/quick-add',
        ),
      );
    },
  );
});
