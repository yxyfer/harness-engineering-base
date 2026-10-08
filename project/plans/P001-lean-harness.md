# P001 Lean harness rebuild

Status: In progress. T001, T002 and T004 are complete; T003 is next.

Make it quick to try an idea, safe to discard it, and straightforward to retain
and improve it. Keep the code readable and give the user a reliable view of how
the application works. The first version consists of a working agreement, native
tool settings, isolation recipes and architecture views, proven on one small
feature using React, Next.js, Vercel and Neon.

The reset is complete. This plan builds forward from commit `0516ee6`; it does
not restore the old harness wholesale. The
[working agreement](../../docs/WORKFLOW.md) owns durable workflow rules. The
[architecture map](../../docs/ARCHITECTURE.md) owns current and intended
responsibilities.

## What changes by mode

| Mode    | What we need to learn or deliver       | Evidence required                                             |
| ------- | -------------------------------------- | ------------------------------------------------------------- |
| Explore | Does this idea or integration work?    | A visible result, stated data boundary and a discard path     |
| Build   | Can we retain and extend it reliably?  | Meaningful tests, edge cases and the real user journey        |
| Release | Is it ready for its intended exposure? | Applicable security, recovery, migration and deployment proof |

Readability, native formatting and safe handling of secrets apply throughout.
The mode does not mandate a new architecture or a document for every prompt.

## Execution order

```mermaid
flowchart LR
  T1[1 Working agreement] --> T2[2 Native quality checks]
  T2 --> T3[3 Reversible experiments]
  T2 --> T4[4 Architecture visibility]
  T3 --> T5[5 Real feature pilot]
  T4 --> T5
```

T003 and T004 can be developed independently after T002. Keep one bounded task
active at a time unless there is a concrete reason to work in parallel.

## P001 T001 Define the working agreement

Task ID: `P001-T001`. State: Complete. Completed: 2026-10-07.

**Outcome:** A practical agreement for Explore, Build and Release, including
readability, testing, refactoring and source-backed architecture views.

**Inspect:** The user's requests, surviving repository files and the supplied
operating contract. Challenge rules that add work without reducing an observed
problem. Keep the distinction between code recovery and external side effects.

**Deliver:** The [agreement](../../docs/WORKFLOW.md), an initial
[architecture map](../../docs/ARCHITECTURE.md), and this plan with embedded
tasks. Use one plan file instead of a new document for every task or agent run.

**Proof:** Each mode states its purpose and required evidence. The plan gives
each remaining task an outcome, investigation, dependencies and acceptance. The
current map labels proposed behaviour and records that CI was removed.

**Reviewer brief:** This changes project guidance, not application behaviour.
The agreement uses the modes already discussed. Its main risk is becoming
paperwork; the pilot measures that overhead. Recovery is an ordinary document
edit. No data or deployed resources are affected.

**Verification:** See the verification section at the end of this plan. This
task proves that the foundation is recorded, not that it improves development.

## P001 T002 Make native quality checks runnable

Task ID: `P001-T002`. State: Complete. Depends on: `P001-T001`. Completed:
2026-10-07.

**Outcome:** Formatting, lint, types and relevant tests run through familiar
project commands, with clear failures and no bespoke policy platform.

**Inspect:** Existing Next.js and TypeScript conventions in Data Miner, read
only; installed framework documentation; test runner support; and missing
formatting settings. Select and lock compatible tool versions before writing
their configuration.

**Reuse or build:** Use Prettier, ESLint with the Next.js and React rules,
TypeScript strict settings, and an existing compatible test runner. Define
concise BASE, NAMING, TESTING and ARCHITECTURE standards with relevant language
profiles before source implementation. Put tool settings in native files and
create a short agent entrypoint that links to the agreement and standards. Test
application settings in a tiny reference project rather than adding app
dependencies to the kit root. Run native checks locally first.

**Framework decisions to check:** Components follow responsibilities; derived
values do not create duplicate state. Reuse one accessible modal primitive with
content and variants rather than duplicate its interaction logic. Use server
components for appropriate reads and small client boundaries for interaction.
Validate and authorise mutations; keep database access server-only. Choose
freshness explicitly. Avoid an internal HTTP hop when server code can read the
source directly. Do not add a repository layer without a real separation need.

**SQL decisions to check:** Parameterised queries, appropriate types and
constraints, transactions for dependent writes, explicit duplicate and
concurrent update behaviour, versioned migrations and query-justified indexes.
PostgreSQL integration claims require PostgreSQL evidence. Choose a migration
tool for the actual driver and schema workflow; do not write a migration engine.

**Proof:** A readable sample passes format, lint, type and relevant behaviour
checks. Introduce one formatting, one type and one behaviour error to show the
appropriate command fails; fix them and rerun. Demonstrate the commands in the
kit and reference project. CI is outside this initial task.

**Reviewer brief:** Changes native configuration and a small reference app.
Start with a known rule tested before implementation and one exploratory UI.
Keep template settings distinct from consumer-owned settings. Recovery is
reverting the kit change; no existing application configuration is overwritten.

**Implementation choice:** Use separate locked kit and reference packages,
native Prettier and ESLint configuration, strict TypeScript, Node behaviour
tests and one Playwright browser journey. The reference is a searchable catalog
with labelled synthetic data. Keep SQL integration and migration-tool selection
in T003, where an actual database connection can verify them. See
[decisions](../../docs/DECISIONS.md). No CI or installer is added, and Data
Miner is inspected read only.

The following proof describes the initial validation app before its removal. The
cleanup record below and the current architecture own today's layout and
commands. App settings were retained as native adoption templates.

**Verification on 2026-10-07:**

| Command or inspection                                                | Result                                                                                                          |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `npm run setup`                                                      | Both locks reproduced with lifecycle scripts disabled and strict peer checks                                    |
| `npm ls --all` in kit and reference                                  | Both dependency trees valid                                                                                     |
| `npm run check`                                                      | Prettier, kit and React lint, generated route types and strict TypeScript passed                                |
| `npm test`                                                           | Five behaviour tests passed; the initial empty implementation failed four before the rule was written           |
| `npm run self-test`                                                  | Seven tests passed, including four deliberate failure probes and successful checks before and after restoration |
| `PLAYWRIGHT_CHANNEL=chrome NEXT_TELEMETRY_DISABLED=1 npm run verify` | Combined checks, tests, self-tests, production build and both browser journeys passed                           |
| Desktop and mobile screenshots                                       | Inspected at 1280 and 390 pixels; readable layout, no horizontal overflow                                       |
| Browser diagnostics                                                  | No console or page errors after fixing the missing icon                                                         |
| Source links and Git inventory                                       | Local links resolve; native dotfile settings are included despite the global ignore rule                        |
| `git diff --check`                                                   | Passed                                                                                                          |

The failure probes ran in a disposable copy: formatting and conditional React
hooks exited 1, the type mismatch exited 2, and the broken rule exited 1 with
assertion failures. Source was restored and checked again. A discovered nested
Node-runner false success was fixed; self-tests now clear its inherited context
and verify that behaviour tests execute.

Browser screenshots were generated in the validation app's ignored
`test-results/` directory by the smoke command. Verification used macOS, Node
24.10.0, npm 11.6.0 and installed Chrome with temporary browser profiles.
Chromium's default configuration, other browsers and other operating systems
were not run. The local server required sandbox permission to listen on its test
port.

The reference's ESLint 9 compatibility debt is explicit in
[project/debt.md](../debt.md). No consumer configuration, production data or
deployment was changed. SQL guidance is present; database correctness,
migrations, authorisation, Neon and Vercel remain unverified until the relevant
later task. The old `harness` and project sync commands were not restored;
native equivalents were exercised and navigation was maintained directly.

**Latest stable follow-up:** Complete, requested and verified on 2026-10-07. The
reference now pins Next.js and its lint config at 16.4.0, with React and React
DOM at 19.3.0. Both React type packages are also current at 19.3.0. Setup and
the full check compare exact pins, lock entries and installed packages with
npm's public `latest` stable releases. Ranges, prereleases, mismatched versions,
outdated pins and unavailable registry evidence fail. The checker performs no
installation or writes. `check:local` remains available for offline iteration;
it does not prove freshness. Scope is the reference and adoption guidance;
consumer commands need explicit wiring. Recovery is restoring the previous pins
and lock and reinstalling them. No deployed app or database changes.

**Follow-up verification:** The real registry gate first exited 1 for Next.js
and its lint config at 16.3.7, reporting 16.4.0 as required. Strict peer
installation and `npm ls --all` passed after the upgrade. `npm run setup`
reproduced both locks and passed the live gate. Then
`PLAYWRIGHT_CHANNEL=chrome NEXT_TELEMETRY_DISABLED=1 npm run verify` passed
formatting, kit and React lint, route types, strict TypeScript, five behaviour
tests, sixteen harness tests, the Next.js 16.4.0 production build and two
browser journeys. The nine new version-policy tests use synthetic metadata and
cover success, drift, prereleases, unavailable or malformed registry responses,
matching companion packages, missing lock entries, non-mutation and CLI failure.
Their initial stub failed all seven initial cases before implementation. Both
built screenshots were inspected again; browser diagnostics remained clear. The
prior browser and environment limitations still apply. Next.js 16.4.0's
experimental upgrade reminder was inspected; it can be skipped and does not
replace the explicit four-package verification gate. No CI was added.

**Keep the kit focused:** Complete, requested and verified on 2026-10-07.
Removed the permanent example app, its lock, installed framework dependencies
and build output. Kept the verified ESLint and TypeScript configurations as
native adoption templates. Kit setup installs only kit tools; kit check covers
formatting and JavaScript lint. Kit tests use disposable configurations and
synthetic package metadata. Removed app dev, types, build and smoke commands.
The version checker requires an explicit installed app directory; receiving apps
must wire it into their own setup and full verification. Previous React and
browser proof above is historical. No consumer app or external resource changes.

**Cleanup proof:** A recovery archive of the uncommitted app source and lock was
created outside the repository and verified against all fifteen source files
before removal. Its SHA-256 is
`755ea1d301fa4583c082bd833ef2adb132d2e8aec72d22b15e0d87d18df0ab3b`. Both
adoption configs matched their tested originals before removal. The
explicit-target command passed against the real installed app and live npm
metadata before cleanup. A new missing-target CLI test initially caught a silent
no-op through the macOS temporary path; Node's native main-module flag fixed
entry detection. Missing targets now exit 1 with usage information. Offline
`npm run setup` reproduced the kit lock, and `npm run verify` passed formatting,
lint and fifteen tests after the app was removed. Inventory checks confirmed no
example directory, no framework packages in the kit lock or installed dependency
directory, and no app command delegation. Browser and application types are no
longer kit checks; receiving apps need their own evidence. The source archive is
local recovery material, not a distributed template or permanent retention
promise.

## P001 T003 Make experiments isolated and recoverable

Task ID: `P001-T003`. State: Next. Depends on: `P001-T002`.

**Outcome:** Try a feature without disturbing retained work; discard its code,
data and temporary resources through a documented, verified procedure.

**Inspect:** Git worktree behaviour with a dirty parent checkout, local runtime
and port isolation, Vercel environment variable scoping, Neon branch creation,
data inheritance, migration timing and resource cleanup in the actual
integration. Check which system owns branch deletion rather than assuming
cleanup follows Git.

**Reuse or build:** Start with Git worktrees and a short resource inventory. Use
a disposable PostgreSQL database locally. Prepare a Vercel Preview and isolated
Neon database recipe with synthetic seed data. Use schema-only branching when a
parent contains data that should not enter an experiment. Promote code and
schema changes deliberately, not experiment data. Add a small helper only if the
manual recipe proves error-prone.

**Needs:** A disposable test project and PostgreSQL runtime. Live acceptance
also needs an authorised Vercel test project and Neon test database with access
to their configuration. Prepare the recipe and local checks before requesting
service access. Production access is outside this task.

**Proof:** Run an experiment from a checkout with unrelated changes. Confirm the
parent files are preserved. Make an isolated database write and show it does not
alter the retained database. Apply a migration in isolation. Discard the
experiment and verify every resource in its inventory is removed or retained
intentionally. Recreate it from recorded inputs. Demonstrate application and
database recovery separately. Label local-only proof if live access is absent.

**Reviewer brief:** This introduces checkout, runtime and database boundaries. A
worktree alone is insufficient. Confirm target identifiers before cleanup; never
use shared history resets or inherited production credentials. Keep a
recoverable snapshot for any retained changes before deleting an experiment.

## P001 T004 Explain the architecture and each change

Task ID: `P001-T004`. State: Complete. Depends on: `P001-T002`. Completed:
2026-10-08.

**Outcome:** The user can understand how the app works and what a change enables
without reading the entire codebase.

**Inspect:** One receiving application's feature owners, state, data flow and
failure paths. Compare what can be extracted reliably from code with what needs
a human or agent explanation. Identify the information the user actually needs
to judge a change; an exhaustive import graph is unlikely to answer that
question.

**Reuse or build:** Begin with Mermaid diagrams and source links in existing
project context. Provide an application overview, one input-to-result feature
flow and a before-and-after change view. Keep a short explanation of intent,
affected boundaries, benefit and proof alongside it. Label fixtures, intended
designs and currently exercised integrations. Reuse these views in task briefs.

**Proof:** Match every node and arrow to source or an explicit planned label.
Open the diagrams in a renderer and follow the source links. The user should be
able to identify where state lives, where a write happens and what changed from
the view alone. Use two minutes as an initial comprehension target, not a proven
benchmark; user feedback is required to establish success.

**Reviewer brief:** This adds explanation, not an application runtime
dependency. The risk is a convincing but stale diagram. Update it with boundary
changes and compare it to source during review. Drop unnecessary detail before
introducing a scanner or dashboard. Recovery is a document edit.

**Implementation choice:** Use the existing architecture entry point, a small
native diagram template and a read-only Data Miner walkthrough. Show current
system owners, the company-save path and this task's before-and-after review
experience. Tie every runtime node and arrow to inspected source. Record the
source revision, state owner, write owner, guards and failure behaviour.
Maintain views when boundaries change; a minor experiment can link the existing
view and explain its delta without new paperwork. Diagrams remain Markdown
source; rendering tools are temporary and add no kit or app dependency.

**Acceptance:** Render the diagrams, resolve source links, compare flows with
their owners, preserve the inspected application's files, and pass kit checks
and tests. Human readability remains a separate check: the user must be able to
find the state owner, persistent write and change without inspecting every file.
The two-minute goal is provisional and requires feedback.

**Verification on 2026-10-08:**

| Check                      | Result                                                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Source comparison          | Runtime owners and arrows matched to Data Miner revision `a047ea4`; manual guidance and template placeholders are labelled |
| Local links                | All 58 local links across the nine changed Markdown files resolve                                                          |
| Diagram rendering          | Nine Mermaid blocks rendered with Mermaid 12.1.0 in isolated Chrome at a 1280-pixel viewport; no page errors               |
| Visual inspection          | All nine screenshots inspected; simplified the change view and checked readable labels and paths                           |
| `npm run verify`           | Formatting, JavaScript lint and all fifteen kit self-tests passed                                                          |
| `git diff --check`         | Passed                                                                                                                     |
| Receiving app preservation | Data Miner remained clean at revision `a047ea4`; no application files or configuration changed                             |

**Reader feedback:** The user answered "Yes, the views make it clear" when asked
about draft state, persistence, research initiation and the changed boundary.
This establishes clarity for this example. The two-minute goal remains a
provisional target, not a measured productivity claim or proof that every future
view will be understandable.

The rendering library and browser script were used outside the repository; no
dependency, scanner or dashboard was added. The views describe inspected source,
not verified database, provider or deployed application behaviour. Application
types, tests, build and journeys were not rerun because this task changed only
kit documentation.

## P001 T005 Prove the approach on a real feature

Task ID: `P001-T005`. State: Planned. Depends on: `P001-T003`, `P001-T004`.

**Outcome:** Evidence that the workflow can produce a fast experiment, a
reliable retained feature and an understandable architecture on the stack we
use.

**Inspect:** The completed recipes and native checks. Choose a small feature
with a visible interaction, one persisted operation and a meaningful failure
case. A candidate is editing a saved item through a reusable modal. Use an
isolated application project outside this kit, with disposable data. Inspect
Data Miner as a subsequent adoption target without modifying it during the kit
pilot.

**Run:** Explore the interaction and demonstrate discard. Recreate or promote
the useful result in Build; add tests for validation, duplicates or concurrent
updates as applicable. Extend it without duplicating its modal or data rules.
Prepare Release evidence in an authorised preview environment, including access
boundaries, migration and recovery. Production deployment is a separate
authorised action. Perform a refactoring review; record either a justified small
refactor or why no refactor is needed.

**Needs:** T003's disposable resources and access for live Vercel and Neon
proof. User review is needed for usefulness and comprehension. Local tests can
proceed independently, but cannot complete the live integration claims.

**Proof:** The feature works through the actual browser and PostgreSQL path,
retained behaviour survives an extension, the experiment is removable, and the
architecture view answers the user's questions. Record failed attempts as well
as successes. Inspect code readability and dependency choices directly.

**Reviewer brief:** The pilot tests the method on a bounded example. It cannot
prove a universal productivity gain. Do not expand it into a second product or
refactor Data Miner as a side effect. Recovery uses the verified discard recipe.

## How we judge whether this helps

Record these observations in the pilot task; use a small table, not a telemetry
service. Agree a comparable feature scope before judging speed.

- Time from the request to the first usable result, separating setup and access
  delays from implementation and process overhead. Five to ten minutes is an
  ambition for a tiny prepared experiment, not a promise for arbitrary features.
- Regression and rework after extending retained behaviour. A test count is not
  a substitute for successful journeys and useful failure coverage.
- Time and resources needed to discard and reproduce the experiment.
- Whether the user can explain the architecture and change from the views.
- Files, dependencies and documentation added, with reasons. Fewer files alone
  is not proof of better design; judge cohesion and ease of change.

Use a recorded baseline when available; otherwise say that the first pilot is a
feasibility result and establishes a baseline. Three comparable later changes
can give a directional comparison, with task differences recorded. Keep the
workflow only if it supports useful results with acceptable rework and overhead.
Remove a rule when its cost is evident and its benefit is not.

## Deferred until the pilot identifies a need

A dashboard, automatic architecture scanner, installer and update protocol,
custom gate engine, universal task tracker, CI setup, cost optimisation and
speculative capacity work. We can add a focused capability when an observed
recurring failure or adoption need makes its value clear.

## Primary guidance to check during implementation

- [Thinking in React](https://react.dev/learn/thinking-in-react)
- [Next.js server and client components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [Next.js data security](https://nextjs.org/docs/app/guides/data-security)
- [Next.js backend for frontend](https://nextjs.org/docs/app/guides/backend-for-frontend)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Vercel environments](https://vercel.com/docs/deployments/environments)
- [Neon branches with Vercel previews](https://neon.com/blog/neon-skills-landed-in-the-vercel-cli)
- [Opportunistic refactoring](https://martinfowler.com/bliki/OpportunisticRefactoring.html)

These guide implementation choices. They are not evidence that this kit or a
consumer application already complies. Check installed framework versions and
the actual Vercel and Neon setup when executing the relevant task.

## Foundation verification

P001-T001 verification on 2026-10-07:

| Check                         | Result                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `python3` document inspection | Passed for all six Markdown files: UTF-8, final newlines, whitespace, 80-column prose and paired code fences |
| Relative link inspection      | All 12 local file links resolve                                                                              |
| Plan and agreement inspection | Five task IDs include their parent plan ID; all three modes are defined                                      |
| Filesystem inspection         | The removed GitHub CI workflow is absent                                                                     |
| `git diff --check`            | Passed                                                                                                       |

The Python inspection was a one-off read-only check, not a new harness command.
Tables and URLs use the agreed width exceptions. Diagrams have not been
rendered, and user comprehension has not been tested; those are T004 outcomes.

No executable `harness` command exists after the reset. `./harness check`,
`./harness test` and `./harness project sync` were not run because their
implementation is absent. No application, database or deployment acceptance is
claimed by this documentation task.
