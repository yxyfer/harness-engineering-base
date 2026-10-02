# Reference design

Status: current

## Experience and journeys

Workroom is a restrained list/detail workspace with explicit synthetic data.
Users open an item, change a title/status, confirm a browser-only preview and
reload to see that nothing was saved. The catalogue shows every state and theme.
No placeholder control pretends to create a work item or connect a service.

## Components and reuse

| Component      | API / variants                                | Responsibility                                  |
| -------------- | --------------------------------------------- | ----------------------------------------------- |
| Button         | primary, secondary, quiet, disabled, asChild  | Actions and semantic links                      |
| Field          | label, id, optional error, native input props | Labelled input and linked error                 |
| ConfirmDialog  | open, onOpenChange, onConfirm, onReturnFocus  | Radix trap/Escape; external form restores focus |
| ThemeSwitch    | Paper / Ink                                   | Set root token theme; no stored preference      |
| WorkItemEditor | serializable WorkItem                         | Validation and local draft/preview only         |
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
Initial interaction/overflow checks are not full accessibility certification.
Screenshots have no approved golden baseline; human brand/design acceptance
and later keyboard/contrast/accessibility coverage remain separate.
