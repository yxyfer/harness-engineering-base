# Quality Context

Status: needs-project-input

## Quality bar

Define the behaviours that must be correct, resilient, understandable, and
observable for this product.

## Verification matrix

| Risk or behaviour | Verification | Command or evidence | Required gate |
| --- | --- | --- | --- |
| Core logic | Automated test | `./harness test` | Yes |
| Project conventions | Static checks | `./harness check` | Yes |
| Golden path | Smoke test | `./harness smoke` | Yes |
| Critical interface states | Visual and interaction QA | Project-specific | When applicable |

## Test strategy

Document unit, integration, contract, end-to-end, accessibility, performance, and
manual checks in proportion to actual risk.

## Known limitations

- TBD

## Release criteria

List the required evidence, approver, rollback readiness, and monitoring signals.
