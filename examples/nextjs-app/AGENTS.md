# Reference app contract

Read `docs/` and the repository-root engineering standards before editing.
Run native `npm run check`, `npm test`, `npm run build` and `npm run smoke`.
Harness commands are invoked from the repository root with this target.

All files here are project-owned, including adapted shadcn-style component
source, native config and lockfile. None belongs to the shipped kit inventory.
Use deterministic synthetic identities/data and trusted loopback only. Local
SQLite and iron-session are real boundaries; SSO/production deployment are not
supported. Run the production build before direct server tests. Keep native
server tests before component tests. Do not run browsers without authorization.
