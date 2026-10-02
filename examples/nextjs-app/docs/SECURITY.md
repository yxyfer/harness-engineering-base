# Reference security

Status: current; disposable local boundaries, not production certification

Actual credential sign-in uses pinned Argon2 2.2.1; iron-session 9.0.1 seals and
verifies the cookie, with no handwritten cryptography. Only an opaque session
UUID is sealed; current identity/role/tenant and one-hour expiry come from SQLite.
Sign-in rotates/revokes a previous session, logout/reset revoke stored sessions.
Library seal expiry is also checked; its 60-second skew does not extend the
database's hard expiry. Wrong-password attempts lock the user after five failures
for at least 60 seconds; unknown users incur real password verification cost.
No registration, impersonation header, default login or production auth bypass
exists. Generated local credentials are private ignored runtime data.

Cookie is HttpOnly, SameSite=Strict, Path=/ with one-hour lifetime.
Secure=false is limited to the enforced HTTP loopback origin; production auth
is unsupported rather than silently configured. Runtime/storage refuse Vercel,
DEPLOYMENT_ENV=production, DATABASE_URL, broad/noncanonical/symlink targets and
unmarked nonempty directories. This guard is not an OS sandbox or defense against
a privileged local attacker. Node 24's SQLite API is experimental and pinned.

GET reads require a real session and resource ownership/tenant scope. PATCH also
requires editor role, exact Origin/Host, no hostile proxy override/cross-site flag
and strict bounded JSON. Login/logout use the same origin guard. Wrong owner or
tenant yields nondisclosing 404; owned viewer mutation is 403.
Anonymous API is 401. Pages safely redirect/deny without private content;
streamed shell HTTP
status alone is not an access assertion. Validation is 400, stale version 409,
storage failures 503 with fixed safe messages. No raw exception/payload/cookie
is logged. Parameterized SQL handles malicious strings; React escapes text.

No user-data cache is present. Fresh per-request authorization/database reads,
private/no-store and dynamic rendering prevent shared account caching. Tests
prove direct denials, expiry, revocation, restart and transactional audit rollback.
External SSO, password recovery/MFA, TLS/production deployment, adversarial host
isolation remain untested. Browser denial/recovery journeys use actual sessions
and database operations, with no fault or impersonation endpoint. Never expose
this local reference
as a production permissioned service. Catalogue permission/success cards remain
labelled synthetic displays, not controls.
The reviewed npm lock is audited through explicit setup; offline verify consumes
its time/source/version-bound capture. Native secrets/source controls apply.

The external macOS policy denies direct non-loopback networking for verification,
not hostile-code filesystem/IPC escape. Use only trusted synthetic local servers.
No model-provider or production requests belong in tests. Setup/advisory access
is separate from verification. The native server suite uses generated private
credentials, a real disposable database and a trusted local production server.
