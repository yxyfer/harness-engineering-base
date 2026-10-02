# Product Context

Status: current product direction; target capabilities are not yet implemented

Updated: 2026-10-01

## Purpose

Help a coding agent deliver safe, usable, maintainable customer applications by
making approved patterns easy to reuse and required verification executable.

The harness should improve three outcomes, in this order: application safety
and correctness, user experience, and code maintainability. Consistency and a
fast development loop support all three. A high score in one area must never
cancel a blocking failure in another.

The product has two parts: a small verification engine and reusable application
foundations. Instructions direct the coding model to those assets and commands.
All automated testing and gate decisions use programmatic tools; no additional
AI reviewers, LLM judges, or model calls are part of verification.

This is a target vision. The [audit](../verification/AUDIT_2026_10_01.md)
records today's behaviour and defects. The
[delivery plan](../plans/active/QUALITY_FIRST_HARNESS.md) defines the next work.

## Users and jobs

Step 10 adds the real [Next.js reference](../examples/nextjs-app/README.md),
separate from the lightweight Node dispatcher fixture. It demonstrates synthetic
list/detail/browser-edit previews, shared components and two token themes.
Step 11 adds actual synthetic credential sessions, owned/tenant/role permissions
and disposable SQLite saves; SSO/production remain unsupported. Native Step 13
axe/keyboard/reflow and lab budgets do not establish accessibility conformance
or field performance. Visual baselines await human acceptance.
Step 12 proves authenticated user and recovery journeys against production and
actual storage, including dependency failure and permission denial. See
[QH-12](../verification/QH-12.md); human acceptance remains separate.

Step 07 implements native format/check delegation and required static-tool
failure, with opt-in strict Python/TypeScript defaults. Native boundary rules
protect the demonstrated layout; this is not complete runtime validation.
See [QH-07](../verification/QH-07.md) and the Step 10 foundation above.

Step 06 now implements read-only applicability and prerequisite diagnosis for
Python, TypeScript and Next.js. Step 10 adds initial native build/navigation
verification; broader browser controls remain pending. Step 09 adds narrow
native security checks and external macOS
direct-egress isolation, not security certification. Multi-package
aggregation is explicitly unsupported. See [QH-06](../verification/QH-06.md).

| User or actor | Job to be done | Current pain | Success signal |
| --- | --- | --- | --- |
| Application developer and coding agent | Make a bounded change correctly | Repeated setup, inconsistent patterns, uncertain verification | Required behaviour passes without unrelated regressions |
| Customer and end user | Complete a task safely and confidently | Broken flows, inconsistent controls, lost work | Main and recovery journeys work across supported devices |
| Maintainer | Understand, change, and support the application | Duplicated logic, hidden coupling, unreliable tests | Small changes have predictable effects and inspectable evidence |

## Scope

### In scope

- TypeScript and Python language profiles. Next.js is the first framework
  profile on top of TypeScript. Python supports services, packages, and scripts;
  a web framework is enabled only when the project actually uses it.
- Relevant controls selected from the project's declared stack, capabilities,
  approved customer foundation, and affected code boundaries.
- Programmatic formatting, static analysis, tests, security checks, browser
  journeys, accessibility checks, and visual regression comparison.
- Reusable foundations for application structure, UI, error handling, data
  boundaries, and test setup, with explicit ownership and versioning.
- Identical gate definitions locally and in CI, with independent CI enforcement.
- Concise project-specific context, source provenance, and clear simulation
  labels. Existing project conventions remain authoritative when equivalent.

### Out of scope

- Building another agent runtime, autonomous review swarm, or LLM test grader.
- Claiming complete security, accessibility, usability, or product-market fit
  from an automated pass.
- Requiring every application to share a brand, screen layout, backend, or
  component library regardless of customer context.
- Replacing existing project tools merely to achieve uniformity.
- Implementing a general installer/updater before a working baseline proves
  useful on real projects.

## Golden path

1. Inspect the project and resolve its language, framework, and capabilities.
2. Present the relevant existing components, patterns, and acceptance criteria.
3. Define the changed behaviour, including material failure and permission cases.
4. Implement using the approved foundation and project conventions.
5. Format automatically, run the applicable checks, and correct real failures.
6. Verify the running application's affected user journey where applicable.
7. Produce an evidence report bound to the tested revision and configuration.
8. Let required CI checks enforce the merge/release boundary.

The model writes implementation and tests. Conventional programs execute and
grade the tests. Humans decide product priorities and approve intentional
design or release changes; their judgment is not impersonated by an AI score.

## Relevant controls

The language is TypeScript or Python; the framework and application capabilities
add controls. Examples of capabilities are browser UI, identity, multi-tenancy,
persistence, file upload, external integrations, and background jobs.

| Project or change | Controls exposed |
| --- | --- |
| Python command-line tool | Python lint/types/tests, file and input boundaries, applicable supply-chain checks |
| Next.js public website | TypeScript/Next.js checks, navigation, responsive layout, accessibility, visual and performance budgets |
| Next.js application with accounts and storage | Website controls plus authorization, persistence, isolation, and recovery tests |
| Shared button or theme change | Component interaction tests and affected visual/accessibility cases across consumers |
| Authentication, dependency, schema, or gate configuration change | Broader security/integration checks; do not narrow solely to changed files |

Detection proposes configuration once; the reviewed project configuration is
durable. Unknown or contradictory capability evidence cannot silently remove a
required control. Show why each control applies, what it tests, and what blocks
completion. Keep unrelated instructions and tools out of the active workflow.

Change selection may accelerate local feedback. A local subset reports partial
verification; CI checks the required applicable suite against the tested
revision. Shared configuration, dependency, security, and uncertain impact
changes broaden the suite. Removing a capability or required test is reviewable.

## Language foundations

These are recommended starting defaults, not new requirements to migrate an
existing project. Exact compatible versions must be pinned and exercised before
shipping each profile. Shell/Markdown remain internal harness tooling concerns.

| Concern | TypeScript / Next.js | Python |
| --- | --- | --- |
| Formatting | Prettier with project settings | Ruff formatter with project settings |
| Static correctness | Strict TypeScript, ESLint, applicable Next.js rules | Ruff and Pyright; strict new core/boundary modules |
| Unit/component tests | Vitest and Testing Library for supported components | pytest; preserve an explicit existing runner where appropriate |
| Application tests | Playwright against a built application | API/CLI/process tests; real disposable persistence when used |
| Boundary validation | Existing typed schema/validation library | Existing schema library or explicit typed validation |
| Environment | Existing lockfile and package manager | Existing lockfile manager; uv for a new project without a convention |
| Architecture | Import-boundary rules and server/client separation | Import-boundary rules and core/I/O separation |

Keep business logic testable without the UI, network, or database. Place runtime
validation at untrusted boundaries; static types alone do not validate input.
Keep dependency additions deliberate. Make line/file/function size limits
advisory unless a concrete failure justifies a stricter rule.

## Next.js: what applications should use and reuse

Start with the customer's existing design system. If none exists, create a
small approved kit using a compatible shadcn/ui foundation, semantic CSS tokens,
and one selected set of accessible primitives. Do not mix alternative primitive
stacks casually. Copied source becomes owned code requiring maintenance;
shadcn/ui provides modifiable component source and distribution conventions.
See [shadcn/ui](https://ui.shadcn.com/docs) and its
[token-based theming](https://ui.shadcn.com/docs/theming).

| Reusable asset | Examples | Programmatic protection |
| --- | --- | --- |
| Theme and tokens | Semantic colours, type scale, spacing, focus, motion | Token/import linting, contrast scans, visual comparisons |
| UI primitives | Button, field, dialog, menu, tabs, table | Keyboard, focus, accessible-name, interaction tests |
| Interaction patterns | Validated forms, pagination, search, confirmation | State transitions, invalid input, duplicate submission tests |
| Page patterns | Loading, empty, error, no-access, success states | Browser journeys and state-specific screenshots |
| Application services | Session access, authorized data access, errors, logging | Contract tests and negative permission/data cases |
| Test foundations | Factories, fake external adapters, isolated data, browser setup | Reproducible fixtures and tests of the harness itself |

Reuse existing local components first, extend their variants second, and create
a new component when its responsibility is genuinely different. Record the new
component's public API and cases. Enforce explicit import/token boundaries with
native lint rules; use duplication reports as advisory signals rather than
pretending arbitrary duplicate intent can be detected reliably.

Share stable behaviour and foundation contracts across applications. Customer
themes, branding, content, and intentional layout differences stay project-owned.
Start with an in-repository component catalogue and rendered examples. Extract
a versioned shared package when multiple applications demonstrate common needs;
pin consumers and test upgrades before propagation. Never automatically replace
customer customisations.

For new Next.js applications, use Server Components for appropriate rendering
and data retrieval, adding Client Components where interaction/browser APIs
require them. Prefer the framework's routing, links, image and font facilities
where applicable. Keep server-only data access, minimal response shapes, input
validation, and resource-level authorization at server entry points. Existing
backend APIs can retain their established access boundary. These choices follow
the framework's [component model](https://nextjs.org/docs/app/getting-started/server-and-client-components)
and [data-security guidance](https://nextjs.org/docs/app/guides/data-security).

Do not apply blanket caching rules. Make freshness, invalidation, and account
isolation explicit and test them where data is cached. Use consistent error,
loading, and recovery patterns without exposing implementation details to users.

## Testing that establishes behaviour

Every critical journey has named acceptance cases tied to real assertions.
Checking that a test file exists or that a page returns HTTP 200 is insufficient.

- Bugs get a regression that fails on the defect and passes on the fix.
- Core decisions get positive, negative, and boundary cases. Use generated-input
  property tests for meaningful invariants, retaining failing examples/seeds.
- Permissioned operations include unauthenticated, wrong role, wrong owner, and
  wrong tenant cases where applicable, calling the server directly as well as
  exercising the UI.
- Persistence tests use a disposable database and verify writes, reloads,
  failures, and transactional behaviour that the application relies on.
- UI tests perform the action and verify its outcome: submit, save, reload,
  search, cancel, recover, or deny. Mocks must not replace the very boundary the
  test claims to verify.
- Accessibility combines automated rules with executable keyboard/focus cases.
  Visual checks compare actual screenshots to intentionally approved baselines
  in a controlled browser environment. No AI screenshot judge is used.
- Use targeted mutation testing on critical pure logic to check whether tests
  detect deliberately altered decisions. Avoid a blanket expensive mutation
  suite or treating its score as proof of overall quality.

Next.js currently recommends E2E tests for async Server Components, which Vitest
does not support, and running Playwright against production builds. Split the
suite accordingly rather than mocking away the framework behaviour.
See [Vitest](https://nextjs.org/docs/app/guides/testing/vitest) and
[Playwright](https://nextjs.org/docs/app/guides/testing/playwright).

Missing runners, zero collected required tests, unexpected skips, absent
required artifacts, unexplained flakiness, and stale results cannot count as
passed verification. Do not silently change runners. Record retries; a passing
retry does not erase the original failure. A required flaky case remains a
failure until fixed or explicitly excepted with owner, scope, and expiry.

Coverage identifies untested paths; it is not the objective. Begin with critical
scenario coverage, then set branch/changed-code floors from a measured baseline.
Raising percentages by excluding important code or writing assertion-free tests
must not satisfy the gate. Mutation checks complement these measures; see
[Stryker's mechanism](https://stryker-mutator.io/docs/).

Automated checks cover only measurable aspects of UX. Product usefulness,
information hierarchy, brand fit, and full accessibility still need human
acceptance. The automated workflow contains no AI evaluation calls. Playwright
documents the limits of [accessibility automation](https://playwright.dev/docs/accessibility-testing)
and the need for consistent environments in
[visual comparisons](https://playwright.dev/docs/test-snapshots).

## Safety and evidence

Use deterministic secret scanning, applicable vulnerability/static scanners,
and executable safety cases. Reports distinguish findings from scanner errors
and missing/stale advisory data. Reviewable policy sets blocking severity and
exceptions; no automatic dependency fix, suppression, or baseline acceptance
may turn a failed gate green.

Test environments use synthetic data, disposable storage, scoped credentials,
and controlled network access. Verification must not call model providers or
production services. For applications that contain AI features, substitute a
deterministic provider at the adapter boundary and report exactly what this
does and does not establish about model output quality.

Each result identifies the source revision/dirty diff, configuration and
lockfile identity, tool versions, scope, commands, exit states, collected and
skipped cases, and evidence paths. Results use passed, failed, unavailable, or
not-applicable states; not-applicable requires an applicability reason. Partial
local execution is explicit. There is no averaged overall quality score.

CI is the enforcement boundary for merging. Required jobs and protected review
of test/configuration/baseline changes prevent the implementing agent from
silently weakening the gate. The harness itself is editable and is not a
sandbox or tamper-proof authority. Runtime permissions and release approval
remain independent.

## Measures

| Outcome | Evidence | Target direction |
| --- | --- | --- |
| Safety and correctness | Escaped defects, negative safety cases, critical journeys | Fewer regressions; all applicable critical cases pass |
| User experience | Journey completion, recovery, accessibility, reviewed visual changes | Predictable behaviour and fewer user-visible defects |
| Maintainability | Boundary violations, change/review effort, repeated defects | Easier changes with fewer unintended effects |
| Customer consistency | Reuse of approved primitives/patterns, theme conformance | Shared interaction quality with intentional brand differences |
| Developer effort | Time to meaningful feedback, setup, rework, flaky failures | Faster reliable feedback and lower human correction effort |

Use actual Next.js and Python projects to establish the baseline early. Measure
accepted work and total human effort, not document counts or raw test counts.
No productivity gain or universal coverage percentage is assumed.

## Constraints and assumptions

- TypeScript and Python are the two current language priorities, inferred from
  the existing harness and the user's Next.js requirement.
- The user explicitly requires automated testing without other AI calls.
- macOS remains the first supported developer platform. CI/browser runners must
  pin their environment; cross-platform support needs its own evidence.
- New command names, profiles, evidence schemas, and defaults in this vision
  require implementation unless described above. Schemas 1/2 remain readable;
  Step 07 adds an optional format command without replacing project files.
- Existing native configurations and customer design systems are preserved.
- Prefer a small reliable foundation; add controls when their applicability and
  failure-detection value are demonstrated.
