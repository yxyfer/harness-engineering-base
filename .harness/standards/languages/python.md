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
- `./harness check` runs `ruff format --check` and `ruff check` when Ruff is
  installed; syntax parsing remains a degraded fallback, reported as such.
