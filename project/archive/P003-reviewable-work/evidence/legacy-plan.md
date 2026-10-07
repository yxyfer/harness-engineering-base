# Plan: Make work and implementation easy to review

- **Status:** complete
- **Outcome:** A maintainer can find the next task and understand implementation
  choices without reading a long roadmap or the entire codebase.
- **Task:** [TASK-017](../tasks/P003-T001-reviewable-work.md)

## Scope

Shorten the roadmap, separate step instructions, index tasks, and add linked
architecture maps and reviewer briefs. Preserve existing acceptance criteria,
evidence, task IDs, and approval boundaries. No application/runtime changes or
execution of future quality-first steps.

## Verification and recovery

Run documentation/link checks, root check/test/self-test, and both fixture
smokes. Inspect moved links, guide completeness and managed checksum changes.
Changes are repository text; recovery is reverting this bounded diff.

## Completion

- [x] TASK-017 acceptance criteria are demonstrated.
- [x] Evidence and durable context are updated.
- [x] Plan moved to completed and work/task indexes refreshed.

Completed: 2026-10-07.

Report: [Verification](REVIEWABLE_WORK.md).
