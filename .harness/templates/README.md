# Native static defaults

Opt-in starting inputs, not an installer or complete application foundation.
Review/copy native files into a new project; do not overwrite existing configs.
After adoption native configuration, commands and lockfiles are project-owned.
Resolve language/framework/context with doctor separately.

## TypeScript

Node 24.10.0, npm 11.6.0 were exercised. Package and lockfile pin Prettier 3.9.6,
ESLint 10.10.0, typescript-eslint 8.67.0 and TypeScript 6.0.3. TypeScript 7 from
the legacy JS fixture is intentionally not imposed on typed ESLint:
its [supported range](https://typescript-eslint.io/users/dependency-versions/)
excludes that version. Use `npm ci --ignore-scripts` for this npm default;
preserve existing pnpm/yarn scripts and reviewed locks in established projects.

`src` and `tests` are maintained/type-checked scope. Native typed lint rules
reject unsafe any operations, floating/misused promises and non-Error throws.
Restricted imports protect domain-to-I/O and client-to-server paths in this
demonstrated layout. Adjust native rules/includes for actual aliases/layout;
they are not transitive framework/security enforcement. No test runner or
Next.js foundation is implied by this static template.
Native ignores protect installed .harness/.agents machinery from application
formatting; the authoring repository's CI checks that machinery explicitly.

## Python

Python 3.14.0 was exercised; native syntax/type target is 3.11. Ruff 0.14.0,
Pyright 1.1.407 and pytest 8.4.2 are hash-locked with dependencies. Create .venv,
then run `.venv/bin/python -m pip install --require-hashes --only-binary=:all:
-r requirements-dev.lock`. Checks never install. An existing uv/Poetry/other
manager keeps its reviewed setup/format/check commands; no forced pip migration.
Pyright also requires an installed Node runtime. The harness invokes the
project-local bundled executable directly, avoiding wrapper update queries and
runtime bootstrapping. Missing Node is a failed prerequisite, not a download.

Strict Pyright covers maintained src/tests. Ruff B/BLE rules catch common bugs
and blanket exception handling. Native TID251 restricts example_app.io/server
adapter imports, with one explicit entrypoint exception. Rename rules together
with modules; runtime input validation still needs implementation and tests.
Two synthetic pytest cases demonstrate a validated pure domain boundary.

## Command contract

`format`: CLI/environment/config override, package format script, then local
Ruff/Prettier. It fixes formatting only; lint fixes require a deliberate native
invocation. Shell/Markdown-only projects declare their formatter command.

`check`: policies first, one reviewed override/aggregate script, a complete
format:check/lint/typecheck trio, or local Ruff/Pyright/Prettier/ESLint/TypeScript
defaults. Missing default tools fail; global tools/downloads never substitute.
Reviewed equivalent commands own coverage and must be non-mutating. The harness
does not parse arbitrary shell bodies or prove their adequacy. Native default
check flags never request autofixes. Source size remains a review prompt.
