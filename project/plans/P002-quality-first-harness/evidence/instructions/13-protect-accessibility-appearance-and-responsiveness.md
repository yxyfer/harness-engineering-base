# Step 13: Protect accessibility, appearance and responsiveness

[Roadmap](../../README.md) ·
[Shared execution contract](execution.md)

Read the shared contract before using this prompt. Progress and dependencies
live in the roadmap; task acceptance and evidence remain linked there.

**Outcome:** applicable UI regressions have repeatable programmatic detection.
Use axe plus explicit keyboard/focus tests, screenshot comparison and a small
set of measured performance budgets. Do not add an AI visual judge.

Cover desktop and mobile viewports, both themes and the important states.
Exercise tab order, field labels, invalid-form announcements, dialog
focus/return, escape behaviour, visible focus, reduced motion and overflow.
Declare the browser matrix and add relevant Firefox/WebKit journeys before
claiming their support.

Capture screenshots with pinned browser/OS/fonts, locale, data and animation
settings. Generate initial candidate baselines, then obtain intentional human
acceptance before treating them as approved. Later changes produce inspectable
diffs. Never auto-update baselines after failure. Steps independent of baseline
approval may continue; visual acceptance remains incomplete until resolved.

Automated scans have
[accessibility limits](https://playwright.dev/docs/accessibility-testing), and
pixel comparisons need a
[consistent environment](https://playwright.dev/docs/test-snapshots). They do
not establish customer usefulness or visual taste.

**Done when:** seeded missing-label/focus, overflow and visual defects fail the
appropriate checks; approved screenshots compare consistently; a controlled
budget breach fails. Performance thresholds follow repeatable measurements and
stated hardware/network conditions, not an arbitrary overall Lighthouse score.

```text
Implement Step 13 only. Read project/plans/P002-quality-first-harness/README.md
and project/plans/P002-quality-first-harness/evidence/instructions/13-protect-accessibility-appearance-and-responsiveness.md.
Follow project/plans/P002-quality-first-harness/evidence/instructions/execution.md. Add programmatic axe, keyboard/focus, responsive,
visual-regression and limited performance checks to the real Next.js example.
Cover the declared viewports, themes, browsers and meaningful UI states.

Pin visual conditions and produce candidate screenshots for human acceptance;
do not impersonate approval or auto-accept failed diffs. Use actual measurements
to propose justified bundle/runtime budgets and label lab metrics accurately.
Keep assertion tolerances narrow and explain masks or exclusions.

Seed representative label/focus, overflow, appearance and budget regressions in
disposable copies and show the correct checks fail. Integrate evidence with
verify. Document remaining human acceptance and accessibility limits in
project/plans/P002-quality-first-harness/evidence/QH-13.md. Stop after the implemented scope; independent work may
continue while any actual baseline approval remains pending.
```
