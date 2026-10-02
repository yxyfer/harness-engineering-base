import { z } from "zod";
import { login, logout, currentPrincipal } from "@/server/session";
import { safely, reply, readJson, trustedRequest } from "@/server/http";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
const credentials = z.strictObject({
  username: z.string().min(1).max(40),
  password: z.string().min(1).max(128),
});

export function POST(request: Request) {
  return safely(async () => {
    if (!trustedRequest(request, true))
      return reply({ error: "Request refused." }, 403);
    let input;
    try {
      input = credentials.safeParse(await readJson(request));
    } catch {
      return reply({ error: "Invalid request." }, 400);
    }
    if (!input.success) return reply({ error: "Invalid request." }, 400);
    const accepted = await login(input.data.username, input.data.password);
    return accepted
      ? reply({ signedIn: true })
      : reply({ error: "Sign in failed." }, 401);
  });
}

export function DELETE(request: Request) {
  return safely(async () => {
    if (!trustedRequest(request, true))
      return reply({ error: "Request refused." }, 403);
    await logout();
    return reply({ signedIn: false });
  });
}

export function GET(request: Request) {
  return safely(async () => {
    if (!trustedRequest(request))
      return reply({ error: "Request refused." }, 403);
    const principal = await currentPrincipal();
    return principal
      ? reply({ user: { id: principal.id, role: principal.role } })
      : reply({ error: "Sign in required." }, 401);
  });
}
