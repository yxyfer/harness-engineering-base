# P002-T007 — Delegate formatting and enforce static checks

- **ID:** P002-T007
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T006
- **Evidence:** ../evidence/QH-07.md

## Outcome

Format delegates to native project tools; check never requests autofixes and
fails missing required defaults. Explicit equivalent project commands retain
precedence and own their coverage. New opt-in native templates provide strict
types and concrete domain/I/O and client/server import rules.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-010-NATIVE-STATIC-TOOLS.md) · [Step
instructions](../evidence/instructions/07-delegate-formatting-and-static-quality-to-native-tools.md)

## Acceptance

- [x] Formatting is idempotent and check mode preserves maintained bytes.
- [x] Missing required tools fail, including isolated no-pip environments.
- [x] Existing commands/package managers/native settings retain authority.
- [x] Actual seeded type, lint, runtime-boundary and import failures are caught.
- [x] Maintained application source is included; size guidance stays advisory.
- [x] Native gates, both suites and fixture smoke pass with retained evidence.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
