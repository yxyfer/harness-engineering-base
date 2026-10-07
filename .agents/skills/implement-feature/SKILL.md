---
name: implement-feature
description: Implement a bounded product feature from repository context through evidence-backed verification. Use for feature work that should update plans, tests, and durable context together.
---

# Implement Feature

Read `AGENTS.md`, the task, relevant `docs/`, and the active plan before editing.
Use `project/README.md` and `project/FORMAT.md` when adopted; read one plan-owned
task and its instructions. Create missing work from `project/templates/plan.md`
and `task.md`: `PNNN-plan-name/README.md` and `PNNN-TNNN-task-name.md` in its
tasks folder. Every task has a parent, fixed status, acceptance and evidence.
Preserve a legacy project's existing conventions when the format is not adopted.

Inspect the current user path and reuse existing components, contracts, and
patterns. State consequential assumptions and preserve human approval gates.

Implement the smallest coherent vertical slice. Add or update tests at the level
that best demonstrates the acceptance criteria. Keep data provenance and real,
synthetic, modelled, or simulated integration status visible.

Keep the task's reviewer brief concise: why the change is needed, implementation
choice, affected boundaries, risk, deployment and recovery. Link source and the
canonical architecture map; update affected flows and durable ADRs together.
State when architecture or deployment is unaffected. Do not copy test logs or
progress history into plans; link acceptance evidence from the task.

Refresh adopted work indexes with `./harness project sync`, then run
`./harness check`, `./harness test`, and relevant `./harness smoke`;
add visual QA
when the interface changes. Record checks actually run in a report created
from `project/templates/report-template.md`, inside the plan's `evidence/`.

Before closing, update durable context or `docs/DECISIONS.md`, record intentional
compromises in `project/debt.md`. Complete tasks stay in the active bundle;
archive only when every task is complete using `./harness project archive PNNN`.
The command refreshes navigation and repairs links. Explicitly replaced plans
remain superseded, not completed. Human acceptance stays distinct from test passes.
