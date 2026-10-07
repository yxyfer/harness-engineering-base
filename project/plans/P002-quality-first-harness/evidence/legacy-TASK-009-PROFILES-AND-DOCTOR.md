# TASK-009: Resolve applicable controls and readiness

- **Status:** complete locally
- **Owner:** repository owner
- **Related plan:** Step 06 of
  `project/plans/P002-quality-first-harness/README.md`

## Outcome

One shared resolution explains languages, Next.js, capabilities, context and
unsupported package scope. Doctor diagnoses prerequisites without installing,
rewriting configuration or claiming checks executed.

## Acceptance criteria

- [x] Python, TypeScript and Next.js selection is independent of tool presence.
- [x] Reviewed requirements persist; conflicting detection blocks readiness.
- [x] Unknown/unimplemented capabilities and multi-package roots are visible
  failures, not silently omitted controls or invented coverage.
- [x] Missing tools, relevant context and required unfinished context fail
  doctor; irrelevant browser/design/data requirements are not imposed on CLI.
- [x] Schema 1 remains readable without mutation; schema 2 is a reviewable
  opt-in with explicit legacy readiness/security diagnostics.
- [x] Policies, inspection and doctor use the same resolver; native tools and
  both suites/fixture smoke are exercised, with evidence in QH-06.

## Constraints and non-goals

No installer, generic policy DSL, arbitrary control plugins, automatic
migration,
security scanners, browser framework or multi-package execution aggregator.
Preserve Step 05 work. Missing prerequisites are readiness gaps, never evidence
that the applicable control can be removed. Doctor is not verification.

## Verification

Use temporary synthetic projects and real no-pip environments. Run regression
cases red first, then native checks, both core suites and applicable smokes.
Document exact compatibility, commands, source identity and limitations.
