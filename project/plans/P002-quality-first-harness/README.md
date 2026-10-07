# P002 — Quality-first harness

- **ID:** P002
- **Status:** active

## Outcome

Deliver reliable verification and reusable Next.js and Python foundations.

## Approach

Execute one numbered task at a time. [Shared execution
contract](evidence/instructions/execution.md).
P002-T013 needs human visual acceptance; P002-T014 is independently ready.
Remote CI and security approval remain unverified/blocked as documented.

## Architecture impact

[Systems](../../architecture/systems.md) ·
[Features](../../architecture/features.md).
Tasks record changed boundaries; shared architecture records current behaviour.

## Tasks

<!-- project:tasks:start -->
| Task | Adds | State | Depends on |
| --- | --- | --- | --- |
| [P002-T001 — Current baseline and independent acceptance cases](tasks/P002-T001-quality-baseline.md) | Later implementation starts from reproducible current observations and explicit behavioural expectations, without treating absent tools or future tests as passes. | complete | none |
| [P002-T002 — Independent application tests and harness self-tests](tasks/P002-T002-application-test-routing.md) | Application failures cannot be hidden by shipped harness tests or a silently substituted runner. Both suites have independent commands and honest exits. | complete | P002-T001 |
| [P002-T003 — Consistent discovery and static-check precedence](tasks/P002-T003-discovery-and-check-precedence.md) | Harness-owned scans inspect maintained files within the target, route supported executable shebangs to their language, and honour directory exclusions. Required policy gates precede one resolved project static-check implementation. | complete | P002-T002 |
| [P002-T004 — Explicit release ownership preserves installation health](tasks/P002-T004-release-ownership.md) | Project additions and generated environments coexist with shipped files. Verification still exposes shipped-file modification, loss and unsafe paths. Release generation selects only explicitly reviewed inputs. | complete | P002-T003 |
| [P002-T005 — Run repaired core checks in pinned macOS CI](tasks/P002-T005-core-ci.md) | A bounded GitHub Actions workflow installs locked tools and runs actual shell, Markdown, Python and TypeScript checks, repaired contract suites and fixtures. | complete | P002-T004 |
| [P002-T006 — Resolve applicable controls and readiness](tasks/P002-T006-profiles-and-doctor.md) | One shared resolution explains languages, Next.js, capabilities, context and unsupported package scope. Doctor diagnoses prerequisites without installing, rewriting configuration or claiming checks executed. | complete | P002-T005 |
| [P002-T007 — Delegate formatting and enforce static checks](tasks/P002-T007-native-static-tools.md) | Format delegates to native project tools; check never requests autofixes and fails missing required defaults. Explicit equivalent project commands retain precedence and own their coverage. New opt-in native templates provide strict types and concrete domain/I/O and client/server import rules. | complete | P002-T006 |
| [P002-T008 — Bind complete verification to native evidence](tasks/P002-T008-verification-evidence.md) | Thin verify coordination produces validated, input-bound machine evidence and a short summary without replacing native controls or inventing test counts. | complete | P002-T007 |
| [P002-T009 — Executable security controls and isolated verification](tasks/P002-T009-security-and-isolation.md) | Run maintained secret/source scanners and offline locked-dependency advisory checks. Required findings, scanner errors and missing/stale data cannot pass. Run opted-in application verification with a clean synthetic environment under the external macOS process sandbox, never a URL filter presented as isolation. | complete | P002-T008 |
| [P002-T010 — Production-buildable synthetic Next.js foundation](tasks/P002-T010-nextjs-reference-app.md) | Buildable Next.js foundation with server-rendered work items and one shared UI kit. | complete | P002-T009 |
| [P002-T011 — Persist authorized synthetic work-item edits](tasks/P002-T011-secure-persistence.md) | Authenticated synthetic users read only owned tenant work and editors save validated changes to real disposable SQLite storage. No production auth bypass. | complete | P002-T010 |
| [P002-T012 — Prove production user and recovery journeys](tasks/P002-T012-user-journeys.md) | Production Chromium journeys prove real local sessions, authorized edits and durable SQLite outcomes. Native results feed verify; no operation is mocked. | complete | P002-T011 |
| [P002-T013 — Measurable reference UI quality](tasks/P002-T013-ui-quality.md) | Native production-browser evidence protects accessible interaction, reflow, appearance and measured lab costs without inventing human design acceptance. | blocked | P002-T012 |
| [P002-T014 — Prove a useful Python application](tasks/P002-T014-prove-a-useful-python-application.md) | Python support handles meaningful inputs, domain behaviour, persistence and failure. Keep the tiny existing server for dispatcher tests. Suggested new location: `examples/python-work-items/`. | ready | P002-T009 |
| [P002-T015 — Establish that important tests detect wrong behaviour](tasks/P002-T015-establish-that-important-tests-detect-wrong-behaviour.md) | critical TypeScript and Python decisions have stronger evidence than a coverage percentage. Add property tests for meaningful invariants and bounded mutation checks for selected pure logic. Choose compatible maintained tools during implementation, and keep slow campaigns outside the fast loop. | planned | P002-T012, P002-T014 |
| [P002-T016 — Enforce the full policy and simplify agent guidance](tasks/P002-T016-enforce-the-full-policy-and-simplify-agent-guidance.md) | full applicable checks run in CI independently of an agent's completion claim; agents receive concise relevant instructions. | planned | P002-T013, P002-T015 |
| [P002-T017 — Measure usefulness on real projects](tasks/P002-T017-measure-usefulness-on-real-projects.md) | decide which controls deserve broader adoption based on evidence. Use an actual Next.js project, a Python project and an established repository with its own conventions. A project can satisfy two categories; include at least one real case for each, and disclose the number of distinct projects. Repository locations/access are owner inputs, not facts to guess. | planned | P002-T016 |
| [P002-T018 — Make adoption and updates safe where they earn their cost](tasks/P002-T018-make-adoption-and-updates-safe-where-they-earn-their-cost.md) | repeated use preserves project context and customisations. Implement only the adoption/update operations justified by Step 17. A small documented copy/diff procedure remains valid when automated distribution is not justified. | planned | P002-T017 |
| [P002-T019 — Rehearse release and hand over operation](tasks/P002-T019-rehearse-release-and-hand-over-operation.md) | a new maintainer can start, verify, troubleshoot and update supported projects from accurate instructions. This produces a local release candidate; public release/deployment is a separate authorised action. | planned | P002-T018 |
<!-- project:tasks:end -->
