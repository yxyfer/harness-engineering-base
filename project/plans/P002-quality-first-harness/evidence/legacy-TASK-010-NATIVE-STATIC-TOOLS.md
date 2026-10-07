# TASK-010: Delegate formatting and enforce static checks

- **Status:** complete locally
- **Owner:** repository owner
- **Related plan:** Step 07 of
  `project/plans/P002-quality-first-harness/README.md`

## Outcome

Format delegates to native project tools; check never requests autofixes and
fails missing required defaults. Explicit equivalent project commands retain
precedence and own their coverage. New opt-in native templates provide strict
types and concrete domain/I/O and client/server import rules.

## Acceptance criteria

- [x] Formatting is idempotent and check mode preserves maintained bytes.
- [x] Missing required tools fail, including isolated no-pip environments.
- [x] Existing commands/package managers/native settings retain authority.
- [x] Actual seeded type, lint, runtime-boundary and import failures are caught.
- [x] Maintained application source is included; size guidance stays advisory.
- [x] Native gates, both suites and fixture smoke pass with retained evidence.

## Constraints and verification

No installer, generic lint parser, security/browser engine or Step 08 verify.
Use native rules and temporary synthetic projects. Review release inventory and
checksums only for authoring inputs. Preserve consumer conflicts and context.
