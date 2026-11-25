# Engineering decisions

Newest first. Read by heading.

## Generated context and token budgets

Date: 2026-11-25. Status: Accepted for the template; turn count is open work.

Asked to cut the tokens a new session spends rebuilding context. Measured on a
real application of about 300 source files, one run per task (directional, not
statistical): every session starts near 64k tokens of system prompt and tools
before reading anything, and every step re-sends the whole conversation, so
steps multiply cost. The application's contract required about 43k tokens of
reading before a source edit, 33k of it one architecture file kept as a dated
change log that repeated the feature documents.

A generated map (areas, status, routes; about 2k tokens), on-demand status and
file indexes, and a contract that routes reads cut context growth by 24% on a
status question and 46% on a build task (148k to 110k peak), with equal or
better answers. Sessions took more steps on three of four tasks, so total input
was roughly flat. Choices:

- Generate the map from READMEs and code, checked in CI, rather than keep a
  hand-written index: hand indexes drift, a generated one cannot.
- The contract routes reads by task. Architecture and decisions are read by
  heading, never whole.
- Documents are present tense with token budgets enforced by a self-test;
  history lives in Git.
- Open items carry a state so status can be rolled up; the measured application
  had 109 open items across 25 documents, 18 with no state.
- Rejected: a hand-written session status file overwritten each session. It goes
  stale silently and duplicates the README open work it would summarise.

Recovery: delete `context/` and the `context` scripts; the READMEs are
unchanged.

## A scaffold for new applications

Date: 2026-11-25. Status: Accepted user request. Supersedes the "no installer"
part of
[Kit without a permanent application](#kit-without-a-permanent-application).

`npm run new-app -- <directory>` creates a Next.js app with `create-next-app` or
adds the layout to an existing app. It is a one-off copy with no sync: the app
records the kit revision in `.harness/UPSTREAM.md` and merges later changes by
hand. It never overwrites a file in an existing app and installs nothing there.
CI is part of the template, not of the kit. Generators in the app
(`new-feature`, `new-experiment`) create folders, READMEs and registrations, and
refuse to overwrite. The template targets Next.js only; another stack gets its
own template when a real project needs one.

## Layered source and tester-first experiments

Date: 2026-11-25. Status: Accepted user request.

Applications use six areas,
`app → experimental → features → components → core → config`, with dependencies
pointing down, checked by lint on resolved paths and proven by a self-test with
eleven forbidden imports. Feature dependencies live in
`src/config/features.json`, which a script can edit safely and a self-test
checks for cycles. Code is placed by evidence: platform pieces start in `core`,
a capability a person would name becomes a feature, anything unproven, billed or
new starts as an experiment.

An experiment has a stage instead of a public opt-in flag. `testers` is the
default for a new one: on by default for testers, invisible to others.
`everyone` adds opt-in for all; `off` is the kill switch. Only explicit choices
are stored, so changing a stage moves everyone who has not chosen. Testers come
from `EXPERIMENT_TESTERS` and, when unset, everyone is a tester under
`next dev`, so local work needs no configuration. Rejected: a stored true or
false per person with a missing choice meaning off; it forced a manual opt-in
for every trial. A `billed` experiment is never on by default. Risk accepted:
testers run experiments on real data, so each experiment's "Turning it off"
states what happens to data it wrote.

## Plans are documents beside the code

Date: 2026-11-25. Status: Accepted user request.

The plan is a tree of `README.md` files mirroring `src/`, in the format of
`project/FORMAT.md`; there are no numbered plans. A parent links its children
and never repeats their status. The kit's own P001 was retired: its finished
tasks are in Git (`git show 40bdd08:project/plans/P001-lean-harness.md`), its
open work moved to the kit README. The environment isolation task stays open,
narrowed to worktrees, databases and preview variables: experiments in the
source tree do not isolate data.

## Native commands for the quality baseline

Date: 2026-10-07. Scope: P001-T002. Status: Historical implementation; the kit
layout is superseded by the removal decision below. Native tools remain the
accepted approach.

Use native npm scripts and tool configuration. The kit and small Next.js
reference app have separate locks and dependency directories, with root scripts
delegating through `npm --prefix`. This keeps the app's lint peer dependencies
separate from the kit's supported lint tools. The kit root declares development
tools; the reference app owns framework dependencies. The initial framework
versions came from Data Miner; its Node test runner was reused without changing
that application. The latest stable policy below now owns framework selection.

The reset removed the old command implementation. Recreating a `harness`
dispatcher, TOML command schema or project sync engine adds no evidence to this
task. Use the native commands directly and maintain the small plan index by
hand. An installer, CI and consumer migration are outside this task.

Use ESLint 10.12.0 for kit JavaScript. The validation app used ESLint 9.39.5
because `eslint-config-next` 16.4.0 resolves `eslint-plugin-react` 7.37.5, whose
declared peer range excludes ESLint 10. ESLint 9 is
[out of maintenance](https://eslint.org/version-support/). Record this in
`project/debt.md`; do not use forced peer installation or disable React rules.
Recheck compatibility before adopting this reference for production.

SQL guidance is part of the baseline, but the database and migration tool must
be selected against the actual connection workflow in P001-T003. Installing a
tool now would add an untested dependency to a reference app with no database.

## Latest stable framework releases

Date: 2026-10-07. Scope: P001-T002 follow-up. Status: Accepted user requirement.

Use npm's `latest` releases for Next.js, React, React DOM and the matching Next
lint config. Accept exact stable versions only. Pin and lock the verified
versions rather than leaving installation to a moving `latest` string. The
receiving app's setup and full verification must invoke the checker with an
explicit app directory. It queries the public registry and fails for outdated
pins, lock or installation drift, prerelease metadata, or unavailable evidence.
Local application quality checks remain available for offline iteration.

The checker reports required upgrades without performing them. Every upgrade,
including a new major, needs strict peer installation, version-matched docs,
native checks and relevant behaviour and browser evidence. Consumer apps must
adopt the check in their own command entrypoints; kit checks do not validate an
application when no target is supplied. There is no background updater or CI
workflow.

## Kit without a permanent application

Date: 2026-10-07. Scope: P001-T002 cleanup. Status: Accepted user request.

Remove the validation app, its dependency lock and installed Next.js runtime.
Its initial proof is retained as historical task evidence. Keep the verified
ESLint and TypeScript settings as native adoption templates, alongside the
standards, kit formatter and JavaScript linter, version checker and small tests.
Kit setup installs only kit tools. App dev, types, build and smoke commands are
owned by the receiving application.

The version checker takes a required app directory and never silently checks a
demo or skips an unknown target. It is run as part of an app's full
verification, while the kit's own checks and tests run locally without Next.js
or React. Temporary package metadata fixtures protect the version policy; kit
failure probes use only kit configurations. They do not replace real application
proof.

Preserve an archive of the uncommitted validation source and lock before
removing it. Consumer-owned configuration, external projects, Git history and
database resources are outside this change.

## Source backed architecture views

Date: 2026-10-08. Scope: P001-T004. Status: Accepted. The user confirmed the
example views are clear; this is qualitative feedback, not a timed benchmark.

Keep the kit overview in `docs/ARCHITECTURE.md`. Demonstrate the format on a
read-only Data Miner source walkthrough, and ship one Markdown adoption
template. Use small Mermaid diagrams for system responsibilities, a feature from
input to result, and the effect of the change. Keep source owners and
verification limits beside each view. An import graph does not replace these
explanations.

Receiving applications keep their own canonical architecture context and update
affected views with boundary changes. Minor experiments can reuse the overview
and explain the delta briefly. No new runtime, scanner, dashboard or automatic
diagram extraction is introduced. Rendering uses temporary tools without adding
a dependency to this kit. Source and rendering checks establish correspondence;
reader feedback establishes comprehension. Recovery is a documentation revert.
