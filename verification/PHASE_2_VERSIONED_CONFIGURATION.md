# Verification Report: Phase 2 versioned configuration contract

- **Date:** 2026-09-08
- **Verifier:** Codex
- **Revision:** `12f9882` plus the Phase 2 working-tree changes
- **Outcome:** pass

## Acceptance evidence

| Criterion | Method | Result | Evidence |
| --- | --- | --- | --- |
| Offline version identity | Read version and run inspect | Pass | Harness `0.1.0`; config and manifest schema `1` |
| Strict TOML schema | Valid and invalid configuration fixtures | Pass | Unknown, missing, invalid-range, invalid-enum, and path rules return config errors |
| Actionable configuration errors | Public and unit tests | Pass | Exit `4` includes configuration file, key, and expected value |
| Deterministic precedence | Config, environment, and CLI commands write a source marker | Pass | CLI overrides environment; environment overrides TOML; automatic detection remains fallback |
| Redacted inspection | Inspect root and both fixtures | Pass | Effective values and command sources shown; command bodies not printed |
| Versioned managed files | Generate and verify manifest | Pass | Schema `1`, 39 relative managed paths, SHA-256 checksums |
| Integrity failure | Modify a temporary managed file | Pass | Verification exits `5` with checksum mismatch |
| Stable public exits | Usage, project failure, invalid config, broken install fixtures | Pass | Exit meanings `1`, `2`, `4`, and `5` verified |
| Existing projects still work | Node and Python check/test/smoke suites | Pass | Both fixture golden paths preserved |
| Path portability | Copy managed layout to a path containing spaces | Pass | Manifest, inspect, and CLI command override succeeded |
| Documentation | Policy and link checks | Pass | Configuration, ownership, precedence, secrets, and exits documented |

## Commands run

```text
./harness help
./harness inspect .
./harness check .
./harness test .
./harness inspect .harness/tests/fixtures/nextjs-project
./harness check .harness/tests/fixtures/nextjs-project
./harness test .harness/tests/fixtures/nextjs-project
./harness smoke .harness/tests/fixtures/nextjs-project
./harness inspect .harness/tests/fixtures/python-project
./harness check .harness/tests/fixtures/python-project
./harness test .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/python-project
python3 .harness/bin/config.py validate .harness/config.toml
python3 .harness/bin/manifest.py verify .
sh -n harness .harness/bin/common.sh .harness/bin/setup \
  .harness/bin/start .harness/bin/inspect .harness/bin/check \
  .harness/bin/test .harness/bin/smoke
python3 -m py_compile .harness/bin/config.py \
  .harness/bin/manifest.py .harness/tests/test_phase2_contract.py
```

Eight harness contract tests passed. The copied-path test also selected a CLI
command override and verified its output in the target project.

## Environment

- macOS 26.6.1
- POSIX `sh`
- Node.js v24.10.0
- Python 3.14.0 using standard-library `tomllib`
- Fixture integrations are local and dependency-free.
- Smoke checks used real responses from temporary loopback HTTP servers.

## Limitations and follow-up

- Language-profile command defaults are reserved in the precedence contract but
  are not populated until Phase 3 defines those profiles.
- Exit `3` is reserved for incomplete readiness and will be implemented in Phase
  4.
- The manifest can generate and verify checksums; installer and upgrade use of
  that data remains Phase 5 and Phase 9 scope.
- `./harness setup` was not run because it intentionally creates environments
  and installs dependencies.
- `./harness start` was not left running separately; both entry points were
  exercised through process-level HTTP smoke tests.
- Loopback smoke checks required expanded sandbox permission.
- Starter context documents still report `needs-project-input` by design.
