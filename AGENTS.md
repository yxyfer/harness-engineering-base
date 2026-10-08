# Agent operating contract

Start at `project/README.md`; read `project/FORMAT.md`, the active plan and its
task. Before source edits, read `docs/WORKFLOW.md`, `docs/ARCHITECTURE.md`, the
four standards in `.harness/standards/`, and relevant language profiles. Read
installed framework documentation before changing framework behaviour.

Use the user's current request first, then this contract, canonical context,
accepted decisions, the active task, and existing code and tests. Stop at a
consequential unresolved ambiguity. State assumptions and record durable
choices.

## Work

- Infer Explore, Build or Release from the request and state the mode briefly.
- Inspect before editing; preserve user changes and existing project owners.
- Keep one bounded outcome in focus and define observable proof before coding.
- Keep the task brief current: intent, choice, boundaries, risk and recovery.
- Use native commands and settings from the project being changed. A non-zero
  exit is a failed check; fix it rather than weaken the gate.
- For Next.js applications, keep Next.js and React on npm's latest stable
  releases with exact tested pins. Run the version checker with the application
  directory and wire it into that app's setup and full verification. Kit checks
  verify the kit; they do not verify a consumer application.
- Update canonical context, task evidence and the plan index for durable
  changes.
- Ask before destructive changes, external publication, production access,
  consequential security trade-offs or irreversible migrations. Existing
  explicit user authorisation applies; reversible local work needs no extra
  ceremony.

## Commands

```sh
npm run setup
npm run format
npm run check
npm run check:versions -- <app-directory>
npm test
npm run self-test
npm run verify
```

Use self-tests for harness changes independently of application behaviour tests.
Run application types, behaviour tests, build and the relevant browser journey
in the receiving application. The kit uses native npm scripts; there is no
`harness` wrapper, project sync engine, installer or CI workflow or installed
demo application in this slice. Maintain the plan index directly. See
`docs/DECISIONS.md`.

Do not overwrite consumer-owned instructions or native configuration during
adoption. Work is done when the requested outcome has evidence, relevant checks
pass, durable context is current and remaining limitations are explicit.
