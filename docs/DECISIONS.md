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

### ADR-004: Separate application runner selection from harness self-testing

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 02
- **Context:** F1 hid app failures behind shipped tests; F2 silently removed
  pytest cases when that runner was absent. A repository-only test command also
  leaked to external targets through the old shared-default config path.
- **Decision:** `test` resolves CLI/environment/config commands, then package
  scripts or Python runner metadata. `[tool.harness.tests]` declares pytest or
  unittest; the Python convention is pytest without runner substitution. Prefer
  the target's local environment and reject zero supported Python collection.
  `self-test` selects the executing kit's suite independently. Managed defaults
  are separate from project-owned configuration; the schema stays version 1.
  This repository configures its own direct suite invocation without recursion.
- **Consequences:** Implicit unittest fallback is removed. Consumers declare
  unittest or retain an explicit native command, and replace the starter's
  repository-only test command. Harness regression setup requires pinned pytest;
  offline test execution never installs or silently skips it. Arbitrary native
  scripts own their exits/collection until broader evidence enforcement arrives.
- **Evidence:** [TASK-005](../tasks/TASK-005-APPLICATION-TEST-ROUTING.md),
  [QH-02](../verification/QH-02.md), installed-copy runner regressions.
- **Supersedes:** ADR-001's use of the project config as the external fallback;
  its schema and ownership rules remain in force.

### ADR-005: Share harness discovery and resolve static checks once

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 03
- **Context:** F3 sent executable Python to shell tools, F4 gave scans different
  exclusions, and F5 added Python checking after explicit project delegation.
- **Decision:** Share a small directory walker and suffix/shebang classifier.
  Bare directory names match at any depth; relative prefixes match from the
  root. Prune excluded trees and skip all file/directory symlinks. Canonical
  policy inputs reject symlink components independently. Required policies run
  before one resolved static implementation: CLI/environment/config override,
  package check, package lint/typecheck pair, then automatic Python checking.
  Native tools retain their own scope and configuration.
- **Consequences:** Unknown extensionless interpreters need native coverage;
  internal symlink sources are omitted by harness scans. Existing native
  configurations are unchanged. Exclusions cannot remove mandatory canonical
  policy requirements. Syntax fallback remains degraded coverage, not lint or
  type verification. The walker is not a runtime sandbox or a concurrent
  filesystem mutation defence. Managed ownership repair remains Step 04.
- **Evidence:** [TASK-006](../tasks/TASK-006-DISCOVERY-AND-CHECK-PRECEDENCE.md),
  [QH-03](../verification/QH-03.md), installed-copy discovery regressions.
- **Supersedes:** ADR-002's generic analysis description with explicit directory
  semantics; native configuration authority remains in force.

### ADR-006: Declare release ownership by exact shipped paths

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 04
- **Context:** F6/F7 treated additions under shared folders as shipped content,
  breaking health checks after project skills or real virtual environments.
- **Decision:** Check an explicit `.harness/release-files.json` list against
  the manifest's exact path set and shipped checksums. Include the inventory's
  checksum. Validate canonical paths/JSON keys and reject links in shipped
  destinations and metadata before opening or hashing files. Generate release
  metadata from only those reviewed inputs to stdout with `generate-release`.
- **Consequences:** Shared folders allow project additions and environments.
  Modified/missing shipped files remain conflicts. Schema 1/version `0.1.0`
  stay unchanged; older kits need an explicit reviewed verifier/inventory
  update. Legacy `generate` exits 2. Metadata is not signed or race-proof.
- **Evidence:** [TASK-007](../tasks/TASK-007-RELEASE-OWNERSHIP.md),
  [QH-04](../verification/QH-04.md), installed-copy ownership regressions.
- **Supersedes:** Broad managed-folder descriptions in ADR-001 and the previous
  roadmap. Project/native configuration ownership remains unchanged.

## Decision template

### ADR-000: Short title

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | superseded
- **Context:** What durable problem or constraint requires a choice?
- **Decision:** What was chosen?
- **Consequences:** What becomes easier, harder, or constrained?
- **Evidence:** Links to relevant plans, code, research, or tests.
- **Supersedes:** ADR-NNN or none.
