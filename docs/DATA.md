# Data Context

## Harness verification artifacts

Step 09 setup records public PyPI/npm native advisory data in fixed ignored
reports/advisories. Source/time, tool version, lock/manifest identity, native
collection and capture hash are required; 24h freshness is enforced. Capture
bytes join verification inputs. Sanitized findings omit secret values/snippets.
Tests generate synthetic token/advisory fixtures; live setup is separate. No
production/model integration or cloud export is introduced.

Step 08 uses local synthetic test data and native runner evidence. The versioned
contract is `.harness/verification/schema.json`; output lives in fixed ignored
`.harness/reports/verify-*/` directories. Reports hold source/config/environment
hashes, collection outcomes, commands, versions and redacted artifact identities,
not source contents. No cloud export, durable database or production dataset is
introduced. Retention/removal is local owner responsibility; no cleanup deletes
project-owned reports. Stale-input validation is provenance, not authenticity.

Status: current; synthetic reference and local verification artifacts

## Data classes

| Dataset or entity | Owner | Source | Classification | Retention |
| --- | --- | --- | --- | --- |
| Reference work items | Repository owner | Owned deterministic fixtures | Synthetic, fictional people | Committed fixture source |
| Edit draft/preview | Browser user | Local input | Synthetic demonstration | Memory only; reload resets |

## Contracts

The [app contract](../examples/nextjs-app/src/domain/work-item.ts) defines id,
title, summary, status union and owner. Title previews accept trimmed length
3–80. This is local UI validation, not a secured server mutation boundary.

## Provenance

For every material output, preserve or expose the source, retrieval time,
transformation, confidence or limitations, and whether data is real, synthetic,
modelled, or simulated.

## Storage and movement

No application database, cache/session policy or live data movement exists.
Server-rendered synthetic fixture values feed local browser state; no edit is
submitted to a server. Persistence and resource-level access belong to Step 11.

## Test and demo data

WI-101–WI-103 and fictional owners are labelled in the UI and source. Tests use
those deterministic fixtures and local server/browser runtimes only.
