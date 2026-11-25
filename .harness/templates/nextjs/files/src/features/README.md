# Features

Stable capabilities a person would name. Each lives in `src/features/<name>/`
with its UI, rules, validation and data access together, and its own
`README.md`. `src/README.md` lists them.

There are none at first: platform work goes in `core` and `src/app` until the
first capability a person would name appears. Then:

```sh
npm run new-feature -- <name> --uses <other,features>
```

It creates the folder, its `index.ts` and `README.md`, adds the feature to
`src/config/features.json` and lists it in `src/README.md`.

## Rules

- A feature may import only the features listed for it in
  `src/config/features.json`; the list has no cycles (`npm run self-test`).
- A feature's public interface is its top-level modules and the entry points of
  its part folders. A folder named `internal` is private to the feature.
- A feature is made of parts. A part starts as a few files and becomes a folder,
  `npm run new-feature -- <part> --part-of <feature>`, when it arrives from an
  experiment or has grown to several files that change together. It exposes
  `index.ts` (and `server.ts` for server code), like an experiment, so promotion
  is a move, not a rewrite.
- Something new for an existing feature is a part of it, not a new feature. A
  new top-level feature needs a line in `docs/DECISIONS.md`.
- Anything off by default starts in `src/experimental`, never here.
