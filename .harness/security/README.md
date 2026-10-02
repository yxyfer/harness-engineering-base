# Offline security and external test isolation

Verify adds required security when mode is local/ci and schema 2 is selected,
or schema 1 explicitly opts in with project-owned `.harness/security.json`.
Legacy schema 1 without that side file reads unchanged and warns no assurance;
off never claims scanning/isolation. Capability controls remain independent.
Check remains static/policy checks, not a substitute for security verification.

## Explicit setup

Use the pinned Python 3.14.0 and npm 11.6.0 environments on macOS:

```sh
sh .harness/security/setup-tools.sh .harness/tmp/security-bin
python3 -m venv .harness/tmp/security-env
.harness/tmp/security-env/bin/python -m pip install --require-hashes \
  --only-binary=:all: -r .harness/security/requirements.lock
python3 .harness/bin/security_advisories.py setup .
./harness verify --self-test
```

Setup has explicit dependency/advisory network access. pip-audit uses
disable-pip/no-deps: it queries exact versions without installing the target.
npm audit uses package-lock-only/ignore-scripts, fixed public registry and no
user auth. Setup exit 1 means captured findings, exit 2 error/unavailable; neither
is a security pass. Offline verification never invokes setup or registries.
CI preserves required findings at its separate offline gate, not a blanket ignore.

Gitleaks 8.30.1 assets use official SHA-256 digests for macOS arm64/x64. Scanner
requirements include Python 3.14/macOS wheel hashes for both architectures;
arm64 was exercised, x64/remote CI were not. Existing local Ruff/ESLint and
native parser configs remain authoritative and lock-pinned; rule IDs are fixed.

## Reviewed project policy

The side file is project-owned; never automatically replace an existing policy:

```json
{
  "schema_version": 1,
  "dependency_scope": "All reviewed application and development locks",
  "locks": [{ "path": "package-lock.json", "ecosystem": "npm" }],
  "exceptions": []
}
```

Supported: npm v3 package-lock with adjacent package.json; flat Python exact
name==version requirements locks with comments/hashes. Includes, URLs, ranges,
editable requirements and other formats/managers are unavailable, not migrated.
Root package/Python metadata cannot omit locked coverage. Multiple package roots
remain unsupported by the shared resolver: run roots independently. Empty locks
need a reviewed stdlib/no-dependency scope. Paths reject traversal, duplicates
and symlink components. This is a fixed contract, not a generic policy DSL.

Findings retain control/ID/path/component or affected range/line/severity and a
SHA-256 fingerprint of those fields, never native secrets/source snippets.
Exact source/dependency exceptions require fingerprint, owner, reason and expires
(timezone-aware ISO date, future and within 90 days). Expired/duplicate/wildcard
entries fail; secret findings cannot be excepted. Critical/high/unknown block,
moderate/low/info remain visible. Existing native lint violations also block.
No automatic fixes, baselines, blanket ignores or error/data exceptions.

## Scope and evidence

Gitleaks scans conservative maintained workspace identity including untracked
and config files, excluding fixed runtime/caches/reports. Force built-in rules
and ignore project allow-comments/ignore files. Git history/archives are not
covered. Source scans include maintained consumer Python/JS/TS, not shipped kit;
the authoring root explicitly scans engine/CI/tests as Python. Nested fixtures
and defaults are checked separately. Arbitrary analysis exclusions cannot hide
source, and missing tools never make a control unnecessary.

Native package collection must match supported locks. Advisory source/time,
tool version/native exit, lock/manifest digest and capture hash are retained.
Data older than 24h, future-dated, changed locks, missing/partial/malformed data
or native errors are unavailable, not clean. Findings fail; errors/unavailability
carry distinct reasons. Partial verify never becomes complete. Capture bytes
join input identity, but ordinary output does not hash itself. Native scanner
logs/snippets are withheld; existing output limits/process cleanup apply.

These are editable unsigned artifacts, not authenticated advisory attestations.
Native counts/rules do not certify test adequacy or general application security.

## External runtime boundary

External Seatbelt denies direct non-loopback sockets, permitting only trusted
synthetic loopback services. Preflight requires EPERM/EACCES, not timeout or DNS
failure; it tests a child and real HTTP production/provider-shaped paths on
TEST-NET-2, never real providers. Inherited credentials/URLs/startup hooks are
not forwarded. No URL-filter-as-sandbox claim.

Opted-in verify isolates static checks/tests/self-tests/smoke and scanners. CI
isolates all static/contract/fixture/negative phases. No inherited executable
HARNESS overrides/startup hooks are forwarded; use reviewed native project
configuration/adapters for the intended suite.

Apple deprecates sandbox-exec. Missing/denied launch fails closed. This is direct
process network restriction, not hostile-code filesystem/VM isolation: local
proxies, IPC delegation and readable host credentials remain risks. Use an
independently controlled disposable host/VM for adversarial code. Native
developer test/smoke alone are unisolated; opted-in verify and CI wrappers
establish only the stated boundary. Remote CI execution remains unverified.

## Primary provenance

- [Gitleaks 8.30.1](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1)
  and [CLI](https://github.com/gitleaks/gitleaks/blob/v8.30.1/README.md).
- [pip-audit 2.10.1](https://github.com/pypa/pip-audit/releases/tag/v2.10.1):
  Python Packaging Advisory Database via PyPI JSON.
- [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit):
  native registry advisory endpoint and severities.
- [Ruff S307](https://docs.astral.sh/ruff/rules/suspicious-eval-usage/), S602/S608;
  [ESLint no-eval](https://eslint.org/docs/latest/rules/no-eval), no-new-func.
- [Apple sandbox-exec deprecation](https://developer.apple.com/forums/thread/661939).
