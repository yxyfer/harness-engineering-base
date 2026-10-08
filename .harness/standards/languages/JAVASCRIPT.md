# JavaScript

Use ES modules for kit configuration and self-tests. Run Prettier and ESLint's
recommended JavaScript rules with Node globals for Node code. Do not enable
browser globals for filesystem or process code.

Use argument arrays for child processes, check their exit status and preserve
diagnostics. Create temporary directories with unique names and clean up only
resources created by that test. Keep maintained code out of `node_modules`.
