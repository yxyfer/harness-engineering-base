# TASK-011: Bind complete verification to native evidence

- **Status:** complete locally
- **Owner:** repository owner
- **Related plan:** `project/plans/P002-quality-first-harness/README.md`, Step
  08 only

## Outcome

Thin verify coordination produces validated, input-bound machine evidence and
a short summary without replacing native controls or inventing test counts.

## Acceptance criteria

- Native success/failure, zero tests, missing/malformed evidence, skips and
  retry events have honest states and blocking exits where required.
- Partial selection cannot claim complete verification; unsupported controls
  remain unavailable. Source/config/locks/untracked inputs identify each run.
- Stale reports and mid-run edits fail; report output does not hash itself.
- Bounded redacted logs and owned process-group cleanup work on timeout/SIGINT.
- Native fixture smoke, check, both contract suites and verify are exercised.

## Boundaries

No security scanner, installer, framework foundation, scheduler, retries or
remote publication. Existing commands/managers remain authoritative. Custom
test runners need an explicit native report adapter; no output scraping.

## Evidence and cohesion

[QH-08](QH-08.md) records 22 evidence regressions, native
fixture runs and 129-case contract suites. Size prompts remain advisory:
linear coordination and one temporary-fixture family stay cohesive; process,
identity and native/schema parsing are separate. TD-002 tracks further growth.
