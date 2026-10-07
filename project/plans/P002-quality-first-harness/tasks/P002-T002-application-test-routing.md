# P002-T002 — Independent application tests and harness self-tests

- **ID:** P002-T002
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T001
- **Evidence:** ../evidence/QH-02.md

## Outcome

Application failures cannot be hidden by shipped harness tests or a silently
substituted runner. Both suites have independent commands and honest exits.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-005-APPLICATION-TEST-ROUTING.md) · [Step
instructions](../evidence/instructions/02-separate-application-tests-from-harness-tests.md)

## Acceptance

- [x] F1/F2 are reproduced before runtime edits and new regressions fail.
- [x] Installed harness plus failing app case fails; healthy app case collects.
- [x] Missing declared pytest fails with setup guidance; no unittest fallback.
- [x] Declared unittest and pytest use the target `.venv` when available.
- [x] Supported Python runners reject zero collected cases.
- [x] CLI > environment > config > package script > Python convention stays
      intact; explicit native commands remain usable.
- [x] `self-test` runs the executing kit's suite independently of app commands,
      app failure or an app environment; it cannot be redirected by overrides.
- [x] Root test command is deliberately configured without recursive routing.
- [x] Both suites, fixture checks/tests/smokes and native checks run; missing
      tools, failures, durations and source identity remain visible.
- [x] Only intended managed files change; inventory diff and compatibility are
      documented, evidence linked and no later step starts.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
