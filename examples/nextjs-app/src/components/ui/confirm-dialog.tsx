"use client";

import * as Dialog from "@radix-ui/react-dialog";
import { Button } from "./button";

// Radix owns trapping/Escape; the external validated form owns return focus.
export function ConfirmDialog({
  open,
  onOpenChange,
  onConfirm,
  onReturnFocus,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void;
  onReturnFocus: () => void;
}) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content
          className="dialog-content"
          onCloseAutoFocus={(event) => {
            event.preventDefault();
            onReturnFocus();
          }}
        >
          <Dialog.Title>Save this change?</Dialog.Title>
          <Dialog.Description>
            This saves the synthetic record to the local database. No live
            service or customer data is connected.
          </Dialog.Description>
          <div className="actions">
            <Dialog.Close asChild>
              <Button variant="secondary">Keep editing</Button>
            </Dialog.Close>
            <Button onClick={onConfirm}>Save change</Button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
