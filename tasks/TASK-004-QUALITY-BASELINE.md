# TASK-004: Current baseline and independent acceptance cases

- **Status:** complete
- **Owner:** repository owner; execution by Codex
- **Related plan:** [Step 01](../plans/active/QUALITY_FIRST_HARNESS.md)
- **Evidence:** [QH-01](../verification/QH-01.md)

## Outcome

Later implementation starts from reproducible current observations and explicit
behavioural expectations, without treating absent tools or future tests as passes.

## Context to read

- `AGENTS.md`, canonical `docs/` context and ADR-001 through ADR-003.
- The quality-first plan's execution contract and Step 01.
- The existing audit, diagnostic probes, command implementations and fixtures.
- Shared standards and the Python, TypeScript, shell and Markdown profiles.

## Constraints and non-goals

- Preserve the existing dirty tree. Do not repair runtime, fixtures or config.
- Use current installed tools, synthetic temporary projects and local services.
- Refresh observations rather than research; no downloads or model calls.
- Acceptance cases specify outcomes independently of implementation.
- Do not start Step 02 or mark the entire plan complete.

## Acceptance criteria

- [x] Existing root/fixture matrix and audit probes have commands, exits,
      environment, source identity, failures and observed feedback durations.
- [x] Missing tools are distinct from successfully executed checks.
- [x] Each F1-F7 finding has a minimal regression and healthy/failing pair.
- [x] Critical plan scenarios have concrete synthetic inputs and assertions,
      including the Next.js journey and Python validation/atomic import.
- [x] A lightweight format records later attempts, effort and evidence without
      invented historical productivity.
- [x] Plan links the evidence; only Step 01 changes status.

## Verification

| Check | Command or method | Expected evidence |
| --- | --- | --- |
| Baseline | Existing command/fixture matrix and diagnostic probes | Actual results, including failures and unavailable tools |
| Native checks | Installed fixture scripts and Python runner | Scope and collection recorded separately |
| Documentation | `./harness check`, `git diff --check` | Links/whitespace checked; tool gaps explicit |
| Preservation | Before/after file digests | Existing files unchanged except the authorised plan update |

## Notes and decisions

The baseline may remain failed or partial while this audit task completes.
Acceptance cases for future applications are specifications, not execution proof.
