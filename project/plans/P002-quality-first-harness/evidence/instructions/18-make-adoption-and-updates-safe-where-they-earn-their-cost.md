# Step 18: Make adoption and updates safe where they earn their cost

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** repeated use preserves project context and customisations.
Implement only the adoption/update operations justified by Step 17. A small
documented copy/diff procedure remains valid when automated distribution is not
justified.

An automated path starts with dry-run inspection and a file-level proposal.
Distinguish absent files, unchanged managed files, modified managed files and
project-owned files. Never overwrite project-owned context/configuration or
customer components. Propose side files or a reviewable merge. Validate version
compatibility, paths, source checksum and ownership before writing. Checksums
show integrity against an inventory; do not claim they authenticate an unknown
remote publisher. Use a trusted pinned local/release source.

Updates need backups, a transaction journal or equivalent, crash-safe recovery
and guarded rollback that preserves subsequent user edits. Runtime state stays
outside the release inventory. A shared component package is conditional on
multiple consumers needing the same contract; upgrade consumers deliberately.

**Done when:** dry-run changes no files; apply is idempotent; conflicts stop
safely; interrupted writes recover; rollback preserves later edits; custom
skills, config and themes survive; malicious paths are rejected. Exercise local
copies, not live customer repositories, for destructive fault tests.

```text
Implement Step 18 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/18-make-adoption-and-updates-safe-where-they-earn-their-cost.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md and the Step 17 adoption decision. Implement only
justified distribution needs. If manual adoption is sufficient, deliver and
rehearse a precise copy/diff/update procedure instead of a general installer.

For automation, start with a non-mutating file-level plan using the explicit
release inventory. Preserve project-owned files and modified managed content;
propose merges/side files. Check compatibility, paths and trusted source before
writes. Provide recoverable apply, idempotence and rollback guarded against
subsequent edits. Keep component distribution separate from harness ownership.

Test clean adoption, conflicts, added skills, customised themes, generated
state, interrupted writes, repeated apply and rollback in disposable projects.
Extract a shared component package only if multiple consumers justify it.
Write project/plans/P002-quality-first-harness/evidence/QH-18.md with recovery evidence and stop.
```
