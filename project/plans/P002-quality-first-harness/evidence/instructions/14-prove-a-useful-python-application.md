# Step 14: Prove a useful Python application

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** Python support handles meaningful inputs, domain behaviour,
persistence and failure. Keep the tiny existing server for dispatcher tests.
Suggested new location: `examples/python-work-items/`.

Default to a small CLI that validates synthetic work-item records, imports them
atomically into a disposable SQLite database and queries the saved results.
Change to a service only if an actual pilot requires an API. Use typed
boundaries, clear exit/error behaviour and a strict core. New projects may use
uv with a committed lock; existing managers stay authoritative. CI must check
lockfile freshness, following
[uv's locked workflow](https://docs.astral.sh/uv/concepts/projects/sync/) when
that manager is selected.

**Done when:** valid import/query works; malformed data, duplicate identifiers
and storage errors fail predictably without unintended partial writes; real
subprocess tests inspect exits/stdout/stderr; collection is complete; the actual
database is checked; Ruff, Pyright and pytest run in the declared environment.

```text
Implement Step 14 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/14-prove-a-useful-python-application.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add a substantive Python reference project while
retaining the lightweight dispatcher fixture. Unless a real pilot establishes
an API need, implement a small typed CLI for validating, atomically importing
and querying synthetic work items in a disposable real SQLite database.

Separate pure domain rules from file/database I/O. Use Ruff, Pyright and pytest
through native project commands and a reproducible environment; preserve an
existing manager or use uv with lock freshness checked. Add no web framework
without an actual requirement. Label data provenance and document CLI contracts.

Test real process exits/output, invalid input, duplicate records, successful
persistence, transaction failure and cleanup. Wire format/check/test/smoke and
verify into the Python profile. Seed an actual boundary defect to demonstrate
failure detection. Write project/plans/P002-quality-first-harness/evidence/QH-14.md and stop.
```
