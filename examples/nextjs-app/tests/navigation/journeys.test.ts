import { test, expect, stored, auditFault } from "./fixtures";

test("invalid input and cancellation never change durable data", async ({
  page,
  signIn,
}) => {
  await signIn();
  const before = stored();
  await page.goto("/work-items/WI-101");
  await page.getByLabel("Title", { exact: true }).fill("a");
  await page.getByRole("button", { name: "Review change" }).click();
  await expect(
    page.getByRole("region", { name: "Edit work item" }).getByRole("alert"),
  ).toHaveText("Use at least 3 characters for the title.");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  expect(stored()).toEqual(before);
  await page.getByLabel("Title", { exact: true }).fill("Cancelled edit");
  await page.getByRole("button", { name: "Review change" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(
    page.getByRole("button", { name: "Review change" }),
  ).toBeFocused();
  expect(stored()).toEqual(before);
  await page.getByRole("button", { name: "Reset draft" }).click();
  await expect(page.getByLabel("Title", { exact: true })).toHaveValue(
    before.title,
  );
  await page.reload();
  await expect(page.getByRole("heading", { name: before.title })).toBeVisible();
  expect(stored()).toEqual(before);
});

test("repeated confirmation commits once and stale replay is rejected", async ({
  page,
  context,
  signIn,
}) => {
  await signIn();
  await page.goto("/work-items/WI-101");
  await page
    .getByLabel("Title", { exact: true })
    .fill("One durable submission");
  await page.getByRole("button", { name: "Review change" }).click();
  await page.getByRole("button", { name: "Save change" }).dblclick();
  await expect(
    page.getByRole("heading", { name: "One durable submission" }),
  ).toBeVisible();
  expect(stored()).toMatchObject({
    title: "One durable submission",
    version: 2,
    audits: 1,
  });
  const replay = await context.request.patch("/api/work-items/WI-101", {
    headers: { Origin: "http://127.0.0.1:3100" },
    data: {
      title: "One durable submission",
      status: "In progress",
      version: 1,
    },
  });
  expect(replay.status()).toBe(409);
  await page.reload();
  await expect(page.getByLabel("Title", { exact: true })).toHaveValue(
    "One durable submission",
  );
  expect(stored().audits).toBe(1);
});

test("audit dependency failure rolls back and the preserved draft recovers", async ({
  page,
  signIn,
}, info) => {
  await signIn();
  const before = stored();
  info.annotations.push({
    type: "expected-http-error",
    description:
      "/api/work-items/WI-101|Failed to load resource: the server responded with a status of 503 (Service Unavailable)",
  });
  auditFault(true);
  await page.goto("/work-items/WI-101");
  await page
    .getByLabel("Title", { exact: true })
    .fill("Recovered durable save");
  await page
    .getByLabel("Status", { exact: true })
    .selectOption("Ready for review");
  await page.getByRole("button", { name: "Review change" }).click();
  const failed = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/work-items/WI-101") &&
      response.request().method() === "PATCH",
  );
  await page.getByRole("button", { name: "Save change" }).click();
  expect((await failed).status()).toBe(503);
  await expect(
    page.getByRole("region", { name: "Edit work item" }).getByRole("alert"),
  ).toHaveText("Save failed. Reload or try again.");
  await expect(page.getByLabel("Title", { exact: true })).toHaveValue(
    "Recovered durable save",
  );
  await expect(page.getByRole("heading", { name: before.title })).toBeVisible();
  expect(stored()).toEqual(before);
  auditFault(false);
  await page.getByRole("button", { name: "Review change" }).click();
  await page.getByRole("button", { name: "Save change" }).click();
  await expect(
    page.getByRole("heading", { name: "Recovered durable save" }),
  ).toBeVisible();
  await page.reload();
  await expect(page.getByLabel("Status", { exact: true })).toHaveValue(
    "Ready for review",
  );
  expect(stored()).toMatchObject({
    title: "Recovered durable save",
    status: "Ready for review",
    version: 2,
    audits: 1,
  });
});

test("anonymous and viewer journeys deny protected editing", async ({
  page,
  context,
  signIn,
}) => {
  await page.goto("/work-items/WI-101");
  await expect(page).toHaveURL(/sign-in$/);
  await expect(
    page.getByRole("button", { name: "Review change" }),
  ).not.toBeVisible();
  await signIn("viewer");
  const before = stored("WI-103");
  await page.goto("/work-items/WI-103");
  await expect(page.getByRole("heading", { name: before.title })).toBeVisible();
  await expect(
    page.getByText("Your viewer role cannot edit this record."),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Review change" }),
  ).not.toBeVisible();
  const denied = await context.request.patch("/api/work-items/WI-103", {
    headers: { Origin: "http://127.0.0.1:3100" },
    data: { title: "Unauthorized edit", status: "Planned", version: 1 },
  });
  expect(denied.status()).toBe(403);
  expect(stored("WI-103")).toEqual(before);
});

for (const username of ["sam", "outsider"]) {
  test(`${username}: other owner or tenant cannot see or change the record`, async ({
    page,
    context,
    signIn,
  }) => {
    await signIn(username);
    const before = stored();
    await page.goto("/");
    await expect(
      page.getByRole("link", { name: before.title }),
    ).not.toBeVisible();
    await page.goto("/work-items/WI-101");
    await expect(
      page.getByRole("heading", { name: "Work item not found" }),
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: before.title }),
    ).not.toBeVisible();
    const denied = await context.request.patch("/api/work-items/WI-101", {
      headers: { Origin: "http://127.0.0.1:3100" },
      data: { title: "Unauthorized edit", status: "Planned", version: 1 },
    });
    expect(denied.status()).toBe(404);
    expect(stored()).toEqual(before);
  });
}
