# TASK-007: Explicit release ownership preserves installation health

- **Status:** complete
- **Owner:** repository owner
- **Related plan:** [Step 04](../plans/active/QUALITY_FIRST_HARNESS.md)

## Outcome

Project additions and generated environments coexist with shipped files.
Verification still exposes shipped-file modification, loss and unsafe paths.
Release generation selects only explicitly reviewed inputs.

## Context to read

- `AGENTS.md`, canonical context and accepted decisions.
- Step 04 and F6/F7 in `verification/AUDIT_2026_10_01.md`.
- Manifest generation/verification, inspection and installation contract tests.

## Constraints and non-goals

- Preserve Step 01–03 work and project-owned content/configuration.
- No installer, updater, consumer migration, CI or new application features.
- No filesystem enumeration to infer release ownership.
- Manifest schema remains 1. New kits require the shipped release inventory;
  older copies need an explicit reviewed metadata/managed-file update.
- Generation is a release-authoring operation; it does not write consumer files.
  Do not regenerate away a consumer checksum conflict.
- Reject unsafe/noncanonical paths and any symlink in a shipped destination or
  metadata path. Unlisted project/environment symlinks are outside this check.
- These editable metadata/checks are not a tamper-proof security boundary.

## Acceptance criteria

- [x] F6/F7 fail before the repair and pass afterwards in full disposable copies.
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

## Verification

| Check | Method | Expected evidence |
| --- | --- | --- |
| Reproduction | Existing F6/F7 probe | Healthy 0, additions fail 5 before repair |
| Ownership | Full-copy subprocess regressions | Additions pass; shipped drift fails |
| Release boundary | Explicit generation and unsafe inputs | Exact paths and read-only failure |
| Release checks | Check/test/self-test, fixtures and native tools | Exits, collection, feedback and limitations |

## Notes and decisions

All customer content, caches and local-secret examples are synthetic. Runtime
environment creation uses stdlib venv without pip or network access.

See [QH-04](../verification/QH-04.md) for 15 focused cases, both full 61-case
suites, before/after probes, native checks and the remaining tool gaps.
