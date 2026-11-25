// Lets Node run a template's TypeScript tests without a dependency: resolves
// extensionless relative imports to the matching .ts file. Node strips the
// types itself (erasable syntax only, as the template tsconfig requires).
import { existsSync } from 'node:fs';
import { registerHooks } from 'node:module';
import { fileURLToPath } from 'node:url';

registerHooks({
  resolve(specifier, context, nextResolve) {
    if (
      specifier.startsWith('.') &&
      !/\.[cm]?[jt]sx?$/.test(specifier) &&
      context.parentURL
    ) {
      const candidate = new URL(`${specifier}.ts`, context.parentURL);
      if (existsSync(fileURLToPath(candidate)))
        return nextResolve(candidate.href, context);
    }
    return nextResolve(specifier, context);
  },
});
