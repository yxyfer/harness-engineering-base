# Next.js application template

Everything under [`files/`](files) is copied into an application by
`npm run new-app -- <directory>` from the kit root, together with the kit's
standards, workflow, document format, formatter settings and version checker.

- **New app** (missing or empty directory): runs `create-next-app` at the latest
  stable release, replaces its ESLint, TypeScript and agent files with these,
  installs `tsx`, `prettier` and `server-only`, pins every dependency exactly,
  formats, and writes the first context map.
- **Existing app** (has a `package.json`): adds only missing files and scripts,
  overwrites nothing, installs nothing, and lists what to merge by hand.

It is a one-off copy. `.harness/UPSTREAM.md` in the app records the kit
revision; later kit changes are merged by hand.

## What the app gets

| Piece                            | Files                                                                    |
| -------------------------------- | ------------------------------------------------------------------------ |
| Contract, as a router            | `AGENTS.md`, `CLAUDE.md`                                                 |
| Layered source, one doc each     | `src/README.md`, `src/{core,features,experimental}/README.md`            |
| Experiment registry and decision | `src/config/experiments.ts`, `src/core/experiments.ts`                   |
| Settings switches                | `src/components/experiment-settings.tsx`                                 |
| Module boundaries                | `eslint.config.mjs`, `eslint.boundaries.mjs`, `src/config/features.json` |
| Generators                       | `scripts/new.mjs` (`npm run new-feature`, `npm run new-experiment`)      |
| Context map                      | `scripts/context.mjs` writes `context/` (`npm run context`)              |
| Self-tests                       | `tests/boundaries.test.mjs`, `tests/documents.test.mjs`                  |
| Experiment tests                 | `tests/experiments.test.ts`                                              |
| CI                               | `.github/workflows/ci.yml`                                               |
| Architecture and decisions       | `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/debt.md`              |

## Layout

`app → experimental → features → components → core → config`; dependencies point
down only, checked by `import/no-restricted-paths` on resolved paths. Zones are
generated from the folders that exist and from `src/config/features.json`, so
new features and experiments are covered without editing the lint config.
`tests/boundaries.test.mjs` lints a synthetic tree with eleven forbidden imports
to prove each rule fails.

## Experiments

An experiment starts at stage `testers`: on by default for testers, who can turn
it off, and invisible to everyone else. `everyone` lets anyone opt in; `off` is
the kill switch. Testers come from `EXPERIMENT_TESTERS` (IDs or emails, or `*`);
when it is unset, everyone is a tester under `next dev`. Only explicit choices
are stored, through an `ExperimentChoiceStore` the app implements. A `billed`
experiment is never on by default.

## Context and token budgets

`context/README.md` (start map), `context/status.md` (every open item by state)
and `context/files.md` (every file and its exports) are generated from the code
and READMEs and checked in CI. The contract tells an agent to read the map and
the one README it needs instead of exploring. `tests/documents.test.mjs` keeps
the always-read documents within token budgets.

## Compatibility

`eslint-config-next` still needs ESLint 9; see
[the debt](../../../project/debt.md). Keep React, hooks and TypeScript rules on,
strict TypeScript and erasable syntax. Read the app's installed Next.js docs
before changing framework behaviour.
