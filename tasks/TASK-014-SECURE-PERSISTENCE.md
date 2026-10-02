# TASK-014: Persist authorized synthetic work-item edits

- **Status:** active
- **Owner:** repository owner
- **Related plan:** `plans/active/QUALITY_FIRST_HARNESS.md`, Step 11 only

## Outcome

Authenticated synthetic users read only owned tenant work and editors save
validated changes to real disposable SQLite storage. No production auth bypass.

## Acceptance criteria

- [ ] Direct HTTP requests prove allowed, anonymous, role/owner/tenant denials.
- [ ] Expired/tampered/revoked sessions and unsafe origins cannot mutate.
- [ ] Runtime input validation, minimal DTOs and safe errors are demonstrated.
- [ ] Committed writes survive reread/restart; failed audit writes roll back.
- [ ] Migration/seed/reset refuse production, unsafe paths and symlinks.
- [ ] React escapes malicious stored text; no user-data cache is introduced.
- [ ] Native static/tests/build and harness checks retain meaningful evidence.
- [ ] Context and QH-11 describe actual boundaries and remaining gaps.

## Constraints and verification

Step 10 browser evidence remains partial. The owner stopped browser execution;
do not run browsers or claim visual acceptance. Use direct production HTTP
tests before component checks. No SSO, production deployment, installer or
Step 12 journey expansion. All prior working-tree changes are preserved.

SQLite uses the pinned Node runtime; iron-session owns cookie cryptography,
Argon2 owns password hashing, Zod validates input. Sessions are database-backed
for expiry/revocation. Local setup generates synthetic credentials, never a
hardcoded impersonation route. Runtime is loopback/disposable only and fails
closed if misconfigured. No automatic production deployment support is implied.
