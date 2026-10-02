# Security Context

Status: current; Step 09 controls implemented, not security certification

The [security contract](../.harness/security/README.md) defines executable scope,
setup, severity policy, provenance and compatibility. Root security scanning is
explicitly opted in through project-owned `.harness/security.json`.

## Trust boundaries

This repository is an editable engineering kit, not an application with users,
sessions or production services. Reviewed commands, adapters, plugins and tests
execute repository code. Config, reports and checksums are unsigned: independent
review/CI enforcement must protect them. The harness is not its own sandbox.

Step 10 adds a separately owned synthetic reference UI, not real users/sessions.
No authentication, authorization or persisted mutation exists. Its no-access
card is a labelled display example, never a permission control. Its own reviewed
npm lock/security config selects the existing offline baseline. The app uses
maintained ESLint 10 with compatible native Next/hooks plugins instead of the
Next bundled React/import/a11y plugins that require unsupported ESLint 9.

Opted-in verify wraps static checks/tests/self-tests/smoke and scanners in
external macOS
Seatbelt. It asserts actual permission-denied direct/child sockets, synthetic
production/provider HTTP paths on TEST-NET-2, and working trusted loopback.
No real provider or production host is contacted. Missing/denied sandbox launch
fails closed. Native developer test/smoke commands alone are **not isolated**.

Apple deprecates sandbox-exec. This establishes direct process-network denial,
not hardened hostile-code VM/filesystem isolation. The allow-default profile
does not prevent every filesystem/IPC/delegation escape. Loopback services must
be synthetic and trusted, never egress proxies. Use an independently controlled
disposable host/VM for adversarial code; never expose host/production credentials.
See [Apple's discussion](https://developer.apple.com/forums/thread/661939).

## Sensitive assets

| Asset | Classification | Protection/evidence |
| --- | --- | --- |
| Code, locks, context | Project code | Ownership/review; exact checksums; input identity |
| Production/provider credentials | Prohibited test input | Fixed environment allowlist; synthetic HOME/token; never supply secrets |
| Findings/logs | Local diagnostics | Values/snippets withheld; bounded redaction; ignored local reports |
| Advisory captures | Public package/dependency data | Explicit source/time/version/lock identity; 24h freshness |

Local artifact access/retention is the repository owner's responsibility. No
cloud export or application database is introduced. Log redaction is heuristic,
not complete DLP; unusual encodings/free-form secrets can escape. Process cleanup
does not guarantee escaped sessions, hard kills or machine crash recovery.

## Threats and controls

- Pinned Gitleaks 8.30.1 scans maintained workspace/untracked/config inputs with
  built-in rules, no project allow-comments/ignore files. No history/archive or
  complete secret-detection guarantee.
- Native npm 11.6.0 audit and pip-audit 2.10.1 capture locked dependencies during
  explicit setup. Offline verification rejects missing/stale/malformed/partial
  data and changed locks; PyPI severity is unknown and therefore blocking.
- Existing local Ruff S307/S602/S608 and ESLint no-eval/no-new-func protect a
  few source patterns, not general authorization/injection/runtime safety.
- External OS policy, clean allowlisted environment and real permission-denial
  assertions restrict direct test egress. URL/text rules are not a sandbox.
- Step 08 native outcomes/input hashes/redacted logs retain provenance. Advisory
  bytes now join identity; generated verification reports do not hash themselves.

Critical/high/unknown findings block; moderate/low/info remain visible. Exact
source/dependency exceptions require owner, reason and timezone-aware expiry
within 90 days. Expired entries block policy. Secret findings cannot be excepted:
remove live values or generate synthetic fixtures at runtime. Exceptions never
suppress scanner failures or unavailable data. No automatic fixes/blanket ignores.

Explicit tool/advisory setup is network-enabled registry/release access, not
application testing. It uses no inherited auth/credentials or target lifecycle
scripts. Verification cannot refresh data. CI preserves pinned macOS runtimes,
SHA-pinned actions, read-only permissions and checkout without persisted auth.
No repository/production secrets are referenced. Test phases use the same
external policy and clean synthetic environment. Remote execution is unverified.

## Human approval gates

Review dependency upgrades, exact exceptions, scanner/rule pins, network policy
and trust/capability changes. Publication, production access, destructive changes
and security trade-offs require owner approval. No remote protections are changed.

## Incident and disclosure path

The repository owner triages findings before release. A live secret requires
stopping publication/verification, revocation at the issuer, access/history review
and reviewed artifact recovery. A scanner cannot prove revocation. Dependencies
require exposure/compatibility review, never automatic exception or upgrade.

Live setup found pytest advisory `PYSEC-2026-1845`, aliases `GHSA-6w46-j5rx-g56g`
and `CVE-2025-71176`, in existing 8.4.2 development locks. Native advisory data
suggests 9.0.3. This step retains the blocking finding for review without changing
existing dependencies. See [QH-09](../verification/QH-09.md).
