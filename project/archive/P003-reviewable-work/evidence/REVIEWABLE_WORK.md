# Verification report: TASK-017

- **Date:** 2026-10-07
- **Verifier:** Codex; programmatic checks, no additional AI reviewers
- **Revision:** working-tree documentation/workflow change over
  `2b36b3cbec259c70fc6b4330c46a6322cfff2457`; initially clean tree
- **Outcome:** pass for this bounded documentation/workflow change
- **Task:** [TASK-017](../tasks/P003-T001-reviewable-work.md)
- **Plan:** [Completed plan](../README.md)
- **Logs:** [All attempts](reviewable-work-logs.tar.gz)
- **Inputs:** [Source hashes](reviewable-work-source.json) records changed file
  hashes; generated
  report/log/snapshot outputs are excluded from that snapshot.

## Acceptance evidence

| Criterion | Method | Result |
| --- | --- | --- |
| Concise roadmap | Compare original at base revision with current source | 1,042 to 73 lines; one table and next action |
| Instructions preserved | Python assertions compare each extracted outcome, acceptance section and prompt body to original | All 19 retained; only routing/shared-context references changed |
| Findable tasks/history | Assert every task filename is in index; inspect moves/links | All 17 indexed; old roadmap outside active; original historical reports retained |
| Reviewer architecture | Inspect existing context, entry points and server/domain/storage source; trace map links | Harness and app maps identify current boundaries, choices, failure/recovery and limits |
| Concise future workflow | Inspect templates, AGENTS and both changed skills | Plans coordinate; tasks hold reviewer briefs; maps/ADRs hold durable facts; reports hold results |
| Links | Python target/heading-fragment assertions over plans/tasks/docs/maps | 312 local targets/fragments valid before closure; [final link audit](reviewable-work-link-audit.txt) |
| Native checks | Public check with installed tools on PATH | Exit 0; policy, ShellCheck/shfmt, Markdownlint, Ruff and Pyright pass |
| Contract suite | Public test and independent self-test | Each exit 0, 154 cases, no skips |
| Relevant smoke | Python and Node fixture smoke | Both exit 0 after recorded sandbox retries |
| Release integrity | Verify inventory/checksums and compare candidate | 110 managed paths unchanged; only the two intended skill hashes change |

No new runtime behaviour or regression-test source was introduced. The existing
contract suite is the required harness check; documentation-specific assertions
verify extraction, indexing and link mechanics rather than mirroring runtime.
The original step input is reproducible from the base revision's
`project/plans/P002-quality-first-harness/README.md`. Shared execution rules,
checkpoints,
constraints, critical scenarios, risks and final acceptance are retained in
`project/plans/P002-quality-first-harness/evidence/instructions/execution.md`.

## Commands and attempts

Installed local tools were already present; no downloads or tool upgrades ran.
Native checks use this environment prefix (repository-relative locations):

```sh
export PATH="$PWD/.harness/tmp/qh05-bin:$PWD/.harness/ci/node_modules/.bin:$PWD/.venv/bin:$PATH"
./harness check
./harness test
./harness self-test
./harness smoke .harness/tests/fixtures/python-project
./harness smoke .harness/tests/fixtures/nextjs-project
python3 .harness/bin/manifest.py verify .
git diff --check
```

| Attempt | Exit | Observation |
| --- | --- | --- |
| Initial check | 1 | Installed ShellCheck, shfmt and Markdownlint absent from shell PATH |
| Check with tools | 1 | App's native aligned-table rule and one moved-link line width exposed formatting errors; corrected |
| Corrected native check | 0 | All native/policy controls pass; pre-existing advisory cohesion warnings retained |
| Initial test / self-test | 1 / 1 | Each collected 154; 5 failures and 3 errors from missing tool PATH, loopback denial and sandbox-exec denial |
| Test with tools, outside execution sandbox | 0 | 154 pass; 137.436 seconds |
| Self-test with tools, outside execution sandbox | 0 | 154 pass; 135.668 seconds |
| Initial Python / Node smoke | 1 / 1 | Loopback bind denied by execution sandbox |
| Python / Node smoke outside execution sandbox | 0 / 0 | Synthetic local fixture golden paths pass |
| Manifest / whitespace check | 0 / 0 | Exact inventory valid; no whitespace errors |

First attempts remain in the archive. Successful retries do not erase failures.
The retries enable actual local synthetic tests and external macOS isolation
probes; they do not invoke production services or model providers. Plain
smoke/test commands are not themselves equivalent to full isolated verify.

Release authoring began from a valid manifest. A generated candidate retained
version, schema, timestamp and the exact 110-path inventory. An assertion
allowed
hash differences only for `code-review/SKILL.md` and
`implement-feature/SKILL.md`; those reviewed candidate bytes replaced metadata.
No consumer conflict or ownership change was accepted through regeneration.

## Environment and limits

macOS; Python 3.14.0; Node 24.10.0; existing locked local native tools. Data in
contract/fixture tests is synthetic; local runtimes and conventional programs
execute/grade evidence. No dependency, runtime, permission or release-policy
change was made.

This change adds repository documentation and workflow guidance. It does not
establish human understanding, productivity gains, semantic architecture
accuracy by automation, or production readiness. Mermaid diagrams were inspected
as source; no rendered diagram/browser acceptance is claimed. No new application
UI needs browser QA. Maps/indexes remain manually maintained with
implementation.

Root smoke remains undefined; the two fixture smokes are the relevant bounded
paths. Full verify/security, remote CI and pending Step 13 screenshot acceptance
were not re-certified. Existing dependency findings and human approvals remain
visible. Steps 14–19 were not executed.

Final closure check: native `./harness check` exits 0 after task/plan closure.
