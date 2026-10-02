import { listWorkItems } from "@/server/work-items";
import { authenticated, safely, reply } from "@/server/http";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export function GET(request: Request) {
  return safely(async () => {
    const auth = await authenticated(request);
    if (auth.response) return auth.response;
    return reply({ items: listWorkItems(auth.principal) });
  });
}
