# Architecture Context

Status: current

## System shape

The root `harness` dispatcher invokes managed command implementations under
`.harness/bin/`. Commands validate project-owned TOML configuration, run managed
policy checks, and then delegate to project-native tools. Visible context remains
project-owned; managed checks, standards, tests, and skills are checksum-tracked.

Managed `default-config.toml` supplies fallback settings; the executing
repository's project-owned `config.toml` does not supply commands to unrelated
targets. Explicit CLI/environment/config commands retain precedence.

Application `test` and harness `self-test` are separate entry points. Python
application metadata declares pytest or unittest; absent metadata uses pytest
without inspecting module availability. The selected app environment owns its
runner. A small stdlib discovery adapter rejects empty unittest collections.
`self-test` selects the executing kit's suite and environment and ignores app
test overrides. This repository declares a direct, non-recursive suite command
in its own configuration. See [ADR-004](DECISIONS.md).

Managed `source_paths.py` owns literal directory exclusion matching, pruned
tree traversal and supported executable shebang classification. Size, link,
claim and degraded Python syntax scans share it. Scans skip all symlinks;
canonical policy inputs reject symlink components independently of exclusions.
Native tools retain their own configuration and discovery. Required policy
checks precede one project static-check implementation; overrides/package
scripts prevent an additional automatic Python stage. See
[ADR-005](DECISIONS.md).

## Boundaries

| Component | Owns | May depend on | Must not depend on |
| --- | --- | --- | --- |
| Root dispatcher | Public command routing | `.harness/bin/` | Project implementation details |
| Managed commands | Resolution and orchestration | Config, checks, project commands | Overwriting project context |
| Policy checks | Cross-project invariants | Validated config and target files | Product-specific assumptions |
| Project tools | Language semantics and formatting | Project source/configuration | Managed harness ownership |

## External systems

| System | Purpose | Authentication | Failure behaviour | Real or simulated |
| --- | --- | --- | --- | --- |
| Local runtimes/tools | Execute configured checks | Local environment | Actionable failure or degraded warning | Real |

## Runtime and deployment

The first supported platform is macOS. The dispatcher uses POSIX `sh`; TOML
validation and managed checks require Python 3.11 or newer. Project runtimes are
used only when a target profile requires them. Commands expose selected profiles,
tool coverage, and failures without printing command bodies or secrets.

## Architectural risks

- Optional tools can be absent before Phase 4 adds dependency diagnostics.
- Tool configuration is shared ownership and requires conflict-aware merging in
  future adoption and upgrade flows.

## Target architecture agreed on 2026-10-01

The [product vision](PRODUCT.md) retains the three ownership layers and adds a
small programmatic control-selection and evidence pipeline. It is planned, not
implemented by the current command suite.

TypeScript and Python are the language profiles; Next.js is a framework profile
on TypeScript. Reviewed project capabilities activate additional controls for
browser UI, identity, persistence, and other actual boundaries. Detection must
not silently remove a configured requirement.

Project-native tools execute every automated gate. No LLM evaluator or external
model call grades verification. The coding agent can author and repair tests;
CI independently executes the required suite. Human product/design acceptance
and runtime permissions remain separate responsibilities.

Reusable application foundations are project-owned or explicitly versioned
dependencies. Customer-specific themes and features must not enter the managed
harness checksum inventory. Existing component systems take precedence over a
new default kit.

Implementation follows [the quality-first plan](../plans/active/QUALITY_FIRST_HARNESS.md).
