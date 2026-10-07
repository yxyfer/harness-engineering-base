# P001-T003 — Establish an enforceable engineering baseline

- **ID:** P001-T003
- **Plan:** P001
- **Status:** complete
- **Depends on:** P001-T002
- **Evidence:** ../evidence/PHASE_3_ENGINEERING_STANDARDS.md

## Outcome

Projects receive a concise shared engineering baseline, idiomatic language
profiles, and executable checks that select only the standards relevant to the
project.

## Implementation

[Implementation map](../../../architecture/README.md) · [Original
task](../evidence/legacy-TASK-003-ENGINEERING-STANDARDS.md)

## Acceptance

- [x] Shared standards cover implementation, naming, testing, and architecture.
- [x] Python, TypeScript/JavaScript, shell, and Markdown profiles are explicit.
- [x] `./harness check` detects relevant profiles and uses configured tools when
      available.
- [x] One check command reports formatter drift consistently.
- [x] Size warnings include their threshold and the route for an exception.
- [x] Generated, vendored, dependency, migration, schema, and fixture paths are
      explicitly excluded from generic size analysis.
- [x] Fixture tool configuration agrees with the shared 80-character limit.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
