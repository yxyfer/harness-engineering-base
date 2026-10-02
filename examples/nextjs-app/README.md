# Workroom: real Next.js reference

A synthetic work-item list/detail/edit foundation, not a deployed product.
Next.js 16.3.8 / React 19.3.0, Node 24.10.0 / npm 11.6.0; exact npm lock.

```sh
npm ci --ignore-scripts --no-audit --no-fund
PLAYWRIGHT_BROWSERS_PATH=.harness/tmp/browsers node node_modules/@playwright/test/cli.js install chromium
npm run check
npm test
npm run build
PLAYWRIGHT_BROWSERS_PATH=.harness/tmp/browsers npm run smoke
npm run start
```

Browser installation is explicit online setup. Build uses webpack deliberately
for a bounded, inspectable production baseline; two workers, no remote fonts.
Smoke starts its own production server at 127.0.0.1:3100, refuses a pre-existing
server and performs real navigation. Run harness commands from the repo root:

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

All records/people are synthetic. Edit confirmation applies a browser-memory
preview; reload resets it. No authentication, authorization, database or mutation
endpoint exists. No-access and success cards are examples, not enforced access
or persisted saves. Persistence/auth belong to Step 11. Initial component and
navigation tests are not full accessibility/performance/visual acceptance.
