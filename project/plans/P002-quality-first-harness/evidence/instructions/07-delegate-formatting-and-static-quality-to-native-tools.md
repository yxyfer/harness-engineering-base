# Step 07: Delegate formatting and static quality to native tools

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** `format` fixes mechanical formatting; `check` reports remaining
issues without rewriting files. Use locked, project-local tooling. For new
profiles use Prettier/ESLint/strict TypeScript and Ruff/Pyright. Add only
concrete import boundaries: domain code separated from I/O and server-only
modules kept out of clients. File/function size remains advisory.

**Done when:** formatting is idempotent; check mode changes no tracked files;
required missing tools fail; seeded type, lint and import-boundary defects are
caught; an existing equivalent toolchain remains in control. Installed fixture
dependencies and relevant maintained source are actually included.

```text
Implement Step 07 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/07-delegate-formatting-and-static-quality-to-native-tools.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add format as a thin delegate to project-local
native formatters, and make check enforce declared static tools without edits.
Preserve existing tools and package managers. Use compatible pinned defaults
for new TypeScript and Python projects; keep settings in native config files.

Cover strict types, runtime-boundary coding conventions through appropriate
lint rules, and a few concrete import boundaries. Do not reimplement linters
with regexes or turn source-size guidance into hard gates. Update shipped
standards to describe real command behaviour, not obsolete optional fallbacks.

Prove formatter idempotence, non-mutating check mode, missing-tool failure and
seeded type/lint/import violations in isolated fixtures. Verify meaningful
maintained source is in scope. Write project/plans/P002-quality-first-harness/evidence/QH-07.md and stop.
```
