# Application quality harness roadmap

- **Status:** active; full delivery incomplete
- **Owner:** repository owner
- **Updated:** 2026-10-07
- **Direction:** [Product](../../../../docs/PRODUCT.md) ·
  [ADR-003](../../../../docs/DECISIONS.md#adr-003-prioritise-application-quality-with-programmatic-verification)

## Outcome

Deliver safer, usable and maintainable customer applications with a small
verification engine and reusable Next.js/TypeScript and Python foundations.
Complete working controls before expanding distribution tooling.

## Next action

Step 13 is implemented; human acceptance of its 44 visual candidates remains
pending. Review [TASK-016](../tasks/P002-T013-ui-quality.md) and
[QH-13](QH-13.md). Step 14 can start independently after
Step 09; it is not started. Do not execute future steps as part of navigation
work.

## Delivery

Read only the selected guide and the [shared execution
contract](instructions/execution.md).
Execute one bounded step at a time. Each guide retains its acceptance criteria
and copy-ready prompt. Tasks own delivery details; reports own test results.
Update this table when evidence changes; do not append another progress log.

| Step | Outcome / task | Depends on | Evidence / state | Instructions |
| --- | --- | --- | --- | --- |
| 01 | [Baseline and acceptance cases](../tasks/P002-T001-quality-baseline.md) | None | [Complete](QH-01.md) | [Guide](instructions/01-establish-the-baseline-and-acceptance-cases.md) |
| 02 | [Correct application test routing](../tasks/P002-T002-application-test-routing.md) | 01 | [Complete](QH-02.md) | [Guide](instructions/02-separate-application-tests-from-harness-tests.md) |
| 03 | [Consistent discovery and command precedence](../tasks/P002-T003-discovery-and-check-precedence.md) | 02 | [Complete](QH-03.md) | [Guide](instructions/03-unify-discovery-and-honour-command-precedence.md) |
| 04 | [Correct managed-file ownership](../tasks/P002-T004-release-ownership.md) | 03 | [Complete](QH-04.md) | [Guide](instructions/04-preserve-managed-and-project-ownership.md) |
| 05 | [Core CI](../tasks/P002-T005-core-ci.md) | 04 | [Complete locally; remote unverified](QH-05.md) | [Guide](instructions/05-add-ci-for-the-repaired-core.md) |
| 06 | [Relevant profiles and prerequisite diagnostics](../tasks/P002-T006-profiles-and-doctor.md) | 05 | [Complete locally](QH-06.md) | [Guide](instructions/06-resolve-relevant-profiles-and-prerequisites.md) |
| 07 | [Native formatting and static checks](../tasks/P002-T007-native-static-tools.md) | 06 | [Complete locally](QH-07.md) | [Guide](instructions/07-delegate-formatting-and-static-quality-to-native-tools.md) |
| 08 | [Native verification evidence](../tasks/P002-T008-verification-evidence.md) | 07 | [Complete locally](QH-08.md) | [Guide](instructions/08-make-complete-verification-produce-trustworthy-evidence.md) |
| 09 | [Security checks and isolated verification](../tasks/P002-T009-security-and-isolation.md) | 08 | [Complete; findings retained](QH-09.md) | [Guide](instructions/09-add-executable-security-checks-and-test-isolation.md) |
| 10 | [Real Next.js foundation and shared UI](../tasks/P002-T010-nextjs-reference-app.md) | 09 | [Historical partial; current journeys in QH-12](QH-10.md) | [Guide](instructions/10-build-a-real-next-js-foundation-with-reusable-ui.md) |
| 11 | [Secure server operations and real persistence](../tasks/P002-T011-secure-persistence.md) | 10 | [Historical partial; current journeys in QH-12](QH-11.md) | [Guide](instructions/11-implement-secure-mutations-and-real-persistence.md) |
| 12 | [Complete application journeys](../tasks/P002-T012-user-journeys.md) | 11 | [Complete locally](QH-12.md) | [Guide](instructions/12-prove-complete-user-and-recovery-journeys.md) |
| 13 | [Accessibility, visual and performance checks](../tasks/P002-T013-ui-quality.md) | 12 | [Implemented; human approval pending](QH-13.md) | [Guide](instructions/13-protect-accessibility-appearance-and-responsiveness.md) |
| 14 | Useful Python reference application | 09 | Not started | [Guide](instructions/14-prove-a-useful-python-application.md) |
| 15 | Stronger tests for critical decisions | 12, 14 | Not started | [Guide](instructions/15-establish-that-important-tests-detect-wrong-behaviour.md) |
| 16 | Full CI enforcement and concise agent guidance | 13, 15 | Not started | [Guide](instructions/16-enforce-the-full-policy-and-simplify-agent-guidance.md) |
| 17 | Real-project pilot and usefulness assessment | 16 | Not started | [Guide](instructions/17-measure-usefulness-on-real-projects.md) |
| 18 | Safe adoption and updates where justified | 17 | Not started | [Guide](instructions/18-make-adoption-and-updates-safe-where-they-earn-their-cost.md) |
| 19 | Release rehearsal and operating handover | 18 | Not started | [Guide](instructions/19-rehearse-release-and-hand-over-operation.md) |

Steps 10–11 retain their historical partial reports. Step 12 supplies renewed,
source-bound browser evidence for the current implementation; it does not
rewrite those reports. Step 09 retains dependency findings blocking security
approval. Remote CI execution and protection settings remain unverified.

## Scope and completion

No agent runtime or AI verification judge. Preserve project-native tools,
customer components, release ownership and consequential human approval gates.
Use synthetic data and disposable services; no production/model calls in tests.

The [shared contract](instructions/execution.md) holds checkpoints,
critical scenarios, risks, recovery and final acceptance criteria. Complete all
applicable steps with linked evidence before moving this plan to completed.
Step 18 remains conditional on measured value and may retain manual adoption.

## Context and history

- [Architecture map](../../../../docs/ARCHITECTURE.md)
- [Baseline audit](AUDIT_2026_10_01.md)
- [Superseded roadmap](../../../archive/P001-harness-foundation/README.md)
- [Historical progress through Step 09](quality-first-progress.md)
