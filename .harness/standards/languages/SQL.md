# PostgreSQL and Neon

Use parameterised queries and server-only credentials. Encode real invariants
with appropriate types, primary and foreign keys, uniqueness, nullability and
check constraints. Use transactions for dependent writes and define duplicate
and concurrent update behaviour explicitly.

Version migrations and test them against disposable PostgreSQL before retained
data. Choose an established migration tool for the actual connection and schema
workflow; do not build a migration engine. Add indexes for observed queries and
investigate performance with PostgreSQL `EXPLAIN` when needed.

Neon driver transport determines transaction and connection support. Inspect
that support before choosing an implementation. Preview databases must have an
explicit data boundary and cleanup owner. A Git revert does not reverse SQL.

P001-T003 selects and exercises the migration and database workflow. This task
ships SQL guidance only: it adds no database, SQL validator or migration tool,
and makes no PostgreSQL or Neon integration claim.
