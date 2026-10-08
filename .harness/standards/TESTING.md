# Testing

Choose evidence according to [the working mode](../../docs/WORKFLOW.md).

- Use TDD for defects and stable core rules when it improves feedback.
- Test outputs, failure cases and important boundaries. Avoid tests that only
  restate implementation or assert an arbitrary file arrangement.
- Use the receiving application's test runner and relevant browser journeys.
  Node's test runner suits plain TypeScript rules; Playwright suits React
  interactions. Type stripping does not perform type checks; run the separate
  TypeScript command.
- Harness self-tests exercise kit commands in disposable fixtures. They must
  demonstrate useful failures as well as success without changing working code.
- Version-check tests use labelled synthetic metadata; a live application
  version check needs an explicit installed app and fresh registry evidence.
- Start child test commands outside the parent's test-runner context and verify
  that tests actually executed; a zero exit alone can be misleading.
- PostgreSQL, external integrations and deployment claims need evidence from
  those systems. Fixtures and local browser checks cannot substitute for it.
