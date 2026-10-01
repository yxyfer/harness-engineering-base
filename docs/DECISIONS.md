# Decision Log

Keep accepted decisions append-only. Supersede an old decision with a new entry
rather than rewriting history.

## Accepted decisions

### ADR-002: Use an 80-character, tool-enforced engineering baseline

- **Date:** 2026-09-08
- **Status:** accepted
- **Context:** Projects need consistent engineering expectations without
  replacing language idioms, duplicating mature linters, or turning heuristic
  size limits and slogans into brittle gates.
- **Decision:** Use an 80-character shared line width, 350-line file and 50-line
  function advisory thresholds, and four concise shared standards with Python,
  TypeScript/JavaScript, shell, and Markdown profiles. Project formatter,
  linter, type-checker, and test configuration is authoritative. TDD applies
  proportionately to defects, core behaviour, and risky refactors; DRY applies
  to demonstrated shared knowledge rather than coincidental syntax.
- **Consequences:** `./harness check` selects only relevant profiles and reports
  missing optional tools as degraded coverage. Size findings request cohesion
  review but do not fail. Scoped tool-native suppressions carry rationale until
  Phase 6 adds the governed exception register.
- **Evidence:** `tasks/TASK-003-ENGINEERING-STANDARDS.md`, the standards under
  `.harness/standards/`, Phase 3 contract tests, and
  `verification/PHASE_3_ENGINEERING_STANDARDS.md`.
- **Supersedes:** none.

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

### ADR-003: Prioritise application quality with programmatic verification

- **Date:** 2026-10-01
- **Status:** accepted direction; implementation pending
- **Context:** The audit found false-success paths and limited evidence that
  existing checks improve applications. The user prioritised safety and quality,
  UX, maintainable code, relevant controls, and customer consistency, and
  explicitly required testing without other AI calls.
- **Decision:** Keep a small project engineering harness with TypeScript and
  Python profiles, a Next.js framework profile, applicable capability controls,
  and reusable app foundations. All automated grading uses conventional tools
  and executable assertions. Separate human acceptance and runtime permissions.
  Repair gate reliability and prove real application journeys before expanding
  adoption/update infrastructure.
- **Consequences:** No LLM judge or secondary reviewer agent is a required test
  stage. Existing project tools and customer design systems remain authoritative.
  Shared UI behaviour can vary through customer themes. Missing verification
  cannot count as a pass. The detailed new-project tool choices are recommended
  defaults requiring compatibility tests, not imposed migrations.
- **Evidence:** User direction on 2026-10-01; [audit](../verification/AUDIT_2026_10_01.md);
  [product vision](PRODUCT.md); [delivery plan](../plans/active/QUALITY_FIRST_HARNESS.md).
- **Supersedes:** the remaining implementation order in Project Harness v2;
  ADR-001 and ADR-002 remain in force. Required-tool CI behaviour will replace
  degraded success only when implemented and verified.

## Decision template

### ADR-000: Short title

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | superseded
- **Context:** What durable problem or constraint requires a choice?
- **Decision:** What was chosen?
- **Consequences:** What becomes easier, harder, or constrained?
- **Evidence:** Links to relevant plans, code, research, or tests.
- **Supersedes:** ADR-NNN or none.
