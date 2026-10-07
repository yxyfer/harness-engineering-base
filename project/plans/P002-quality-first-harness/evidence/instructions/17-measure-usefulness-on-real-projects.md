# Step 17: Measure usefulness on real projects

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

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
Implement Step 17 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/17-measure-usefulness-on-real-projects.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Use the measurement records already collected.
Identify owner-authorised real Next.js, Python and established-toolchain pilot
projects; if paths/access are missing, prepare the concrete pilot protocol and
ask for those inputs without inventing results or mutating unrelated projects.

Compare existing native engineering controls with the added harness through
actual requested changes and deterministic defect replay. Keep acceptance cases
and environments comparable. Measure task outcomes, escaped defects, review/
rework, setup, feedback time, flaky/false failures and maintenance cost.
Separate foundation reuse from harness-wrapper benefit; launch no extra AI
evaluations.

Write project/plans/P002-quality-first-harness/evidence/QH-17.md with raw evidence, limitations and explicit keep/
change/remove recommendations. Prepare fixes for observed harness problems as
bounded follow-up tasks. Do not build distribution tooling until this checkpoint
supports it. Stop with the evidence-backed decision.
```
