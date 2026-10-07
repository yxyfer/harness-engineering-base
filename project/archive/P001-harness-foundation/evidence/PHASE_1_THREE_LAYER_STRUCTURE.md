# Verification Report: Phase 1 three-layer structure

- **Date:** 2026-09-08
- **Verifier:** Codex
- **Implementation revision:** `24e2c3e`
- **Outcome:** pass

## Acceptance evidence

| Criterion | Method | Result | Evidence |
| --- | --- | --- | --- |
| Root is the starter layout | File inventory and obsolete-path assertions | Pass | Root contains `AGENTS.md`, context directories, `harness`, `.harness/`, and `.agents/` |
| Agent skills are discoverable | Path and frontmatter inspection | Pass | Five skills are under `.agents/skills/<name>/SKILL.md` |
| Managed machinery is hidden | File inventory | Pass | Commands, checks, and fixtures are under `.harness/` |
| Public dispatcher works | Help and command invocation | Pass | `./harness help` plus inspect, check, test, and smoke commands |
| Node behaviour is preserved | Policy check, package check, Node test, HTTP smoke | Pass | One Node test and golden-path response passed |
| Python behaviour is preserved | Policy check, syntax parse, unittest, HTTP smoke | Pass | One unittest and golden-path response passed |
| Nested invocation works | Invoke root dispatcher from the Node fixture | Pass | Inspect, check, and test resolved the fixture and checks correctly |
| Paths containing spaces work | Copy complete layout to a temporary spaced path | Pass | Both fixtures passed inspect, check, and test |
| Documentation remains valid | Repository documentation check | Pass | 27 Markdown files checked; no broken links |
| Obsolete layout is removed | Explicit absence assertions | Pass | `template/`, `skills/`, `checks/`, and `examples/` are absent |

## Baseline before migration

The former commands passed before files moved:

```text
./template/harness/inspect examples/nextjs-project
./template/harness/check examples/nextjs-project
./template/harness/test examples/nextjs-project
./template/harness/smoke examples/nextjs-project
./template/harness/inspect examples/python-project
./template/harness/check examples/python-project
./template/harness/test examples/python-project
./template/harness/smoke examples/python-project
./template/harness/check template
```

## Commands run after migration

```text
./harness help
./harness inspect .harness/tests/fixtures/nextjs-project
./harness check .harness/tests/fixtures/nextjs-project
./harness test .harness/tests/fixtures/nextjs-project
./harness smoke .harness/tests/fixtures/nextjs-project
./harness inspect .harness/tests/fixtures/python-project
./harness check .harness/tests/fixtures/python-project
./harness test .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/python-project
./harness check .
sh -n harness .harness/bin/common.sh .harness/bin/setup \
  .harness/bin/start .harness/bin/inspect .harness/bin/check \
  .harness/bin/test .harness/bin/smoke
.harness/checks/documentation/check .
git diff --check
```

The copied-path run repeated inspect, check, and test against both fixtures from
a temporary directory whose path contained spaces.

## Environment

- macOS 26.6.1
- Node.js v24.10.0
- Python 3.14.0
- Node and Python fixtures are local examples with no external integrations.
- Smoke checks used temporary loopback HTTP servers and real HTTP responses.

## Limitations and follow-up

- `./harness setup` was not run because it intentionally creates environments
  and installs dependencies. Existing dependency-free check, test, and smoke
  paths did not require it.
- `./harness start` was not left running as a separate manual check; both
  fixture
  server entry points were exercised by their process-level smoke checks.
- Loopback smoke checks required expanded sandbox permission to bind localhost.
- Project context templates correctly still report `needs-project-input`; the
  semantic readiness workflow belongs to Phase 4.
- Version, configuration, manifest, installer, adoption, update, standards, and
  CI behaviour remain later phases and were not implied by this result.
