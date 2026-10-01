# Python profile

- Supported baseline: Python 3.11 or newer unless the project records another
  maintained range.
- Format and lint with Ruff. Configure `line-length = 80`; enable rules in
  project configuration rather than relying on user-global settings.
- Type-check maintained application code with Pyright in standard or strict mode;
  prefer strict mode for new modules and domain boundaries.
- Test with pytest. Name files `test_*.py`, functions `test_*`, variables and
  functions `snake_case`, and classes `PascalCase`.
- Use explicit exceptions and narrow `# noqa` or `# pyright: ignore[...]`
  suppressions. Include the rule code and a reason when it is not obvious.
- Without a reviewed equivalent check command, `./harness check` requires
  project-local `.venv` Ruff and Pyright, runs `ruff format --check`, `ruff check`
  and `pyright --project .`. Missing tools fail; syntax-only success is removed.
  Maintained extensionless Python scripts are explicitly sent to Ruff.
- `./harness format` runs only `ruff format` by default: no lint autofixes or
  type edits. A reviewed `commands.format` retains an existing formatter/manager.
- New opt-in defaults under `.harness/templates/python/` use strict Pyright,
  Ruff bugbear/broad-exception rules and TID251 adapter import restrictions.
  The entrypoint exception is scoped; adapt module names to actual architecture.
  Runtime validation is still code/test responsibility, not static proof.
