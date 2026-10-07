# Features

Current flows; tasks hold change-specific choices, risk and verification.

| Feature | Implementation flow | Code | Evidence |
| --- | --- | --- | --- |
| Project progress | Task fields → validation → generated plan/project tables | [Records](../../.harness/bin/project_records.py), [index operations](../../.harness/bin/project_work.py) | [P004](../archive/P004-project-organisation/README.md) |
| Complete-plan archive | Validate completion/evidence → move bundle → repair links → refresh indexes; rollback ordinary write errors | [Archive](../../.harness/bin/project_work.py) | [P004 task](../archive/P004-project-organisation/tasks/P004-T001-organise-project-work.md) |
| Static checks | Config/profile selection → policies → one native check | [Check](../../.harness/bin/check), [static](../../.harness/bin/static.py) | [P002-T007](../plans/P002-quality-first-harness/tasks/P002-T007-native-static-tools.md) |
| App/kit test routing | Application runner/environment → native cases; independent kit self-test | [App test](../../.harness/bin/test), [kit test](../../.harness/bin/self-test) | [P002-T002](../plans/P002-quality-first-harness/tasks/P002-T002-application-test-routing.md) |
| Source-bound verification | Applicable controls → native reports → input identity → explicit partial/full result | [Coordinator](../../.harness/bin/verify.py) | [P002-T008](../plans/P002-quality-first-harness/tasks/P002-T008-verification-evidence.md) |
| Reference sign-in | Credentials → Argon2 → DB identity/session → sealed cookie | [Session route](../../examples/nextjs-app/src/app/api/session/route.ts), [session](../../examples/nextjs-app/src/server/session.ts) | [QH-11](../plans/P002-quality-first-harness/evidence/QH-11.md), [QH-12](../plans/P002-quality-first-harness/evidence/QH-12.md) |
| Reference save | PATCH → session/origin/schema → owner/tenant/editor policy → versioned item/audit transaction → safe response → reload | [Route](../../examples/nextjs-app/src/app/api/work-items/%5Bid%5D/route.ts), [service](../../examples/nextjs-app/src/server/work-items.ts) | [QH-12](../plans/P002-quality-first-harness/evidence/QH-12.md) |
| Save conflict/failure | Stale version → 409/reload; audit failure → rollback/retry; denial → no write | [HTTP](../../examples/nextjs-app/src/server/http.ts), [journeys](../../examples/nextjs-app/tests/navigation/journeys.test.ts) | [QH-12](../plans/P002-quality-first-harness/evidence/QH-12.md) |
| Reference UI quality | Production pages → axe/keyboard/reflow/pixel/lab checks → native evidence; human baseline approval separate | [UI tests](../../examples/nextjs-app/tests/navigation/ui-quality.test.ts) | [P002-T013](../plans/P002-quality-first-harness/tasks/P002-T013-ui-quality.md) |

Recovery and permission detail: [application
architecture](../../examples/nextjs-app/docs/ARCHITECTURE.md).
Flow arrows explain execution/data movement, not unrestricted import permission.
