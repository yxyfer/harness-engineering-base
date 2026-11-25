// Formats what the harness scripts write with the application's own Prettier
// and settings, so generated and updated files pass `format:check` like any
// other file.
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

let prettier;

async function load(appDir, optional) {
  if (prettier !== undefined) return prettier;
  try {
    const require = createRequire(join(resolve(appDir), 'package.json'));
    const loaded = await import(
      pathToFileURL(require.resolve('prettier')).href
    );
    // The CommonJS entry exposes the API as `default`; the ESM one does not.
    prettier = loaded.format ? loaded : loaded.default;
    return prettier;
  } catch {
    prettier = null;
    if (optional) return null;
    console.error(
      'Prettier is not installed in this app. Run `npm install --save-exact --save-dev prettier`.',
    );
    process.exit(1);
  }
}

/**
 * Formats text as the file at `path` would be formatted. With `optional`, a
 * missing Prettier returns the text tidied but unformatted.
 */
export async function formatText(
  appDir,
  path,
  text,
  { optional = false } = {},
) {
  const api = await load(appDir, optional);
  if (!api) return `${text.replace(/\n{3,}/g, '\n\n').trimEnd()}\n`;
  const options = (await api.resolveConfig(path)) ?? {};
  return api.format(text, { ...options, filepath: path });
}

/** Rewrites each file in place, formatted. */
export async function formatFiles(appDir, paths) {
  for (const path of paths)
    writeFileSync(
      path,
      await formatText(appDir, path, readFileSync(path, 'utf8')),
    );
}
