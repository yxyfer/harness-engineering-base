# Reference quality

Status: current

Native Prettier, strict TypeScript and typed ESLint cover maintained TS/TSX,
configuration and tests. Production builds use real `next build --webpack` with
two workers and no external fonts. Component tests use Vitest/Testing Library;
navigation uses Chromium Playwright against `next start`, with no retries.
Native JUnit collection is retained, not inferred from a successful process.

ESLint 10 uses the official Next plugin and compatible React-hooks/typed rules.
The bundled Next config currently pulls React/import/a11y plugins requiring
unsupported ESLint 9; neither that version nor peer overrides are used. Full
accessibility is a later gate, not silently claimed by this minimal foundation.

Initial checks cover edit validation/confirmation/cancel/reset, theme state,
list/detail/catalogue/404 navigation and mobile/desktop overflow. Screenshots
are evidence, not auto-approved visual baselines. Full accessibility, performance,
persisted reload, authentication and end-to-end product acceptance are pending.
