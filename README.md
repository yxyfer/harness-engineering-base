# Lean engineering harness

Keep the code readable, prototype quickly, and make the architecture easy to
understand. Use Explore, Build or Release according to the intended use and
consequences of failure. Start at [project/README.md](project/README.md).

This repository holds the engineering agreement, native settings and small
verification tools. Application code and framework installations belong to the
actual application. There is no installed Next.js example, database, installer
or CI workflow here.

## What we keep

| Owner                                                                                                   | Purpose                                                              |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)                                                                                  | Entry point and working contract                                     |
| [docs/WORKFLOW.md](docs/WORKFLOW.md)                                                                    | Explore, Build, Release and refactoring rules                        |
| [.harness/standards/](.harness/standards/BASE.md)                                                       | Readability, architecture, testing and language guidance             |
| [.harness/templates/nextjs/](.harness/templates/nextjs/README.md)                                       | Small native ESLint and TypeScript configurations to merge into apps |
| Native root configs and dependency lock                                                                 | Formatting and JavaScript lint for kit code                          |
| [Version checker](scripts/check-framework-versions.mjs) and [tests/](tests/framework-versions.test.mjs) | Stable framework enforcement and kit failure probes                  |
| [Architecture](docs/ARCHITECTURE.md), [decisions](docs/DECISIONS.md) and [plan](project/README.md)      | Current boundaries, choices and rebuild evidence                     |

## Work on the kit

Use Node 24.10 or later in the Node 24 line and npm 11.6 or later in the npm 11
line. Setup installs only the kit's formatting and lint dependencies, with
lifecycle scripts disabled.

```sh
npm run setup
npm run verify
```

| Command             | What it verifies                                                         |
| ------------------- | ------------------------------------------------------------------------ |
| `npm run format`    | Formats maintained files at the shared 80-column width                   |
| `npm run check`     | Kit formatting and JavaScript lint, without registry access              |
| `npm test`          | Version policy and real native-tool failure probes in temporary fixtures |
| `npm run self-test` | Alias for the kit tests                                                  |
| `npm run verify`    | Kit checks and tests                                                     |

The kit has no application dev server, type-check, build or browser command. Its
green verification does not prove a receiving app works.

## Use the standards in an application

Inspect the app's existing owners, dependencies and native commands. Merge the
[adoption settings](.harness/templates/nextjs/README.md) where appropriate;
install framework dependencies in that app and run its formatter, lint, types,
behaviour tests, build and relevant browser journey. Do not overwrite its
configuration or create duplicate components.

Next.js, React and React DOM use npm's current `latest` stable releases with
exact tested pins and a lock. React DOM matches React; the Next lint config
matches Next. Run the retained checker against a standalone npm app with its own
lock and installed dependency directory:

```sh
npm run check:versions -- ../your-app
```

Wire this command into the app's setup and full verification. Missing targets,
ranges, prereleases, outdated versions, mismatched lock or installed packages,
and unavailable registry evidence fail. The checker queries fresh public
metadata with a ten-second request timeout and never installs or writes files.
Keep local app checks available for offline iteration; retained-work
verification includes the live version gate.

Every upgrade needs strict peer installation, installed framework docs and
appropriate application proof. Review
[the lint compatibility constraint](project/debt.md) before choosing consumer
lint dependencies.

T002's initial React, type and browser proof is recorded as historical evidence
in [the plan](project/plans/P001-lean-harness.md). Application isolation,
architecture views and the real feature pilot remain the next work.
