# Step 05: Add CI for the repaired core

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** clean environments run the repaired contract with actual required
tools. Use existing CI, or a thin GitHub Actions workflow when none exists.
Start with macOS. Install ShellCheck, shfmt and Markdown tooling; do not depend
on warning-only coverage. Pin tools/runtimes and install locked dependencies.

**Done when:** a clean setup runs the suite; deliberate failures reach the
correct jobs; remote execution is evidenced or explicitly unverified. A workflow
file alone does not establish successful CI or branch protection.

```text
Implement Step 05 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/05-add-ci-for-the-repaired-core.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add a small CI workflow for the repaired harness
and existing fixtures, using the current provider or a documented GitHub Actions
default. Preserve macOS support; pin compatible tools, runtimes and action refs.

Actually run relevant shell, Markdown, TypeScript and Python checks, self-tests,
fixture tests and smoke. Fix exposed in-scope defects without blanket disables.
Use locked installs, bounded jobs, temporary data and useful logs. Show negative
fixtures fail without leaving the working tree broken. Do not change remote
protection settings. Record a remote run if authorised and available; otherwise
mark execution unverified. Write project/plans/P002-quality-first-harness/evidence/QH-05.md and stop.
```
