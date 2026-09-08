# Project Harness

A small, inspectable engineering harness for agent-assisted software projects. It
keeps project intent, implementation constraints, work plans, and verification in
the repository so that humans and coding agents operate from the same context.

The repository is itself the starter layout: clone it or create a repository from
it and the project context, harness commands, checks, fixtures, and Codex skills
are already in their runtime locations. The harness detects common Node.js and
Python conventions, delegates to project-owned scripts where they exist, and
fails with an actionable message where they do not.

## Three-layer structure

- Project context stays visible in `AGENTS.md`, `docs/`, `plans/`, `tasks/`, and
  `verification/` so humans and agents can maintain it together.
- Managed machinery lives under `.harness/`, including command implementations,
  policy checks, and test fixtures.
- Agent workflows live under `.agents/skills/`, where Codex can discover them at
  repository scope.

The root `harness` executable is the only public entry point into managed
machinery.

## Command contract

All commands accept a target directory as their first argument and default to the
current directory.

```sh
./harness inspect .harness/tests/fixtures/nextjs-project
./harness check .harness/tests/fixtures/nextjs-project
./harness test .harness/tests/fixtures/nextjs-project
./harness smoke .harness/tests/fixtures/nextjs-project
```

| Command | Purpose |
| --- | --- |
| `setup` | Install dependencies using the lockfile-native package manager. |
| `start` | Run the project's declared development entry point. |
| `check` | Run harness policy checks, then project lint/type checks. |
| `test` | Run the project's declared automated tests. |
| `smoke` | Run the smallest user-visible health check. |
| `inspect` | Print detected stack, commands, context coverage, and Git state. |

Set `HARNESS_KIT_ROOT` when the command implementation is hosted outside the
target repository. Set `HARNESS_CHECKS_DIR` to select a different checks
directory.

## Starting a new project

1. Create a repository from this base or clone the complete repository, including
   its hidden `.harness/` and `.agents/` directories.
2. Fill in the seven files under `docs/`; delete prompts that do not apply.
3. Put the first bounded plan in `plans/active/` and create a task from
   `tasks/TASK_TEMPLATE.md`.
4. Add project-native `check`, `test`, and `smoke` scripts where the detected
   defaults are insufficient.
5. Run `./harness inspect`, then `./harness check`, `./harness test`, and
   `./harness smoke`.

Automated, conflict-aware adoption into an existing repository is planned but is
not part of this phase. Until then, do not paste these files over existing project
files without reviewing collisions.

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

The supported platform is macOS. Commands require POSIX `sh`, and policy checks
use Python 3. Git, Node.js, and package managers are required only when the target
project uses them.
