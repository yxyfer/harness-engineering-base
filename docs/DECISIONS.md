# Decision Log

Keep accepted decisions append-only. Supersede an old decision with a new entry
rather than rewriting history.

## Accepted decisions

### ADR-001: Use versioned TOML configuration and a checksum manifest

- **Date:** 2026-09-08
- **Status:** accepted
- **Context:** The harness needs deterministic project overrides, offline version
  identity, strict validation, and a future-safe way to distinguish managed files
  from project-owned context during installation and updates.
- **Decision:** Store the semantic harness version in `.harness/VERSION`, use a
  complete schema-versioned `.harness/config.toml`, and record relative managed
  file paths with SHA-256 checksums in `.harness/manifest.json`. Configuration is
  project-owned after creation and is excluded from managed-file checksums.
- **Consequences:** Configuration requires Python 3.11 or newer for standard
  library TOML parsing. Unknown and missing keys fail early. Future updates can
  detect managed-file drift without treating normal project configuration as
  corruption.
- **Evidence:** `tasks/TASK-002-VERSIONED-CONFIGURATION.md`,
  `verification/PHASE_2_VERSIONED_CONFIGURATION.md`, and the Phase 2 contract
  tests under `.harness/tests/`.
- **Supersedes:** none.

## Decision template

### ADR-000: Short title

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | superseded
- **Context:** What durable problem or constraint requires a choice?
- **Decision:** What was chosen?
- **Consequences:** What becomes easier, harder, or constrained?
- **Evidence:** Links to relevant plans, code, research, or tests.
- **Supersedes:** ADR-NNN or none.
