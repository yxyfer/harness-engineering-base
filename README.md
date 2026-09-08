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

All commands accept one optional target directory and default to the current
directory. Use `--config PATH` to select another TOML file or `--command COMMAND`
to override a project command for one invocation.

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

## Version and configuration

The harness version is available offline in `.harness/VERSION` and is displayed
by `./harness inspect`. The configuration schema begins at version `1` and lives
in `.harness/config.toml`.

| Section | Purpose |
| --- | --- |
| `project.profiles` | Enabled language profiles; `auto` delegates to detection. |
| `commands` | Optional setup, start, check, test, and smoke commands. |
| `checks.required` | Ordered policy-check identifiers that must run. |
| `standards` | Shared line, file, and function thresholds. |
| `readiness` | Required context files and future readiness-gate behaviour. |
| `security` | `off`, `local`, or `ci` security mode. |
| `analysis.exclude` | Relative paths excluded from repository analysis. |

Every section and key is validated. Unknown or missing keys, invalid types,
unsupported values, absolute exclusions, and parent-directory exclusions fail
with the configuration path, failing key, and expected value.

Configuration-file selection uses this order:

1. `--config PATH`.
2. `HARNESS_CONFIG`.
3. The target project's `.harness/config.toml`.
4. The executing harness's default `.harness/config.toml`.

Project command selection uses this order:

1. `--command COMMAND` for the current action.
2. `HARNESS_SETUP_COMMAND`, `HARNESS_START_COMMAND`,
   `HARNESS_CHECK_COMMAND`, `HARNESS_TEST_COMMAND`, or
   `HARNESS_SMOKE_COMMAND`.
3. The corresponding `commands` value in TOML.
4. A language-profile default when profiles begin supplying commands in Phase 3.
5. Existing Node.js and Python auto-detection.

`./harness inspect` shows the effective non-sensitive values and the source of
each resolved command. Command bodies are reported as configured or automatic,
not printed. Configuration must reference secrets through environment variables;
never commit literal credentials or machine-specific paths.

## Exit contract

| Exit | Meaning |
| --- | --- |
| `0` | The requested operation succeeded. |
| `1` | A project command, check, test, or smoke operation failed. |
| `2` | CLI usage or options are invalid. |
| `3` | Reserved for incomplete project readiness in Phase 4. |
| `4` | Configuration is invalid or incompatible. |
| `5` | The harness installation or managed-file contract is broken. |

Delegated project-command exit codes are included in the error message and
normalised to exit `1` at the public harness boundary.

## File ownership

| Paths | Owner after creation | Update rule |
| --- | --- | --- |
| `.harness/**`, except project-owned files below | Harness | Check checksums before replacing. |
| `.agents/skills/<shipped-skill>/**` | Harness | Check for local changes before replacing. |
| `harness` | Harness | Check its checksum before replacing. |
| `.harness/config.toml` and future `exceptions.yml` | Project | Never overwrite automatically. |
| `AGENTS.md`, `docs/`, `plans/`, `tasks/`, `verification/` | Project | Never overwrite automatically. |
| Language and tool configuration | Shared | Change only through a reviewable merge. |

`.harness/manifest.json` records the installed harness version, manifest schema,
installation timestamp, and SHA-256 checksums for managed files. It deliberately
excludes project-owned configuration and context.

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

The supported platform is macOS. Commands require POSIX `sh`; configuration uses
Python 3.11 or newer so it can rely on the standard-library TOML parser. Git,
Node.js, and package managers are required only when the target project uses
them.
