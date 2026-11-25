# Agent operating contract

This repository is the harness kit: the engineering contract, standards and the
Next.js application template that `npm run new-app` sets up. Start at
[README.md](README.md): what the kit holds, its open work and evidence. Before
changing the template or scripts, read `docs/WORKFLOW.md`,
`docs/ARCHITECTURE.md`, the four standards in `.harness/standards/` and the
relevant language profile.

Use the user's current request first, then this contract, accepted decisions in
`docs/DECISIONS.md` (read by heading) and existing code and tests. Stop at a
consequential unresolved ambiguity. State assumptions and record durable
choices.

## Work

- Infer Explore, Build or Release from the request and state the mode briefly.
- Inspect before editing; preserve user changes and existing project owners.
- Keep one bounded outcome in focus and define observable proof before coding.
- Use native commands. A non-zero exit is a failed check; fix it rather than
  weaken the gate.
- For Next.js applications, keep Next.js and React on npm's latest stable
  releases with exact tested pins; the template wires the version checker into
  the app's setup and verification.
- The template is generic: no product names, domain terms or data from any
  application belong in it.
- A template change needs kit proof (`npm run verify`, including the scaffold
  test) and, when it affects lint, types or build, a disposable app made with
  `npm run new-app` and verified there, then deleted.
- Update the README's open work and evidence, `docs/ARCHITECTURE.md` and
  `docs/DECISIONS.md` with durable changes.
- Ask before destructive changes, external publication, production access,
  consequential security trade-offs or irreversible migrations.

## Commands

```sh
npm run setup
npm run format
npm run check
npm test
npm run verify
npm run new-app -- <directory>
npm run check:versions -- <app-directory>
```

Kit checks verify the kit; they do not verify an application. Do not overwrite
consumer-owned instructions or configuration: `new-app` only adds missing files
to an existing app. Work is done when the outcome has evidence, relevant checks
pass, durable context is current and remaining limits are explicit.
