import { findWorkItem, updateWorkItem } from "@/server/work-items";
import {
  authenticated,
  safely,
  reply,
  readJson,
  idSchema,
  updateSchema,
} from "@/server/http";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
type Context = { params: Promise<{ id: string }> };

export function GET(request: Request, context: Context) {
  return safely(async () => {
    const auth = await authenticated(request);
    if (auth.response) return auth.response;
    const { id } = await context.params;
    if (!idSchema.safeParse(id).success)
      return reply({ error: "Not found." }, 404);
    const item = findWorkItem(auth.principal, id);
    return item ? reply({ item }) : reply({ error: "Not found." }, 404);
  });
}

export function PATCH(request: Request, context: Context) {
  return safely(async () => {
    const auth = await authenticated(request, true);
    if (auth.response) return auth.response;
    const { id } = await context.params;
    if (!idSchema.safeParse(id).success)
      return reply({ error: "Not found." }, 404);
    let input;
    try {
      input = updateSchema.safeParse(await readJson(request));
    } catch {
      return reply({ error: "Invalid request." }, 400);
    }
    if (!input.success) return reply({ error: "Invalid request." }, 400);
    const result = updateWorkItem(auth.principal, id, input.data);
    if (result.item) return reply({ item: result.item });
    if (result.error === "conflict")
      return reply({ error: "Changed elsewhere. Reload before saving." }, 409);
    if (result.error === "forbidden")
      return reply({ error: "Editing is not permitted." }, 403);
    return reply({ error: "Not found." }, 404);
  });
}
