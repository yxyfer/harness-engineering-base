// Module boundaries for the layered source tree, checked by
// `import/no-restricted-paths` on resolved paths: aliases, relative paths,
// re-exports, type imports and literal dynamic imports alike. AGENTS.md
// describes the layout; tests/boundaries.test.mjs proves the rules reject.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

/** Each feature and the features it may use: src/config/features.json. */
export function readFeatureDependencies(root) {
  const file = join(root, 'src/config/features.json');
  return existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : {};
}

function directories(root, path) {
  const full = join(root, path);
  return existsSync(full)
    ? readdirSync(full, { withFileTypes: true })
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)
    : [];
}

export function boundaryZones(
  root,
  featureDependencies = readFeatureDependencies(root),
) {
  // A client component reaches a Server Action through its module reference.
  // Anchored so the globs also match under a hidden worktree directory.
  const serverActions = ['**/actions.ts', '**/*-actions.ts'].map((pattern) =>
    join(root, 'src/app', pattern),
  );
  const entryFiles = ['./src/proxy.ts', './src/middleware.ts'];
  return [
    {
      target: './src/config',
      from: './src',
      except: ['./config'],
      message:
        'src/config holds plain registries and imports no application code.',
    },
    {
      target: './src/core',
      from: './src',
      except: ['./core', './config'],
      message: 'Core may use only core and src/config.',
    },
    {
      target: './src/components',
      from: './src',
      except: ['./components', './core', './config'],
      message: 'Shared UI may use only shared UI, core and src/config.',
    },
    {
      target: './src/features',
      from: './src/experimental',
      message: 'Stable features never depend on experiments.',
    },
    {
      target: ['./src/features', './src/experimental'],
      from: ['./src/app/**/*'],
      except: serverActions,
      message: 'Only Server Action modules may be imported from src/app.',
    },
    ...entryFiles.map((from) => ({
      target: ['./src/features', './src/experimental'],
      from,
      message: 'The request proxy is an application entry point.',
    })),
    ...directories(root, 'src/features').flatMap((feature) => [
      {
        target: `./src/features/${feature}`,
        from: './src/features',
        except: [feature, ...(featureDependencies[feature] ?? [])].map(
          (name) => `./${name}`,
        ),
        message: `${feature} may use only the features listed for it in src/config/features.json.`,
      },
      {
        target: [
          './src/app/**/*',
          './src/experimental/**/*',
          `./src/features/!(${feature})/**/*`,
        ],
        from: `./src/features/${feature}/internal`,
        message: `${feature}/internal is private to that feature.`,
      },
    ]),
    ...directories(root, 'src/experimental').flatMap((experiment) => [
      {
        target: `./src/experimental/${experiment}`,
        from: './src/experimental',
        except: [`./${experiment}`],
        message: 'Experiments stay independent of one another.',
      },
      {
        target: ['./src/app', ...entryFiles],
        from: `./src/experimental/${experiment}`,
        except: ['./index.ts', './index.tsx', './server.ts'],
        message: `Import ${experiment} only through its index or server entry point.`,
      },
    ]),
  ];
}
