# Technical Debt

## Step 10 verification follow-up

- The standalone Next.js foundation has passing production-build, static and
  component evidence on the final kit. Earlier navigation/render evidence is
  retained, but the owner stopped final browser execution. Resume only with
  owner authorization; do not treat the earlier full report as current or begin
  Step 11 here. See [QH-10](../verification/QH-10.md).

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
