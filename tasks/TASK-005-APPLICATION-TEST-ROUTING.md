# TASK-005: Independent application tests and harness self-tests

- **Status:** complete
- **Owner:** repository owner; execution by Codex
- **Related plan:** [Step 02](../plans/active/QUALITY_FIRST_HARNESS.md)
- **Prerequisite:** [QH-01](../verification/QH-01.md)
- **Evidence:** [QH-02](../verification/QH-02.md)

## Outcome

Application failures cannot be hidden by shipped harness tests or a silently
substituted runner. Both suites have independent commands and honest exits.

## Context to read

- `AGENTS.md`, canonical context and accepted decisions.
- The plan execution contract, Step 02 and F1/F2 audit evidence.
- Dispatcher, configuration/command resolution, tests and fixtures.
- Base standards; shell, Python and Markdown profiles.

## Constraints and non-goals

- Preserve existing work and Step 01 evidence.
- Keep schema 1 and CLI/environment/config command precedence.
- Add `self-test`, not future `doctor`, `format` or `verify` commands.
- Do not repair F3-F7, source discovery, static-check scope or ownership policy.
- Synthetic disposable installations only; explicit setup downloads followed by
  offline test execution. No providers or production access.

## Acceptance criteria

- [x] F1/F2 are reproduced before runtime edits and new regressions fail.
- [x] Installed harness plus failing app case fails; healthy app case collects.
- [x] Missing declared pytest fails with setup guidance; no unittest fallback.
- [x] Declared unittest and pytest use the target `.venv` when available.
- [x] Supported Python runners reject zero collected cases.
- [x] CLI > environment > config > package script > Python convention stays
      intact; explicit native commands remain usable.
- [x] `self-test` runs the executing kit's suite independently of app commands,
      app failure or an app environment; it cannot be redirected by overrides.
- [x] Root test command is deliberately configured without recursive routing.
- [x] Both suites, fixture checks/tests/smokes and native checks run; missing
      tools, failures, durations and source identity remain visible.
- [x] Only intended managed files change; inventory diff and compatibility are
      documented, evidence linked and no later step starts.

## Verification

| Check | Command or method | Expected evidence |
| --- | --- | --- |
| Before | Existing probes and focused new regression suite | F1/F2 current false-success and intended assertion failures |
| Regression | `./harness self-test` | Installed copies, missing runners, real collection and zero cases |
| Root | `./harness check`, `./harness test`, `./harness inspect` | Honest exits and manifest validity |
| Fixtures | Existing check/test/smoke matrix and native commands | Preserved Node scripts; explicit Python unittest path |

## Notes and decisions

Implemented declaration: `[tool.harness.tests] runner = "pytest"` or `"unittest"`
in `pyproject.toml`. Existing native command overrides retain authority. Python
convention defaults to pytest, independently of installed modules. Root config
explicitly runs the guarded unittest suite; application consumers must replace
that repository-specific command. Arbitrary native commands own their collection
contract; complete cross-runner evidence enforcement belongs to Step 08.
Managed defaults are separate from the root project's explicit command.
