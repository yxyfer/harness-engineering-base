# Core

The platform below the features. It knows no product rule and imports only
itself and `src/config`.

## What it does

Gives every feature the same platform pieces so none is written twice. Start
here: until there is a capability a person would name, work lands in `core` and
`src/app`.

## How it works

Plain modules that features and `src/app` import directly. A module belongs here
when several product areas use it, it knows no product rule, and it has been
exercised in production.

## Parts

| Part        | What it is for                                               | Where            |
| ----------- | ------------------------------------------------------------ | ---------------- |
| Experiments | The one decision on whether an experiment is on for a person | `experiments.ts` |

## Choices

- One experiment decision for every entry point. See
  [experiments](../experimental/README.md).

## Open work

## Evidence and limits

`tests/experiments.test.ts` covers the experiment decision.
