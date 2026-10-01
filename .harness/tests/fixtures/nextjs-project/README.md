# Next.js-shaped example

This fixture shows the package-script contract expected by the harness. The page
uses an App Router layout; checks, tests, and smoke validation intentionally use
Node.js rather than a real Next.js runtime. Locked setup installs native static
tools and type-only React declarations; all maintained app/scripts/tests sources,
including the JSX page, are included in type checking. No download occurs in
format/check/test/smoke.

In a real Next.js project, `dev` would normally call `next dev` and the other
scripts would delegate to the project's chosen linter, type checker, test runner,
and browser smoke suite.
