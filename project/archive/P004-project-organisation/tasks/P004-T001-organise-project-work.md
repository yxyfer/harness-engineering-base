# P004-T001 — Organise project work

- **ID:** P004-T001
- **Plan:** P004
- **Status:** complete
- **Depends on:** none
- **Evidence:** ../evidence/REPORT.md

## Outcome

Navigate one project folder with plan-owned tasks/evidence and a current
architecture view.

## Implementation

[Record contract](../../../../.harness/bin/project_records.py) ·
[Index/archive helper](../../../../.harness/bin/project_work.py).

## Acceptance

- [x] All existing records migrate with old/new path provenance.
- [x] IDs, dependencies, acceptance, evidence and generated indexes are checked.
- [x] Complete-plan archive preserves evidence and repairs links.
- [x] Required native, contract and fixture checks pass.

## Review

Migration is reversible from the saved pre-change tree; artifacts retain bytes.
Archive has guarded completion and ordinary write-error rollback. Process crash
atomicity is not claimed. Human visual approval remains pending for P002-T013.

The archive function exceeds the advisory 50-line limit: completion checks,
precomputed edits, move and rollback remain one cohesive operation. Helpers
separate link rewriting and index generation; the failure-path test covers rollback.
