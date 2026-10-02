import { expect, test } from "@playwright/test";

test.beforeEach(async ({ context }) => {
  await context.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (url.hostname === "127.0.0.1" && url.port === "3100")
      return route.continue();
    return route.abort("blockedbyclient");
  });
});

test("production list, detail, confirmation and reload are honest", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByText("SYNTHETIC DATA", { exact: false }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Work items", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("link", { name: "Review the onboarding journey" })
    .click();
  await expect(page).toHaveURL(/work-items\/WI-101$/);
  await page
    .getByLabel("Title", { exact: true })
    .fill("An updated browser preview");
  await page.getByRole("button", { name: "Review change" }).click();
  await page.getByRole("button", { name: "Keep editing" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(
    page.getByRole("button", { name: "Review change" }),
  ).toBeFocused();
  await page.getByRole("button", { name: "Review change" }).click();
  await page.getByRole("button", { name: "Apply preview" }).click();
  await expect(page.getByRole("status")).toContainText("not saved");
  await page.reload();
  await expect(page.getByLabel("Title", { exact: true })).toHaveValue(
    "Review the onboarding journey",
  );
});

test("catalogue, both themes and real unknown-route recovery", async ({
  page,
}) => {
  await page.goto("/components");
  await expect(
    page.getByRole("heading", { name: "One kit. Two expressions." }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Switch theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "ink");
  await expect(
    page.getByText(
      "Synthetic permission example, not an authorization control.",
    ),
  ).toBeVisible();
  await page.getByRole("button", { name: "Switch theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "paper");
  const response = await page.goto("/work-items/unknown");
  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: "Work item not found" }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Back to work items" }).click();
  await expect(page).toHaveURL("http://127.0.0.1:3100/");
});

test("rendered routes reflow at mobile and desktop without horizontal overflow", async ({
  page,
}) => {
  for (const width of [390, 1440]) {
    await page.setViewportSize({ width, height: 1000 });
    for (const theme of ["paper", "ink"]) {
      for (const path of ["/", "/work-items/WI-101", "/components"]) {
        await page.goto(path);
        if (theme === "ink")
          await page.getByRole("button", { name: "Switch theme" }).click();
        await expect(page.locator("html")).toHaveAttribute("data-theme", theme);
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= window.innerWidth,
          ),
        ).toBe(true);
        await page.screenshot({
          path: `.harness/reports/screenshots/${width}-${theme}-${path === "/" ? "list" : path === "/components" ? "catalogue" : "detail"}.png`,
          fullPage: true,
        });
      }
    }
  }
});
