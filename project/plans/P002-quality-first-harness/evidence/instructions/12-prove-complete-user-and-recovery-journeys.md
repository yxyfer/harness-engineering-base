# Step 12: Prove complete user and recovery journeys

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** browser tests demonstrate customer actions and resulting state, not
just page availability. Run Playwright against the built Next.js application
with isolated storage, fixed data and controlled time where relevant.

Cover list/detail, edit/save/reload, invalid input, cancellation, duplicate
submission, permission denial and recoverable save failure. Validate persistence
through the real data path. Fault injection happens at the dependency that
fails; do not mock the action under test. Keep fixture fault controls out of
normal production routes. Native reports feed Step 08's evidence adapters.

**Done when:** main and recovery journeys pass; replacing save with a no-op
fails; an authorisation defect fails direct-boundary tests; invalid data remains
absent from storage; unexpected browser errors fail; servers/storage are cleaned
up. The `smoke` script is a small meaningful subset, not an HTTP 200 probe.

```text
Implement Step 12 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/12-prove-complete-user-and-recovery-journeys.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add Playwright journeys against the production
build and real disposable persistence. Test list/detail, edit/save/reload,
validation, cancellation, repeated submission, denied access and save recovery.
Use stable semantic locators and isolated fixtures; avoid arbitrary sleeps.

Assert user-visible outcomes plus durable data changes. Inject failures at an
explicit test dependency boundary, not by mocking the operation being verified.
Keep test fault controls out of normal production paths. Define a small real
smoke journey, feed native results to verify, and clean up processes/storage.

Demonstrate that a broken save handler and a representative access-control
regression are caught in disposable copies. Treat unexpected console/page errors
as failures, with narrowly documented expected errors for deliberate negative
cases. Write project/plans/P002-quality-first-harness/evidence/QH-12.md and stop.
```
