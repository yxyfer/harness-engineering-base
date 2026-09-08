# TASK-001: Adopt the three-layer harness structure

- **Status:** complete
- **Owner:** repository owner
- **Related plan:** `plans/active/PROJECT_HARNESS_V2.md`, Phase 1

## Outcome

Make the repository root the directly usable starter layout, with visible
project-owned context, hidden managed harness machinery, and Codex-discoverable
repository skills, while preserving the existing command behaviour.

## Context read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/QUALITY.md`
- `docs/DECISIONS.md`
- `plans/active/PROJECT_HARNESS_V2.md`

## Constraints and non-goals

- Preserve every existing source file and fixture during the move.
- Preserve unrelated repository state.
- Support macOS and paths containing spaces.
- Keep project-owned context visible at the root.
- Do not implement Phase 2 configuration, versioning, installation, adoption,
  standards, or readiness behaviour.

## Acceptance criteria

- [x] `AGENTS.md` and project-owned context are at the repository root.
- [x] Managed commands, checks, and fixtures are under `.harness/`.
- [x] Shipped skills are under `.agents/skills/`.
- [x] `./harness <command>` is the single public command interface.
- [x] The Node and Python fixtures pass inspect, check, test, and smoke.
- [x] Inspect, check, and test pass from a copied path containing spaces.
- [x] Documentation contains no broken local links.
- [x] The obsolete `template/`, `skills/`, `checks/`, and `examples/` paths are
  absent.

## Verification

| Check | Result | Evidence |
| --- | --- | --- |
| Static and policy checks | Pass | `./harness check` against root and both fixtures |
| Automated tests | Pass | Node test and Python unittest fixtures |
| Golden paths | Pass | Both process-level HTTP smoke checks |
| Path safety | Pass | Both fixtures checked from a temporary path containing spaces |
| Structure | Pass | Old directories absent; new paths and executable modes present |

Full evidence is recorded in `verification/PHASE_1_THREE_LAYER_STRUCTURE.md`.

## Notes and decisions

- The former hidden `.common.sh` helper was ignored by the machine's global Git
  rules. It is now the trackable `.harness/bin/common.sh`.
- The repository README explicitly distinguishes new-project use from the future
  Phase 5 existing-project adoption workflow.
