# P002-T004 — Explicit release ownership preserves installation health

- **ID:** P002-T004
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T003
- **Evidence:** ../evidence/QH-04.md

## Outcome

Project additions and generated environments coexist with shipped files.
Verification still exposes shipped-file modification, loss and unsafe paths.
Release generation selects only explicitly reviewed inputs.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-007-RELEASE-OWNERSHIP.md) · [Step
instructions](../evidence/instructions/04-preserve-managed-and-project-ownership.md)

## Acceptance

- [x] F6/F7 fail before the repair and pass afterwards in full disposable
      copies.
- [x] A project skill, additions under shared directories, a real no-pip fixture
  environment, dependencies and caches preserve verify/inspect success.
- [x] Modified/missing shipped files and incomplete/extra manifest entries fail;
  consumer files and manifest bytes remain unchanged.
- [x] Unsafe manifest/inventory paths, duplicate JSON keys, invalid release
  entries and symlink destinations/parents/metadata fail before hashing them.
- [x] Release output contains exactly intended paths, is deterministic with a
  fixed timestamp, ignores project/generated files and requires shipped inputs.
- [x] Both suites, required commands and fixture/native checks run with failures
  and missing tools preserved in QH-04.
- [x] Inventory changes are reviewed and canonical ownership/compatibility and
  the plan link the final evidence. Stop after Step 04.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
