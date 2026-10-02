import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";
import { WorkItemEditor } from "@/components/work-item-editor";
import { ThemeSwitch } from "@/components/theme-switch";
import { StateExample } from "@/components/state-example";
import { Button } from "@/components/ui/button";
import type { WorkItem } from "@/domain/work-item";

const item: WorkItem = {
  id: "WI-101",
  title: "Synthetic item",
  status: "Planned",
  summary: "Test fixture",
  owner: "Synthetic owner",
  version: 1,
};

it("links title validation errors to the input without confirming", async () => {
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.clear(screen.getByLabelText("Title"));
  await user.click(screen.getByRole("button", { name: "Review change" }));
  expect(screen.getByRole("alert")).toHaveTextContent("at least 3");
  expect(screen.getByLabelText("Title")).toHaveAttribute(
    "aria-invalid",
    "true",
  );
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
});

it("confirms a browser-only preview and reset preserves that preview", async () => {
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.clear(screen.getByLabelText("Title"));
  await user.type(screen.getByLabelText("Title"), "Revised synthetic title");
  await user.selectOptions(screen.getByLabelText("Status"), "In progress");
  await user.click(screen.getByRole("button", { name: "Review change" }));
  expect(screen.getByRole("dialog")).toHaveAccessibleName(
    "Apply this preview?",
  );
  await user.click(screen.getByRole("button", { name: "Apply preview" }));
  expect(screen.getByRole("status")).toHaveTextContent(
    "Revised synthetic title · In progress",
  );
  expect(screen.getByRole("status")).toHaveTextContent("not saved");
  await user.type(screen.getByLabelText("Title"), " unsaved draft");
  await user.click(screen.getByRole("button", { name: "Reset draft" }));
  expect(screen.getByLabelText("Title")).toHaveValue("Revised synthetic title");
});

it("Escape cancels confirmation without changing the preview", async () => {
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.click(screen.getByRole("button", { name: "Review change" }));
  await user.keyboard("{Escape}");
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Review change" })).toHaveFocus();
});

it("switches both semantic themes through the same component", async () => {
  const user = userEvent.setup();
  render(<ThemeSwitch />);
  await user.click(screen.getByRole("button", { name: "Switch theme" }));
  expect(document.documentElement.dataset.theme).toBe("ink");
  expect(screen.getByRole("button")).toHaveAttribute("aria-pressed", "true");
  await user.click(screen.getByRole("button"));
  expect(document.documentElement.dataset.theme).toBe("paper");
});

it("keeps disabled button variants inert and supports semantic links", async () => {
  const user = userEvent.setup();
  render(
    <>
      <Button disabled>Disabled</Button>
      <Button asChild variant="secondary">
        <a href="/components">Catalogue</a>
      </Button>
    </>,
  );
  await user.click(screen.getByRole("button"));
  expect(screen.getByRole("button")).toBeDisabled();
  expect(screen.getByRole("link")).toHaveAttribute("href", "/components");
});

it("labels all five state examples as synthetic", () => {
  render(
    <>
      {(["loading", "empty", "error", "no-access", "success"] as const).map(
        (state) => (
          <StateExample key={state} state={state} />
        ),
      )}
    </>,
  );
  expect(screen.getAllByText(/synthetic example/)).toHaveLength(5);
  expect(screen.getByText(/not an authorization control/)).toBeInTheDocument();
});
