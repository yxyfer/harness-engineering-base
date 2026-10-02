import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { WorkItemEditor } from "@/components/work-item-editor";
import { ThemeSwitch } from "@/components/theme-switch";
import { StateExample } from "@/components/state-example";
import { Button } from "@/components/ui/button";
import type { WorkItem } from "@/domain/work-item";

vi.mock("next/navigation", () => ({ useRouter: () => ({ refresh: vi.fn() }) }));
afterEach(() => {
  vi.unstubAllGlobals();
});

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

it("confirms a server save response and reset preserves the saved draft", async () => {
  const saved = {
    ...item,
    title: "Revised synthetic title",
    status: "In progress",
    version: 2,
  };
  const fetchMock = vi.fn().mockResolvedValue(Response.json({ item: saved }));
  vi.stubGlobal("fetch", fetchMock);
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.clear(screen.getByLabelText("Title"));
  await user.type(screen.getByLabelText("Title"), "Revised synthetic title");
  await user.selectOptions(screen.getByLabelText("Status"), "In progress");
  await user.click(screen.getByRole("button", { name: "Review change" }));
  expect(screen.getByRole("dialog")).toHaveAccessibleName("Save this change?");
  await user.click(screen.getByRole("button", { name: "Save change" }));
  expect(await screen.findByRole("status")).toHaveTextContent(
    "Revised synthetic title · In progress",
  );
  expect(screen.getByRole("status")).toHaveTextContent(
    "Saved to local database",
  );
  expect(fetchMock).toHaveBeenCalledWith(
    "/api/work-items/WI-101",
    expect.objectContaining({ method: "PATCH" }),
  );
  await user.type(screen.getByLabelText("Title"), " unsaved draft");
  await user.click(screen.getByRole("button", { name: "Reset draft" }));
  expect(screen.getByLabelText("Title")).toHaveValue("Revised synthetic title");
});

it("Escape cancels confirmation without saving", async () => {
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.click(screen.getByRole("button", { name: "Review change" }));
  await user.keyboard("{Escape}");
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Review change" })).toHaveFocus();
});

it("a refused server save exposes recovery without claiming success", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(Response.json({ error: "conflict" }, { status: 409 })),
  );
  const user = userEvent.setup();
  render(<WorkItemEditor item={item} />);
  await user.click(screen.getByRole("button", { name: "Review change" }));
  await user.click(screen.getByRole("button", { name: "Save change" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Changed elsewhere",
  );
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
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
