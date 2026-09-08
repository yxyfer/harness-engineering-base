# Next.js-shaped example

This fixture shows the package-script contract expected by the harness. The page
uses an App Router layout; checks, tests, and smoke validation intentionally use
Node.js only so the harness can be exercised without downloading dependencies.

In a real Next.js project, `dev` would normally call `next dev` and the other
scripts would delegate to the project's chosen linter, type checker, test runner,
and browser smoke suite.
