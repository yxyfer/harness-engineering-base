# Step 11: Implement secure mutations and real persistence

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** an authorised synthetic user can edit a work item and reload the
saved result. A denied user cannot read or mutate another user's/tenant's data.
Use the selected local database engine for real persistence; test its actual
transaction behaviour, not an in-memory repository substitute.

Keep server entry points thin, runtime-validate input and enforce identity,
role, ownership and tenant scope at the data boundary. Return minimal response
shapes and safe errors. Use a maintained auth/session library where practical;
do not invent cryptography. Synthetic local identities must exercise the actual
session verification and authorisation path. Test adapters are explicit and
cannot enable a production bypass. External SSO remains unverified unless
tested.

Choose a freshness/caching policy explicitly; any cache must preserve isolation
and invalidate after writes. Avoid blanket caching. Define migration/seed/reset
commands for disposable storage and basic failure/recovery semantics. This
follows Next.js
[data-security guidance](https://nextjs.org/docs/app/guides/data-security).

**Done when:** direct server tests prove allowed and denied cases; invalid input
cannot write; a save survives a new read/process; a simulated storage failure
cannot leave a partial committed result; errors/logs omit secrets; cached reads,
if used, neither leak nor remain incorrectly stale.

```text
Implement Step 11 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/11-implement-secure-mutations-and-real-persistence.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Replace the reference app's persistence stubs
with a disposable real database and secure server operations. Use synthetic
local identities through actual session handling; use a maintained library and
no hand-written cryptography or production auth bypass. Label untested SSO.

Implement runtime validation, resource/role/tenant authorisation, minimal DTOs,
safe errors and a deliberate freshness policy. Keep domain decisions testable
separately from I/O. Add repeatable migration/seed/reset commands that refuse
unsafe production targets. Update data and security context for actual
behaviour.

Before UI-only checks, test direct server entry points for allowed,
unauthenticated, wrong-role, wrong-owner, wrong-tenant and invalid-input cases.
Include expired sessions, malicious input and rejected unsafe mutation origins
where relevant. Verify safe rendering, committed storage after reload/restart,
rollback on relevant failure and cache isolation if caching exists. Write
project/plans/P002-quality-first-harness/evidence/QH-11.md and stop.
```
