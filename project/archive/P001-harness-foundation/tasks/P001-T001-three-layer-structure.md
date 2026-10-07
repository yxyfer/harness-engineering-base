# P001-T001 — Adopt the three-layer harness structure

- **ID:** P001-T001
- **Plan:** P001
- **Status:** complete
- **Depends on:** none
- **Evidence:** ../evidence/PHASE_1_THREE_LAYER_STRUCTURE.md

## Outcome

Make the repository root the directly usable starter layout, with visible
project-owned context, hidden managed harness machinery, and Codex-discoverable
repository skills, while preserving the existing command behaviour.

## Implementation

[Implementation map](../../../architecture/README.md) · [Original
task](../evidence/legacy-TASK-001-THREE-LAYER-STRUCTURE.md)

## Acceptance

- [x] `AGENTS.md` and project-owned context are at the repository root.
- [x] Managed commands, checks, and fixtures are under `.harness/`.
- [x] Shipped skills are under `.agents/skills/`.
- [x] `./harness <command>` is the single public command interface.
- [x] The Node and Python fixtures pass inspect, check, test, and smoke.
- [x] Inspect, check, and test pass from a copied path containing spaces.
- [x] Documentation contains no broken local links.
- [x] The obsolete `template/`, `skills/`, `checks/`, and `examples/` paths are
  absent.

## Review

Preserve existing verification/approval limits. Source recovery is a reviewed
revert; operational/data recovery remains in the architecture map.
