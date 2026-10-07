# P001 — Harness foundation

- **ID:** P001
- **Status:** superseded

## Outcome

Establish repository layers, configuration and engineering standards.

## Approach

[Original roadmap](evidence/legacy-plan.md). Phases 1–3 were delivered; the
remaining sequence was replaced by P002 and is not marked complete.

## Architecture impact

[Shared architecture](../../architecture/README.md). No active implementation
sequence remains in this archived direction.

## Tasks

<!-- project:tasks:start -->
| Task | Adds | State | Depends on |
| --- | --- | --- | --- |
| [P001-T001 — Adopt the three-layer harness structure](tasks/P001-T001-three-layer-structure.md) | Make the repository root the directly usable starter layout, with visible project-owned context, hidden managed harness machinery, and Codex-discoverable repository skills, while preserving the existing command behaviour. | complete | none |
| [P001-T002 — Add the versioned harness configuration contract](tasks/P001-T002-versioned-configuration.md) | Give the harness one offline, machine-readable contract for its version, configuration, managed files, command precedence, and exit behaviour. Make the effective configuration and its source visible without editing harness scripts. | complete | P001-T001 |
| [P001-T003 — Establish an enforceable engineering baseline](tasks/P001-T003-engineering-standards.md) | Projects receive a concise shared engineering baseline, idiomatic language profiles, and executable checks that select only the standards relevant to the project. | complete | P001-T002 |
<!-- project:tasks:end -->
