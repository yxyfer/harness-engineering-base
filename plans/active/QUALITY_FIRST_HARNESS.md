# Application quality harness implementation plan

- **Status:** active; Steps 01-03 complete; Steps 04-19 not started
- **Owner:** repository owner
- **Created and expanded:** 2026-10-01
- **Direction:** [Product vision](../../docs/PRODUCT.md)
- **Baseline:** [Repository audit](../../verification/AUDIT_2026_10_01.md)
- **Decision:** [ADR-003](../../docs/DECISIONS.md)
- **History:** [Previous roadmap](PROJECT_HARNESS_V2.md)

Build a small engineering harness that helps coding agents produce safer, more
usable and maintainable customer applications. Deliver working foundations and
trustworthy verification before expanding distribution tooling. The first
application stacks are TypeScript with Next.js and Python.

This document turns the agreed vision into 19 ordered implementation steps. Each
has an outcome, acceptance criteria and a copy-ready prompt. It replaces the
earlier A–E slice outline while preserving its priorities. Proposed commands,
foundations and CI gates below are not claims about current capabilities.

## How to execute this plan

Use one step prompt at a time in this repository. Each prompt tells the coding
agent to read this plan's execution contract, so it works in a fresh chat
without copying the earlier conversation. Complete the step's evidence before
beginning dependent work. Do not paste all prompts as one implementation
request.

Default to numbered order. Dependencies allow independent work when another step
needs owner input; they do not request sub-agents or concurrent editing. Split a
large step into smaller tasks while preserving its acceptance criteria.

Use the next free task number from
[the task template](../../tasks/TASK_TEMPLATE.md). Create evidence in
`verification/QH-01.md` through `verification/QH-19.md` as steps run, using
[the report template](../../verification/REPORT_TEMPLATE.md). These are future
output paths. Add task/evidence links to the status table only when the files
exist. Partially verified steps stay incomplete.

## Execution contract for every prompt

1. Read `AGENTS.md`, relevant canonical context, accepted decisions, this step
   and its prerequisites. Before source edits read the base standards and
   relevant language profiles. Inspect Git status and preserve existing work.
2. Work only on this step. Reuse project-native tools, components and commands.
   Customise through project configuration, not project-specific engine logic.
   Do not build a plugin platform or another agent runtime.
3. Define observable acceptance cases before implementation. Defect fixes need a
   reproduction that fails for the intended reason before the fix and passes
   afterwards. Test behaviour and boundaries, not implementation trivia.
4. All automated execution and grading use conventional programs. No LLM judges,
   AI screenshot reviewers, secondary AI test calls or model-provider requests
   belong in verification. The coding agent may author tests. Human
   product/design acceptance stays separate from automated grading.
5. Use synthetic data, temporary projects, disposable databases and local test
   services. Dependency/advisory downloads are explicit setup work; tests must
   not silently access production or model providers.
6. Do not weaken checks to pass: no silent runner changes, test deletion,
   blanket suppressions, hidden retries or auto-approved screenshots. Legitimate
   policy changes need an explicit reason and independent review. Unavailable
   verification remains visible, including missing tools and network failures.
7. Run `./harness check`, `./harness test`, relevant fixture smoke and native
   checks. After Step 02, also use `./harness self-test` for harness changes.
   After Step 08, use the implemented `verify` interface for complete evidence.
   Never call future commands before they exist. Root smoke is currently
   undefined; use applicable fixture smoke and state that limitation.
8. For managed-file changes, inspect manifest differences and regenerate only
   intended release inputs. Never absorb unrelated files or bless consumer
   checksum conflicts simply to make inspection pass.
9. Update canonical context for durable implemented facts; label proposals.
   Record commands, exits, collection, evidence, tested source identity and
   limitations in the step report. Update the status table honestly.
10. End with changes, verification, limitations and the next eligible step; then
    stop. Destructive changes, publication, production access, security
    trade-offs and irreversible migrations retain the repository approval rules.
    Ordinary reversible implementation needs no additional approval ceremony.

## Delivery sequence and checkpoints

Steps 01-03 are **complete**; Steps 04-19 are **not started**. Proposed paths may
use established equivalents if implementation records the mapping.

| Step | Deliverable                                    | Depends on | Status      |
| ---- | ---------------------------------------------- | ---------- | ----------- |
| 01   | [Baseline and acceptance cases](../../tasks/TASK-004-QUALITY-BASELINE.md) | None | [Complete](../../verification/QH-01.md) |
| 02   | [Correct application test routing](../../tasks/TASK-005-APPLICATION-TEST-ROUTING.md) | 01 | [Complete](../../verification/QH-02.md) |
| 03   | [Consistent discovery and command precedence](../../tasks/TASK-006-DISCOVERY-AND-CHECK-PRECEDENCE.md) | 02 | [Complete](../../verification/QH-03.md) |
| 04   | Correct managed-file ownership                 | 03         | Not started |
| 05   | CI for the repaired harness                    | 04         | Not started |
| 06   | Relevant profiles and prerequisite diagnostics | 05         | Not started |
| 07   | Native formatting and static checks            | 06         | Not started |
| 08   | Complete verification and trustworthy reports  | 07         | Not started |
| 09   | Security checks and isolated verification      | 08         | Not started |
| 10   | Real Next.js foundation and shared UI          | 09         | Not started |
| 11   | Secure server operations and real persistence  | 10         | Not started |
| 12   | Complete application journey tests             | 11         | Not started |
| 13   | Accessibility, visual and performance checks   | 12         | Not started |
| 14   | Useful Python reference application            | 09         | Not started |
| 15   | Stronger tests for critical decisions          | 12, 14     | Not started |
| 16   | Full CI enforcement and concise agent guidance | 13, 15     | Not started |
| 17   | Real-project pilot and usefulness assessment   | 16         | Not started |
| 18   | Safe adoption and updates where justified      | 17         | Not started |
| 19   | Release rehearsal and operating handover       | 18         | Not started |

| Checkpoint | Original slice     | What is usable                          | Continue when                                             |
| ---------- | ------------------ | --------------------------------------- | --------------------------------------------------------- |
| After 05   | A                  | Repaired commands and core CI           | F1–F7 are covered and required tools run                  |
| After 09   | B                  | Small verification engine               | Missing checks cannot masquerade as success               |
| After 13   | C                  | Reusable Next.js app and tested journey | Behaviour, permission, recovery and UI defects are caught |
| After 16   | D plus enforcement | Both language foundations and full CI   | Python boundaries and critical logic have evidence        |
| After 17   | E usefulness       | Measured adoption decision              | Benefits justify friction or the design is narrowed       |
| After 19   | E distribution     | Supported release candidate             | Upgrade/recovery rehearsal passes                         |

The first usable milestone is Step 05. Observe feedback time and developer
effort there; Step 17 synthesises those observations. Step 18 may retain
documented manual adoption if an updater does not earn its cost. This is an
implementation sequence, not an elapsed-time estimate; estimate remaining work
after Step 05.

## Design constraints and defaults

Keep the interface small: existing `setup`, `start`, `inspect`, `check`, `test`,
`smoke`; proposed `self-test`, `doctor`, `format`, `verify`. Preserve
target/config conventions. Native scripts remain usable directly. Scanners are
controls, not additional top-level commands by default.

```text
Reviewed stack and capabilities + repository evidence
  -> applicable controls with explicit reasons
  -> project-native tools and small adapters
  -> per-control results + evidence + overall exit
```

A control needs an ID, applicability, purpose, prerequisites, runner, scope,
required outcomes and a known failure case. Start with ordinary code and small
data structures. No remote control plane, agent orchestration, hosted telemetry,
generic rule language or dependency graph engine is needed.

| Area               | Starting choice                                                      | Boundary                                                      |
| ------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------- |
| TypeScript         | Prettier, ESLint, strict TypeScript                                  | Preserve equivalent existing tools                            |
| Next.js            | App Router, Vitest/Testing Library, Playwright                       | Test async server behaviour through the running app           |
| Python             | Ruff, Pyright, pytest                                                | Preserve an explicitly declared compatible runner             |
| Dependencies       | Existing manager and lockfile; uv for a new Python example           | Pin compatible versions during implementation                 |
| UI                 | Customer design system first; otherwise small owned shadcn-based kit | One primitive stack, semantic tokens, project-owned themes    |
| Storage            | Disposable database appropriate to the reference app                 | SQLite is a minimal proposed default, not PostgreSQL evidence |
| Reference use case | Synthetic customer work items with list, edit and save               | Demonstrate quality without building a large product          |
| Browsers           | Chromium desktop/mobile viewport first                               | Add Firefox/WebKit against the declared support matrix        |
| Platforms          | macOS is currently supported                                         | Linux requires runnable evidence; no implied Windows support  |

Use current official documentation when implementing and record exercised
versions. Newest package versions are not automatically compatible. The testing
split follows Next.js guidance on
[Vitest and async components](https://nextjs.org/docs/app/guides/testing/vitest)
and
[Playwright against production builds](https://nextjs.org/docs/app/guides/testing/playwright).

## Step 01 — Establish the baseline and acceptance cases

**Outcome:** implementation starts from current facts and independent behaviour
expectations. Refresh the existing audit, not the whole research exercise.

**Done when:** commands and missing tools are recorded; F1–F7 each have an
expected failure/pass pair; the critical scenarios later in this plan have
specific inputs/outputs; a lightweight measurement format exists. No repair is
claimed merely because its future acceptance test has been described.

```text
Implement Step 01 of plans/active/QUALITY_FIRST_HARNESS.md only.
Read and follow its execution contract and the repository instructions.

Refresh the existing audit against the current working tree. Run the existing
command/fixture matrix, distinguish missing tools from successful checks, and
preserve unrelated work. Define minimal regression cases for F1-F7 and concrete
acceptance cases for the synthetic Next.js work-item journey and Python
validation/import example. Use expected behaviour independent of implementation.

Record commands, exits, environment, failures and observed feedback time in
verification/QH-01.md. Create a lightweight measurement format for later steps;
do not invent historical effort or productivity. Do not repair runtime code in
this step. Link the evidence from the plan and stop.
```

## Step 02 — Separate application tests from harness tests

**Outcome:** `test` tests the application; `self-test` tests the harness. Fix
F1/F2 while retaining explicit overrides and declared unittest support.
Configure this repository's own root test command deliberately, without
recursion.

**Done when:** an installed harness plus a failing app test fails; absent pytest
cannot drop module-level cases; explicit unittest works; zero required tests
fail; both suites run independently with honest exit states.

```text
Implement Step 02 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Read F1/F2 and the dispatcher, resolver and
tests.

First reproduce failing application tests being hidden by harness self-tests,
and mixed pytest/unittest suites losing pytest cases when pytest is absent.
Add self-test and make test resolve the application's declared runner and local
environment. Preserve override precedence and explicit unittest projects.
Never switch runners because one is missing. Configure this repository's own
test command deliberately and avoid recursion.

Add regressions using disposable installed projects, including missing runners
and zero collected required tests. Run both suites and fixture commands, update
the intended managed inventory, document compatibility, and save before/after
evidence in verification/QH-02.md. Stop after this step.
```

## Step 03 — Unify discovery and honour command precedence

**Outcome:** files reach the correct tools and project commands control their
promised scope. Fix F3–F5 with shared harness-owned path discovery. Define
root-relative versus directory-component exclusions and symlink handling. Native
tools keep their own exclusions. Mandatory policy checks remain separate from
the single resolved project static-check implementation.

**Done when:** extensionless Python avoids shell tools; nested exclusions apply
consistently; excluded trees are pruned; traversal stays inside the intended
root; paths with spaces work; project overrides run once; policy failures block.

```text
Implement Step 03 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract and reproduce F3, F4 and F5 first.

Create the smallest shared walker/classifier needed by harness-owned checks.
Route supported shebangs correctly, define exclusion semantics, prune ignored
trees and prevent symlink escapes. Keep native tool configuration authoritative
for native scope. Resolve one project static-check implementation after required
policy checks. An explicit project override must not trigger automatic Python
checking as an additional hidden stage.

Test extensionless Python/shell, nested exclusions, spaced paths, symlinks,
failing mandatory policy and exactly-once project command invocation. Run real
installed tools where possible; report missing coverage. Reconcile the managed
inventory, write verification/QH-03.md, and stop.
```

## Step 04 — Preserve managed and project ownership

**Outcome:** normal customisation and generated environments preserve
installation health; shipped-file modifications stay visible. Fix F6/F7 using an
explicit release-owned inventory. Additional project skills are not shipped
skills.

**Done when:** added skills, `.venv`, dependencies and caches are allowed;
changed/missing shipped files fail; unsafe manifest paths and symlink
destinations are rejected; regeneration never absorbs customer files or local
secrets.

```text
Implement Step 04 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract and reproduce F6 and F7 first.

Make release ownership explicit rather than treating every file under shared
folders as managed. Preserve shipped-file checksum checks while allowing project
skills and runtime environments. Validate manifest paths and symlink handling.
Do not build the installer yet or regenerate away a consumer conflict.

Exercise a disposable full installation with a project skill, a real no-pip
virtual environment, caches, modified/missing shipped files and unsafe paths.
Prove release generation contains only intended inputs. Document ownership and
compatibility, run required checks, write verification/QH-04.md, and stop.
```

## Step 05 — Add CI for the repaired core

**Outcome:** clean environments run the repaired contract with actual required
tools. Use existing CI, or a thin GitHub Actions workflow when none exists.
Start with macOS. Install ShellCheck, shfmt and Markdown tooling; do not depend
on warning-only coverage. Pin tools/runtimes and install locked dependencies.

**Done when:** a clean setup runs the suite; deliberate failures reach the
correct jobs; remote execution is evidenced or explicitly unverified. A workflow
file alone does not establish successful CI or branch protection.

```text
Implement Step 05 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add a small CI workflow for the repaired harness
and existing fixtures, using the current provider or a documented GitHub Actions
default. Preserve macOS support; pin compatible tools, runtimes and action refs.

Actually run relevant shell, Markdown, TypeScript and Python checks, self-tests,
fixture tests and smoke. Fix exposed in-scope defects without blanket disables.
Use locked installs, bounded jobs, temporary data and useful logs. Show negative
fixtures fail without leaving the working tree broken. Do not change remote
protection settings. Record a remote run if authorised and available; otherwise
mark execution unverified. Write verification/QH-05.md and stop.
```

## Step 06 — Resolve relevant profiles and prerequisites

**Outcome:** projects see applicable controls and actionable prerequisite gaps.
Add `doctor` and small validated language/framework/capability configuration.
Detection proposes; reviewed settings persist. Unsupported capabilities are
explicit gaps, not imaginary controls. Multi-package projects need declared
roots and aggregation, or an explicit unsupported result.

**Done when:** Python-only projects have no browser requirements; Next.js
selects TypeScript/framework checks; contradictions cannot remove requirements;
missing prerequisites fail readiness. Schema changes preserve project ownership
through tested compatibility or a reviewable migration. Existing
readiness/security fields gain real semantics or honest unsupported/deprecation
diagnostics.

```text
Implement Step 06 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add shared profile/capability resolution and a
thin doctor command. Detection must not rewrite reviewed requirements or infer
that a missing tool makes a control unnecessary. Explain selection reasons.

Support TypeScript/Python and Next.js as a framework. Add capabilities only with
an implemented control or visible unsupported result. Treat multi-package roots
explicitly. Resolve inert readiness/security fields; require only relevant
context. Preserve old config via tested compatibility or reviewable migration,
not automatic replacement of project-owned files. Avoid a generic policy DSL.

Test plain Python, TypeScript, Next.js, mixed roots, missing tools,
contradictions and unsupported capabilities. Update actual context, write
verification/QH-06.md, and stop.
```

## Step 07 — Delegate formatting and static quality to native tools

**Outcome:** `format` fixes mechanical formatting; `check` reports remaining
issues without rewriting files. Use locked, project-local tooling. For new
profiles use Prettier/ESLint/strict TypeScript and Ruff/Pyright. Add only
concrete import boundaries: domain code separated from I/O and server-only
modules kept out of clients. File/function size remains advisory.

**Done when:** formatting is idempotent; check mode changes no tracked files;
required missing tools fail; seeded type, lint and import-boundary defects are
caught; an existing equivalent toolchain remains in control. Installed fixture
dependencies and relevant maintained source are actually included.

```text
Implement Step 07 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add format as a thin delegate to project-local
native formatters, and make check enforce declared static tools without edits.
Preserve existing tools and package managers. Use compatible pinned defaults
for new TypeScript and Python projects; keep settings in native config files.

Cover strict types, runtime-boundary coding conventions through appropriate
lint rules, and a few concrete import boundaries. Do not reimplement linters
with regexes or turn source-size guidance into hard gates. Update shipped
standards to describe real command behaviour, not obsolete optional fallbacks.

Prove formatter idempotence, non-mutating check mode, missing-tool failure and
seeded type/lint/import violations in isolated fixtures. Verify meaningful
maintained source is in scope. Write verification/QH-07.md and stop.
```

## Step 08 — Make complete verification produce trustworthy evidence

**Outcome:** `verify` runs the full applicable suite and emits a validated JSON
report plus a readable summary. Reuse resolution from Step 06. Do not build a
parallel scheduler. Native runner output supplies collection and outcomes.

Each control reports `passed`, `failed`, `unavailable` or `not-applicable` with
a reason. A required failed/unavailable control makes full verification
non-zero. A local selected subset is visibly partial and cannot be presented as
complete. Unexpected skips, flaky retries and absent artifacts cannot disappear
into a success count. Opaque custom runners need a documented evidence adapter
before claiming complete test verification.

Record source revision and working-tree input digest, selected configuration,
lockfiles, harness/tool versions, scope, commands with secrets redacted, exit
codes, duration, collection/skips/retries and artifact hashes. Include relevant
untracked source; exclude declared output directories so writing the report does
not invalidate itself. Detect input changes during execution. Treat this as
provenance, not a cryptographic guarantee against a malicious editor.

**Done when:** clean/failing/unavailable/partial runs have correct reports and
exits; zero collection and malformed/missing artifacts fail; an input edit makes
old evidence stale; timeouts and interrupts terminate owned child processes;
logs are bounded and synthetic secret markers are redacted.

```text
Implement Step 08 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Build verify as a thin coordinator of the shared
applicable controls. Produce schema-validated JSON and a short human summary.
Use native runner reports for counts and outcomes; never invent collection data
from a successful shell exit. Make missing required evidence fail explicitly.

Implement honest per-control states, overall completeness and non-zero exits for
required failures/unavailability. Preserve retries/skips. Fingerprint actual
source, including relevant untracked files, config and locks; exclude generated
reports. Reject stale evidence and detect inputs changed mid-run. Bound logs,
redact secrets and clean up owned processes on timeout or interruption.

Test success, failure, zero tests, missing/malformed reports, partial scope,
stale inputs, flaky retries, interrupts and secret redaction. Prove report
writing does not invalidate its own input identity. Document the trust limits,
write verification/QH-08.md, and stop.
```

## Step 09 — Add executable security checks and test isolation

**Outcome:** secret, dependency and applicable static security checks run as
programs. Test execution uses scoped synthetic environments. This adds evidence
about specific threats; it is not a complete security certification.

Select maintained tools at implementation time, favouring existing project/CI
capabilities. Keep scanning local where practical. Pin tools and rule sets;
record advisory data source/time. Separate policy findings from scanner failure,
missing tools and unavailable/stale advisory data. Define blocking severities
and narrow owner/reason/expiry exceptions in reviewable configuration.

Populate the harness trust model in `docs/SECURITY.md`: configured commands are
executable repository code; the harness is not its own sandbox. Do not expose
real secrets to untrusted pull requests. Use external runtime/CI controls for
network isolation, with only necessary local test services. If egress cannot be
enforced on a supported environment, say so and leave that guarantee unverified.

**Done when:** fake secret and vulnerable-advisory fixtures trigger findings;
clean cases pass; scanner failure cannot pass; model-provider/production
attempts are blocked in the verified isolated setup; output does not disclose
test secrets.

```text
Implement Step 09 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Select a minimal maintained programmatic security
baseline for secrets, locked dependencies and applicable source checks. Prefer
existing native/CI tools, pin versions and record advisory provenance. Separate
findings, errors and unavailable data; no automatic fixes or blanket ignores.

Define reviewable severity/exception rules and fill the actual harness security
context. Separate dependency/advisory setup access from application test access.
Use synthetic secrets, scoped environments and external runtime/CI isolation to
prevent production and model-provider calls during verification. Do not claim
that a text rule or URL regex is an effective network sandbox.

Test representative findings, safe cases, expired exceptions, scanner failure,
missing data, secret redaction and denied egress in the supported setup. Record
remaining environment limits in verification/QH-09.md and stop.
```

## Step 10 — Build a real Next.js foundation with reusable UI

**Outcome:** a real production-buildable Next.js example replaces the current
fixture as evidence about Next.js. Keep the lightweight Node fixture for command
routing tests. Suggested new location: `examples/nextjs-app/`, outside managed
harness internals, with its own native scripts and project configuration.

Build only the synthetic work-item list/detail/edit interface and the components
it needs: button, field, error message, dialog/confirmation, navigation and a
simple table/list. Use semantic tokens and two visibly different themes with the
same component APIs. Add loading, empty, error, no-access and success examples.
Keep a small rendered catalogue; do not install a documentation platform just
for it. Use existing customer assets first; no customer assets are assumed here.

**Done when:** the actual app builds and runs; relevant `.tsx` source is
checked; components have interaction tests; both themes reuse the same
implementation; example data is labelled synthetic. Persistence/security are
still pending until Step 11; fixture stubs must not be described as live
integrations.

```text
Implement Step 10 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add a real Next.js/TypeScript reference app with
compatible pinned dependencies, native scripts and its own harness config.
Retain the lightweight Node dispatcher fixture. Keep example app source outside
managed harness internals and document source/dependency ownership.

Build a small synthetic work-item list/detail/edit UI using an approved local
component kit, semantic tokens and two themes sharing component implementations.
Prefer existing assets; otherwise use a small owned shadcn-based foundation with
one primitive stack. Add only needed controls and loading/empty/error/no-access/
success examples. Keep browser state in small Client Components and use Server
Components appropriately. Document components, variants and reuse rules.

Run the real production build and initial component/navigation checks. Label
stubbed data and pending persistence/auth accurately. Populate relevant design
context, write verification/QH-10.md, and stop.
```

## Step 11 — Implement secure mutations and real persistence

**Outcome:** an authorised synthetic user can edit a work item and reload the
saved result. A denied user cannot read or mutate another user's/tenant's data.
Use the selected local database engine for real persistence; test its actual
transaction behaviour, not an in-memory repository substitute.

Keep server entry points thin, runtime-validate input and enforce identity,
role, ownership and tenant scope at the data boundary. Return minimal response
shapes and safe errors. Use a maintained auth/session library where practical;
do not invent cryptography. Synthetic local identities must exercise the actual
session verification and authorisation path. Test adapters are explicit and
cannot enable a production bypass. External SSO remains unverified unless
tested.

Choose a freshness/caching policy explicitly; any cache must preserve isolation
and invalidate after writes. Avoid blanket caching. Define migration/seed/reset
commands for disposable storage and basic failure/recovery semantics. This
follows Next.js
[data-security guidance](https://nextjs.org/docs/app/guides/data-security).

**Done when:** direct server tests prove allowed and denied cases; invalid input
cannot write; a save survives a new read/process; a simulated storage failure
cannot leave a partial committed result; errors/logs omit secrets; cached reads,
if used, neither leak nor remain incorrectly stale.

```text
Implement Step 11 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Replace the reference app's persistence stubs
with a disposable real database and secure server operations. Use synthetic
local identities through actual session handling; use a maintained library and
no hand-written cryptography or production auth bypass. Label untested SSO.

Implement runtime validation, resource/role/tenant authorisation, minimal DTOs,
safe errors and a deliberate freshness policy. Keep domain decisions testable
separately from I/O. Add repeatable migration/seed/reset commands that refuse
unsafe production targets. Update data and security context for actual
behaviour.

Before UI-only checks, test direct server entry points for allowed,
unauthenticated, wrong-role, wrong-owner, wrong-tenant and invalid-input cases.
Include expired sessions, malicious input and rejected unsafe mutation origins
where relevant. Verify safe rendering, committed storage after reload/restart,
rollback on relevant failure and cache isolation if caching exists. Write
verification/QH-11.md and stop.
```

## Step 12 — Prove complete user and recovery journeys

**Outcome:** browser tests demonstrate customer actions and resulting state, not
just page availability. Run Playwright against the built Next.js application
with isolated storage, fixed data and controlled time where relevant.

Cover list/detail, edit/save/reload, invalid input, cancellation, duplicate
submission, permission denial and recoverable save failure. Validate persistence
through the real data path. Fault injection happens at the dependency that
fails; do not mock the action under test. Keep fixture fault controls out of
normal production routes. Native reports feed Step 08's evidence adapters.

**Done when:** main and recovery journeys pass; replacing save with a no-op
fails; an authorisation defect fails direct-boundary tests; invalid data remains
absent from storage; unexpected browser errors fail; servers/storage are cleaned
up. The `smoke` script is a small meaningful subset, not an HTTP 200 probe.

```text
Implement Step 12 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add Playwright journeys against the production
build and real disposable persistence. Test list/detail, edit/save/reload,
validation, cancellation, repeated submission, denied access and save recovery.
Use stable semantic locators and isolated fixtures; avoid arbitrary sleeps.

Assert user-visible outcomes plus durable data changes. Inject failures at an
explicit test dependency boundary, not by mocking the operation being verified.
Keep test fault controls out of normal production paths. Define a small real
smoke journey, feed native results to verify, and clean up processes/storage.

Demonstrate that a broken save handler and a representative access-control
regression are caught in disposable copies. Treat unexpected console/page errors
as failures, with narrowly documented expected errors for deliberate negative
cases. Write verification/QH-12.md and stop.
```

## Step 13 — Protect accessibility, appearance and responsiveness

**Outcome:** applicable UI regressions have repeatable programmatic detection.
Use axe plus explicit keyboard/focus tests, screenshot comparison and a small
set of measured performance budgets. Do not add an AI visual judge.

Cover desktop and mobile viewports, both themes and the important states.
Exercise tab order, field labels, invalid-form announcements, dialog
focus/return, escape behaviour, visible focus, reduced motion and overflow.
Declare the browser matrix and add relevant Firefox/WebKit journeys before
claiming their support.

Capture screenshots with pinned browser/OS/fonts, locale, data and animation
settings. Generate initial candidate baselines, then obtain intentional human
acceptance before treating them as approved. Later changes produce inspectable
diffs. Never auto-update baselines after failure. Steps independent of baseline
approval may continue; visual acceptance remains incomplete until resolved.

Automated scans have
[accessibility limits](https://playwright.dev/docs/accessibility-testing), and
pixel comparisons need a
[consistent environment](https://playwright.dev/docs/test-snapshots). They do
not establish customer usefulness or visual taste.

**Done when:** seeded missing-label/focus, overflow and visual defects fail the
appropriate checks; approved screenshots compare consistently; a controlled
budget breach fails. Performance thresholds follow repeatable measurements and
stated hardware/network conditions, not an arbitrary overall Lighthouse score.

```text
Implement Step 13 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add programmatic axe, keyboard/focus, responsive,
visual-regression and limited performance checks to the real Next.js example.
Cover the declared viewports, themes, browsers and meaningful UI states.

Pin visual conditions and produce candidate screenshots for human acceptance;
do not impersonate approval or auto-accept failed diffs. Use actual measurements
to propose justified bundle/runtime budgets and label lab metrics accurately.
Keep assertion tolerances narrow and explain masks or exclusions.

Seed representative label/focus, overflow, appearance and budget regressions in
disposable copies and show the correct checks fail. Integrate evidence with
verify. Document remaining human acceptance and accessibility limits in
verification/QH-13.md. Stop after the implemented scope; independent work may
continue while any actual baseline approval remains pending.
```

## Step 14 — Prove a useful Python application

**Outcome:** Python support handles meaningful inputs, domain behaviour,
persistence and failure. Keep the tiny existing server for dispatcher tests.
Suggested new location: `examples/python-work-items/`.

Default to a small CLI that validates synthetic work-item records, imports them
atomically into a disposable SQLite database and queries the saved results.
Change to a service only if an actual pilot requires an API. Use typed
boundaries, clear exit/error behaviour and a strict core. New projects may use
uv with a committed lock; existing managers stay authoritative. CI must check
lockfile freshness, following
[uv's locked workflow](https://docs.astral.sh/uv/concepts/projects/sync/) when
that manager is selected.

**Done when:** valid import/query works; malformed data, duplicate identifiers
and storage errors fail predictably without unintended partial writes; real
subprocess tests inspect exits/stdout/stderr; collection is complete; the actual
database is checked; Ruff, Pyright and pytest run in the declared environment.

```text
Implement Step 14 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Add a substantive Python reference project while
retaining the lightweight dispatcher fixture. Unless a real pilot establishes
an API need, implement a small typed CLI for validating, atomically importing
and querying synthetic work items in a disposable real SQLite database.

Separate pure domain rules from file/database I/O. Use Ruff, Pyright and pytest
through native project commands and a reproducible environment; preserve an
existing manager or use uv with lock freshness checked. Add no web framework
without an actual requirement. Label data provenance and document CLI contracts.

Test real process exits/output, invalid input, duplicate records, successful
persistence, transaction failure and cleanup. Wire format/check/test/smoke and
verify into the Python profile. Seed an actual boundary defect to demonstrate
failure detection. Write verification/QH-14.md and stop.
```

## Step 15 — Establish that important tests detect wrong behaviour

**Outcome:** critical TypeScript and Python decisions have stronger evidence
than a coverage percentage. Add property tests for meaningful invariants and
bounded mutation checks for selected pure logic. Choose compatible maintained
tools during implementation, and keep slow campaigns outside the fast loop.

Example invariants: invalid operations cannot create stored records; a tenant
cannot gain access by changing only a record ID; valid normalisation is
idempotent; failed atomic imports leave storage unchanged. Select invariants
that fit the implemented contract, not all examples mechanically.

**Done when:** intentionally changed critical decisions are caught; remaining
survivors are explained and addressed; seeds/failing examples are retained;
coverage exposes meaningful gaps without a universal 100% target. A mixed
Next.js/Python API needs real contract tests only if such an integration exists.

```text
Implement Step 15 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Review the critical scenario contract and tests
in both reference apps. Add a small set of meaningful generated-input invariants
and targeted mutation checks for critical pure validation/permission decisions.
Use maintained compatible native tools, deterministic seeds and saved failures.

Demonstrate that selected wrong decisions cause tests to fail. Investigate
surviving mutations; do not lower thresholds or add exclusions merely to pass.
Use coverage to identify missing branches, not as a universal quality score.
Keep mutation scope/runtime bounded and its cadence separate from quick
feedback.
If a real mixed-stack API exists, test its request/error/auth contract across
both sides; otherwise record that integration as not applicable.

Write verification/QH-15.md with detected defects, unresolved survivors, cost
and scope limitations. Stop after this step.
```

## Step 16 — Enforce the full policy and simplify agent guidance

**Outcome:** full applicable checks run in CI independently of an agent's
completion claim; agents receive concise relevant instructions.

Extend Step 05's workflow to both real examples, security, browser checks and
required evidence. Keep unit/static feedback fast, with explicit broader jobs
for relevant capabilities. Expensive mutation checks may use a separate release
cadence; no partial PR run may claim that the full release suite passed.
Required jobs must not accidentally disappear through path filters or
cancellation.

Prepare protected review for workflows, harness policy, test configuration,
exceptions and visual baselines. Use existing CI/CODEOWNERS capabilities and
verified maintainers; do not invent usernames. Rule enforcement is repository
configuration outside a checked-in file. Prepare exact changes and, where
required, obtain owner approval before applying them. Verify actual settings
before claiming protection. See
[protected branch controls](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Reduce `AGENTS.md` and skills to workflow maps, reuse rules and relevant command
links. Preserve obligations; replace duplicated prose with implemented native
configuration. Changes to shipped skills need the normal managed-file process.
Keep the global entry point short; no large always-loaded component catalogue.

**Done when:** a failing app, missing artifact and weakened policy change are
visible at the correct boundary; fast/full scopes cannot be confused; CI has no
model-provider credentials; guidance matches commands. Record prepared versus
actually enforced controls separately. Local pilots may proceed with that
limitation while external protection approval is pending; release claims cannot.

```text
Implement Step 16 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Extend core CI to run the full required policy
for both real examples, including security, browser and evidence checks. Define
fast feedback and full release scopes with honest completeness. Avoid path
filters, cancellation or continue-on-error hiding required failures.

Prepare independent protection of gate/config/test/baseline changes using the
existing CI provider and real maintainer ownership. Do not claim protection from
YAML or CODEOWNERS alone. Prepare reviewable remote-setting changes and follow
required owner approval before applying them; verify settings when available.

Simplify agent instructions and shipped skills to relevant workflow maps and
reuse guidance. Do not add AI reviewers or an orchestration layer. Prove failure
propagation and missing-artifact handling, and record local/remote evidence and
pending external controls in verification/QH-16.md. Stop.
```

## Step 17 — Measure usefulness on real projects

**Outcome:** decide which controls deserve broader adoption based on evidence.
Use an actual Next.js project, a Python project and an established repository
with its own conventions. A project can satisfy two categories; include at least
one real case for each, and disclose the number of distinct projects. Repository
locations/access are owner inputs, not facts to guess.

Start with read-only inspection and a reversible adoption patch. Preserve native
types/tests/CI in the comparison baseline. Use naturally requested development
work plus programmatic replay of representative defects; no extra model runs or
AI judges are needed for the evaluation. A suggested small pilot covers a
feature, defect repair and shared-component/domain change in each applicable
project. This yields directional evidence, not statistical proof.

Compare baseline tools with the added harness using the same acceptance cases,
environment and time accounting. Separate benefits from new shared components
from benefits of the command wrapper. Record setup/maintenance time as well as
saved correction time. Do not time only successful runs or omit failed attempts.

**Done when:** the report includes measured benefits/costs, limitations,
controls to keep/change/remove and a justified recommendation. Representative
critical seeded defects must be caught; pilot work must not weaken existing
controls. Agree a practical feedback-time budget from observed use before
evaluating it. If benefits are unclear, improve the narrow failing part before
distribution.

```text
Implement Step 17 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Use the measurement records already collected.
Identify owner-authorised real Next.js, Python and established-toolchain pilot
projects; if paths/access are missing, prepare the concrete pilot protocol and
ask for those inputs without inventing results or mutating unrelated projects.

Compare existing native engineering controls with the added harness through
actual requested changes and deterministic defect replay. Keep acceptance cases
and environments comparable. Measure task outcomes, escaped defects, review/
rework, setup, feedback time, flaky/false failures and maintenance cost.
Separate foundation reuse from harness-wrapper benefit; launch no extra AI
evaluations.

Write verification/QH-17.md with raw evidence, limitations and explicit keep/
change/remove recommendations. Prepare fixes for observed harness problems as
bounded follow-up tasks. Do not build distribution tooling until this checkpoint
supports it. Stop with the evidence-backed decision.
```

## Step 18 — Make adoption and updates safe where they earn their cost

**Outcome:** repeated use preserves project context and customisations.
Implement only the adoption/update operations justified by Step 17. A small
documented copy/diff procedure remains valid when automated distribution is not
justified.

An automated path starts with dry-run inspection and a file-level proposal.
Distinguish absent files, unchanged managed files, modified managed files and
project-owned files. Never overwrite project-owned context/configuration or
customer components. Propose side files or a reviewable merge. Validate version
compatibility, paths, source checksum and ownership before writing. Checksums
show integrity against an inventory; do not claim they authenticate an unknown
remote publisher. Use a trusted pinned local/release source.

Updates need backups, a transaction journal or equivalent, crash-safe recovery
and guarded rollback that preserves subsequent user edits. Runtime state stays
outside the release inventory. A shared component package is conditional on
multiple consumers needing the same contract; upgrade consumers deliberately.

**Done when:** dry-run changes no files; apply is idempotent; conflicts stop
safely; interrupted writes recover; rollback preserves later edits; custom
skills, config and themes survive; malicious paths are rejected. Exercise local
copies, not live customer repositories, for destructive fault tests.

```text
Implement Step 18 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract and the Step 17 adoption decision. Implement only
justified distribution needs. If manual adoption is sufficient, deliver and
rehearse a precise copy/diff/update procedure instead of a general installer.

For automation, start with a non-mutating file-level plan using the explicit
release inventory. Preserve project-owned files and modified managed content;
propose merges/side files. Check compatibility, paths and trusted source before
writes. Provide recoverable apply, idempotence and rollback guarded against
subsequent edits. Keep component distribution separate from harness ownership.

Test clean adoption, conflicts, added skills, customised themes, generated
state, interrupted writes, repeated apply and rollback in disposable projects.
Extract a shared component package only if multiple consumers justify it.
Write verification/QH-18.md with recovery evidence and stop.
```

## Step 19 — Rehearse release and hand over operation

**Outcome:** a new maintainer can start, verify, troubleshoot and update
supported projects from accurate instructions. This produces a local release
candidate; public release/deployment is a separate authorised action.

Rehearse from a clean environment with a new TypeScript/Next.js project, a
Python project and an existing project with custom conventions. Run complete
applicable checks, confirm deliberate defects fail, and rehearse recovery.
Record exact supported runtimes, platforms, tools, profile capabilities and
limitations.

Replace obsolete phase references and template status only where implemented
facts justify it. Complete relevant product/design/data/security context,
command reference, maintenance ownership, dependency update cadence and failure
recovery instructions. Keep examples and component contracts small. Define how a
control can be deprecated without silently reducing a consumer's required
verification.

**Done when:** onboarding and recovery are reproducible; no implemented scope is
misrepresented; all required evidence and actual approvals are linked; remaining
debt has concrete owners/triggers. Move this plan to completed only when its
criteria really hold, updating inbound links so they remain valid.

```text
Implement Step 19 of plans/active/QUALITY_FIRST_HARNESS.md only.
Follow its execution contract. Rehearse a local release candidate in clean
supported environments for new Next.js/Python projects and an existing project
with custom conventions. Verify full checks, representative failure detection,
adoption/update recovery and absence of verification model calls.

Reconcile documentation with implemented capabilities, remove obsolete phase
claims, and publish no unsupported guarantees. Document versions, ownership,
setup, relevant controls, evidence, troubleshooting, update policy and recovery.
Link real CI/protection/visual acceptance evidence; keep gaps explicit. No
public release, deployment or production access is authorised by this prompt.

Write verification/QH-19.md. Mark the plan complete and move it to completed
only if all completion criteria are evidenced; update inbound links.
Otherwise leave it active with precise outstanding work. Stop with the
release-readiness result.
```

## Critical acceptance scenarios

Step 01 turns these contracts into specific synthetic inputs and assertions.
Later tests reference stable IDs; the harness need not build a requirements
management system. Add cases only for capabilities a project actually exposes.

| ID  | Behaviour                                            | Minimum proof                                                             | First complete evidence |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------- |
| H01 | Installed harness executes app tests                 | Deliberately failing app test produces failure with harness suite present | 02                      |
| H02 | Missing runner cannot reduce collection              | Mixed suite plus absent declared runner fails explicitly                  | 02                      |
| H03 | Source scope is honoured                             | Shebang, nested exclusion and override regressions                        | 03                      |
| H04 | Project ownership survives                           | Custom skill/venv allowed; shipped modification detected                  | 04                      |
| H05 | Missing verification cannot pass                     | Missing tool, zero tests, skips, stale/malformed evidence fail            | 08                      |
| H06 | Verification does not call model/production services | Enforced test isolation plus denied-call cases in supported runtime       | 09                      |
| N01 | Authorised edit persists                             | Browser save, reload and independent stored-state assertion               | 12                      |
| N02 | Invalid input is safe and understandable             | Field feedback and no invalid committed change                            | 12                      |
| N03 | Access is enforced at the server                     | Direct unauthenticated, wrong role/owner/tenant cases                     | 11                      |
| N04 | Failed save can recover                              | Preserved input, safe error, retry and correct durable result             | 12                      |
| N05 | Repeated submission is safe                          | One intended operation/result despite repeat action                       | 12                      |
| N06 | UI works across themes and viewports                 | Same journey/keyboard assertions and accepted screenshot comparisons      | 13                      |
| N07 | Supported UI budgets are respected                   | Explicit measured budget breach is detected                               | 13                      |
| P01 | Valid Python input is processed                      | CLI/API result plus real stored state                                     | 14                      |
| P02 | Bad input/failure cannot partly commit               | Negative process/transaction assertions                                   | 14                      |
| Q01 | Critical tests detect changed logic                  | Targeted mutations and preserved generated failure examples               | 15                      |
| C01 | Required CI and review controls are effective        | Actual job results and protection configuration evidence                  | 16                      |
| A01 | Adoption/update preserves user work                  | Conflict, interruption and rollback fixtures                              | 18                      |

## Verification cadence

| When                      | Run                                                                            | Result may claim                                      |
| ------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------- |
| While editing             | Native formatter, focused lint/types and relevant tests                        | Only the explicitly tested scope                      |
| Before completing a step  | Repository checks, self-tests for harness changes, applicable app/smoke checks | That step's acceptance evidence                       |
| Pull request              | Full applicable required PR controls and new regressions                       | PR policy satisfied at its tested revision            |
| Reference release         | Full app, browser, security, mutation and adoption suites as declared          | Supported release policy satisfied                    |
| Intentional visual change | Programmatic comparison plus explicit baseline acceptance                      | Reviewed appearance; no automatic usability guarantee |

No aggregated quality score can compensate for a safety failure. Full acceptance
requires every applicable required control; `not-applicable` needs a reason. A
passing retry remains a recorded flaky event and is governed by explicit policy.
Exceptions use owner, scope, rationale and expiry; they are never hidden.

## Pilot measurement and decision rules

| Measure        | Record                                                              | Interpretation                                       |
| -------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| Correctness    | Accepted scenarios and defects found after completion               | Distinguish genuine behaviour from test-count growth |
| Safety         | Missed/detected seeded boundary defects; observed incidents         | No production exposure is needed for probes          |
| Human effort   | Actual review, correction, setup and maintenance minutes            | Include the cost of adopting the harness             |
| Feedback speed | Cold/warm setup and check durations, including failures             | Report environment and repeated observations         |
| Reliability    | First-run failures, retries, false positives and unavailable checks | Do not discard inconvenient runs                     |
| Consistency    | Reused component/pattern contracts and customer deviations          | Intentional brand differences are valid              |
| UX             | Journey/recovery results and separate human acceptance              | Automated conformance is not product usefulness      |

Retain a control when it catches relevant failures or removes recurring effort
at an acceptable cost. Narrow noisy controls before making them mandatory. If
local feedback is too slow, improve reuse/caching/selection while preserving the
full required CI scope. Do not weaken the correctness definition to improve a
reported metric. A small pilot supports an adoption decision, not a universal
productivity percentage or a claim that the harness guarantees safe software.

## Inputs and approvals needed later

Planning needs no additional answers. Routine reversible implementation choices
can follow the defaults above and record their rationale. The following inputs
are genuinely external; ask only when the relevant concrete work is ready.

| Input                                                             | Needed by | Continue independently with                                            |
| ----------------------------------------------------------------- | --------- | ---------------------------------------------------------------------- |
| Intended visual appearance and baseline acceptance                | 13        | Candidate screenshots and programmatic interaction checks; Python work |
| Real maintainer IDs and authority to change remote protection     | 16        | Local workflow, policy proposal and negative fixtures                  |
| Actual authorised pilot repository paths and customer constraints | 17        | Reference apps and a complete pilot protocol                           |
| Feedback-time tolerance based on observed workflow                | 17        | Recorded measurements and a justified proposed budget                  |
| Publication/release decision                                      | After 19  | Local release candidate, changelog and recovery instructions           |

These approvals do not replace tests or require AI reviewers. The repository's
existing approval rule applies to destructive changes, external publication,
production access, security trade-offs and irreversible migrations.

## Risks and recovery

| Risk                                     | Prevention and recovery                                                         |
| ---------------------------------------- | ------------------------------------------------------------------------------- |
| Building too much infrastructure         | Stop at usable checkpoints; require Step 17 evidence before distribution        |
| Tests repeat a model's wrong assumptions | Define cases first; use direct boundaries, negative cases and mutation evidence |
| Agent weakens its own checks             | Separate CI execution and protected review; keep trust limits explicit          |
| UI tests become slow or flaky            | Stable data, semantic locators, controlled rendering and small critical suites  |
| Existing conventions are overwritten     | Dry-run proposals, explicit ownership, conflict detection and guarded rollback  |
| Docs describe future work as delivered   | Update facts only with evidence and separate prepared from enforced controls    |
| Example app becomes a product platform   | Keep one bounded workflow; add capabilities only after real project demand      |
| Dependency churn breaks templates        | Pin compatible versions and test upgrades in consumers before propagation       |

Use one reviewable change per bounded task. Keep source/schema migrations
compatible where practical. Roll back a failed local harness change through a
reviewed patch or branch operation that preserves unrelated work; never reset a
customer's working tree to recover the harness. Database fault tests and
migration rehearsals use disposable storage, with no production credentials.

## Completion criteria

- [ ] F1–F7 are fixed with before/after behavioural evidence.
- [ ] Application tests and harness self-tests are independent.
- [ ] Required missing tools, absent cases and invalid evidence block
      completion.
- [ ] Profile/capability selection exposes only relevant implemented controls.
- [ ] TypeScript, actual Next.js and Python paths run their native tools.
- [ ] Next.js journeys prove persistence, permission, validation and recovery.
- [ ] Reused UI behaves consistently across themes and supported viewports.
- [ ] Visual baselines have deliberate acceptance; no AI judge grades them.
- [ ] Python behaviour, boundaries and failure cases have meaningful coverage.
- [ ] Critical test strength is demonstrated through negative/property/mutation
      cases.
- [ ] Verification has no model-provider calls and reports its isolation limits.
- [ ] Results are bound to tested inputs, configuration, tools and artifacts.
- [ ] Local partial results and full CI/release results are distinguishable.
- [ ] Claimed CI protections are verified, not merely configured in files.
- [ ] Real-project pilot evidence supports the retained scope and trade-offs.
- [ ] Adoption/update/recovery is proven at the justified level of automation.
- [ ] Canonical documentation matches the supported implementation.
- [ ] Final evidence is linked before moving the plan to completed.

## Current status

This expanded plan and its prompts were authored on 2026-10-01. Step 01 was
executed separately against the current dirty tree: see
[TASK-004](../../tasks/TASK-004-QUALITY-BASELINE.md) and
[QH-01 evidence](../../verification/QH-01.md). The refreshed matrix, F1-F7
regression contracts, synthetic application cases and measurement format are
recorded. Runtime code was not repaired. The baseline remains partial, with
F1-F7 open, missing tools and undefined root smoke explicitly retained.

Step 02 is complete: [TASK-005](../../tasks/TASK-005-APPLICATION-TEST-ROUTING.md)
and [QH-02](../../verification/QH-02.md) record F1/F2 reproductions, installed-copy
regressions, separate application/self-test commands, declared Python runners,
zero-collection failures and compatibility. That run had 28 passing kit cases;
fixture smoke checks pass after recorded sandbox retries. Static tool gaps and
undefined root smoke remain visible; F3-F7 are not repaired.

Step 03 is complete: [TASK-006](../../tasks/TASK-006-DISCOVERY-AND-CHECK-PRECEDENCE.md)
and [QH-03](../../verification/QH-03.md) record F3–F5 reproductions, shared
discovery, exclusion/shebang/symlink contracts and single static implementation
resolution after policy checks. Both root suites pass 46 cases, including 18
new regressions. Both fixture smokes pass after recorded permission retries;
optional native tool gaps and undefined root smoke remain visible. Managed
ownership findings F6–F7 remain for Step 04.

Step 04 is next eligible. No later step has started, and future application
journey acceptance cases remain specifications, not execution evidence.
