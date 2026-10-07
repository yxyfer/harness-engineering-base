# Task index

Read one task for its outcome, acceptance and reviewer brief. The
[roadmap](../../../../plans/P002-quality-first-harness/README.md) owns
sequencing and future steps; reports own the actual commands/results. Task IDs
and paths stay stable.

## Open work

| Task | State / limit | Evidence |
| --- | --- | --- |
| [016: Measurable reference UI quality](../../../../plans/P002-quality-first-harness/tasks/P002-T013-ui-quality.md) | active; implementation verified, human baseline acceptance pending | [QH-13](../../../../plans/P002-quality-first-harness/evidence/QH-13.md) |

## Delivered locally

| Task | State / limit | Evidence |
| --- | --- | --- |
| [017: Make work and implementation easy to review](../../../P003-reviewable-work/tasks/P003-T001-reviewable-work.md) | complete locally | [Report](../../../P003-reviewable-work/evidence/REVIEWABLE_WORK.md) |
| [004: Current baseline and independent acceptance cases](../../../../plans/P002-quality-first-harness/tasks/P002-T001-quality-baseline.md) | complete | [QH-01](../../../../plans/P002-quality-first-harness/evidence/QH-01.md) |
| [005: Independent application tests and harness self-tests](../../../../plans/P002-quality-first-harness/tasks/P002-T002-application-test-routing.md) | complete | [QH-02](../../../../plans/P002-quality-first-harness/evidence/QH-02.md) |
| [006: Consistent discovery and static-check precedence](../../../../plans/P002-quality-first-harness/tasks/P002-T003-discovery-and-check-precedence.md) | complete | [QH-03](../../../../plans/P002-quality-first-harness/evidence/QH-03.md) |
| [007: Explicit release ownership preserves installation health](../../../../plans/P002-quality-first-harness/tasks/P002-T004-release-ownership.md) | complete | [QH-04](../../../../plans/P002-quality-first-harness/evidence/QH-04.md) |
| [008: Run repaired core checks in pinned macOS CI](../../../../plans/P002-quality-first-harness/tasks/P002-T005-core-ci.md) | complete locally; remote execution unverified | [QH-05](../../../../plans/P002-quality-first-harness/evidence/QH-05.md) |
| [009: Resolve applicable controls and readiness](../../../../plans/P002-quality-first-harness/tasks/P002-T006-profiles-and-doctor.md) | complete locally | [QH-06](../../../../plans/P002-quality-first-harness/evidence/QH-06.md) |
| [010: Delegate formatting and enforce static checks](../../../../plans/P002-quality-first-harness/tasks/P002-T007-native-static-tools.md) | complete locally | [QH-07](../../../../plans/P002-quality-first-harness/evidence/QH-07.md) |
| [011: Bind complete verification to native evidence](../../../../plans/P002-quality-first-harness/tasks/P002-T008-verification-evidence.md) | complete locally | [QH-08](../../../../plans/P002-quality-first-harness/evidence/QH-08.md) |
| [012: Executable security controls and isolated verification](../../../../plans/P002-quality-first-harness/tasks/P002-T009-security-and-isolation.md) | complete locally; security approval blocked by retained findings | [QH-09](../../../../plans/P002-quality-first-harness/evidence/QH-09.md) |
| [015: Prove production user and recovery journeys](../../../../plans/P002-quality-first-harness/tasks/P002-T012-user-journeys.md) | complete locally | [QH-12](../../../../plans/P002-quality-first-harness/evidence/QH-12.md) |

## Historical partial reports

| Task | State / limit | Evidence |
| --- | --- | --- |
| [013: Production-buildable synthetic Next.js foundation](../../../../plans/P002-quality-first-harness/tasks/P002-T010-nextjs-reference-app.md) | Historical partial; current journeys in QH-12 | [QH-10](../../../../plans/P002-quality-first-harness/evidence/QH-10.md) |
| [014: Persist authorized synthetic work-item edits](../../../../plans/P002-quality-first-harness/tasks/P002-T011-secure-persistence.md) | Historical partial; current journeys in QH-12 | [QH-11](../../../../plans/P002-quality-first-harness/evidence/QH-11.md) |

[QH-12](../../../../plans/P002-quality-first-harness/evidence/QH-12.md) records
renewed browser authorization and current journey evidence for Steps 10–11.
Their original partial reports and
unchecked historical criteria remain unchanged; they are not current browser
prohibitions. Human visual acceptance remains pending in TASK-016.

## Earlier foundation work

| Task | State / limit | Evidence |
| --- | --- | --- |
| [001: Adopt the three-layer harness structure](../../../P001-harness-foundation/tasks/P001-T001-three-layer-structure.md) | complete | [Phase 1](../../../P001-harness-foundation/evidence/PHASE_1_THREE_LAYER_STRUCTURE.md) |
| [002: Add the versioned harness configuration contract](../../../P001-harness-foundation/tasks/P001-T002-versioned-configuration.md) | complete | [Phase 2](../../../P001-harness-foundation/evidence/PHASE_2_VERSIONED_CONFIGURATION.md) |
| [003: Establish an enforceable engineering baseline](../../../P001-harness-foundation/tasks/P001-T003-engineering-standards.md) | complete | [Phase 3](../../../P001-harness-foundation/evidence/PHASE_3_ENGINEERING_STANDARDS.md) |

Create new work from the [task template](../../../../templates/task.md), using
the next free
ID. Keep the brief short and link architecture, choices and evidence. Update
this index and the coordinating plan when state changes. A local pass does not
establish remote CI, security approval or human acceptance.
