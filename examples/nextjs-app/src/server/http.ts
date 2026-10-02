import { z } from "zod";
import { localRuntime } from "./local-runtime.ts";
import { currentPrincipal } from "./session.ts";
import { statuses } from "../domain/work-item";

export const updateSchema = z.strictObject({
  title: z
    .string()
    .trim()
    .min(3)
    .max(80)
    .refine((value) =>
      [...value].every((character) => character.charCodeAt(0) >= 32),
    ),
  status: z.enum(statuses),
  version: z.number().int().positive().max(2147483646),
});
export const idSchema = z.string().regex(/^WI-\d{3}$/);

export function reply(body: unknown, status = 200) {
  return Response.json(body, {
    status,
    headers: {
      "Cache-Control": "private, no-store",
      Vary: "Cookie",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

export async function safely(
  operation: () => Promise<Response>,
): Promise<Response> {
  try {
    return await operation();
  } catch {
    return reply({ error: "Service unavailable. Try again." }, 503);
  }
}

export function trustedRequest(request: Request, mutation = false) {
  const origin = localRuntime().origin;
  // Next may normalize Request.url to localhost internally. Authenticate the
  // actual Host and explicit Origin instead, never trust proxy host overrides.
  if (
    request.headers.get("host") !== new URL(origin).host ||
    (request.headers.has("x-forwarded-host") &&
      request.headers.get("x-forwarded-host") !== new URL(origin).host) ||
    (request.headers.has("x-forwarded-proto") &&
      request.headers.get("x-forwarded-proto") !== "http")
  )
    return false;
  if (
    mutation &&
    (request.headers.get("origin") !== origin ||
      request.headers.get("sec-fetch-site") === "cross-site")
  )
    return false;
  return true;
}

export async function readJson(request: Request): Promise<unknown> {
  if (request.headers.get("content-type")?.split(";")[0] !== "application/json")
    throw new Error("JSON required");
  if (Number(request.headers.get("content-length")) > 4096)
    throw new Error("Body too large");
  const reader = request.body?.getReader();
  if (!reader) throw new Error("Missing body");
  const chunks: Uint8Array[] = [];
  let size = 0;
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    size += value.length;
    if (size > 4096) {
      await reader.cancel();
      throw new Error("Body too large");
    }
    chunks.push(value);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8")) as unknown;
}

export async function authenticated(request: Request, mutation = false) {
  if (!trustedRequest(request, mutation))
    return { response: reply({ error: "Request refused." }, 403) };
  const principal = await currentPrincipal();
  return principal
    ? { principal }
    : { response: reply({ error: "Sign in required." }, 401) };
}
