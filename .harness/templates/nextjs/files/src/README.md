# {{name}}

The application as a whole, in the same format as each feature's document. A
parent names and links its children; status and open work are read in the child.
Format: [docs/FORMAT.md](../docs/FORMAT.md).

## What it does

TODO: what a person can do with {{name}}, in a few sentences.

## How it works

Six areas; dependencies point down only and lint enforces it:
`app → experimental → features → components → core → config`. See
[the layout](../AGENTS.md#code-layout).

## Parts

Features, lowest first. Add one with `npm run new-feature -- <name>`.

| Feature | What it is | Uses |
| ------- | ---------- | ---- |

<!-- features:end -->

Below the features, [`core`](core/README.md) is the platform. Experiments, off
by default, are listed in [experimental](experimental/README.md).

## Choices

- Layered source, placed by evidence of maturity. Plans are this tree of
  documents, not a list of numbered plans.

## Open work

Only what belongs to no single feature.

## Evidence and limits

`npm run verify` runs the framework pins, format, lint with the module
boundaries, types, the boundary and document self-tests, the application tests,
the context check and the build.
