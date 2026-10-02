# Reference decisions

## Accepted decisions

- Use one owned shadcn-style Radix foundation, adapted to semantic CSS tokens.
  Radix owns dialog focus/keyboard behavior; native fields/selects need no other
  primitive stack. Existing assets were absent. No component platform is added.
- Paper and Ink share every component; themes change tokens, not page markup.
- Server Components render fixtures; browser-only state is confined to small
  interactive components. No persistence or authentication is simulated as real.
- This standalone package is checked separately; repository aggregation remains
  unsupported. Native tools and all component source remain project-owned.

## Step 11 superseding boundary decision

Replace immutable fixture/local-preview behavior with real disposable SQLite,
actual Argon2 credential sign-in and iron-session cookies referencing revocable
database sessions. This supersedes the Step 10 no-persistence/auth statement, not
the shared UI/ownership choices. Reads are per-request and private/no-store;
owner/tenant plus editor policy is pure domain logic. Version checks and audit
write commit atomically. No shared data cache or production SSO adapter is added.
Use generated local private credentials and guarded repeatable db commands.
Libraries own cryptography; server tests call real HTTP with real storage.

## Step 12 journey evidence decision

Use real production Chromium, sessions and SQLite with test-owned lifecycle
scripts. Fault the audit dependency via a real trigger, never the save operation
or a production route. Prove visible recovery and transactional data, and build
disposable save/ownership mutants to test detection. Smoke is one meaningful
journey; verify's reviewed native adapter runs the complete journey superset.
Browser errors fail except the exact deliberate 503 resource error. Unique
fixture storage and recorded server children are removed on success/interruption.
No accessibility/visual baseline or production security assurance is implied.

## Step 13 native quality and human acceptance boundary

Keep UI quality inside project-native Playwright/axe, not managed engine logic.
Chromium/macOS alone is declared; Firefox/WebKit require separate evidence.
Retain explicit keyboard checks alongside automated WCAG-tagged scans. Compare
only intentionally human-approved, condition/hash-matched PNGs with native
snapshot updating disabled. Candidates and disposable synthetic comparator
fixtures never count as approval. Missing acceptance blocks the full native
suite and verify, while independent controls can proceed. Lab budgets remain
reviewable proposals based on measured synthetic costs, not field claims.
