# Plan: Outcome-oriented title

- **Status:** proposed | active | blocked | complete
- **Owner:** TBD
- **Created:** YYYY-MM-DD
- **Target completion:** YYYY-MM-DD or not time-bound
- **Related tasks:** `tasks/TASK-NNN.md`

## Objective

Describe the user or system outcome this plan coordinates and why it matters.

## Non-goals

- State what this effort will deliberately not address.

## Context and constraints

- List the relevant product, architecture, design, data, quality, and security context.
- Record fixed technical, commercial, timing, or approval constraints.
- Link to applicable entries in `docs/DECISIONS.md`.

## Implementation slices

Keep each slice independently understandable and verifiable. Create a task from
`tasks/TASK_TEMPLATE.md` when a slice needs its own owner, acceptance criteria, or
work history.

| Slice | Outcome | Task | Dependencies | Status |
| --- | --- | --- | --- | --- |
| 1 | TBD | `tasks/TASK-NNN.md` | None | proposed |

## Dependencies

| Dependency | Owner | Needed by | Current state |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## Risks and mitigations

| Risk | Impact | Mitigation or fallback | Owner |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## Decisions requiring human input

| Decision | Options and trade-offs | Decision owner | Needed by |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

Promote accepted, durable decisions to `docs/DECISIONS.md`.

## Verification strategy

| Behaviour or risk | Verification method | Evidence required |
| --- | --- | --- |
| Core logic | `./harness test` | Passing automated tests |
| Project conventions | `./harness check` | Passing static and policy checks |
| Golden path | `./harness smoke` | Observable successful outcome |

Add project-specific integration, visual, accessibility, performance, security,
or manual checks in proportion to risk.

## Rollout and recovery

Describe sequencing, feature controls, migration, monitoring, rollback, and human
approval where applicable. Write `Not applicable` with a reason when no rollout
is involved.

## Completion criteria

- [ ] All linked tasks and implementation slices meet their acceptance criteria.
- [ ] Required checks pass and evidence is recorded.
- [ ] Durable context and decisions are updated.
- [ ] Intentional compromises are recorded in `plans/technical-debt.md`.
- [ ] A verification report is linked below.
- [ ] This plan is moved unchanged to `plans/completed/`.

## Final verification

- **Report:** `verification/...`
- **Completed:** YYYY-MM-DD
- **Remaining limitations:** TBD
