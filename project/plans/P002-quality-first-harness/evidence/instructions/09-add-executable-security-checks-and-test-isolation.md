# Step 09: Add executable security checks and test isolation

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** secret, dependency and applicable static security checks run as
programs. Test execution uses scoped synthetic environments. This adds evidence
about specific threats; it is not a complete security certification.

Select maintained tools at implementation time, favouring existing project/CI
capabilities. Keep scanning local where practical. Pin tools and rule sets;
record advisory data source/time. Separate policy findings from scanner failure,
missing tools and unavailable/stale advisory data. Define blocking severities
and narrow owner/reason/expiry exceptions in reviewable configuration.

Populate the harness trust model in `docs/SECURITY.md`: configured commands are
executable repository code; the harness is not its own sandbox. Do not expose
real secrets to untrusted pull requests. Use external runtime/CI controls for
network isolation, with only necessary local test services. If egress cannot be
enforced on a supported environment, say so and leave that guarantee unverified.

**Done when:** fake secret and vulnerable-advisory fixtures trigger findings;
clean cases pass; scanner failure cannot pass; model-provider/production
attempts are blocked in the verified isolated setup; output does not disclose
test secrets.

```text
Implement Step 09 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/09-add-executable-security-checks-and-test-isolation.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Select a minimal maintained programmatic security
baseline for secrets, locked dependencies and applicable source checks. Prefer
existing native/CI tools, pin versions and record advisory provenance. Separate
findings, errors and unavailable data; no automatic fixes or blanket ignores.

Define reviewable severity/exception rules and fill the actual harness security
context. Separate dependency/advisory setup access from application test access.
Use synthetic secrets, scoped environments and external runtime/CI isolation to
prevent production and model-provider calls during verification. Do not claim
that a text rule or URL regex is an effective network sandbox.

Test representative findings, safe cases, expired exceptions, scanner failure,
missing data, secret redaction and denied egress in the supported setup. Record
remaining environment limits in project/plans/P002-quality-first-harness/evidence/QH-09.md and stop.
```
