# Agent Operating Contract

This file governs all work in this repository. Read it before changing code, and
read canonical context under `docs/` and `project/architecture/` before making
product or architectural decisions.

Before editing source, also read `.harness/standards/BASE.md`,
`NAMING.md`, `TESTING.md`, and `ARCHITECTURE.md`, plus every relevant profile
under `.harness/standards/languages/`. Tool configuration is authoritative when
it is more specific than prose.

## Sources of truth

Use the narrowest authoritative source in this order:

1. The user's current request and explicit constraints.
2. This file.
3. `docs/PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, `DATA.md`, `QUALITY.md`, and
   `SECURITY.md`.
4. Accepted records in `docs/DECISIONS.md`.
5. The active plan and task.
6. Existing code and tests.

If these disagree, stop at any consequential ambiguity. Record a resolved,
durable choice in the appropriate context file or decision record.

## Working agreement

- Inspect before editing. Preserve unrelated and user-authored changes.
- Keep one bounded task and one verifiable outcome in focus.
- Prefer existing project components and conventions over parallel abstractions.
- State assumptions. Label mocked, synthetic, modelled, and simulated behaviour.
- Do not claim that an integration, test, or user flow works without evidence.
- Keep generated artifacts reproducible and source inputs traceable.
- Ask for human approval before destructive changes, external publication,
  production access, security trade-offs, or irreversible migrations.
- Update canonical context when implementation changes a durable fact.

## Standard workflow

1. Start at `project/README.md`. Read `project/FORMAT.md`, the selected plan and
   its task; task IDs must contain their parent plan ID. Load only relevant
   implementation instructions and context. Legacy projects retain their layout.
2. Reproduce or inspect the current behaviour.
3. Define observable acceptance criteria and verification before implementation.
4. Make the smallest coherent change. Keep the task's reviewer brief current:
   intent, implementation choice, affected boundaries, risk and recovery. Update
   the architecture map and ADRs for durable changes; link instead of duplicating.
5. Run `./harness check`, `./harness test`, and the relevant smoke or visual
   check.
6. Write a verification report with commands, results, evidence, and limitations.
7. Update task state/evidence and run `./harness project sync` before checks.
   Complete tasks stay with their plan. When every task is complete, run
   `./harness project archive PNNN` to move the bundle and repair navigation.
   Replaced plans may be explicitly superseded; unfinished scope stays incomplete.
   Update `project/debt.md` and the shared architecture for durable changes.

## Harness commands

```sh
./harness setup
./harness start
./harness inspect
./harness doctor
./harness format
./harness check
./harness test
./harness self-test
./harness smoke
./harness verify
./harness project check
./harness project sync
./harness project archive PNNN
```

Commands accept an optional target directory. A non-zero exit is a failed gate,
not an invitation to hide or weaken the check.

Use `self-test` for changes to the harness. It runs the executing kit's contract
suite independently of the target application's test command.

Configuration is defined in `.harness/config.toml`. Use project configuration
instead of editing command implementations to customise setup, start, check,
test, or smoke behaviour.

## Ownership boundaries

- Treat `AGENTS.md`, `docs/`, `project/`, legacy context folders, and
  `.harness/config.toml`, `.harness/evidence.json`, and `.harness/security.json`
  as project-owned after creation.
  `.harness/evidence.json` native evidence invocation is also project-owned.
- Managed ownership is the explicit file list in `.harness/release-files.json`,
  including each shipped skill file. Shared folders are not wholly managed:
  project skills/additions and generated environments remain project/local.
  Modify shipped files only when the task explicitly changes the harness.
- Never overwrite project-owned files during installation or updates. Propose a
  reviewable merge or side file instead.
- A managed-file checksum mismatch is a conflict to investigate, not permission
  to discard the local version.
- `manifest.py generate-release` is release authoring to stdout from reviewed
  inputs. Never use it to accept a consumer conflict; compare release inventory
  and checksum changes before replacing release metadata.
- Keep literal credentials, tokens, and machine-specific absolute paths out of
  committed harness configuration.

## Engineering baseline

- Use an 80-character line width unless a project records a compatible
  exception. URLs, generated content, tables, and indivisible tokens may remain
  longer where wrapping harms usability.
- Treat files above 350 maintained source lines and functions above 50 lines as
  cohesion review prompts, not automatic failures.
- Use formatter, linter, type-checker, and test settings from the relevant
  language profile. Keep suppressions narrow and explain non-obvious reasons.
- Apply TDD to defects and core behaviour where it improves feedback. Apply DRY
  to shared knowledge after the common concept is clear; neither is a ritual.

## Definition of done

Work is done only when the requested behaviour is implemented, acceptance
criteria are demonstrated, relevant checks pass, provenance and security impacts
are addressed, documentation reflects durable changes, and remaining limitations
are explicit.
