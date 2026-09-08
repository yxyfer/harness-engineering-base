# Agent Operating Contract

This file governs all work in this repository. Read it before changing code, and
read the canonical context under `docs/` before making product or architectural
decisions.

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

1. Read the task, relevant context, and active plan.
2. Reproduce or inspect the current behaviour.
3. Define observable acceptance criteria and verification before implementation.
4. Make the smallest coherent change.
5. Run `./harness check`, `./harness test`, and the relevant smoke or visual
   check.
6. Write a verification report with commands, results, evidence, and limitations.
7. Move a completed plan to `plans/completed/` and update context or debt.

## Harness commands

```sh
./harness setup
./harness start
./harness inspect
./harness check
./harness test
./harness smoke
```

Commands accept an optional target directory. A non-zero exit is a failed gate,
not an invitation to hide or weaken the check.

Configuration is defined in `.harness/config.toml`. Use project configuration
instead of editing command implementations to customise setup, start, check,
test, or smoke behaviour.

## Ownership boundaries

- Treat `AGENTS.md`, `docs/`, `plans/`, `tasks/`, `verification/`, and
  `.harness/config.toml` as project-owned after creation.
- Treat `harness`, other `.harness/` files, and shipped `.agents/skills/` as
  managed harness files. Modify them only when the task explicitly changes the
  harness itself.
- Never overwrite project-owned files during installation or updates. Propose a
  reviewable merge or side file instead.
- A managed-file checksum mismatch is a conflict to investigate, not permission
  to discard the local version.
- Keep literal credentials, tokens, and machine-specific absolute paths out of
  committed harness configuration.

## Definition of done

Work is done only when the requested behaviour is implemented, acceptance
criteria are demonstrated, relevant checks pass, provenance and security impacts
are addressed, documentation reflects durable changes, and remaining limitations
are explicit.
