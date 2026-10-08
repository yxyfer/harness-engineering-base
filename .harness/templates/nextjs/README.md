# Next.js native settings

These are adoption configurations, with no app source, dependency lock or
installed framework. The ESLint and TypeScript settings were exercised during
P001-T002; the validation app was then removed from the kit.

- Merge [eslint.config.mjs](eslint.config.mjs) into the receiving app's native
  config. Keep Next core web vitals, React hooks and TypeScript rules enabled.
- Merge [tsconfig.json](tsconfig.json) while preserving the app's aliases,
  includes and framework needs. Keep strict checking and erasable syntax.
- Reuse the kit's Prettier, editor and npm settings when compatible with the
  project. Do not overwrite consumer-owned files.

Install Next.js, React, React DOM, the matching Next lint config and compatible
ESLint, TypeScript and type definitions in the receiving app. Resolve current
stable versions and save exact pins with a lock and strict peer checks. See
[the compatibility debt](../../../project/debt.md) before choosing ESLint; do
not force an incompatible dependency tree.

Use native app commands for `eslint . --max-warnings=0`,
`next typegen && tsc --noEmit`, behaviour tests, `next build` and relevant
browser journeys. Read that app's installed framework docs before changing
behaviour.

Wire `node <kit-directory>/scripts/check-framework-versions.mjs <app-directory>`
into the app's setup and full verification. This command targets a standalone
npm app with its own lock and installed dependency directory; it checks stable
freshness, exact pins, lock entries and installed packages without changing
them. Invoke it from the kit with `npm run check:versions -- <app-directory>`.
Missing targets, unknown freshness and outdated versions fail. Local app lint
and types can run offline; retained-work verification must include the live
version gate.

The kit's own setup installs formatting and lint tools only. Its verification
does not type-check, build or exercise a receiving application.
