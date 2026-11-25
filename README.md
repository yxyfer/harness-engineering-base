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
- **Cheap orientation.** A context map generated per checkout (areas, where to
  start, status by state and age, files and exports), loaded at session start in
  Claude Code, a contract that routes reads, and token budgets.
- **Measurement and upkeep.** `npm run bench` measures steps and tokens on fixed
  tasks; `npm run harness:diff -- <app>` shows which kit changes an app can
  take.
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

- Templates and a one-off scaffold, no sync engine; a read-only drift report
  shows what to merge.
  [Decision](docs/DECISIONS.md#a-scaffold-for-new-applications).
- Layered layout and tester-first experiments.
  [Decisions](docs/DECISIONS.md#layered-source-and-tester-first-experiments).
- Plans are documents beside the code; the numbered kit plan was retired.
  [Decision](docs/DECISIONS.md#plans-are-documents-beside-the-code).
- Context is generated per checkout, routed, and measured.
  [Decision](docs/DECISIONS.md#context-is-generated-per-checkout-and-measured).

## Open work

- **Waiting on the owner:** push the pilot. An existing application was moved
  onto the template locally and passes its own verification; this session had no
  push access to it. Outcome: its pull request merged after review, with
  `EXPERIMENT_TESTERS` set in its deployments.
- **Next:** prove `new-app` on a new feature from Explore to Build. Outcome: a
  feature built as an experiment, promoted, and the experiment removed cleanly.
  Proof: the app's `npm run verify`, a browser journey, and a benchmark run.
- **Next:** isolated environments for experiments that write data. Outcome: a
  recorded recipe for a worktree, a disposable or branched database and preview
  variables, with cleanup verified. Depends on a test database and preview
  project. Proof: create, write, discard and recreate, with the parent checkout
  and database untouched.
- **Next:** fewer steps when locating a defect. In the pilot, bug hunting got
  worse (8 to 9 steps, input up 24%) while planning and build orientation
  improved. Outcome: a change that helps that task; proof: `npm run bench` with
  at least three runs per task.
- **To decide:** the token budgets (2,500 per README, 5,000 for the
  architecture) were chosen without data; the pilot needed 4,500 temporarily for
  seven READMEs.

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

Pilot on an existing application (about 300 source files), 2026-11-25: moved
onto the template with production behaviour unchanged. Its own checks pass:
version gate, format, lint with generated zones, types, 35 self-tests (11
forbidden imports rejected, documents), 555 application tests including 3 new
tester tests, context and build. Benchmark, one run per task before and after
(directional): total input across four tasks fell 10% (1,297k to 1,172k);
planning fell 28% and build orientation 30%, each with two fewer steps; status
fell 5%; locating a defect rose 24%. `AGENTS.md` fell from about 4,700 to 1,600
tokens.

Not verified: a real feature built with it, an existing app extended by it, CI
on GitHub, and the Settings component in a browser.
