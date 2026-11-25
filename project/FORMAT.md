# Document format

The plan is a tree of `README.md` files that mirrors `src/`: `src/README.md` for
the application, then one beside each feature (`src/features/<name>/`), each
part with its own folder, and each experiment (`src/experimental/<name>/`). It
describes the present and is edited in the pull request that changes the code.
There are no numbered plans.

Use these sections, in this order. Leave one out when it would be empty.

1. **Title, status line and "Start with".** A feature: "Stable feature. Uses …".
   An experiment: "Experiment, off by default. Stage: …. Destination: a feature
   of its own" or "Destination: part of `<feature>`". Then
   `Start with: \`file.ts\` (\`mainFunction\`), \`other.ts\``: the two or three
   files a newcomer should open first. The context map shows it, so an agent
   opens the right file instead of searching.
2. **What it does.** What a person can do, in a few sentences. Its first
   sentence is shown in the context map, so make it stand alone.
3. **How it works.** The path from input to result, and who owns state and
   writes. Link source files and the relevant section of `docs/ARCHITECTURE.md`
   instead of copying them.
4. **Parts.** The sub-features: name, what it is for, where it lives.
5. **Choices.** Why it is built this way, including what was rejected. Link
   `docs/DECISIONS.md` for the durable ones.
6. **Turning it off.** Experiments only: what a person sees with it off, how to
   switch it off for everyone, every call site to delete, and what happens to
   data it stored.
7. **Open work.** What is agreed and not done, most important first. Each item
   starts with its state in bold: `**Next:**`, `**In progress:**`,
   `**Waiting on <who>:**` or `**To decide:**`, then the outcome, what it
   depends on and the proof that will close it. At most five items are Next; the
   rest are To decide or deleted. Delete an item when it is done.
8. **Evidence and limits.** Which tests and journeys cover it, and what has not
   been verified. Keep local, preview and production evidence apart.

A fact is stored once, at the lowest document it belongs to. A parent's "Parts"
names its children and links them; status, open work and evidence are read in
the child. `npm run context` rolls every open item up into `context/status.md`,
grouped by state and by whom an item waits on, oldest first, with each item's
age taken from Git. `context/` is generated per checkout and not committed.

Write for someone who has not read the history: present behaviour, not the order
it was built in. No change logs; Git and the pull request keep those. Record
recovery for anything that writes data or spends money.

`npm run self-test` fails when a feature, part folder with a README, or
experiment lacks its document or its parent's link, when an open item has no
state, when a feature or experiment has no "Start with" line, when a document
has more than five Next items, or when a document exceeds its token budget. The
budget exists because every session that reads a document pays for it: move
detail down to the owning README and history to Git.
