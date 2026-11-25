// The files the kit copies into an application, and where each one lands.
// new-app copies them; harness-diff compares an app's copies with the kit.
import { existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const kitRoot = fileURLToPath(new URL('../', import.meta.url));
export const templatePath = '.harness/templates/nextjs/files';

// Kit files every app gets a copy of, so the app never depends on the kit.
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

function files(root, prefix = '') {
  return readdirSync(join(root, prefix), { withFileTypes: true }).flatMap(
    (entry) => {
      const path = join(prefix, entry.name);
      return entry.isDirectory() ? files(root, path) : [path];
    },
  );
}

/**
 * Every copied file as { kit, app, named }: paths relative to the kit and to
 * the app, and whether `{{name}}` is replaced with the app's name.
 */
export function kitFiles() {
  const entries = files(join(kitRoot, templatePath)).map((file) => ({
    kit: join(templatePath, file),
    app: file,
    named: file.endsWith('.md'),
  }));
  for (const [from, to] of Object.entries(SHARED)) {
    const source = join(kitRoot, from);
    if (!existsSync(source)) continue;
    if (statSync(source).isDirectory())
      for (const file of files(source))
        entries.push({
          kit: join(from, file),
          app: join(to, file),
          named: false,
        });
    else entries.push({ kit: from, app: to, named: false });
  }
  return entries;
}
