# Lean engineering harness

A kit for starting and running Next.js applications with readable code, fast
experiments and context an agent can load cheaply. Use Explore, Build or Release
according to the intended use and the consequences of failure.

```sh
npm run setup
npm run new-app -- ../my-app
```

## What it does

`new-app` creates a Next.js app, or adds to an existing one, with:

- **A layered source tree.**
  `app → experimental → features → components → core → config`, dependencies
  pointing down, enforced by lint and proven by a self-test. Work starts in
  `core`; `npm run new-feature` and `npm run new-experiment` add the rest
  consistently.
- **Experiments that reach testers without config edits.** A new experiment is
  on by default for testers and invisible to others; testers can turn it off.
  One stage field opens it to everyone or switches it off.
- **Plans as documents beside the code.** One `README.md` per feature, part and
  experiment, in one format, with open work labelled by state.
- **Cheap orientation.** A generated context map (areas, status, files and
  exports), a contract that routes reads instead of requiring them, and token
  budgets on the documents every session reads.
- **Native checks.** Format, lint, types, self-tests, tests, context check,
  build and the stable framework version gate, locally and in CI.

## How it works

| Owner                                                                                         | Purpose                                                        |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)                                                                        | Contract for working on the kit                                |
| [docs/WORKFLOW.md](docs/WORKFLOW.md)                                                          | Explore, Build, Release and refactoring rules (copied to apps) |
| [.harness/standards/](.harness/standards/BASE.md)                                             | Readability, architecture, testing and language guidance       |
| [.harness/templates/nextjs/](.harness/templates/nextjs/README.md)                             | The application template                                       |
| [scripts/new-app.mjs](scripts/new-app.mjs)                                                    | Creates or extends an app from the template                    |
| [scripts/check-framework-versions.mjs](scripts/check-framework-versions.mjs)                  | Stable framework version gate (copied to apps)                 |
| [project/FORMAT.md](project/FORMAT.md)                                                        | The document format (copied to apps as `docs/FORMAT.md`)       |
| [tests/](tests/scaffold.test.mjs)                                                             | Kit tests, including the scaffold and generators               |
| [Architecture](docs/ARCHITECTURE.md), [decisions](docs/DECISIONS.md), [debt](project/debt.md) | Kit boundaries and choices                                     |

| Command          | What it verifies                                                                                |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| `npm run check`  | Kit formatting and JavaScript lint, offline                                                     |
| `npm test`       | Version policy, native failure probes, scaffold, generators, app document and experiment checks |
| `npm run verify` | Both                                                                                            |

Use Node 24.10 or later and npm 11.6 or later. Kit checks do not prove an
application works; each app runs its own `npm run verify`.

## Choices

- Templates and a one-off scaffold, no sync engine.
  [Decision](docs/DECISIONS.md#a-scaffold-for-new-applications).
- Layered layout and tester-first experiments.
  [Decisions](docs/DECISIONS.md#layered-source-and-tester-first-experiments).
- Plans are documents beside the code; the numbered kit plan was retired.
  [Decision](docs/DECISIONS.md#plans-are-documents-beside-the-code).
- Context is generated and routed, with budgets.
  [Decision](docs/DECISIONS.md#generated-context-and-token-budgets).

## Open work

- **Next:** prove `new-app` on a real feature. Outcome: one small feature with a
  visible interaction, one persisted operation and a failure case, built in a
  new app from Explore (as an experiment) to Build (promoted), with the
  experiment removed cleanly and the context map answering where things are.
  Proof: the app's `npm run verify`, a browser journey, and a note of time,
  rework and tokens spent orienting.
- **Next:** fewer turns per task. Measured: the map and router cut peak context
  by 9 to 46%, but sessions took more steps, so total input was roughly flat.
  Outcome: a map that names the function to open, and guidance that batches
  reads. Proof: the same four tasks re-measured.
- **Next:** isolated environments for experiments that write data. Outcome: a
  recorded recipe for a worktree, a disposable or branched database and preview
  variables, with cleanup verified. Depends on a test database and preview
  project. Proof: create, write, discard and recreate, with the parent checkout
  and database untouched.
- **To decide:** whether to offer a Claude Code hook that loads
  `context/README.md` at session start, or keep the contract agent-neutral.

## Evidence and limits

`npm run verify` on Node 24.22.3 (24 tests): formatting, lint, version policy,
native failure probes and the scaffold test (layout, idempotence, generators and
their refusals, document checks including cycles, missing states and budgets,
the experiment decision, context freshness and lint zones).

On 2026-11-25 a new app made by `npm run new-app` from an empty directory passed
its own `npm run verify` with no manual step: Next.js 16.4.6 and React 19.3.1 at
latest stable, format, lint, types, 18 self-tests (eleven forbidden imports
rejected, document tree and budgets), 8 experiment tests, context check and
production build. The generators then added two features and an experiment wired
into a page, and verification passed again. The app was deleted.

Not verified: a real feature built with it, an existing app extended by it, CI
on GitHub, and the Settings component in a browser.
