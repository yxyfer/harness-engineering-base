# P002-T009 — Executable security controls and isolated verification

- **ID:** P002-T009
- **Plan:** P002
- **Status:** complete
- **Depends on:** P002-T008
- **Evidence:** ../evidence/QH-09.md

## Outcome

Run maintained secret/source scanners and offline locked-dependency advisory
checks. Required findings, scanner errors and missing/stale data cannot pass.
Run opted-in application verification with a clean synthetic environment under
the external macOS process sandbox, never a URL filter presented as isolation.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-012-SECURITY-AND-ISOLATION.md) · [Step
instructions](../evidence/instructions/09-add-executable-security-checks-and-test-isolation.md)

## Acceptance

- [x] Native secret, Python/JavaScript source and dependency findings fail;
  safe cases pass; scanner failures and absent/malformed data are unavailable.
- [x] Exact finding exceptions require owner, reason and future expiry;
  expired exceptions fail and never suppress scanner errors.
- [x] Advisory setup records source/time, scanner version and lock identity;
  verification performs no advisory downloads and rejects stale identities.
- [x] Synthetic environment excludes inherited credentials and provider flags.
  Direct non-loopback sockets and child attempts fail with permission denial;
  necessary loopback services work under the actual external macOS sandbox.
- [x] Reports contain identifiers/locations, not secret values/source snippets.
- [x] Existing schemas remain readable; explicit side-file opt-in does not
  replace project-owned configs. Unsupported capability controls stay required.
- [x] Required native checks, tests, self-tests, fixture smoke and verify run.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
