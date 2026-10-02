import { expect, test, auditFault, stored } from "./fixtures";
import { examine, matrix, theme, requireApproval } from "./ui-quality";

for (const { width, theme: selected } of matrix) {
  const prefix = `${width}-${selected}`;
  for (const mode of ["@ui", "@visual-approved"]) {
    test(`${mode} states ${prefix}`, async ({ page, signIn }, info) => {
      if (mode === "@visual-approved") requireApproval(page);
      await page.setViewportSize({ width, height: 1000 });
      await signIn();
      for (const [name, path] of [
        ["list", "/"],
        ["detail", "/work-items/WI-101"],
        ["catalogue", "/components"],
        ["denied", "/work-items/unknown"],
        ["sign-in", "/sign-in"],
      ] as const) {
        await page.goto(path);
        await theme(page, selected);
        await examine(page, `${prefix}-${name}`, info);
      }
      await page.goto("/work-items/WI-101");
      await theme(page, selected);
      await page.getByLabel("Title", { exact: true }).fill("x");
      await page.getByRole("button", { name: "Review change" }).click();
      await expect(page.getByLabel("Title", { exact: true })).toHaveAttribute(
        "aria-invalid",
        "true",
      );
      await expect(page.getByLabel("Title", { exact: true })).toHaveAttribute(
        "aria-describedby",
        "title-error",
      );
      await expect(
        page.getByRole("region", { name: "Edit work item" }).getByRole("alert"),
      ).toHaveText("Use at least 3 characters for the title.");
      await examine(page, `${prefix}-invalid`, info);
      await page
        .getByLabel("Title", { exact: true })
        .fill("Accessible saved item");
      await page.getByRole("button", { name: "Review change" }).click();
      await expect(page.getByRole("dialog")).toBeVisible();
      await examine(page, `${prefix}-dialog`, info);
      auditFault(true);
      info.annotations.push({
        type: "expected-http-error",
        description:
          "/api/work-items/WI-101|Failed to load resource: the server responded with a status of 503 (Service Unavailable)",
      });
      await page.getByRole("button", { name: "Save change" }).click();
      await expect(
        page.getByRole("region", { name: "Edit work item" }).getByRole("alert"),
      ).toHaveText("Save failed. Reload or try again.");
      await examine(page, `${prefix}-recovery`, info);
      auditFault(false);
      await page.getByRole("button", { name: "Review change" }).click();
      await page.getByRole("button", { name: "Save change" }).click();
      await expect(
        page.getByRole("heading", { name: "Accessible saved item" }),
      ).toBeVisible();
      expect(stored().version).toBe(2);
      await page.reload();
      await expect(
        page.getByRole("heading", { name: "Accessible saved item" }),
      ).toBeVisible();
      await theme(page, selected);
      await examine(page, `${prefix}-saved`, info);
      await signIn("viewer");
      await page.goto("/work-items/WI-103");
      await theme(page, selected);
      await expect(
        page.getByText("Your viewer role cannot edit this record."),
      ).toBeVisible();
      await examine(page, `${prefix}-viewer`, info);
      await signIn("outsider");
      await page.goto("/");
      await theme(page, selected);
      await expect(page.locator(".work-list li")).toHaveCount(0);
      await examine(page, `${prefix}-empty`, info);
    });
  }

  test(`@ui keyboard ${prefix}`, async ({ page, signIn }) => {
    await signIn();
    await page.setViewportSize({ width, height: 1000 });
    await page.goto("/work-items/WI-101");
    await expect(page.locator("main h1")).toBeVisible();
    await page.keyboard.press("Tab");
    await expect(
      page.getByRole("link", { name: "Skip to content" }),
    ).toBeFocused();
    for (const control of [
      page.getByRole("link", { name: "Workroom" }),
      page.getByRole("navigation").getByRole("link", { name: "Work items" }),
      page.getByRole("link", { name: "Component kit" }),
      page.getByRole("button", { name: "Switch theme" }),
      page.getByRole("button", { name: "Sign out" }),
      page.getByRole("link", { name: "← Work items" }),
    ]) {
      await page.keyboard.press("Tab");
      await expect(control).toBeFocused();
    }
    for (let step = 0; step < 6; step++) await page.keyboard.press("Shift+Tab");
    await expect(
      page.getByRole("link", { name: "Skip to content" }),
    ).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/#main$/);
    await expect(page.getByRole("main")).toBeFocused();
    await theme(page, selected);
    const title = page.getByLabel("Title", { exact: true });
    await expect(title).toBeVisible();
    await title.focus();
    await expect(title).toBeFocused();
    await page.keyboard.press("Tab");
    await expect(page.getByLabel("Status", { exact: true })).toBeFocused();
    await page.keyboard.press("Tab");
    const review = page.getByRole("button", { name: "Review change" });
    await expect(review).toBeFocused();
    expect(
      await review.evaluate((element) => {
        const style = getComputedStyle(element);
        return (
          style.outlineStyle !== "none" && parseFloat(style.outlineWidth) >= 2
        );
      }),
      "visible keyboard focus",
    ).toBe(true);
    await page.keyboard.press("Tab");
    await expect(
      page.getByRole("button", { name: "Reset draft" }),
    ).toBeFocused();
    await page.keyboard.press("Shift+Tab");
    await page.keyboard.press("Enter");
    const keep = page.getByRole("button", { name: "Keep editing" });
    const save = page.getByRole("button", { name: "Save change" });
    await expect(keep).toBeFocused();
    await page.keyboard.press("Shift+Tab");
    await expect(save).toBeFocused();
    await page.keyboard.press("Tab");
    await expect(keep).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(page.getByRole("dialog")).not.toBeVisible();
    await expect(review).toBeFocused();
    expect(stored().version).toBe(1);
    expect(
      await page.evaluate(
        () => matchMedia("(prefers-reduced-motion: reduce)").matches,
      ),
    ).toBe(true);
    expect(await page.evaluate(() => document.getAnimations().length)).toBe(0);
  });
}
