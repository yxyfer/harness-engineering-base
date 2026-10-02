import { resolve } from "node:path";
import { initialize, seed } from "../src/server/setup.ts";
import { migrate } from "../src/server/database.ts";

try {
  const directory =
    process.env.WORKROOM_DB_DIR ?? resolve(".harness/tmp/workroom-local");
  const command = process.argv[2];
  if (command === "init") {
    initialize(directory);
    await seed();
  } else if (command === "migrate") migrate();
  else if (command === "seed") await seed();
  else if (command === "reset" && process.argv[3] === "--confirm-disposable")
    await seed(true);
  else
    throw new Error("Use init, migrate, seed or reset --confirm-disposable.");
  console.log(
    "Disposable database command completed; credentials remain in private runtime.json.",
  );
} catch {
  console.error(
    "Disposable database command refused or failed; review target/configuration.",
  );
  process.exitCode = 1;
}
