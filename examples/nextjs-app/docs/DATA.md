# Reference data

Status: current

WI-101 through WI-103 are owned synthetic work items and fictional people.
Identifier, title, summary, status and owner are strings; status is a closed
union. No customer records are read or sent. Server fixture data is immutable.
The local editor validates title length 3–80 after trimming. State is memory
only: reload discards the preview. No database, cache policy or session exists.

## Provenance

Source: owned deterministic fixtures in `src/server/work-items.ts`, with fictional
people and no external retrieval. The preview is simulated browser behavior,
not a saved mutation. Limitations: this proves neither persistence nor resource
authorization; no customer or live dataset is included.
