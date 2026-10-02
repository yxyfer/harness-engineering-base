# Reference design

Status: current

## Experience and journeys

Workroom is a restrained list/detail workspace with explicit synthetic data.
Users sign in locally, open owned work, change title/status and confirm an
authorized save; reload retains it. Viewer roles show a real no-edit explanation.
Conflict/failure preserves the draft and offers reload/retry, never false success.
Sign-in/out use existing Button/Field controls. The catalogue shows every state
and theme. Production Chromium exercises saved reload, validation, cancellation,
repeat confirmation, denied editing and recovery without losing the draft.
No placeholder control pretends to create a work item or connect a service.

## Components and reuse

| Component      | API / variants                                | Responsibility                                  |
| -------------- | --------------------------------------------- | ----------------------------------------------- |
| Button         | primary, secondary, quiet, disabled, asChild  | Actions and semantic links                      |
| Field          | label, id, optional error, native input props | Labelled input and linked error                 |
| ConfirmDialog  | open, onOpenChange, onConfirm, onReturnFocus  | Radix trap/Escape; external form restores focus |
| ThemeSwitch    | Paper / Ink                                   | Set root token theme; no stored preference      |
| WorkItemEditor | serializable WorkItem with version            | Draft validation and authorized HTTP save       |
| StateExample   | loading, empty, error, no-access, success     | Labelled synthetic recovery examples            |

Reuse these first; add a variant before a parallel control. A genuinely new
responsibility can get a new component. Native select and semantic list/navigation
remain native: no new primitive package is needed. Radix is the only primitive
stack; the button/dialog contracts are owned adaptations of shadcn/ui patterns.
No component is duplicated per theme. See upstream
[Radix dialog](https://ui.shadcn.com/docs/components/radix/dialog) and
[semantic theming](https://ui.shadcn.com/docs/theming).

## Tokens and assets

Background, foreground, surface, muted, primary/primary-foreground, border,
accent, danger, success and ring are semantic CSS variables. Paper uses warm
light surfaces and forest accents; Ink uses navy surfaces and pale blue accents.
Typography is local Arial/Helvetica, not a network font. The wordmark and tiny
text arrows are owned text assets. No customer artwork was available.

## Responsive and accessibility intent

Desktop uses a fixed navigation rail; at 640px it reflows above content. Detail
columns stack at 900px. Verify 390px and 1440px for list/detail/catalogue in both
themes. Semantic landmarks, a skip link, labels, focus outlines, linked error
messages and Radix modal focus behavior are required. No motion is necessary.
Step 13 adds axe, explicit keyboard/focus, reflow and lab-budget assertions.
The skip target is focusable without entering sequential Tab order. State
captures wait for visible streamed content and fonts; saved captures assert the
committed heading after reload and reapply the selected theme.
Screenshots have no approved golden baseline. Forty-four pinned candidates
await human review under `tests/visual-baselines/README.md`; no AI acceptance
or automatic diff approval is used. Native pixel threshold is 0.1, allowing
zero changed pixels above that colour-distance threshold, with no masks.
Programmatic accessibility checks do not establish conformance or visual taste.
