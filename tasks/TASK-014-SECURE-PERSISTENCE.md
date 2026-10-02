# TASK-014: Persist authorized synthetic work-item edits

- **Status:** partially verified; server evidence passes, browser execution paused
- **Owner:** repository owner
- **Related plan:** `plans/active/QUALITY_FIRST_HARNESS.md`, Step 11 only

## Outcome

Authenticated synthetic users read only owned tenant work and editors save
validated changes to real disposable SQLite storage. No production auth bypass.

## Acceptance criteria

- [x] Direct HTTP requests prove allowed, anonymous, role/owner/tenant denials.
- [x] Expired/tampered/revoked sessions and unsafe origins cannot mutate.
- [x] Runtime input validation, minimal DTOs and safe errors are demonstrated.
- [x] Committed writes survive reread/restart; failed audit writes roll back.
- [x] Migration/seed/reset refuse production, unsafe paths and symlinks.
- [x] React escapes malicious stored text; no user-data cache is introduced.
- [x] Native static/tests/build and harness checks retain meaningful evidence.
- [x] Context and QH-11 describe actual boundaries and remaining gaps.
- [ ] Updated browser UI/rendered evidence remains owner-paused.

## Cohesion review

The server integration file holds one production-server fixture and 14 named
boundary cases. Its formatter-expanded length exceeds the 350-line advisory;
it is not suppressed or treated as a hard gate. Shared request/runtime setup
stays in one place while the independent domain and client suites stay separate.
Extract the fixture if another integration family needs it, not a second runner.

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
