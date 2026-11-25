# Experiments

One folder per prototype or feature in hardening: `src/experimental/<name>/`,
with its behaviour, UI, tests and `README.md` together. Entry points:
`index.ts(x)` for the browser and `server.ts` for routes and Server Actions.
Nothing here is reachable without an entry in
[`src/config/experiments.ts`](../config/experiments.ts) and a call site in
`src/app`. Stable code never names an experiment; that is what keeps each one
removable.

| Experiment | Destination when promoted |
| ---------- | ------------------------- |

<!-- experiments:end -->

## Who gets an experiment

One decision, `experimentActive` in
[`src/core/experiments.ts`](../core/experiments.ts):

| Person | `testers`                  | `everyone`                 | `off` |
| ------ | -------------------------- | -------------------------- | ----- |
| Tester | on by default, can opt out | on by default, can opt out | off   |
| Other  | not visible                | off by default, can opt in | off   |

- A tester is a person with a row in `experiment_testers` (user ID or email,
  lower case), or listed in `EXPERIMENT_TESTERS` (`*` for everyone, useful for
  previews). When neither applies, everyone is a tester under `next dev` and
  nobody elsewhere. To add or remove yourself, no redeploy:

  ```sql
  insert into experiment_testers (person) values ('you@example.com');
  delete from experiment_testers where person = 'you@example.com';
  ```

- Only explicit choices are stored; no choice means the default.
- `billed: true` is never on by default, not even for testers.
- `stage: 'off'` switches it off for everyone in code. In an incident,
  `EXPERIMENTS_OFF=<id>,<id>` does the same for one deployment without a code
  change (the host restarts or redeploys to read it).

## Wiring

The template wires the decision once, in `src/app`:

- [`src/app/experiments.ts`](../app/experiments.ts): `currentViewer()`, loaded
  once per request. Replace its two TODOs with the signed-in person and
  `sqlChoiceStore` from
  [`src/core/experiment-store.ts`](../core/experiment-store.ts) over the app's
  database client; apply `experimentChoicesTable()` with the app's migration
  tool.
- [`src/app/experiment-actions.ts`](../app/experiment-actions.ts): the Server
  Action Settings calls. Render `ExperimentSettings` from `src/components` with
  `experimentStates(await currentViewer())` and this action.

## Add

```sh
npm run new-experiment -- <name> --destination feature
npm run new-experiment -- <name> --destination part:<feature> [--server] [--billed]
```

It creates the folder with `index.ts` (and `server.ts`), a `README.md` stating
its destination with a "Turning it off" section, a registry entry at stage
`testers`, and a row above. Then, in `src/app` only:

1. Read `activeExperimentIds(await currentViewer())` and decide there what to
   render. A stable screen takes what it needs as a prop or slot it would accept
   from anyone; it never names an experiment.
2. Every route or Server Action that runs it calls
   `requireExperiment('<id>', await currentViewer())` next to its usual access
   check.
3. List each call site in the experiment's "Turning it off".

## Open, promote, retire

- **Open to everyone as opt-in:** set `stage: 'everyone'`.
- **Promote:** verify production behaviour and the fallback, then move the
  folder to its destination (`src/features/<name>/` with an entry in
  `src/config/features.json`, or `src/features/<feature>/<name>/` as a part),
  update callers, move its `README.md`, and delete the registry entry and its
  `requireExperiment` calls. Say in the pull request whether it becomes the
  default or stays opt-in for a stated period.
- **Retire:** delete the folder, the registry entry and every call site listed
  in its "Turning it off". Saved choices for the old ID are ignored; never reuse
  the ID. Decide what happens to data it stored, and record that decision.
- A new call that spends money and that the application starts by itself is an
  experiment first, with `billed: true`.
