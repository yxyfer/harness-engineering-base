# TASK-NNN: Outcome-oriented title

- **Status:** ready | active | blocked | complete
- **Owner:** TBD
- **Related plan:** `plans/active/...`

## Outcome

State the observable user or system outcome, not the implementation activity.

## Context to read

- `AGENTS.md`
- Relevant files under `docs/`
- Relevant decision records and code entry points

## Constraints and non-goals

- TBD

## Acceptance criteria

- [ ] Given/when/then or another observable criterion.
- [ ] Failure, empty, and permission states are addressed where relevant.
- [ ] Provenance and simulation labels are correct where relevant.

## Verification

| Check | Command or method | Expected evidence |
| --- | --- | --- |
| Static | `./harness check` | Exit 0 and recorded output |
| Automated | `./harness test` | Exit 0 and test result |
| Golden path | `./harness smoke` | Observable successful outcome |

## Notes and decisions

Record only task-specific facts. Promote durable decisions to `docs/`.
