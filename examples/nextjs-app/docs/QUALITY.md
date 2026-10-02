# Reference quality

Status: current

Native Prettier, strict TypeScript and typed ESLint cover maintained TS/TSX,
configuration and tests. Production builds use real `next build --webpack` with
two workers and no external fonts. Component tests use Vitest/Testing Library;
navigation uses Chromium Playwright against `next start`, with no retries.
Native JUnit collection is retained, not inferred from a successful process.

ESLint 10 uses the official Next plugin and compatible React-hooks/typed rules.
The bundled Next config currently pulls React/import/a11y plugins requiring
unsupported ESLint 9; neither that version nor peer overrides are used. Full
accessibility conformance is not claimed by the native checks below.

Native tests run real production HTTP/session/database cases before component
checks. Separate server JUnit preserves security/storage collection; the parent
ordered Vitest report includes server and domain/components. Component fetch
mocks prove interaction rendering only, not storage. Real HTTP tests prove
storage/authorization. Production Chromium journeys cover real UI sign-in,
list/detail, save/reload, validation, cancellation, duplicate confirmation,
anonymous/viewer/owner/tenant denial and audit-failure recovery. SQL assertions
check committed values, versions and audit counts. One worker resets a unique
per-run database before each isolated context; no retries or arbitrary UI sleeps.
Unexpected console/page errors fail. The recovery case permits at most one exact
Chromium resource-error message for `/api/work-items/WI-101` returning 503; its
response and safe UI error are separately asserted. No other errors are waived.

`npm run smoke` selects the one `@smoke` sign-in/list/detail/save/reload case.
`npm run test:journeys` runs all 22 cases; the reviewed smoke-evidence adapter
runs that full superset in verify and supplies native Playwright JUnit counts.
`npm run test:regressions` builds disposable no-op-save and ownership mutants,
requires intended native assertion failures and retains evidence. It also proves
unexpected console and page errors fail on the healthy production artifact.
`npm run test:cleanup` checks the preceding successful run and interrupts a new
runner at its collection barrier: owned storage must be absent and port 3100
must refuse a connection. Run it after a successful full journey or smoke.

## Step 13 UI controls

`npm run test:ui` selects nine independent cases: four full-page axe/reflow
state cases, four keyboard/focus cases and one lab-performance case. Forty-four
scans/candidates cover list, detail, catalogue, unknown-resource denial, sign-in,
invalid title, confirmation, actual audit-failure recovery, saved/reloaded data,
viewer and real empty list. Catalogue loading/success presentations remain
labelled synthetic; no artificial production loading switch is introduced.
Each deliberate audit failure permits the same one exact 503 console error.

Chromium 153.0.8010.12 / Playwright 1.63.0, macOS 26.7 build 25G229 arm64;
390×1000 and 1440×1000, Paper/Ink, DPR 1, en-GB, UTC, local Arial/Helvetica,
reduced motion, hidden caret and disabled screenshot animation. Dialog images
use the actual viewport; other states capture the full document. No masks or
exclusions. Axe wrapper/engine are locked at 4.13.0, with WCAG 2 A/AA and 2.1
A/AA tags. Native attachments preserve violations and incomplete checks.
Keyboard cases assert navigation/form tab order, skip-to-main, linked invalid
errors, modal initial/trapped/returned focus, Escape and visible 2px focus.
The skip target has tabindex -1, outside sequential Tab order.

`npm run ui:candidates` validates all candidate hashes/source/environment and
generates an ignored review index. `npm run test:visual` selects four required
matrix cases. Missing human approval, environment/hash mismatch or pixel change
fails; snapshots never update automatically. See
[baseline procedure](../tests/visual-baselines/README.md). Candidate hashes and
source digest are also in native JUnit stdout; verify fingerprints maintained
source, tests, configs, locks and eventually approved baselines. The existing
native smoke adapter runs all 22 cases, so pending approval blocks completeness.
Independent UI success is explicitly partial, not a full verify pass.

### Proposed lab budgets

Apple M3 Pro, 18 GiB, warm loopback production server; Chromium CDP 4× CPU,
10 Mbps/20 ms, cache disabled, five full document navigations. Initial runs
measured 334,475 gzip bytes and 86–417 ms DOMContentLoaded; repeated current
measurements are retained in native attachments. The 400,000-byte ceiling gives
19.6% bundle headroom; 900 ms is about 2.2× the observed initial worst navigation,
allowing bounded local scheduler variance without a multi-second tolerance.
These project-owned ceilings are proposals for review, enforced until changed
deliberately in `tests/performance-budgets.json`.

Bundle bytes are the gzip sum of all shipped `.next/static/chunks` JavaScript,
not route first-load transfer. Runtime is desktop Paper detail navigation only,
not field Core Web Vitals, mobile hardware, interaction latency or Lighthouse
score. No hidden retries or discarded timing samples. `test:ui-regressions`
builds actual disposable label/focus/overflow/appearance/oversized-client mutants;
native failures, screenshots/diffs/traces and lab data remain in unique reports.
The healthy screenshot comparator uses an explicitly unapproved synthetic pixel
fixture in a disposable copy, never human acceptance. Owned copies are removed.

Screen-reader announcements, assistive technology, zoom, cognitive usability,
brand/product acceptance and Firefox/WebKit remain unverified. Axe pass is not
accessibility conformance. Reports/traces contain only fictional data and
ephemeral synthetic sessions whose database is removed; do not upload real
credential traces or reuse this setup with production identities.
