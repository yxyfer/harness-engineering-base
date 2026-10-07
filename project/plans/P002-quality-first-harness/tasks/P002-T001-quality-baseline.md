# P002-T001 — Current baseline and independent acceptance cases

- **ID:** P002-T001
- **Plan:** P002
- **Status:** complete
- **Depends on:** none
- **Evidence:** ../evidence/QH-01.md

## Outcome

Later implementation starts from reproducible current observations and explicit
behavioural expectations, without treating absent tools or future tests as
passes.

## Implementation

[Implementation map](../../../architecture/features.md) · [Original
task](../evidence/legacy-TASK-004-QUALITY-BASELINE.md) · [Step
instructions](../evidence/instructions/01-establish-the-baseline-and-acceptance-cases.md)

## Acceptance

- [x] Existing root/fixture matrix and audit probes have commands, exits,
      environment, source identity, failures and observed feedback durations.
- [x] Missing tools are distinct from successfully executed checks.
- [x] Each F1-F7 finding has a minimal regression and healthy/failing pair.
- [x] Critical plan scenarios have concrete synthetic inputs and assertions,
      including the Next.js journey and Python validation/atomic import.
- [x] A lightweight format records later attempts, effort and evidence without
      invented historical productivity.
- [x] Plan links the evidence; only Step 01 changes status.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
