# Project Harness

A small, inspectable engineering harness for agent-assisted software projects. It
keeps project intent, implementation constraints, work plans, and verification in
the repository so that humans and coding agents operate from the same context.

This first pass is intentionally framework-light. The harness detects common
Node.js and Python conventions, delegates to project-owned scripts where they
exist, and fails with an actionable message where they do not.

## What is included

- `template/` — the files copied into an application repository.
- `skills/` — reusable agent workflows for common engineering tasks.
- `checks/` — portable policy checks used by `harness/check`.
- `examples/` — minimal Node/Next.js-shaped and Python projects used to exercise
  the command contract.

## Command contract

All commands accept a target directory as their first argument and default to the
current directory.

```sh
./template/harness/inspect examples/nextjs-project
./template/harness/check examples/nextjs-project
./template/harness/test examples/nextjs-project
./template/harness/smoke examples/nextjs-project
```

| Command | Purpose |
| --- | --- |
| `setup` | Install dependencies using the lockfile-native package manager. |
| `start` | Run the project's declared development entry point. |
| `check` | Run harness policy checks, then project lint/type checks. |
| `test` | Run the project's declared automated tests. |
| `smoke` | Run the smallest user-visible health check. |
| `inspect` | Print detected stack, commands, context coverage, and Git state. |

Set `HARNESS_KIT_ROOT` when the commands have been copied away from this
repository but should still use its policy checks. Set `HARNESS_CHECKS_DIR` to
select a different checks directory.

## Starting a project

1. Copy the contents of `template/` into the application repository.
2. Fill in the seven files under `docs/`; delete prompts that do not apply.
3. Put the first bounded plan in `plans/active/` and create a task from
   `tasks/TASK_TEMPLATE.md`.
4. Add project-native `check`, `test`, and `smoke` scripts where the detected
   defaults are insufficient.
5. Run `harness/inspect`, then `harness/check`, `harness/test`, and
   `harness/smoke`.

The templates contain `Status: needs-project-input` markers on purpose. The
documentation check reports these as warnings until the project context is made
specific.

## Design choices

- Repository files are the durable source of truth; chat history is not.
- Project-native commands remain authoritative; the harness orchestrates them.
- Verification records evidence and limitations instead of asserting success.
- Demo and data provenance are explicit, including synthetic and simulated paths.
- Human approval is required at consequential product, security, and release
  boundaries.

## Requirements

The shell commands require POSIX `sh`. Policy checks use Python 3. Git, Node.js,
and package managers are required only when the target project uses them.
