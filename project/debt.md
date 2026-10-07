# Technical Debt

## Architecture and archive limits

- Architecture meaning remains manually maintained; ID/link checks cannot prove
  it matches runtime. Indexes are derived and checked. Archive rolls back ordinary
  write failures; process crash/concurrent edits require reviewed recovery.
  Add stronger automation only when an actual need warrants it.

## Step 13 acceptance and support limits

- Human acceptance of 44 screenshot candidates is pending; full verify remains
  incomplete, without automatic approval. Review the pinned environment and
  source before adding accepted baselines. Firefox/WebKit and assistive
  technology remain unverified. Lab budgets are measured proposals, not field
  Core Web Vitals. See
  [QH-13](plans/P002-quality-first-harness/evidence/QH-13.md).

## Step 12 operating limits

- Chromium/macOS only; fixed port 3100 requires sequential browser commands.
  Success and SIGINT cleanup pass. Machine crash/SIGKILL/escaped processes
  remain
  outside guaranteed cleanup. Step 13 adds native UI checks, not other-browser
  or accessibility-conformance assurance.
  See [QH-12](plans/P002-quality-first-harness/evidence/QH-12.md); no
  production/SSO assurance is added.

## Step 11 verification follow-up

- Direct production HTTP, real sessions and disposable storage are exercised.
  Step 12's renewed authorization exercises current sign-in/save/permission
  browser rendering. Historical Step 10/11 reports remain partial; new evidence
  closes that execution gap rather than promoting old results.
  SSO/TLS/production auth remain explicitly unsupported. See
  [QH-11](plans/P002-quality-first-harness/evidence/QH-11.md). Full UI quality
  controls remain Step 13.

## Step 10 verification follow-up

- The standalone Next.js foundation has passing production-build, static and
  component evidence on the final kit. Earlier navigation/render evidence is
  retained, but the owner stopped that step's final browser execution. Step 12
  explicitly authorizes current journeys; do not treat old reports as current.
  See [QH-10](plans/P002-quality-first-harness/evidence/QH-10.md).

## Step 09 security follow-up

- Review pytest 8.4.2 advisory `PYSEC-2026-1845` across existing development
  locks; native data suggests 9.0.3. Prove compatibility before a reviewed
  upgrade. No auto-fix/exception is applied here.
- Apple deprecates sandbox-exec. Evidence covers direct process network denial
  on tested macOS arm64, not hostile-code filesystem/IPC isolation. Select/prove
  an independently managed VM/container replacement when needed. Unavailable
  isolation stays blocking, without unrestricted fallback.
- Remote CI/x86_64 security execution is unverified; no remote protection or
  publication changes are authorised in this step.

Track intentional compromises that have a concrete impact. Do not use this as a
general wishlist.

| ID | Debt and evidence | Impact | Trigger to address | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TD-000 | Example; replace or delete | TBD | TBD | TBD | open |
| TD-001 | Native static fixture cases share one large contract file (QH-07) | Cohesion review cost as cases grow; no gate suppression | Further distinct fixture families | Repository owner | monitored |
| TD-002 | Verify coordinator retains one linear orchestration function (QH-08) | Cohesion review prompt, not a size gate; adapters/process/identity are separate | Additional control families | Repository owner | monitored |
