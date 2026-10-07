# P002-T008 — Bind complete verification to native evidence

- **ID:** P002-T008
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T007
- **Evidence:** ../evidence/QH-08.md

## Outcome

Thin verify coordination produces validated, input-bound machine evidence and a
short summary without replacing native controls or inventing test counts.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-011-VERIFICATION-EVIDENCE.md) · [Step
instructions](../evidence/instructions/08-make-complete-verification-produce-trustworthy-evidence.md)

## Acceptance

- [x] Native success/failure, zero tests, missing/malformed evidence, skips and
  retry events have honest states and blocking exits where required.
- [x] Partial selection cannot claim complete verification; unsupported controls
  remain unavailable. Source/config/locks/untracked inputs identify each run.
- [x] Stale reports and mid-run edits fail; report output does not hash itself.
- [x] Bounded redacted logs and owned process-group cleanup work on
      timeout/SIGINT.
- [x] Native fixture smoke, check, both contract suites and verify are
      exercised.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
