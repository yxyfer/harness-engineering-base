import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { isAbsolute, join, resolve, sep } from "node:path";
import { tmpdir } from "node:os";
import { z } from "zod";

const configSchema = z.strictObject({
  kind: z.literal("workroom-disposable-v1"),
  origin: z.string().url(),
  sessionSecret: z.string().min(32),
  syntheticPassword: z.string().min(24),
});

export function safeDirectory(directory: string): string {
  if (!isAbsolute(directory) || resolve(directory) !== directory)
    throw new Error("Use a canonical disposable directory.");
  if (
    process.env.VERCEL ||
    process.env.DEPLOYMENT_ENV === "production" ||
    process.env.DATABASE_URL
  )
    throw new Error("Production/database targets are not supported.");
  const appTmp = resolve(".harness/tmp");
  const systemTmp = realpathSync(tmpdir());
  const parent = resolve(directory, "..");
  if (
    ![appTmp, systemTmp].includes(parent) ||
    !directory.slice(parent.length + 1).startsWith("workroom-")
  )
    throw new Error("Target must be a direct workroom-* disposable directory.");
  let current: string = sep;
  for (const part of directory.split(sep).filter(Boolean)) {
    current = join(current, part);
    try {
      if (lstatSync(current).isSymbolicLink())
        throw new Error("Symlink targets are refused.");
    } catch (error) {
      if (!(
        error instanceof Error &&
        "code" in error &&
        error.code === "ENOENT"
      ))
        throw error;
    }
  }
  return directory;
}

export function localRuntime() {
  const directory = safeDirectory(
    process.env.WORKROOM_DB_DIR ?? resolve(".harness/tmp/workroom-local"),
  );
  if (
    (lstatSync(directory).mode & 0o077) !== 0 ||
    (lstatSync(join(directory, "runtime.json")).mode & 0o077) !== 0
  )
    throw new Error("Disposable runtime must be private to its local owner.");
  for (const name of [
    "runtime.json",
    "data.sqlite",
    "data.sqlite-wal",
    "data.sqlite-shm",
  ]) {
    try {
      if (lstatSync(join(directory, name)).isSymbolicLink())
        throw new Error("Symlink runtime files are refused.");
    } catch (error) {
      if (!(
        error instanceof Error &&
        "code" in error &&
        error.code === "ENOENT"
      ))
        throw error;
    }
  }
  const config = configSchema.parse(
    JSON.parse(readFileSync(join(directory, "runtime.json"), "utf8")),
  );
  const origin = new URL(config.origin);
  if (
    origin.protocol !== "http:" ||
    origin.hostname !== "127.0.0.1" ||
    !origin.port ||
    origin.pathname !== "/" ||
    origin.search ||
    origin.hash ||
    origin.username ||
    origin.password
  )
    throw new Error("Only explicit loopback origins are supported.");
  return { ...config, directory };
}
