"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { z } from "zod";
import {
  titleError,
  statuses,
  type WorkItem,
  type WorkStatus,
} from "@/domain/work-item";
import { Button } from "./ui/button";
import { Field } from "./ui/field";
import { ConfirmDialog } from "./ui/confirm-dialog";

export function WorkItemEditor({ item }: { item: WorkItem }) {
  const router = useRouter();
  const reviewButton = useRef<HTMLButtonElement>(null);
  const [preview, setPreview] = useState(item);
  const [title, setTitle] = useState(item.title);
  const [status, setStatus] = useState<WorkStatus>(item.status);
  const [error, setError] = useState<string>();
  const [confirming, setConfirming] = useState(false);
  const [success, setSuccess] = useState(false);
  const [saving, setSaving] = useState(false);

  async function save() {
    setConfirming(false);
    setSaving(true);
    setError(undefined);
    try {
      const response = await fetch(`/api/work-items/${item.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, status, version: preview.version }),
      });
      if (!response.ok) {
        setError(
          response.status === 409
            ? "Changed elsewhere. Reload before saving."
            : "Save failed. Reload or try again.",
        );
        return;
      }
      const parsed = z
        .object({
          item: z.object({
            id: z.string(),
            title: z.string(),
            summary: z.string(),
            status: z.enum(statuses),
            owner: z.string(),
            version: z.number().int(),
          }),
        })
        .parse(await response.json());
      setPreview(parsed.item);
      setSuccess(true);
      router.refresh();
    } catch {
      setError("Save failed. Reload or try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="panel editor" aria-label="Edit work item">
      <p className="eyebrow">Authorized local edit</p>
      <h2>Make a small change</h2>
      <p className="muted">
        Confirm to save title and status to the disposable local database.
      </p>
      <form
        noValidate
        onSubmit={(event) => {
          event.preventDefault();
          const message = titleError(title);
          setError(message);
          setSuccess(false);
          if (!message) setConfirming(true);
        }}
      >
        <Field
          id="title"
          label="Title"
          value={title}
          error={error}
          onChange={(event) => setTitle(event.target.value)}
        />
        <div className="field">
          <label htmlFor="status">Status</label>
          <select
            id="status"
            value={status}
            onChange={(event) => {
              const selected = statuses.find(
                (value) => value === event.target.value,
              );
              if (selected) setStatus(selected);
            }}
          >
            {statuses.map((value) => (
              <option key={value}>{value}</option>
            ))}
          </select>
        </div>
        <div className="actions">
          <Button ref={reviewButton} type="submit" disabled={saving}>
            Review change
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => {
              setTitle(preview.title);
              setStatus(preview.status);
              setError(undefined);
              setSuccess(false);
            }}
          >
            Reset draft
          </Button>
        </div>
      </form>
      <ConfirmDialog
        open={confirming}
        onReturnFocus={() => reviewButton.current?.focus()}
        onOpenChange={setConfirming}
        onConfirm={() => {
          void save();
        }}
      />
      {success && (
        <div className="notice notice-success" role="status">
          <strong>Saved to local database</strong>
          <p>
            {preview.title} · {preview.status}. Reload keeps this change.
          </p>
        </div>
      )}
    </section>
  );
}
