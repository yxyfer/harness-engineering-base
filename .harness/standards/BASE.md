# Shared engineering baseline

Apply this document to all source changes, together with each relevant language
profile. Automated formatters and linters are authoritative where configured.

## Required practices

- Optimise first for code another maintainer can understand and change safely.
- Validate untrusted input at system boundaries; keep trusted internal paths
  simple.
- Fail explicitly with actionable context. Do not hide errors or silently invent
  successful results.
- Use the strongest practical type guarantees without duplicating runtime
  validation already performed at a boundary.
- Add a dependency only when it removes more risk or maintenance than it adds.
  Prefer an existing project dependency or platform capability.
- Comment decisions, constraints, and surprising trade-offs. Do not narrate code
  that is already clear.
- Reuse established project components and conventions before adding a parallel
  abstraction.
- Remove dead code when its removal is safe and in scope. Do not keep speculative
  paths for hypothetical future use.

## Shared numeric defaults

- Line width: 80 characters. A formatter may leave an unavoidable line longer;
  use its documented exemptions for URLs, generated content, or indivisible
  tokens.
- Large file: warn above 350 source lines.
- Large function: warn above 50 source lines where reliable language-aware
  analysis is available.

Size warnings prompt a cohesion review; they are not automatic failures. If a
larger unit is clearer, keep it and record a short rationale in the task or the
narrowest tool-native suppression. The governed exception register arrives in
Phase 6.

## Exclusions

Generic size analysis excludes generated and vendored code, installed
dependencies, build output, migrations, schemas, and fixtures. Keep exclusions
explicit in `.harness/config.toml`; a project may narrow them when those files
are genuinely maintained as source.
