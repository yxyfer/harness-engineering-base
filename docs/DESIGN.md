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
| Authorized local save | Owned detail editor | SQLite commit and fresh reload | Linked title error, cancel/reset/conflict |
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
dialog keyboard/focus handling. Step 13's native axe and keyboard cases do not
establish accessibility conformance or assistive-technology compatibility.
No animation is needed. Human design acceptance is separate from test results.

## Visual verification

Check list/detail/catalogue at 390px and 1440px in both themes, including edit
validation/confirmation/saved-success and the five catalogue states. Screenshots
are evidence, not automatically approved golden baselines. Detail columns stack
at 900px; navigation becomes a top rail at 640px.

Step 11 adds local sign-in/out using existing controls and a viewer explanation.
Step 12's renewed authorization allows current production Chromium journeys and
the existing two-theme/mobile/desktop reflow evidence. This is not human visual
acceptance. Step 13 adds pinned candidates and native comparisons that require
intentional human baseline acceptance; absence blocks full verify. No masks,
AI grading or automatic diff approval are used. See the app's baseline procedure
and [QH-13](../verification/QH-13.md).
