import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const packages = {
  next: 'dependencies',
  react: 'dependencies',
  'react-dom': 'dependencies',
  'eslint-config-next': 'devDependencies',
};
const stableVersion = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function readPins(directory) {
  const manifest = readJson(join(directory, 'package.json'));
  const lock = readJson(join(directory, 'package-lock.json'));
  const pins = {};

  for (const [name, section] of Object.entries(packages)) {
    const pin = manifest[section]?.[name];
    if (typeof pin !== 'string' || !stableVersion.test(pin)) {
      throw new Error(
        `${name} must use an exact stable version in package.json`,
      );
    }
    const sources = {
      'lock manifest': lock.packages?.['']?.[section]?.[name],
      'lock resolution': lock.packages?.[`node_modules/${name}`]?.version,
      installed: readJson(join(directory, 'node_modules', name, 'package.json'))
        .version,
    };
    for (const [source, version] of Object.entries(sources)) {
      if (version !== pin) {
        throw new Error(
          `${name}: ${source} is ${version ?? 'missing'}; expected ${pin}. ` +
            'Review app pins and lock, then run npm ci in that app.',
        );
      }
    }
    pins[name] = pin;
  }
  for (const [name, owner] of [
    ['react-dom', 'react'],
    ['eslint-config-next', 'next'],
  ]) {
    if (pins[name] !== pins[owner]) {
      throw new Error(`${name} must match ${owner}: ${pins[owner]}`);
    }
  }
  return pins;
}

async function latestStable(name, request) {
  try {
    const response = await request(
      `https://registry.npmjs.org/${name}/latest`,
      {
        cache: 'no-store',
        redirect: 'error',
        signal: AbortSignal.timeout(10000),
      },
    );
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const metadata = await response.json();
    if (
      metadata.name !== name ||
      typeof metadata.version !== 'string' ||
      !stableVersion.test(metadata.version)
    ) {
      throw new Error('Registry latest metadata is not a stable release');
    }
    return metadata.version;
  } catch (error) {
    throw new Error(
      `Cannot verify latest stable ${name}: ${error.message}. ` +
        'Fresh registry evidence is required; retry with network access.',
      { cause: error },
    );
  }
}

export async function checkFrameworkVersions(directory, request = fetch) {
  const pins = readPins(directory);
  const names = Object.keys(packages);
  const latest = await Promise.all(
    names.map((name) => latestStable(name, request)),
  );
  const outdated = names.flatMap((name, index) =>
    pins[name] === latest[index]
      ? []
      : [`${name}: pinned ${pins[name]}; latest stable is ${latest[index]}`],
  );
  if (outdated.length > 0) {
    throw new Error(
      outdated.join('\n') +
        '\nUpdate exact pins and the lock, then rerun full verification.',
    );
  }
  return names.map((name) => `${name}: ${pins[name]} (latest stable)`);
}

if (import.meta.main) {
  try {
    if (!process.argv[2] || process.argv.length !== 3) {
      throw new Error('Usage: npm run check:versions -- <app-directory>');
    }
    const directory = resolve(process.argv[2]);
    const lines = await checkFrameworkVersions(directory);
    console.log(lines.join('\n'));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
