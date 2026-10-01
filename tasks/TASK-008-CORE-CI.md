# TASK-008: Run repaired core checks in pinned macOS CI

- **Status:** active
- **Owner:** repository owner
- **Related plan:** Step 05 of `plans/active/QUALITY_FIRST_HARNESS.md`

## Outcome

A bounded GitHub Actions workflow installs locked tools and runs actual shell,
Markdown, Python and TypeScript checks, repaired contract suites and fixtures.

## Acceptance criteria

- [ ] Runtime/action/tool versions are pinned; dependency installs are locked.
- [ ] Missing required CI tools fail; native findings are fixed without blanket
  rule disables or silently shrinking the tested source scope.
- [ ] Both core suites, fixture tests/smokes and negative controls execute.
- [ ] Failures produce useful logs; negative cases use temporary data and leave
  the source tree healthy.
- [ ] Local execution and remote execution are distinguished in QH-05.

## Non-goals

No installer, remote protection changes, later profile/doctor work or new app
foundations. Preserve all Step 04 work and consumer ownership contracts.

## Verification

Run the same CI commands locally with actual pinned tools. Preserve initial
failures and fixes, native versions, source identity and execution limits in
`verification/QH-05.md`. Stop after Step 05.
