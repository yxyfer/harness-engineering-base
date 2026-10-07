# Step 16: Enforce the full policy and simplify agent guidance

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** full applicable checks run in CI independently of an agent's
completion claim; agents receive concise relevant instructions.

Extend Step 05's workflow to both real examples, security, browser checks and
required evidence. Keep unit/static feedback fast, with explicit broader jobs
for relevant capabilities. Expensive mutation checks may use a separate release
cadence; no partial PR run may claim that the full release suite passed.
Required jobs must not accidentally disappear through path filters or
cancellation.

Prepare protected review for workflows, harness policy, test configuration,
exceptions and visual baselines. Use existing CI/CODEOWNERS capabilities and
verified maintainers; do not invent usernames. Rule enforcement is repository
configuration outside a checked-in file. Prepare exact changes and, where
required, obtain owner approval before applying them. Verify actual settings
before claiming protection. See
[protected branch
controls](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Reduce `AGENTS.md` and skills to workflow maps, reuse rules and relevant command
links. Preserve obligations; replace duplicated prose with implemented native
configuration. Changes to shipped skills need the normal managed-file process.
Keep the global entry point short; no large always-loaded component catalogue.

**Done when:** a failing app, missing artifact and weakened policy change are
visible at the correct boundary; fast/full scopes cannot be confused; CI has no
model-provider credentials; guidance matches commands. Record prepared versus
actually enforced controls separately. Local pilots may proceed with that
limitation while external protection approval is pending; release claims cannot.

```text
Implement Step 16 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/16-enforce-the-full-policy-and-simplify-agent-guidance.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Extend core CI to run the full required policy
for both real examples, including security, browser and evidence checks. Define
fast feedback and full release scopes with honest completeness. Avoid path
filters, cancellation or continue-on-error hiding required failures.

Prepare independent protection of gate/config/test/baseline changes using the
existing CI provider and real maintainer ownership. Do not claim protection from
YAML or CODEOWNERS alone. Prepare reviewable remote-setting changes and follow
required owner approval before applying them; verify settings when available.

Simplify agent instructions and shipped skills to relevant workflow maps and
reuse guidance. Do not add AI reviewers or an orchestration layer. Prove failure
propagation and missing-artifact handling, and record local/remote evidence and
pending external controls in project/plans/P002-quality-first-harness/evidence/QH-16.md. Stop.
```
