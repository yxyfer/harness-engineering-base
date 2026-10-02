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
| Reference work items | Repository owner | Owned deterministic seed and local SQLite | Synthetic, fictional people | Disposable local owner policy |
| Edit draft | Browser user | Local input | Synthetic demonstration | Memory until authorized save |

## Contracts

The [app contract](../examples/nextjs-app/src/domain/work-item.ts) defines id,
title, summary, status union and owner. Title previews accept trimmed length
3–80. Step 11 also runtime-validates strict server JSON and integer versions;
static/client validation alone is not the secured mutation boundary.

## Provenance

For every material output, preserve or expose the source, retrieval time,
transformation, confidence or limitations, and whether data is real, synthetic,
modelled, or simulated.

## Storage and movement

Step 11 supersedes the Step 10 preview rows above: the standalone application
uses private marked local SQLite and real synthetic sessions. Users, sessions,
versioned work items and transactional audit are stored; reset revokes sessions.
Minimal DTOs omit identity secrets and tenant fields. Fresh private/no-store
reads are not shared-cached. Generated credentials/databases are ignored local
runtime artifacts, not shipped release content. See the
[actual data contract](../examples/nextjs-app/docs/DATA.md).

## Test and demo data

Step 12's production journeys use private unique per-run storage, reset between
isolated browser contexts and remove only their owned fixture. SQL values,
versions and audit counts corroborate UI outcomes; the audit trigger exercises
real rollback/recovery outside production paths. Developer storage is preserved.

WI-101–WI-103 and fictional owners are labelled in the UI and source. Tests use
those deterministic fixtures and local server/browser runtimes only.
