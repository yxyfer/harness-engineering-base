import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  copyFileSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { checkFrameworkVersions } from '../scripts/check-framework-versions.mjs';

// These releases and registry responses are synthetic, never freshness proof.
const versions = {
  next: '20.0.0',
  react: '22.0.0',
  'react-dom': '22.0.0',
  'eslint-config-next': '20.0.0',
};

function fixture(context, overrides = {}) {
  const root = mkdtempSync(join(tmpdir(), 'harness-framework-versions-'));
  context.after(() => rmSync(root, { recursive: true, force: true }));
  const pins = { ...versions, ...overrides.pins };
  const manifest = {
    dependencies: {
      next: pins.next,
      react: pins.react,
      'react-dom': pins['react-dom'],
    },
    devDependencies: { 'eslint-config-next': pins['eslint-config-next'] },
  };
  const locked = { ...pins, ...overrides.locked };
  const installed = { ...pins, ...overrides.installed };
  const packages = { '': manifest };
  for (const name of Object.keys(versions)) {
    packages[`node_modules/${name}`] = { version: locked[name] };
    const directory = join(root, 'node_modules', name);
    mkdirSync(directory, { recursive: true });
    writeFileSync(
      join(directory, 'package.json'),
      JSON.stringify({ name, version: installed[name] }),
    );
  }
  writeFileSync(join(root, 'package.json'), JSON.stringify(manifest));
  writeFileSync(
    join(root, 'package-lock.json'),
    JSON.stringify({ lockfileVersion: 3, packages }),
  );
  return root;
}

function registry(overrides = {}) {
  return async (url, options) => {
    const name = new URL(url).pathname.split('/')[1];
    assert.equal(url, `https://registry.npmjs.org/${name}/latest`);
    assert.equal(options.cache, 'no-store');
    assert.equal(options.redirect, 'error');
    assert.ok(options.signal instanceof AbortSignal);
    return Response.json({ name, version: versions[name], ...overrides[name] });
  };
}

test('current exact pins, lock and installed packages pass', async (context) => {
  const calls = [];
  const request = registry();
  const lines = await checkFrameworkVersions(
    fixture(context),
    (url, options) => {
      calls.push(url);
      return request(url, options);
    },
  );
  assert.equal(calls.length, 4);
  assert.equal(lines.length, 4);
  assert.match(lines.join('\n'), /next: 20\.0\.0/);
});

test('a new stable release rejects an otherwise valid install', async (context) => {
  const directory = fixture(context);
  const manifest = readFileSync(join(directory, 'package.json'), 'utf8');
  const lock = readFileSync(join(directory, 'package-lock.json'), 'utf8');
  await assert.rejects(
    checkFrameworkVersions(
      directory,
      registry({ next: { version: '20.0.1' } }),
    ),
    /next: pinned 20\.0\.0; latest stable is 20\.0\.1/,
  );
  assert.equal(readFileSync(join(directory, 'package.json'), 'utf8'), manifest);
  assert.equal(
    readFileSync(join(directory, 'package-lock.json'), 'utf8'),
    lock,
  );
});

test('ranges and prerelease pins are rejected', async (context) => {
  for (const version of ['^20.0.0', 'latest', '20.1.0-canary.1']) {
    await assert.rejects(
      checkFrameworkVersions(
        fixture(context, { pins: { next: version } }),
        registry(),
      ),
      /next must use an exact stable version/,
    );
  }
});

test('a manifest edit cannot hide lock or installed drift', async (context) => {
  for (const source of ['locked', 'installed']) {
    await assert.rejects(
      checkFrameworkVersions(
        fixture(context, { [source]: { react: '21.0.0' } }),
        registry(),
      ),
      /react.*21\.0\.0.*22\.0\.0/,
    );
  }
});

test('missing lock entries and stale root pins are rejected', async (context) => {
  for (const source of ['root', 'resolved']) {
    const directory = fixture(context);
    const path = join(directory, 'package-lock.json');
    const lock = JSON.parse(readFileSync(path, 'utf8'));
    if (source === 'root') lock.packages[''].dependencies.next = '19.0.0';
    else delete lock.packages['node_modules/next'];
    writeFileSync(path, JSON.stringify(lock));
    await assert.rejects(
      checkFrameworkVersions(directory, registry()),
      /next: lock.*expected 20\.0\.0/,
    );
  }
});

test('React DOM and Next lint config must match their owners', async (context) => {
  for (const name of ['react-dom', 'eslint-config-next']) {
    await assert.rejects(
      checkFrameworkVersions(
        fixture(context, { pins: { [name]: '1.0.0' } }),
        registry(),
      ),
      /must match/,
    );
  }
});

test('unreachable registry and HTTP errors fail instead of using a cache', async (context) => {
  const offline = async () => {
    throw new Error('synthetic network failure');
  };
  const unavailable = async () => new Response(null, { status: 503 });
  for (const request of [offline, unavailable]) {
    await assert.rejects(
      checkFrameworkVersions(fixture(context), request),
      /Cannot verify latest stable next/,
    );
  }
});

test('prerelease or malformed latest metadata cannot pass', async (context) => {
  for (const metadata of [
    { version: '20.1.0-rc.1' },
    { version: undefined },
    { name: 'different-package' },
  ]) {
    await assert.rejects(
      checkFrameworkVersions(fixture(context), registry({ next: metadata })),
      /Cannot verify latest stable next/,
    );
  }
});

test('the executable exits nonzero for an incomplete app', (context) => {
  const directory = fixture(context);
  rmSync(join(directory, 'node_modules', 'react'), { recursive: true });
  const script = new URL(
    '../scripts/check-framework-versions.mjs',
    import.meta.url,
  );
  const result = spawnSync(
    process.execPath,
    [fileURLToPath(script), directory],
    {
      encoding: 'utf8',
      timeout: 10000,
    },
  );
  assert.equal(result.error, undefined);
  assert.equal(result.status, 1, result.stdout + result.stderr);
  assert.match(result.stderr, /ENOENT.*react\/package\.json/);
});

test('the executable requires an explicit application directory', (context) => {
  const directory = fixture(context);
  const tools = join(directory, 'tools');
  mkdirSync(tools);
  const script = join(tools, 'check-framework-versions.mjs');
  copyFileSync(
    new URL('../scripts/check-framework-versions.mjs', import.meta.url),
    script,
  );
  const result = spawnSync(process.execPath, [script], {
    encoding: 'utf8',
    timeout: 10000,
  });
  assert.equal(result.error, undefined);
  assert.equal(result.status, 1, result.stdout + result.stderr);
  assert.match(result.stderr, /Usage:.*<app-directory>/);
});
