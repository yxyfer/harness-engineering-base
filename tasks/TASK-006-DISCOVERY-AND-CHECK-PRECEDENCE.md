# TASK-006: Consistent discovery and static-check precedence

- **Status:** active
- **Owner:** repository owner
- **Related plan:** [Step 03](../plans/active/QUALITY_FIRST_HARNESS.md)

## Outcome

Harness-owned scans inspect maintained files within the target, route supported
executable shebangs to their language, and honour directory exclusions. Required
policy gates precede one resolved project static-check implementation.

## Context to read

- `AGENTS.md`, canonical context and ADR-001 through ADR-004.
- F3–F5 in `verification/AUDIT_2026_10_01.md`.
- Dispatcher, check command, managed checks, standards and existing tests.

## Constraints and non-goals

- Preserve Step 01/02 work and other existing files.
- Native tools retain their own configuration and scope.
- Skip file and directory symlinks in harness-owned scans, including internal
  links; canonical policy documents cannot be supplied through symlinks.
- Exclusions match directories: a bare name at any depth, or a slash-containing
  root-relative prefix. They are literal paths, not globs.
- No ownership-engine repair, dependency installation flow, new CI, readiness
  enforcement, application features or future verification command.

## Acceptance criteria

- [ ] F3–F5 reproduce before the fix and pass behavioural regressions afterwards.
- [ ] Direct/env/env `-S` Python shebangs receive Python analysis; supported shell
  shebangs reach shell tools with spaced paths intact. Unknown executables do
  not default to shell.
- [ ] All harness-owned tree scans use configured exclusions, prune before
  descent, retain similarly named siblings and stay inside the root.
- [ ] Extensionless Python participates in degraded syntax validation.
- [ ] CLI/environment/config precedence is preserved; selected commands run
  exactly once with no hidden Python stage. Package checks behave likewise.
- [ ] A mandatory policy failure blocks project commands; native tool scope is
  unaffected by harness analysis exclusions.
- [ ] Both suites and applicable fixture/native checks run; missing tools and
  failed attempts remain explicit in QH-03.
- [ ] Only intended managed inputs enter the inventory; durable context and the
  active plan link this step's evidence.

## Verification

| Check | Method | Expected evidence |
| --- | --- | --- |
| Defects | Before probe and red/green regressions | Named F3–F5 failures then pass |
| Commands | Installed disposable targets and counters | Single invocation and policy-first failure |
| Scope | Synthetic exclusions and symlinks | No excluded/outside reads |
| Release | Check, test, self-test and fixture matrix | Recorded exits and coverage gaps |

## Notes and decisions

Fixtures and tool-call recorders are synthetic. Real native tool execution is
recorded separately; tool recorders prove routing, not tool correctness.
