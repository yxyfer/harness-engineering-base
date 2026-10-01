# Verification Report: TASK-003

- **Date:** 2026-09-08
- **Verifier:** Codex
- **Revision:** Phase 3 working tree
- **Outcome:** pass

## Acceptance evidence

| Criterion | Method | Result | Evidence |
| --- | --- | --- | --- |
| Shared and language-specific rules are explicit | Document inventory contract test | Pass | Four shared documents and four language profiles detected |
| Profiles are selected proportionately | Phase 3 contract tests | Pass | Auto and explicit selection, plus exclusions, covered |
| Numeric defaults remain consistent | Config and fixture contract test | Pass | Harness, Ruff, and Prettier use 80; size thresholds are 350/50 |
| Established tools are authoritative | Node fixture static gate | Pass | Prettier, ESLint, and strict TypeScript all exited 0 |
| Size checks are advisory and actionable | Generated oversized function test | Pass | Warning names threshold and scoped-rationale route |
| Existing harness behaviour remains healthy | Full contract suite | Pass | 14 tests passed |
| Both fixture golden paths remain healthy | Localhost smoke tests | Pass | Node and Python smoke scripts reported `smoke: pass` |

## Commands run

```text
python3 -m unittest discover -s .harness/tests -p 'test_phase3_standards.py' -v
npm install --ignore-scripts
npm run check
./harness inspect .
./harness check .
./harness test .
./harness check .harness/tests/fixtures/nextjs-project
./harness test .harness/tests/fixtures/nextjs-project
./harness smoke .harness/tests/fixtures/nextjs-project
./harness check .harness/tests/fixtures/python-project
./harness test .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/python-project
```

The first sandboxed smoke attempts failed because local port binding returned
`EPERM`. Both were repeated with approved local execution and passed.

## Environment

- macOS, zsh host; harness scripts remain POSIX `sh`.
- Python 3.14.0 and Node.js 24.10.0 were used for verification.
- The Node fixture uses a committed lockfile. `npm install --ignore-scripts`
  installed 103 development packages and reported zero audited vulnerabilities.
- Ruff, Pyright, ShellCheck, shfmt, and markdownlint-cli2 were not installed on
  the host; the harness reported those checks as degraded rather than claiming
  they ran.

## Limitations and follow-up

- Phase 4 must make optional tool readiness installable and visible through
  setup/doctor commands.
- Function-size analysis is AST-aware for Python only. Other languages rely on
  project linters to avoid fragile generic parsing.
- The Phase 2 configuration validator is above the advisory function-size
  threshold; the scoped rationale is recorded in TASK-003.
- Time-bound central exceptions remain Phase 6 work.
