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
to override a project command for one invocation. `self-test` rejects
`--command`; application command overrides cannot redirect that suite.

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
| `self-test` | Run the executing harness's contract suite independently. |
| `smoke` | Run the smallest user-visible health check. |
| `inspect` | Print detected stack, commands, context coverage, and Git state. |

Set `HARNESS_KIT_ROOT` when the command implementation is hosted outside the
target repository. Set `HARNESS_CHECKS_DIR` to select a different checks
directory.

## Core CI

The [core CI guide](.harness/ci/README.md) describes the default pinned macOS
GitHub Actions workflow and reproducible locked setup. It executes actual native
checks, both harness suites, fixture tests/smokes and disposable negative cases.
Local execution evidence and remote execution status are separate in
[QH-05](verification/QH-05.md). No remote protection settings are configured.

## Version and configuration

The harness version is available offline in `.harness/VERSION` and is displayed
by `./harness inspect`. The configuration schema begins at version `1` and lives
in project-owned `.harness/config.toml`. Managed `.harness/default-config.toml`
supplies defaults when the target has no project configuration; it does not
inherit the executing repository's custom commands.

| Section | Purpose |
| --- | --- |
| `project.profiles` | Enabled language profiles; `auto` delegates to detection. |
| `commands` | Optional setup, start, check, test, and smoke commands. |
| `checks.required` | Ordered policy-check identifiers that must run. |
| `standards` | Shared line, file, and function thresholds. |
| `readiness` | Required context files and future readiness-gate behaviour. |
| `security` | `off`, `local`, or `ci` security mode. |
| `analysis.exclude` | Literal directories excluded from harness-owned scans. |

## Engineering standards

The shared baseline lives in `.harness/standards/`, split into four small
documents for implementation, naming, testing, and architecture. Language
profiles cover Python, TypeScript/JavaScript, shell, and Markdown. Agents must
read the shared rules and only the profiles relevant to files they change.

The default line width is 80 characters. Files above 350 maintained source lines
and Python functions above 50 lines produce advisory cohesion warnings. These
limits deliberately do not fail the gate: a larger unit may be the clearer
design, provided the task or a scoped tool setting records why.

`./harness check` detects configured or present profiles. It delegates style and
correctness to established tools instead of reimplementing their parsers:

| Profile | Formatter | Linter/type check | Test convention |
| --- | --- | --- | --- |
| Python | Ruff | Ruff and Pyright | pytest |
| TypeScript/JavaScript | Prettier | ESLint and strict TypeScript | project runner |
| Shell | shfmt | ShellCheck | command/exit behaviour |
| Markdown | formatter/editor wrapping | markdownlint and local-link check | rendered/config evidence |

Missing optional tools are reported as degraded coverage. Project-native
commands and tool configuration remain authoritative. The fixture projects show
complete Python and Node configurations aligned to the shared defaults.

Harness-owned size, link, claim and degraded Python syntax scans share directory
discovery. In `analysis.exclude`, `generated` matches a directory at any depth;
`src/generated` matches only that root-relative prefix. Rules are literal, not
globs, and do not exclude similarly named siblings or files. Ignored directories
are pruned before traversal. All file/directory symlinks are skipped, including
internal links. Required canonical context is checked separately and rejects
symlinks. Native tools retain their own scope; see
[the exclusion contract](.harness/standards/BASE.md).

Extensionless executables with direct, `env` or `env -S` shebangs are classified
as Python (`python`, `python3`, versioned Python 3) or shell (`sh`, `bash`, `dash`).
Unknown interpreters and complex env prefixes do not default to shell. Other
interpreters require deliberate project-native coverage.

After required policy checks, `check` selects one project implementation:
CLI override, environment override, configured command, package `check`, package
`lint`/`typecheck` fallback, then automatic Python checks. The package fallback
can run both declared scripts once. Any selected override/package path prevents
an additional automatic Python stage. A failed policy or selected command stops
the gate. With no native Python tools, syntax parsing follows harness discovery,
including supported extensionless Python; that remains degraded coverage.

Every section and key is validated. Unknown or missing keys, invalid types,
unsupported values, absolute exclusions, and parent-directory exclusions fail
with the configuration path, failing key, and expected value.

Configuration-file selection uses this order:

1. `--config PATH`.
2. `HARNESS_CONFIG`.
3. The target project's `.harness/config.toml`.
4. The executing harness's managed `.harness/default-config.toml`.

Project command selection uses this order:

1. `--command COMMAND` for the current action.
2. `HARNESS_SETUP_COMMAND`, `HARNESS_START_COMMAND`,
   `HARNESS_CHECK_COMMAND`, `HARNESS_TEST_COMMAND`, or
   `HARNESS_SMOKE_COMMAND`.
3. The corresponding `commands` value in TOML.
4. The target package's `test` script for Node.js testing.
5. Python runner declaration/convention for Python testing, or the existing
   detected command for the other actions.

`./harness inspect` shows the effective non-sensitive values and the source of
each resolved command. Command bodies are reported as configured or automatic,
not printed. Configuration must reference secrets through environment variables;
never commit literal credentials or machine-specific paths.

## Application tests and harness self-tests

`test` never selects `.harness/tests` implicitly. For a Python project, declare
the intended runner in `pyproject.toml`:

```toml
[tool.harness.tests]
runner = "pytest"
```

Use `runner = "unittest"` for an explicit stdlib discovery project. Without a
declaration, the Python convention is pytest, regardless of which modules are
installed. Missing pytest fails with setup guidance; it never falls back to
unittest. Unittest discovers `tests/test_*.py`; pytest keeps its native project
configuration. Both supported Python paths fail if no cases are collected.

Python testing selects the target's `.venv/bin/python` when available. An
incomplete `.venv` blocks automatic Python testing. Native command overrides
also receive that environment on PATH when valid, so `python`/`python3` resolve
locally; explicit executable paths remain authoritative. Other environments
and runners can use the existing command overrides. Arbitrary native scripts
own their collection/exit contract; full evidence enforcement is future Step 08.

`self-test [target]` selects the executing kit's tests and kit-root Python
environment, irrespective of the target's runner, package script or test
override. When kit and app share a root, they also share that root environment.
There is no `commands.self-test` configuration key. The schema remains version 1.

This repository deliberately configures `commands.test` as a direct guarded
unittest invocation of `.harness/tests`, without calling the dispatcher again.
When creating an application from this repository, replace that repository-only
command with the application's native command or leave it empty for detection.
Use the managed default configuration for a disposable clean installation;
never overwrite an existing consumer's configuration automatically.

The harness regression suite needs real pytest for mixed-suite and collection
cases. Set up the kit environment explicitly before verification:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r .harness/tests/requirements.txt
./harness test
./harness self-test
```

Tests install nothing and require no external service. A missing regression
dependency fails visibly instead of skipping the required cases. The Python
command fixture declares unittest and needs no pytest to run its own one case.
Existing unittest-only projects that relied on the old implicit fallback must
declare their runner or keep an explicit native command. Update the complete
managed inventory together; older kits lack the new defaults and runner helper.

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
| Exact files listed in `.harness/release-files.json` | Harness | Check checksums before replacing. |
| Additional files in shared folders, including project skills | Project/local | Never absorb into release ownership automatically. |
| `harness` | Harness | Check its checksum before replacing. |
| `.harness/config.toml` and future `exceptions.yml` | Project | Never overwrite automatically. |
| `AGENTS.md`, `docs/`, `plans/`, `tasks/`, `verification/` | Project | Never overwrite automatically. |
| Language and tool configuration | Shared | Change only through a reviewable merge. |

`.harness/manifest.json` records the installed harness version, manifest schema,
installation timestamp, and SHA-256 checksums for managed files. It deliberately
excludes project-owned configuration and context.

`.harness/release-files.json` is the reviewed release input list; its own
checksum is included in the manifest. Verification requires the manifest's
paths to match that list exactly and verifies every shipped checksum. Added
skills, notes, `.venv`, dependencies and caches do not change installation
health, even inside shared folders. Shipped fixture source remains managed.

Release maintainers can emit a candidate manifest with
`python3 .harness/bin/manifest.py generate-release ROOT [UTC_TIMESTAMP]`.
This reads only listed files, writes JSON to stdout and never discovers new
ownership by scanning directories. Review inventory additions/removals and
hash changes before replacing release metadata. Generation is an explicit
release-authoring operation and must never bless consumer edits. The old
`generate` action now returns usage exit 2.

Manifest/inventory entries must be canonical relative POSIX paths in managed
namespaces. Traversal, absolute/drive paths, aliases, duplicate JSON keys,
runtime/cache inputs and project-owned configuration are rejected. Shipped
files and metadata must be regular files with no symlink in their destination
or parents. Unlisted project/runtime symlinks are allowed and are not traversed.

Manifest schema 1 and version `0.1.0` are retained for this unreleased base.
The new verifier requires the release inventory; an older kit without it fails
exit 5. Updating an old kit requires reviewed metadata and verifier changes
with existing conflicts preserved; no automatic installer/migration exists.
The inventory and checksums are editable integrity metadata, not signatures or
a defence against concurrent filesystem replacement or a malicious maintainer.

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
