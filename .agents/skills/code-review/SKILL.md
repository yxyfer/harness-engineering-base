---
name: code-review
description: Review a code change for concrete correctness, security, maintainability, and verification gaps. Use when the user asks for review rather than implementation.
---

# Code Review

Read `AGENTS.md`, the relevant context, and the complete change against its target
base. Inspect callers and tests needed to understand behaviour.

Prioritise defects that can produce incorrect behaviour, data loss, security or
privacy exposure, broken compatibility, misleading demo behaviour, or an
unverified acceptance claim. Do not report a preference as a defect.

For every finding, identify the tightest code location, the triggering conditions,
the observable impact, and why existing verification misses it. Rank by severity
and confidence. Avoid duplicating one root cause across several findings.

Do not edit code unless explicitly asked. If no actionable defect is found, say
so and note material untested risks or verification limits.
