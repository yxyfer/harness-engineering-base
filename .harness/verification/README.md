# Verification evidence contract

`./harness verify [target]` coordinates check, native application tests and smoke.
`--self-test` adds the independent kit suite for harness changes. Shared
selection retains unsupported requirements. Static results are one aggregate:
a failed aggregate does not claim every underlying tool ran. Reasons list scope.

`--only check tests smoke self-test` selects partial local work: it remains
incomplete/non-zero even when selected controls pass. `--timeout SECONDS` bounds
each control (default 180, maximum 1800). No retries, installs, formatter writes
or model grading are added.

## Native evidence

Identity, multi-tenancy and persistence require a separate native server suite:
review `test:server` plus project-owned `.harness/server-evidence.json` using the
same fixed adapter/argv shape, restricted to JUnit. `verify` runs the required
`server-boundaries` control before application tests, after the production build
where applicable. Missing/zero/failed reports and partial omissions fail closed.
Projects own scenario adequacy; declaring this contract does not certify SSO,
production auth or arbitrary database security. No scenario/policy DSL is added.

Python preserves existing pytest/unittest metadata and local environments.
Pytest writes JUnit; the stdlib adapter serializes discovery and TestResult
counts. JUnit reads testcase records and failure/error/skip/rerun/flaky tags.
Node's direct-testcase variant is supported. Counts never come from a successful
shell exit or scraped stdout. Opaque package/configured commands require a
reviewed project-owned `.harness/evidence.json`:

```json
{
  "adapter": "junit",
  "command": ["project-local-runner", "--junit", "{report}"]
}
```

The argv must invoke the same required suite, not a smaller replacement.
`{report}` expands to a fresh path; `HARNESS_TEST_REPORT` also supplies it.
Supported adapters are junit and unittest; others remain explicitly unsupported.
Static and legacy smoke exits give outcomes, not test counts. Projects may
review `.harness/smoke-evidence.json` with the same native adapter/argv shape;
verify then requires its native collection and preserves outcomes in a distinct
`smoke.native` artifact. Missing/malformed/zero/failing reports cannot pass.
Selected browser-ui (including Next.js) requires this side file: absence is
unavailable, never a fallback to exit-only browser assurance. Existing non-browser
projects without the side file retain exit-only smoke compatibility; no native
collection is claimed for them. Existing managers survive. Browser consumers
review/add the native side file explicitly; no project config is replaced.

The reference app's smoke script selects one real sign-in/save/reload journey.
Its reviewed smoke-evidence argv deliberately runs the full production journey
suite in verify, a superset of that small smoke. Both use Playwright JUnit,
unique real SQLite fixtures and native teardown, never fabricated collection.
For Next.js, a reviewed root build/test/smoke contract with a native adapter
enables initial framework/browser controls. Verify always runs a required native
production build (lock-selected npm/pnpm/yarn); missing/failed builds cannot pass.
Browser evidence is project-declared scope, not full accessibility/performance
or authorization assurance. Missing contracts/other capabilities remain visible.

Zero tests, absent/oversized/malformed reports, failures, skips, expected
failures, unexpected successes and retries block completeness. Native redacted
artifacts preserve detail. No test exception/retry approval policy is implemented;
security-finding exceptions do not waive native test outcomes.
Executed means runner-accounted cases (including separately recorded skips),
not assertion count.

## Report and identity

Fresh `.harness/reports/verify-*/` directories hold reports and bounded logs.
`schema.json` is versioned JSON Schema. A dependency-free validator implements
only its type/required/properties/additionalProperties/enum/minimum/items/anyOf
keywords; it is not a general schema engine. Counts/exits are typed and unknown
fields/states fail. Required failures/unavailability exit non-zero.
Not-applicable needs a reason. Full completeness requires full scope, stable
inputs and every applicable required control. Undefined root smoke blocks full
root completeness. `--validate-report PATH` checks schema, current identity and
artifact hashes; incomplete reports remain non-zero.

SHA-256 identity covers regular source/context/config/lock files and modes,
including
untracked and analysis-excluded maintained files, executing kit inventory,
selected config and relevant environment/command hashes. Git HEAD is separate.
File contents are not exposed. Dependency/runtime caches and fixed
`.harness/reports`/`.harness/tmp` at any kit depth are excluded. Source must not
live there. Maintained symlinks fail rather than omitting linked source.
Start/end/final snapshots reject edits during execution. Later edits stale old
evidence; report writes never hash themselves.

## Trust limits

- Native config/argv must collect intended tests. Counts do not establish useful
  assertions, critical-case coverage or an honest custom runner.
- Installed tool versions are probed. Transitive/custom binaries and installed
  dependency bytes are not exhaustively authenticated; lockfiles are hashed.
- Logs retain 64 KiB per command; accepted native reports are bounded to 4 MiB.
  Larger reports fail and retained output is truncated. Setup remains explicit.
- Sensitive environment values and common credential/Bearer forms are redacted.
  This is not exhaustive DLP: unusual encoding or free-form secrets may escape.
  Use synthetic scoped data, never production credentials.
- Timeout/SIGINT/SIGTERM cleanup targets owned POSIX groups and descendants.
  Escaped sessions, SIGKILL, OS denial and crashes cannot guarantee cleanup or
  report writing. Ordinary command leftovers are also terminated.
- Provenance is editable, unsigned and not race-proof or a runtime sandbox.
  Step 09 opts in to external macOS direct-egress isolation, not inferred from
  an ordinary pass. See [scope/limits](../security/README.md). Plain native
  test/smoke remain unisolated.
- Advisory captures are setup inputs: their bytes join identity, unlike ordinary
  generated output. Missing/stale/partial native collections cannot satisfy
  security. Verification never refreshes advisory data.
- Invalid config/unsafe identity startup errors fail before a run report.
  Once initialized, required execution/evidence gaps are reported explicitly.
