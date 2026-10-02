# Reference architecture

Status: current

## System shape

Next.js App Router pages/layout are Server Components. Only theme selection,
edit draft, dialog, sign-in/out and error recovery use browser state. Server-only
data access validates stored rows and emits minimal DTOs. Pure access policy is
independent of I/O; Zod validates untrusted JSON at HTTP entry points. Node's
SQLite driver executes prepared statements and real transactions. Iron-session
owns cookie sealing/verification; Argon2 owns password hashing. The database
stores revocable sessions and roles rather than trusting cookie role claims.
Vitest first calls actual production HTTP, then tests domain/client controls.
Playwright calls the real production build with unique disposable SQLite and
actual credential sessions. Test-only scripts own fixture processes/storage;
audit failure injection uses a real SQLite trigger, never a production switch.
The native runner explicitly stops its recorded server children and process
group even when interrupted before Playwright installs its own teardown.
Step 13 keeps axe, keyboard, pixel comparison and lab budgets in native project
tests. The existing JUnit adapter delegates all cases; no application-specific
engine or extra policy language is introduced. Missing human screenshot approval
is a visible native failure, not a silently skipped control.

## Boundaries

UI imports domain types, not server adapters. Pages retrieve server data and
pass serializable values to the editor. Native ESLint protects the demonstrated
UI/domain imports; Next.js enforces server-only boundaries at build time.
The Next.js/React dependencies and all app files are project-owned; lockfile
updates require review. There is no shared-package extraction or installer.

## External systems

No live systems. Explicit setup downloads registry packages and Chromium.
Application verification runs with synthetic input under the external macOS
direct-egress policy; loopback server only. Browser routes additionally deny
non-local traffic, but that route rule is not the OS sandbox.
