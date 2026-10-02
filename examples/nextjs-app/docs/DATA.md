# Reference data

Browser tests allocate private unique per-run storage, reset before each case
and inspect real SQLite values/version/audit count after user actions. A test-only
audit trigger proves rollback and retry; invalid/cancelled/denied edits leave
the stored record unchanged. Runner teardown removes only its own fixture;
developer `workroom-local` storage is never removed by journey commands.

Status: current

WI-101 through WI-103 and four identities are owned synthetic records.
SQLite schema v1 stores users, sessions, work_items and audit. Users carry role,
tenant and Argon2 password hash. Sessions store opaque IDs and absolute expiry.
Items carry owner/tenant and an optimistic integer version; audit records only
item/actor/version, not input payloads. Foreign keys and status/role constraints
apply. DTOs contain only id/title/summary/status/display owner/version, not tenant,
identity secrets or hashes. Every entry point validates JSON at runtime: strict
keys, bounded 4 KiB body, trimmed 3–80 title, closed status and positive version.

There is no shared account-data cache. Reads are fresh per request; APIs use
private/no-store and Vary: Cookie, pages are force-dynamic. Saves and audit rows
commit together under BEGIN IMMEDIATE; any storage error rolls back both. A stale
version returns safe conflict without writing. Reload/restart retains commits.

Private marked disposable directories hold runtime.json and data.sqlite. Init
generates local secrets, migration/seed preserve existing edits, explicit reset
clears synthetic data/sessions inside a transaction. No production migration or
rollback strategy is claimed: v1 has no earlier application schema to downgrade.
Unknown versions refuse migration. Local owner controls retention; disposable
HTTP tests clean their exact generated directory and owned server processes.

## Provenance

Source: owned deterministic seed in `src/server/setup.ts`, fictional people,
no external retrieval. Storage and session verification are real local behavior,
not an in-memory repository substitute. External SSO/customer data are absent.
Limitations: no production migration/SSO/retention service is implemented.
Catalogue state cards remain simulated examples, not database outcomes.
