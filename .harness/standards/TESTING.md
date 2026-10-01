# Testing standard

Choose evidence in proportion to the risk and the kind of change.

- Start a bug fix with a failing reproduction that distinguishes the defect from
  the intended behaviour.
- Develop core domain behaviour test-first unless exploration is needed to learn
  the interface. Preserve the resulting behavioural test once the interface is
  understood.
- Put characterisation coverage around risky existing behaviour before a
  refactor.
- Verify observable inputs, outputs, state, and boundaries. Avoid tests that
  merely repeat implementation details or lock in call order without need.
- Keep the test pyramid appropriate to the system: many focused tests, enough
  boundary/integration tests to prove wiring, and a small golden-path smoke set.
- Use rendered or interaction evidence for visual changes. Use schema validation
  and representative fixtures for configuration-only changes.
- Make tests deterministic. Control time, randomness, and external services;
  label simulations and retain provenance for test data.

TDD is a decision rule, not a ceremony. Documentation-only edits, mechanical
formatting, disposable discovery work, and changes whose only valid proof is a
rendered or external-system observation may use more suitable evidence. Record
what was verified and any omitted path in the verification report.
