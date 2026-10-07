# P002-T012 — Prove production user and recovery journeys

- **ID:** P002-T012
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T011
- **Evidence:** ../evidence/QH-12.md

## Outcome

Production Chromium journeys prove real local sessions, authorized edits and
durable SQLite outcomes. Native results feed verify; no operation is mocked.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-015-USER-JOURNEYS.md) · [Step
instructions](../evidence/instructions/12-prove-complete-user-and-recovery-journeys.md)

## Acceptance

- [x] List/detail and save/reload pass with storage and audit assertions.
- [x] Validation, cancellation and repeated confirmation preserve correct data.
- [x] Anonymous, viewer, wrong-owner and wrong-tenant access are denied.
- [x] A real audit dependency failure rolls back, preserves draft and recovers.
- [x] Unexpected console/page errors fail; deliberate HTTP negatives are narrow.
- [x] Owned servers and uniquely allocated storage are cleaned on exit.
- [x] Small smoke and full native journey evidence are distinct and
      reproducible.
- [x] Disposable no-op save and authorization mutants fail intended assertions.
- [x] Required checks and QH-12 record actual results and limits.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
