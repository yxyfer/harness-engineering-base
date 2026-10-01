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
