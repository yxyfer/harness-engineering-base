# Design Context

Status: current; Step 10 synthetic reference foundation

## Experience principles

- Make the user's next decision obvious.
- Show system state, provenance, and uncertainty at the point of use.
- Preserve a human confirmation step for consequential actions.

## Key journeys

| Journey | Entry | Success state | Failure or empty state |
| --- | --- | --- | --- |
| Browse synthetic work | Work-item list | Detail snapshot | Real unknown-item 404 |
| Edit preview | Detail editor | Confirmed local preview | Linked title error, cancel/reset |
| Inspect reusable kit | Component catalogue | Same components in Paper/Ink | Explicit loading/empty/error/no-access examples |

## Interface system

The [standalone app](../examples/nextjs-app/README.md) owns its small
shadcn-style Radix foundation: button variants, labelled field/error, confirmation
dialog, semantic navigation/list, theme switch and edit/state patterns.
Component APIs and reuse rules are in its
[design context](../examples/nextjs-app/docs/DESIGN.md). No customer assets were
available; system fonts, owned text mark and semantic CSS tokens avoid downloads.
Paper uses warm light/forest tokens; Ink uses navy/pale-blue tokens. Components
and behavior are shared, not cloned per theme. No shared package is extracted.

## Accessibility

Use landmarks, labels, visible focus, a skip link, linked input errors and Radix
dialog keyboard/focus handling. Initial interaction checks are not full
accessibility/contrast certification; that belongs to the later browser gates.
No animation is needed. Human design acceptance is separate from test results.

## Visual verification

Check list/detail/catalogue at 390px and 1440px in both themes, including edit
validation/confirmation/local-success and the five catalogue states. Screenshots
are evidence, not automatically approved golden baselines. Detail columns stack
at 900px; navigation becomes a top rail at 640px.
