# TypeScript and JavaScript profile

- Use an actively supported Node.js release recorded by the project. Prefer
  TypeScript for maintained domain and boundary code; JavaScript is valid for
  small scripts and existing codebases.
- Format with Prettier at 80 characters and lint with ESLint flat configuration.
  Run both through project-owned package scripts.
- Enable strict TypeScript for new projects. Narrow `unknown` at boundaries and
  avoid `any` unless an interoperability constraint is documented.
- Use `camelCase` for values/functions and `PascalCase` for types/components.
  Follow framework-required filenames.
- Name tests `*.test.ts`, `*.test.tsx`, or their JavaScript equivalents. Use the
  project's established test runner.
- Keep disables scoped to a line or file and include a reason. Do not use a
  repository-wide disable to avoid fixing unrelated violations.
- `format` uses a project format script, then local Prettier; `check` uses the
  reviewed check command/script, a complete format:check/lint/typecheck trio,
  or local Prettier check, ESLint and TypeScript --noEmit. Missing controls fail.
  No npx download or global tool substitution occurs. Existing managers survive.
- Opt-in `.harness/templates/typescript/` pins a compatible typed ESLint toolchain
  separately from the existing JS fixture. Strict types, unsafe any/operations,
  floating promises and thrown-value rules protect boundary coding conventions.
  Domain-to-I/O and client-to-server restrictions use native restricted-import
  rules for the demonstrated layout. They are not a transitive security graph;
  aliases/dynamic imports and framework enforcement need project-specific rules.
