# Systems

Current implementation. `unsupported` rows are deliberate visibility of gaps.

| System | Uses | Implementation | Source | State |
| --- | --- | --- | --- | --- |
| Command/configuration | POSIX sh, Python TOML | Resolve reviewed target/config, then delegate native tools | [Dispatcher](../../harness), [config](../../.harness/bin/config.py) | implemented |
| Work organisation | Python stdlib, Markdown | Validate IDs/dependencies/evidence; derive indexes; archive complete bundles | [Records](../../.harness/bin/project_records.py), [operations](../../.harness/bin/project_work.py) | implemented |
| Profiles/readiness | Reviewed stack and capabilities | Missing tools never remove required controls | [Profiles](../../.harness/bin/profiles.py), [readiness](../../.harness/bin/readiness.py) | implemented |
| Verification | Native runners, fixed adapters | Collection/outcome validation; source/config/lock identity | [Verify](../../.harness/bin/verify.py), [evidence](../../.harness/verification/README.md) | implemented |
| Security/isolation | Native scanners, external macOS policy | Explicit advisory setup; offline controls; direct-egress limits | [Security](../../.harness/security/README.md) | implemented; retained findings |
| Reference login/session | Argon2, iron-session, SQLite | Hashed synthetic credentials; sealed cookies; DB expiry/revocation/roles | [Session](../../examples/nextjs-app/src/server/session.ts) | real local synthetic boundary |
| Reference authorization | Pure owner/tenant/role policy | Server resource checks on every protected action | [Policy](../../examples/nextjs-app/src/domain/access.ts), [HTTP](../../examples/nextjs-app/src/server/http.ts) | implemented locally |
| Reference storage | Node SQLite, prepared statements | Optimistic version; atomic item/audit writes; private DTOs/reads | [Data service](../../examples/nextjs-app/src/server/work-items.ts), [database](../../examples/nextjs-app/src/server/database.ts) | disposable/local |
| Reference UI | Next.js, owned Radix kit | Server pages; small client editor; Paper/Ink semantic themes | [Components](../../examples/nextjs-app/src/components), [app map](../../examples/nextjs-app/docs/ARCHITECTURE.md) | implemented; human visual acceptance pending |
| AI calls | none | No model grading/provider calls in verification; no AI app feature implemented | [Policy](../../docs/QUALITY.md) | not applicable |
| Deployment/CI | Local production build; GitHub Actions definition | Root controls and separate package execution | [CI](../../.harness/ci/README.md) | local; remote execution/protection unverified |
| Production auth/deployment | none | No SSO/provider integration or production rollout procedure | [Limits](../../docs/SECURITY.md) | unsupported |

Each row states responsibility, technology, flow, code and implementation state.
Add systems when actually used; distinguish planned, simulated and real
boundaries.
