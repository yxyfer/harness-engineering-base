# Naming standard

Names describe domain meaning and remain consistent within a concept. Prefer a
clear full word to an unfamiliar abbreviation. Avoid encoding types or
implementation details in names.

## Shared semantics

- Boolean names read as predicates: `is_ready`, `has_access`, `can_publish`, or
  their idiomatic language equivalent.
- Functions use verbs or verb phrases; data types and components use nouns.
- Constants describe meaning, not merely their literal value.
- Tests name the behaviour and condition being demonstrated.
- Private symbols use the language's supported visibility mechanism. A naming
  prefix is only a convention where the language lacks one.
- Interfaces are named for the capability or role they expose; do not add `I`
  solely to signal that something is an interface.

## Casing map

| Construct | Python | TypeScript/JavaScript | Shell | Markdown |
| --- | --- | --- | --- | --- |
| Variables/functions | `snake_case` | `camelCase` | `snake_case` | n/a |
| Types/classes | `PascalCase` | `PascalCase` | n/a | n/a |
| Constants | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | n/a |
| Source files | `snake_case.py` | project convention; prefer `kebab-case` | `kebab-case` | `UPPERCASE.md` for canonical context, otherwise `kebab-case.md` |
| Test files | `test_*.py` | `*.test.ts` or `*.test.js` | `*-test.sh` | n/a |

Framework conventions take precedence for framework-owned filenames such as
`page.tsx`. Do not rename established public APIs merely to satisfy this table;
treat compatibility as a stronger constraint.
