---
name: implement-feature
description: Implement a bounded product feature from repository context through evidence-backed verification. Use for feature work that should update plans, tests, and durable context together.
---

# Implement Feature

Read `AGENTS.md`, the task, relevant `docs/`, and the active plan before editing.
If no task exists, create one from `tasks/TASK_TEMPLATE.md` with observable
acceptance criteria and explicit non-goals.

Inspect the current user path and reuse existing components, contracts, and
patterns. State consequential assumptions and preserve human approval gates.

Implement the smallest coherent vertical slice. Add or update tests at the level
that best demonstrates the acceptance criteria. Keep data provenance and real,
synthetic, modelled, or simulated integration status visible.

Run `./harness check`, `./harness test`, and `./harness smoke`; add visual verification
when the interface changed. Record only checks actually run in a report created
from `verification/REPORT_TEMPLATE.md`.

Before closing, update durable context or `docs/DECISIONS.md`, record intentional
compromises in `plans/technical-debt.md`, and move the completed plan.
