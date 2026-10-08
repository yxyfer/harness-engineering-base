# TypeScript React and Next.js

Read the receiving app's installed `node_modules/next/dist/docs/` before
changing framework behaviour. Resolve the Next package from that app when it is
hoisted. Match the installed Next.js and `eslint-config-next` versions. Native
starting configurations live in
[the templates](../../templates/nextjs/README.md); merge them with the
application's existing settings rather than overwriting.

- Use npm's current `latest` stable releases for Next.js, React and React DOM;
  keep exact pins and locks. React DOM must match React. Run the version checker
  with an explicit app directory and include it in that app's setup and full
  verification. It validates pins, lock entries and installed packages against
  the live public registry. Do not use canary, beta or RC versions as this
  baseline. After an upgrade, read the new installed docs and rerun the relevant
  tests and smoke. The kit itself does not install Next.js or React.
- Use strict TypeScript, explicit type imports and erasable syntax. Keep
  relative `.ts` extensions for rules executed by Node. Node does not run TSX or
  apply `tsconfig` aliases; browser tests cover React interactions.
- Run Prettier, ESLint with Next.js core web vitals and TypeScript rules, and
  `next typegen && tsc --noEmit`. Do not disable type failures during builds.
- Start from component responsibilities. Build uncertain UI with fixtures first,
  keep state minimal and derive filtered lists or counts from it.
- Use server components for appropriate reads and client components for
  interaction. Keep secrets and database access server-only. Do not route a
  server read through the application's own HTTP endpoint without a reason.
- Validate and authorise every real mutation. Pass only data the browser needs.
  Choose caching and freshness for the actual flow and installed version.
- Use semantic HTML, associated labels and visible keyboard focus. Keep CSS
  close to the feature until shared styling or components have a clear owner.

These configurations were exercised in the T002 validation app before its
removal. Every receiving application needs its own types, lint, behaviour, build
and browser evidence.
