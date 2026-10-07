# P002-T006 — Resolve applicable controls and readiness

- **ID:** P002-T006
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T005
- **Evidence:** ../evidence/QH-06.md

## Outcome

One shared resolution explains languages, Next.js, capabilities, context and
unsupported package scope. Doctor diagnoses prerequisites without installing,
rewriting configuration or claiming checks executed.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-009-PROFILES-AND-DOCTOR.md) · [Step
instructions](../evidence/instructions/06-resolve-relevant-profiles-and-prerequisites.md)

## Acceptance

- [x] Python, TypeScript and Next.js selection is independent of tool presence.
- [x] Reviewed requirements persist; conflicting detection blocks readiness.
- [x] Unknown/unimplemented capabilities and multi-package roots are visible
  failures, not silently omitted controls or invented coverage.
- [x] Missing tools, relevant context and required unfinished context fail
  doctor; irrelevant browser/design/data requirements are not imposed on CLI.
- [x] Schema 1 remains readable without mutation; schema 2 is a reviewable
  opt-in with explicit legacy readiness/security diagnostics.
- [x] Policies, inspection and doctor use the same resolver; native tools and
  both suites/fixture smoke are exercised, with evidence in QH-06.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
