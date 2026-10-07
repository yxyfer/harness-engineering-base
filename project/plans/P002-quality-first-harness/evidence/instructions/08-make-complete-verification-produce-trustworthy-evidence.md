# Step 08: Make complete verification produce trustworthy evidence

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** `verify` runs the full applicable suite and emits a validated JSON
report plus a readable summary. Reuse resolution from Step 06. Do not build a
parallel scheduler. Native runner output supplies collection and outcomes.

Each control reports `passed`, `failed`, `unavailable` or `not-applicable` with
a reason. A required failed/unavailable control makes full verification
non-zero. A local selected subset is visibly partial and cannot be presented as
complete. Unexpected skips, flaky retries and absent artifacts cannot disappear
into a success count. Opaque custom runners need a documented evidence adapter
before claiming complete test verification.

Record source revision and working-tree input digest, selected configuration,
lockfiles, harness/tool versions, scope, commands with secrets redacted, exit
codes, duration, collection/skips/retries and artifact hashes. Include relevant
untracked source; exclude declared output directories so writing the report does
not invalidate itself. Detect input changes during execution. Treat this as
provenance, not a cryptographic guarantee against a malicious editor.

**Done when:** clean/failing/unavailable/partial runs have correct reports and
exits; zero collection and malformed/missing artifacts fail; an input edit makes
old evidence stale; timeouts and interrupts terminate owned child processes;
logs are bounded and synthetic secret markers are redacted.

```text
Implement Step 08 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/08-make-complete-verification-produce-trustworthy-evidence.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Build verify as a thin coordinator of the shared
applicable controls. Produce schema-validated JSON and a short human summary.
Use native runner reports for counts and outcomes; never invent collection data
from a successful shell exit. Make missing required evidence fail explicitly.

Implement honest per-control states, overall completeness and non-zero exits for
required failures/unavailability. Preserve retries/skips. Fingerprint actual
source, including relevant untracked files, config and locks; exclude generated
reports. Reject stale evidence and detect inputs changed mid-run. Bound logs,
redact secrets and clean up owned processes on timeout or interruption.

Test success, failure, zero tests, missing/malformed reports, partial scope,
stale inputs, flaky retries, interrupts and secret redaction. Prove report
writing does not invalidate its own input identity. Document the trust limits,
write project/plans/P002-quality-first-harness/evidence/QH-08.md, and stop.
```
