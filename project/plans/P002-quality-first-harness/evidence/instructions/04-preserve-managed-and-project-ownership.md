# Step 04: Preserve managed and project ownership

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** normal customisation and generated environments preserve
installation health; shipped-file modifications stay visible. Fix F6/F7 using an
explicit release-owned inventory. Additional project skills are not shipped
skills.

**Done when:** added skills, `.venv`, dependencies and caches are allowed;
changed/missing shipped files fail; unsafe manifest paths and symlink
destinations are rejected; regeneration never absorbs customer files or local
secrets.

```text
Implement Step 04 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/04-preserve-managed-and-project-ownership.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md and reproduce F6 and F7 first.

Make release ownership explicit rather than treating every file under shared
folders as managed. Preserve shipped-file checksum checks while allowing project
skills and runtime environments. Validate manifest paths and symlink handling.
Do not build the installer yet or regenerate away a consumer conflict.

Exercise a disposable full installation with a project skill, a real no-pip
virtual environment, caches, modified/missing shipped files and unsafe paths.
Prove release generation contains only intended inputs. Document ownership and
compatibility, run required checks, write project/plans/P002-quality-first-harness/evidence/QH-04.md, and stop.
```
