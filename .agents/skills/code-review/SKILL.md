---
name: code-review
description: Review a code change for concrete correctness, security, maintainability, and verification gaps. Use when the user asks for review rather than implementation.
---

# Code Review

Read `AGENTS.md`, the relevant context, and the complete change against its target
base. Inspect callers and tests needed to understand behaviour.

Start with the task's reviewer brief and canonical architecture map when
present. Challenge necessity, scope and the implementation choice; trace the
affected boundaries to source and ADRs. Assess operational context, deployment
and recovery, and surface material missing context for human discussion.
Automated checks support review; they do not establish human understanding or
approval. Missing briefs/maps in older work do not alone establish a defect.

For adopted projects, start at `project/README.md` and follow the selected plan's
`PNNN-TNNN` task. Read shared systems/feature maps in `project/architecture/`, then
task-specific evidence. Check IDs, status/dependencies and derived navigation with
`./harness project check`; mechanical consistency is not semantic approval.

Prioritise defects that can produce incorrect behaviour, data loss, security or
privacy exposure, broken compatibility, misleading demo behaviour, or an
unverified acceptance claim. Do not report a preference as a defect.

For every finding, identify the tightest code location, the triggering conditions,
the observable impact, and why existing verification misses it. Rank by severity
and confidence. Avoid duplicating one root cause across several findings.

Do not edit code unless explicitly asked. If no actionable defect is found, say
so and note material untested risks or verification limits.
