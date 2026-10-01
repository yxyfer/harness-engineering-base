# Plan: Project Harness v2 — installable, enforceable project baseline

- **Status:** phases 1–3 implemented; remaining sequence superseded
- **Owner:** repository owner
- **Created:** 2026-09-08
- **Target completion:** not time-bound
- **Related tasks:** create one task per phase from the repository task template

On 2026-10-01, the user prioritised application safety, user experience, code
quality, customer consistency, and entirely programmatic verification. Follow
[the quality-first plan](QUALITY_FIRST_HARNESS.md) for new work. This document
retains the original roadmap and completed-phase evidence; its unfinished
capabilities are not delivered or marked complete.

## Objective

Turn this first-pass harness into a dependable macOS-first base that can be used
in two ways:

1. Create a new project directly from this repository and have the harness work
   immediately.
2. Adopt the harness safely into an existing project, inspect what is already
   there, draft missing context, and establish an honest baseline without
   overwriting project-owned work.

The completed harness must give humans and agents the same durable project
context, apply consistent engineering standards, expose task-specific workflows,
and provide executable evidence that installation, project readiness, code
quality, security, tests, and the golden path are healthy.

## Why this plan exists

The current first pass proves the core command contract and documentation model,
but its source and installed layouts are different:

- Copyable project files are nested under `template/`.
- Skills are under `skills/`, while repository-discovered agent skills need to
  be installed under `.agents/skills/`.
- Checks are outside the copyable template, so copying `template/` alone does
  not produce a self-contained installation.
- There is no installer, adoption workflow, central configuration, version
  marker, managed-file policy, readiness assessment, CI gate, or upgrade path.
- Engineering and architecture principles are described only partially and are
  not yet backed by language-specific tool configurations.

This plan resolves those gaps in dependency order. Phase 1 establishes the final
layout before later work adds behaviour to paths that would otherwise move.

## Guiding model

The installed repository has three layers:

| Layer | Purpose | Ownership | Discovery |
| --- | --- | --- | --- |
| Project context | Product truth, plans, tasks, decisions, and evidence | Human/project owned | Visible at repository root |
| Harness machinery | Commands, checks, standards, templates, version, and configuration | Harness managed unless explicitly configured | Hidden under `.harness/` |
| Agent integration | Task-specific agent workflows | Harness managed with project additions allowed | Codex discovers `.agents/skills/` |

Universal rules that must always apply belong in the root `AGENTS.md` or in a
document it explicitly requires agents to read. Task-specific procedures belong
in skills. Formatting and lint rules must be implemented in tools and
configuration rather than relying on prose alone.

## Target installed structure

```text
project-root/
├── AGENTS.md
├── README.md
├── harness                         # Small dispatcher: ./harness <command>
├── docs/
│   ├── PRODUCT.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── DATA.md
│   ├── QUALITY.md
│   ├── SECURITY.md
│   └── DECISIONS.md
├── plans/
│   ├── PLAN_TEMPLATE.md
│   ├── active/
│   ├── completed/
│   └── technical-debt.md
├── tasks/
│   └── TASK_TEMPLATE.md
├── verification/
│   └── REPORT_TEMPLATE.md
├── .harness/
│   ├── VERSION
│   ├── manifest.json
│   ├── config.toml
│   ├── bin/
│   ├── checks/
│   ├── standards/
│   │   ├── BASE.md
│   │   ├── NAMING.md
│   │   ├── TESTING.md
│   │   ├── ARCHITECTURE.md
│   │   └── languages/
│   │       ├── python.md
│   │       ├── typescript.md
│   │       ├── shell.md
│   │       └── markdown.md
│   ├── templates/
│   ├── tests/
│   │   └── fixtures/
│   └── exceptions.yml
└── .agents/
    └── skills/
        ├── implement-feature/
        ├── reproduce-bug/
        ├── code-review/
        ├── visual-qa/
        └── update-project-context/
```

## Ownership and update boundaries

These boundaries must be settled before implementing the updater.

| Path | Default owner | Update behaviour |
| --- | --- | --- |
| `.harness/**` | Harness | May update after checksum and conflict checks |
| `.agents/skills/<shipped-skill>/**` | Harness | May update after conflict checks |
| `harness` dispatcher | Harness | May update after conflict checks |
| `AGENTS.md` | Project after creation | Never overwrite automatically |
| `docs/**` | Project | Never overwrite; offer new templates as side files |
| `plans/**` | Project | Never overwrite active or completed records |
| `tasks/**` | Project | Never overwrite project tasks |
| `verification/**` | Project | Never overwrite evidence |
| Tool configuration | Shared | Merge only through an explicit, reviewable proposal |

The manifest records shipped files and their checksums. A locally modified
managed file is a conflict, not permission to overwrite it.

## Fixed decisions for this plan

- macOS is the only supported platform for the first complete release.
- User-facing setup guidance may assume zsh and Homebrew.
- Harness shell scripts should remain POSIX `sh` where that is inexpensive.
- The root becomes the canonical installed layout; `template/` is removed after
  migration and verification.
- `./harness <command>` becomes the single public command interface.
- TOML is the central configuration format.
- Installation and health checks are non-destructive by default.
- Existing project failures are recorded as a baseline; adoption must not imply
  that pre-existing failures were introduced by the harness.
- Root `AGENTS.md` carries mandatory operating expectations. Skills supplement
  it but are not the only way universal rules are delivered.
- Project context generated during adoption is a draft until a human confirms
  it. Inferences must be labelled.

## Open policy choices

Resolve these while implementing the relevant phase. Do not allow them to block
Phase 1.

| Choice | Proposed default | Decide by |
| --- | --- | --- |
| Shared line width | 80 characters | Resolved in Phase 3 |
| Large file warning | 350 source lines | Resolved in Phase 3 |
| Large function warning | 50 source lines | Resolved in Phase 3 |
| Python tools | Ruff format/lint, Pyright, pytest | Resolved in Phase 3 |
| TypeScript tools | Prettier, ESLint, strict TypeScript | Resolved in Phase 3 |
| Markdown tools | Markdownlint plus link check | Resolved in Phase 3 |
| Exception expiry | Required, maximum 90 days by default | Phase 6 |
| Readiness levels | ready, needs-input, blocked | Phase 4 |
| Harness release scheme | Semantic versioning; initial version `0.1.0` | Resolved in Phase 2 |

## Ordered implementation roadmap

### Phase 1 — Adopt the three-layer installed structure

**Outcome:** The repository itself is a valid starter project. A fresh clone has
the files in their final locations, Codex can discover its instructions and
skills, and all existing harness behaviours still work.

**Why first:** Every later feature depends on stable paths. Adding standards,
doctor, CI, or installers before this migration would create avoidable rewrites.

#### Steps

1. Capture the current baseline by running the existing `inspect`, `check`,
   `test`, and `smoke` commands against both example projects. Record the exact
   commands and results in a temporary migration verification report.
2. Move `template/AGENTS.md` to the repository root.
3. Move the human-owned directories from `template/` to the root: `docs/`,
   `plans/`, `tasks/`, and `verification/`. Preserve this active plan when
   reconciling the two plan directories.
4. Move shipped skills from `skills/` to `.agents/skills/`. Confirm every skill
   retains its `SKILL.md`, name, description, and executable resources.
5. Move checks from `checks/` to `.harness/checks/`.
6. Move the current example projects to `.harness/tests/fixtures/`. Rename them
   only if doing so improves their role as test fixtures.
7. Move internal command implementations from `template/harness/` to
   `.harness/bin/` and update their root-resolution logic.
8. Add a small root `harness` dispatcher supporting the existing subcommands:
   `setup`, `start`, `inspect`, `check`, `test`, and `smoke`.
9. Ensure the dispatcher resolves its repository root correctly when launched
   from the root or a nested working directory and when the repository path
   contains spaces.
10. Update all documentation, skills, checks, fixtures, and error messages to use
    `./harness <command>` and the new paths.
11. Remove the now-empty `template/`, `skills/`, `checks/`, and `examples/`
    directories only after confirming every tracked file has a target location.
12. Update `.gitignore` for Python caches, temporary harness state, test output,
    environment files, and tool caches without ignoring evidence or project
    context.
13. Run a repository-wide link and stale-path search for `template/`, root
    `skills/`, root `checks/`, and the former command syntax.

#### Acceptance criteria

- `AGENTS.md` is present at the Git root.
- Every shipped skill is under `.agents/skills/<name>/SKILL.md`.
- All managed machinery is under `.harness/`, except the root dispatcher.
- Human-owned context remains visible at the root.
- `./harness inspect`, `check`, `test`, and `smoke` work against both fixtures.
- Commands work when the repository path contains spaces.
- Documentation contains no stale paths or broken local links.
- The old directories are absent and no source file was lost.

#### Verification

```text
./harness inspect .harness/tests/fixtures/nextjs-project
./harness check .harness/tests/fixtures/nextjs-project
./harness test .harness/tests/fixtures/nextjs-project
./harness smoke .harness/tests/fixtures/nextjs-project
./harness inspect .harness/tests/fixtures/python-project
./harness check .harness/tests/fixtures/python-project
./harness test .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/python-project
```

Also copy the repository to a temporary path containing spaces and repeat the
non-install checks there.

#### Suggested commit

`refactor(harness): adopt three-layer repository structure`

---

### Phase 2 — Define the harness contract, configuration, and version identity

**Outcome:** Commands, configuration, ownership, compatibility, and versioning
have one documented and machine-readable contract.

#### Steps

1. Add `.harness/VERSION` with the first semantic version of the new layout.
2. Define `.harness/config.toml` with a documented, minimal schema for:
   - enabled language profiles;
   - project command overrides;
   - required checks;
   - warning and failure thresholds;
   - readiness requirements;
   - security-check modes;
   - paths excluded from analysis.
3. Add `.harness/manifest.json` containing harness version, schema version,
   installed managed paths, checksums, and installation timestamp. Do not put
   volatile project state or secrets in the manifest.
4. Define precedence: explicit CLI option, environment override, project config,
   language-profile default, then auto-detection.
5. Define stable exit behaviour for success, project failure, incomplete
   readiness, invalid configuration, and broken installation.
6. Make `./harness inspect` display the effective configuration and its source.
7. Document managed versus project-owned files in the root README and
   `AGENTS.md`.
8. Validate configuration strictly. Unknown keys should produce an actionable
   error or version-aware warning rather than being silently ignored.

#### Acceptance criteria

- A user can determine the installed harness and schema version offline.
- Effective configuration is deterministic and inspectable.
- Project commands can be overridden without editing harness scripts.
- Configuration errors identify the file, key, and expected value.
- No secret or machine-specific absolute path is written to committed files.

#### Suggested commit

`feat(harness): add versioned configuration contract`

---

### Phase 3 — Establish enforceable engineering and architecture standards

**Status:** completed on 2026-09-08. Evidence is recorded in
`verification/PHASE_3_ENGINEERING_STANDARDS.md`.

**Outcome:** The repository defines a consistent baseline while retaining
language idioms and allowing justified exceptions.

#### Steps

1. Write `.harness/standards/BASE.md` covering readability, explicit failure,
   validation at boundaries, type safety, dependency discipline, comments that
   explain why, reuse of existing code, and removal of dead code.
2. Write `.harness/standards/NAMING.md` with shared semantic rules and a language
   mapping for casing. Include conventions for booleans, types, constants,
   files, tests, interfaces, and intentionally private symbols.
3. Write `.harness/standards/TESTING.md` with proportionate test-first rules:
   - bugs begin with a failing reproduction;
   - core domain behaviour is normally test-first;
   - risky refactors begin with characterisation coverage;
   - tests verify observable behaviour rather than duplicating implementation;
   - visual or configuration-only changes use appropriate evidence.
4. Write `.harness/standards/ARCHITECTURE.md` covering cohesion, dependency
   direction, deterministic core versus external I/O, stable interfaces at
   volatile boundaries, KISS, YAGNI, qualified DRY, least privilege,
   observability, compatible data change, rollback, provenance, and ADR triggers.
5. Add language profiles for Python, TypeScript/JavaScript, shell, and Markdown.
   Each profile defines its formatter, linter, type checker where applicable,
   naming rules, test convention, supported version range, and exceptions.
6. Decide and record numeric defaults for line width, large files, and large
   functions. Begin size rules as warnings, not blocking failures.
7. Add actual formatter and linter configuration for the fixture projects.
   Documentation must agree with executable configuration.
8. Add a standards check that selects only profiles relevant to the detected or
   configured languages.
9. Exclude generated code, vendored code, dependency directories, migrations,
   schemas, and fixtures where a rule would create noise. Keep exclusions
   explicit and reviewable.
10. Update `AGENTS.md` so agents must read the relevant standards before editing
    affected languages.

#### Acceptance criteria

- Each supported language has unambiguous formatting and naming rules.
- `./harness check` runs the configured tools rather than checking prose with
  fragile regular expressions.
- One command can format or report formatting differences consistently.
- Large-file and large-function warnings name the threshold and exception path.
- TDD and DRY are expressed as decision rules, not absolute slogans.

#### Suggested commit

`feat(standards): define enforceable engineering baseline`

---

### Phase 4 — Add doctor, self-test, and readiness assessment

**Outcome:** The harness distinguishes installation health, harness behaviour,
and project-context readiness.

#### Steps

1. Add `./harness doctor` as a read-only installation diagnostic.
2. Have doctor verify root detection, dispatcher permissions, version and
   manifest consistency, configuration validity, managed file presence,
   discoverable skills, checks, required runtimes, and selected tool availability.
3. Provide exact remediation commands, but do not mutate automatically.
4. Add `./harness doctor --repair` only for safe, deterministic repairs. Preview
   every change and require approval before overwriting or installing software.
5. Add `./harness self-test` to create disposable fixtures in a temporary
   directory and test:
   - Node and Python detection;
   - command overrides;
   - missing manifests and runtimes;
   - failing checks and tests;
   - missing smoke commands;
   - paths containing spaces;
   - malformed configuration;
   - installer idempotency once Phase 5 lands.
6. Add `./harness readiness` with `ready`, `needs-input`, and `blocked` results.
7. Give context documents structured metadata such as status, owner, and last
   review date so readiness does not depend only on searching for `TBD`.
8. Make readiness assess product purpose and golden path, architecture
   boundaries, data provenance, real versus simulated integrations, quality
   gates, security ownership, active work, and unresolved human decisions.
9. Keep deterministic readiness separate from semantic assessment. Create or
   extend a skill that reviews whether populated context is specific and
   evidence-backed.
10. Produce both human-readable output and a stable machine-readable format for
    CI and tooling.

#### Acceptance criteria

- Doctor distinguishes missing optional tools from a broken installation.
- Self-test leaves no persistent processes or files outside its temporary area.
- A freshly installed but unconfigured project reports `needs-input`, not pass.
- A structurally broken installation reports `blocked` with remediation.
- Readiness never marks inferred adoption content as human-confirmed.

#### Suggested commit

`feat(harness): add health and readiness diagnostics`

---

### Phase 5 — Build new-project initialization and existing-project adoption

**Outcome:** Users can install the harness safely into new or existing
repositories, and agents can guide the workflow without inventing context.

#### Steps

1. Add an idempotent installer exposed as `./harness init <target>` for empty or
   new repositories.
2. Add `./harness adopt <target>` for existing repositories.
3. Implement a non-mutating preflight that inspects Git state, languages,
   manifests, package managers, existing scripts, tests, CI, documentation,
   architecture signals, environment files, and likely generated directories.
4. Produce a proposed file-operation and configuration plan before writing.
5. Refuse implicit overwrites. For collisions, support keep-existing,
   side-by-side proposal, explicit merge, or abort.
6. Install managed machinery, the root dispatcher, and shipped repo skills.
7. Create project-owned context files only when absent. When present, propose
   additions rather than replacing them.
8. Draft product and technical context from repository evidence. Mark every
   inference and unresolved field, and keep document status as `needs-input`.
9. Detect current project-native commands and propose mappings in
   `.harness/config.toml`.
10. Run existing checks before enforcing new ones. Save a timestamped adoption
    baseline that separates pre-existing failures from installation defects.
11. Offer to record intentional inherited issues in technical debt, with owner
    and trigger, rather than silently waiving them.
12. Finish with doctor and readiness reports plus the smallest list of human
    questions required to reach ready status.
13. Add `--dry-run`, `--non-interactive`, and machine-readable output. The
    non-interactive mode must fail safely on conflicts or missing decisions.
14. Add a user-level `bootstrap-project-harness` skill whose only installation
    logic is to locate and invoke the versioned installer. The skill should
    orchestrate inspection, explain proposed changes, and preserve approval
    boundaries.
15. Document how to install that user-level skill once under
    `~/.agents/skills/`, while keeping repo-specific skills in
    `.agents/skills/`.

#### Acceptance criteria

- Running init twice produces no unintended changes.
- Adoption works in a dirty repository without touching unrelated changes.
- Dry-run output completely describes planned mutations.
- Existing documents and tool configuration are never silently overwritten.
- Pre-existing check failures are clearly distinguished from harness failures.
- The bootstrap skill delegates to the installer and does not fork its own
  installation implementation.
- A new Codex session sees the root `AGENTS.md` and repository skills after
  installation.

#### Suggested commits

```text
feat(installer): add idempotent project initialization
feat(adoption): add evidence-led existing-project workflow
feat(skills): add user-level harness bootstrap workflow
```

---

### Phase 6 — Add governed exceptions

**Outcome:** Teams can make temporary, explicit exceptions without weakening a
rule globally or hiding debt.

#### Steps

1. Define `.harness/exceptions.yml` with rule ID, scope, reason, owner, creation
   date, expiry or review date, and optional ADR/debt link.
2. Validate exception syntax and reject unknown rule IDs.
3. Make checks apply the narrowest matching exception and report when it is used.
4. Warn before expiry and fail expired exceptions in CI.
5. Prohibit repository-wide wildcards unless accompanied by an accepted ADR.
6. Add `./harness exceptions list`, `validate`, and `expiring` commands.
7. Ensure inline tool suppressions either reference an exception or remain
   governed by a documented language-specific convention.

#### Acceptance criteria

- Every bypass has an owner, reason, scope, and review point.
- Expired or malformed exceptions cannot silently pass.
- Reports distinguish passed checks from excepted checks.
- Removing an exception re-enables the underlying rule immediately.

#### Suggested commit

`feat(governance): add time-bound check exceptions`

---

### Phase 7 — Add security automation

**Outcome:** Fast local controls and stronger CI controls cover common project
and harness risks without exposing secrets.

#### Steps

1. Extend `docs/SECURITY.md` with the supported security-check contract and
   ownership expectations.
2. Add local checks for committed secret patterns, tracked environment files,
   unsafe file permissions, suspicious hard-coded credentials, and demo versus
   production-data claims.
3. Add ecosystem-native dependency auditing for enabled language profiles.
4. Add a heavier CI security mode for full-history secret scanning and deeper
   dependency analysis where the selected tools support it.
5. Redact candidate secret values from all output. Report file and rule without
   echoing the value.
6. Route false positives through governed exceptions rather than broad ignores.
7. Add fixtures for real detections, redaction, false positives, ignored
   generated files, and expired security exceptions.
8. Document network requirements and keep offline-safe checks available.

#### Acceptance criteria

- A known fixture secret fails without printing the secret.
- `.env.example` is allowed only when it contains non-sensitive placeholders.
- Dependency failures identify the affected ecosystem and remediation path.
- Local and CI security modes are explicit and reproducible.

#### Suggested commit

`feat(security): add local and CI security checks`

---

### Phase 8 — Add CI and pull-request gates

**Outcome:** The same commands developers and agents run locally protect the
default branch.

#### Steps

1. Add a macOS CI workflow because macOS is the supported platform.
2. Run doctor, configuration validation, self-test, project check, project test,
   smoke where feasible, readiness, exception validation, and security checks.
3. Cache dependencies without caching project outputs that could hide failures.
4. Upload verification artifacts and machine-readable reports on failure.
5. Keep CI orchestration thin: it must call the public harness commands instead
   of reimplementing their logic in workflow YAML.
6. Define which readiness states block a pull request and which only warn during
   initial adoption.
7. Add a scheduled job for expiring exceptions and dependency/security checks if
   those checks are too slow for every pull request.
8. Document required branch protections without assuming permission to configure
   a remote repository automatically.

#### Acceptance criteria

- Local and CI results use the same underlying commands and configuration.
- A deliberately failing fixture demonstrates each blocking gate.
- CI failure artifacts explain the failing command and remediation.
- The workflow does not require repository secrets for ordinary checks.

#### Suggested commit

`ci(harness): enforce project health gates on macOS`

---

### Phase 9 — Implement safe updates and migrations

**Outcome:** Installed projects can discover and adopt newer harness versions
without losing local context or managed-file changes.

#### Steps

1. Define semantic-version compatibility for the harness and config schema.
2. Add `./harness update --check` to report available or supplied versions
   without modifying the project.
3. Add `./harness update --dry-run` to compare the installed manifest with the
   target version and classify unchanged, locally modified, new, removed, and
   conflicting files.
4. Update only unchanged managed files automatically.
5. Preserve locally modified managed files and generate a reviewable merge or
   side file. Never overwrite project-owned files.
6. Add ordered, versioned migrations for config or manifest schema changes.
7. Back up replaced managed files to a temporary recoverable location for the
   duration of the update and report how to restore them.
8. Run doctor and self-test after the update. Roll back managed changes if the
   new installation is structurally broken.
9. Record the resulting version and checksums only after successful validation.
10. Test upgrades from every supported prior schema, including interrupted and
    conflicting updates.

#### Acceptance criteria

- Update check and dry-run are non-mutating.
- Project-owned context is unchanged after every update fixture.
- Local managed-file modifications produce conflicts rather than data loss.
- Failed migrations leave the prior installation usable or provide an exact
  recovery path.
- Manifest and version are updated atomically after success.

#### Suggested commit

`feat(harness): add safe versioned updates`

---

### Phase 10 — Dogfood, document, and release the base

**Outcome:** A clean user can create or adopt a project using only documented
steps, and the resulting repository is ready for agent-assisted work.

#### Steps

1. Run the full workflow against a new empty repository.
2. Run adoption against representative existing Python and Next.js repositories,
   including one with existing docs, custom scripts, and known failures.
3. Start Codex from the root and a nested directory and verify instruction and
   skill discovery.
4. Review generated context for unsupported inference, false certainty, and
   project-specific leakage from the harness fixtures.
5. Review all first-run output for a clear distinction between installed,
   healthy, and ready.
6. Finalise the README quickstart for:
   - using the repository as a new-project template;
   - adopting an existing repository;
   - installing the user-level bootstrap skill;
   - checking health and readiness;
   - updating the harness.
7. Add a concise changelog and release notes describing supported macOS scope,
   required tools, known limitations, and recovery paths.
8. Tag the first stable release only after all phase acceptance criteria and the
   final verification matrix pass.

#### Acceptance criteria

- A new user can reach a correct doctor result using only the README.
- A clean new project reaches `needs-input`, then `ready` after context is filled.
- An existing project can be adopted without overwriting its files.
- All examples and self-tests pass on a clean supported macOS environment.
- Documentation and command help agree.
- The release records limitations honestly and contains no project-specific
  secrets, absolute paths, caches, or generated state.

#### Suggested commit

`docs(harness): prepare first stable project baseline`

## Cross-phase verification matrix

| Capability | Unit/fixture evidence | End-to-end evidence | Human review |
| --- | --- | --- | --- |
| Three-layer layout | Path and manifest assertions | Fresh clone commands | Discoverability |
| Configuration | Parser and precedence tests | Override a fixture command | Schema clarity |
| Standards | Passing and failing language fixtures | Run project check | Rule usefulness |
| Doctor | Broken-installation fixtures | Diagnose and repair copy | Remediation clarity |
| Readiness | State transition fixtures | Draft-to-ready project | Context quality |
| Init | Empty-directory fixtures | Initialise twice | Generated usability |
| Adopt | Collision and dirty-tree fixtures | Adopt existing projects | Inference accuracy |
| Exceptions | Valid, invalid, expired fixtures | CI exception report | Justification quality |
| Security | Detection and redaction fixtures | Local and CI modes | False-positive rate |
| Update | Version and conflict matrix | Upgrade and rollback | Diff clarity |

## Risks and mitigations

| Risk | Impact | Mitigation or fallback | Owner |
| --- | --- | --- | --- |
| Harness becomes more complex than projects | Maintenance burden and avoidance | Keep one dispatcher, small config, and project-native commands | Harness owner |
| Universal rules fight language conventions | Low-quality code and constant exceptions | Use language profiles and shared semantic naming only | Standards owner |
| Adoption overwrites existing work | Data loss and loss of trust | Dry-run, checksums, side files, and explicit conflict choices | Installer owner |
| Generated context appears authoritative | Agents act on invented assumptions | Mark drafts/inference and require human readiness approval | Context owner |
| Size rules reward artificial splitting | Worse architecture | Begin as warnings and allow narrow governed exceptions | Standards owner |
| Security output leaks candidate secrets | Secondary exposure | Redact values and test output explicitly | Security owner |
| Updates drift from locally modified harness | Broken projects or hidden divergence | Manifest checksums and conflict-aware updates | Release owner |
| Skills contain universal rules but do not activate | Inconsistent agent behaviour | Put mandatory rules in root `AGENTS.md` | Agent-integration owner |
| macOS-only assumptions spread into project code | Future portability cost | Isolate platform logic in harness internals | Harness owner |

## Phase completion discipline

For each phase:

1. Create a bounded task with its exact acceptance criteria.
2. Read this plan and the affected canonical context before editing.
3. Record any durable deviation in `docs/DECISIONS.md`.
4. Implement only the current phase or a smaller coherent slice.
5. Run the phase verification and the regression suite from completed phases.
6. Create a verification report containing commands actually run, output summary,
   environment, limitations, and unresolved decisions.
7. Update this plan's status table below.
8. Commit the coherent phase only when explicitly requested.

## Progress tracker

| Phase | Status | Verification report | Notes |
| --- | --- | --- | --- |
| 1. Three-layer structure | complete | `verification/PHASE_1_THREE_LAYER_STRUCTURE.md` | Completed 2026-09-08 at `24e2c3e` |
| 2. Contract and configuration | complete | `verification/PHASE_2_VERSIONED_CONFIGURATION.md` | Completed 2026-09-08; version `0.1.0`, schema `1` |
| 3. Standards and principles | complete | `verification/PHASE_3_ENGINEERING_STANDARDS.md` | Completed 2026-09-08; 80/350/50 defaults |
| 4. Health and readiness | next | Not started | Uses config and standards |
| 5. Init, adopt, and bootstrap skill | proposed | Not started | Uses doctor and readiness |
| 6. Governed exceptions | proposed | Not started | Integrates with all checks |
| 7. Security automation | proposed | Not started | Uses exception mechanism |
| 8. CI gates | proposed | Not started | Runs public command contract |
| 9. Updates and migrations | proposed | Not started | Requires versioned installer |
| 10. Dogfood and release | proposed | Not started | Final end-to-end evidence |

## Overall completion criteria

- [ ] The repository root is the canonical three-layer starter layout.
- [ ] A fresh clone works on supported macOS without moving template files.
- [ ] A single dispatcher exposes documented commands and stable exit behaviour.
- [ ] Engineering and architecture standards are documented and tool-enforced.
- [ ] Doctor, self-test, and readiness have distinct, tested responsibilities.
- [ ] New-project init and existing-project adoption are safe and idempotent.
- [ ] The user-level bootstrap skill delegates to the installer.
- [ ] Exceptions are narrow, owned, time-bound, and visible in reports.
- [ ] Security checks redact sensitive values and run locally and in CI.
- [ ] CI calls the same public commands used locally.
- [ ] Versioned updates preserve project-owned and locally modified files.
- [ ] Full new-project and adoption journeys have verification reports.
- [ ] Supported platform and known limitations are explicit.

## Final verification

- **Report:** `verification/PROJECT_HARNESS_V2.md` when complete
- **Completed:** pending
- **Remaining limitations:** pending final verification
