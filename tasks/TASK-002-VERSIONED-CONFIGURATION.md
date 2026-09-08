# TASK-002: Add the versioned harness configuration contract

- **Status:** complete
- **Owner:** repository owner
- **Related plan:** `plans/active/PROJECT_HARNESS_V2.md`, Phase 2

## Outcome

Give the harness one offline, machine-readable contract for its version,
configuration, managed files, command precedence, and exit behaviour. Make the
effective configuration and its source visible without editing harness scripts.

## Context to read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/QUALITY.md`
- `docs/SECURITY.md`
- `docs/DECISIONS.md`
- `plans/active/PROJECT_HARNESS_V2.md`, Phase 2

## Constraints and non-goals

- Support macOS only in this phase.
- Use Python's standard library; add no third-party runtime dependency.
- Keep committed configuration free of secrets and machine-specific paths.
- Preserve automatic Node and Python detection.
- Do not implement standards enforcement, readiness, installers, adoption,
  exceptions, security scanning, CI, or updates from later phases.

## Acceptance criteria

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

## Verification

| Check | Command or method | Expected evidence |
| --- | --- | --- |
| Unit | `./harness test` | Configuration and manifest tests pass |
| Static | `./harness check` | Policy, syntax, and project checks pass |
| Configuration | `./harness inspect` | Values and sources are visible |
| Precedence | CLI, environment, config, and auto fixture runs | Highest available source wins |
| Integrity | Modify a temporary managed fixture | Manifest verification detects drift |
| Golden path | `./harness smoke` on both fixtures | Observable HTTP response succeeds |

## Notes and decisions

- `0.1.0` is the first formal harness version; the configuration schema starts
  at version `1`.
- TOML parsing requires Python 3.11 or newer because the harness uses the standard
  library `tomllib` parser.
- Language-profile command defaults are an explicit precedence slot. No Phase 2
  profile supplies a command; those defaults arrive with Phase 3 profiles.
- Full evidence is recorded in
  `verification/PHASE_2_VERSIONED_CONFIGURATION.md`.
