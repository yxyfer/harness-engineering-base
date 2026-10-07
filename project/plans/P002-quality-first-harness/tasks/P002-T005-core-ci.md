# P002-T005 — Run repaired core checks in pinned macOS CI

- **ID:** P002-T005
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T004
- **Evidence:** ../evidence/QH-05.md

## Outcome

A bounded GitHub Actions workflow installs locked tools and runs actual shell,
Markdown, Python and TypeScript checks, repaired contract suites and fixtures.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-008-CORE-CI.md) · [Step
instructions](../evidence/instructions/05-add-ci-for-the-repaired-core.md)

## Acceptance

- [x] Runtime/action/tool versions are pinned; dependency installs are locked.
- [x] Missing required CI tools fail; native findings are fixed without blanket
  rule disables or silently shrinking the tested source scope.
- [x] Both core suites, fixture tests/smokes and negative controls execute.
- [x] Failures produce useful logs; negative cases use temporary data and leave
  the source tree healthy.
- [x] Local execution and remote execution are distinguished in QH-05.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
