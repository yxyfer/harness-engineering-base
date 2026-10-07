# P001-T002 — Add the versioned harness configuration contract

- **ID:** P001-T002
- **Plan:** P001
- **Status:** complete
- **Depends on:** P001-T001
- **Evidence:** ../evidence/PHASE_2_VERSIONED_CONFIGURATION.md

## Outcome

Give the harness one offline, machine-readable contract for its version,
configuration, managed files, command precedence, and exit behaviour. Make the
effective configuration and its source visible without editing harness scripts.

## Implementation

[Implementation map](../../../architecture/README.md) · [Original
task](../evidence/legacy-TASK-002-VERSIONED-CONFIGURATION.md)

## Acceptance

- [x] `.harness/VERSION` contains a semantic version.
- [x] `.harness/config.toml` implements the documented schema.
- [x] `.harness/manifest.json` records schema/version identity and managed-file
  checksums without absolute paths.
- [x] Unknown keys and invalid values fail with file, key, and expectation.
- [x] Command precedence is CLI, environment, project config, language-profile
  default, then automatic detection.
- [x] `./harness inspect` reports effective configuration and sources.
- [x] Project commands can be configured without editing harness scripts.
- [x] Stable exit meanings are documented and implemented at harness boundaries.
- [x] Managed and project-owned file boundaries are documented.
- [x] Unit, fixture, documentation, and smoke verification pass.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
