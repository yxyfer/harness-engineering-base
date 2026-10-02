export const statuses = ["Planned", "In progress", "Ready for review"] as const;
export type WorkStatus = (typeof statuses)[number];
export type WorkItem = {
  id: string;
  title: string;
  summary: string;
  status: WorkStatus;
  owner: string;
  version: number;
};

export function titleError(value: string): string | undefined {
  const length = value.trim().length;
  if (length < 3) return "Use at least 3 characters for the title.";
  if (length > 80) return "Keep the title to 80 characters or fewer.";
}
