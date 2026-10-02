import Link from "next/link";
import { listWorkItems } from "@/server/work-items";
import { currentPrincipal } from "@/server/session";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";
export default async function WorkItemsPage() {
  const principal = await currentPrincipal();
  if (!principal) redirect("/sign-in");
  const items = listWorkItems(principal);
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Overview</p>
          <h1>
            A little clarity.
            <br />A good next step.
          </h1>
          <p className="muted">
            Your owned synthetic work items. Saved changes persist locally.
          </p>
        </div>
        <span className="count">
          {items.length} <small>work items</small>
        </span>
      </div>
      <section className="panel" aria-labelledby="items-heading">
        <div className="panel-heading">
          <h2 id="items-heading">Work items</h2>
          <span className="muted">Small, shared, inspectable</span>
        </div>
        <ul className="work-list">
          {items.map((item) => (
            <li key={item.id}>
              <div>
                <span className="item-id">{item.id}</span>
                <h3>
                  <Link href={`/work-items/${item.id}`}>{item.title}</Link>
                </h3>
                <p className="muted">{item.summary}</p>
              </div>
              <div className="item-meta">
                <span className="badge">{item.status}</span>
                <span className="muted">{item.owner}</span>
                <span aria-hidden="true">↗</span>
              </div>
            </li>
          ))}
        </ul>
      </section>
      <div className="bottom-note">
        <strong>Built for the next person.</strong>
        <p>
          The same components, two themes, and explicit limits. Explore the{" "}
          <Link href="/components">component kit and state examples</Link>.
        </p>
      </div>
    </>
  );
}
