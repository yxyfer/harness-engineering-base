# Harness architecture

## Current state

The kit holds instructions, native configuration templates, JavaScript tools and
their tests. The Next.js validation app was removed after proving the initial
settings. The root installs only its formatting and JavaScript lint
dependencies. Application runtime and dependencies belong to receiving apps.

| Responsibility                     | Current owner                                                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Agent contract                     | [AGENTS.md](../AGENTS.md)                                                                                   |
| Workflow and quality principles    | [WORKFLOW.md](WORKFLOW.md)                                                                                  |
| Engineering and language standards | [standards](../.harness/standards/BASE.md)                                                                  |
| Next.js native adoption configs    | [templates](../.harness/templates/nextjs/README.md)                                                         |
| Kit command entrypoints            | [package.json](../package.json)                                                                             |
| Shared formatting                  | [.prettierrc.json](../.prettierrc.json) and [.editorconfig](../.editorconfig)                               |
| Kit JavaScript lint                | [eslint.config.mjs](../eslint.config.mjs)                                                                   |
| Stable application versions        | [checker](../scripts/check-framework-versions.mjs) and [policy tests](../tests/framework-versions.test.mjs) |
| Disposable kit failure probes      | [native-checks.test.mjs](../tests/native-checks.test.mjs)                                                   |
| Rebuild outcomes and evidence      | [P001](../project/plans/P001-lean-harness.md)                                                               |

Kit checks cover kit formatting, JavaScript lint and behaviour tests. Native
failure probes copy only kit configuration into a unique temporary directory,
reuse the kit's installed tools, inject faults and remove that fixture.

The version checker requires an explicit installed npm app directory. It reads
that app's exact pins, lock entries and installed packages, then compares them
with npm's live stable releases. It has no write or install behaviour. Policy
tests use labelled synthetic metadata and package files; a live run needs the
actual app and registry access. Receiving apps must wire this gate into their
own setup and full verification.

No database, project scanner, installer, CI workflow, app server or `harness`
wrapper exists here. Broader application and database isolation is P001-T003
work. Prior React and browser verification remains historical evidence in P001.

## Intended operation

The harness supplies principles and settings; each application owns the code,
data, dependencies and executable verification for its product.

```mermaid
flowchart TD
  Request[Requested outcome] --> Mode[Explore, Build or Release]
  Mode --> Inspect[Inspect application owners and boundaries]
  Kit[Kit standards and native templates] --> Inspect
  Inspect --> Change[Small coherent application change]
  Change --> Native[App formatting, lint, types, versions and tests]
  Change --> Journey[App build and relevant real journey]
  Native --> Evidence[Result, evidence and limitations]
  Journey --> Evidence
  Change --> Views[Architecture and change views with source links]
  Evidence --> Decision[Keep, improve, release or discard]
```

Programming tools check precise properties; the agent explains responsibilities
and choices; the user judges whether the result is useful and understandable. An
import graph can assist inspection but cannot establish business meaning.

The initial architecture views will be maintained diagrams in the project.
P001-T004 will test whether they are sufficient. A dashboard or automatic
scanner is deferred until we observe a gap they cannot address.
