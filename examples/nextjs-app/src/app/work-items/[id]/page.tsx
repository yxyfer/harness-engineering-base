import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { findWorkItem } from "@/server/work-items";
import { currentPrincipal } from "@/server/session";
import { WorkItemEditor } from "@/components/work-item-editor";

export const dynamic = "force-dynamic";

export default async function WorkItemPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const principal = await currentPrincipal();
  if (!principal) redirect("/sign-in");
  const item = findWorkItem(principal, id);
  if (!item) notFound();
  return (
    <>
      <Link className="back-link" href="/">
        ← Work items
      </Link>
      <div className="page-heading">
        <div>
          <p className="eyebrow">{item.id} · synthetic work item</p>
          <h1>{item.title}</h1>
          <p className="muted">{item.summary}</p>
        </div>
      </div>
      <div className="detail-grid">
        <section className="panel detail">
          <h2>Saved synthetic record</h2>
          <dl>
            <dt>Owner</dt>
            <dd>{item.owner}</dd>
            <dt>Status</dt>
            <dd>
              <span className="badge">{item.status}</span>
            </dd>
            <dt>Source</dt>
            <dd>Owned synthetic fixture</dd>
          </dl>
          <p className="muted">
            Fresh authorized read from local SQLite. No shared user-data cache.
          </p>
        </section>
        {principal.role === "editor" ? (
          <WorkItemEditor key={`${item.id}-${item.version}`} item={item} />
        ) : (
          <p className="notice">Your viewer role cannot edit this record.</p>
        )}
      </div>
    </>
  );
}
