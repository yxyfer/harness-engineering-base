# TASK-015: Prove production user and recovery journeys

- **Status:** complete locally
- **Owner:** repository owner / coding agent
- **Related plan:** `project/plans/P002-quality-first-harness/README.md`, Step
  12 only

## Outcome

Production Chromium journeys prove real local sessions, authorized edits and
durable SQLite outcomes. Native results feed verify; no operation is mocked.

## Acceptance criteria

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

## Constraints and non-goals

Use existing pinned tools and components. No production fault routes, SSO,
installer, accessibility/visual baselines, extra browser engines or Step 13.
Preserve the in-flight Step 11 changes and historical partial reports.

## Verification

Production build, native static/component/server tests, Playwright journeys and
smoke under external macOS isolation; shared verify and harness self-tests when
managed coordination changes. Faults use an actual SQLite audit trigger. Mutants
live only in owned disposable source copies, never the working application.

Evidence: [QH-12](QH-12.md). Full app verify has stable inputs,
14 direct-server, 25 application (including those server cases) and nine browser
cases. Both root harness suites pass 154 cases. No Step 13 work was started.
