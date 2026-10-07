# TASK-016: Measurable reference UI quality

- **Status:** active; implementation verified, human baseline acceptance pending
- **Owner:** repository maintainer
- **Related plan:** `project/plans/P002-quality-first-harness/README.md`, Step
  13 only

## Outcome

Native production-browser evidence protects accessible interaction, reflow,
appearance and measured lab costs without inventing human design acceptance.

## Context to read

AGENTS, canonical design/quality/security context, Step 13, QH-12 and the
project-owned Next.js browser fixtures and disposable database runner.

## Constraints and non-goals

Chromium/macOS, 390×1000 and 1440×1000, Paper and Ink. Firefox/WebKit are
unverified, not supported claims. No AI grading, automatic baseline acceptance,
production access, installer work or Step 14. Preserve preceding dirty work.

## Acceptance criteria

- [x] Axe scans and explicit keyboard/focus checks cover the matrix and states.
- [x] Pinned candidate screenshots remain distinct from human-approved images.
- [x] Native comparisons require reviewed approval and never update snapshots.
- [x] Actual bundle and navigation measurements justify proposed lab budgets.
- [x] Disposable label/focus/overflow/appearance/budget defects fail native
      gates.
- [x] Native JUnit feeds verify; pending approval blocks full completeness.
- [x] Required checks, smoke, context and QH-13 record evidence and limits.
- [ ] Human accepts the 44 candidates; full native visual cases compare cleanly.

## Verification

Use project-local Playwright/axe, production build, synthetic SQLite, external
macOS isolation, native static/Vitest checks and harness contracts. Preserve
failed JUnit, screenshots and bounded logs; clean up owned runtime resources.

## Handoff

See `project/plans/P002-quality-first-harness/evidence/QH-13.md` and the
generated app candidate index. Source remains
unchanged by negative controls. No accepted screenshots/approval record exist.
Step 14 may proceed independently with authorization; it is not implemented.
