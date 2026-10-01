# TASK-003: Establish an enforceable engineering baseline

- **Status:** complete
- **Owner:** repository owner
- **Related plan:** `plans/active/PROJECT_HARNESS_V2.md`

## Outcome

Projects receive a concise shared engineering baseline, idiomatic language
profiles, and executable checks that select only the standards relevant to the
project.

## Context to read

- `AGENTS.md`
- `docs/ARCHITECTURE.md`, `docs/QUALITY.md`, and `docs/SECURITY.md`
- Phase 3 of `plans/active/PROJECT_HARNESS_V2.md`
- `.harness/config.toml`

## Constraints and non-goals

- Use an 80-character shared line width.
- Keep large-file and large-function thresholds advisory.
- Prefer established language tools over custom style parsers.
- Do not implement the Phase 6 exception registry or the Phase 4 installer.
- Do not make TDD, DRY, or numeric size limits absolute rules.

## Acceptance criteria

- [x] Shared standards cover implementation, naming, testing, and architecture.
- [x] Python, TypeScript/JavaScript, shell, and Markdown profiles are explicit.
- [x] `./harness check` detects relevant profiles and uses configured tools when
      available.
- [x] One check command reports formatter drift consistently.
- [x] Size warnings include their threshold and the route for an exception.
- [x] Generated, vendored, dependency, migration, schema, and fixture paths are
      explicitly excluded from generic size analysis.
- [x] Fixture tool configuration agrees with the shared 80-character limit.

## Verification

| Check | Command or method | Expected evidence |
| --- | --- | --- |
| Static | `./harness check` | Exit 0; standards profile and tool results shown |
| Automated | `./harness test` | Exit 0; Phase 3 contract tests pass |
| Golden path | fixture `check`, `test`, and `smoke` commands | Both fixtures pass |

## Notes and decisions

The full time-bound exception registry remains Phase 6 work. Until then,
exceptions use the narrowest tool-native suppression and must state why.

The existing Phase 2 `config.py:validate` function exceeds the advisory
50-line threshold. It remains cohesive around one schema-validation transaction;
split it when the schema gains another section or a second consumer needs its
sub-validation steps.
