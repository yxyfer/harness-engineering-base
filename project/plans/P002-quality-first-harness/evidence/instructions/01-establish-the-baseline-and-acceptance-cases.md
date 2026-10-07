# Step 01: Establish the baseline and acceptance cases

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** implementation starts from current facts and independent behaviour
expectations. Refresh the existing audit, not the whole research exercise.

**Done when:** commands and missing tools are recorded; F1–F7 each have an
expected failure/pass pair; the critical scenarios in the shared contract have
specific inputs/outputs; a lightweight measurement format exists. No repair is
claimed merely because its future acceptance test has been described.

```text
Implement Step 01 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/01-establish-the-baseline-and-acceptance-cases.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md and AGENTS.md.

Refresh the existing audit against the current working tree. Run the existing
command/fixture matrix, distinguish missing tools from successful checks, and
preserve unrelated work. Define minimal regression cases for F1-F7 and concrete
acceptance cases for the synthetic Next.js work-item journey and Python
validation/import example. Use expected behaviour independent of implementation.

Record commands, exits, environment, failures and observed feedback time in
project/plans/P002-quality-first-harness/evidence/QH-01.md. Create a lightweight measurement format for later steps;
do not invent historical effort or productivity. Do not repair runtime code in
this step. Link the evidence from the plan and stop.
```
