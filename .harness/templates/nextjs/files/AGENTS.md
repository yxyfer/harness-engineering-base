# {{name}} engineering contract

{{name}} is a Next.js application. `CLAUDE.md` imports this file; edit this one
only. This file is a router: read what the task needs, not everything.

## Start here

1. [`context/README.md`](context/README.md): the generated map of every area,
   what it is for, where to start, what is open and the entry points. Read it
   instead of exploring the tree. `context/` is generated, not committed: Claude
   Code loads the map at session start (`.claude/settings.json`); otherwise run
   `npm run context` first if it is missing.
2. The `README.md` of the area you will touch, linked from the map, and the
   files its "Start with" line names: how it works, why, and what is open.
3. To find a file or a name, search [`context/files.md`](context/files.md)
   before searching `src/`. For "where are we", read
   [`context/status.md`](context/status.md).
4. Before a source edit: the four short standards in `.harness/standards/` and
   the relevant profile in `.harness/standards/languages/`.

Read more only when the task matches:

| When the task…                                 | Read                                                     |
| ---------------------------------------------- | -------------------------------------------------------- |
| adds a feature or part                         | [src/features/README.md](src/features/README.md)         |
| adds, opens, promotes or retires an experiment | [src/experimental/README.md](src/experimental/README.md) |
| records open work, a choice or a decision      | [docs/FORMAT.md](docs/FORMAT.md)                         |
| moves state, write ownership or an integration | the matching section of `docs/ARCHITECTURE.md`           |
| is a release, or changes how work is done      | [docs/WORKFLOW.md](docs/WORKFLOW.md)                     |

Never read `docs/ARCHITECTURE.md` or `docs/DECISIONS.md` whole: list their
headings and read the section you need. Batch independent reads and searches
into one step; every extra step re-sends the whole conversation.

The user's current request comes first. State Explore, Build or Release in a
line, inspect existing owners, preserve unrelated changes and define the
evidence before editing. Stop at a consequential ambiguity.

## Code layout

`src/` has six areas. Dependencies point down only, and `npm run lint` rejects
anything else on resolved paths (`eslint.boundaries.mjs`).

| Path                    | Holds                                                   | May import                                                  |
| ----------------------- | ------------------------------------------------------- | ----------------------------------------------------------- |
| `src/app/`              | Routes, layouts, Server Actions: the wiring per request | Everything; an experiment only via `index` or `server`      |
| `src/experimental/<x>/` | One experiment, off by default, removable               | Features, shared UI, core, config; never another experiment |
| `src/features/<x>/`     | Stable capabilities a person would name                 | Features listed in `src/config/features.json`, below        |
| `src/components/`       | Shared UI with no product knowledge                     | Shared UI, core, config                                     |
| `src/core/`             | Platform with no product rule                           | Core, config                                                |
| `src/config/`           | Plain registries                                        | Nothing in `src/`                                           |

Where new code goes is decided by evidence, not age. Start in `core` and
`src/app`; the first capability a person would name becomes a feature
(`npm run new-feature`). Anything unproven, billed, or built in the last few
days starts as an experiment (`npm run new-experiment`) with a stable fallback.
Features and experiments may import Server Action modules (`actions.ts`,
`*-actions.ts`) from `src/app`, nothing else there. `internal/` folders are
private to their feature.

## Plans are the documents beside the code

There are no numbered plans. Each feature, part and experiment has one
`README.md` describing the present: what it does, how, why, open work and
evidence. Plan work under "Open work" of the area it changes, in the same pull
request as the code; delete an item when it is done, since Git keeps history.
Work across features goes in `src/README.md`. Durable decisions go in
`docs/DECISIONS.md`; constraints nobody is working on in `docs/debt.md`.

Keep these documents cheap to read: present tense, no change logs, within the
budgets `npm run self-test` enforces. Keep each README's "Start with" line
pointing at the two or three files a newcomer should open first. After changing
code or a README, run `npm run context` to refresh your own map.

## Commands

```sh
npm run setup
npm run check
npm run self-test
npm test
npm run context
npm run verify
```

A nonzero exit is a failure: fix the cause, never weaken the gate. Keep exact
stable Next.js, React and React DOM pins (`npm run check:versions -- .`). Run
the relevant browser journey for behaviour changes and keep local, preview and
production evidence apart.

Ask before destructive changes, external publication, production access,
consequential security trade-offs or irreversible migrations. At completion
report the result, actual verification, remaining limits and recovery.
