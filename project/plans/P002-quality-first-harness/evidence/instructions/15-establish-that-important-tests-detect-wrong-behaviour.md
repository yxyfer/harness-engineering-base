# Step 15: Establish that important tests detect wrong behaviour

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** critical TypeScript and Python decisions have stronger evidence
than a coverage percentage. Add property tests for meaningful invariants and
bounded mutation checks for selected pure logic. Choose compatible maintained
tools during implementation, and keep slow campaigns outside the fast loop.

Example invariants: invalid operations cannot create stored records; a tenant
cannot gain access by changing only a record ID; valid normalisation is
idempotent; failed atomic imports leave storage unchanged. Select invariants
that fit the implemented contract, not all examples mechanically.

**Done when:** intentionally changed critical decisions are caught; remaining
survivors are explained and addressed; seeds/failing examples are retained;
coverage exposes meaningful gaps without a universal 100% target. A mixed
Next.js/Python API needs real contract tests only if such an integration exists.

```text
Implement Step 15 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/15-establish-that-important-tests-detect-wrong-behaviour.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Review the critical scenario contract and tests
in both reference apps. Add a small set of meaningful generated-input invariants
and targeted mutation checks for critical pure validation/permission decisions.
Use maintained compatible native tools, deterministic seeds and saved failures.

Demonstrate that selected wrong decisions cause tests to fail. Investigate
surviving mutations; do not lower thresholds or add exclusions merely to pass.
Use coverage to identify missing branches, not as a universal quality score.
Keep mutation scope/runtime bounded and its cadence separate from quick
feedback.
If a real mixed-stack API exists, test its request/error/auth contract across
both sides; otherwise record that integration as not applicable.

Write project/plans/P002-quality-first-harness/evidence/QH-15.md with detected defects, unresolved survivors, cost
and scope limitations. Stop after this step.
```
