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

| Piece                            | Files                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------- |
| Contract, as a router            | `AGENTS.md`, `CLAUDE.md`                                                                  |
| Layered source, one doc each     | `src/README.md`, `src/{core,features,experimental}/README.md`                             |
| Experiment registry and decision | `src/config/experiments.ts`, `src/core/experiments.ts`                                    |
| Settings switches                | `src/components/experiment-settings.tsx`                                                  |
| Module boundaries                | `eslint.config.mjs`, `eslint.boundaries.mjs`, `src/config/features.json`                  |
| Generators                       | `scripts/new.mjs` (`npm run new-feature`, `npm run new-experiment`)                       |
| Context map                      | `scripts/context.mjs` writes `context/` (`npm run context`)                               |
| Self-tests                       | `tests/boundaries.test.mjs`, `tests/documents.test.mjs`                                   |
| Experiment tests                 | `tests/experiments.test.ts`                                                               |
| CI                               | `.github/workflows/ci.yml`                                                                |
| Session-start map (Claude Code)  | `.claude/settings.json`                                                                   |
| Per-request experiment viewer    | `src/app/experiments.ts`, `src/app/experiment-actions.ts`, `src/core/experiment-store.ts` |
| Token benchmark                  | `scripts/bench.mjs`, `.harness/bench.json` (`npm run bench`)                              |
| Architecture and decisions       | `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/debt.md`                               |

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

`context/README.md` (start map with "Start with" files), `context/status.md`
(open items by state, by whom they wait on, with ages) and `context/files.md`
(every file and its exports) are generated per checkout and ignored by Git. In
Claude Code the session-start hook regenerates the map and prints it into the
session. The contract routes reads by task; `tests/documents.test.mjs` keeps
documents within token budgets and at most five Next items each. Measure with
`npm run bench` before and after changing documents.

## Compatibility

`eslint-config-next` still needs ESLint 9; see
[the debt](../../../project/debt.md). Keep React, hooks and TypeScript rules on,
strict TypeScript and erasable syntax. Read the app's installed Next.js docs
before changing framework behaviour.

## Adopting in an existing app

Learned moving a real application onto this template:

- Any test that copies `eslint.config.mjs` into a temporary folder must copy
  `eslint.boundaries.mjs` (and give its synthetic tree a
  `src/config/features.json`), or ESLint cannot load the config.
- Map an old public opt-in flag to `stage: 'everyone'` and an internal-only one
  to `stage: 'testers'`. With `EXPERIMENT_TESTERS` unset in production, public
  behaviour is unchanged; pass the tester flag as a trailing argument so
  existing tests keep their meaning.
- Unlabelled open work is mostly known limitations. Label them `To decide`
  rather than inventing commitments, and let the owner prune.
- Over-budget READMEs and a change-log architecture file are real debts: record
  them as open work with a temporary budget rather than rewriting history in the
  adoption change.
- The Next.js build does not follow a symlinked `node_modules`; use a real
  install (or a hard-linked copy) in a worktree.
