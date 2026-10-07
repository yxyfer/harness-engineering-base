# Step 02: Separate application tests from harness tests

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** `test` tests the application; `self-test` tests the harness. Fix
F1/F2 while retaining explicit overrides and declared unittest support.
Configure this repository's own root test command deliberately, without
recursion.

**Done when:** an installed harness plus a failing app test fails; absent pytest
cannot drop module-level cases; explicit unittest works; zero required tests
fail; both suites run independently with honest exit states.

```text
Implement Step 02 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/02-separate-application-tests-from-harness-tests.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Read F1/F2 and the dispatcher, resolver and
tests.

First reproduce failing application tests being hidden by harness self-tests,
and mixed pytest/unittest suites losing pytest cases when pytest is absent.
Add self-test and make test resolve the application's declared runner and local
environment. Preserve override precedence and explicit unittest projects.
Never switch runners because one is missing. Configure this repository's own
test command deliberately and avoid recursion.

Add regressions using disposable installed projects, including missing runners
and zero collected required tests. Run both suites and fixture commands, update
the intended managed inventory, document compatibility, and save before/after
evidence in project/plans/P002-quality-first-harness/evidence/QH-02.md. Stop after this step.
```
