# Project format

Format: 1

| Record | Location | Required format |
| --- | --- | --- |
| Plan | `plans/P001-plan-name/README.md` | ID, status; Outcome, Approach, Architecture impact, generated Tasks |
| Task | `tasks/P001-T001-task-name.md` inside its plan | ID, parent plan, status, dependencies, evidence; Outcome, Implementation, Acceptance, Review |
| Architecture | `architecture/` | README diagram; systems inventory; feature flows |
| Evidence | `evidence/` inside its plan | Report, commands/results, inputs and limitations |
| Archive | `archive/P001-plan-name/` | Complete or explicitly superseded plan bundle |

IDs are immutable. Plan numbers are project-wide; task numbers restart per plan.
Use three digits and lowercase kebab-case names. Outcomes are at most 60 words.
Every task belongs to its folder's plan. Dependencies use task IDs; evidence
uses relative file paths within the same bundle. `pending` is allowed before
complete.

Task states: `planned`, `ready`, `active`, `blocked`, `partial`, `complete`.
Plan states: `proposed`, `active`, `blocked`, `complete`, `superseded`.
Complete requires checked acceptance and existing evidence. Partial evidence and
human acceptance remain explicit; no automated pass supplies human approval.

| Action | Command |
| --- | --- |
| Refresh progress/navigation | `./harness project sync` |
| Validate structure and derived indexes | `./harness project check` |
| Archive a complete bundle and repair links | `./harness project archive P001` |

Edit task state once; never hand-edit generated tables. Complete tasks stay with
an active plan. Archiving moves the whole bundle and retains IDs/evidence; the
shared architecture remains current. Superseded plans retain unfinished scope.
Archive is reversible, with rollback for ordinary write failures; process-crash
atomicity is not claimed. Restore archived work through a reviewed move and
sync.

Read plan → task → implementation/evidence. Link source and choices; avoid logs
and chronological notes in summaries. Use [templates](templates/) for new work.
`FORMAT.md` opts this contract into checks; unrelated legacy projects are not
forced to migrate. See [migration IDs](migration.md) for previous record names.
