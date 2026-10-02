# Reference architecture

Status: current

## System shape

Next.js App Router pages/layout are Server Components. Only theme selection,
edit preview, dialog and error recovery use browser state. The server-only
fixture adapter returns typed synthetic values. Pure title validation is shared
without I/O. Vitest tests client controls; Playwright tests the production server.

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
