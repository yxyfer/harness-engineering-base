import assert from "node:assert/strict";
import test from "node:test";
import { pageContent } from "../app/content.js";

test("the golden path has user-visible content", () => {
  assert.equal(pageContent.title, "Harness ready");
  assert.match(pageContent.description, /Project-native/);
});
