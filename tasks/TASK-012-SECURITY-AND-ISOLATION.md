# TASK-012: Executable security controls and isolated verification

- **Status:** complete locally; security approval blocked by retained findings
- **Owner:** repository owner
- **Related plan:** `plans/active/QUALITY_FIRST_HARNESS.md`, Step 09 only

## Outcome

Run maintained secret/source scanners and offline locked-dependency advisory
checks. Required findings, scanner errors and missing/stale data cannot pass.
Run opted-in application verification with a clean synthetic environment under
the external macOS process sandbox, never a URL filter presented as isolation.

## Acceptance criteria

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

## Constraints and verification

No installer, app foundation, remote changes, auto-fixes, blanket exclusions or
security certification. macOS sandbox-exec is deprecated and may be unavailable;
failure must remain visible. Tests use temporary synthetic inputs and TEST-NET
addresses, never real model-provider or production requests. Record exact
evidence and environment limits in `verification/QH-09.md`.

## Cohesion review

Size warnings remain advisory. Coordination keeps four fixed controls, two
native language adapters and two advisory formats, not a generic policy DSL.
Long branches keep native argv, error/data states and sanitization inspectable
together. Tests group boundary cases. No size suppression/hard gate is added.
CI launch code stays authoring-owned, not shipped consumer machinery.

The owner approved the exact existing architecture-check formatting edit.
The authoritative formatter restored canonical 80-column layout (HEAD bytes).
No other consumer change is absorbed.
