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
- **Evidence:**
  `project/archive/P001-harness-foundation/tasks/P001-T003-engineering-standards.md`,
  the standards under
  `.harness/standards/`, Phase 3 contract tests, and
  `project/archive/P001-harness-foundation/evidence/PHASE_3_ENGINEERING_STANDARDS.md`.
- **Supersedes:** none.

### ADR-001: Use versioned TOML configuration and a checksum manifest

- **Date:** 2026-09-08
- **Status:** accepted
- **Context:** The harness needs deterministic project overrides, offline
  version
  identity, strict validation, and a future-safe way to distinguish managed
  files
  from project-owned context during installation and updates.
- **Decision:** Store the semantic harness version in `.harness/VERSION`, use a
  complete schema-versioned `.harness/config.toml`, and record relative managed
  file paths with SHA-256 checksums in `.harness/manifest.json`. Configuration
  is
  project-owned after creation and is excluded from managed-file checksums.
- **Consequences:** Configuration requires Python 3.11 or newer for standard
  library TOML parsing. Unknown and missing keys fail early. Future updates can
  detect managed-file drift without treating normal project configuration as
  corruption.
- **Evidence:**
  `project/archive/P001-harness-foundation/tasks/P001-T002-versioned-configuration.md`,
  `project/archive/P001-harness-foundation/evidence/PHASE_2_VERSIONED_CONFIGURATION.md`,
  and the Phase 2 contract
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
  stage. Existing project tools and customer design systems remain
  authoritative.
  Shared UI behaviour can vary through customer themes. Missing verification
  cannot count as a pass. The detailed new-project tool choices are recommended
  defaults requiring compatibility tests, not imposed migrations.
- **Evidence:** User direction on 2026-10-01;
  [audit](../project/plans/P002-quality-first-harness/evidence/AUDIT_2026_10_01.md);
  [product vision](PRODUCT.md); [delivery
  plan](../project/plans/P002-quality-first-harness/README.md).
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
- **Evidence:**
  [TASK-005](../project/plans/P002-quality-first-harness/tasks/P002-T002-application-test-routing.md),
  [QH-02](../project/plans/P002-quality-first-harness/evidence/QH-02.md),
  installed-copy runner regressions.
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
- **Evidence:**
  [TASK-006](../project/plans/P002-quality-first-harness/tasks/P002-T003-discovery-and-check-precedence.md),
  [QH-03](../project/plans/P002-quality-first-harness/evidence/QH-03.md),
  installed-copy discovery regressions.
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
- **Evidence:**
  [TASK-007](../project/plans/P002-quality-first-harness/tasks/P002-T004-release-ownership.md),
  [QH-04](../project/plans/P002-quality-first-harness/evidence/QH-04.md),
  installed-copy ownership regressions.
- **Supersedes:** Broad managed-folder descriptions in ADR-001 and the previous
  roadmap. Project/native configuration ownership remains unchanged.

### ADR-007: Execute native core gates in pinned macOS CI

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 05
- **Context:** Warning-only optional tools did not establish native correctness;
  there was no existing CI provider configuration.
- **Decision:** Use a thin GitHub Actions macOS workflow with exact runtimes,
  SHA-pinned actions, hashed Python requirements, npm lockfiles and verified
  shell binary digests. Conventional programs run static checks, both contract
  commands, existing fixture tests/smokes and disposable negative controls.
- **Consequences:** Required CI tools fail when missing. Developer commands
  retain explicit degraded optional coverage. CI authoring files are not added
  to consumer release ownership. Fixture-native Markdown configs are shipped;
  dependency/runtime directories are excluded, not maintained sources. Local
  passes do not prove remote execution or branch protection.
- **Evidence:**
  [TASK-008](../project/plans/P002-quality-first-harness/tasks/P002-T005-core-ci.md),
  [QH-05](../project/plans/P002-quality-first-harness/evidence/QH-05.md), [CI
  guide](../.harness/ci/README.md).
- **Supersedes:** None; ownership and native configuration authority remain.

### ADR-008: Resolve applicability without rewriting reviewed requirements

- **Date:** 2026-10-01
- **Status:** accepted
- **Decision:** Share a small fixed resolver across check, policies, inspect and
  doctor. Preserve reviewed requirements, retain conflicting detected controls,
  fail unsupported capabilities/package aggregation and diagnose missing tools.
  Opt in to schema 2 through a reviewed side-file merge; retain schema 1 reads.
- **Consequences:** Doctor is prerequisite diagnosis, not quality verification.
  Next.js/browser/security assurance remains unsupported. Readiness flags now
  affect required unfinished context. No project-owned configuration
  replacement.
- **Evidence:**
  [TASK-009](../project/plans/P002-quality-first-harness/tasks/P002-T006-profiles-and-doctor.md),
  [QH-06](../project/plans/P002-quality-first-harness/evidence/QH-06.md).
- **Supersedes:** Earlier explicit-profile omission behaviour only; native tool
  authority and ownership remain unchanged.

### ADR-009: Native formatting and required static defaults

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 07
- **Decision:** Preserve one reviewed native implementation and project package
  managers. Add optional format config, require local default static tools and
  ship separate compatible native starting configs/locks. Missing controls fail;
  check defaults never request edits. Native rule IDs, not regex parsing,
  enforce
  demonstrated boundary conventions. Source-size guidance remains advisory.
- **Consequences:** Legacy configs read unchanged but missing static tools no
  longer count as degraded success. Reviewed arbitrary commands own complete,
  non-mutating coverage. Application formatting excludes managed kit; authoring
  CI covers it explicitly. Pyright executes its installed bundled native entry
  point without wrapper downloads. Adoption is manual and reviewable.
- **Evidence:**
  [TASK-010](../project/plans/P002-quality-first-harness/tasks/P002-T007-native-static-tools.md),
  [QH-07](../project/plans/P002-quality-first-harness/evidence/QH-07.md).
- **Supersedes:** Optional-tool success and syntax fallback from
  ADR-002/005/007;
  preserves native authority, ownership and single implementation precedence.

### ADR-010: Bind native verification outcomes to current inputs

- **Date:** 2026-10-01
- **Status:** accepted; implemented in Step 08
- **Decision:** Coordinate shared required controls without a scheduler;
  preserve
  native unittest/JUnit outcomes and fail missing evidence/zero/skips/retries.
  Use fixed output paths, conservative source/config/lock identities, bounded
  redacted artifacts and POSIX owned-group cleanup. Custom native evidence argv
  is project-owned and needs review; no generic policy DSL or implicit retries.
- **Consequences:** Successful shell exit alone cannot establish collection.
  Full root verification stays incomplete without root smoke. Reports remain
  editable provenance, not signed authenticity, test adequacy or a sandbox.
- **Evidence:**
  [TASK-011](../project/plans/P002-quality-first-harness/tasks/P002-T008-verification-evidence.md),
  [QH-08](../project/plans/P002-quality-first-harness/evidence/QH-08.md),
  [contract](../.harness/verification/README.md).
- **Supersedes:** ADR-004's deferred evidence requirement only.

### ADR-011: Separate offline security evidence from test network isolation

- **Date:** 2026-10-01
- **Status:** accepted; Step 09 implementation
- **Decision:** Use pinned Gitleaks, native npm audit/pip-audit captures and a
  few Ruff/ESLint rules. Explicit registry setup records source/time/version,
  native package coverage and lock/manifest identity; offline verify rejects
  stale/missing data. Critical/high/unknown block; exact source/dependency
  exceptions need owner/reason/expiry within 90 days. Secrets cannot be
  excepted.
  Project-owned security.json is explicit schema 1 opt-in; schema 2 mode selects
  required controls. No automatic project-file replacement or fixes.
- **Consequences:** Application verify/CI test phases use synthetic allowlisted
  environments and external macOS Seatbelt with actual direct/child/HTTP denial
  preflight. Seatbelt is deprecated, unavailable launch fails closed, and no
  hostile-code filesystem/VM or IPC-escape guarantee is made. Plain developer
  test/smoke are unisolated. Capability-specific security remains unsupported.
- **Evidence:**
  [TASK-012](../project/plans/P002-quality-first-harness/tasks/P002-T009-security-and-isolation.md),
  [QH-09](../project/plans/P002-quality-first-harness/evidence/QH-09.md),
  [contract](../.harness/security/README.md).
- **Supersedes:** ADR-008's unsupported security-mode result only. Ownership,
  native tool authority, unsigned evidence and independent runtime trust remain.

### ADR-012: Keep the real Next.js foundation project-owned and narrowly verified

- **Date:** 2026-10-02
- **Status:** accepted; Step 10 implementation
- **Decision:** Add `examples/nextjs-app/` with exact Next.js/React/native tool
  pins and its own config/lock. Retain the lightweight Node dispatcher fixture.
  Use a small owned shadcn-style Radix kit, two semantic token themes and local
  assets. Server Components render synthetic fixtures; only interaction state
  is client-owned. No application persistence/auth boundary is claimed.
- **Consequences:** App/components/dependencies never enter managed ownership.
  Package roots run independently. A reviewed native build/test/smoke plus
  evidence adapter enables initial Next.js/browser controls; verify executes
  the production build explicitly. Missing contracts and other capabilities
  remain required unsupported results. This is not complete browser assurance.
  Use maintained ESLint 10 with native Next/hooks rules: the bundled Next plugin
  set currently requires unsupported ESLint 9. No incompatible peer overrides.
- **Evidence:**
  [TASK-013](../project/plans/P002-quality-first-harness/tasks/P002-T010-nextjs-reference-app.md),
  [reference](../examples/nextjs-app/README.md),
  [partial
  verification](../project/plans/P002-quality-first-harness/evidence/QH-10.md).
- **Supersedes:** ADR-008's initial Next.js/browser unsupported result only;
  full accessibility/performance, aggregation and application security remain
  unimplemented. Native coverage/config ownership and Step 09 trust limits stay.

### ADR-013: Secure disposable persistence through real server boundaries

- **Date:** 2026-10-02
- **Status:** accepted; Step 11 implementation
- **Decision:** Replace the app's fixture-only edits with SQLite, versioned
  atomic save/audit, pure owner/tenant/editor policy and fresh private reads.
  Iron-session owns encrypted cookie verification; Argon2 owns password hashes.
  Opaque sessions load current identity/role/tenant and hard expiry from
  storage.
  Generated local credentials use the same actual sign-in path as every user.
- **Consequences:** Only private marked disposable loopback targets are
  supported;
  migration/seed/reset refuse production/unsafe/symlink targets. No handmade
  cryptography, impersonation route, shared user cache or production SSO bypass.
  Node's SQLite API is experimental on the pinned runtime. Native direct HTTP
  tests prove storage and denials; browser execution remains owner-paused.
  Declared identity/tenant/persistence controls require a separate native JUnit
  adapter, not merely successful UI tests or test-file presence.
- **Evidence:**
  [TASK-014](../project/plans/P002-quality-first-harness/tasks/P002-T011-secure-persistence.md),
  [app security](../examples/nextjs-app/docs/SECURITY.md).
- **Supersedes:** ADR-012's no-persistence/auth boundary only; ownership, native
  tool authority and external macOS isolation limits remain unchanged.

### ADR-014: Prove journeys through native production and storage evidence

- **Date:** 2026-10-02
- **Status:** accepted; Step 12 implementation
- **Decision:** Use pinned Playwright against the production build and actual
  synthetic sessions/SQLite. Inject audit dependency failure outside production
  code; assert visible outcomes and durable versions/audits. Test-only lifecycle
  scripts own unique storage and recorded server processes. Optional reviewed
  smoke-evidence.json reuses the native evidence contract; the reference adapter
  runs full journeys while smoke stays one meaningful case.
- **Consequences:** Unexpected console/page errors fail with one exact
  deliberate
  503 resource-error allowance. Disposable save/ownership mutants must fail
  intended assertions. Renewed authorization closes the current browser gap
  without rewriting historical partial evidence. Chromium/macOS only; full UI
  quality controls and human acceptance remain separate.
- **Evidence:**
  [TASK-015](../project/plans/P002-quality-first-harness/tasks/P002-T012-user-journeys.md).
- **Supersedes:** ADR-013's owner-paused current browser status only; security,
  ownership and unsigned/native evidence trust limits remain unchanged.

### ADR-015: Native UI controls do not impersonate human acceptance

- **Date:** 2026-10-02
- **Status:** accepted implementation boundary; visual approval pending
- **Decision:** Keep axe, keyboard/reflow, native screenshot comparison and
  measured lab budgets in the project-owned Next.js tests. Delegate their JUnit
  through the existing browser evidence adapter. Chromium/macOS is the declared
  matrix; untested engines remain unverified. Disable native snapshot updating.
- **Consequences:** Missing human-reviewed baseline metadata/images fail the
  native full suite and block verify completeness. Forty-four pinned candidates
  and synthetic disposable comparator tests do not establish human acceptance.
  Lab budgets are reviewable proposals, not field performance or conformance.
- **Evidence:**
  [QH-13](../project/plans/P002-quality-first-harness/evidence/QH-13.md), app
  quality/baseline procedure.
- **Supersedes:** Step 12's pending programmatic UI controls only.

### ADR-016: Separate work navigation from implementation review detail

- **Date:** 2026-10-07
- **Status:** accepted; repository workflow implementation
- **Context:** Long roadmaps mixed sequence, prompts and progress history;
  reviewers lacked a short route from intent to implementation boundaries.
- **Decision:** Keep one concise roadmap table, stable task IDs, separate step
  guides and explicit completed/superseded directories. Tasks own acceptance and
  change-specific reviewer briefs; canonical architecture owns linked component
  maps, important flows, choices and operational limits. Reports own evidence.
- **Consequences:** Update incoming links and indexes on state/move changes.
  Maps and briefs require source inspection and maintenance; no generated
  inventory, additional status database or runtime command is introduced.
  Mechanical checks do not replace human challenge of intent, context and risk.
  Apply the brief/map workflow to new work; historical evidence stays intact.
- **Evidence:**
  [TASK-017](../project/archive/P003-reviewable-work/tasks/P003-T001-reviewable-work.md),
  [work index](../project/README.md), [reviewer entry](README.md).
- **Rationale:** [Allspaw's review
  essay](https://www.adaptivecapacitylabs.com/2026/08/24/there-is-more-to-code-review-than-automatable-detection/)
  motivates maintaining shared understanding and discussion alongside automated
  detection. This is our workflow interpretation, not a measured productivity
  claim or a substitute for inspecting code.
- **Supersedes:** Plan/task document organisation only; existing implementation
  and verification contracts and approval boundaries remain authoritative.

### ADR-017: Plan-owned work bundles with derived navigation

- **Date:** 2026-10-07
- **Status:** accepted; requested project organisation
- **Decision:** Keep project management in `project/`. Use project-wide PNNN
  plans with per-plan PNNN-TNNN tasks/evidence. Shared current architecture lives
  outside bundles. Archive whole complete/superseded bundles; retain IDs/history.
- **Formalism:** Markdown fields and fixed headings; task state owns progress.
  Stdlib helpers validate records/dependencies/evidence and generate indexes.
  `FORMAT.md` opts projects in; legacy layouts remain supported.
- **Operations:** Explicit sync writes navigation. Archive checks completion,
  repairs links and rolls back ordinary write failures. Process-crash atomicity
  and semantic architecture validation are not claimed.
- **Evidence:** [P004](../project/archive/P004-project-organisation/README.md).
- **Supersedes:** ADR-016's separate plan/task folders and manual progress indexes.

## Decision template

### ADR-000: Short title

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | superseded
- **Context:** What durable problem or constraint requires a choice?
- **Decision:** What was chosen?
- **Consequences:** What becomes easier, harder, or constrained?
- **Evidence:** Links to relevant plans, code, research, or tests.
- **Supersedes:** ADR-NNN or none.
