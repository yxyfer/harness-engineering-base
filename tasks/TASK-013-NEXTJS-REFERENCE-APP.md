# TASK-013: Production-buildable synthetic Next.js foundation

- **Status:** partially verified; final browser evidence blocked by owner choice
- **Owner:** repository owner
- **Related plan:** `plans/active/QUALITY_FIRST_HARNESS.md`, Step 10 only

## Outcome

Build and run a real Next.js application outside managed kit internals. A user
can navigate synthetic work items, preview an edit and inspect shared components
in two themes. Persistence and authorization are explicitly not implemented.

## Acceptance criteria

- [x] Exact compatible pins, lockfile, native scripts and own harness config.
- [x] List/detail Server Components; small interactive Client Components.
- [x] One owned Radix/shadcn-style kit, semantic tokens and two shared themes.
- [x] Loading, empty, error, no-access and local-success examples are labelled.
- [x] Component validation, confirmation/cancel and theme interactions pass.
- [ ] Final current-kit production browser evidence: earlier build/navigation
  passed, but the owner stopped browser execution after diagnostic kit cleanup.
- [x] Source/dependency ownership, component reuse and design context recorded.
- [x] Existing Node dispatcher fixture is unchanged and still passes smoke.

## Constraints and verification

No installer, database, authentication, remote publication, full accessibility
certification or visual-baseline approval. Conventional programs grade tests;
human product/design acceptance remains separate. Use only local synthetic
services and record unavailable controls rather than changing requirements.
Use native Vitest JUnit and Playwright reports, actual production build,
harness commands and rendered evidence in `verification/QH-10.md`.

## Cohesion review and remaining evidence

The stylesheet keeps token themes, shared controls and responsive layout in one
entrypoint. Its 516 formatter-expanded lines exceed advisory guidance; this is
not suppressed or a hard gate. Extract by responsibility when a second consumer
or material styling change demonstrates a need. The editor is 103 lines with
local validation/draft/preview behavior, not a form/state framework.

The owner explicitly requested no further browser execution. Do not bypass the
in-app denial through native browser commands. Saved earlier screenshots and
navigation results remain historical evidence. Final non-browser verification
must remain partial; do not begin Step 11 or claim current complete verification.
