# Engineering decisions

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
