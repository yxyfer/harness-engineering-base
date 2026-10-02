# Workroom: real Next.js reference

A synthetic work-item list/detail/edit foundation, not a deployed product.
Next.js 16.3.8 / React 19.3.0, Node 24.10.0 / npm 11.6.0; exact npm lock.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run db:init
PLAYWRIGHT_BROWSERS_PATH=.harness/tmp/browsers node node_modules/@playwright/test/cli.js install chromium
npm run check
npm run build
npm test
PLAYWRIGHT_BROWSERS_PATH=.harness/tmp/browsers npm run smoke
npm run start
```

Browser installation is explicit online setup. Build uses webpack deliberately
for a bounded, inspectable production baseline; two workers, no remote fonts.
Smoke starts its own production server at 127.0.0.1:3100, refuses a pre-existing
server and signs in, opens owned work, saves, reloads and asserts actual SQLite.
`npm run test:journeys` runs all 22 production cases. `npm run test:regressions`
builds disposable copies and proves broken save/ownership/browser-error detection.
`npm run test:cleanup` follows a successful journey run and proves success/SIGINT
storage/server cleanup. All fixtures are synthetic and unique; lifecycle scripts
are outside production routes. Run harness commands from the repo root:

```sh
./harness check examples/nextjs-app
./harness test examples/nextjs-app
./harness start examples/nextjs-app
./harness smoke examples/nextjs-app
./harness verify examples/nextjs-app
```

Use external macOS isolation and scoped synthetic data for verification; browser
route restrictions alone are not a network sandbox. Missing browser/runtime or
advisory data must fail, not trigger installation during tests. See root security
setup instructions for pinned scanners and explicit advisory capture.

## Ownership and reuse

Everything here is project-owned: source, adapted shadcn-style controls, themes,
native configs and dependency lock. None enters `.harness/release-files.json`.
Radix/cva/clsx/tailwind-merge are normal pinned dependencies. There is no remote
component registry, automatic component upgrade, shared package or installer.
The small owned kit adapts MIT shadcn patterns; its API/reuse rules and upstream
references are in `docs/DESIGN.md`. Review copied-source changes like other code.

The existing `.harness/tests/fixtures/nextjs-project` remains a lightweight Node
dispatcher fixture. It is not evidence that Next.js itself builds or runs.
Run packages separately: root multi-package aggregation is not implemented.

## Honest limits

All records/people are synthetic. Sign in with alex, sam, viewer or outsider and
the generated password in private `.harness/tmp/workroom-local/runtime.json`.
Never commit that file or copy it into a deployment. No identity-only test login
route exists. Edits commit to actual SQLite; refresh/restart retains them.
Viewer can read owned work; only editors can write owned same-tenant work.
Other resources are hidden. External SSO and production deployment are untested
and unsupported; this is a disposable loopback application, not production auth.

`npm run db:migrate` and `npm run db:seed` are repeatable without discarding edits.
`npm run db:reset` explicitly resets only a marked safe disposable target and
revokes sessions. All commands refuse unsafe targets/production markers/links.
Set `WORKROOM_DB_DIR` only to a canonical private `workroom-*` directory directly
under app `.harness/tmp` or the current canonical temporary directory.

`npm run test:server` calls actual production HTTP endpoints, uses its own fresh
database, proves permissions/expiry/rollback/restart, and cleans owned processes
and data. `npm test` uses native ordered Vitest projects: direct server first,
then domain/components. Native JUnit evidence is available for both. No shared
user-data cache exists; dynamic pages and API responses are private/no-store.
No-access/success catalogue cards remain labelled display examples. Browser
journeys execute in Step 12 under renewed explicit authorization. Verify runs
the full journey superset through native JUnit, while the smoke command remains
one meaningful case. Step 13 adds `test:ui`, `test:visual`, `ui:candidates` and
`test:ui-regressions`; see [quality scope](docs/QUALITY.md) and the
[human baseline procedure](tests/visual-baselines/README.md). Missing visual
approval intentionally fails the full native suite/verify, while independent
UI checks can pass. No baseline is auto-approved. Firefox/WebKit, assistive
technology and human product acceptance remain unverified.
