# Quality-first execution contract

[Roadmap](../../README.md). Read this contract and only
the selected step guide. These are execution requirements and planned defaults,
not a second progress record. Current implementation lives in docs and evidence.

## How to execute this plan

Use one step prompt at a time in this repository. Each prompt tells the coding
agent to read the shared execution contract, so it works in a fresh chat
without copying the earlier conversation. Complete the step's evidence before
beginning dependent work. Do not paste all prompts as one implementation
request.

Default to numbered order. Dependencies allow independent work when another step
needs owner input; they do not request sub-agents or concurrent editing. Split a
large step into smaller tasks while preserving its acceptance criteria.

Use the next free task number from
[the task template](../../../../templates/task.md). Create evidence in
`project/plans/P002-quality-first-harness/evidence/QH-01.md` through
`project/plans/P002-quality-first-harness/evidence/QH-19.md` as steps run, using
[the report template](../../../../templates/report-template.md). These are
future
output paths. Add task/evidence links to the roadmap only when the files exist.
Partially verified steps stay incomplete.

## Execution contract for every prompt

1. Read `AGENTS.md`, relevant canonical context, accepted decisions, the
selected
   step and its prerequisites. Before source edits read the base standards and
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
[Playwright against production
builds](https://nextjs.org/docs/app/guides/testing/playwright).

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
