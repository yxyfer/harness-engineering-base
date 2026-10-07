# P004-T001 verification

- **Date:** 2026-10-07
- **Revision:** working tree over `2b36b3cbec259c70fc6b4330c46a6322cfff2457`;
  prior conversation changes preserved in migration inputs.
- **Outcome:** pass; complete bundle archived and closure checked

## Acceptance evidence

| Criterion | Evidence |
| --- | --- |
| One project folder, stable names | 4 bundles; 24 tasks; old/new crosswalk in project/migration.md |
| Concise current progress | Derived 13-line overview; P002 12/19, T013 blocked, T014 ready |
| Fixed format and agent workflow | FORMAT/templates; AGENTS and implementation/review/context skills |
| Meaningful enforcement | 11 new cases: parent/duplicate IDs, dependencies/cycles, completion/evidence, symlinks, stale indexes, archive/link repair, rollback, CLI/policy integration, legacy compatibility |
| Source/artefact preservation | 64 machine artifacts/archive files retain exact original bytes; source/hash mapping in migration.json |
| Navigation | 163 new navigation/source/evidence links/fragments valid before closure; documentation gate checks all maintained links |
| Architecture | Current diagram plus system/feature tables; real local auth/storage, no AI provider calls, deployment/support limits visible |

## Checks

| Final check | Result |
| --- | --- |
| Native format/lint/types/documentation | pass |
| Scoped project contracts | 11 passed |
| Root application test command | 165 passed; 157.237 seconds |
| Harness self-test | 165 passed; 156.355 seconds |
| Python fixture smoke | pass |
| Next.js fixture smoke | pass |

Initial scoped tests failed on missing new modules. Earlier suites passed 164
cases. The late managed-link guard exposed macOS temporary-path aliases in its
fixture; normalising roots resolved that failure, and the final 165-case suites
passed.
Native formatting attempts exposed moved-link line width and rebase issues;
those were corrected without suppressions or weakened gates. All attempts are
retained in logs. Tests run conventional programs with synthetic local services;
no model provider or AI grader executes verification.

```sh
export PATH="$PWD/.harness/tmp/qh05-bin:$PWD/.harness/ci/node_modules/.bin:$PWD/.venv/bin:$PATH"
./harness project sync
./harness project check
./harness check
./harness test
./harness self-test
./harness smoke .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/nextjs-project
python3 .harness/bin/manifest.py verify .
git diff --check
```

`./harness project archive P004` closes the verified bundle; the final
result and link/source checks are recorded below. Full suites and fixture
smokes run outside the execution sandbox for their existing synthetic loopback
and external macOS isolation probes. Direct native commands do not themselves
establish full isolated verify or production safety.

## Provenance and recovery

Migration inputs preserve the initial dirty tree's project records. Historical
Markdown was moved and links rebased; machine artifacts and captured hashes
retain their historical scope/bytes. Migration scripts and mapping are retained;
path/link cleanup afterwards is part of the reviewed diff. Application runtime source/config,
security policy and dependencies were not changed. Archived evidence scripts may
retain original path assumptions; their old inputs are preserved in the archive.

The release inventory adds exactly three stdlib helpers and one contract test.
Six existing managed hashes change: dispatcher, documentation check, inventory,
and three skills. The candidate retained version/schema/timestamp and all prior
managed paths; no consumer checksum conflict was accepted. Final identity is
recorded in the source snapshot after archival.

Archive validates all tasks, acceptance/evidence and dependencies before moving.
It repairs incoming/internal links and regenerates indexes. A managed-file link
requiring an update blocks archival before mutation. Ordinary write-error
rollback is tested; process-crash atomicity and concurrent edits are not claimed.
Restore through a reviewed bundle move/link update and sync, or recover from the
saved migration inputs. Do not reset unrelated application data.

## Limits

Source diagrams/tables were inspected; no rendered visual acceptance, production
identity/deployment, remote CI/protection, full security re-certification or
semantic architecture guarantee is claimed. Existing Step 13 human acceptance
and retained security findings remain open. Steps 14–19 were not implemented.
The adoption marker preserves legacy projects, including unrelated symlinked
project source directories. Only adopted record format/index consistency is
newly enforced. No new application UI requires browser QA.

## Closure

The final archive command passed on P004. Project validation, native checks,
release identity (114 managed files) and diff whitespace checks passed.
All 64 migrated machine artifacts retained original bytes after archival.
Completed tasks stay in their plan; P002 remains active with human acceptance
explicitly blocked. Source identity and command logs accompany this report.
