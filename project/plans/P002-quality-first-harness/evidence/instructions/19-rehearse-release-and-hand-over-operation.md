# Step 19: Rehearse release and hand over operation

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** a new maintainer can start, verify, troubleshoot and update
supported projects from accurate instructions. This produces a local release
candidate; public release/deployment is a separate authorised action.

Rehearse from a clean environment with a new TypeScript/Next.js project, a
Python project and an existing project with custom conventions. Run complete
applicable checks, confirm deliberate defects fail, and rehearse recovery.
Record exact supported runtimes, platforms, tools, profile capabilities and
limitations.

Replace obsolete phase references and template status only where implemented
facts justify it. Complete relevant product/design/data/security context,
command reference, maintenance ownership, dependency update cadence and failure
recovery instructions. Keep examples and component contracts small. Define how a
control can be deprecated without silently reducing a consumer's required
verification.

**Done when:** onboarding and recovery are reproducible; no implemented scope is
misrepresented; all required evidence and actual approvals are linked; remaining
debt has concrete owners/triggers. Move this plan to completed only when its
criteria really hold, updating inbound links so they remain valid.

```text
Implement Step 19 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/19-rehearse-release-and-hand-over-operation.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Rehearse a local release candidate in clean
supported environments for new Next.js/Python projects and an existing project
with custom conventions. Verify full checks, representative failure detection,
adoption/update recovery and absence of verification model calls.

Reconcile documentation with implemented capabilities, remove obsolete phase
claims, and publish no unsupported guarantees. Document versions, ownership,
setup, relevant controls, evidence, troubleshooting, update policy and recovery.
Link real CI/protection/visual acceptance evidence; keep gaps explicit. No
public release, deployment or production access is authorised by this prompt.

Write project/plans/P002-quality-first-harness/evidence/QH-19.md. Mark the plan complete and move it to completed
only if all completion criteria are evidenced; update inbound links.
Otherwise leave it active with precise outstanding work. Stop with the
release-readiness result.
```
