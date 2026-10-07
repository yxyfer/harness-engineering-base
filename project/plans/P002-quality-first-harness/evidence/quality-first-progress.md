# Quality-first historical progress notes

Historical notes through Step 09, retained from the original roadmap. Statements
about unfinished steps/tools describe those earlier runs, not current status.
Use the [current roadmap](../README.md).

This expanded plan and its prompts were authored on 2026-10-01. Step 01 was
executed separately against the current dirty tree: see
[TASK-004](../tasks/P002-T001-quality-baseline.md) and
[QH-01 evidence](QH-01.md). The refreshed matrix, F1-F7
regression contracts, synthetic application cases and measurement format are
recorded. Runtime code was not repaired. The baseline remains partial, with
F1-F7 open, missing tools and undefined root smoke explicitly retained.

Step 02 is complete:
[TASK-005](../tasks/P002-T002-application-test-routing.md) and
[QH-02](QH-02.md) record F1/F2 reproductions, installed-copy
regressions, separate application/self-test commands, declared Python runners,
zero-collection failures and compatibility. That run had 28 passing kit cases;
fixture smoke checks pass after recorded sandbox retries. Static tool gaps and
undefined root smoke remain visible; F3-F7 are not repaired.

Step 03 is complete:
[TASK-006](../tasks/P002-T003-discovery-and-check-precedence.md) and
[QH-03](QH-03.md) record F3–F5 reproductions, shared
discovery, exclusion/shebang/symlink contracts and single static implementation
resolution after policy checks. Both root suites pass 46 cases, including 18 new
regressions. Both fixture smokes pass after recorded permission retries;
optional native tool gaps and undefined root smoke remain visible. Managed
ownership findings F6–F7 remain for Step 04.

Step 04 is complete: [TASK-007](../tasks/P002-T004-release-ownership.md) and
[QH-04](QH-04.md) record F6/F7 before/after probes, explicit
release ownership, 15 full-copy regression cases, unsafe path/symlink rejection,
and deterministic generation from reviewed inputs. Both root suites pass 61
cases; both fixture smokes pass after recorded permission retries. Consumer
content and conflict evidence remain preserved. Optional native-tool gaps and
undefined root smoke remain visible.

Step 05 is complete locally: [TASK-008](../tasks/P002-T005-core-ci.md) and
[QH-05](QH-05.md) record pinned macOS CI, locked clean setup,
actual native tools, both 61-case core suites, fixture tests/smokes and rejected
negative controls. Remote execution is unverified; protection settings are
unchanged. Root smoke remains undefined.

Steps 06-08 are complete locally: QH-06, QH-07 and QH-08 document selection,
native tools and input-bound evidence. Root verify remains incomplete because
root smoke is undefined; actual fixture verify/smoke are the applicable
acceptance evidence. Remote CI is unverified. Step 09 is complete locally;
QH-09 records executable security, 147-case test/self-test passes and actual
external macOS denial probes. Existing pytest advisories block security
approval;
no automatic fixes or exceptions were applied. Step 10 is not started. Future
application journey acceptance cases remain specifications, not execution
evidence.
