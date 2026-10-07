# P002-T003 — Consistent discovery and static-check precedence

- **ID:** P002-T003
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T002
- **Evidence:** ../evidence/QH-03.md

## Outcome

Harness-owned scans inspect maintained files within the target, route supported
executable shebangs to their language, and honour directory exclusions. Required
policy gates precede one resolved project static-check implementation.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-006-DISCOVERY-AND-CHECK-PRECEDENCE.md) · [Step
instructions](../evidence/instructions/03-unify-discovery-and-honour-command-precedence.md)

## Acceptance

- [x] F3–F5 reproduce before the fix and pass behavioural regressions
      afterwards.
- [x] Direct/env/env `-S` Python shebangs receive Python analysis; supported
      shell
  shebangs reach shell tools with spaced paths intact. Unknown executables do
  not default to shell.
- [x] All harness-owned analysis scans use configured exclusions, prune before
  descent, retain similarly named siblings and stay inside the root.
- [x] Extensionless Python participates in degraded syntax validation.
- [x] CLI/environment/config precedence is preserved; selected commands run
  exactly once with no hidden Python stage. Package checks behave likewise.
- [x] A mandatory policy failure blocks project commands; native tool scope is
  unaffected by harness analysis exclusions.
- [x] Both suites and applicable fixture/native checks run; missing tools and
  failed attempts remain explicit in QH-03.
- [x] Only intended managed inputs enter the inventory; durable context and the
  active plan link this step's evidence.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
