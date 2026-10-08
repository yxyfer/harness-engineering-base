# Engineering working agreement

Optimise for a useful result, readable code and fast feedback. Choose the mode
from the request and state it briefly. Ask only when ambiguity changes the
outcome, exposure or recovery. A mode changes the required evidence; it does not
excuse unreadable code or unsafe access to real systems.

## Working modes

### Explore

Answer one question with the smallest runnable experiment. State the question,
scope and how to discard it in a short message. Show the result early. Use an
isolated checkout and disposable data when the experiment can affect existing
work. Synthetic data is appropriate for UI exploration; testing an integration
requires the real integration in an isolated environment.

Run the available formatter and relevant lint or type checks. Demonstrate the
intended interaction or result. Add a targeted test when a known rule or defect
needs protection. Finish with a keep, change or discard recommendation and label
what was actually exercised. A formal test suite or plan document must not
become a prerequisite for trying an uncertain idea.

### Build

Turn a useful result into behaviour we intend to keep. Inspect existing owners
of state, domain rules and integration code before adding another component or
abstraction. Define a few observable acceptance examples. Cover meaningful
rules, edge cases and integration boundaries with tests, then exercise the
actual user journey. Handle loading, empty, error and retry behaviour where
relevant. Update the architecture view when responsibilities or flows change.

Promote the useful implementation and findings from Explore deliberately. Rework
shortcuts whose assumptions no longer hold; merging an experiment is not itself
proof that it is ready to maintain.

### Release

Prepare a retained feature for its intended users and environment. Add evidence
for applicable authorisation, validation, accessibility, concurrency, failure
recovery, migrations and deployment behaviour. Verify the built application in
the target class of environment. Define application recovery and database
recovery separately. Capacity work follows actual demand and consequences.

Prepare a concrete release and its verification before requesting any required
production approval. A preview deployment is evidence for the preview tested; it
does not prove that production configuration or data migration works.

## Code quality in every mode

- Use the project's native formatter, linter and type checker. Default to an
  80-character width; allow indivisible URLs and generated content. Existing
  tool settings are authoritative when more specific.
- Choose clear names and cohesive responsibilities. Review functions above 50
  lines and files above 350 maintained source lines for cohesion. Splitting code
  solely to meet a line count is not an improvement.
- Prefer the smallest coherent change. Each new file, dependency and layer
  should have a reason. Reuse an existing owner before creating a parallel one.
- Apply KISS and YAGNI. Extract shared knowledge when the common concept is
  clear. Similar syntax alone is not enough reason to create an abstraction.
- Use TDD for defects and stable core rules when it gives useful feedback. For
  an uncertain UI, try the interaction first and test retained behaviour. Tests
  should protect outcomes rather than mirror implementation details.
- Keep secrets on the server, parameterise SQL, and validate untrusted inputs.
  Real data, external users and consequential actions require safeguards from
  the first experiment that exposes them.

Stack-specific guidance lives in `.harness/standards/languages/`; native
adoption configurations live in `.harness/templates/`. P001-T002 originally
exercised them on a disposable validation app. Receiving applications install
their own dependencies and run their own quality checks and relevant journeys.
Kit checks cover kit code. These principles do not certify an implementation.

## Refactoring

Make small local improvements during the current change when their behaviour can
be checked and their scope stays coherent. Fix repeated knowledge, unclear
ownership and avoidable coupling where they obstruct the requested work.

Start with a short review after about three completed retained features, or
earlier when regressions or repeated edits reveal a structural problem. This
cadence is provisional and will be evaluated in the pilot. A review can conclude
that no refactor is needed. Larger changes need a concrete reason, affected
boundaries, expected benefit and proof that behaviour is preserved.

Keep unrelated rewrites out of the current task. Obtain the required approval
for destructive changes, production access and consequential security or data
trade-offs. Small reversible improvements do not need a separate ceremony.

## Understanding the code

Maintain three views when they add information: the application's main
responsibilities and dependencies, the flow of a feature from input to result,
and the effect of the current change. Use a small diagram with links to the
source owners. Explain what the change enables and where state or data lives.

Keep intended designs separate from current behaviour. Mark real integrations,
fixtures and simulated results clearly. An import graph can assist inspection;
it cannot establish business meaning or prove that a user journey works.

## Recovery and feedback

Git protects code history, not database writes, provider actions or deployed
configuration. An experiment needs an inventory of any resources it creates, its
data boundary and its cleanup procedure. Preserve user changes and use normal
commits and branches rather than rewriting shared history.

At completion, state the result, its proof, remaining limitations and recovery.
Use failures to improve the smallest relevant test, component or tool setting.
Add custom automation only after an observed, recurring problem justifies it.
