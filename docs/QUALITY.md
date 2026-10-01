# Quality Context

Status: current

## Quality bar

Harness commands must resolve deterministically, preserve project ownership,
fail with actionable messages, and report only evidence they actually ran. The
engineering baseline must remain concise, language-idiomatic, and executable
through project-owned tools.

## Verification matrix

| Risk or behaviour | Verification | Command or evidence | Required gate |
| --- | --- | --- | --- |
| Core logic | Automated test | `./harness test` | Yes |
| Harness contract | Independent automated suite | `./harness self-test` | For harness changes |
| Project conventions | Static checks | `./harness check` | Yes |
| Golden path | Smoke test | `./harness smoke` | Yes |
| Critical interface states | Visual and interaction QA | Project-specific | When applicable |

## Test strategy

Contract tests cover configuration, manifests, profile selection, exclusions,
and exit behaviour. Both fixture projects exercise static checks, automated
tests, and smoke paths. Changes to command behaviour require regression coverage;
documentation-only changes require link and consistency checks.

Step 02 regressions use disposable installed copies, real no-pip environments,
and real pytest collection. They cover failing/healthy app tests, mixed suites,
missing local runners, declared unittest, zero collection and independent
self-tests. Required pytest cases fail visibly if setup is missing; they do not
download dependencies or skip. [QH-02](../verification/QH-02.md) records evidence.

Step 03 regressions exercise installed disposable targets, supported shebangs,
pruned nested exclusions, spaced paths, symlink boundaries, policy failures and
single project command resolution. Tool-call recorders prove argv/scope routing;
they do not establish native tool correctness. Real installed native tools and
missing coverage are reported separately in [QH-03](../verification/QH-03.md).

## Core CI

Step 05 adds a pinned macOS GitHub Actions workflow and
[locked native CI setup](../.harness/ci/README.md). Its static phase requires
ShellCheck, shfmt, Markdownlint, Ruff and Pyright; the existing Node fixture runs
Prettier, ESLint and TypeScript. Both contract commands, fixture tests/smokes
and disposable negative controls run without model-based grading. Unique logs
retain failed attempts. [QH-05](../verification/QH-05.md) distinguishes local
evidence from unverified remote execution; no branch protection is configured.

## Known limitations

- Optional developer tools are not installed by the harness yet. Missing tools
  are reported as degraded coverage until Phase 4 adds setup and doctor flows.
- Generic function-size analysis is Python-aware only. Other profiles rely on
  their project linters rather than fragile harness parsing.

## Release criteria

A phase is complete only when `./harness check`, `./harness test`, and relevant
fixture smoke paths pass and a verification report records exact evidence and
limitations.

Harness changes also require `./harness self-test`. Native overrides/scripts
retain their own collection contract; general required-case/skip/evidence
enforcement remains proposed for Step 08. Optional static tools can still be
unavailable despite a zero command exit. Steps 02–03 repair F1–F5; managed-file
ownership findings F6–F7 are repaired in Step 04.

Step 04 uses full disposable installations, a real no-pip environment and
synthetic project additions to prove health remains intact. Shipped edits/loss,
unsafe paths, JSON duplicates, inventory drift and symlink destinations fail.
Deterministic release generation includes exactly reviewed inputs and leaves
consumer files/metadata untouched. [QH-04](../verification/QH-04.md) records
before/after evidence and native coverage limits.

## Target quality policy agreed on 2026-10-01

The following is the intended policy from the [product vision](PRODUCT.md).
Current enforcement remains limited to the implementation described above and
the [audit findings](../verification/AUDIT_2026_10_01.md).

- Automated test execution and grading are entirely programmatic. No secondary
  AI calls, LLM reviewers, or model-based screenshot judgments are permitted in
  the verification pipeline.
- Application tests and harness self-tests are separate suites. Missing declared
  runners, uncollected required cases, missing evidence, or unknown scope must
  not produce a fully verified result.
- Test meaningful outcomes and negative cases at the actual boundary. Use
  disposable persistence for storage claims and direct server requests for
  authorization claims. Identify mocked external integrations explicitly.
- Use browser interaction assertions, automated accessibility rules, and pixel
  comparisons against deliberately approved baselines for measurable UI quality.
  Human product/design judgment is not represented as an automated pass.
- Coverage, mutation results, duplication, and source size are supporting
  evidence. No single percentage or composite score establishes quality.
- Gates select relevant language/framework/capability controls and explain their
  scope. Local partial runs are explicit; required CI suites remain complete.
- Record failed retries and reviewable exceptions. Do not silently disable a
  test, lower a threshold, update a baseline, or change the runner to pass.
- Bind reports to source, configuration, lockfiles, tools, and evidence. A later
  edit invalidates an earlier completion claim for affected behaviour.

The initial implementation milestone fixes the audit's false-success paths and
adds CI before expanding installation/update functionality.
