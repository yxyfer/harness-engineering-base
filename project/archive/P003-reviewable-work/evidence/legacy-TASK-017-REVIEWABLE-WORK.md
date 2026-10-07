# TASK-017: Make work and implementation easy to review

- **Status:** complete locally
- **Owner:** repository maintainer
- **Evidence:** [Verification](REVIEWABLE_WORK.md)
- **Plan:** [Reviewable work](../README.md)

## Outcome

Find current work from one index; read a concise roadmap and only the selected
step; understand harness and reference-app boundaries from linked diagrams.

## Acceptance criteria

- [x] The roadmap is under 150 lines with one progress table and a next action.
- [x] All 19 step outcomes, acceptance criteria and copy-ready prompts survive
  in individual guides, with shared constraints linked explicitly.
- [x] Superseded work is outside active; every existing task remains findable.
- [x] Architecture maps link actual code, choices, trust boundaries and
      evidence.
- [x] New plan/task templates and workflows keep intent, impact, risk, release
  and recovery visible without duplicating canonical context or test logs.
- [x] Required checks and fixture smokes are recorded with honest limitations.

## Reviewer brief

**Why:** Long plans duplicate status and prompts; reviewers lack a short path
from intent to implementation. The stale opening status contradicts the later
table. Existing task IDs and acceptance contracts must remain stable.

**Impact:** Repository navigation, templates, and two shipped workflow skills.
No runtime, dependency, data or permission change. Architecture maps describe
current code and keep synthetic sessions/local SQLite visibly bounded.

**Choice:** One roadmap, task-owned delivery details, canonical architecture
maps, separate execution guides. Avoid another status database or dashboard.

**Risk and recovery:** Moved links or lost instructions; verify link targets and
compare every extracted step with its source. Revert the text diff to recover.
No deployment or migration. Human review still challenges intent and choices;
automated checks only establish their measured scope.

## Verification

Run `./harness check`, `./harness test`, `./harness self-test`, both fixture
smokes, manifest verification and `git diff --check`. Preserve current reports;
write new evidence in
`project/archive/P003-reviewable-work/evidence/REVIEWABLE_WORK.md`.
